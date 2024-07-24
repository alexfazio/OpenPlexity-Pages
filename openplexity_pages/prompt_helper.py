from experiments import vertex_api
from prompt_states import prompt_states
from agent_writer import main as agent_writer
import groq_search

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

    story_title = global_elements.get('story_title', '')
    block_title = block_elements.get('title', block)

    if story_title and block_title:
        groq_search_query = f"{story_title} {block_title}"
        research_results = groq_search.run_conversation(groq_search_query)
    else:
        research_results = "<research_results>"

    # Fetch word count from block_elements, which is updated by app.py
    word_count = block_elements.get('word_count', '60') // 15  # "`// 15` converts the desired word count into an
    # approximate sentence count, which is more easily recognized by LLMS.

    # Include the story title in the prompt
    story_title = global_elements.get('story_title', 'Untitled Story')

    prompt = f"You are tasked with writing a concise article section for a larger story. Your goal is to create informative and engaging content that adheres to specific guidelines. Follow these instructions carefully: "

    prompt += f"""
    1. Review the following research results. These will serve as the factual basis for your writing:

    <research_results>
    {research_results}
    </research_results>
    """

    prompt += f"""
    2. Take note of the story title and section title:
    
    <story_title>{story_title}</story_title>
    <section_title>{block_elements.get('title', block)}</section_title>
    """

    prompt += f"""
    3. Consider the following input variables while writing:
    """
    if global_elements.get("tone_style"):
        prompt += f"\n<tone>{global_elements['tone_style']}</tone>"
    if global_elements.get("audience"):
        prompt += f"\n<target_audience>{global_elements['audience']}</target_audience>"
    if block_elements.get("keywords"):
        prompt += f"\n<keywords>{block_elements['keywords']}</keywords>\n"

    prompt += f"""\n4. Write a {word_count}-sentence article section based on the story title and section title provided. Ensure that each sentence contains factual information about the section topic.
    """

    prompt += f"""5. Include sources for your information as inline citations (e.g., [1]) within the text. After the {word_count} sentences, provide an aggregate list of sources used.
    """

    prompt += f"""6. Maintain the specified tone throughout the article section. Remember your target audience and adjust your language and complexity accordingly.
    """

    prompt += f"""7. Write in the style exemplified by the style examples provided. Emulate the voice and manner of expression demonstrated in these examples.
    """

    prompt += f"""8. Incorporate the given keywords naturally into your text. Don't force them if they don't fit the context of the section.
    """

    prompt += f"""9. Present your article section within <article_section> tags. Use <inline_citations> tags for the numbered citations within the text, and <aggregate_citations> tags for the list of sources at the end.
    """

    prompt += f"""10. Focus on creating engaging, factual content that meets all the specified requirements. Your goal is to inform and captivate the target audience while maintaining the appropriate tone and style.
    """

    if block_elements.get("notes"):
        prompt += f"\n 11. Consider these additional_notes and include relevant information if it fits within the context of the '{block_elements.get('title', block)}' section."


    prompt += f"""
    \nPresent your article section using the following format:
    
    <article_section>
    Write your {word_count} sentences here, including <inline_citations> tags for the numbered citations within the text.
    </article_section>
    
    <aggregate_citations>
    List your sources here, numbered to match the inline citations.
    </aggregate_citations>

    Remember to ground your writing in the provided research results, adhere to the specified tone and style, and create content that is both informative and engaging for the target audience.
    """

    return prompt


# New function to generate content
def generate_api_response(block):
    prompt = get_formatted_prompt(block)
    full_response = agent_writer(prompt)
    return full_response

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