from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the API key
pplx_api = os.getenv("pplx_api")

client = OpenAI(api_key=pplx_api, base_url="https://api.perplexity.ai")

def ppl_query_api(system_prompt):
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": "Please write the requested content based on the instructions provided."
        }
    ]

    # chat completion without streaming
    response = client.chat.completions.create(
        model="llama-3-sonar-large-32k-online",
        messages=messages,
    )

    # Access and return the content of the message
    return response.choices[0].message.content

def ppl_query_api_stream(system_prompt):
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": "Please write the requested content based on the instructions provided."
        }
    ]

    # chat completion with streaming
    response_stream = client.chat.completions.create(
        model="llama-3-sonar-large-32k-online",
        messages=messages,
        stream=True,
    )

    for response in response_stream:
        if response.choices[0].delta.content is not None:
            yield response.choices[0].delta.content