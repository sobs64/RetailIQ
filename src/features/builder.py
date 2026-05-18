import os
import pandas as pd
import numpy as np
from sklearn.neighbors import BallTree

# -----------------------------
# BASE PATHS
# -----------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

RAW_PATH = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "bangalore_supermarkets.csv"
)

PROCESSED_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed"
)

GRID_PATH = os.path.join(
    BASE_DIR,
    "data",
    "grid"
)

os.makedirs(PROCESSED_PATH, exist_ok=True)
os.makedirs(GRID_PATH, exist_ok=True)

# -----------------------------
# LOAD DATA
# -----------------------------

df = pd.read_csv(RAW_PATH)

print(f"Loaded {len(df)} stores")

# -----------------------------
# CLEAN DATA
# -----------------------------

df = df.dropna(subset=["lat", "lng"])

# -----------------------------
# BALLTREE
# -----------------------------

coords = df[["lat", "lng"]].values
coords_rad = np.radians(coords)

tree = BallTree(coords_rad, metric="haversine")

# -----------------------------
# FEATURE 1: COMPETITION
# -----------------------------

comp_radius_km = 1
comp_radius_rad = comp_radius_km / 6371

competitor_counts = tree.query_radius(
    coords_rad,
    r=comp_radius_rad,
    count_only=True
)

df["competitor_count_1km"] = competitor_counts - 1

# -----------------------------
# FEATURE 2: AREA DENSITY
# -----------------------------

density_radius_km = 3
density_radius_rad = density_radius_km / 6371

density_counts = tree.query_radius(
    coords_rad,
    r=density_radius_rad,
    count_only=True
)

df["area_store_density_3km"] = density_counts

# -----------------------------
# FEATURE 3: COMPETITION RATIO
# -----------------------------

df["competition_ratio"] = (
    df["competitor_count_1km"] /
    (df["area_store_density_3km"] + 1)
)

# -----------------------------
# FEATURE 4: REVIEW FEATURES
# -----------------------------

df["log_reviews"] = np.log1p(
    df["user_ratings_total"]
)

# -----------------------------
# FEATURE 5: SUCCESS SCORE
# -----------------------------

df["success_score"] = (
    df["rating"] *
    df["log_reviews"]
)

# -----------------------------
# TARGET VARIABLE
# -----------------------------

threshold = df["success_score"].quantile(0.6)

df["is_good_location"] = (
    df["success_score"] > threshold
).astype(int)

# -----------------------------
# FEATURE 6: HIGH COMPETITION
# -----------------------------

median_comp = df["competitor_count_1km"].median()

df["is_high_competition"] = (
    df["competitor_count_1km"] > median_comp
).astype(int)

# -----------------------------
# FEATURE 7: LOCATION SCORE
# -----------------------------

df["location_score"] = (
    (df["area_store_density_3km"] * 0.7)
    -
    (df["competitor_count_1km"] * 0.3)
)

# -----------------------------
# GRID GENERATION
# -----------------------------

print("Generating grid points...")

lat_min = df["lat"].min()
lat_max = df["lat"].max()

lng_min = df["lng"].min()
lng_max = df["lng"].max()

# Better density
grid_step = 0.005

lat_range = np.arange(lat_min, lat_max, grid_step)
lng_range = np.arange(lng_min, lng_max, grid_step)

grid_points = []

for lat in lat_range:
    for lng in lng_range:
        grid_points.append([lat, lng])

grid_df = pd.DataFrame(
    grid_points,
    columns=["lat", "lng"]
)

print(f"Generated {len(grid_df)} grid points")

# -----------------------------
# GRID FEATURES
# -----------------------------

grid_coords = grid_df[["lat", "lng"]].values
grid_coords_rad = np.radians(grid_coords)

grid_comp = tree.query_radius(
    grid_coords_rad,
    r=comp_radius_rad,
    count_only=True
)

grid_density = tree.query_radius(
    grid_coords_rad,
    r=density_radius_rad,
    count_only=True
)

grid_df["competitor_count_1km"] = grid_comp

grid_df["area_store_density_3km"] = grid_density

grid_df["competition_ratio"] = (
    grid_df["competitor_count_1km"] /
    (grid_df["area_store_density_3km"] + 1)
)

grid_df["is_high_competition"] = (
    grid_df["competitor_count_1km"] > median_comp
).astype(int)

# Placeholder values
grid_df["log_reviews"] = df["log_reviews"].median()
grid_df["rating"] = df["rating"].median()

# -----------------------------
# SAVE FILES
# -----------------------------

processed_save = os.path.join(
    PROCESSED_PATH,
    "bangalore_features.csv"
)

grid_save = os.path.join(
    GRID_PATH,
    "bangalore_grid.csv"
)

df.to_csv(processed_save, index=False)

grid_df.to_csv(grid_save, index=False)

# -----------------------------
# FINAL OUTPUT
# -----------------------------

print("\n✅ FEATURE ENGINEERING COMPLETE")

print("\nProcessed dataset:")
print(processed_save)

print("\nGrid dataset:")
print(grid_save)

print(f"\nStore Rows: {len(df)}")
print(f"Grid Rows: {len(grid_df)}")