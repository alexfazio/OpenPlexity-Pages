import streamlit as st
import toggles_helper
import prompt_helper
import ppl_api
import time

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
    </style>
""", unsafe_allow_html=True)

# Main title
st.title("Openplexity Pages")

# Create two columns: Settings and Content
settings_column, content_column = st.columns([1, 3])

with settings_column:
    st.header("Article Settings")
    
    settings_tab, _ = st.tabs(["Settings", "Output"])
    
    with settings_tab:
        # Global settings
        try:
            default_title = prompt_helper.get_global_prompt_elem("story_title", "The Future of AI")
        except Exception as e:
            st.error(f"Error loading story title: {str(e)}")
            default_title = "The Future of AI"
        
        story_title = st.text_input("Story Title", default_title)
        prompt_helper.update_global_prompt_elem("story_title", story_title)
        
        # Global toggles
        for toggle, label in [("style", "Tone Style"), ("target_audience", "Audience"), ("persona", "Role"), ("exemplars", "Example Tone")]:
            toggle_key = f"tgl_{toggle}"
            if st.checkbox(f"Toggle {label}", key=f"toggle_{toggle}", value=toggles_helper.get_global_toggle_state(toggle_key)):
                toggles_helper.update_global_toggle_state(toggle_key, True)
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
                    example_tone = st.text_area("Example Tone", prompt_helper.get_global_prompt_elem("example_tone"))
                    prompt_helper.update_global_prompt_elem("example_tone", example_tone)
            else:
                toggles_helper.update_global_toggle_state(toggle_key, False)
                if toggle == "style":
                    prompt_helper.update_global_prompt_elem("tone_style", "")
                elif toggle == "target_audience":
                    prompt_helper.update_global_prompt_elem("audience", "")
                elif toggle == "persona":
                    prompt_helper.update_global_prompt_elem("role", "")
                elif toggle == "exemplars":
                    prompt_helper.update_global_prompt_elem("example_tone", "")

# Content column
with content_column:
    st.header(story_title)

    # Story blocks
    for block in story_blocks:
        st.subheader(f"{block} Block")
        
        output_tab, settings_tab = st.tabs(["Output", "Settings"])
        
        with output_tab:
            # Move block title and generate button to output tab
            title = st.text_input(f"Block Title", prompt_helper.get_block_prompt_elem(block, "title"), key=f"{block}_title_input")
            prompt_helper.update_block_prompt_elem(block, "title", title)
            
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
            
            # Display the generated content
            if f"{block}_response" in st.session_state:
                st.markdown(f"""
                <div class="block-content">
                    <h2>{prompt_helper.get_block_prompt_elem(block, 'title')}</h2>
                    <p>{st.session_state[f'{block}_response']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with settings_tab:
            word_count = st.slider("Word Count", 100, 1000, prompt_helper.get_block_prompt_elem(block, "word_count", 300), key=f"{block}_word_count_slider")
            prompt_helper.update_block_prompt_elem(block, "word_count", word_count)
            
            keywords = st.text_input("Keywords", prompt_helper.get_block_prompt_elem(block, "keywords"), key=f"{block}_keywords_input")
            prompt_helper.update_block_prompt_elem(block, "keywords", keywords)
            
            if st.checkbox("Toggle Keywords", key=f"{block}_tgl_keywords", value=toggles_helper.get_block_toggle_state(block, "tgl_keywords")):
                toggles_helper.update_block_toggle_state(block, "tgl_keywords", True)
            else:
                toggles_helper.update_block_toggle_state(block, "tgl_keywords", False)
                prompt_helper.update_block_prompt_elem(block, "keywords", "")

            # Debug information
            st.text_area(f"Debug: Prompt for {block}", prompt_helper.get_formatted_prompt(block), height=150)