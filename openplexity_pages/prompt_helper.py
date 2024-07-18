import json
from pathlib import Path

PROMPT_STATE_FILE = Path(__file__).parent / "prompt_states.json"

def load_prompt_state():
    if PROMPT_STATE_FILE.exists():
        try:
            with open(PROMPT_STATE_FILE, "r") as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
                else:
                    print("Warning: prompt_states.json is empty. Initializing with default state.")
        except json.JSONDecodeError:
            print("Error: Invalid JSON in prompt_states.json. Initializing with default state.")
    return {
        "global": {},
        "blocks": {}
    }

def save_prompt_state(state):
    with open(PROMPT_STATE_FILE, "w") as f:
        json.dump(state, f)

def update_global_prompt_element(key, value):
    state = load_prompt_state()
    state["global"][key] = value
    save_prompt_state(state)

def update_block_prompt_element(block, key, value):
    state = load_prompt_state()
    if block not in state["blocks"]:
        state["blocks"][block] = {}
    state["blocks"][block][key] = value
    save_prompt_state(state)

def get_global_prompt_element(key, default=""):
    state = load_prompt_state()
    return state["global"].get(key, default)

def get_block_prompt_element(block, key, default=""):
    state = load_prompt_state()
    return state["blocks"].get(block, {}).get(key, default)

def get_formatted_prompt(block):
    global_elements = load_prompt_state()["global"]
    block_elements = load_prompt_state()["blocks"].get(block, {})

    prompt = f"Write a {block_elements.get('word_count', '300')} word article section titled '{block_elements.get('title', block)}'. "
    
    if global_elements.get("tone_style"):
        prompt += f"Use a {global_elements['tone_style']} tone. "
    
    if global_elements.get("audience"):
        prompt += f"Target audience: {global_elements['audience']}. "
    
    if global_elements.get("role"):
        prompt += f"Write in the style of {global_elements['role']}. "
    
    if global_elements.get("example_tone"):
        prompt += f"Use this as an example of the desired tone: {global_elements['example_tone']}. "
    
    if block_elements.get("keywords"):
        prompt += f"Include these keywords: {block_elements['keywords']}. "
    
    return prompt

# Initialize default states if the file doesn't exist or is invalid
if not PROMPT_STATE_FILE.exists() or load_prompt_state() == {"global": {}, "blocks": {}}:
    default_state = {
        "global": {
            "story_title": "The Future of AI",
            "tone_style": "",
            "audience": "",
            "role": "",
            "example_tone": "",
        },
        "blocks": {
            "Introduction": {"title": "Introduction", "word_count": 300, "keywords": ""},
            "Main": {"title": "Main", "word_count": 500, "keywords": ""},
            "Conclusion": {"title": "Conclusion", "word_count": 200, "keywords": ""},
        }
    }
    save_prompt_state(default_state)