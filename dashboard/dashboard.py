import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import calendar
sns.set(style='dark')

def create_by_SO2_NO2(df, year):
    df_year = df[df['year'] == year]
    avg_so2_per_month = df_year.groupby('month')['SO2'].mean().reset_index()
    avg_no2_per_month = df_year.groupby('month')['NO2'].mean().reset_index()

    monthly_so2_no2_avg = avg_so2_per_month.merge(avg_no2_per_month, on='month')
    monthly_so2_no2_avg['month'] = monthly_so2_no2_avg['month'].apply(lambda x: calendar.month_name[x])
    month_order = list(calendar.month_name[1:])
    monthly_so2_no2_avg['month'] = pd.Categorical(monthly_so2_no2_avg['month'], categories=month_order, ordered=True)
    monthly_so2_no2_avg = monthly_so2_no2_avg.sort_values('month')
    
    return monthly_so2_no2_avg

def create_by_CO(df, year):
    df_year = df[df['year'] == year]
    avg_co_per_month = df_year.groupby('month')['CO'].mean().reset_index()
    avg_co_per_month['month'] = avg_co_per_month['month'].apply(lambda x: calendar.month_name[x])

    month_order = list(calendar.month_name[1:])
    avg_co_per_month['month'] = pd.Categorical(avg_co_per_month['month'], categories=month_order, ordered=True)
    avg_co_per_month = avg_co_per_month.sort_values('month')
    
    return avg_co_per_month

air_quality = pd.read_csv("guanyuan_air_quality.csv")


with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/5024/5024480.png")
    st.title("Guanyuan Air Quality:cloud::sparkles:")
    years = air_quality['year'].unique()
    years.sort()
    
    selected_year = st.selectbox('Select Year', years)

    monthly_so2_no2_co = create_by_SO2_NO2(air_quality, selected_year)

avg_pm = air_quality.groupby('year')[['PM2.5', 'PM10']].mean().reset_index()

st.title("Air Quality in Guanyuan")
col1, col2, col3 = st.columns(3)

with col1:
    count_row = air_quality.shape[0]
    st.metric("Total Rows", value=count_row)

with col2:
    avg_pm25 = air_quality['PM2.5'].mean()
    st.metric("Rata-rata PM2.5", value=f"{avg_pm25:.2f}")

with col3:
    avg_pm10 = air_quality['PM10'].mean()
    st.metric("Rata-rata PM10", value=f"{avg_pm10:.2f}")

st.title("Average PM2.5 and PM10 per Year")
st.line_chart(avg_pm.set_index('year'))

st.title("Average SO2, NO2, and CO per Year")
st.subheader("Polutant that makes the air quality bad")
st.subheader("SO2 and NO2")

col1, col2, col3, col4 = st.columns(4)
with col1:
    count_row = air_quality[air_quality['year'] == selected_year].shape[0]
    st.metric("Total Rows", value=count_row)

with col2:
    avg_so2 = air_quality[air_quality['year'] == selected_year]['SO2'].mean()
    st.metric("Rata-rata SO2", value=f"{avg_so2:.2f}")

with col3:
    avg_no2 = air_quality[air_quality['year'] == selected_year]['NO2'].mean()
    st.metric("Rata-rata NO2", value=f"{avg_no2:.2f}")

with col4:
    avg_co = air_quality[air_quality['year'] == selected_year]['CO'].mean()
    st.metric("Rata-rata CO", value=f"{avg_co:.2f}")

monthly_so2_no2_avg = create_by_SO2_NO2(air_quality, selected_year)
st.line_chart(monthly_so2_no2_avg.set_index('month'))

st.subheader("CO")
monthly_co_avg = create_by_CO(air_quality, selected_year)
st.line_chart(monthly_co_avg.set_index('month'))







