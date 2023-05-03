import json
import matplotlib.pyplot as plt

cities = [
    "Helsinki",
    "Espoo",
    "Tampere",
    "Vantaa",
    "Oulu",
    "Turku",
    "Jyväskylä",
    "Lahti",
    "Kuopio",
    "Kouvola",
    "Pori",
    "Joensuu",
    "Lappeenranta",
    "Hämeenlinna",
    "Vaasa",
]


def start_menu():
    print()
    choice = -1
    while choice != 0:
        print("What would you like to do?")
        print("1. See temperature graph")
        print("2. See precipitation and humidity graph")
        print("3. See wind speed and direction table")
        print("4. See weather of a spesific city at the moment")
        print("0. Exit")
        choice = input("Your choice: ")
        if choice.isdigit() and (0 <= int(choice) <= 4):
            return choice
        else:
            print("Invalid choice. Please try again.")
        print()
    return choice


def city_menu(i_option):
    print()
    if int(i_option) == 1:
        option = "temperature graph"
    elif int(i_option) == 2:
        option = "precipitation and humidity graph"
    elif int(i_option) == 3:
        option = "wind speed and direction graph"
    elif int(i_option) == 4:
        option = "weather"
    else:
        option = "'How did you manage to get this?'"
    choice = -1
    while choice != 0:
        print(f"Chooce a city you want to see the {option} about:")
        for city in cities:
            print(f"{cities.index(city) + 1}. {city}")
        print("0. Return back")
        choice = input("Your choice: ")
        if choice.isdigit() and (0 <= int(choice) <= 15):
            return choice, cities[int(choice) - 1]
        else:
            print("Invalid choice. Please try again.")
        print()
    return choice, cities[choice - 1]


# Create temperature chart from data and save it
def save_temperature_chart(city):
    filepath = f"data/processed_data/weather_data_{city.lower()}.json"

    try:
        with open(filepath) as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {filepath} doesn't exist.")
        print(f"Could not get weather data for {city}.")
        return
    except json.JSONDecodeError:
        print(f"Error: {filepath} is an invalid JSON file.")
        print(f"Could not get weather data for {city}.")
        return
    except Exception as e:
        print(f"Error: {e}")
        print(f"Could not get weather data for {city}.")
        return

    temperatures = []
    dates = []
    for forecast in data["weather_data"]:
        temperatures.append(forecast["temperature"])
        day, month, year = forecast["date"].split(".")
        time_date = f"{forecast['time']}\n{day}.{month}"
        dates.append(time_date)

    # Create graph and add data to it
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.plot(dates, temperatures, color="r")
    ax.tick_params(labelsize=6)
    ax.set_xlabel("Time and Date")
    ax.set_title(f"Temperature (°C) in {city}")

    # Make filename based on the date and time of the first data entry
    time, date = dates[0].split("\n")
    dd, mm = date.split(".")
    hh, mnt = time.split(":")
    plt.subplots_adjust(bottom=0.2)
    pathname = f"data/graphs/temperature_{city.lower()}_{dd}-{mm}_{hh}-{mnt}.png"
    plt.savefig(pathname)
    print("Graph saved on data/graphs/ folder succesfully.")


def save_precipitation_and_humidity_graph(city):
    filepath = f"data/processed_data/weather_data_{city.lower()}.json"

    try:
        with open(filepath) as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {filepath} doesn't exist.")
        print(f"Could not get weather data for {city}.")
        return
    except json.JSONDecodeError:
        print(f"Error: {filepath} is an invalid JSON file.")
        print(f"Could not get weather data for {city}.")
        return
    except Exception as e:
        print(f"Error: {e}")
        print(f"Could not get weather data for {city}.")
        return

    precipitations = []
    humidities = []
    dates = []
    for forecast in data["weather_data"]:
        precipitations.append(forecast["precipitation"])
        humidities.append(forecast["humidity"])
        day, month, year = forecast["date"].split(".")
        time_date = f"{forecast['time']}\n{day}.{month}"
        dates.append(time_date)

    # Create graph and add data to it
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.plot(dates, humidities, label="Humidity (%)")
    ax.bar(dates, precipitations, label="Precipitation (mm)", alpha=0.5)
    ax.tick_params(labelsize=6)
    ax.set_xlabel("Time and Date")
    ax.set_title(f"Humidity and Precipitation in {city}")
    ax.legend(loc="upper left")

    # Make filename based on the date and time of the first data entry
    time, date = dates[0].split("\n")
    dd, mm = date.split(".")
    hh, mnt = time.split(":")
    plt.subplots_adjust(bottom=0.2)
    pathname = (
        f"data/graphs/humidityAndPrecipitation_{city.lower()}_{dd}-{mm}_{hh}-{mnt}.png"
    )
    plt.savefig(pathname)
    print("Graph saved on data/graphs/ folder succesfully.")


def wind_speed_and_direction(city):
    filepath = f"data/processed_data/weather_data_{city.lower()}.json"

    try:
        with open(filepath) as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {filepath} doesn't exist.")
        print(f"Could not get weather data for {city}.")
        return
    except json.JSONDecodeError:
        print(f"Error: {filepath} is an invalid JSON file.")
        print(f"Could not get weather data for {city}.")
        return
    except Exception as e:
        print(f"Error: {e}")
        print(f"Could not get weather data for {city}.")
        return

    # Get and print wind speeds and directions
    print(f"Date and Time:\tWind speed & direction:")
    for forecast in data["weather_data"]:
        wind_speed = forecast["wind_speed"]
        wind_direction = forecast["wind_direction"]
        day, month, year = forecast["date"].split(".")
        time = forecast["time"]
        print(f"{day}.{month} {time}\t{wind_speed}\t{wind_direction}")


# Read the weather now for a spesific city from a file and print it out
def weather_now(city):
    filepath = f"data/processed_data/weather_data_{city.lower()}.json"

    try:
        with open(filepath) as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {filepath} doesn't exist.")
        print(f"Could not get weather data for {city}.")
        return
    except json.JSONDecodeError:
        print(f"Error: {filepath} is an invalid JSON file.")
        print(f"Could not get weather data for {city}.")
        return
    except Exception as e:
        print(f"Error: {e}")
        print(f"Could not get weather data for {city}.")
        return

    weather = data["weather_data"][0]["weather"]
    temperature = data["weather_data"][0]["temperature"]
    humidity = data["weather_data"][0]["humidity"]
    precipitation = data["weather_data"][0]["precipitation"]
    wind_speed = data["weather_data"][0]["wind_speed"]
    wind_direction = data["weather_data"][0]["wind_direction"]

    print()
    print(f"Weather now in {city}:\n{weather.capitalize()}")
    print(f"Temperature: {temperature} °C")
    print(f"Wind: {wind_speed} m/s towards {wind_direction}")
    print(f"Humidity: {humidity}%")
    print(f"Precipitation: {precipitation}mm")


def main():
    graph_type = -1
    while True:
        graph_type = start_menu()
        if int(graph_type) == 0:
            print("Shutting down...")
            exit()
        index, city = city_menu(graph_type)
        if int(index) == 0:
            continue
        if int(graph_type) == 1:  # Temperature graph
            save_temperature_chart(city)
        elif int(graph_type) == 2:  # Precipitation and humidity graph
            save_precipitation_and_humidity_graph(city)
        elif int(graph_type) == 3:  # Print wind speed and direction
            wind_speed_and_direction(city)
        elif int(graph_type) == 4:  # Weather now on spesific city
            weather_now(city)
        print()


main()
