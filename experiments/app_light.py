import streamlit as st
import toggles_helper
import prompt_helper
import time
import random
from rentry import export_to_rentry
import webbrowser
from toggle_states import toggle_states_structure
import requests
from serper_api import search_images as serper_search_images
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import base64
from pathlib import Path
from streamlit_image_select import image_select

# Define story blocks
story_blocks = ["Introduction", "Main", "Conclusion"]

st.set_page_config(page_title="AI Article Generator", layout="wide")

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
        captions=[f"Image {i+1}" for i in range(len(image_urls))],
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
                    examples = st.text_area("Paste Example of tone/style",
                                            prompt_helper.get_global_prompt_elem("exemplars"))
                    prompt_helper.update_global_prompt_elem("exemplars", examples)

# Content column
with content_column:

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

                            # Add the image at the top of the content if it exists
                            if f"{block}_image_url" in st.session_state:
                                image_html = img_to_html(st.session_state[f"{block}_image_url"])
                                display_content = image_html + formatted_response
                            else:
                                display_content = formatted_response

                            content_placeholder.markdown(f"""
                            <div class="block-content">
                                <h2>{title}</h2>
                                {display_content}
                            </div>
                            """, unsafe_allow_html=True)

                        # Store the complete response including the image in session state
                        if f"{block}_image_url" in st.session_state:
                            image_html = img_to_html(st.session_state[f"{block}_image_url"])
                            st.session_state[f"{block}_response"] = image_html + formatted_response
                        else:
                            st.session_state[f"{block}_response"] = formatted_response

                        st.success(f"{block} generated successfully!")


                # Run the function
                update_content()

            elif f"{block}_response" in st.session_state:
                # Add the image at the top of the content if it exists
                if f"{block}_image_url" in st.session_state:
                    image_html = img_to_html(st.session_state[f"{block}_image_url"])
                    display_content = image_html + st.session_state[f'{block}_response']
                else:
                    display_content = st.session_state[f'{block}_response']

                st.markdown(f"""
                <div class="block-content">
                    <h2>{prompt_helper.get_block_prompt_elem(block, 'title')}</h2>
                    {display_content}
                </div>
                """, unsafe_allow_html=True)

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