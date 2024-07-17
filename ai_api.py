from openai import OpenAI
import streamlit as st


def run_prompt(prompt, API_ENDPOINT, API_KEY, role="user"):
    messages = [
      {
          "role": "system",
          "content": (
              "You are an artificial intelligence assistant and you need to "
              "respond accordingly."
              "Provide citations for every affirmation."
              "Reply in Markdown format only."
          ),
      },
      {
          "role": role,
          "content": prompt,
      },
    ]
    model_name = ""
    client = OpenAI(api_key=API_KEY, base_url=API_ENDPOINT)
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        max_tokens=450,
    )
    return response.choices[0].message.content