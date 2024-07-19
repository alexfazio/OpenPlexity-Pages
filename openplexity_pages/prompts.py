import logging

# Setup logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Global prompt elements
global_prompt_elements = {
    "story_title": "",
    "tone_style": "",
    "audience": "",
    "role": "",
    "example_tone": "",
}

# Block-specific prompt elements
block_prompt_elements = {
    "Zero": {},
    "One": {},
    "Two": {},
}

def get_formatted_prompt(global_toggles, block_toggles, global_elements, block_elements):
    prompt = f"Write a {block_elements['word_count']} word article section titled '{block_elements['title']}'. "
    prompt += f"The story title is '{global_elements['story_title']}'. "

    if global_toggles["tgl_style"]:
        prompt += f"Use a {global_elements['tone_style']} tone. "
    
    if global_toggles["tgl_target_audience"]:
        prompt += f"Target audience: {global_elements['audience']}. "
    
    if global_toggles["tgl_persona"]:
        prompt += f"Write in the style of {global_elements['role']}. "
    
    if global_toggles["tgl_exemplars"]:
        prompt += f"Use this as an example of the desired tone: {global_elements['example_tone']}. "
    
    if block_toggles["tgl_keywords"]:
        prompt += f"Include these keywords: {block_elements['keywords']}. "
    
    return prompt

# TODO: separate il dizionario dinamico di Vasile per i prompt, in un dizionario più curato

# dummy_prompt = f"""
# {{
#     "Target Audience": "{prompt_elements['target_audience']}",
#     "Example Tone": "{prompt_elements['example_tone']}",
#     "Keywords": "{prompt_elements['keywords']}",
#     "Story Block Position": "{prompt_elements['story_block_position']}",
#     "Story Block Sentence Count": "{prompt_elements['story_block_sentence_count']}",
#     "Story Block Title": "{prompt_elements['story_block_title']}",
#     "Story Block Word Count": "{prompt_elements['story_block_word_count']}",
#     "Story Style": "{prompt_elements['story_style']}",
#     "Story Title": "{prompt_elements['story_title']}",
#     "Story Tone": "{prompt_elements['story_tone']}",
#     "Writer Role Persona": "{prompt_elements['writer_role_persona']}"
# }}
# """

# logging.info("PRINTING dummy_prompt from prompts.py")
# print(dummy_prompt)

#---

# # Global prompt elements
# global_prompt_elements = {
#     "story_title": "",
#     "tone_style": "",
#     "audience": "",
#     "role": "",
#     "example_tone": "",
# }

# block_prompt_elements = {
#     "story_block_position": "",  # Intro, conclusion, etc.
#     "story_block_sentence_count": "",
#     "story_block_title": "",
#     "story_block_word_count": "",
# }