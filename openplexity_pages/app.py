import streamlit as st
import toggles_helper
import prompt_helper
import ppl_api
import time
import random  # Add this import for the placeholder function

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
    st.session_state[f"tgl_{toggle}"] = not st.session_state.get(f"tgl_{toggle}", False)
    value = st.session_state[f"tgl_{toggle}"]
    toggles_helper.update_global_toggle_state(f"tgl_{toggle}", value)
    if not value:
        prompt_helper.update_global_prompt_elem(toggle, "")

with settings_column:
    st.header("Article Settings")
    
    settings_tab, ai_api_settings_tab, placeholder_tab = st.tabs(["Settings", "AI API Settings", ""])
    
    with settings_tab:
        # Global toggles
        for toggle, label in [("style", "Tone Style"), ("target_audience", "Audience"), ("persona", "Role"), ("exemplars", "Examples")]:
            if toggle not in st.session_state:
                st.session_state[f"tgl_{toggle}"] = toggles_helper.get_global_toggle_state(f"tgl_{toggle}")
            
            if st.checkbox(f"Toggle {label}", key=f"toggle_{toggle}", value=st.session_state[f"tgl_{toggle}"], on_change=toggle_callback, args=(toggle,)):
                if toggle == "style":
                    tone_style = st.selectbox("Tone", ["Professional", "Friendly"])
                    prompt_helper.update_global_prompt_elem("tone_style", tone_style)
                elif toggle == "target_audience":
                    audience = st.selectbox("Audience", ["Students", "Tech Enthusiasts", "General Public"])
                    prompt_helper.update_global_prompt_elem("audience", audience)
                elif toggle == "persona":
                    role = st.selectbox("Role", ["Shakespeare", "Martin", "Tolkien"])
                    prompt_helper.update_global_prompt_elem("role", role)
                elif toggle == "exemplars":
                    exemplars = st.text_area("Examples", prompt_helper.get_global_prompt_elem("exemplars"))
                    prompt_helper.update_global_prompt_elem("exemplars", exemplars)

    with ai_api_settings_tab:
        st.subheader("AI API Settings")
        
        # API provider dropdown
        api_provider = st.selectbox(
            "API Provider",
            ["OpenAI", "Anthropic", "Google", "Other"],
            key="api_provider"
        )
        
        # Model selection dropdown
        if api_provider == "OpenAI":
            model = st.selectbox(
                "Model",
                ["gpt-3.5-turbo", "gpt-4", "text-davinci-003"],
                key="openai_model"
            )
        elif api_provider == "Anthropic":
            model = st.selectbox(
                "Model",
                ["claude-v1", "claude-instant-v1"],
                key="anthropic_model"
            )
        elif api_provider == "Google":
            model = st.selectbox(
                "Model",
                ["palm-2", "text-bison-001"],
                key="google_model"
            )
        else:
            model = st.text_input("Model", key="other_model")
        
        # API key input
        api_key = st.text_input(
            "API Key",
            type="password",
            key="api_key"
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

    with placeholder_tab:
        # This tab is intentionally left empty
        pass

# Add this placeholder function at the top of the file
def search_image(query):
    # Placeholder function - replace with actual image search API later
    return f"https://placekitten.com/{random.randint(300, 500)}/{random.randint(300, 500)}"

# Content column
with content_column:
    # Move story title input and header to the top of the content column
    try:
        default_title = prompt_helper.get_global_prompt_elem("story_title", "The Future of AI")
    except Exception as e:
        st.error(f"Error loading story title: {str(e)}")
        default_title = "The Future of AI"
    
    # Display the header first
    st.header(default_title)
    
    # Then display the text input
    story_title = st.text_input("Story Title", default_title)
    prompt_helper.update_global_prompt_elem("story_title", story_title)  # User input sent

    # Update the header if the story title changes
    if story_title != default_title:
        st.header(story_title)

    # Story blocks
    for block in story_blocks:
        st.subheader(f"{block} Block")
        
        output_tab, settings_tab, image_tab = st.tabs(["Output", "Settings", "Image"])
        
        with output_tab:
            # Move block title and generate button to output tab
            # User text input for block title
            title = st.text_input(f"Block Title", prompt_helper.get_block_prompt_elem(block, "title"), key=f"{block}_title_input")
            prompt_helper.update_block_prompt_elem(block, "title", title)  # User input sent
            
            if st.button(f"Generate {block}", key=f"generate_{block}"):
                prompt = prompt_helper.get_formatted_prompt(block)
                
                # Simulate streaming output
                output_placeholder = st.empty()
                full_response = ""
                for chunk in ppl_api.ppl_query_api_stream(prompt):
                    full_response += chunk
                    output_placeholder.markdown(f"""
                    <div class="block-content">
                        <h2>{title}</h2>
                        <p>{full_response}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(0.05)  # Adjust this value to control the streaming speed
                
                st.session_state[f"{block}_response"] = full_response
                st.success(f"{block} generated successfully!")
            
            # Display the generated content only if it hasn't been displayed during generation
            elif f"{block}_response" in st.session_state:
                st.markdown(f"""
                <div class="block-content">
                    <h2>{prompt_helper.get_block_prompt_elem(block, 'title')}</h2>
                    <p>{st.session_state[f'{block}_response']}</p>
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

            # Debug information
            st.text_area(f"Debug: Prompt for {block}", prompt_helper.get_formatted_prompt(block), height=150)

        with image_tab:
            st.subheader(f"Image Search for {block}")
            image_query = st.text_input(f"Search query for {block} image", key=f"{block}_image_query")
            if st.button(f"Search Image for {block}", key=f"{block}_search_image"):
                image_url = search_image(image_query)
                st.image(image_url, caption=f"Image for {block}", use_column_width=True)
                st.session_state[f"{block}_image_url"] = image_url
            elif f"{block}_image_url" in st.session_state:
                st.image(st.session_state[f"{block}_image_url"], caption=f"Image for {block}", use_column_width=True)

# New outline_column
with outline_column:
    st.header("Overview")
    
    outline_tab, preview_tab = st.tabs(["Outline", "Preview/Export"])
    
    with outline_tab:
        st.subheader("Article Outline")
        for block in story_blocks:
            block_title = prompt_helper.get_block_prompt_elem(block, 'title')
            if block_title:
                st.markdown(f"- **{block}**: {block_title}")
            else:
                st.markdown(f"- **{block}**: *No title set*")
    
    with preview_tab:
        if st.button("Preview"):
            st.markdown("### Article Preview")
            for block in story_blocks:
                if f"{block}_response" in st.session_state:
                    st.markdown(f"#### {prompt_helper.get_block_prompt_elem(block, 'title')}")
                    st.markdown(st.session_state[f"{block}_response"])
                else:
                    st.warning(f"{block} not generated yet.")
        
        if st.button("Export"):
            # Implement export functionality here
            st.success("Export functionality not implemented yet.")