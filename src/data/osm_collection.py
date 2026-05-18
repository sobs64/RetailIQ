import os
import requests
import pandas as pd
import time
from dotenv import load_dotenv

# -----------------------------
# BASE PATH
# -----------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

# -----------------------------
# LOAD ENV
# -----------------------------

env_path = os.path.join(BASE_DIR, ".env")

load_dotenv(env_path)

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# -----------------------------
# DEBUG API KEY
# -----------------------------

if API_KEY:
    print("✅ API Key Loaded Successfully")
    print("Key Prefix:", API_KEY[:10])
else:
    print("❌ API Key NOT FOUND")
    exit()

# -----------------------------
# DATA PATH
# -----------------------------

RAW_PATH = os.path.join(BASE_DIR, "data", "raw")

os.makedirs(RAW_PATH, exist_ok=True)

# -----------------------------
# SEARCH LOCATIONS
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

# -----------------------------
# GOOGLE PLACES API
# -----------------------------

url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

all_places = []

# -----------------------------
# FETCH DATA
# -----------------------------

for loc in locations:

    print(f"\n📍 Fetching stores near: {loc}")

    params = {
        "location": loc,
        "radius": 3000,
        "type": "supermarket",
        "key": API_KEY
    }

    while True:

        response = requests.get(url, params=params).json()

        # -----------------------------
        # DEBUG ERRORS
        # -----------------------------

        if response.get("status") != "OK" and response.get("status") != "ZERO_RESULTS":

            print("\n❌ API ERROR:")
            print(response)

        # -----------------------------
        # EXTRACT RESULTS
        # -----------------------------

        for place in response.get("results", []):

            all_places.append({
                "name": place.get("name"),
                "lat": place["geometry"]["location"]["lat"],
                "lng": place["geometry"]["location"]["lng"],
                "rating": place.get("rating", 0),
                "user_ratings_total": place.get("user_ratings_total", 0),
                "vicinity": place.get("vicinity")
            })

        # -----------------------------
        # PAGINATION
        # -----------------------------

        next_page_token = response.get("next_page_token")

        if not next_page_token:
            break

        print("➡ Fetching next page...")

        time.sleep(2)

        params = {
            "pagetoken": next_page_token,
            "key": API_KEY
        }

# -----------------------------
# CREATE DATAFRAME
# -----------------------------

df = pd.DataFrame(all_places)

# -----------------------------
# REMOVE DUPLICATES
# -----------------------------

df = df.drop_duplicates(
    subset=["name", "lat", "lng"]
)

# -----------------------------
# SAVE
# -----------------------------

save_path = os.path.join(
    RAW_PATH,
    "bangalore_supermarkets.csv"
)

df.to_csv(save_path, index=False)

# -----------------------------
# FINAL OUTPUT
# -----------------------------

print("\n✅ DATA COLLECTION COMPLETE")
print("Saved:", save_path)
print("Total Stores:", len(df))