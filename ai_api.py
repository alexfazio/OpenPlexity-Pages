from openai import OpenAI
import os
import streamlit as st


def run_prompt(prompt, OPENAI_API_ENDPOINT, OPENAI_API_KEY):
    # Initialize API clients
    # OPENAI_API_ENDPOINT = st.secrets("OPENAI_API_ENDPOINT")
    # OPENAI_API_KEY  = st.secrets("OPENAI_API_KEY")

    messages = [
      {
          "role": "system",
          "content": (
              "You are an artificial intelligence assistant and you need to "
              "engage in a helpful, detailed, polite conversation with a user."
              "Provide citations for every affirmation."
          ),
      },
      {
          "role": "user",
          "content": prompt,
      },
    ]
    model_name = ""
    print("openai api key: ", OPENAI_API_KEY)
    print("openai api endpoint: ", OPENAI_API_ENDPOINT)
    client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_ENDPOINT)
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content