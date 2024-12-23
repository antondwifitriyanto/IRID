import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import matplotlib.pyplot as plt

# Judul dan Deskripsi
st.title("Climate Change Impact Simulator")
st.markdown("""
Simulasi dampak perubahan iklim terhadap kejadian banjir dan kekeringan. 
Aplikasi ini menggunakan skenario emisi dari IPCC AR5 (RCP 2.6, 4.5, 6.0, dan 8.5).
""")

# Sidebar untuk Input Pengguna
st.sidebar.header("Pilihan Skenario dan Wilayah")
scenario = st.sidebar.selectbox(
    "Pilih Skenario Emisi (RCP):",
    options=["RCP 2.6", "RCP 4.5", "RCP 6.0", "RCP 8.5"]
)

region = st.sidebar.text_input(
    "Masukkan Nama Wilayah atau Koordinat:",
    value="Sukabumi"
)

st.sidebar.markdown("---")
st.sidebar.write("**Catatan:** Data saat ini merupakan simulasi. Untuk analisis nyata, hubungkan dengan data CMIP5.")

# Data Dummy Simulasi (Curah Hujan dan Suhu)
years = list(range(2025, 2100, 5))
data = {
    "year": years,
    "temperature": np.random.normal(loc=1.5, scale=0.5, size=len(years)),
    "precipitation": np.random.normal(loc=100, scale=20, size=len(years))
}
df = pd.DataFrame(data)

# Menampilkan Data dan Tren
st.subheader(f"Simulasi Tren Iklim: {scenario}")
st.markdown(f"Wilayah: **{region}**")

# Grafik Tren Suhu
st.write("### Perubahan Suhu")
plt.figure(figsize=(10, 4))
plt.plot(df["year"], df["temperature"], marker="o", label="Temperature Anomaly (°C)")
plt.title("Proyeksi Perubahan Suhu")
plt.xlabel("Tahun")
plt.ylabel("Anomali Suhu (°C)")
plt.grid(True)
plt.legend()
st.pyplot(plt)

# Grafik Tren Curah Hujan
st.write("### Perubahan Curah Hujan")
plt.figure(figsize=(10, 4))
plt.bar(df["year"], df["precipitation"], color="skyblue", label="Precipitation (mm)")
plt.title("Proyeksi Perubahan Curah Hujan")
plt.xlabel("Tahun")
plt.ylabel("Curah Hujan (mm)")
plt.grid(True)
plt.legend()
st.pyplot(plt)

# Data Peta Risiko (Dummy)
st.subheader("Peta Risiko Perubahan Iklim")
map_data = pd.DataFrame({
    "lat": np.random.uniform(-6.9, -6.6, 100),
    "lon": np.random.uniform(106.5, 106.8, 100),
    "risk": np.random.choice(["Low", "Medium", "High"], 100)
})

# Visualisasi Peta
risk_color = {
    "Low": [0, 255, 0],
    "Medium": [255, 255, 0],
    "High": [255, 0, 0]
}
map_data["color"] = map_data["risk"].map(risk_color)

st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(
        latitude=-6.75,
        longitude=106.65,
        zoom=10,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=map_data,
            get_position=["lon", "lat"],
            get_color="color",
            get_radius=200,
        ),
    ],
))

# Ringkasan dan Kesimpulan
st.subheader("Ringkasan")
st.write(f"""
Pada skenario emisi **{scenario}**, wilayah **{region}** diproyeksikan mengalami perubahan suhu rata-rata sebesar {df['temperature'].mean():.2f}°C 
dan curah hujan rata-rata sebesar {df['precipitation'].mean():.2f} mm hingga tahun 2100.
""")

# Tambahan: Tautan untuk Data Resmi
st.markdown("""
---  
**Referensi Data:**  
- [IPCC AR5 Climate Projections](https://www.ipcc.ch/report/ar5/)  
- [CMIP5 Data Repository](https://esgf-node.llnl.gov/projects/cmip5/)
""")
