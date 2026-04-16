import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
import joblib

# -----------------------------
# PATH SETUP
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "bangalore_features.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model", "location_model.pkl")

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv(DATA_PATH)

# -----------------------------
# NEW FEATURE (IMPORTANT)
# -----------------------------
df["competition_ratio"] = df["competitor_count_1km"] / (
    df["area_store_density_3km"] + 1
)

# -----------------------------
# TARGET (FIXED - NO LEAKAGE)
# -----------------------------
df["is_good_location"] = (
    df["location_score"] > df["location_score"].quantile(0.6)
).astype(int)

# -----------------------------
# FEATURES
# -----------------------------
features = [
    "competitor_count_1km",
    "area_store_density_3km",
    "competition_ratio",
    "is_high_competition"
]

X = df[features]
y = df["is_good_location"]

# -----------------------------
# TRAIN TEST SPLIT
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# MODEL
# -----------------------------
model = RandomForestClassifier(
    n_estimators=300,
    random_state=42
)

model.fit(X_train, y_train)

# -----------------------------
# EVALUATION
# -----------------------------
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")

# -----------------------------
# FEATURE IMPORTANCE
# -----------------------------
print("\nFeature Importance:")
for f, imp in zip(features, model.feature_importances_):
    print(f"{f}: {imp:.4f}")

# -----------------------------
# SAVE MODEL
# -----------------------------
os.makedirs(os.path.join(BASE_DIR, "model"), exist_ok=True)
joblib.dump(model, MODEL_PATH)

print("\n✅ Model saved successfully!")