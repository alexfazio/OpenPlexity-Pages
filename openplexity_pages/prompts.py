import logging

# Setup logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

global_prompt_elements = {
    "target_audience": "",
    "example_tone": "",
    "keywords":
    "",  # Is the keyword feature specific to a story block, or is it a feature of the story as a whole?
    "story_style": "",
    "story_title": "",
    "story_tone": "",
    "writer_role_persona": ""
}

story_block = {
    "story_title": story_title,
}

# block_prompt_elements = {
#     "story_block_position": "",  # Intro, conclusion, etc.
#     "story_block_sentence_count": "",
#     "story_block_title": "",
#     "story_block_word_count": "",
# }

# TODO: separare il dizionario dinamico di Vasile per i prompt, in un dizionario più curato

dummy_prompt = f"""
{{
    "Target Audience": "{prompt_elements['target_audience']}",
    "Example Tone": "{prompt_elements['example_tone']}",
    "Keywords": "{prompt_elements['keywords']}",
    "Story Block Position": "{prompt_elements['story_block_position']}",
    "Story Block Sentence Count": "{prompt_elements['story_block_sentence_count']}",
    "Story Block Title": "{prompt_elements['story_block_title']}",
    "Story Block Word Count": "{prompt_elements['story_block_word_count']}",
    "Story Style": "{prompt_elements['story_style']}",
    "Story Title": "{prompt_elements['story_title']}",
    "Story Tone": "{prompt_elements['story_tone']}",
    "Writer Role Persona": "{prompt_elements['writer_role_persona']}"
}}
"""

logging.info("PRINTING dummy_prompt from prompts.py")
print(dummy_prompt)
