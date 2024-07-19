import streamlit as st
import random
from datetime import datetime

def apply_custom_css():
    st.markdown("""
    <style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&family=Red+Hat+Display:ital,wght@0,300..900;1,300..900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&display=swap');

/*
  <color name="Eerie black" hex="1c1c1c" r="28" g="28" b="28" />
  <color name="Platinum" hex="daddd8" r="218" g="221" b="216" />
  <color name="Alabaster" hex="ecebe4" r="236" g="235" b="228" />
  <color name="Anti-flash white" hex="eef0f2" r="238" g="240" b="242" />
  <color name="Ghost white" hex="fafaff" r="250" g="250" b="255" />
*/
                
.article-container {
  background-color: #ecebe4;
  border-radius: 22px;
  padding: 20px 60px;
  max-width: 800px;
  margin: 20px auto;
}

.article-title {
  font-family: "Playfair Display", serif;
  color: #1c1c1c;
  font-size: 60px;
  font-weight: 900;
  line-height: 1.2;
  margin-bottom: 0px;
  transition: transform 0.3s ease;
}

.block-title {
  font-family: "Playfair Display", serif;
  color: #1c1c1c;
  font-size: 36px;
  font-weight: 700;
  margin-top: 40px;
  margin-bottom: 20px;
  border-bottom: 2px solid #e0e0e0;
  padding-bottom: 10px;
  transition: transform 0.3s ease;
}

.article-content {
  font-size: 18px;
  font-family: "Lato", sans-serif;
  font-weight: 400;
  line-height: 1.8;
  color: #1c1c1c;
  margin-bottom: 30px;
  transition: transform 0.3s ease;
}

.article-image {
  width: 100%;
  max-width: 100%;
  height: auto;
  margin: 10px 0;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.article-image:hover {
  transform: scale(1.02);
}
.article-title:hover {
  transform: scale(1.02);
}
.block-title:hover {
  transform: scale(1.01);
}              
hr {
  border: none;
  height: 1px;
  background-color: #e0e0e0;
  margin: 10px 0;
}

.article-metadata {
  font-family: "Lato", sans-serif;
  font-size: 14px;
  color: #666;
  margin-bottom: 20px;
}
.article-tags {
  margin-top: 20px;
  padding: auto 5px;
}
.article-tag {
  display: inline-block;
  background-color: #daddd8;
  color: #1c1c1c;
  padding: 5px 10px;
  margin-right: 10px;
  border-radius: 15px;
  font-size: 12px;
}
    </style>
    """, unsafe_allow_html=True)

    


def calculate_reading_time(story_blocks, session_state):
    # Placeholder function to calculate reading time
    # You can implement a more accurate calculation based on word count later
    total_words = sum(len(session_state.get(f"{block}_response", "").split()) for block in story_blocks)
    return max(1, round(total_words / 200))  # Assume 200 words per minute, minimum 1 minute

def generate_tags(title, story_blocks, session_state):
    # Placeholder function to generate tags
    # You can implement a more sophisticated tag generation system later
    tags = set()
    tags.add(title.split()[0])  # Add the first word of the title as a tag
    for block in story_blocks:
        if f"{block}_response" in session_state:
            content = session_state[f"{block}_response"]
            words = content.split()
            tags.update(random.sample(words, min(3, len(words))))  # Add up to 3 random words from each block
    return list(tags)[:5]  # Return up to 5 tags

def format_article(story_blocks, block_prompt_elements, session_state):
    formatted_article = '<div class="article-container">'
    formatted_article += f'<h1 class="article-title">{session_state.get("story_title", "")}</h1>'
    
    # Add metadata
    formatted_article += '<div class="article-metadata">'
    formatted_article += f'<span>By AI Writer</span> | '
    formatted_article += f'<span>{datetime.now().strftime("%B %d, %Y")}</span> | '
    formatted_article += f'<span>Estimated reading time: {calculate_reading_time(story_blocks, session_state)} min</span>'
    formatted_article += '</div>'

    # Add tags
    formatted_article += '<div class="article-tags">'
    for tag in generate_tags(session_state.get("story_title", ""), story_blocks, session_state):
        formatted_article += f'<span class="article-tag">{tag}</span>'
    formatted_article += '</div>'

    for block in story_blocks:
        if f"{block}_response" in session_state:
            random_number = random.randint(1, 1000)
            
            formatted_article += f'<h2 class="block-title">{block_prompt_elements[block]["title"]}</h2>'
            formatted_article += f'<img src="https://picsum.photos/seed/{random_number}/640/160" alt="{block} image" class="article-image">'
            formatted_article += f'<div class="article-content">{session_state[f"{block}_response"]}</div>'
            
            # Add buttons
            formatted_article += '<div class="article-buttons">'
            formatted_article += f'<button class="copy-button" onclick="copyToClipboard(\'{block}\')">Copy to Clipboard</button>'
            formatted_article += f'<button class="sources-button" onclick="showSources(\'{block}\')">Sources</button>'
            formatted_article += f'<button class="share-button" onclick="shareArticle(\'{block}\')">Share</button>'
            formatted_article += '</div>'

    formatted_article += '</div>'
    return formatted_article