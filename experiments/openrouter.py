import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
operouter_api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=operouter_api_key,
)

stream  = client.chat.completions.create(
  model="meta-llama/llama-3-8b-instruct:free",
  messages=[
    {
      "role": "user",
      "content": "Say this is a test",
    },
  ],
  stream=True,
)
# Print the streamed response
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end='', flush=True)
print()  # Add a newline at the end