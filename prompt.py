import os

class Prompt:
    def __init__(self, section_type, story_title, toggle_tone_style, tone_style,
                 toggle_audience, audience, toggle_role, role, toggle_example_tone, example_tone,
                 block_title, word_count, sentence_count, keywords, llm_model, temperature,
                 template_file='prompt_template.txt'):
        self.section_type = section_type
        self.story_title = story_title
        self.toggle_tone_style = toggle_tone_style
        self.tone_style = tone_style
        self.toggle_audience = toggle_audience
        self.audience = audience
        self.toggle_role = toggle_role
        self.role = role
        self.toggle_example_tone = toggle_example_tone
        self.example_tone = example_tone
        self.block_title = block_title
        self.word_count = word_count
        self.sentence_count = sentence_count
        self.keywords = keywords
        self.llm_model = llm_model
        self.temperature = temperature
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
        template = self.template.replace("{{section_type}}", self.section_type)\
                            .replace("{{story_title}}", self.story_title)\
                            .replace("{{block_title}}", str(self.block_title))\
                            .replace("{{word_count}}", str(self.word_count))\
                            .replace("{{sentence_count}}", str(self.sentence_count))\
                            .replace("{{keywords}}", str(self.keywords))\
                            .replace("{{llm_model}}", str(self.llm_model))\
                            .replace("{{temperature}}", str(self.temperature))

        template = template.replace("{{tone_style}}", str(self.tone_style) if self.toggle_tone_style else "")
        template = template.replace("{{audience}}", str(self.audience) if self.toggle_audience else "")
        template = template.replace("{{role}}", str(self.role) if self.toggle_role else "")
        template = template.replace("{{example_tone}}", str(self.example_tone) if self.toggle_example_tone else "")

        return template

    def __str__(self):
        return f"Prompt(section_type={self.section_type}, story_title={self.story_title}, tone_style={self.tone_style})"