# 🛒 Retail Location Intelligence System

An end-to-end **ML-powered geospatial recommendation system** that identifies high-potential locations for opening supermarkets using demand and competition analysis.

---

# 🚀 Overview

Choosing the right location is critical for retail success.  
This project uses **spatial data + machine learning** to recommend optimal supermarket locations in Bangalore.

It answers:

> **"Where should I open a new supermarket?"**

---

# 🔥 Features

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

# 🧠 Methodology

## 1. Data Collection
- Google Maps Places API used to collect supermarket data in Bangalore

## 2. Feature Engineering
- `competitor_count_1km` → local competition
- `area_store_density_3km` → demand proxy
- `competition_ratio` → balance between demand & competition

## 3. ML Model
- Random Forest Classifier
- Target: high-potential vs low-potential locations

## 4. Scoring + Prediction
- ML predicts whether a location is suitable for a new store
- Confidence score included

---

# 🏗️ Project Structure

```bash
retail-location-ml/
│
├── data/
│   ├── bangalore_supermarkets.csv
│   └── bangalore_features.csv
│
├── src/
│   ├── data_collection.py
│   ├── feature_engineering.py
│   └── model.py
│
├── model/
│   └── location_model.pkl
│
├── app/
│   └── streamlit_app.py
│
├── requirements.txt
├── .env (not committed)
└── README.md
```

---

# ⚙️ Setup Instructions

## 1. Clone Repository

```bash
git clone https://github.com/sobs64/RetailIQ.git
cd RetailIQ
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
GOOGLE_MAPS_API_KEY=your_api_key_here
```

---

# ▶️ Execution Steps

## Step 1: Collect Supermarket Data

Run the data collection script to fetch supermarket locations from Google Maps API.

```bash
python src/data_collection.py
```

### Output:
- `data/bangalore_supermarkets.csv`

---

## Step 2: Generate Features

Run feature engineering to compute demand and competition metrics.

```bash
python src/feature_engineering.py
```

### Output:
- `data/bangalore_features.csv`

---

## Step 3: Train Machine Learning Model

Train the Random Forest classifier.

```bash
python src/model.py
```

### Output:
- `model/location_model.pkl`

---

## Step 4: Launch Streamlit Dashboard

Start the interactive web application.

```bash
streamlit run app/streamlit_app.py
```

---

# 🖥️ Dashboard Features

- Interactive Bangalore supermarket map
- Location recommendation heat zones
- Competition analysis
- Real-time prediction for custom coordinates
- Confidence score visualization

---

# 📈 Sample Prediction Workflow

1. User enters latitude & longitude
2. System extracts nearby competition features
3. ML model predicts suitability
4. Dashboard displays:
   - Recommendation
   - Confidence Score
   - Demand vs Competition insights

---

# 🛠️ Tech Stack

- **Python**
- **Scikit-learn**
- **Pandas**
- **GeoPy**
- **Folium**
- **Streamlit**
- **Google Maps Places API**

---

# 🎯 Future Improvements

- Add demographic and income-level analysis
- Integrate traffic and mobility data
- Deep learning-based spatial analysis
- Real-time competitor updates
- Expansion to multiple cities

---

# 📌 Example Use Cases

- Retail expansion planning
- Franchise location intelligence
- Urban commercial analysis
- Startup market research
- Smart city retail analytics

---

# 🤝 Contributing

Contributions are welcome!

```bash
# Fork the repository

# Create a new feature branch
git checkout -b feature-name

# Commit changes
git commit -m "Added new feature"

# Push branch
git push origin feature-name
```

---

# 📄 License

This project is licensed under the MIT License.

---

# ⭐ Support

If you found this project useful, consider giving it a star on GitHub ⭐
