# app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for seaborn
sns.set(style="whitegrid")

# Set the title of the app
st.title("Proyek Analisis Data: Penggunaan Sepeda :bike:")

# Display author information
st.sidebar.header("Author Info")
st.sidebar.write("**Nama:**Fakhran al anshari")
st.sidebar.write("**Email:** fakhranalanshari3@gmail.com")




# Load Data
# Replace 'path_to_hour_csv' and 'path_to_day_csv' with the actual paths to the CSV files
hour_df = pd.read_csv('hour.csv')
day_df = pd.read_csv('day.csv')

st.subheader("Data Hourly")
st.write(hour_df.head())

st.subheader("Data Daily")
st.write(day_df.head())


# Rename and convert datetime columns
hour_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'cnt': 'count',
    'hum': 'humidity'
}, inplace=True)
day_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'cnt': 'count',
    'hum': 'humidity'
}, inplace=True)

# Convert 'dateday' to datetime
hour_df['dateday'] = pd.to_datetime(hour_df['dateday'])
day_df['dateday'] = pd.to_datetime(day_df['dateday'])



# Exploratory Data Analysis (EDA)
st.header("Data Visualization")

st.subheader("Pengaruh Waktu terhadap Penggunaan Sepeda")
avg_holiday = hour_df[hour_df['holiday'] == 1]['count'].mean()
avg_weekday = hour_df[hour_df['weekday'] == 1]['count'].mean()
avg_workingday = hour_df[hour_df['workingday'] == 1]['count'].mean()

categories = ['holiday', 'weekday', 'workingday']
avg_counts = [avg_holiday, avg_weekday, avg_workingday]

fig, ax = plt.subplots()
ax.bar(categories, avg_counts, color=['#A19882', '#C2B8A3', '#E6DDC6'])
ax.set_xlabel('Kategori Waktu')
ax.set_ylabel('Rata-rata Jumlah Pengguna Sepeda')
ax.set_title('Rata-rata Pengguna Sepeda pada Waktu Holiday, Weekday, Workingday')
st.pyplot(fig)

st.subheader("Perbandingan Pengguna Terdaftar (Registered) dan Pengguba Biasa (Casual)")
total_users = day_df.groupby(by='year').agg({'registered': 'sum', 'casual': 'sum'}).reset_index()
total_users = pd.melt(total_users, id_vars='year', value_vars=['registered', 'casual'],
                      var_name='User Type', value_name='Count')

fig, ax = plt.subplots()
sns.barplot(x='year', y='Count', hue='User Type', data=total_users, ax=ax, palette=['#617A55', '#A4D0A4'])
ax.set_title('Total Pengguna Registered dan Casual per Tahun')
ax.set_xlabel('Tahun')
ax.set_ylabel('Jumlah Penggunaan')
st.pyplot(fig)

st.subheader("Pengaruh Kondisi Cuaca terhadap Penggunaan Sepeda")
fig, ax = plt.subplots(1, 2, figsize=(15, 5))

sns.barplot(data=day_df, x='weathersit', y='count', ci=None, ax=ax[0], palette='viridis')
ax[0].set_title('Rata-rata Penggunaan Harian berdasarkan Kondisi Cuaca')
ax[0].set_xlabel('Kondisi Cuaca')
ax[0].set_ylabel('Rata-rata Jumlah Pengguna Harian')
ax[0].set_xticks([0, 1, 2, 3])
ax[0].set_xticklabels(['Clear', 'Cloudy', 'Rain', 'Snow'], rotation=45)

sns.barplot(data=hour_df, x='weathersit', y='count', ci=None, ax=ax[1], palette='viridis')
ax[1].set_title('Rata-rata Pengguna Per Jam berdasarkan Kondisi Cuaca')
ax[1].set_xlabel('Kondisi Cuaca')
ax[1].set_ylabel('Jumlah Pengguna Rata-rata Per Jam')
ax[1].set_xticks([0, 1, 2, 3])
ax[1].set_xticklabels(['Clear', 'Cloudy', 'Rain', 'Snow'], rotation=45)

st.pyplot(fig)

st.header("Conclusion")
st.write("""
- **Penggunaan sepeda tertinggi** terjadi saat hari kerja (workingday) dibandingkan hari libur atau hari biasa.
- **Pengguna terdaftar** jauh lebih banyak dibandingkan pengguna biasa, terutama pada tahun 2012.
- **Cuaca cerah** mendorong lebih banyak penggunaan sepeda, sedangkan hujan dan salju mengurangi jumlah pengguna.
""")
