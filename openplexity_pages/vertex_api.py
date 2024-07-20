import os
from google.oauth2 import service_account
import vertexai
from vertexai.generative_models import GenerationConfig
from vertexai.preview.generative_models import GenerativeModel as PreviewGenerativeModel
import re

def generate_stream(prompt):
    # Set the path to the new service account JSON file
    service_account_file = "./gemini-advanced-4c22cc22d8c3.json"

    # Check if the file exists
    if not os.path.exists(service_account_file):
        raise FileNotFoundError(f"The service account file '{service_account_file}' does not exist.")

    # Create credentials object
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file,
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )

    # Initialize Vertex AI with credentials
    vertexai.init(project="gemini-advanced", location="europe-central2", credentials=credentials)

    # Define generation config
    generation_config = GenerationConfig(
        max_output_tokens=8192,
        temperature=0.0,  # Set to 0.0 for ideal results with grounding
        top_p=0.8,
    )

    # Create the model
    model = PreviewGenerativeModel("gemini-pro")
    
    # Generate content with streaming
    response = model.generate_content(
        prompt,
        generation_config=generation_config,
        stream=True
    )

    # Variable to store the full raw response
    full_raw_response = ""

    # Yield each chunk of the response
    for chunk in response:
        if chunk.text:
            full_raw_response += chunk.text
            yield chunk.text

    # Print the full raw response to console
    print("Raw API Response:")
    print(full_raw_response)

def extract_citations(text):
    # Extract sources from the end of the text
    sources_match = re.search(r'\*\*Sources:\*\*\n(.*)', text, re.DOTALL)
    if sources_match:
        sources_text = sources_match.group(1)
        citations = []
        for line in sources_text.split('\n'):
            if line.strip():
                parts = line.split(': ', 1)
                if len(parts) == 2:
                    citations.append({"title": parts[0].strip('* '), "url": parts[1].strip()})
        return citations
    return []

def format_response_with_citations(response, citations):
    formatted_response = re.sub(r'\*\*Sources:\*\*\n.*', '', response, flags=re.DOTALL).strip()

    for i, citation in enumerate(citations, 1):
        citation_marker = f"[^{i}]({citation['url']})"
        
        sentences = re.split('(?<=[.!?]) +', formatted_response)
        
        most_relevant_sentence = max(sentences, key=lambda s: len(set(s.lower().split()) & set(citation['title'].lower().split())))
        
        formatted_response = formatted_response.replace(most_relevant_sentence, f"{most_relevant_sentence}{citation_marker}")

    formatted_response += "\n\n## Sources\n"
    for i, citation in enumerate(citations, 1):
        formatted_response += f"{i}. [{citation['title']}]({citation['url']})\n"
    
    return formatted_response