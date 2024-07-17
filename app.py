import streamlit as st
from prompt import Prompt
import utils
import ai_api 
import os

API_ENDPOINT = "http://localhost:5000/v1"
API_KEY = "na"

st.set_page_config(page_title="AI Article Generator", layout="wide")
WORDS_PER_SENTENCE = 10

# Main title
st.title("Openplexity Pages")
story_blocks = [
    "Introduction",
    "Main",
    "Conclusion",
]
left_column, middle_column, right_column = st.columns([1, 1, 1])

with left_column:
    st.header("Generate New Article")

    story_title = st.text_input("Story Title", "The Future of Artificial Intelligence")
    generation_details = {
        "story_title": story_title,
    }
    
    for block in story_blocks:
        with st.expander(f"{block} Block", expanded=True):
            generation_details[f"story_title"] = story_title
            generation_details[f"{block}_block_title"] = st.text_input(f"{block} Block Title", f"{block}", key=f"{block}_title")
            generation_details[f"{block}_audience"] = st.selectbox("Audience", ["Students and Educators", "Tech Enthusiasts", "General Public"], key=f"{block}_audience")
            generation_details[f"{block}_style"] = st.selectbox("Style", ["Journalist", "Researcher", "Student"], key=f"{block}_style")
            generation_details[f"{block}_tone_style"] = st.selectbox("Tone", ["Professional", "Friendly"], key=f"{block}_tone_style")
            generation_details[f"{block}_word_count"] = st.slider("Word Count", min_value=100, max_value=1000, value=300, step=50, key=f"{block}_word_count")
            generation_details[f"{block}_sentence_count"] = generation_details[f"{block}_word_count"] / WORDS_PER_SENTENCE
            generation_details[f"{block}_keywords"] = st.text_input("Keywords", key=f"{block}_keywords")
            st.divider()
            generation_details[f"{block}_llm_model"] = st.selectbox("LLM Model", ["GPT-3", "GPT-4", "Claude", "Custom Model"], key=f"{block}_llm_model")
            generation_details[f"{block}_temperature"] = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1, key=f"{block}_temperature")
            generation_details[f"{block}_role"] = "user"
            generation_details[f"{block}_tone"] = generation_details[f"{block}_tone_style"]
    
    # Generate button
    if st.button("Generate Article"):
        st.success("Article generation requested!")
        for block in story_blocks:
            prompt = utils.get_formatted_prompt(generation_details, block)
            st.session_state[f"{block}_prompt"] = prompt

with middle_column:
    st.header("Debug column")
    
    for block in story_blocks:
        if f"{block}_prompt" in st.session_state:
            st.subheader(f"{block} Prompt")
            st.text_area(f"{block} Prompt", st.session_state[f"{block}_prompt"], height=300, key=f"{block}_prompt_display")
            
            if st.button(f"Run {block} Prompt"):
                with st.spinner(f"Generating {block}..."):
                    response = ai_api.run_prompt(st.session_state[f"{block}_prompt"], API_ENDPOINT, API_KEY)
                st.session_state[f"{block}_response"] = response
                st.success(f"{block} generated successfully!")
            
with right_column:
    st.header("Formatted Article")
    
    # formatted_article = f"# {story_title}\n\n"
    formatted_article = ""
    
    for block in story_blocks:
        if f"{block}_response" in st.session_state:
            formatted_article += f"## {generation_details[f'{block}_block_title']}\n\n"
            formatted_article += f"![Alt text](https://placehold.co/600x400)  \n"
            formatted_article += st.session_state[f"{block}_response"] + "\n\n"
    
    st.markdown(formatted_article)