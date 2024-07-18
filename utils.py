import os
from prompt import Prompt

def get_formatted_prompt(generation_details, blockName):
  prompt = Prompt(
    # section_type=blockName,
    # story_title=generation_details["story_title"],
    # block_title=generation_details[f"{blockName}_block_title"],
    # audience=generation_details[f"audience"],
    # style=generation_details[f"{blockName}_style"],
    # word_count=generation_details[f"{blockName}_word_count"],
    # sentence_count=generation_details[f"{blockName}_sentence_count"],
    # keywords=generation_details[f"{blockName}_keywords"],
    # tone_style=generation_details[f"{blockName}_tone_style"],
    # role=generation_details[f"{blockName}_role"],
    # tone=generation_details[f"{blockName}_tone"],

    section_type=blockName,
    story_title=generation_details["story_title"],

    toggle_tone_style=generation_details[f"toggle_tone_style"],
    tone_style=generation_details[f"tone_style"],
    toggle_audience=generation_details[f"toggle_audience"],
    audience=generation_details[f"audience"],
    toggle_role=generation_details[f"toggle_role"],
    role=generation_details[f"role"],
    toggle_example_tone=generation_details[f"toggle_example_tone"],
    example_tone=generation_details[f"example_tone"],

    block_title=generation_details[f"{blockName}_block_title"],
    word_count=generation_details[f"{blockName}_word_count"],
    sentence_count=generation_details[f"{blockName}_sentence_count"],
    keywords=generation_details[f"{blockName}_keywords"],
    
    llm_model=generation_details[f"{blockName}_llm_model"],
    temperature=generation_details[f"{blockName}_temperature"],

  ) 
  return prompt.get_formatted_prompt()
