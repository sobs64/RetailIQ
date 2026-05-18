import os
import pandas as pd
import streamlit as st
import folium

from folium.plugins import HeatMap
from streamlit_folium import st_folium

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="RetailIQ",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

/* Typography */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    scroll-behavior: smooth;
}

/* Animated gradient background */
@keyframes gradientShift {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

.stApp {
    background: linear-gradient(135deg, #0f172a, #020617);
    background-size: 400% 400%;
    animation: gradientShift 30s ease infinite;
    color: #f8fafc;
    padding-bottom: 2rem;
}

.block-container {
    padding-top: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* Header logo */
.logo {
    display: block;
    margin: 0 auto 1rem auto;
    width: 120px;
    filter: drop-shadow(0 0 8px rgba(0,255,255,0.6));
    transition: transform 0.3s ease;
}
.logo:hover {
    transform: scale(1.08);
}

.glass-card {
    background: linear-gradient(145deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.4) 100%);
    border-radius: 24px;
    padding: 32px;
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    margin-bottom: 24px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.glass-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.4);
    border: 1px solid rgba(255,255,255,0.1);
}

.title-text {
    font-size: 64px;
    font-weight: 800;
    background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 12px;
    letter-spacing: -1px;
    text-align: center;
}

.subtitle-text {
    color: #94a3b8;
    font-size: 22px;
    font-weight: 400;
    text-align: center;
    margin-bottom: 2rem;
}

.metric-card {
    background: linear-gradient(145deg, rgba(30,41,59,0.6) 0%, rgba(15,23,42,0.3) 100%);
    border-radius: 20px;
    padding: 24px;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.04);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
}

.metric-card:hover {
    border: 1px solid rgba(56, 189, 248, 0.3);
    box-shadow: 0 8px 25px rgba(56, 189, 248, 0.15);
    transform: translateY(-3px);
}

.metric-title {
    color: #94a3b8;
    font-size: 15px;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
    margin-bottom: 8px;
}

