import logging
import os
import re
import datetime
from groq import Groq
from crewai import Agent, Task, Crew, Process
from textwrap import dedent
from langchain_groq import ChatGroq
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import groq_search

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()
search_tool = SerperDevTool()

# Get the API key from the environment variable
SERPER_API_KEY = os.getenv('SERPER_API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Check if the 'output-files' directory exists, and create it if it doesn't
if not os.path.exists('output-files'):
    os.makedirs('output-files')

# Agent Definitions

writer_agent = Agent(
    role=dedent((
        """
        You are a professional writer.
        """)),
    backstory=dedent((
        """
        You are a professional writer, experienced in adhering to writing instructions for outstanding quality writing output.
        """)),
    goal=dedent((
        """
        Write an article according to the brief.
        """)),
    allow_delegation=False,
    verbose=True,
    max_iter=1,
    max_rpm=3,
    llm=ChatGroq(temperature=0.8, model_name="llama-3.1-70b-versatile"),
)

# Task Definitions

task_is_writing = Task(
    description=dedent((
        """
        {prompt}
        """)),
    expected_output=dedent((
        """
        Present your article section using the following format:
        
        <article_section>
        Write your four sentences here, including <inline_citations> tags for the numbered citations within the text.
        </article_section>
        
        <aggregate_citations>
        List your sources here, numbered to match the inline citations.
        </aggregate_citations>
        """)),
    agent=writer_agent,
    output_file=f'output-files/output_task_is_writing_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
)


# Crew Kickoff
def main(prompt):
    # Instantiate your crew with a sequential process
    crew = Crew(
        agents=[writer_agent],
        tasks=[task_is_writing],
        verbose=2,
        process=Process.sequential
    )

    inputs = {
        "prompt": prompt,
    }

    result = crew.kickoff(inputs=inputs)
    logging.info("\n\n########################")
    logging.info("## Here is your custom crew run result:")
    logging.info("########################\n")
    logging.info(result)

    # Convert result to string if it's not already
    return str(result)


def summarise_paragraph(paragraph):
    summary = ""

    # Initialize the Groq client
    client = Groq()

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",  # Keeping the original model name
            messages=[
                {
                    "role": "system",
                    "content": dedent(f"""
                    Your task is to summarize a given paragraph in two sentences. Do not omit any idea. Here's the paragraph:

                    <paragraph>
                    {paragraph}
                    </paragraph>

                    To summarize this paragraph effectively:
                    1. Read the paragraph carefully to understand its main idea and key points.
                    2. Identify the most important information that captures the essence of the paragraph.
                    3. Condense this information into a single, concise sentence that accurately represents the paragraph's content.
                    4. Ensure your summary sentence is clear, coherent, and grammatically correct.
                    5. Avoid including minor details or examples unless they are crucial to the main idea.

                    Please provide your one-sentence summary inside <summary> tags. Your summary should be no longer than 30 words.
                    """)
                }
            ],
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        for chunk in completion:
            if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                logging.info(content)
                summary += content

    except Exception as e:
        logging.error(f"An error occurred while generating the summary: {str(e)}")
        return None

    # Extract the summary from between the <summary> tags
    match = re.search(r'<summary>(.*?)</summary>', summary, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        logging.warning("Could not find a properly formatted summary in the response.")
        return None



# if __name__ == "__main__":
#     prompt=dedent((
#         """
#         You are tasked with writing a 4-sentence article section for a story. Your goal is to create engaging, informative content that adheres to specific guidelines. Follow these instructions carefully:
#
#         1. Review the following input variables:
#         <story_title>Mark Zuckerberg</story_title>
#         <section_title>Early Life</section_title>
#         <tone>Mark Zuckerberg</tone>
#         <target_audience>Children</target_audience>
#         <style_example>{{STYLE_EXAMPLE}}</style_example>
#         <keywords>china, mars, Elon Musk</keywords>
#         <additional_notes>{{ADDITIONAL_NOTES}}</additional_notes>
#
#         2. Write a 4-sentence article section based on the story_title and section_title provided. Ensure that each sentence contains factual information about the subject's early life.
#
#         3. Include sources for your information as inline citations (e.g., [1]) within the text. After the 4 sentences, provide an aggregate list of sources used.
#
#         4. Maintain a TONE throughout the article section. Remember that your target_audience is TARGET_AUDIENCE, so adjust your language and complexity accordingly.
#
#         5. Write in the style exemplified by the style_example provided. Emulate the voice and manner of expression demonstrated in this example.
#
#         6. Incorporate the given keywords naturally into your text. Don't force them if they don't fit the context of the early life section.
#
#         7. Consider the additional_notes and include relevant information if it fits within the context of the early life section.
#
#         8. Present your article section within <article_section> tags. Use <inline_citations> tags for the numbered citations within the text, and <aggregate_citations> tags for the list of sources at the end.
#
#         Remember to focus on creating engaging, factual content that meets all the specified requirements. Your goal is to inform and captivate the target audience while maintaining the appropriate tone and style.
#         """))
#     result = main(prompt)
#     logging.info(result)
#     summary = summarise_paragraph(result)
#     logging.info(summary)