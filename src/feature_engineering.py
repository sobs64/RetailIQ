import os
import pandas as pd
import numpy as np
from sklearn.neighbors import BallTree

# -----------------------------
# PATH SETUP
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data")

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv(os.path.join(DATA_PATH, "bangalore_supermarkets.csv"))

# -----------------------------
# GEO COORDINATES
# -----------------------------
coords = df[["lat", "lng"]].values
coords_rad = np.radians(coords)

tree = BallTree(coords_rad, metric="haversine")

radius = 1 / 6371  # 1 km

# -----------------------------
# COMPETITOR DENSITY
# -----------------------------
counts = tree.query_radius(coords_rad, r=radius, count_only=True)
df["competitor_count_1km"] = counts - 1

# -----------------------------
# DEMAND FEATURES (PROXY)
# -----------------------------
# Nearby store density (activity proxy)
# Larger radius for demand
large_radius = 3 / 6371  # 3 km

large_counts = tree.query_radius(coords_rad, r=large_radius, count_only=True)

df["area_store_density_3km"] = large_counts - 1

# Demand-supply ratio
df["demand_supply_ratio"] = 1 / (1 + df["competitor_count_1km"])

# Binary feature (non-linear signal)
df["is_high_competition"] = (df["competitor_count_1km"] > 5).astype(int)

# -----------------------------
# 🔥 FINAL LOCATION SCORE (IMPORTANT)
# -----------------------------
df["location_score"] = (
    df["area_store_density_3km"] * 0.7
    - df["competitor_count_1km"] * 1.0
)

# Optional (for reference only)
df["log_reviews"] = np.log1p(df["user_ratings_total"])

# -----------------------------
# SAVE
# -----------------------------
df.to_csv(os.path.join(DATA_PATH, "bangalore_features.csv"), index=False)

print("✅ Feature engineering complete (final version)!")