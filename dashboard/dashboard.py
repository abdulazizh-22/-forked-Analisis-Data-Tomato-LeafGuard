import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import subprocess
import sys

st.set_page_config(
    page_title="Tomato-LeafGuard Farm Disease Dashboard",
    page_icon="🍅",
    layout="wide"
)

# Input Data
file_id = '1SYB6jD3NXckgpkvtF4tk5AxLZWDfIoLN'
url = f'https://drive.google.com/uc?export=download&id={file_id}'

df = pd.read_csv(url)

# Sidebar
st.sidebar.header("🍅 Filter Kebun Tomat")

# Filter Berdasarkan Residue
all_residues = ['Semua Kategori'] + list(df['residue'].unique())
selected_residue = st.sidebar.selectbox("Pilih Tingkat Residu Lahan:", all_residues)

# Filter Berdasarkan Penyakit
all_diseases = list(df['disease'].unique())
selected_diseases = st.sidebar.multiselect("Pilih Jenis Penyakit/Kondisi:", all_diseases, default=all_diseases)


# Terapkan Filter ke Data
df_filtered = df[df['disease'].isin(selected_diseases)]

if selected_residue != 'Semua Kategori':
    df_filtered = df_filtered[df_filtered['residue'] == selected_residue]

# header
st.title("🍅 Dashboard Analisis Penyakit Kebun Tomat")
st.markdown("""
Dashboard ini mendeteksi hubungan antara **kondisi lingkungan (Suhu, Kelembapan, Kadar Nitrogen, Residu)** dengan **kesehatan tanaman tomat**.
""")
st.write("---")

# Ringkasan
col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
with col_kpi1:
    st.metric("Total Sampel Data", len(df_filtered))
with col_kpi2:
    total_sehat = len(df_filtered[df_filtered['disease'] == 'healthy'])
    st.metric("Tanaman Sehat", f"{total_sehat} pohon")


st.write("---")

# Visualisasi utama
col1, col2 = st.columns(2)

with col1:
    st.subheader("Hubungan Penyakit dengan Suhu & Kelembapan")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(
        data=df_filtered, 
        x='temperature', 
        y='humidity', 
        hue='disease', 
        palette='tab10', 
        alpha=0.8,
        ax=ax
    )
    ax.set_xlabel("Suhu (°C)")
    ax.set_ylabel("Kelembapan (%)")
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0.)
    st.pyplot(fig)

with col2:
    st.subheader("Distribusi Kadar Nitrogen dalam Tanah pada Tiap Penyakit")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(
        data=df_filtered, 
        y='disease', 
        x='nutrient', 
        palette='vlag',
        ax=ax
    )
    ax.set_xlabel("Kadar Nutrisi kg/ha")
    ax.set_ylabel("Jenis Penyakit / Kondisi")
    plt.tight_layout()
    st.pyplot(fig)

st.write("---")

# visualisasi lainnya
st.subheader("Visualisasi Lainnya")
col3, col4 = st.columns([1, 2])

with col3:
    st.write("**Proporsi Kondisi Kesehatan Tanaman**")   

    disease_counts = df_filtered['disease'].value_counts()
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Highlight potongan 'healthy' jika ada di data terfilter
    explode = [0.1 if idx == 'healthy' else 0 for idx in disease_counts.index]
    
    ax.pie(
        disease_counts, 
        labels=disease_counts.index, 
        autopct='%1.1f%%', 
        startangle=140, 
        explode=explode,
        colors=sns.color_palette('pastel')
    )
    st.pyplot(fig)

with col4:
    st.write("**Matriks Korelasi Antar Faktor Lingkungan**")

    # Hanya menghitung korelasi variabel numerik
    corr_matrix = df_filtered[['temperature', 'humidity', 'nutrient']].corr()
    
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(
        corr_matrix, 
        annot=True, 
        cmap='coolwarm', 
        vmin=-1, 
        vmax=1, 
        center=0,
        ax=ax
    )
    st.pyplot(fig)

# Preview data
st.write("---")
st.subheader("Preview Data Terfilter (Top 5 Baris)")
st.dataframe(df_filtered.head())
