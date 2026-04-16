# 🛒 Retail Location Intelligence System

An end-to-end **ML-powered geospatial recommendation system** that identifies high-potential locations for opening supermarkets using demand and competition analysis.

---

## 🚀 Overview

Choosing the right location is critical for retail success.  
This project uses **spatial data + machine learning** to recommend optimal supermarket locations in Bangalore.

It answers:

> **"Where should I open a new supermarket?"**

---

## 🔥 Features

- 📍 **Geospatial Analysis**
  - Uses latitude/longitude data of supermarkets
  - Multi-scale spatial modeling (1km vs 3km)

- 🧠 **Machine Learning Model**
  - Classifies locations as *Good* or *Not Recommended*
  - Uses features like demand, competition, and ratios

- 🗺️ **Interactive Dashboard**
  - Built with Streamlit + Folium
  - Visual map with recommended locations

- 📊 **Explainability**
  - Shows demand vs competition insights
  - Provides human-readable reasoning

- 🎯 **Custom Location Prediction**
  - Input any latitude & longitude
  - Get real-time ML prediction + confidence

---

## 🧠 Methodology

### 1. Data Collection
- Google Maps Places API used to collect supermarket data in Bangalore

### 2. Feature Engineering
- `competitor_count_1km` → local competition
- `area_store_density_3km` → demand proxy
- `competition_ratio` → balance between demand & competition

### 3. ML Model
- Random Forest Classifier
- Target: high-potential vs low-potential locations

### 4. Scoring + Prediction
- ML predicts whether a location is suitable for a new store
- Confidence score included

---

## 🏗️ Project Structure
```
retail-location-ml/
│
├── data/
│ ├── bangalore_supermarkets.csv
│ └── bangalore_features.csv
│
├── src/
│ ├── data_collection.py
│ ├── feature_engineering.py
│ └── model.py
│
├── model/
│ └── location_model.pkl
│
├── app/
│ └── streamlit_app.py
│
├── requirements.txt
├── .env (not committed)
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone repository

```bash
git clone https://github.com/sobs64/RetailIQ.git
cd RetailIQ