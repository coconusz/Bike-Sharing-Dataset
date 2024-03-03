import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe
def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='date').agg({
       "count": "sum"
    }).reset_index()
    return daily_rent_df
   
def create_daily_casual_rent_df(df):
    daily_casual_rent_df = df.groupby(by='date').agg({
       "casual": "sum"
    }).reset_index()
    return daily_casual_rent_df

def create_daily_registered_rent_df(df):
   daily_registered_rent_df = df.groupby(by='date').agg({
       "registered": "sum"
    }).reset_index()
   return daily_registered_rent_df

def create_season_rent_df(df):
    season_rent_df = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return season_rent_df

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

def create_yearly_rent_df(df):
    yearly_rent_df = df.groupby(by='year').agg({
        'count': 'sum'
    })
    ordered_year = ['2011', '2012']
    yearly_rent_df = yearly_rent_df.reindex(ordered_year, fill_value=0)
    return yearly_rent_df
    
def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_rent_df
    
def create_workingday_rent_df(df):
    workingday_rent_df = df.groupby(by='workingday').agg({
        'count': 'sum'
    }).reset_index()
    return workingday_rent_df

def create_holiday_rent_df(df):
    holiday_rent_df = df.groupby(by='holiday').agg({
        'count': 'sum'
    }).reset_index()
    return holiday_rent_df

def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by='weather').agg({
        'count': 'sum'
    })
    return weather_rent_df
        
# Load cleaned data
all_df = pd.read_csv("https://github.com/coconusz/Bike-Sharing-Dataset/blob/main/Dashboard/all_data.csv", sep='\t')

# Filter data
min_date = pd.to_datetime(all_df['date']).dt.date.min()
max_date = pd.to_datetime(all_df['date']).dt.date.max()

with st.sidebar:
    # Menambahkan logo
    image_url = "https://chattahoochee.whitewaterexpress.com/wp-content/uploads/sites/4/2020/03/yellow-bike-rentals-chattahoochee-whitewater-express-2-e1598905480969-1024x567.jpg"
    st.image(image_url, use_column_width=True)

    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Time Range',
        min_value= min_date,
        max_value= max_date,
        value= [min_date, max_date]
    )

main_df = all_df[(all_df["date"] >= str(start_date)) & 
                (all_df["date"] <= str(end_date))]

# Menyiapkan berbagai dataframe
daily_rent_df = create_daily_rent_df(main_df)
daily_casual_rent_df = create_daily_casual_rent_df(main_df)
daily_registered_rent_df = create_daily_registered_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)
monthly_rent_df = create_monthly_rent_df(main_df)
yearly_rent_df = create_yearly_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
workingday_rent_df = create_workingday_rent_df(main_df)
holiday_rent_df = create_holiday_rent_df(main_df)
weather_rent_df = create_weather_rent_df(main_df)

# Membuat judul dashboard
st.header('🚴‍♂️ Bike Rental 🚴‍♂️')

# Membuat jumlah penyewa sepeda per hari
st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent_casual = daily_casual_rent_df['casual'].sum()
    st.metric('Casual Customer', value=daily_rent_casual)
    
with col2:
    daily_rent_registered = daily_registered_rent_df['registered'].sum()
    st.metric('Registered Customer', value=daily_rent_registered)
    
with col3:
    daily_rent_total = daily_rent_df['count'].sum()
    st.metric('Total Customer', value=daily_rent_total)

# Membuat jumlah penyewa sepeda per bulan
st.subheader('Monthly Rentals')
fig, ax = plt.subplots(figsize=(24, 8))
ax.plot(
    monthly_rent_df.index,
    monthly_rent_df['count'],
    marker='o', 
    linewidth=2,
    color='tab:green'
)

for index, row in enumerate(monthly_rent_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.tick_params(axis='x', labelsize=25, rotation=45)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)

# Membuat jumlah penyewa sepeda per tahun
all_df['month'] = pd.Categorical(all_df['month'], categories=
    ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
    ordered=True)

monthly_counts = all_df.groupby(by=["month", "year"]).agg({
    "count": "sum"
}).reset_index()

st.subheader("Numbers of Renters by Month and Year")
fig, ax = plt.subplots(figsize=(10, 6))

sns.lineplot(
    data=monthly_counts,
    x="month",
    y="count",
    hue="year",
    palette="viridis",
    marker="o",
    ax=ax
)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.legend(title="Year", loc="upper left")

st.pyplot(fig)


# Visualisasi 1: Jumlah Penyewaan Sepeda Berdasarkan Kondisi Cuaca
st.subheader('Number of Renters by Weather')
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(y=all_df["count"], x=all_df["weather"], orient="v", palette="viridis", ax=ax)
ax.set_ylabel("Number of Renters")
st.pyplot(fig)

# Visualisasi 2: Jumlah Penyewaan Sepeda Berdasarkan Musim
st.subheader('Number of Renters by Season')
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(y=all_df["count"], x=all_df["season"], orient="v", palette="viridis", ax=ax)
ax.set_ylabel("Number of Renters")
st.pyplot(fig)

# Visualisasi 3: Jumlah Penyewaan Sepeda per Jam
st.subheader('Number of Renters by Hour')
fig, ax = plt.subplots(figsize=(12, 6))
hourly_counts = all_df.groupby('hour')['count'].mean().reset_index()
sns.lineplot(x='hour', y='count', data=hourly_counts, marker='o', color='green', ax=ax)
ax.set_xlabel("Time")
ax.set_ylabel("Number of Renters")
ax.set_xticks(hourly_counts['hour'])  
ax.tick_params(axis='x', rotation=45)  
ax.grid(True)

fig.tight_layout()
st.pyplot(fig)

# Visualisasi 4: Hubungan Suhu, Kelembaban, dan Kecepatan Angin dengan Jumlah Penyewaan
st.subheader('The Relation between Temp, Hum, Windspeed and Renters')
fig, axes = plt.subplots(3, 1, figsize=(12, 8))

# Scatter plot temp vs count
sns.scatterplot(x='temp', y='count', data=all_df, ax=axes[0])
ax.set_title('The Relation between Temperature and Renters')

# Scatter plot hum vs count
sns.scatterplot(x='hum', y='count', data=all_df, ax=axes[1])
ax.set_title('The Relation between Humidity and Renters')

# Scatter plot windspeed vs count
sns.scatterplot(x='windspeed', y='count', data=all_df, ax=axes[2])
ax.set_title('The Relation between Windspeed and Renters')

fig.tight_layout()
st.pyplot(fig)

# Visualisasi 5: Perbandingan Jumlah Penyewaan Sepeda pada Hari Libur dan Bukan Hari Libur
st.subheader('Comparison of Rents on Holiday and Weekday')
all_df['holiday'] = all_df['holiday'].map({0: 'Not Holiday', 1: 'Holiday'})

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='holiday', y='count', data=all_df, ci=None, palette='viridis', ax=ax)

ax.set_xlabel('Tipe Hari')
ax.set_ylabel('Number of Renters')
st.pyplot(fig)

st.caption('Copyright (c) Sabrina Marta Disa 2024')