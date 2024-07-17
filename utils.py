import os
from prompt import Prompt

def get_formatted_prompt(generation_details, blockName):
  prompt = Prompt(
    section_type=blockName,
    story_title=generation_details["story_title"],
    block_title=generation_details[f"{blockName}_block_title"],
    audience=generation_details[f"{blockName}_audience"],
    style=generation_details[f"{blockName}_style"],
    word_count=generation_details[f"{blockName}_word_count"],
    sentence_count=generation_details[f"{blockName}_sentence_count"],
    keywords=generation_details[f"{blockName}_keywords"],
    tone_style=generation_details[f"{blockName}_tone_style"],
    role=generation_details[f"{blockName}_role"],
    tone=generation_details[f"{blockName}_tone"],
  ) 
  return prompt.get_formatted_prompt()
