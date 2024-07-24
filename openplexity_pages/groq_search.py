import os
from groq import Groq
import json
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Groq client
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
SERPER_API_KEY = os.getenv('SERPER_API_KEY')

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set")
client = Groq(api_key=GROQ_API_KEY)
MODEL = 'llama3-groq-70b-8192-tool-use-preview'

def google_search(query):
    """Perform a Google search using Serper API and return detailed results"""
    url = 'https://google.serper.dev/search'
    payload = json.dumps({
        'q': query,
        'num': 5,  # Request 10 results
        'gl': 'us',
        'hl': 'en',
        'type': 'search'
    })
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload)
    results = response.json().get('organic', [])
    
    formatted_results = ["Search results:"]
    for r in results:
        formatted_result = f"Title: {r.get('title', '')}\nLink: {r.get('link', '')}\nSnippet: {r.get('snippet', '')}\n---"
        formatted_results.append(formatted_result)
    
    return "\n".join(formatted_results)

def run_conversation(user_prompt):
    messages = [
        {
            "role": "system",
            "content": """
            You are an AI assistant designed to help with Google searches and provide comprehensive answers based on the search results. Your task is to use the google_search function to find information and present the results in a clear and informative manner.
            
            To perform a search, use the following function:
            <function_call>google_search(query="{{QUERY}}")</function_call>
            
            The search results will include titles, links, and detailed snippets. Always cite the source of information by mentioning the link when providing answers.
            
            Present the search results in the following format:
            
            ```
            Search results:
            Title: [Title of the search result]
            Link: [URL of the search result]
            Snippet: [Snippet from the search result]
            ---
            [Repeat for each search result]
            ```
            
            After presenting the search results, provide a comprehensive answer to the query based on the information found. Synthesize the information from multiple sources when possible, and always cite the sources by mentioning the relevant links.
            
            Here is the query to search for:
            <query>{{QUERY}}</query>
            
            Begin by performing the search using the google_search function. Then, present the search results in the specified format. Finally, provide your answer to the query based on the search results.
            
            If the google_search function returns an error or no results, inform the user that the search was unsuccessful and that you are unable to provide an answer based on the given query.
            
            Present your final answer within <answer> tags.
            """
        },
        {
            "role": "user",
            "content": user_prompt,
        }
    ]
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "google_search",
                "description": "Perform a Google search and return top 5 results",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query",
                        }
                    },
                    "required": ["query"],
                },
            },
        }
    ]

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            max_tokens=4096
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            available_functions = {
                "google_search": google_search,
            }
            messages.append(response_message)

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(
                    query=function_args.get("query")
                )
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )

            second_response = client.chat.completions.create(
                model=MODEL,
                messages=messages
            )
            return second_response.choices[0].message.content
        else:
            return response_message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"