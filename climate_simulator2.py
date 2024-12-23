import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from io import BytesIO

# Judul Aplikasi
st.title("Climate Change Impact Simulator")
st.markdown("""
Simulasi dampak perubahan iklim terhadap kejadian banjir dan kekeringan, 
termasuk prediksi risiko berbasis data dan analisis visual interaktif.
""")

# Sidebar untuk Input Pengguna
st.sidebar.header("Input Data")
scenario = st.sidebar.selectbox("Pilih Skenario Emisi:", ["RCP 2.6", "RCP 4.5", "RCP 6.0", "RCP 8.5"])
st.sidebar.markdown("---")

# Dummy Data untuk Model Prediksi Risiko
st.subheader("1. Model Prediksi Risiko")
st.markdown("""
Model ini menggunakan data curah hujan, kelembapan tanah, dan elevasi untuk memprediksi risiko banjir.
""")

# Data Simulasi
X_dummy = np.random.rand(500, 3) * [200, 1, 500]  # Curah Hujan (mm), Kelembapan Tanah, Elevasi
y_dummy = np.random.choice(["Low", "Medium", "High"], 500)

# Split Data dan Train Model
X_train, X_test, y_train, y_test = train_test_split(X_dummy, y_dummy, test_size=0.3, random_state=42)
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Evaluasi Model
y_pred = model.predict(X_test)
st.write("**Hasil Evaluasi Model:**")
st.text(classification_report(y_test, y_pred))

# Prediksi Risiko Baru
st.write("**Prediksi Risiko Baru:**")
curah_hujan = st.number_input("Curah Hujan (mm):", min_value=0, max_value=300, value=100)
kelembapan_tanah = st.number_input("Kelembapan Tanah (0-1):", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
elevasi = st.number_input("Elevasi (m):", min_value=0, max_value=1000, value=200)
prediksi = model.predict([[curah_hujan, kelembapan_tanah, elevasi]])
st.write(f"**Risiko yang Diprediksi:** {prediksi[0]}")

# Visualisasi Data Interaktif
st.subheader("2. Visualisasi Interaktif")
st.markdown("Berikut adalah visualisasi distribusi risiko banjir berdasarkan data simulasi.")

# Data Visualisasi
visual_data = pd.DataFrame(X_dummy, columns=["Curah Hujan", "Kelembapan Tanah", "Elevasi"])
visual_data["Risiko"] = y_dummy

# Visualisasi Plotly
fig = px.scatter_3d(
    visual_data, x="Curah Hujan", y="Kelembapan Tanah", z="Elevasi",
    color="Risiko", title="Distribusi Risiko Banjir",
    labels={"Curah Hujan": "Curah Hujan (mm)", "Kelembapan Tanah": "Kelembapan Tanah", "Elevasi": "Elevasi (m)"}
)
st.plotly_chart(fig)

# Ekspor Laporan
st.subheader("3. Ekspor Laporan")
st.markdown("""
Hasil simulasi dan prediksi risiko dapat diunduh dalam format Excel.
""")

# Membuat Dataframe untuk Laporan
report_data = pd.DataFrame({
    "Curah Hujan (mm)": X_dummy[:, 0],
    "Kelembapan Tanah": X_dummy[:, 1],
    "Elevasi (m)": X_dummy[:, 2],
    "Risiko": y_dummy
})

# Fungsi untuk Ekspor ke Excel
def export_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")
    df.to_excel(writer, index=False, sheet_name="Laporan Risiko")
    writer.save()
    processed_data = output.getvalue()
    return processed_data

# Tombol Unduh Laporan
excel_file = export_excel(report_data)
st.download_button(
    label="Unduh Laporan Simulasi",
    data=excel_file,
    file_name="laporan_risiko_banjir.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
