import openai

# Initialize API clients
openai.api_key = "your-openai-api-key"

def run_prompt(prompt, model):
    if model in ["GPT-3", "GPT-4"]:
        return run_openai_prompt(prompt, model)
    else:
        return "Unsupported model selected"

def run_openai_prompt(prompt, model):
    model_name = "gpt-3.5-turbo" if model == "GPT-3" else "gpt-4"
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].message['content'].strip()
