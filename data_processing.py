import json
import os
import datetime


# Converts degrees to cardinal directions
def degrees_to_cardinal(degrees):
    cardinal_directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

    # The data seems to have 180 degree offset on the wind direction so 180 degrees is added
    index = round(((degrees + 180) % 360) / (360.0 / len(cardinal_directions))) % len(
        cardinal_directions
    )
    return cardinal_directions[index]


# Format epoch time
def epoch_to_formatted(epoch):
    dt = datetime.datetime.fromtimestamp(int(epoch))
    date = dt.strftime("%d.%m.%Y")
    time = dt.strftime("%H:%M")
    return (date, time)


# Processes the data and write to the output file
def process_forecast_data(city):
    filepath = f"data/raw_data/forecast_weather_data_{city}.json"

    try:
        with open(filepath) as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {filepath} doesn't exist.")
        print(f"Could not process forecast weather data for {city.capitalize()}.")
        return
    except json.JSONDecodeError:
        print(f"Error: {filepath} is an invalid JSON file.")
        print(f"Could not process forecast weather data for {city.capitalize()}.")
        return
    except Exception as e:
        print(f"Error: {e}")
        print(f"Could not process forecast weather data for {city.capitalize()}.")
        return

    processed_data = {"city": city.capitalize(), "weather_data": []}
    for forecast in data["list"]:
        epoch_time = forecast["dt"]
        date, time = epoch_to_formatted(epoch_time)

        weather = forecast["weather"][0]["description"]
        temp_celsius = int(round(forecast["main"]["temp"] - 273.15, 0))
        humidity = forecast["main"]["humidity"]
        precipitation = forecast.get("rain", {}).get("3h", 0)
        wind_speed = round(forecast["wind"]["speed"], 1)

        wind_direction_degrees = forecast["wind"]["deg"]
        wind_direction_cardinal = degrees_to_cardinal(wind_direction_degrees)

        # Add the processed data to the output
        processed_data["weather_data"].append(
            {
                "date": date,
                "time": time,
                "weather": weather,
                "temperature": temp_celsius,
                "humidity": humidity,
                "precipitation": precipitation,
                "wind_speed": wind_speed,
                "wind_direction": wind_direction_cardinal,
            }
        )

    try:
        # Write the processed data to the output file
        processed_filepath = f"data/processed_data/weather_data_{city}.json"
        with open(processed_filepath, "w") as f:
            json.dump(processed_data, f, indent=4)
    except Exception as e:
        print(f"Error: {e}")
        print(
            f"Could not write processed weather data to file for {city.Capitalize()}."
        )
        return

    print(f"Forecast weather data of {city.capitalize()} processed succesfully.")


# Processes the data and adds it to the output data of process_forecast_data()
def process_current_data(city):
    filepath = f"data/raw_data/current_weather_data_{city}.json"

    try:
        with open(filepath) as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {filepath} doesn't exist.")
        print(f"Could not process current weather data for {city.capitalize()}.")
        return
    except json.JSONDecodeError:
        print(f"Error: {filepath} is an invalid JSON file.")
        print(f"Could not process current weather data for {city.capitalize()}.")
        return
    except Exception as e:
        print(f"Error: {e}")
        print(f"Could not process current weather data for {city.capitalize()}.")
        return

    epoch_time = data["dt"]
    date, time = epoch_to_formatted(epoch_time)

    weather = data["weather"][0]["description"]
    temp_celsius = int(round(data["main"]["temp"] - 273.15, 0))
    humidity = data["main"]["humidity"]
    precipitation = data.get("rain", {}).get("1h", 0)
    wind_speed = round(data["wind"]["speed"], 1)

    wind_direction_degrees = data["wind"]["deg"]
    wind_direction_cardinal = degrees_to_cardinal(wind_direction_degrees)

    # Add the processed data to the dictionary
    processed_data = {
        "city": city.capitalize(),
        "weather_data": [
            {
                "date": date,
                "time": time,
                "weather": weather,
                "temperature": temp_celsius,
                "humidity": humidity,
                "precipitation": precipitation,
                "wind_speed": wind_speed,
                "wind_direction": wind_direction_cardinal,
            }
        ],
    }

    # Read the existing data from the output file
    processed_filepath = f"data/processed_data/weather_data_{city}.json"
    try:
        with open(processed_filepath) as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {processed_filepath} doesn't exist.")
        print(
            f"Could not read existing data of current weather data for {city.capitalize()}."
        )
        return
    except json.JSONDecodeError:
        print(f"Error: {processed_filepath} is an invalid JSON file.")
        print(
            f"Could not read existing data of current weather data for {city.capitalize()}."
        )
        return
    except Exception as e:
        print(f"Error: {e}")
        print(
            f"Could not read existing data of current weather data for {city.capitalize()}."
        )
        return

    # Add the processed current data to the output file
    existing_data["weather_data"].insert(0, processed_data["weather_data"][0])

    try:
        with open(processed_filepath, "w") as f:
            json.dump(existing_data, f, indent=4)
    except Exception as e:
        print(f"Error: {e}")
        print(
            f"Could not write processed current weather data for {city.capitalize()}."
        )

    print(f"Current weather data of {city.capitalize()} processed succesfully.")


# Process the data by going through the raw_data folder
def process_data():
    for filename in os.listdir("data/raw_data/"):
        if filename.startswith("forecast_") and filename.endswith(".json"):
            city = filename[22:-5]
            process_forecast_data(city)
            process_current_data(city)
        elif not filename.startswith("current_"):
            print(f"Error: {filename} is an invalid file name.")
            print(f"Skipping file...")
    print("\n---Processing raw weather data finished---\n")


process_data()
