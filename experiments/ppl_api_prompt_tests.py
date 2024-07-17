import logging
# import warnings

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def ppl_query_api(system_prompt):
    from openai import OpenAI
    from dotenv import load_dotenv
    import os

    logging.info("STARTING ppl_query_api")

    # Load environment variables from .env file
    load_dotenv()

    # Access the API key
    pplx_api = os.getenv("pplx_api")

    messages = [
        {
            "role": "system",
            "content": (
                "You are an artificial intelligence assistant and you need to "
                "engage in a helpful, detailed, polite conversation with a user."
            ),
        },
        {
            "role": "user",
            "content": (
                "How many stars are in the universe?"
            ),
        },
    ]

    client = OpenAI(api_key=pplx_api, base_url="https://api.perplexity.ai")

    # chat completion without streaming
    response = client.chat.completions.create(
        model="llama-3-sonar-large-32k-online",
        messages=messages,
    )

    logging.info("RESULT ppl_query_api")

    print(response.choices[0].message.content)

    logging.info("ENDING ppl_query_api")

    # Access and return the content of the message
    return response.choices[0].message.content


system_prompt = """
                You are an experienced writer tasked with creating a high-quality academic piece. Your goal is to write a well-researched, detailed, and comprehensive chapter for a work discussing the topic: The Impact of Climate Change on Global Agriculture. Follow these instructions carefully to produce an excellent piece of writing:

1. Begin by thoroughly researching the topic. Use reputable academic sources, peer-reviewed journals, and authoritative books to gather information. Take detailed notes and organize your findings.

2. Plan your chapter structure. If it's an introduction, provide context, state the purpose, and outline the main points. For a chapter, organize your content logically with clear headings and subheadings. If it's a conclusion, summarize key points and provide final thoughts or recommendations.

3. Write in a formal tone. Maintain this tone consistently throughout your writing. Use formal language appropriate for academic writing, avoiding colloquialisms and overly casual expressions.

4. Provide a comprehensive overview of the subject matter. Present logical arguments or analyses, and substantiate them with relevant sources, theories, or data. Ensure each paragraph has a clear topic sentence and supporting details.

5. Incorporate current and relevant references to support your points. Use in-text citations according to the appropriate academic style guide (e.g., APA, MLA, Chicago). Include a mix of seminal works and recent research to show a thorough understanding of the field.

6. Use precise and clear language. Define any technical terms or jargon that may be unfamiliar to some readers. Use transitions effectively to ensure smooth flow between ideas and paragraphs.

7. Format your document according to standard academic writing guidelines. Use a consistent font and size, appropriate line spacing, and proper margins. If including figures or tables, ensure they are properly labeled and referenced in the text.

8. Proofread your work carefully for clarity, coherence, grammar, and punctuation. Pay special attention to sentence structure, verb tense consistency, and proper use of academic vocabulary.

9. Ensure your writing is original and properly cited. Avoid plagiarism by paraphrasing ideas from sources and giving credit where due.

10. Your final output should be the completed chapter only, without any additional comments or explanations. Begin your response with the appropriate heading (e.g., "Introduction", "Chapter X: [Relevant Title]", or "Conclusion") and end it when the section is complete.

Remember, you are writing as an experienced environmental scientist. Draw upon the expertise and perspective associated with this role throughout your writing.

Begin writing your chapter now, incorporating all the above guidelines. Do not include any meta-commentary or additional text outside of the actual chapter content.
                """

ppl_query_api(system_prompt)
