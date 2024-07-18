from openai import OpenAI
from dotenv import load_dotenv
import os

def ppl_query_api(system_prompt):
    # Load environment variables from .env file
    load_dotenv()

    # Access the API key
    pplx_api = os.getenv("pplx_api")

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

    client = OpenAI(api_key=pplx_api, base_url="https://api.perplexity.ai")

    # chat completion without streaming
    response = client.chat.completions.create(
        model="llama-3-sonar-large-32k-online",
        messages=messages,
    )

    # Access and return the content of the message
    return response.choices[0].message.content