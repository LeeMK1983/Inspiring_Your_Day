# Phase 3: Code Each Module

import json
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import os
import random

# Load the Quote Pool
def load_quote_dataset(path=os.path.join(os.path.dirname(__file__), "quotes.json")):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

# Load Image Pool (URL-based)
def load_image_pool(path=os.path.join(os.path.dirname(__file__), "images.json")):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

# Select the Best Quote Based on Tags
def select_relevant_quote(user_tags, quotes):
    best_quote = []
    highest_score = 0 

    for quote in quotes:
        match_score = len(set(user_tags).intersection(set(quote["tags"])))
        print("QUOTE DEBUG:", quote, type(quote))
        if match_score > highest_score:
            highest_score = match_score
            best_quote = [quote]
        elif match_score == highest_score:
            best_quote.append(quote)
    
    if best_quote:
        print("Best Quote", best_quote)
        return random.choice(best_quote) # randomly choose among top matches
    else:
        return None # no good match found

# Select Image by Mood Tag
def get_image_url(tag, image_pool):
    return image_pool.get(tag, image_pool.get("default", None))

def load_image_from_url(url, size=(300, 300)):
    try:
        print("Fetching image from:", url)
        response = requests.get(url)                # Download the Image _ This line sends an HTTP GET request to the URL, if successful, it retrieves the image binary data from the internet
        print("HTTP status:", response.status_code)

        img = Image.open(BytesIO(response.content)) # Convert Binary to Image _ response.content is raw image bytes, BytesIO turns it into a readable stream(file-like object), Image.open from PIL loads the image from the stream
        img = img.resize(size, Image.Resampling.LANCZOS)     # Resizes the image to the size specified, Image.ANTIALIAS ensures the resized image is smooth and high quality
        photo = ImageTk.PhotoImage(img)
        return photo              # ImageTk.PhotoImage() converts the Pillow image into a format that tkinter can display (tkinter-compatible)
    
    except Exception as e:
        print("Image load failed:", e)
        return None