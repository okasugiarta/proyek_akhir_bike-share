import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Menyiapkan data day_df
day_df = pd.read_csv("dashboard/day.csv")
day_df.head()

# Mengubah tipe data pada beberapa kolom
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
day_df['season'] = day_df.season.astype('category')
day_df['mnth'] = day_df.mnth.astype('category')
day_df['holiday'] = day_df.holiday.astype('category')
day_df['weekday'] = day_df.weekday.astype('category')
day_df['workingday'] = day_df.workingday.astype('category')
day_df['weathersit'] = day_df.weathersit.astype('category')

# Mengubah angka menjadi keterangan
day_df.season.replace((1,2,3,4), ('Winter','Spring','Summer','Fall'), inplace=True)
day_df.yr.replace((0,1), (2011,2012), inplace=True)
day_df.mnth.replace((1,2,3,4,5,6,7,8,9,10,11,12),('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'), inplace=True)
day_df.weathersit.replace((1,2,3,4), ('Clear','Misty','Light_RainSnow','Heavy_RainSnow'), inplace=True)
day_df.weekday.replace((0,1,2,3,4,5,6), ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'), inplace=True)
day_df.workingday.replace((0,1), ('No', 'Yes'), inplace=True)

# Menghapus kolom yang tidak diperlukan
day_df = day_df.drop("instant", axis=1)
day_df.head()

# Merubah nama kolom

day_df.rename(columns={
    "dteday" : "date",
    "yr" : "year",
    "mnth" : "month",
    "weathersit" : "weather",
    "hum" : "humidity",
    "cnt" : "total_count"}, inplace=True
)

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
monthly_rent_df = create_monthly_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)

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
