import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Menyiapkan data day_df
day_df = pd.read_csv("dashboard/day.csv")
day_df.head()

# Menghapus kolom yang tidak diperlukan
day_df = day_df.drop("instant", axis=1)
day_df.head()

# Mengubah tipe data pada beberapa kolom
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
day_df['season'] = day_df.season.astype('category')
day_df['mnth'] = day_df.mnth.astype('category')
day_df['holiday'] = day_df.holiday.astype('category')
day_df['weekday'] = day_df.weekday.astype('category')
day_df['workingday'] = day_df.workingday.astype('category')
day_df['weathersit'] = day_df.weathersit.astype('category')

# Merubah nama kolom

day_df.rename(columns={
    "dteday" : "date",
    "yr" : "year",
    "mnth" : "month",
    "weathersit" : "weather",
    "hum" : "humidity",
    "cnt" : "total_count"}, inplace=True
)

# Mengubah angka menjadi keterangan
day_df['month'] = day_df['month'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})
day_df['season'] = day_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})
day_df['weekday'] = day_df['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
})
day_df['weather'] = day_df['weather'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})





# Merubah nilai dari 'temp', 'atemp', 'humidity, 'windspeed' ke dalam nilai yang belum dinormalisasi

day_df['temp'] = day_df['temp']*41
day_df['atemp'] = day_df['atemp']*50
day_df['humidity'] = day_df['humidity']*100
day_df['windspeed'] = day_df['windspeed']*67

# Menyiapkan monthly_rent_df
def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by='month').agg({
        'count': 'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)
    return monthly_rent_df

# Menyiapkan season_rent_df
def create_season_rent_df(df):
    season_rent_df = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return season_rent_df


    
# Menyiapkan berbagai dataframe
monthly_rent_df = create_monthly_rent_df(day_df)
season_rent_df = create_season_rent_df(day_df)

# Membuat Dashboard secara lengkap

# Membuat judul
st.header('Bike Share Rental Dashboard 🚲')

# Membuat jumlah penyewaan bulanan
st.subheader('Monthly Rentals')
plt.figure(figsize=(16,6))


sns.boxplot(
    x="month",
    y="total_count",
    data=day_df,
    palette=["blue", "lightblue"]
)

plt.xlabel("Month")
plt.ylabel("Total Rides")
plt.title("Total Bike share riding tiap bulan")

plt.show()

# Membuat jumlah penyewaan berdasarkan season
st.subheader('Seasonly Rentals')
plt.figure(figsize=(16,6))

sns.boxplot(
    x="season",
    y="total_count",
    data=day_df,
    palette=["blue", "lightblue"]
)

plt.xlabel("Season")
plt.ylabel("Total Rides")
plt.title("Total bike share riding per musim")

plt.show()


st.caption('Copyright (c) I Gusti Putu Oka Sugiarta 2024')
