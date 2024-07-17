import os
from prompt import Prompt

def get_formatted_prompt(generation_details, blockName):
  prompt = Prompt(
    section_type=blockName,
    story_title=generation_details["story_title"],
    block_title=generation_details[f"{blockName.lower()}_block_title"],
    audience=generation_details[f"{blockName.lower()}_audience"],
    persona=generation_details[f"{blockName.lower()}_persona"],
    word_count=generation_details[f"{blockName.lower()}_word_count"],
    key_points=generation_details[f"{blockName.lower()}_key_points"],
    tone_style=generation_details[f"{blockName.lower()}_llm_model"]
  ) 
  print(prompt)
  print(prompt.get_formatted_prompt())
  return prompt.get_formatted_prompt()
