import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()
hf_api_key = os.getenv("HUGGING_FACE_API_KEY")


client = InferenceClient(
    "meta-llama/Meta-Llama-3-8B-Instruct",
    token=hf_api_key,
)

for message in client.chat_completion(
	messages=[{"role": "user", "content": "What is the capital of France?"}],
	max_tokens=500,
	stream=True,
):
    print(message.choices[0].delta.content, end="")