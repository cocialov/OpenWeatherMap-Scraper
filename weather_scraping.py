import os
import requests
import time
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env file

API_KEY = os.getenv("API_KEY")  # get API key from environment variables

# Coordinates of the locations
locations = [
    {
        "name": "Petromidia",
        "lat": "44.34452",
        "lon": "28.64399"
    },
    {
        "name": "Vega",
        "lat": "44.96478170793081",
        "lon": "26.02463782325529"
    },
    {
        "name": "Headquarters",
        "lat": "44.47774672270021",
        "lon": "26.071376726062486"
    }
]

FORECAST_URL = "http://api.openweathermap.org/data/2.5/weather?"
units = "metric"

def get_weather_data(location):
    """Fetches and saves weather data for a specific location."""
    try:
        # Build the URL for the API request
        url = FORECAST_URL + "lat=" + location["lat"] + "&lon=" + location["lon"] + "&units=" + units + "&appid=" + API_KEY
        response = requests.get(url).json()
        if response['cod'] != 200:  # HTTP status code for success is 200
            print(f"Failed to get data for {location['name']}, status code: {response['cod']}")
            return

        # Extract the data
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        temp = response['main']['temp']
        status = response['weather'][0]['main']
        rain = response.get('rain', {}).get('1h', 0)
        humidity = response['main']['humidity']
        visibility = response.get('visibility', 0)
        wind_speed = response['wind']['speed']

        # Create a DataFrame with the data
        df = pd.DataFrame({
            'Date': [date],
            'Temperature': [temp],
            'Status': [status],
            'Chance of Rain': [rain],
            'Humidity': [humidity],
            'Visibility': [visibility],
            'Wind Speed': [wind_speed],
            'Location': [location["name"]]
        })

        # Append the data to the CSV file for this location
        file_name = location["name"] + ".csv"
        if os.path.exists(file_name):
            header = False  
        else:
            header = True  

        df.to_csv(file_name, mode='a', header=header, index=False)
        print("Weather data for", location["name"], "has been added to the CSV.")
    except Exception as e:
        print(f"An error occurred while fetching data for {location['name']}: {e}")

# Loop to get weather data for all locations
for location in locations:
    get_weather_data(location)
time.sleep(3600)