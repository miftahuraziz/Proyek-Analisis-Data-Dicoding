import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_theme(style='dark')

def daily_rent(day_df):
    daily_rent_df = day_df.resample(rule='D', on='date_time').agg({
        "total_rent": "sum"
    })
    return daily_rent_df

def hourly_rent(hour_df):
    hourly_rent_df = hour_df.groupby("hour").total_rent.sum().sort_values(ascending=False).reset_index()
    return hourly_rent_df

def seasonly_rent(hour_df):
    seasonly_rent_df = hour_df.groupby(by="season").total_rent.sum().reset_index() 
    return seasonly_rent_df

def registered(day_df):
   registered_df =  day_df.groupby(by="date_time").agg({
      "registered": "sum"
    })
   registered_df = registered_df.reset_index()
   return registered_df

def casual(day_df):
   casual_df =  day_df.groupby(by="date_time").agg({
      "casual": "sum"
    })
   casual_df = casual_df.reset_index()
   return casual_df

#Gunakan ini untuk dashboard online
hours_df = pd.read_csv("https://raw.githubusercontent.com/miftahuraziz/Proyek-Analisis-Data-Dicoding/main/dashboard/hour_df_clean.csv")
days_df = pd.read_csv("https://raw.githubusercontent.com/miftahuraziz/Proyek-Analisis-Data-Dicoding/main/dashboard/day_df_clean.csv")

#Gunakan ini untuk dashboard local dan disable kode di atas
#hours_df = pd.read_csv("hour_df_clean.csv")
#days_df = pd.read_csv("day_df_clean.csv")


datetime_columns = ["date_time"]
days_df.sort_values(by="date_time", inplace=True)
days_df.reset_index(inplace=True)

hours_df.sort_values(by="date_time", inplace=True)
hours_df.reset_index(inplace=True)

for column in datetime_columns:
    days_df[column] = pd.to_datetime(days_df[column])
    hours_df[column] = pd.to_datetime(hours_df[column])

min_date_days = days_df["date_time"].min()
max_date_days = days_df["date_time"].max()

min_date_hour = hours_df["date_time"].min()
max_date_hour = hours_df["date_time"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://storage.googleapis.com/kaggle-datasets-images/3556223/6194875/c51f57d9f027c00fc8d573060eef197b/dataset-cover.jpeg?t=2023-07-25-20-43-36")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days]
    )

main_day_df = days_df[(days_df["date_time"] >= str(start_date)) &
                       (days_df["date_time"] <= str(end_date))]

main_hour_df = hours_df[(hours_df["date_time"] >= str(start_date)) & 
                        (hours_df["date_time"] <= str(end_date))]

daily_rent_df = daily_rent(main_day_df)
hourly_rent_df = hourly_rent(main_hour_df)
seasonly_df = seasonly_rent(main_hour_df)
registered_df = registered(main_day_df)
casual_df = casual(main_day_df)

st.header('Bike Sharing Dashboard:sparkles:')

st.subheader('Daily Rent')
col1, col2, col3 = st.columns(3)

with col1:
    total_rent = daily_rent_df.total_rent.sum()
    st.metric("Total Bike Rent", value=total_rent)

with col2:
    total_registered = registered_df.registered.sum()
    st.metric("Registered User", value=total_registered)

with col3:
    total_casual = casual_df.casual.sum()
    st.metric("Casual User", value=total_casual)

st.subheader('Performa Penyewaan Beberapa Tahun Terakhir')
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    days_df["date_time"],
    days_df["total_rent"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)
st.pyplot(fig)

st.subheader("Penyewaan Berdasarkan Jam")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

sns.barplot(x="hour", y="total_rent", data=hourly_rent_df.head(5), palette=["#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3"], ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Hours", fontsize=30)
ax[0].set_title("Most Rentals by Hour", loc="center", fontsize=30)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="hour", y="total_rent", data=hourly_rent_df.sort_values(by="hour", ascending=True).head(5), palette=["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3","#90CAF9"], ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Hours",  fontsize=30)
ax[1].set_title("Lowest Rentals by Hour", loc="center", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)

st.subheader("Penyewaan Berdasarkan Season")
colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#90CAF9"]
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
        y="total_rent", 
        x="season",
        data=seasonly_df.sort_values(by="season", ascending=False),
        palette=colors,
        ax=ax
    )
ax.set_title("Most Rentals by Season", loc="center", fontsize=35)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=30)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

st.subheader("Perbandingan Penyewaan Berdasarkan Jenis Customer")
labels = 'Casual User', 'Registered User'
data = total_casual, total_registered
explode = (0, 0.1) 

fig1, ax1 = plt.subplots()
ax1.pie(data, explode=explode, labels=labels, autopct='%1.1f%%',colors=["#D3D3D3", "#90CAF9"],
        shadow=True, startangle=90)
ax1.axis('equal')
st.pyplot(fig1)
