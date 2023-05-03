import requests
import json

# API key
api_key = ""  # I've deleted the api key since it should be private

# Dictionary of city names and coordinates
cities = {
    "Helsinki": (60.1699, 24.9384),
    "Espoo": (60.2055, 24.6559),
    "Tampere": (61.4981, 23.7608),
    "Vantaa": (60.2929, 25.0504),
    "Oulu": (65.0121, 25.4651),
    "Turku": (60.4518, 22.2666),
    "Jyväskylä": (62.2416, 25.7209),
    "Lahti": (60.9827, 25.6615),
    "Kuopio": (62.8926, 27.6783),
    "Kouvola": (60.8681, 26.7046),
    "Pori": (61.4818, 21.7979),
    "Joensuu": (62.6018, 29.7636),
    "Lappeenranta": (61.0586, 28.1865),
    "Hämeenlinna": (60.9959, 24.4646),
    "Vaasa": (63.0954, 21.6158),
}


# Loop through the cities and download the weather data
def get_data():
    for city, coords in cities.items():
        lat, lon = coords

        # URLs
        current_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}"

        # Make API request to get what weather it is now
        try:
            c_response = requests.get(current_url)
            c_response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error: {e}")
            print(f"Failed to download current weather data for {city}.")
            continue
        except requests.exceptions.RequestException as e:
            print(f"Request exception: {e}")
            print(f"Failed to download current weather data for {city}.")
            continue
        except Exception as e:
            print(f"Error: {e}")
            print(f"Failed to download current weather data for {city}.")
            continue

        data = json.loads(c_response.content)

        # Save the JSON data to a file
        save_path = f"data/raw_data/current_weather_data_{city.lower()}.json"
        try:
            with open(save_path, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error: {e}")
            print(f"Could not write raw current weather data file for {city}.")

        # Make API request to get weather forecast data
        try:
            f_response = requests.get(forecast_url)
            f_response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error: {e}")
            print(f"Failed to download forecast weather data for {city}.")
            continue
        except requests.exceptions.RequestException as e:
            print(f"Request exception: {e}")
            print(f"Failed to download forecast weather data for {city}.")
            continue
        except Exception as e:
            print(f"Error: {e}")
            print(f"Failed to download forecast weather data for {city}.")
            continue

        data = json.loads(f_response.content)

        # Save the JSON data to a file
        save_path = f"data/raw_data/forecast_weather_data_{city.lower()}.json"
        try:
            with open(save_path, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error: {e}")
            print(f"Could not write raw forecast weather data file for {city}.")

        print(f"Weather data for {city} downloaded succesfully.")
    print("\n---Downloading weather data from OpenWeatherMap finished---\n")


get_data()
