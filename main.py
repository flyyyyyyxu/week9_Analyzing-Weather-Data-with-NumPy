import requests

def get_lat_lon(city_name):
    """通过城市名获取经纬度"""
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}"
    geo_response = requests.get(geo_url)
    geo_data = geo_response.json()

    if "results" not in geo_data or len(geo_data["results"]) == 0:
        raise ValueError("找不到该城市，请检查拼写")

    city_info = geo_data["results"][0]
    return city_info["latitude"], city_info["longitude"]

def get_weekly_avg_temperature(lat, lon):
    """通过经纬度获取未来7天平均气温"""
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

    # 计算平均温度
    avg_temps = [(max_temps[i] + min_temps[i]) / 2 for i in range(len(dates))]

    # 整理成数组
    weekly_data = []
    for i in range(len(dates)):
        weekly_data.append({
            "date": dates[i],
            "avg_temp": round(avg_temps[i], 1),
            "max_temp": max_temps[i],
            "min_temp": min_temps[i]
        })

    return weekly_data

if __name__ == "__main__":
    city = input("请输入城市名：")
    try:
        lat, lon = get_lat_lon(city)
        print(f"🌍 {city} 的经纬度: {lat}, {lon}")

        weekly_temps = get_weekly_avg_temperature(lat, lon)
        print(f"\n📅 {city} 接下来7天的平均气温：")
        for day in weekly_temps:
            print(day)
    except Exception as e:
        print("❌ 出错：", e)