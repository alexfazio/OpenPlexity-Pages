from textwrap import dedent
import os
from getpass import getpass
from crewai import Agent, Task, Crew, Process
from textwrap import dedent
from langchain_groq import ChatGroq
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
search_tool = SerperDevTool()

# Get the API key from the environment variable
SERPER_API_KEY = os.getenv('SERPER_API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Check if the 'output-files' directory exists, and create it if it doesn't
if not os.path.exists('output-files'):
    os.makedirs('output-files')

# import prompt_helper
# prompt = prompt_helper.get_formatted_prompt()

# prompt=dedent((
#     """
#     You are tasked with writing a 4-sentence article section for a story. Your goal is to create engaging, informative content that adheres to specific guidelines. Follow these instructions carefully:
#
#     1. Review the following input variables:
#     <story_title>Mark Zuckerberg</story_title>
#     <section_title>Early Life</section_title>
#     <tone>Mark Zuckerberg</tone>
#     <target_audience>Children</target_audience>
#     <style_example>{{STYLE_EXAMPLE}}</style_example>
#     <keywords>china, mars, Elon Musk</keywords>
#     <additional_notes>{{ADDITIONAL_NOTES}}</additional_notes>
#
#     2. Write a 4-sentence article section based on the story_title and section_title provided. Ensure that each sentence contains factual information about the subject's early life.
#
#     3. Include sources for your information as inline citations (e.g., [1]) within the text. After the 4 sentences, provide an aggregate list of sources used.
#
#     4. Maintain a TONE throughout the article section. Remember that your target_audience is TARGET_AUDIENCE, so adjust your language and complexity accordingly.
#
#     5. Write in the style exemplified by the style_example provided. Emulate the voice and manner of expression demonstrated in this example.
#
#     6. Incorporate the given keywords naturally into your text. Don't force them if they don't fit the context of the early life section.
#
#     7. Consider the additional_notes and include relevant information if it fits within the context of the early life section.
#
#     8. Present your article section within <article_section> tags. Use <inline_citations> tags for the numbered citations within the text, and <aggregate_citations> tags for the list of sources at the end.
#
#     Remember to focus on creating engaging, factual content that meets all the specified requirements. Your goal is to inform and captivate the target audience while maintaining the appropriate tone and style.
#     """))

# Agent Definitions

goog_researcher_agent = Agent(
    role=dedent((
        """
        Google Researcher
        """)), # Think of this as the job title
    backstory=dedent((
        """
        You are a seasoned researcher specialized in Google SEO with a knack for uncovering and fact-checking information.
        """)), # This is the backstory of the agent, this helps the agent to understand the context of the task
    goal=dedent((
        """
        Your goal is to distill the essence of the brief into a list of grounding facts with their sources, using Google search to find accurate and up-to-date information.
        """)), # This is the goal that the agent is trying to achieve
    tools=[search_tool],
    allow_delegation=False,
    verbose=True,
    # ↑ Whether the agent execution should be in verbose mode
    max_iter=1,
    # ↑ maximum number of iterations the agent can perform before being forced to give its best answer (generate the output)
    max_rpm=100, # This is the maximum number of requests per minute that the agent can make to the language model
    # llm=ChatOpenAI(model_name="gpt-4o", temperature=0.8)
    # ↑ uncomment to use OpenAI API + "gpt-4o"
    llm=ChatGroq(temperature=0.8, model_name="llama-3.1-70b-versatile"),
    # ↑ uncomment to use Groq's API + "llama3-70b-8192"
    # llm=ChatGroq(temperature=0.6, model_name="llama3-70b-8192"),
    # ↑ uncomment to use Groq's API + "mixtral-8x7b-32768"
)
writer_agent = Agent(
    role=dedent((
        """
        You are Mark Zuckerberg
        """)), # Think of this as the job title
    backstory=dedent((
        """
        You are an American businessman. You co-founded the social media service Facebook and its parent company Meta Platforms (formerly Facebook, Inc.), of which you are chairman, chief executive officer and controlling shareholder.
        """)), # This is the backstory of the agent, this helps the agent to understand the context of the task
    goal=dedent((
        """
        Write an article according to the brief.
        """)), # This is the goal that the agent is trying to achieve
    allow_delegation=False,
    verbose=True,
    # ↑ Whether the agent execution should be in verbose mode
    max_iter=1,
    # ↑ maximum number of iterations the agent can perform before being forced to give its best answer (generate the output)
    max_rpm=100, # This is the maximum number of requests per minute that the agent can make to the language model
    # llm=ChatOpenAI(model_name="gpt-4o", temperature=0.8)
    # ↑ uncomment to use OpenAI API + "gpt-4o"
    llm=ChatGroq(temperature=0.8, model_name="llama-3.1-70b-versatile"),
    # ↑ uncomment to use Groq's API + "llama3-70b-8192"
)

# Task Definitions

import datetime

task_1 = Task(
    description=dedent((
        """
        Your goal is to distill the essence of the article brief into a list of grounding facts with their sources, using Google search to find accurate and up-to-date information.

        Here is the brief for the article you are researching:
        <article_brief>
        {prompt}
        </article_brief>

        Follow these steps to complete your task:

        1. Carefully read the article brief.

        2. Create a concise and effective search query to search Google and find facts that best match the content of the article brief. Look for segments that contain the most overlapping words or phrases with the brief.

        3. For each relevant fact you find, format it as follows:

        [fact number]

        [fact content]

        [fact URL]

        [matched article brief extract]

        4. Repeat steps 2-3 for each topic or question mentioned in the article brief, maintaining the order in which they appear in the brief.

        5. Combine all formatted facts into a single block of text.

        Your output should be formatted in markdown and contain only the list of facts. Do not include:
        - Comments explaining your work
        - Notes about which extracts matched which segments
        - Any additional text that isn't part of the fact segments

        Important rules to follow:
        - Use only the provided search query
        - Ensure all facts are directly relevant to the article brief
        - Provide accurate citations for each fact
        - Maintain the order of topics as they appear in the article brief
        - Do not add any personal opinions or analysis
        - Do not summarize or paraphrase the facts; present them as found
        - Include only the formatted list of facts in your response

        Begin your research now and present your findings in the specified format.
        """)),
    expected_output=dedent((
        """
        A list of facts with inline and aggregate citations, in markdown:

        Format each match exactly as follows, and include only these details:

        Here are some key facts about <article brief>:

        - Fact 1 [1][2].
        - Fact 2 [1][4].
        - Fact 3 [2].
        - Fact 4 [2].

        Citations:
        [1] https://www.url-sample.com/facts/sample
        [2] https://www.url-sample.com/facts/sample
        [3] https://www.url-sample.com/facts/sample
        [4] https://www.url-sample.com/facts/sample
        """)),
    agent=goog_researcher_agent,
    output_file=f'output-files/new_file_writer_agent_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
    # ↑ The output of each task iteration will be saved here
)

task_2 = Task(
    description=dedent((
        """
        {prompt}
        """)),
    expected_output=dedent((
        """
        Final article in markdown
        """)),
    agent=writer_agent,
    context=[task_1],
    output_file=f'output-files/new_file_agent_3_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
    # ↑ The output of each task iteration will be saved here
)

# Crew Kickoff
def main(prompt):
    # Instantiate your crew with a sequential process
    crew = Crew(
        agents=[goog_researcher_agent, writer_agent],
        tasks=[task_1, task_2],
        verbose=2,  # You can set it to 1 or 2 to different logging levels
        # ↑ indicates the verbosity level for logging during execution.
        process=Process.sequential
        # ↑ the process flow that the crew will follow (e.g., sequential, hierarchical).
    )


    inputs = {
    "prompt": prompt,
    }

    result = crew.kickoff(inputs=inputs)
    print("\n\n########################")
    print("## Here is your custom crew run result:")
    print("########################\n")
    print(result)

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
                print(content, end="", flush=True)
                summary += content

    except Exception as e:
        print(f"An error occurred while generating the summary: {str(e)}")
        return None

    # Extract the summary from between the <summary> tags
    match = re.search(r'<summary>(.*?)</summary>', summary, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        print("Could not find a properly formatted summary in the response.")
        return None


if __name__ == "__main__":
    result = main()
    print(result)
    summary = summarise_paragraph(result)
    print(summary)