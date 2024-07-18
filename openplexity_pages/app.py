import streamlit as st
from toggles_state import global_toggle_states, block_toggle_states
from prompts import global_prompt_elements, block_prompt_elements, get_formatted_prompt
import ppl_api

# Define story blocks
story_blocks = ["Introduction", "Main", "Conclusion"]

# Initialize prompts in session state
if "prompts_initialized" not in st.session_state:
    for block in story_blocks:
        st.session_state[f"{block}_prompt"] = "Prompt will appear here..."
    st.session_state["prompts_initialized"] = True

st.set_page_config(page_title="AI Article Generator", layout="wide")
WORDS_PER_SENTENCE = 10

# Main title
st.title("Openplexity Pages")

def update_prompt(block):
    prompt = get_formatted_prompt(global_toggle_states, block_toggle_states[block], global_prompt_elements, block_prompt_elements[block])
    st.session_state[f"{block}_prompt"] = prompt

left_column, middle_column, right_column = st.columns([1, 1, 1])

with left_column:
    st.header("Generate New Article")

    # Global settings
    global_prompt_elements["story_title"] = st.text_input("Story Title", "The Future of AI", on_change=lambda: [update_prompt(block) for block in story_blocks])
    
    # Global toggles
    for toggle, label in [("style", "Tone Style"), ("target_audience", "Audience"), ("persona", "Role"), ("exemplars", "Example Tone")]:
        global_toggle_states[f"tgl_{toggle}"] = st.checkbox(f"Toggle {label}", key=f"toggle_{toggle}", on_change=lambda: [update_prompt(block) for block in story_blocks])
        if global_toggle_states[f"tgl_{toggle}"]:
            if toggle == "style":
                global_prompt_elements["tone_style"] = st.selectbox("Tone", ["Professional", "Friendly"], on_change=lambda: [update_prompt(block) for block in story_blocks])
            elif toggle == "target_audience":
                global_prompt_elements["audience"] = st.selectbox("Audience", ["Students", "Tech Enthusiasts", "General Public"], on_change=lambda: [update_prompt(block) for block in story_blocks])
            elif toggle == "persona":
                global_prompt_elements["role"] = st.selectbox("Role", ["Shakespeare", "Martin", "Tolkien"], on_change=lambda: [update_prompt(block) for block in story_blocks])
            elif toggle == "exemplars":
                global_prompt_elements["example_tone"] = st.text_area("Example Tone", on_change=lambda: [update_prompt(block) for block in story_blocks])

    # Story blocks
    for block in story_blocks:
        with st.expander(f"{block} Block", expanded=True):
            block_prompt_elements[block] = {
                "title": st.text_input(f"{block} Block Title", block, key=f"{block}_title", on_change=lambda b=block: update_prompt(b)),
                "word_count": st.slider("Word Count", 100, 1000, 300, 50, key=f"{block}_word_count", on_change=lambda b=block: update_prompt(b)),
                "sentence_count": lambda: block_prompt_elements[block]["word_count"] / WORDS_PER_SENTENCE,
                "keywords": st.text_input("Keywords", key=f"{block}_keywords", on_change=lambda b=block: update_prompt(b)),
                "llm_model": st.selectbox("LLM Model", ["Mistral", "GPT-3", "GPT-4", "Claude"], key=f"{block}_llm_model", on_change=lambda b=block: update_prompt(b)),
                "temperature": st.slider("Temperature", 0.0, 1.0, 0.7, 0.1, key=f"{block}_temperature", on_change=lambda b=block: update_prompt(b))
            }
            block_toggle_states[block] = {
                "tgl_keywords": st.checkbox("Toggle Keywords", key=f"{block}_tgl_keywords", on_change=lambda b=block: update_prompt(b))
            }

    # Generate button
    if st.button("Generate Article"):
        st.success("Article generation requested!")
        for block in story_blocks:
            with st.spinner(f"Generating {block}..."):
                response = ppl_api.ppl_query_api(st.session_state[f"{block}_prompt"])
            st.session_state[f"{block}_response"] = response
            st.success(f"{block} generated successfully!")

with middle_column:
    st.header("Debug column")

    for block in story_blocks:
        st.subheader(f"{block} Prompt")
        prompt = st.session_state.get(f"{block}_prompt", "Prompt will appear here...")
        st.text_area(f"{block} Prompt", prompt, height=300, key=f"{block}_prompt_display", disabled=True)
        
        if st.button(f"Run {block} Prompt"):
            with st.spinner(f"Generating {block}..."):
                response = ppl_api.ppl_query_api(prompt)
            st.session_state[f"{block}_response"] = response
            st.success(f"{block} generated successfully!")

with right_column:
    st.header("Formatted Article")

    formatted_article = ""

    for block in story_blocks:
        if f"{block}_response" in st.session_state:
            formatted_article += f"## {block_prompt_elements[block]['title']}\n\n"
            formatted_article += f"![Alt text](https://placehold.co/600x400)  \n"
            formatted_article += st.session_state[f"{block}_response"] + "\n\n"

    st.markdown(formatted_article)