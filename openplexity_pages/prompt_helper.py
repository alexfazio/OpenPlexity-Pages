from prompt_states import prompt_states
import vertex_api

# Default values moved here
DEFAULT_GLOBAL_PROMPT_ELEM = {
    "story_title": "The Future of AI",
    "tone_style": "",
    "audience": "",
    "persona_first_name": "",
    "persona_last_name": "",
    "exemplars": ""
}

DEFAULT_BLOCKWISE_PROMPT_ELEM = {
    "Introduction": {"title": "Introduction", "word_count": 60, "keywords": "", "notes": ""},
    "Main": {"title": "Main", "word_count": 60, "keywords": "", "notes": ""},
    "Conclusion": {"title": "Conclusion", "word_count": 60, "keywords": "", "notes": ""}
}

# State Management Functions

def load_general_prompt_state():
    return prompt_states


def save_general_prompt_state(state):
    prompt_states.clear()
    prompt_states.update(state)


# Setter Functions

def update_global_prompt_elem(key, value):
    if "global_prompt_elem" not in prompt_states:
        prompt_states["global_prompt_elem"] = {}
    prompt_states["global_prompt_elem"][key] = value


def update_block_prompt_elem(block, key, value):
    if "blockwise_prompt_elem" not in prompt_states:
        prompt_states["blockwise_prompt_elem"] = {}
    if block not in prompt_states["blockwise_prompt_elem"]:
        prompt_states["blockwise_prompt_elem"][block] = {}
    prompt_states["blockwise_prompt_elem"][block][key] = value


# Getter Functions

def get_global_prompt_elem(key, default=None):
    if default is None:
        default = DEFAULT_GLOBAL_PROMPT_ELEM.get(key, "")
    return prompt_states.get("global_prompt_elem", {}).get(key, default)


def get_block_prompt_elem(block, key, default=None):
    if default is None:
        default = DEFAULT_BLOCKWISE_PROMPT_ELEM.get(block, {}).get(key, "")
    return prompt_states.get("blockwise_prompt_elem", {}).get(block, {}).get(key, default)


# Prompt Generation Function

def get_formatted_prompt(block):
    global_elements = load_general_prompt_state()["global_prompt_elem"]
    block_elements = load_general_prompt_state()["blockwise_prompt_elem"].get(block, {})

    # Fetch word count from block_elements, which is updated by app.py
    word_count = block_elements.get('word_count', '60') // 15
    
    # Include the story title in the prompt
    story_title = global_elements.get('story_title', 'Untitled Story')
    
    prompt = f"Write a {word_count} sentence article section for the story titled '{story_title}'. "
    prompt += f"This section is titled '{block_elements.get('title', block)}'. "
    prompt += f"Please include sources for your information as inline and aggregate citations."

    if global_elements.get("tone_style"):
        prompt += f"Use a {global_elements['tone_style']} tone. "

    if global_elements.get("audience"):
        prompt += f"Target audience: {global_elements['audience']}. "

    if global_elements.get("persona_first_name") and global_elements.get("persona_last_name"):
        full_name = f"{global_elements['persona_first_name']} {global_elements['persona_last_name']}"
        prompt += f"Write in the style of {full_name}. "

    if global_elements.get("exemplars"):
        prompt += f"Use this as an example of the desired tone: {global_elements['exemplars']}. "

    if block_elements.get("keywords"):
        prompt += f"\nInclude these keywords: {block_elements['keywords']}. "

    if block_elements.get("notes"):
        prompt += f"\nConsider these additional notes: {block_elements['notes']}. "

    return prompt


# New function to generate content using Vertex AI
def generate_content(block):
    prompt = get_formatted_prompt(block)
    full_response = ""
    for chunk in vertex_api.generate_stream(prompt):
        full_response += chunk
    
    citations = vertex_api.extract_citations(full_response)
    formatted_response = vertex_api.format_response_with_citations(full_response, citations)
    return formatted_response


# Initialization
if not prompt_states["global_prompt_elem"]:
    prompt_states["global_prompt_elem"] = DEFAULT_GLOBAL_PROMPT_ELEM.copy()

if not prompt_states["blockwise_prompt_elem"]:
    prompt_states["blockwise_prompt_elem"] = DEFAULT_BLOCKWISE_PROMPT_ELEM.copy()