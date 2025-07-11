import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Set your API key here
API_KEY = 'b707e6168fe3847e7698ee3519453904'  # Replace with your OpenWeatherMap API key

# UI Input
st.title("Weather Data Visualizer")
city = st.text_input("Enter a city name", "Hyderabad")

if st.button("Get Weather Data"):
    # Make API request to get forecast data
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        st.success(f"Showing 5-day forecast (3-hour intervals) for **{city}**")

        # Extract required fields into a DataFrame
        forecast_list = data['list']
        weather_data = {
            "Time": [datetime.fromtimestamp(item['dt']) for item in forecast_list],
            "Temperature (°C)": [item['main']['temp'] for item in forecast_list],
            "Humidity (%)": [item['main']['humidity'] for item in forecast_list]
        }
        df = pd.DataFrame(weather_data)

        # Show table
        st.dataframe(df.head(10))

        # Plotting temperature trend
        st.subheader("Temperature Trend")
        plt.figure(figsize=(10, 4))
        plt.plot(df['Time'], df['Temperature (°C)'], marker='o', color='orange')
        plt.xticks(rotation=45)
        plt.xlabel("Time")
        plt.ylabel("Temperature (°C)")
        plt.title(f"Temperature Forecast for {city}")
        plt.tight_layout()
        st.pyplot(plt)

    else:
        st.error("Failed to fetch data. Please check the city name or try again later.")
