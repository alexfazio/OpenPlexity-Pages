from experiments import vertex_api
from prompt_states import prompt_states
from crew import main

# Default values moved here
DEFAULT_GLOBAL_PROMPT_ELEM = {
    "story_title": "",
    "tone_style": "",
    "audience": "",
    "persona_first_name": "",
    "persona_last_name": "",
    "exemplars": ""
}

DEFAULT_BLOCK_LEVEL_PROMPT_ELEM = {
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
    if "block_level_prompt_elem" not in prompt_states:
        prompt_states["block_level_prompt_elem"] = {}
    if block not in prompt_states["block_level_prompt_elem"]:
        prompt_states["block_level_prompt_elem"][block] = {}
    prompt_states["block_level_prompt_elem"][block][key] = value


# Getter Functions

def get_global_prompt_elem(key, default=None):
    if default is None:
        default = DEFAULT_GLOBAL_PROMPT_ELEM.get(key, "")
    return prompt_states.get("global_prompt_elem", {}).get(key, default)


def get_block_prompt_elem(block, key, default=None):
    if default is None:
        default = DEFAULT_BLOCK_LEVEL_PROMPT_ELEM.get(block, {}).get(key, "")
    return prompt_states.get("block_level_prompt_elem", {}).get(block, {}).get(key, default)


# Prompt Generation Function

def get_formatted_prompt(block):
    global_elements = load_general_prompt_state()["global_prompt_elem"]
    block_elements = load_general_prompt_state()["block_level_prompt_elem"].get(block, {})

    # Fetch word count from block_elements, which is updated by app.py
    word_count = block_elements.get('word_count', '60') // 15  # "`// 15` converts the desired word count into an
    # approximate sentence count, which is more easily recognized by LLMS.

    # Include the story title in the prompt
    story_title = global_elements.get('story_title', 'Untitled Story')

    prompt = f"You are tasked with writing a {word_count} sentences article section section for a story titled '{story_title}'. "

    prompt += f"\n1. Review the following input variables:\n"

    prompt += f"\n<story_title>{global_elements.get('story_title', 'Untitled Story')}</story_title>\n"

    prompt += f"\n<section_title>{block_elements.get('title', block)}</section_title>\n"

    if global_elements.get("tone_style"):
        prompt += f"\n<tone>{global_elements['tone_style']}</tone>\n"

    if global_elements.get("audience"):
        prompt += f"\n<target_audience>{global_elements['audience']}</target_audience>\n"

    if global_elements.get("persona_first_name") and global_elements.get("persona_last_name"):
        prompt += f"\n<persona>{global_elements['persona_first_name']} {global_elements['persona_last_name']}</persona>\n"

    if global_elements.get("exemplars"):
        prompt += f"\n<style_examples>{global_elements['exemplars']}</style_examples>\n"

    if block_elements.get("keywords"):
        prompt += f"\n<keywords>{block_elements['keywords']}</keywords>\n"

    prompt += f"2. Write a 4-sentence article section based on the story_title and section_title provided. Ensure that each sentence contains factual information about the subject's early life."

    prompt += f"3. Include sources for your information as inline citations (e.g., [1]) within the text. After the 4 sentences, provide an aggregate list of sources used."

    prompt += f"4. Maintain a TONE throughout the article section. Remember that your target_audience is TARGET_AUDIENCE, so adjust your language and complexity accordingly."

    prompt += f"5. Write in the style exemplified by the style_example provided. Emulate the voice and manner of expression demonstrated in this example."

    prompt += f"6. Incorporate the given keywords naturally into your text. Don't force them if they don't fit the context of the early life section."

    prompt += f"7. Consider the additional_notes and include relevant information if it fits within the context of the early life section."

    prompt += f"8. Present your article section within <article_section> tags. Use <inline_citations> tags for the numbered citations within the text, and <aggregate_citations> tags for the list of sources at the end."

    prompt += f"Remember to focus on creating engaging, factual content that meets all the specified requirements. Your goal is to inform and captivate the target audience while maintaining the appropriate tone and style."

    if block_elements.get("notes"):
        prompt += f"\nConsider these additional notes: \n<additional_notes>{block_elements['notes']}</additional_notes>\n "

    return prompt


# New function to generate content
def generate_api_response(block):
    prompt = get_formatted_prompt(block)
    full_response = main(prompt)
    return full_response
    # try:
    #  full_response = ""
        # for chunk in vertex_api.generate_stream(prompt):
        #     full_response += chunk
        # full_response = main(prompt)

        # citations = vertex_api.extract_citations(full_response)
        # formatted_response = vertex_api.format_response_with_citations(full_response, citations)
        # return formatted_response
        # return full_response
    # except Exception as e:
    #     error_message = get_user_friendly_error_message(e)
    #     return f"Error: {error_message}"


def get_user_friendly_error_message(error):
    if isinstance(error, ValueError) and "blocked by the safety filters" in str(error):
        return ("The content was blocked by safety filters. Please try rephrasing your request or using less "
                "controversial topics.")
    elif isinstance(error, Exception):
        return f"An unexpected error occurred: {str(error)}. Please try again or contact support if the issue persists."
    else:
        return "An unknown error occurred. Please try again or contact support if the issue persists."


# Initialization
if not prompt_states["global_prompt_elem"]:
    prompt_states["global_prompt_elem"] = DEFAULT_GLOBAL_PROMPT_ELEM.copy()

if not prompt_states["block_level_prompt_elem"]:
    prompt_states["block_level_prompt_elem"] = DEFAULT_BLOCK_LEVEL_PROMPT_ELEM.copy()