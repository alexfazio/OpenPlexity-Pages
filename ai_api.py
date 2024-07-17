from openai import OpenAI
import os
import streamlit as st


def run_prompt(prompt, API_ENDPOINT, API_KEY):
    messages = [
      {
          "role": "system",
          "content": (
              "You are an artificial intelligence assistant and you need to "
              "engage in a helpful, detailed, polite conversation with a user."
              "Provide citations for every affirmation."
              "Reply in Markdown format only."
          ),
      },
      {
          "role": "user",
          "content": prompt,
      },
    ]
    model_name = ""
    print("openai api key: ", API_KEY)
    print("openai api endpoint: ", API_ENDPOINT)
    client = OpenAI(api_key=API_KEY, base_url=API_ENDPOINT)
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        max_tokens=150,
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content