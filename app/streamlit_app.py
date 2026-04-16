import pandas as pd
import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import numpy as np
from sklearn.neighbors import BallTree
import joblib
import os

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="Retail Location Intelligence",
    layout="wide",
    page_icon="🛒"
)

# -----------------------------
# PATHS
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "bangalore_features.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model", "location_model.pkl")

# -----------------------------
# LOAD DATA + MODEL
# -----------------------------
df = pd.read_csv(DATA_PATH)
model = joblib.load(MODEL_PATH)

coords = df[["lat", "lng"]].values
coords_rad = np.radians(coords)
tree = BallTree(coords_rad, metric="haversine")

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("⚙️ Controls")

top_n = st.sidebar.slider("Top Locations", 5, 50, 10)
show_all = st.sidebar.checkbox("Show All Stores")
show_heatmap = st.sidebar.checkbox("Show Demand Heatmap")

st.sidebar.markdown("---")
st.sidebar.subheader("📍 Custom Location")

custom_lat = st.sidebar.number_input("Latitude", value=12.97)
custom_lng = st.sidebar.number_input("Longitude", value=77.59)

# -----------------------------
# HEADER
# -----------------------------
st.title("🛒 Retail Location Intelligence Dashboard")
st.caption("ML-powered system for supermarket expansion")

# -----------------------------
# KPIs
# -----------------------------
col1, col2, col3 = st.columns(3)
col1.metric("Total Locations", len(df))
col2.metric("Avg Competition", round(df["competitor_count_1km"].mean(), 2))
col3.metric("Avg Demand", round(df["area_store_density_3km"].mean(), 2))

# -----------------------------
# FILTER DATA
# -----------------------------
top_locations = df.sort_values(
    by="location_score",
    ascending=False
).head(top_n)

# -----------------------------
# MAP
# -----------------------------
st.subheader("🗺️ Location Intelligence Map")

map_center = [df["lat"].mean(), df["lng"].mean()]
m = folium.Map(location=map_center, zoom_start=12)

def get_color(score):
    if score > 50:
        return "green"
    elif score > 30:
        return "orange"
    else:
        return "red"

# Plot recommended
for _, row in top_locations.iterrows():
    folium.Marker(
        location=[row["lat"], row["lng"]],
        popup=f"{row['name']}<br>Score: {round(row['location_score'],2)}",
        icon=folium.Icon(color=get_color(row["location_score"]))
    ).add_to(m)

# Show all stores
if show_all:
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lng"]],
            radius=2,
            color="blue",
            fill=True,
            fill_opacity=0.2
        ).add_to(m)

# Heatmap
if show_heatmap:
    HeatMap(df[["lat", "lng"]].values.tolist()).add_to(m)

# -----------------------------
# ML PREDICTION 🔥
# -----------------------------
point = np.radians([[custom_lat, custom_lng]])

comp = tree.query_radius(point, r=1/6371, count_only=True)[0]
demand = tree.query_radius(point, r=3/6371, count_only=True)[0]

is_high = int(comp > 5)
ratio = comp / (demand + 1)

features = np.array([[comp, demand, ratio, is_high]])

prediction = model.predict(features)[0]
prob = model.predict_proba(features)[0][prediction]

# Verdict
if prediction == 1:
    verdict = "🟢 Good Location"
else:
    verdict = "🔴 Not Recommended"

# Add marker
folium.Marker(
    location=[custom_lat, custom_lng],
    popup=f"Prediction: {verdict}<br>Confidence: {round(prob*100,2)}%",
    icon=folium.Icon(color="purple")
).add_to(m)

# -----------------------------
# DISPLAY MAP
# -----------------------------
st_folium(m, width=1200, height=550)

# -----------------------------
# INSIGHT PANEL
# -----------------------------
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Top Locations")
    st.dataframe(
        top_locations[["name", "vicinity", "location_score"]],
        use_container_width=True
    )

with col2:
    st.subheader("🤖 ML Prediction")

    st.markdown(f"""
    **Latitude:** {custom_lat}  
    **Longitude:** {custom_lng}

    ---
    **Demand (3km):** {demand}  
    **Competition (1km):** {comp}

    ---
    ### {verdict}
    **Confidence:** {round(prob*100,2)}%
    """)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("ML + Geospatial Intelligence • Streamlit")