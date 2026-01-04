import requests
import sys
import os
# This Project get location and infromation about weather in India using OpenWeatherMap API
API_KEY = os.getenv("WEATHER_API_KEY", "bc91792b1b803710e6a5548c4047dd63")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    if not city:
        print("❌ Error: City name cannot be empty.")
        sys.exit(1)
    if not API_KEY:
        print("❌ Error: API key not found. Set WEATHER_API_KEY environment variable.")
        sys.exit(1)
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        city_name = data.get("name")
        weather_desc = data["weather"][0]["description"].title()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        print(f"🌤️ Weather in {city_name}:")
        print(f"  Conditions : {weather_desc}")
        print(f"  Humidity: {humidity}%")
        print(f"  Temperature: {temp}°C")
        print(f"  Wind Speed: {wind_speed} m/s")
    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError:
        print("❌ Network error. Please check your internet connection.")
    except requests.exceptions.Timeout: 
        print("❌ Request timed out. Please try again later.")
    except KeyError:
        print("❌ Error: Unexpected response format.")
    except Exception as err:
        print(f"❌ An error occurred: {err}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        city = input("Enter city name: ")
    else:
        city = " ".join(sys.argv[1:])
    get_weather(city)



