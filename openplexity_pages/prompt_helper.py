from prompt_states import prompt_states

# Retrieves the current state of prompt_states
def load_prompt_state():
    return prompt_states

# Updates the global prompt_states variable with a new state
def save_prompt_state(state):
    global prompt_states
    prompt_states = state

# Updates a specific key-value pair in the global section of prompt_states
def update_global_prompt_element(key, value):
    prompt_states["global"][key] = value

# Updates a specific key-value pair for a given block in the blocks section of prompt_states
# If the block doesn't exist, it creates it
def update_block_prompt_element(block, key, value):
    if block not in prompt_states["blocks"]:
        prompt_states["blocks"][block] = {}
    prompt_states["blocks"][block][key] = value

# Retrieves a value from the global section of prompt_states for a given key
# Returns a default value if the key is not found
def get_global_prompt_element(key, default=""):
    return prompt_states["global"].get(key, default)

# Retrieves a value from a specific block in the blocks section of prompt_states for a given key
# Returns a default value if the block or key is not found
def get_block_prompt_element(block, key, default=""):
    return prompt_states["blocks"].get(block, {}).get(key, default)

# Generates a formatted prompt string for a given block
# Incorporates various elements from both global and block-specific settings
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

# Initialize default states if not already set
# This ensures that there's always a basic structure in place for the prompts
if not prompt_states:
    prompt_states.update({
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
    })