prompt_elements = {
    "audience": "",
    "example_tone": "",
    "keywords": "",
    "role": "",
    "sentence_count": "",
    "story_block_title": "",
    "story_title": "",
    "style": "",
    "tone": "",
    "word_count": ""
}

dummy_prompt = f"""
{
  "Story Title": {prompt_elements['story_title']},
  "Audience": {prompt_elements['audience']},
  "Role": {prompt_elements['role']},
  "Tone": {prompt_elements['tone']},
  "Example Tone": {prompt_elements['example_tone']},
  "Story Block Title": {prompt_elements['story_block_title']},
  "Style": {prompt_elements['style']},
  "Keywords": {prompt_elements['keywords']},
  "Word Count": {prompt_elements['word_count']},
  "Sentence Count": {prompt_elements['sentence_count']}
}
"""