import requests
import numpy as np

def get_lat_lon(city_name):
    """Obtain latitude and longitude from city name"""
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}"
    geo_response = requests.get(geo_url)
    geo_data = geo_response.json()

    if "results" not in geo_data or len(geo_data["results"]) == 0:
        raise ValueError("The city cannot be found. Please check the spelling.")

    city_info = geo_data["results"][0]
    return city_info["latitude"], city_info["longitude"]

def get_weekly_avg_temperature(lat, lon):
    """Obtain the average temperature for the next 7 days using latitude and longitude."""
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&daily=temperature_2m_max,temperature_2m_min"
        f"&timezone=auto"
    )
    response = requests.get(weather_url)
    data = response.json()

    dates = data["daily"]["time"]
    max_temps = data["daily"]["temperature_2m_max"]
    min_temps = data["daily"]["temperature_2m_min"]

    # Calculate the average temperature
    weekly_temps = np.array([(max_temps[i] + min_temps[i]) / 2 for i in range(len(dates))])
    return weekly_temps
    

if __name__ == "__main__":
    city = input("Please enter the city name:")
    try:
        lat, lon = get_lat_lon(city)
        print(f"🌍 {city} latitude and longitude: {lat}, {lon}")

        weekly_temps = get_weekly_avg_temperature(lat, lon)
        max_temp = np.max(weekly_temps)
        min_temp = np.min(weekly_temps)
        weekly_avg=np.mean(weekly_temps)
        avg_temps_f = weekly_temps * 9/5 + 32
        weekly_avg_f = weekly_avg * 9/5 + 32
        days_above_20=np.sum(weekly_temps>20)
        print(f"\nAverage temperature over the next seven days(°C):{np.round(weekly_temps,1)}")
        print(f"Maximum average temperature:{max_temp:.1f}°C")
        print(f"Minimum average temperature:{min_temp:.1f}°C")
        print(f"Average temperature over a week:{weekly_avg:.1f}°C")
        print(f"Average temperature over the next seven days(°F):{np.round(avg_temps_f, 1)}")
        print(f"Number of days above 20°C:{int(days_above_20)} days")

    except Exception as e:
        print("❌ Error:", e)