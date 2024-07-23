import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
deepinfra_api_key = os.getenv("DEEPINFRA_API_KEY")

client = OpenAI(
  base_url="https://api.deepinfra.com/v1/openai",
  api_key=deepinfra_api_key,
)

stream  = client.chat.completions.create(
  model="meta-llama/Meta-Llama-3-8B-Instruct",
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