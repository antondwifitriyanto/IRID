import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import st_folium
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Data untuk Desa Lembur Sawah (default)
default_data = {
    "KETERPAPARAN (EXPOSURE)": 0.086957,
    "SENSITIVITAS (SENSITIVITY)": 0.106448,
    "KAPASITAS ADAPTIF (CAPACITY)": 0.283833,
    "BAHAYA (HAZARD)": 0.002609,
    "IRID": 0.479846,
    "STATUS": "Kerentanan Sedang"
}

# Judul Aplikasi
st.title("Climate Change Impact Simulator")
st.markdown("""
Simulasi dampak perubahan iklim terhadap risiko banjir dan kekeringan, dengan fokus pada Indeks Risiko Iklim Desa (IRID) berdasarkan data Desa Lembur Sawah.
""")

# Sidebar untuk Input Pengguna
st.sidebar.header("Input Data")
exposure = st.sidebar.number_input("Keterpaparan (Exposure):", min_value=0.0, max_value=1.0, value=default_data["KETERPAPARAN (EXPOSURE)"])
sensitivity = st.sidebar.number_input("Sensitivitas (Sensitivity):", min_value=0.0, max_value=1.0, value=default_data["SENSITIVITAS (SENSITIVITY)"])
adaptive_capacity = st.sidebar.number_input("Kapasitas Adaptif (Capacity):", min_value=0.0, max_value=1.0, value=default_data["KAPASITAS ADAPTIF (CAPACITY)"])
hazard = st.sidebar.number_input("Bahaya (Hazard):", min_value=0.0, max_value=1.0, value=default_data["BAHAYA (HAZARD)"])

# Prediksi IRID
st.subheader("Prediksi Indeks Risiko Iklim Desa (IRID)")
irid = (exposure + sensitivity - adaptive_capacity) * hazard
status = ""
if irid >= 0.6:
    status = "Kerentanan Tinggi"
elif 0.4 <= irid < 0.6:
    status = "Kerentanan Sedang"
else:
    status = "Kerentanan Rendah"

st.write(f"**IRID (Indeks Risiko Iklim Desa):** {irid:.3f}")
st.write(f"**Status Kerentanan:** {status}")

# Data Simulasi untuk Model Visualisasi
st.subheader("Visualisasi Interaktif")
st.markdown("Visualisasi distribusi IRID berdasarkan berbagai parameter.")

data = {
    "Exposure": np.random.uniform(0, 1, 100),
    "Sensitivity": np.random.uniform(0, 1, 100),
    "Adaptive Capacity": np.random.uniform(0, 1, 100),
    "Hazard": np.random.uniform(0, 1, 100),
}
data["IRID"] = (data["Exposure"] + data["Sensitivity"] - data["Adaptive Capacity"]) * data["Hazard"]
data["Status"] = pd.cut(
    data["IRID"], bins=[0, 0.4, 0.6, 1.0], labels=["Kerentanan Rendah", "Kerentanan Sedang", "Kerentanan Tinggi"]
)

simulated_data = pd.DataFrame(data)
fig = px.scatter_3d(
    simulated_data, x="Exposure", y="Sensitivity", z="Adaptive Capacity",
    color="Status", size="IRID", title="Simulasi 3D IRID"
)
st.plotly_chart(fig)

# Visualisasi Peta
st.subheader("Visualisasi Peta")
st.markdown("Berikut adalah peta lokasi Desa Lembur Sawah dengan status kerentanannya.")

# Lokasi Desa Lembur Sawah
latitude = -7.0501
longitude = 106.7224

# Membuat peta dengan Folium
map_lembur_sawah = folium.Map(location=[latitude, longitude], zoom_start=13)
folium.Marker(
    [latitude, longitude],
    popup=f"Desa Lembur Sawah\nIRID: {irid:.3f}\nStatus: {status}",
    tooltip="Desa Lembur Sawah"
).add_to(map_lembur_sawah)

# Menampilkan peta di Streamlit
st_folium(map_lembur_sawah, width=700, height=500)

# Studi Kasus Banjir Bandang
st.subheader("Studi Kasus: Banjir Bandang di Desa Lembur Sawah")
st.markdown("""
Pada saat ini, Desa Lembur Sawah terkena bencana banjir bandang yang menyebabkan ratusan rumah rusak. Simulasi berikut mencoba memodelkan dampak jika terjadi peningkatan curah hujan dan faktor lainnya berdasarkan acuan IPCC.
""")

# Parameter tambahan untuk studi kasus
rainfall = st.sidebar.slider("Curah Hujan (mm/hari):", min_value=0, max_value=500, value=300)
deforestation = st.sidebar.slider("Tingkat Deforestasi (%):", min_value=0, max_value=100, value=30)

# Simulasi dampak tambahan
adjusted_hazard = hazard + (rainfall / 500) * 0.3 + (deforestation / 100) * 0.2
adjusted_irid = (exposure + sensitivity - adaptive_capacity) * adjusted_hazard
adjusted_status = ""
if adjusted_irid >= 0.6:
    adjusted_status = "Kerentanan Tinggi"
elif 0.4 <= adjusted_irid < 0.6:
    adjusted_status = "Kerentanan Sedang"
else:
    adjusted_status = "Kerentanan Rendah"

st.write(f"**Curah Hujan:** {rainfall} mm/hari")
st.write(f"**Tingkat Deforestasi:** {deforestation}%")
st.write(f"**Adjusted IRID (Indeks Risiko Iklim Desa):** {adjusted_irid:.3f}")
st.write(f"**Adjusted Status Kerentanan:** {adjusted_status}")

# Machine Learning untuk Prediksi Banjir
st.subheader("Prediksi Kapan Banjir Akan Terjadi")
st.markdown("Menggunakan model machine learning untuk memprediksi risiko banjir berdasarkan data historis curah hujan.")

# Data simulasi untuk machine learning
ml_data = pd.DataFrame({
    "Rainfall": np.random.randint(100, 500, 1000),
    "Deforestation": np.random.randint(0, 100, 1000),
    "Flood": np.random.choice([0, 1], size=1000, p=[0.7, 0.3])  # 0: Tidak Banjir, 1: Banjir
})

X = ml_data[["Rainfall", "Deforestation"]]
y = ml_data["Flood"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model Random Forest
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Prediksi berdasarkan input pengguna
flood_prediction = model.predict([[rainfall, deforestation]])[0]
flood_risk = "Banjir" if flood_prediction == 1 else "Tidak Banjir"

st.write(f"**Prediksi Risiko Banjir:** {flood_risk}")
