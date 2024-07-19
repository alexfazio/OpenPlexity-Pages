from prompt_states import prompt_states

# Default values moved here
DEFAULT_GLOBAL_PROMPT_ELEM = {
    "story_title": "The Future of AI",
    "tone_style": "",
    "audience": "",
    "role": "",
    "exemplars": ""
}

DEFAULT_BLOCKWISE_PROMPT_ELEM = {
    "Introduction": {"title": "Introduction", "word_count": 60, "keywords": ""},
    "Main": {"title": "Main", "word_count": 60, "keywords": ""},
    "Conclusion": {"title": "Conclusion", "word_count": 60, "keywords": ""}
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
    word_count = block_elements.get('word_count', '60')
    
    prompt = f"Write a {word_count} word article section titled '{block_elements.get('title', block)}'. "

    if global_elements.get("tone_style"):
        prompt += f"Use a {global_elements['tone_style']} tone. "

    if global_elements.get("audience"):
        prompt += f"Target audience: {global_elements['audience']}. "

    if global_elements.get("role"):
        prompt += f"Write in the style of {global_elements['role']}. "

    if global_elements.get("exemplars"):
        prompt += f"Use this as an example of the desired tone: {global_elements['exemplars']}. "

    if block_elements.get("keywords"):
        prompt += f"Include these keywords: {block_elements['keywords']}. "

    return prompt


# Initialization
if not prompt_states["global_prompt_elem"]:
    prompt_states["global_prompt_elem"] = DEFAULT_GLOBAL_PROMPT_ELEM.copy()

if not prompt_states["blockwise_prompt_elem"]:
    prompt_states["blockwise_prompt_elem"] = DEFAULT_BLOCKWISE_PROMPT_ELEM.copy()