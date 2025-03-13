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

# Kelompokkan berdasarkan musim dan kondisi cuaca
season_weather_groups = day_df.groupby(['season', 'weathersit'])['cnt'].mean().reset_index()

# Definisikan label untuk musim
season_labels = {
    1: 'Musim Semi',
    2: 'Musim Panas',
    3: 'Musim Gugur',
    4: 'Musim Dingin'
}

# Menambahkan label untuk musim dan cuaca
season_weather_groups['season_label'] = season_weather_groups['season'].map(season_labels)

weather_labels = {
    1: 'Cerah',
    2: 'Berkabut/Berawan',
    3: 'Hujan Ringan',
    4: 'Hujan Lebat'
}
season_weather_groups['weather_label'] = season_weather_groups['weathersit'].map(weather_labels)

# Kelompokkan data berdasarkan jam
hourly_groups = hour_df.groupby('hr')['cnt'].mean().reset_index()

# **Visualisasi 1: Pengaruh Cuaca terhadap Penyewaan Sepeda**
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='season_label', y='cnt', hue='weather_label', data=season_weather_groups, ax=ax)
ax.set_title('Rata-rata Pengguna Sepeda Berdasarkan Musim dan Cuaca')
ax.set_xlabel('Musim')
ax.set_ylabel('Rata-rata Jumlah Pengguna Sepeda')
ax.legend(title="Kondisi Cuaca")
plt.xticks(rotation=15)
plt.tight_layout()
st.pyplot(fig)
st.text('Berdasarkan bar chart di atas, dapat disimpulkan bahwa cuaca dan musim merupakan faktor penting yang memengaruhi penggunaan jasa penyewaan sepeda. Cuaca cerah dan musim gugur menunjukkan tingkat penggunaan sepeda yang paling tinggi dibandingkan kondisi lainnya. Hal ini mengindikasikan bahwa pengguna lebih cenderung menyewa sepeda saat cuaca mendukung dan suhu lebih nyaman, seperti pada musim gugur yang umumnya memiliki udara sejuk dan kondisi yang stabil.')

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
st.text ('Berdasarkan Line Chart diatas terdapat dua lonjakan utama pada pukul 08:00 pagi dan 17:00–18:00 sore, yang kemungkinan besar berkaitan dengan jam berangkat kerja dan aktivitas setelah jam kantor.')

st.subheader("***Kesimpulan***")
st.text('Setelah analisis dilakukan saya melihat bahwa cuaca, musim, dan waktu dalam sehari memiliki pengaruh signifikan terhadap jumlah penyewaan sepeda. Cuaca cerah meningkatkan jumlah penyewaan, sementara kondisi hujan mengurangi minat pengguna. Selain itu, musim gugur menjadi periode dengan jumlah penyewaan tertinggi, kemungkinan karena suhu yang lebih nyaman dan kondisi cuaca yang stabil dibandingkan musim lainnya.Dari segi pola penggunaan berdasarkan waktu, terdapat dua lonjakan utama pada pukul 08:00 pagi dan 17:00–18:00 sore, yang kemungkinan besar berkaitan dengan jam berangkat kerja dan aktivitas setelah jam kantor, seperti pulang kerja atau rekreasi.')
