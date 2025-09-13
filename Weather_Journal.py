import requests

from collections import defaultdict
from datetime import datetime

class Weather_Forecast(object):
    weather_API = "58e3b566e5bed0958072fca73566c81f"
    
    def get_three_hours_weather_forecast(self, CITY):
        weather_url = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={self.weather_API}&units=metric&lang=en"
        #
        response = requests.get(weather_url)
        data = response.json()

        weather_forecast_date = []
        weather_forecast_temperature = []
        weather_forecast_description = []
        for item in data["list"][:10]:  # max 10 records
            date = datetime.fromtimestamp(item["dt"])
            temp = item["main"]["temp"]
            desc = item["weather"][0]["description"]
            weather_forecast_date.append(f"{date.strftime("%H:%M:%S")}")
            weather_forecast_temperature.append(f"{temp} C")
            weather_forecast_description.append(f"{desc}")
        return weather_forecast_date, weather_forecast_temperature, weather_forecast_description


    def get_five_day_weather_forecast(self, CITY):
        weather_url = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={self.weather_API}&units=metric&lang=en"
        #One Call API
        response = requests.get(weather_url)
        data = response.json()

        #
        forecast_by_day = defaultdict(list)

        for item in data["list"]:
            date = datetime.fromtimestamp(item["dt"]).date()
            temp = item["main"]["temp"]
            desc = item["weather"][0]["description"]
            forecast_by_day[date].append((temp, desc))
        
        five_day_weather_forecast_date = []
        five_day_weather_forecast_temperature = []
        five_day_weather_forecast_description = []
        for date, values in list(forecast_by_day.items())[:5]:  # max 5 days
            min_temp = min(v[0] for v in values)
            max_temp = max(v[0] for v in values)
            descs = [v[1] for v in values]
            five_day_weather_forecast_date.append(f"{date}")
            five_day_weather_forecast_temperature.append(f" {min_temp:.1f} C {max_temp:.1f} C")
            five_day_weather_forecast_description.append(f"{descs[0]}")
        return five_day_weather_forecast_date, five_day_weather_forecast_temperature, five_day_weather_forecast_description
