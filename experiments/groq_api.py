from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the API key
groq_api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=groq_api_key)

def groq_query_api(system_prompt):
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
        model="llama3-70b-8192",
        messages=messages,
        temperature=0.6,
        max_tokens=8192,
        top_p=1,
        stream=False,
    )

    # Access and return the content of the message
    return response.choices[0].message.content

def groq_query_api_stream(system_prompt):
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
        model="llama3-70b-8192",
        messages=messages,
        temperature=0.6,
        max_tokens=8192,
        top_p=1,
        stream=True,
    )

    for chunk in response_stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content
