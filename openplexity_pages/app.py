import streamlit as st
from prompts import prompt_elements
import ppl_api
import os

st.set_page_config(page_title="AI Article Generator", layout="wide")
WORDS_PER_SENTENCE = 10

# Main title
st.title("Openplexity Pages")
story_blocks = [
    "Zero",
    "One",
    "Two",
]
left_column, middle_column, right_column = st.columns([1, 1, 1])

with left_column:
    st.header("Generate New Article")

    story_title = st.text_input("Story Title",
                                "The Future of Artificial Intelligence")
    tgl_global_states = {
        "story_title": story_title,
    }

    # Article settings
    tgl_global_states[f"tgl_style"] = st.checkbox("Toggle Tone Style",
                                                  key="tgl_style")
    if tgl_global_states[f"tgl_style"]:
        tgl_global_states[f"tone_style"] = st.selectbox(
            "Tone", ["Professional", "Friendly"], key=f"tone_style")
    else:
        tgl_global_states[f"tone_style"] = None

    tgl_global_states[f"tgl_target_audience"] = st.checkbox(
        "Toggle Audience", key="tgl_target_audience")
    if tgl_global_states[f"tgl_target_audience"]:
        tgl_global_states[f"audience"] = st.selectbox(
            "Audience",
            ["Students and Educators", "Tech Enthusiasts", "General Public"],
            key=f"audience")
    else:
        tgl_global_states[f"audience"] = None

    tgl_global_states[f"tgl_persona"] = st.checkbox("Toggle Role",
                                                    key="tgl_persona")
    if tgl_global_states[f"tgl_persona"]:
        tgl_global_states[f"role"] = st.selectbox(
            "Role", ["William Shakespeare", "George R.R. Martin", "Tolkien"],
            key=f"role")
    else:
        tgl_global_states[f"role"] = None

    tgl_global_states[f"tgl_exemplars"] = st.checkbox("Toggle Example Tone",
                                                      key="tgl_exemplars")
    if tgl_global_states[f"tgl_exemplars"]:
        tgl_global_states[f"example_tone"] = st.text_area("Example Tone",
                                                          key=f"example_tone")
    else:
        tgl_global_states[f"example_tone"] = None

    for block in story_blocks:
        with st.expander(f"{block} Block", expanded=True):
            prompt_elements[f"{block}_block_title"] = st.text_input(
                f"{block} Block Title", f"{block}", key=f"{block}_title")
            prompt_elements[f"{block}_word_count"] = st.slider(
                "Word Count",
                min_value=100,
                max_value=1000,
                value=300,
                step=50,
                key=f"{block}_word_count")
            prompt_elements[f"{block}_sentence_count"] = prompt_elements[
                f"{block}_word_count"] / WORDS_PER_SENTENCE
            prompt_elements[f"{block}_keywords"] = st.text_input(
                "Keywords", key=f"{block}_keywords")
            st.divider()
            prompt_elements[f"{block}_llm_model"] = st.selectbox(
                "LLM Model",
                ["Mistral", "GPT-3", "GPT-4", "Claude", "Custom Model"],
                key=f"{block}_llm_model")
            prompt_elements[f"{block}_temperature"] = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                key=f"{block}_temperature")

    # Generate button
    if st.button("Generate Article"):
        st.success("Article generation requested!")
        for block in story_blocks:
            prompt = utils.get_formatted_prompt(tgl_global_states, block)
            st.session_state[f"{block}_prompt"] = prompt

with middle_column:
    st.header("Debug column")

    # DEBUG PROMPT VALUE BEFORE PASS

    for block in story_blocks:
        if f"{block}_prompt" in st.session_state:
            st.subheader(f"{block} Prompt")
            st.text_area(f"{block} Prompt",
                         st.session_state[f"{block}_prompt"],
                         height=300,
                         key=f"{block}_prompt_display")

            if st.button(f"Run {block} Prompt"):
                with st.spinner(f"Generating {block}..."):
                    response = ppl_api.ppl_query_api(
                        st.session_state[f"{block}_prompt"])
                st.session_state[f"{block}_response"] = response
                st.success(f"{block} generated successfully!")

# DEBUG PROMPT VALUE BEFORE PASS

with right_column:
    st.header("Formatted Article")

    # formatted_article = f"# {story_title}\n\n"
    formatted_article = ""

    for block in story_blocks:
        if f"{block}_response" in st.session_state:
            formatted_article += f"## {tgl_global_states[f'{block}_block_title']}\n\n"
            formatted_article += f"![Alt text](https://placehold.co/600x400)  \n"
            formatted_article += st.session_state[f"{block}_response"] + "\n\n"

    st.markdown(formatted_article)

# TODO: Aggiungere toggle per keywords block
