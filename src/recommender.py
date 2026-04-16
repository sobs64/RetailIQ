import os
import pandas as pd

# Path setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data")

# Load data
df = pd.read_csv(os.path.join(DATA_PATH, "bangalore_features.csv"))

# Sort by best locations
df_sorted = df.sort_values(by="location_score", ascending=False)

# Top 10 locations
top_locations = df_sorted.head(10)

print("\n🔥 Top 10 Recommended Locations:\n")
print(top_locations[["name", "vicinity", "location_score"]])