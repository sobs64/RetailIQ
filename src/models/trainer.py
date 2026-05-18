import os
import pandas as pd
import joblib
import shap

from xgboost import XGBClassifier
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

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

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "bangalore_features.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model"
)

os.makedirs(MODEL_PATH, exist_ok=True)

# -----------------------------
# LOAD DATA
# -----------------------------

df = pd.read_csv(DATA_PATH)

print(f"Loaded {len(df)} rows")

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

X = df[features]

y = df["is_good_location"]

# -----------------------------
# TRAIN TEST SPLIT
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# -----------------------------
# MODEL
# -----------------------------

model = XGBClassifier(
    n_estimators=300,
    max_depth=5,
    learning_rate=0.05,
    random_state=42
)

model.fit(X_train, y_train)

# -----------------------------
# EVALUATION
# -----------------------------

y_pred = model.predict(X_test)

acc = accuracy_score(y_test, y_pred)

print(f"\nAccuracy: {acc:.4f}")

# -----------------------------
# FEATURE IMPORTANCE
# -----------------------------

print("\nFeature Importance:")

for feature, importance in zip(
    features,
    model.feature_importances_
):
    print(f"{feature}: {importance:.4f}")

# -----------------------------
# SHAP
# -----------------------------

explainer = shap.TreeExplainer(model)

# -----------------------------
# KMEANS
# -----------------------------

cluster_model = KMeans(
    n_clusters=3,
    random_state=42
)

cluster_model.fit(
    df[[
        "competitor_count_1km",
        "area_store_density_3km"
    ]]
)

# -----------------------------
# SAVE MODELS
# -----------------------------

joblib.dump(
    model,
    os.path.join(
        MODEL_PATH,
        "xgb_model.pkl"
    )
)

joblib.dump(
    cluster_model,
    os.path.join(
        MODEL_PATH,
        "kmeans_model.pkl"
    )
)

joblib.dump(
    explainer,
    os.path.join(
        MODEL_PATH,
        "shap_explainer.pkl"
    )
)

# -----------------------------
# COMPLETE
# -----------------------------

print("\n✅ MODELS SAVED SUCCESSFULLY")