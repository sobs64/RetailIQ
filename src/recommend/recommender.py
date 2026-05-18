import os
import pandas as pd
import joblib

from geopy.geocoders import Nominatim

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

GRID_PATH = os.path.join(
    BASE_DIR,
    "data",
    "grid",
    "bangalore_grid.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "xgb_model.pkl"
)

# -----------------------------
# LOAD GRID DATA
# -----------------------------

print("Loading grid dataset...")

grid_df = pd.read_csv(GRID_PATH)

print(f"Loaded {len(grid_df)} grid points")

# -----------------------------
# LOAD MODEL
# -----------------------------

print("Loading trained model...")

model = joblib.load(MODEL_PATH)

# -----------------------------
# FEATURES
# -----------------------------

features = [
    "competitor_count_1km",
    "area_store_density_3km",
    "competition_ratio",
    "is_high_competition",
    "log_reviews",
    "rating"
]

# -----------------------------
# ML PREDICTIONS
# -----------------------------

print("Generating ML predictions...")

ml_predictions = model.predict_proba(
    grid_df[features]
)[:, 1]

grid_df["ml_score"] = ml_predictions

# -----------------------------
# HYBRID RECOMMENDATION SCORE
# -----------------------------

grid_df["recommendation_score"] = (
    (grid_df["area_store_density_3km"] * 0.7)
    -
    (grid_df["competitor_count_1km"] * 0.3)
    +
    (grid_df["ml_score"] * 100)
)

# -----------------------------
# SORT BEST LOCATIONS
# -----------------------------

top_locations = grid_df.sort_values(
    by="recommendation_score",
    ascending=False
)

top_20 = top_locations.head(20).copy()

# -----------------------------
# REVERSE GEOCODING
# -----------------------------

print("Fetching area names...")

geolocator = Nominatim(
    user_agent="retailiq"
)

area_names = []

for _, row in top_20.iterrows():

    try:

        location = geolocator.reverse(
            f"{row['lat']}, {row['lng']}",
            timeout=10
        )

        address = location.raw.get(
            "address",
            {}
        )

        area = (
            address.get("suburb")
            or address.get("neighbourhood")
            or address.get("city_district")
            or address.get("town")
            or "Unknown Area"
        )

        area_names.append(area)

    except:
        area_names.append("Unknown Area")

top_20["area_name"] = area_names

# -----------------------------
# DISPLAY RESULTS
# -----------------------------

print("\n🔥 TOP 20 RECOMMENDED LOCATIONS\n")

print(
    top_20[
        [
            "area_name",
            "recommendation_score",
            "competitor_count_1km",
            "area_store_density_3km"
        ]
    ]
)

# -----------------------------
# SAVE RECOMMENDATIONS
# -----------------------------

SAVE_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "top_recommendations.csv"
)

top_20.to_csv(SAVE_PATH, index=False)

# -----------------------------
# COMPLETE
# -----------------------------

print("\n✅ Recommendations saved!")

print(f"\nSaved to:\n{SAVE_PATH}")