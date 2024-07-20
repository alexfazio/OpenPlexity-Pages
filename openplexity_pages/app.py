import streamlit as st
import toggles_helper
import prompt_helper
import time
import random
from rentry import export_to_rentry
import webbrowser
from toggle_states import toggle_states_structure
import requests
from serper_api import search_images
from PIL import Image, UnidentifiedImageError
from io import BytesIO

# Define story blocks
story_blocks = ["Introduction", "Main", "Conclusion"]

st.set_page_config(page_title="AI Article Generator", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .block-content {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .block-content h2 {
        color: #1E1E1E;
        border-bottom: 2px solid #4CAF50;
        padding-bottom: 10px;
    }
    .block-content p {
        color: #333;
        line-height: 1.6;
    }
    .centered-image {
        display: block;
        margin-left: auto;
        margin-right: auto;
        max-width: 66.67%;  /* Matches the width of the center column */
        height: auto;
        padding: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Place the image at the top of the page
st.markdown('<img src="https://i.imgur.com/foi8itb.png" alt="Openplexity Pages" class="centered-image">', unsafe_allow_html=True)

# Create three columns: Settings, Content, and Outline/Preview
settings_column, content_column, outline_column = st.columns([1, 2, 1])

# Add this at the beginning of the script, after the imports
if 'toggles_initialized' not in st.session_state:
    toggles_helper.reset_all_toggles()
    st.session_state.toggles_initialized = True

def toggle_callback(toggle):
    st.session_state[toggle] = not st.session_state.get(toggle, False)
    value = st.session_state[toggle]
    toggles_helper.update_global_toggle_state(toggle, value)
    if not value:
        prompt_helper.update_global_prompt_elem(toggle, "")

def display_image_grid(images, num_cols=3):
    cols = st.columns(num_cols)
    selected_images = []

    for i, image in enumerate(images):
        with cols[i % num_cols]:
            try:
                response = requests.get(image['imageUrl'], timeout=5)
                response.raise_for_status()
                img = Image.open(BytesIO(response.content))
                st.image(img, use_column_width=True)
                if st.checkbox(f"Select Image {i+1}", key=f"checkbox_{i}"):
                    selected_images.append(image['imageUrl'])
            except (requests.RequestException, UnidentifiedImageError, IOError) as e:
                st.error(f"Error loading image {i+1}: {str(e)}")
                continue
    
    return selected_images

with settings_column:
    st.header("Article Settings")
    
    settings_tab, ai_api_settings_tab, image_search_api_tab = st.tabs(["Settings", "AI API Settings", "Image Search API"])
    
    with settings_tab:
        # Global toggles
        for toggle in toggle_states_structure["global_tgl_elem"]:
            if toggle not in st.session_state:
                st.session_state[toggle] = toggles_helper.get_global_toggle_state(toggle)
            
            # Convert toggle name to a more readable format
            label = " ".join(toggle.split("_")[1:]).title()
            
            if st.checkbox(f"Toggle {label}", key=f"toggle_{toggle}", value=st.session_state[toggle], on_change=toggle_callback, args=(toggle,)):
                if toggle == "tgl_style":
                    tone_style = st.selectbox("Tone", ["Professional", "Friendly"])
                    prompt_helper.update_global_prompt_elem("tone_style", tone_style)
                elif toggle == "tgl_target_audience":
                    audience = st.selectbox("Audience", ["Students", "Tech Enthusiasts", "General Public"])
                    prompt_helper.update_global_prompt_elem("audience", audience)
                elif toggle == "tgl_persona":
                    col1, col2 = st.columns(2)
                    with col1:
                        first_name = st.text_input("First Name", key="persona_first_name")
                    with col2:
                        last_name = st.text_input("Last Name", key="persona_last_name")
                    if first_name and last_name:
                        prompt_helper.update_global_prompt_elem("persona_first_name", first_name)
                        prompt_helper.update_global_prompt_elem("persona_last_name", last_name)
                elif toggle == "tgl_exemplars":
                    examples = st.text_area("Paste Example of tone/style", prompt_helper.get_global_prompt_elem("exemplars"))
                    prompt_helper.update_global_prompt_elem("exemplars", examples)

    with ai_api_settings_tab:
        st.subheader("AI API Settings")
        
        # API provider dropdown
        api_provider = st.selectbox(
            "API Provider",
            ["Perplexity", "Google"],
            key="api_provider"
        )
        
        # Model selection dropdown
        if api_provider == "Perplexity":
            model = st.selectbox(
                "Model",
                ["llama-3-sonar-large-32k-online", "llama-3-sonar-small-32k-online"],
                key="perplexity_model"
            )
            # API key input for Perplexity
            api_key = st.text_input(
                "API Key",
                type="password",
                key="perplexity_api_key"
            )
        elif api_provider == "Google":
            model = st.selectbox(
                "Model",
                ["gemini-1.5-flash-001", "gemini-1.5-pro-001", "gemini-1.0-pro-002", "gemini-1.0-pro-001"],
                key="google_model"
            )
            # Service account file upload for Google
            service_account_file = st.file_uploader(
                "Upload Service Account JSON File",
                type=["json"],
                key="google_service_account_file"
            )
        
        # Model temperature slider
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1,
            key="model_temperature"
        )


        # Top K slider
        top_k = st.slider(
            "Top K",
            min_value=1,
            max_value=100,
            value=50,
            step=1,
            key="top_k"
        )

        # Top P slider
        top_p = st.slider(
            "Top P",
            min_value=0.0,
            max_value=1.0,
            value=1.0,
            step=0.01,
            key="top_p"
        )

        # Frequency penalty slider
        frequency_penalty = st.slider(
            "Frequency Penalty",
            min_value=-2.0,
            max_value=2.0,
            value=0.0,
            step=0.1,
            key="frequency_penalty"
        )

        # Presence penalty slider
        presence_penalty = st.slider(
            "Presence Penalty",
            min_value=-2.0,
            max_value=2.0,
            value=0.0,
            step=0.1,
            key="presence_penalty"
        )

        # Max Tokens dropdown
        max_tokens_options = {
            "256": 256,
            "512": 512,
            "1K": 1024,
            "2K": 2048,
            "4K": 4096,
            "8K": 8192
        }
        max_tokens = st.selectbox(
            "Max Tokens",
            options=list(max_tokens_options.keys()),
            format_func=lambda x: x,
            key="max_tokens"
        )
        max_tokens_value = max_tokens_options[max_tokens]

    with image_search_api_tab:
        st.subheader("Serper API Settings")
        
        # Warning message moved below the API key input
        st.warning("You need an API key from Serper API to use this feature. Get your API key at [https://serper.dev/](https://serper.dev/)")
        
        # Add any additional Serper API settings here if needed

# Content column
with content_column:
    # Add a div with class 'content-column' to target the CSS
    st.markdown('<div class="content-column">', unsafe_allow_html=True)
    
    # Add custom CSS for centering the title
    st.markdown("""
        <style>
        .centered-title {
            text-align: center;
            padding: 10px 0;
            font-size: 2.5em;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Create a placeholder for the centered header
    header_placeholder = st.empty()
    
    # Display the default title or the user-provided title
    if 'story_title' not in st.session_state:
        st.session_state.story_title = "Create a New Article"
    
    header_placeholder.markdown(f'<div class="centered-title">{st.session_state.story_title}</div>', unsafe_allow_html=True)
    
    # Display the chat input
    story_title = st.chat_input("Story Title", key="story_title_input")
    if story_title:
        # Convert the story title to title case
        st.session_state.story_title = story_title.title()
        prompt_helper.update_global_prompt_elem("story_title", st.session_state.story_title)
        header_placeholder.markdown(f'<div class="centered-title">{st.session_state.story_title}</div>', unsafe_allow_html=True)
    
    # Story blocks
    for block in story_blocks:
        output_tab, settings_tab, image_tab = st.tabs(["Output", "Settings", "Image"])
        
        with output_tab:
            title = st.chat_input(f"{block} Title", key=f"{block}_title_input")
            
            if title:
                prompt_helper.update_block_prompt_elem(block, "title", title)
                
                # Create a placeholder for the streamed content
                output_placeholder = st.empty()
                
                # Function to update the placeholder with streamed content
                def update_content():
                    with st.spinner(f"Generating {block} content..."):
                        content_generator = prompt_helper.generate_content(block)
                        
                        # Create a placeholder for the streamed content
                        content_placeholder = output_placeholder.empty()
                        
                        formatted_response = ""
                        for chunk in content_generator:
                            formatted_response += chunk
                            content_placeholder.markdown(f"""
                            <div class="block-content">
                                <h2>{title}</h2>
                                {formatted_response}
                            </div>
                            """, unsafe_allow_html=True)
                        
                    st.session_state[f"{block}_response"] = formatted_response
                    st.success(f"{block} generated successfully!")

                # Run the function
                update_content()
            
            elif f"{block}_response" in st.session_state:
                st.markdown(f"""
                <div class="block-content">
                    <h2>{prompt_helper.get_block_prompt_elem(block, 'title')}</h2>
                    {st.session_state[f'{block}_response']}
                </div>
                """, unsafe_allow_html=True)
        
        with settings_tab:
            # User input for word count
            word_count = st.slider("Word Count", 50, 200, prompt_helper.get_block_prompt_elem(block, "word_count", 60), key=f"{block}_word_count_slider")
            prompt_helper.update_block_prompt_elem(block, "word_count", word_count)  # User input sent
            
            # User toggle for keywords
            if st.checkbox("Toggle Keywords", key=f"{block}_tgl_keywords", value=toggles_helper.get_block_toggle_state(block, "tgl_keywords")):
                toggles_helper.update_block_toggle_state(block, "tgl_keywords", True)
                # User input for keywords (only shown when toggle is activated)
                keywords = st.text_input("Keywords", prompt_helper.get_block_prompt_elem(block, "keywords"), key=f"{block}_keywords_input")
                prompt_helper.update_block_prompt_elem(block, "keywords", keywords)  # User input sent
            else:
                toggles_helper.update_block_toggle_state(block, "tgl_keywords", False)
                prompt_helper.update_block_prompt_elem(block, "keywords", "")

            # New: User toggle for custom notes
            if st.checkbox("Toggle Custom Notes", key=f"{block}_tgl_notes", value=toggles_helper.get_block_toggle_state(block, "tgl_notes")):
                toggles_helper.update_block_toggle_state(block, "tgl_notes", True)
                # User input for custom notes (only shown when toggle is activated)
                notes = st.text_area("Custom Notes", prompt_helper.get_block_prompt_elem(block, "notes"), key=f"{block}_notes_input", height=150)
                prompt_helper.update_block_prompt_elem(block, "notes", notes)  # User input sent
            else:
                toggles_helper.update_block_toggle_state(block, "tgl_notes", False)
                prompt_helper.update_block_prompt_elem(block, "notes", "")

            # Debug information
            st.text_area(f"Debug: Prompt for {block}", prompt_helper.get_formatted_prompt(block), height=150)

        with image_tab:
            st.subheader(f"Image Search for {block}")
            image_query = st.chat_input(f"Enter search query for {block} image", key=f"{block}_image_query")
            if image_query:  # This will trigger when the user submits the chat input
                with st.spinner("Searching for images..."):
                    images = search_images(image_query)
                if images:
                    selected_images = display_image_grid(images)
                    if selected_images:
                        st.subheader("Selected Images:")
                        for img_url in selected_images:
                            try:
                                st.image(img_url, caption=f"Selected Image for {block}", use_column_width=True)
                                st.session_state[f"{block}_image_url"] = img_url
                            except Exception as e:
                                st.error(f"Error displaying selected image: {str(e)}")
                else:
                    st.warning("No images found for the given query. Please try a different search term.")
            elif f"{block}_image_url" in st.session_state:
                try:
                    st.image(st.session_state[f"{block}_image_url"], caption=f"Image for {block}", use_column_width=True)
                except Exception as e:
                    st.error(f"Error displaying saved image: {str(e)}")
                    del st.session_state[f"{block}_image_url"]

    # Close the content-column div
    st.markdown('</div>', unsafe_allow_html=True)

# New outline_column
with outline_column:
    st.header("Overview")
    
    outline_tab, export_tab = st.tabs(["Outline", "Export"])
    
    with outline_tab:
        st.subheader("Article Outline")
        for block in story_blocks:
            block_title = prompt_helper.get_block_prompt_elem(block, 'title')
            if block_title:
                st.markdown(f"- **{block}**: {block_title}")
            else:
                st.markdown(f"- **{block}**: *No title set*")
    
    with export_tab:
        if st.button("Export to Rentry"):
            # Generate full content here
            full_content = f"# {st.session_state.story_title}\n\n"
            for block in story_blocks:
                if f"{block}_response" in st.session_state:
                    block_title = prompt_helper.get_block_prompt_elem(block, 'title')
                    full_content += f"## {block_title}\n\n"
                    full_content += f"{st.session_state[f'{block}_response']}\n\n"
                else:
                    st.warning(f"{block} not generated yet.")
                    full_content += f"## {block}\n\n*Content not generated*\n\n"

            rentry_url, edit_code = export_to_rentry(full_content)
            if rentry_url:
                st.success(f"Successfully exported to Rentry. URL: {rentry_url}")
                st.info(f"Edit code: {edit_code}")
                
                # Open the Rentry URL in a new browser tab
                webbrowser.open_new_tab(rentry_url)
                
                # Provide a manual link in case automatic opening fails
                st.markdown(f"If the page doesn't open automatically, [click here to view your Rentry]({rentry_url})")
            else:
                st.error("Failed to export to Rentry. Please try again.")