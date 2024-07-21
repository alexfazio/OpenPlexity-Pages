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
        "num": 30  # Request more images to account for filtering
    })
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        all_images = response.json()['images']
        
        print(f"Total images returned by API: {len(all_images)}")
        
        # Filter images based on aspect ratio (1.59:1) with a larger margin of error
        target_ratio = 1.59
        margin = 0.2  # 20% margin of error
        
        filtered_images = [
            img for img in all_images
            if 'width' in img and 'height' in img
            and abs((img['width'] / img['height']) - target_ratio) <= margin
            and not any(domain in img['imageUrl'].lower() for domain in ['savannahnow.com', 'creativefabrica.com'])
        ]
        
        print(f"Images after filtering: {len(filtered_images)}")
        
        # If no images match the criteria, return all images
        if not filtered_images:
            print("No images matched the criteria. Returning all images.")
            filtered_images = all_images
        
        # Return only the requested number of images
        return filtered_images[:num_images]
    except requests.RequestException as e:
        print(f"Error occurred while making API call: {e}")
        return None