.metric-value {
    font-size: 38px;
    font-weight: 800;
    color: #f8fafc;
    background: linear-gradient(90deg, #f8fafc, #cbd5e1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.insight-box {
    background: rgba(16, 185, 129, 0.1);
    border-left: 4px solid #10b981;
    padding: 20px;
    border-radius: 12px;
    margin-top: 16px;
    color: #d1d5db;
    line-height: 1.6;
}

[data-testid="stDataFrame"] {
    border-radius: 20px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

h2 {
    color: #f8fafc !important;
    font-weight: 700 !important;
    padding-bottom: 16px;
}

hr {
    border-color: rgba(255, 255, 255, 0.1);
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# PATHS
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

FEATURE_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "bangalore_features.csv"
)

RECOMMENDATION_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "top_recommendations.csv"
)

# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv(FEATURE_PATH)

recommendations = pd.read_csv(
    RECOMMENDATION_PATH
)

# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="glass-card">
    <div class="title-text">
        🧠 RetailIQ
    </div>
    <div class="subtitle-text">
        AI-Powered Retail Location Intelligence Platform
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙ Controls")

top_n = st.sidebar.slider(
    "Top Recommendations",
    5,
    20,
    10
)

show_heatmap = st.sidebar.checkbox(
    "Show Demand Heatmap",
    value=True
)

show_existing = st.sidebar.checkbox(
    "Show Existing Stores",
    value=False
)

# =========================================================
# METRICS
# =========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Stores</div>
        <div class="metric-value">{len(df)}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Recommended Zones</div>
        <div class="metric-value">{len(recommendations)}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Top Score</div>
        <div class="metric-value">
            {round(recommendations['recommendation_score'].max(), 2)}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Avg Competition</div>
        <div class="metric-value">
            {round(df['competitor_count_1km'].mean(), 2)}
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# MAP TITLE
# =========================================================

st.markdown("## 🗺 Retail Opportunity Map")

# =========================================================
# MAP
# =========================================================

m = folium.Map(
    location=[12.97, 77.59],
    zoom_start=11,
    tiles="cartodb dark_matter"
)

# =========================================================
# HEATMAP
# =========================================================

if show_heatmap:

    heat_data = df[
        ["lat", "lng"]
    ].values.tolist()

    HeatMap(
        heat_data,
        radius=18,
        blur=15
    ).add_to(m)

# =========================================================
# EXISTING STORES
# =========================================================

if show_existing:

    for _, row in df.iterrows():

        folium.CircleMarker(
            location=[
                row["lat"],
                row["lng"]
            ],
            radius=3,
            color="cyan",
            fill=True,
            fill_opacity=0.4,
            popup=row["name"]
        ).add_to(m)

# =========================================================
# TOP RECOMMENDATIONS
# =========================================================

top_locations = recommendations.head(top_n)

for _, row in top_locations.iterrows():

    comp = row["competitor_count_1km"]
    demand = row["area_store_density_3km"]

    if comp <= 5:
        insight = (
            "Low competition with strong surrounding demand."
        )

    elif comp <= 12:
        insight = (
            "Balanced commercial zone with healthy retail activity."
        )

    else:
        insight = (
            "High-demand retail corridor with intense competition."
        )

    popup_html = f"""
    <div style="width:260px">

        <h3>📍 {row['area_name']}</h3>

        <hr>

        <b>Recommendation Score:</b>
        {round(row['recommendation_score'],2)}

        <br><br>

        <b>Competition Nearby:</b>
        {comp}

        <br>

        <b>Demand Density:</b>
        {demand}

        <br><br>

        <b>AI Insight:</b>

        <br>

        {insight}

    </div>
    """

    folium.CircleMarker(
        location=[
            row["lat"],
            row["lng"]
        ],
        radius=9,
        color="lime",
        fill=True,
        fill_color="lime",
        fill_opacity=0.85,
        popup=folium.Popup(
            popup_html,
            max_width=300
        )
    ).add_to(m)

# =========================================================
# DISPLAY MAP
# =========================================================

st.markdown("<div class='map-container'>", unsafe_allow_html=True)
st_folium(
    m,
    width=1400,
    height=700
)
st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# AI INSIGHTS
# =========================================================

st.markdown("## 🤖 AI Insights")

best = recommendations.iloc[0]

col1, col2 = st.columns(2)

with col1:

    st.markdown(f"""
    <div class="glass-card">

        <h2>🏆 Best Recommended Area</h2>

        <h1>{best['area_name']}</h1>

        <hr>

        <p><b>Recommendation Score:</b>
        {round(best['recommendation_score'],2)}</p>

        <p><b>Competition Nearby:</b>
        {int(best['competitor_count_1km'])}</p>

        <p><b>Demand Density:</b>
        {int(best['area_store_density_3km'])}</p>

    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown(f"""
    <div class="glass-card">

        <h2>📈 Strategic Business Insight</h2>

        <div class="insight-box">

        <b>{best['area_name']}</b> demonstrates strong retail expansion potential.

        <br><br>

        ✅ Strong surrounding commercial activity

        <br>

        ✅ Healthy customer density signals

        <br>

        ✅ High retail engagement potential

        <br>

        ⚠ Competition exists but demand appears capable of sustaining additional retail operations.

        <br><br>

        💡 Recommended for supermarkets, hypermarkets, and expansion-focused retail brands.

        </div>

    </div>
    """, unsafe_allow_html=True)

# =========================================================
# TABLE
# =========================================================

st.markdown("## 🏆 Top Recommended Retail Zones")

display_cols = [
    "area_name",
    "recommendation_score",
    "competitor_count_1km",
    "area_store_density_3km"
]

st.dataframe(
    recommendations[
        display_cols
    ].head(top_n),
    use_container_width=True
)

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<br><br>

<center>

Built with ❤️ using Machine Learning,
Geospatial Analytics,
XGBoost,
and Explainable AI

</center>
""", unsafe_allow_html=True)