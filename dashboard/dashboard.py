import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Membuat Helper function

#ui sebelah kiri
def create_daily_df(df):
    daily_df = df.groupby(by="dteday").agg({"cnt": "sum"}).reset_index()
    return daily_df

#Ui tengah-tengah
def create_users_df(df):
    total_casual_users = df["casual"].sum()
    total_registered_users = df["registered"].sum()

    user_type_df = {
        "Type of Users": ["Casual Users", "Registered Users"],
        "Users Total": [total_casual_users, total_registered_users],
    }
    return user_type_df

#Ui kiri
def create_year_df(df):
    year_df = df.groupby(by="yr").agg({"cnt": "sum"}).reset_index()
    return year_df

def create_monthly_df(df):
    monthly_df = df.groupby(by="mnth").agg({"cnt": "sum"}).reset_index()
    return monthly_df

def create_weather_df(df):
    weather_df = df.groupby(by="weathersit").agg({"cnt": "sum"}).reset_index()
    return weather_df

# jadi, setelah menyiapkan beberapa helper function tersebut
# tahap berikutnya load berkas
all_df = pd.read_csv("dashboard/data_jam.csv")

# membuat komponen date
min_date = pd.to_datetime(all_df["dteday"]).dt.date.min()
max_date = pd.to_datetime(all_df["dteday"]).dt.date.max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image(
        "https://st2.depositphotos.com/4403291/6970/v/950/depositphotos_69708149-stock-illustration-trendy-flat-bike-logo.jpg"
    )

# Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label="Pilih Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
    )

# Nah, start_date dan end_date di atas akan digunakan untuk memfilter all_df. Data yang telah difilter ini selanjutnya akan disimpan dalam main_df. 
# Proses ini dijalankan menggunakan kode berikut.
main_df = all_df[
    (all_df["dteday"] >= str(start_date)) & (all_df["dteday"] <= str(end_date))
]

# DataFrame yang telah difilter (main_df) inilah yang digunakan untuk menghasilkan berbagai DataFrame yang dibutuhkan untuk membuat visualisasi data.
# Proses ini tentunya dilakukan dengan memanggil helper function yang telah kita buat sebelumnya.
daily_df = create_daily_df(main_df)
user_type_df = create_users_df(main_df)
year_df = create_year_df(main_df)
monthly_df = create_monthly_df(main_df)
weather_df = create_weather_df(main_df)

st.header("BIKE R3NT4L")
st.subheader("Daily Rentals")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Casual Users", value=int(main_df["casual"].sum()))
with col2:
    st.metric("Registered Users", value=int(main_df["registered"].sum()))
with col3:
    st.metric("Total Users", value=int(main_df["cnt"].sum()))

st.subheader("Rental Analysis")

# Berdasarkan cuaca
st.subheader("Based on weather")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="weathersit", y="cnt", data=weather_df, palette="viridis", ax=ax)
ax.set_title("Total Bike Rentals by Weather Condition")
ax.set_xlabel("Weather Condition")
ax.set_ylabel("Total Rentals")
st.pyplot(fig)

# Tren peningkatan dan penurunan dalam perbulan
st.subheader("Monthly increasing and decreasing trends")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="mnth", y="cnt", data=monthly_df, palette="viridis", ax=ax)
ax.set_title("Total Monthly increasing and decreasing trends")
ax.set_xlabel("Month")
ax.set_ylabel("Total Rentals")
st.pyplot(fig)

st.caption("Copyright 2024 ©️ Muhammad Dimas 2024")
