import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
SERPER_API_KEY = os.getenv('SERPER_API_KEY')

def search_images(query, num_images=6):
    url = "https://google.serper.dev/images"
    payload = json.dumps({
        "q": query,
        "num": min(num_images, 6)  # Limit the number of images to a maximum of 6
    })
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        images = response.json()['images']
        return images[:6]  # Return only the first 6 images
    except requests.RequestException as e:
        print(f"Error occurred while making API call: {e}")
        return None