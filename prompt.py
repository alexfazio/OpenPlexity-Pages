import os

class Prompt:
    def __init__(self, section_type, story_title, block_title, audience,
                 style, word_count, sentence_count, keywords, tone_style,
                 role, tone, template_file='prompt_template.txt'):
        self.section_type = section_type
        self.story_title = story_title
        self.block_title = block_title
        self.audience = audience
        self.style = style
        self.word_count = word_count
        self.sentence_count = sentence_count
        self.keywords = keywords
        self.tone_style = tone_style
        self.role = role
        self.tone = tone
        self.template = self.load_template(template_file)

    def load_template(self, template_file):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, template_file)
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Template file not found: {file_path}")

    def get_formatted_prompt(self):
        return self.template.replace("{{section_type}}", self.section_type)\
                            .replace("{{story_title}}", self.story_title)\
                            .replace("{{block_title}}", self.block_title)\
                            .replace("{{audience}}", self.audience)\
                            .replace("{{style}}", self.style)\
                            .replace("{{word_count}}", str(self.word_count))\
                            .replace("{{sentence_count}}", str(self.sentence_count))\
                            .replace("{{keywords}}", self.keywords)\
                            .replace("{{tone_style}}", self.tone_style)\
                            .replace("{{role}}", self.role)\
                            .replace("{{tone}}", self.tone)

    def __str__(self):
        return f"Prompt(section_type={self.section_type}, story_title={self.story_title}, tone_style={self.tone_style})"