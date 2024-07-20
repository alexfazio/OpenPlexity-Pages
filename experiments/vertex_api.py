import os
from google.oauth2 import service_account
import vertexai
from vertexai.generative_models import Part, GenerationConfig
from vertexai.preview.generative_models import GenerativeModel as PreviewGenerativeModel
from vertexai.preview.language_models import TextGenerationModel
import re

def generate():
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

    # Define the text prompt
    text1 = """Write a 60 word article section for the story titled 'Curiosity Mars Rover'. This section is titled 'The tech behind'. Please use the most up-to-date information available and include specific technical details. Cite your sources."""

    # Define generation config
    generation_config = GenerationConfig(
        max_output_tokens=8192,
        temperature=0.0,  # Set to 0.0 for ideal results with grounding
        top_p=0.8,
    )

    # Create the model
    model = PreviewGenerativeModel("gemini-pro")
    
    # Generate content
    response = model.generate_content(
        text1,
        generation_config=generation_config,
    )

    full_response = ""
    search_query = ""
    metadata = {}
    citations = []

    if response.text:
        full_response = response.text

    # Extract metadata and citations if available
    if hasattr(response, 'candidates') and response.candidates:
        candidate = response.candidates[0]
        if hasattr(candidate, 'citation_metadata'):
            metadata['citation_metadata'] = str(candidate.citation_metadata)
            if hasattr(candidate.citation_metadata, 'citations'):
                citations = [
                    {"url": citation.url, "title": citation.title}
                    for citation in candidate.citation_metadata.citations
                ]

    return full_response, search_query, metadata, citations

def format_response_with_citations(response, citations):
    formatted_response = response

    # Add inline citations
    for i, citation in enumerate(citations, 1):
        citation_marker = f"[^{i}]"
        if f"[{i}]" in formatted_response:
            formatted_response = formatted_response.replace(f"[{i}]", citation_marker)
        else:
            # If no placeholder exists, append the citation to the end of the relevant sentence
            sentences = formatted_response.split('. ')
            for j, sentence in enumerate(sentences):
                if citation['title'].lower() in sentence.lower():
                    sentences[j] = f"{sentence}{citation_marker}"
                    break
            formatted_response = '. '.join(sentences)

    # Add aggregate citations at the end
    formatted_response += "\n\n## Sources\n"
    for i, citation in enumerate(citations, 1):
        formatted_response += f"[^{i}]: [{citation['title']}]({citation['url']})\n"
    
    return formatted_response

if __name__ == "__main__":
    try:
        result, query, metadata, citations = generate()
        if result:
            print("\nGeneration completed successfully.")
            formatted_result = format_response_with_citations(result, citations)
            print("Final result with inline and aggregate citations (Markdown):")
            print(formatted_result)
            print("\nMetadata:")
            for key, value in metadata.items():
                print(f"{key}: {value}")
        else:
            print("\nGeneration did not produce a valid result.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")