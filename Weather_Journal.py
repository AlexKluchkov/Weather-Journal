from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from urllib.parse import urlencode
import httpx
import Weather_Forecast
from fastapi.staticfiles import StaticFiles

import requests

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/.well-known", StaticFiles(directory=".well-known"), name="well-known")
templates = Jinja2Templates(directory="templates")
WeatherForecast = Weather_Forecast.Weather_Forecast()

def my_geolocetion(request):
    client_host = request.client.host     # When uploading to the server, uncomment
    response = requests.get(f"http://ip-api.com/json/{client_host}?fields=city,country,query")
    data = response.json()
    return data.get("city")

@app.get("/", response_class=HTMLResponse)
def show_form(request: Request): 
    my_city = my_geolocetion(request)
    five_day_weather_forecast_date, five_day_weather_forecast_temperature, five_day_weather_forecast_description = WeatherForecast.get_five_day_weather_forecast(my_city)
    return templates.TemplateResponse("index.html", {"request": request, "my_city": my_city, "weather_forecast_date": five_day_weather_forecast_date, "weather_forecast_temperature": five_day_weather_forecast_temperature, "weather_forecast_description": five_day_weather_forecast_description})

@app.post("/submit")
def submit_query(request: Request, city: str = Form(...)):
    params = urlencode({"city": city})
    return RedirectResponse(url=f"/result?{params}", status_code=303)

@app.get("/result", response_class=HTMLResponse)
def result_page(request: Request, city: str):
    five_day_weather_forecast_date, five_day_weather_forecast_temperature, five_day_weather_forecast_description = WeatherForecast.get_five_day_weather_forecast(city)
    if(five_day_weather_forecast_description == 'city not found'):
        return RedirectResponse(url="/")
    return templates.TemplateResponse("index.html", {"request": request, "my_city": city, "weather_forecast_date": five_day_weather_forecast_date, "weather_forecast_temperature": five_day_weather_forecast_temperature, "weather_forecast_description": five_day_weather_forecast_description})

@app.get("/weather-for-the-day", response_class=HTMLResponse)
async def weather_for_the_day_page(request: Request):
    city = my_geolocetion(request)
    three_hours_weather_forecast_time, three_hours_weather_forecast_temperature, three_hours_weather_forecast_description, three_hours_weather_forecast_date = WeatherForecast.get_three_hours_weather_forecast(city)
    return templates.TemplateResponse("result.html", {"request": request, "my_city": city, "weather_forecast_time": three_hours_weather_forecast_time, "weather_forecast_temperature": three_hours_weather_forecast_temperature,  "weather_forecast_description": three_hours_weather_forecast_description, "weather_forecast_date": three_hours_weather_forecast_date})
