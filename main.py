import requests
import numpy as np

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
    weekly_temps = np.array([(max_temps[i] + min_temps[i]) / 2 for i in range(len(dates))])
    return weekly_temps
    

if __name__ == "__main__":
    city = input("请输入城市名：")
    try:
        lat, lon = get_lat_lon(city)
        print(f"🌍 {city} 的经纬度: {lat}, {lon}")

        weekly_temps = get_weekly_avg_temperature(lat, lon)
        max_temp = np.max(weekly_temps)
        min_temp = np.min(weekly_temps)
        weekly_avg=np.mean(weekly_temps)
        avg_temps_f = weekly_temps * 9/5 + 32
        weekly_avg_f = weekly_avg * 9/5 + 32
        days_above_20=np.sum(weekly_temps>20)
        print(f"\n七天平均气温(°C):{np.round(weekly_temps,1)}")
        print(f"最高平均气温：{max_temp:.1f}°C")
        print(f"最低平均气温：{min_temp:.1f}°C")
        print(f"一周平均气温：{weekly_avg:.1f}°C")
        print(f"七天平均气温(°F):{np.round(avg_temps_f, 1)}")
        print(f"高于20°C的天数:{int(days_above_20)} 天")

    except Exception as e:
        print("❌ 出错：", e)