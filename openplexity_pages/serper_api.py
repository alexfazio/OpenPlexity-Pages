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
        "num": 30  # Request a higher number of images from the API
    })
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        images = response.json()['images']
        
        # Function to calculate aspect ratio
        def calculate_aspect_ratio(image):
            width = image.get('imageWidth')
            height = image.get('imageHeight')
            if width and height:
                return height / width
            return None
        
        # Filter images based on aspect ratio
        filtered_images = [
            image for image in images
            if calculate_aspect_ratio(image) is not None and calculate_aspect_ratio(image) <= 9/16
        ]
        
        return filtered_images[:num_images]  # Return the desired number of filtered images
    except requests.RequestException as e:
        print(f"Error occurred while making API call: {e}")
        return None