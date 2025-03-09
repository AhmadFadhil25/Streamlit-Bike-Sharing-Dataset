import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul aplikasi
st.title('Analisis Pola Penyewaan Sepeda')
st.write('Visualisasi pola penyewaan sepeda berdasarkan cuaca dan jam')
st.write('### Tujuan Penelitian:')
st.write("""
1. Bagaimana pengaruh cuaca (weathersit) dan musim (season) terhadap jumlah total penyewaan sepeda (cnt)? 
2. Bila melihat berdasarkan jam, apakah ada pola tertentu? Seperti jam berapa terpadat dan terlonggar?
""")

# Load data
day_df = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')

# Tampilkan data
st.subheader("Data Penyewaan Harian")
st.dataframe(day_df)

st.subheader("Data Penyewaan Per Jam")
st.dataframe(hour_df)

# Kelompokkan data berdasarkan weathersit
weather_groups = day_df.groupby('weathersit')['cnt'].mean().reset_index()

# Membuat label manual untuk cuaca
weather_labels = {
    1: 'Cerah',
    2: 'Berkabut/Berawan',
    3: 'Hujan Ringan',
    4: 'Hujan Lebat'
}
weather_groups['weather_label'] = weather_groups['weathersit'].map(weather_labels)

# Kelompokkan data berdasarkan jam
hourly_groups = hour_df.groupby('hr')['cnt'].mean().reset_index()

# **Visualisasi 1: Pengaruh Cuaca terhadap Penyewaan Sepeda**
st.subheader("Rata-rata Jumlah Pengguna Sepeda Berdasarkan Kondisi Cuaca")
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x='weather_label', y='cnt', data=weather_groups, ax=ax)
ax.set_title('Rata-rata Jumlah Pengguna Sepeda Berdasarkan Kondisi Cuaca')
ax.set_xlabel('Kondisi Cuaca')
ax.set_ylabel('Rata-rata Jumlah Pengguna Sepeda')
st.pyplot(fig)

# **Visualisasi 2: Pola Penggunaan Sepeda Berdasarkan Jam**
st.subheader("Pola Penggunaan Sepeda Berdasarkan Jam")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='hr', y='cnt', data=hourly_groups, marker='o', ax=ax)
ax.set_title('Pola Penggunaan Sepeda Berdasarkan Jam')
ax.set_xlabel('Jam')
ax.set_ylabel('Rata-rata Jumlah Pengguna Sepeda')
ax.set_xticks(range(0, 24))
ax.grid(True, linestyle='--', alpha=0.7)
st.pyplot(fig)
st.text('Bila kita melihat dari 2 Chart diatas kita dapat menyimpulkan sebagai berikut: ')
st.text ('1. Kondisi Cuaca merupakan faktor penting untuk pelaku usaha penyewaan sepeda. Bila kita melihat Bar Chart di atas bahwa Cuaca cerah memiliki hasil tertinggi dibandingkan yang lain ')
st.text ('2. Berdasarkan Line Chart di atas jam teramai dan terlonggar dalam penyewaan sepeda ialah jam 17 dan jam 4 pagi.')