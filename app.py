import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

st.title("🧪 GIS Sampling Ikan Sapu-sapu - DAS Ciliwung")
st.markdown("Visualisasi titik sampling berbasis data lapangan & berita")

# Load default dataset
@st.cache_data
def load_data():
    return pd.read_csv("data_ciliwung_sampling.csv")

df = load_data()

# Sidebar upload
st.sidebar.header("📂 Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("Dataset berhasil diupload!")

# Map center (Jakarta)
m = folium.Map(location=[-6.23, 106.85], zoom_start=11)

# Color mapping
def get_color(kategori):
    if kategori == "core":
        return "red"
    elif kategori == "sekunder":
        return "orange"
    else:
        return "blue"

# Add markers
for _, row in df.iterrows():
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=f"""
        <b>{row['nama_lokasi']}</b><br>
        Kategori: {row['kategori']}<br>
        Info: {row['keterangan']}
        """,
        icon=folium.Icon(color=get_color(row["kategori"]))
    ).add_to(m)

# Display map
st.subheader("🗺️ Peta Sampling")
st_data = st_folium(m, width=1200, height=600)

# Show table
st.subheader("📊 Data Sampling")
st.dataframe(df)

# Add new point manually
st.subheader("➕ Tambah Titik Sampling")

with st.form("form_tambah"):
    nama = st.text_input("Nama Lokasi")
    lat = st.number_input("Latitude", format="%.6f")
    lon = st.number_input("Longitude", format="%.6f")
    kategori = st.selectbox("Kategori", ["core", "sekunder", "hilir"])
    ket = st.text_input("Keterangan")

    submit = st.form_submit_button("Tambah")

    if submit:
        new_row = pd.DataFrame([{
            "nama_lokasi": nama,
            "lat": lat,
            "lon": lon,
            "kategori": kategori,
            "keterangan": ket
        }])
        df = pd.concat([df, new_row], ignore_index=True)
        st.success("Titik berhasil ditambahkan (sementara, belum disimpan ke file)")
