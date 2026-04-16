import requests
import pandas as pd
import time
import os
from dotenv import load_dotenv

# -----------------------------
# LOAD ENV VARIABLES
# -----------------------------
load_dotenv()

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

if not API_KEY:
    raise ValueError("API key not found. Check your .env file.")

# -----------------------------
# PATH SETUP
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_PATH, exist_ok=True)

# -----------------------------
# LOCATIONS
# -----------------------------
locations = [
    "12.9716,77.5946",  # Central Bangalore
    "12.9352,77.6245",  # Koramangala
    "12.9279,77.6271",  # HSR Layout
    "13.0358,77.5970",  # Hebbal
    "12.9698,77.7499",  # Whitefield
    "12.9141,77.6100",  # BTM
    "13.0067,77.5750",  # Rajajinagar
    "12.9784,77.6408",  # Indiranagar
]

url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

all_places = []

# -----------------------------
# FETCH DATA
# -----------------------------
for loc in locations:
    params = {
        "location": loc,
        "radius": 3000,
        "type": "supermarket",
        "key": API_KEY
    }

    while True:
        response = requests.get(url, params=params).json()

        for place in response.get("results", []):
            all_places.append({
                "name": place.get("name"),
                "lat": place["geometry"]["location"]["lat"],
                "lng": place["geometry"]["location"]["lng"],
                "rating": place.get("rating", 0),
                "user_ratings_total": place.get("user_ratings_total", 0),
                "vicinity": place.get("vicinity")
            })

        next_page_token = response.get("next_page_token")

        if not next_page_token:
            break

        time.sleep(2)  # required for next_page_token
        params = {
            "pagetoken": next_page_token,
            "key": API_KEY
        }

# -----------------------------
# SAVE DATA
# -----------------------------
df = pd.DataFrame(all_places)

df = df.drop_duplicates(subset=["name", "lat", "lng"])

df.to_csv(os.path.join(DATA_PATH, "bangalore_supermarkets.csv"), index=False)

print("Final count:", len(df))