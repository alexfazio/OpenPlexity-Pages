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
        "q": f"{query} imagesize:1200x750",
        "num": num_images * 2  # Request more images to account for filtering
    })
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        all_images = response.json()['images']
        
        # Filter out problematic images
        filtered_images = [
            img for img in all_images
            if not any(domain in img['imageUrl'] for domain in ['savannahnow.com', 'creativefabrica.com'])
        ]
        
        # Return only the requested number of images
        return filtered_images[:num_images]
    except requests.RequestException as e:
        print(f"Error occurred while making API call: {e}")
        return None

def get_first_image_url(query):
    images = search_images(query, num_images=1)
    if images and len(images) > 0:
        return images[0]['imageUrl']
    return None

def get_first_image_url(query):
    images = search_images(query, num_images=1)
    if images and len(images) > 0:
        return images[0]['imageUrl']
    return None