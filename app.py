import streamlit as st
from prompt import Prompt
import utils
import ai_api 
import os

# Get API_KEY from .env file
# OPENAI_API_ENDPOINT = os.getenv("OPENAI_API_ENDPOINT")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

OPENAI_API_ENDPOINT = "http://localhost:5000/v1"
OPENAI_API_KEY = "na"



# Set page title and layout
st.set_page_config(page_title="AI Article Generator", layout="wide")

# Main title
st.title("Openplexity Pages")
story_blocks = [
    "Introduction",
    "Main",
    "Conclusion",
]
left_column, right_column = st.columns([1, 1])

# Left column: Inputs for article generation
with left_column:
    st.header("Generate New Article")

    story_title = st.text_input("Story Title", "The Future of Artificial Intelligence")
    generation_details = {
        "story_title": story_title,
    }
    
    # Create three collapsible story blocks
    for block in story_blocks:
        with st.expander(f"{block} Block", expanded=True):
            generation_details[f"{block.lower()}_block_title"] = st.text_input(f"{block} Block Title", f"Sample {block} Title", key=f"{block.lower()}_title")
            generation_details[f"{block.lower()}_audience"] = st.selectbox("Audience", ["Students and Educators", "Tech Enthusiasts", "General Public"], key=f"{block.lower()}_audience")
            generation_details[f"{block.lower()}_persona"] = st.selectbox("Persona", ["Journalist", "Researcher", "Student"], key=f"{block.lower()}_persona")
            generation_details[f"{block.lower()}_word_count"] = st.slider("Word Count", min_value=100, max_value=1000, value=300, step=50, key=f"{block.lower()}_word_count")
            generation_details[f"{block.lower()}_key_points"] = st.text_area("Key Points to Include (one per line)", key=f"{block.lower()}_key_points")
            st.divider()
            generation_details[f"{block.lower()}_llm_model"] = st.selectbox("LLM Model", ["GPT-3", "GPT-4", "Claude", "Custom Model"], key=f"{block.lower()}_llm_model")
            generation_details[f"{block.lower()}_temperature"] = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1, key=f"{block.lower()}_temperature")
    
    # Generate button
    if st.button("Generate Article"):
        st.success("Article generation requested! (This is a placeholder - actual generation not implemented)")
        for block in story_blocks:
            prompt = utils.get_formatted_prompt(generation_details, block)
            st.session_state[f"{block.lower()}_prompt"] = prompt

# Right column: Display generated articles and prompts
with right_column:
    st.header("Generated Articles")
    
    for block in story_blocks:
        if f"{block.lower()}_prompt" in st.session_state:
            st.subheader(f"{block} Prompt")
            st.text_area(f"{block} Prompt", st.session_state[f"{block.lower()}_prompt"], height=300, key=f"{block.lower()}_prompt_display")
            
            if st.button(f"Run {block} Prompt"):
                with st.spinner(f"Generating {block}..."):
                    response = ai_api.run_prompt(st.session_state[f"{block.lower()}_prompt"], OPENAI_API_ENDPOINT, OPENAI_API_KEY)
                st.session_state[f"{block.lower()}_response"] = response
                st.success(f"{block} generated successfully!")
            
            if f"{block.lower()}_response" in st.session_state:
                st.subheader(f"{block} Response")
                st.text_area(f"{block} Response", st.session_state[f"{block.lower()}_response"], height=300, key=f"{block.lower()}_response_display")