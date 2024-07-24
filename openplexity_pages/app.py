import streamlit as st
import toggles_helper
import prompt_helper
from rentry import export_to_rentry
import webbrowser
from toggle_states import toggle_states_structure
from serper_api import search_images as serper_search_images
from streamlit_image_select import image_select
import re
import html
import markdown

# Define story blocks
story_blocks = ["Introduction", "Main", "Conclusion"]

# Initialize the story blocks in session state
if 'story_blocks' not in st.session_state:
    st.session_state.story_blocks = ["Introduction", "Main", "Conclusion"]

st.set_page_config(page_title="Openplexity Pages", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&display=swap');
            
    .block-content {
        background-color: white;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .block-content h2 {
        color: #1E1E1E;
        padding-bottom: 10px;
        font-size: 28px;
        font-family: "Montserrat";
    }
    .block-content h3 {
        color: #333;
        margin-top: 20px;
        font-size: 24px;
        font-family: "Montserrat"
    }
    .block-content p {
        color: #333;
        line-height: 1.6;
        font-size: 20px;
        font-family: "Lato";
    }
    .block-image {
        max-width: 100%;
        height: auto;
        margin: 20px 0;
    }
    figure {
        margin: 0;
        text-align: center;
    }
    figcaption {
        font-style: italic;
        color: #666;
    }
    blockquote {
        background-color: #f9f9f9;
        border-left: 5px solid #ccc;
        margin: 1.5em 10px;
        padding: 0.5em 10px;
        color: #666;
        quotes: "\\201C""\\201D""\\2018""\\2019";
    }
    blockquote:before {
        color: #ccc;
        content: open-quote;
        font-size: 4em;
        line-height: 0.1em;
        margin-right: 0.25em;
        vertical-align: -0.4em;
    }
    sup {
        color: #0066cc;
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
st.markdown('<img src="https://i.imgur.com/foi8itb.png" alt="Openplexity Pages" class="centered-image">',
            unsafe_allow_html=True)

# Create three columns: Settings, Content, and Outline/Preview
settings_column, content_column, outline_column = st.columns([1, 2, 1])

# Add this at the beginning of the script, after the imports
if 'toggles_initialized' not in st.session_state:
    toggles_helper.reset_all_toggles()
    st.session_state.toggles_initialized = True

def format_markdown_content(block, content):
    # Convert Markdown to HTML
    html_content = markdown.markdown(content)
    
    # Handle custom tags
    html_content = re.sub(r'<aggregate_citations>(.*?)</aggregate_citations>', 
                          r'<div class="citations">\1</div>', 
                          html_content, 
                          flags=re.DOTALL)
    
    return html_content

def add_new_block():
    new_block_name = f"Custom Block {len(st.session_state.story_blocks) - 2}"
    st.session_state.story_blocks.append(new_block_name)
    # Initialize prompt elements for the new block
    prompt_helper.update_block_prompt_elem(new_block_name, "title", new_block_name)
    prompt_helper.update_block_prompt_elem(new_block_name, "word_count", 60)
    prompt_helper.update_block_prompt_elem(new_block_name, "keywords", "")
    prompt_helper.update_block_prompt_elem(new_block_name, "notes", "")

def remove_block(block_name):
    if block_name in st.session_state.story_blocks and len(st.session_state.story_blocks) > 3:
        st.session_state.story_blocks.remove(block_name)
        # Clean up all associated state
        for key in list(st.session_state.keys()):
            if key.startswith(f"{block_name}_"):
                del st.session_state[key]
        # Remove block from prompt_helper
        prompt_helper.remove_block_prompt_elem(block_name)
    print(f"after deletion {block_name}", prompt_helper.get_block_prompt_elem(block_name, None))

def toggle_callback(toggle):
    st.session_state[toggle] = not st.session_state.get(toggle, False)
    value = st.session_state[toggle]
    toggles_helper.update_global_toggle_state(toggle, value)
    if not value:
        prompt_helper.update_global_prompt_elem(toggle, "")


def img_to_html(img_url):
    img_html = f"<img src='{img_url}' class='img-fluid'>"
    return img_html


def search_images(image_query, num_images=6):
    with st.spinner("Searching for images..."):
        images = serper_search_images(image_query, num_images=num_images)
    if images:
        image_urls = [img['imageUrl'] for img in images]
        return image_urls
    else:
        st.warning("No images found for the given query. Please try a different search term.")
        return []


def display_image_select(block, image_urls):
    selected_image_index = image_select(
        label="Select an image",
        images=image_urls,
        captions=[f"Image {i + 1}" for i in range(len(image_urls))],
        use_container_width=True,
        return_value="index"
    )
    if selected_image_index is not None:
        selected_image_url = image_urls[selected_image_index]
        st.session_state[f"{block}_image_url"] = selected_image_url
        st.success(f"Image selected for {block}.")
    else:
        st.warning("No image selected. Please select an image to add to the article.")


with settings_column:
    st.header("Article Settings")

    settings_tab, ai_api_settings_tab, image_search_api_tab = st.tabs(
        ["Settings", "AI API Settings", "Image Search API"])

    with settings_tab:
        # Global toggles
        for toggle in toggle_states_structure["global_tgl_elem"]:
            if toggle not in st.session_state:
                st.session_state[toggle] = toggles_helper.get_global_toggle_state(toggle)

            # Convert toggle name to a more readable format
            label = " ".join(toggle.split("_")[1:]).title()

            if st.checkbox(f"Toggle {label}", key=f"toggle_{toggle}", value=st.session_state[toggle],
                           on_change=toggle_callback, args=(toggle,)):
                if toggle == "tgl_style":
                    tone_style = st.selectbox("Tone", [
                        "Professional", "Friendly", "Authoritative", "Sarcastic", "Funny",
                        "Concise", "Clear", "Engaging", "Informative", "Persuasive",
                        "Assertive", "Courteous", "Empathetic", "Emotive", "Compelling",
                        "Conversational"
                    ])
                    prompt_helper.update_global_prompt_elem("tone_style", tone_style)
                elif toggle == "tgl_target_audience":
                    audience = st.selectbox("Audience", [
                        "Students", "Tech Enthusiasts", "General Public",
                        "Children", "Young Adults", "College Students",
                        "Professionals", "Entrepreneurs", "Retirees or Seniors",
                        "Parents", "Educators", "Hobbyists",
                        "Technology Enthusiasts", "Fitness and Health Enthusiasts",
                        "Travel Enthusiasts", "Environmental Activists",
                        "Social Justice Advocates", "Personal Finance Seekers",
                        "Self-Improvement Seekers", "Specific Cultural or Ethnic Groups",
                        "LGBTQ+ Community", "People with Disabilities",
                        "People with Specific Medical Conditions", "Pet Owners",
                        "Homeowners", "Renters", "Urban Dwellers",
                        "Rural Residents", "Low-Income Individuals",
                        "High-Income Individuals", "Luxury Consumers",
                        "Bargain Hunters", "Fans of Specific Entertainment Genres"
                    ])
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
                    examples = st.text_area("Paste Example of tone/style",
                                            prompt_helper.get_global_prompt_elem("exemplars"))
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
        st.warning(
            "You need an API key from Serper API to use this feature. Get your API key at [https://serper.dev/]("
            "https://serper.dev/)")

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

    header_placeholder.markdown(f'<div class="centered-title">{st.session_state.story_title}</div>',
                                unsafe_allow_html=True)

    # Display the chat input
    story_title = st.chat_input("Story Title", key="story_title_input")
    if story_title:
        # Convert the story title to title case
        st.session_state.story_title = story_title.title()
        prompt_helper.update_global_prompt_elem("story_title", st.session_state.story_title)
        header_placeholder.markdown(f'<div class="centered-title">{st.session_state.story_title}</div>',
                                    unsafe_allow_html=True)

    # Story blocks
    for block in st.session_state.story_blocks:
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
                        try:
                            content_generator = prompt_helper.generate_api_response(block)
                            content_placeholder = output_placeholder.empty()
                            
                            # Accumulate the entire response
                            full_response = ""
                            for chunk in content_generator:
                                full_response += chunk
                                # Show a loading message or progress bar
                                content_placeholder.text("Generating content...")
                            
                            # Format the complete content
                            display_content = format_markdown_content(block, full_response)
                            
                            # Wrap the content in a block-content div
                            wrapped_content = f'<div class="block-content">{display_content}</div>'
                            
                            # Display the formatted content
                            content_placeholder.markdown(wrapped_content, unsafe_allow_html=True)
                            
                            # Store the complete response in session state
                            st.session_state[f"{block}_response"] = wrapped_content
                        except Exception as e:
                            error_message = prompt_helper.get_user_friendly_error_message(e)
                            st.error(f"An error occurred while generating content: {error_message}")
                            st.button("Retry", on_click=update_content)


                # Run the function
                update_content()

            elif f"{block}_response" in st.session_state:
                # Add the image at the top of the content if it exists
                if f"{block}_image_url" in st.session_state:
                    image_html = img_to_html(st.session_state[f"{block}_image_url"])
                    display_content = image_html + st.session_state[f'{block}_response']
                else:
                    display_content = st.session_state[f'{block}_response']

                # st.markdown(f"""
                # <div class="block-content">
                #     <h2>{prompt_helper.get_block_prompt_elem(block, 'title')}</h2>
                #     {display_content}
                # </div>
                # """, unsafe_allow_html=True)
                st.markdown(st.session_state[f'{block}_response'], unsafe_allow_html=True)

        if block not in story_blocks:
            if st.button(f"Remove {block}"):
                print(f"before deletion {block}", prompt_helper.get_block_prompt_elem(block, ""))
                remove_block(block)
                st.rerun()

        with settings_tab:
            # User input for word count
            word_count = st.slider("Word Count", 50, 200, prompt_helper.get_block_prompt_elem(block, "word_count", 60),
                                   key=f"{block}_word_count_slider")
            prompt_helper.update_block_prompt_elem(block, "word_count", word_count)  # User input sent

            # User toggle for keywords
            if st.checkbox("Toggle Keywords", key=f"{block}_tgl_keywords",
                           value=toggles_helper.get_block_toggle_state(block, "tgl_keywords")):
                toggles_helper.update_block_toggle_state(block, "tgl_keywords", True)
                # User input for keywords (only shown when toggle is activated)
                keywords = st.text_input("Keywords", prompt_helper.get_block_prompt_elem(block, "keywords"),
                                         key=f"{block}_keywords_input")
                prompt_helper.update_block_prompt_elem(block, "keywords", keywords)  # User input sent
            else:
                toggles_helper.update_block_toggle_state(block, "tgl_keywords", False)
                prompt_helper.update_block_prompt_elem(block, "keywords", "")

            # New: User toggle for custom notes
            if st.checkbox("Toggle Custom Notes", key=f"{block}_tgl_notes",
                           value=toggles_helper.get_block_toggle_state(block, "tgl_notes")):
                toggles_helper.update_block_toggle_state(block, "tgl_notes", True)
                # User input for custom notes (only shown when toggle is activated)
                notes = st.text_area("Custom Notes", prompt_helper.get_block_prompt_elem(block, "notes"),
                                     key=f"{block}_notes_input", height=150)
                prompt_helper.update_block_prompt_elem(block, "notes", notes)  # User input sent
            else:
                toggles_helper.update_block_toggle_state(block, "tgl_notes", False)
                prompt_helper.update_block_prompt_elem(block, "notes", "")

            # Debug information
            st.text_area(f"Debug: Prompt for {block}", prompt_helper.get_formatted_prompt(block), height=150)

        with image_tab:
            st.subheader(f"Image Search for {block}")
            image_query = st.chat_input(f"Enter search query for {block} image", key=f"{block}_image_query")
            if image_query:
                image_urls = search_images(image_query)
                if image_urls:
                    display_image_select(block, image_urls)

            if f"{block}_image_url" in st.session_state:
                st.image(st.session_state[f"{block}_image_url"], caption=f"Image for {block}", use_column_width=True)


    # Close the content-column div
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("Add New Block"):
            add_new_block()
            st.rerun()

# New outline_column
with outline_column:
    st.header("Overview")

    debug_tab, outline_tab, export_tab = st.tabs(["Debug", "Outline", "Export"])

    with debug_tab:
        st.subheader("Debug Information")
        st.json(prompt_helper.prompt_states)

    with outline_tab:
        st.subheader("Article Outline")
        for block in st.session_state.story_blocks:
            block_title = prompt_helper.get_block_prompt_elem(block, 'title')
            if block_title:
                st.markdown(f"- **{block}**: {block_title}")
            else:
                st.markdown(f"- **{block}**: *No title set*")

    with export_tab:
        if st.button("Export to Rentry"):
            # Generate full content here
            full_content = f"# {st.session_state.story_title}\n\n"
            for block in st.session_state.story_blocks:
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
