import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(
    page_title="Bike Rental Dashboard", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# CSS untuk mempercantik tampilan
st.markdown("""
    <style>
        [data-testid="stSidebar"][aria-expanded="true"] {
            min-width: 320px;
            max-width: 320px;
        }
        .main .block-container {
            padding-left: 2rem;
            padding-right: 2rem;
            max-width: 95%;
        }
    </style>
""", unsafe_allow_html=True)

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    day_df = pd.read_csv("day.csv")
    hour_df = pd.read_csv("hour.csv")
    
    # Konversi kolom tanggal ke format datetime
    day_df["dteday"] = pd.to_datetime(day_df["dteday"])
    hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])
    
    return day_df, hour_df

# Load dataset
day_df, hour_df = load_data()

# Sidebar untuk kontrol pengguna
with st.sidebar:
    st.image("https://static.republika.co.id/uploads/member/images/news/fl9q1auagt.jpg", width=200)
    st.title("🚲 Bike Rental Dashboard")
    st.write("Analisis penyewaan sepeda berdasarkan data historis.")

    # Pilih dataset
    dataset_choice = st.radio("Pilih Dataset", ["Harian", "Per Jam"], index=1)

    # Pilihan rentang tanggal
    min_date = day_df["dteday"].min().date()
    max_date = day_df["dteday"].max().date()
    selected_dates = st.date_input(
        "Pilih Rentang Tanggal", 
        (min_date, max_date), 
        min_value=min_date, 
        max_value=max_date
    )

    # Pastikan rentang tanggal valid
    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_date, end_date = selected_dates
    else:
        start_date, end_date = min_date, max_date
    
    st.write(f"📅 **Rentang tanggal dipilih:** {start_date.strftime('%d %B %Y')} - {end_date.strftime('%d %B %Y')}")

# Pilih dataset berdasarkan pilihan pengguna
df = day_df if dataset_choice == "Harian" else hour_df

# Filter data berdasarkan rentang tanggal
with st.spinner("Memuat data..."):
    df["date_only"] = df["dteday"].dt.date
    filtered_data = df[(df["date_only"] >= start_date) & (df["date_only"] <= end_date)]

# Tampilkan data jika tersedia
if filtered_data.empty:
    st.warning(f"Tidak ada data untuk rentang {start_date.strftime('%d %B %Y')} - {end_date.strftime('%d %B %Y')}. Pilih rentang lain.")
else:
    st.subheader(f"Data Penyewaan dari {start_date.strftime('%d %B %Y')} hingga {end_date.strftime('%d %B %Y')}")
    
    display_columns = ['dteday', 'season', 'weathersit', 'temp', 'hum', 'windspeed', 'cnt']
    if dataset_choice == "Per Jam":
        display_columns.insert(1, 'hr')

    st.dataframe(filtered_data[display_columns], use_container_width=True)

    # Visualisasi penyewaan per jam jika memilih dataset per jam
    if dataset_choice == "Per Jam":
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(x="hr", y="cnt", data=filtered_data.sort_values('hr'), marker="o", ax=ax)
        ax.set_title(f"📈 Pola Penggunaan Sepeda dari {start_date.strftime('%d %B %Y')} hingga {end_date.strftime('%d %B %Y')}")
        ax.set_xlabel("Jam")
        ax.set_ylabel("Jumlah Penyewaan")
        ax.set_xticks(range(0, 24))
        ax.grid(True, linestyle="--", alpha=0.7)
        st.pyplot(fig)

# Analisis pengaruh cuaca terhadap penyewaan
st.subheader("🌦 Pengaruh Cuaca terhadap Penyewaan Sepeda")
season_weather_groups = day_df.groupby(['season', 'weathersit'])['cnt'].mean().reset_index()

season_labels = {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}
weather_labels = {1: 'Cerah', 2: 'Berkabut/Berawan', 3: 'Hujan Ringan', 4: 'Hujan Lebat'}

season_weather_groups['season_label'] = season_weather_groups['season'].map(season_labels)
season_weather_groups['weather_label'] = season_weather_groups['weathersit'].map(weather_labels)
season_weather_groups = season_weather_groups.dropna(subset=['weather_label'])

if not season_weather_groups.empty:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='season_label', y='cnt', hue='weather_label', data=season_weather_groups, ax=ax)
    ax.set_title('Rata-rata Pengguna Sepeda Berdasarkan Musim dan Cuaca')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Rata-rata Jumlah Pengguna Sepeda')
    ax.legend(title="Kondisi Cuaca")
    plt.xticks(rotation=15)
    plt.tight_layout()
    st.pyplot(fig)

# Kesimpulan
st.subheader("📌 Kesimpulan")
st.write("""
Setelah analisis dilakukan, terlihat bahwa cuaca, musim, dan waktu dalam sehari memiliki pengaruh signifikan terhadap jumlah penyewaan sepeda:
- **Cuaca cerah** meningkatkan jumlah penyewaan, sementara **hujan mengurangi** minat pengguna.
- **Musim gugur** menjadi periode dengan jumlah penyewaan tertinggi karena suhu yang nyaman dan kondisi cuaca yang stabil.
- Dari segi waktu, terdapat lonjakan utama pada pukul **08:00 pagi** dan **17:00–18:00 sore**, kemungkinan berkaitan dengan jam kerja dan aktivitas pulang kerja.
""")
