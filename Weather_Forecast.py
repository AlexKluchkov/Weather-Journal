import requests

from collections import defaultdict
from datetime import datetime

class Weather_Forecast(object):
    weather_API = "58e3b566e5bed0958072fca73566c81f"
   
    def get_weather_forecast(self, CITY):
        weather_url = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={self.weather_API}&units=metric&lang=en"
        #One Call API
        response = requests.get(weather_url)
        data = response.json()

        # fg
        forecast_by_day = defaultdict(list)

        for item in data["list"]:
            date = datetime.fromtimestamp(item["dt"]).date()
            temp = item["main"]["temp"]
            desc = item["weather"][0]["description"]
            forecast_by_day[date].append((temp, desc))
        
        five_day_weather_forecast = []
        for date, values in list(forecast_by_day.items())[:5]:  # максимум 5 дней
            avg_temp = sum(v[0] for v in values) / len(values)
            descs = [v[1] for v in values]
            five_day_weather_forecast.append(f"{date}: {avg_temp:.1f} C, {descs[0]}")
        return five_day_weather_forecast