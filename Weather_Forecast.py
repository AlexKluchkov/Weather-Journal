from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from urllib.parse import urlencode
import httpx
import Weather_Forecast
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/.well-known", StaticFiles(directory=".well-known"), name="well-known")
templates = Jinja2Templates(directory="templates")
WeatherForecast = Weather_Forecast.Weather_Forecast()


@app.get("/", response_class=HTMLResponse)
async def show_form(request: Request):

    client_host = request.client.host     # When uploading to the server, uncomment
    # client_host = "8.8.8.8"                 # When uploading to the server, comment
    
    # Обращаемся к бесплатному API для определения геолокации
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"http://ip-api.com/json/{client_host}?fields=status,country,regionName,city,lat,lon,query")
        my_city = resp.json()["city"]

    five_day_weather_forecast_date, five_day_weather_forecast_temperature, five_day_weather_forecast_description = WeatherForecast.get_five_day_weather_forecast(my_city)

    return templates.TemplateResponse("index.html", {"request": request, "my_city": my_city, "weather_forecast_date": five_day_weather_forecast_date, "weather_forecast_temperature": five_day_weather_forecast_temperature, "weather_forecast_description": five_day_weather_forecast_description})

@app.post("/submit")
def submit_query(request: Request, city: str = Form(...)):
    params = urlencode({"city": city})
    return RedirectResponse(url=f"/result?{params}", status_code=303)

@app.get("/result", response_class=HTMLResponse)
def result_page(request: Request, city: str):
    five_day_weather_forecast_date, five_day_weather_forecast_temperature, five_day_weather_forecast_description = WeatherForecast.get_five_day_weather_forecast(city)
    return templates.TemplateResponse("index.html", {"request": request, "my_city": city, "weather_forecast_date": five_day_weather_forecast_date, "weather_forecast_temperature": five_day_weather_forecast_temperature, "weather_forecast_description": five_day_weather_forecast_description})

@app.get("/weather-for-the-day", response_class=HTMLResponse)
async def result_page(request: Request):

    client_host = request.client.host     # When uploading to the server, uncomment
    # client_host = "8.8.8.8"                 # When uploading to the server, comment
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"http://ip-api.com/json/{client_host}?fields=status,country,regionName,city,lat,lon,query")
        city = resp.json()["city"]

    three_hours_weather_forecast_date, three_hours_weather_forecast_temperature, three_hours_weather_forecast_description = WeatherForecast.get_three_hours_weather_forecast(city)
    return templates.TemplateResponse("index.html", {"request": request, "my_city": city, "weather_forecast_date": three_hours_weather_forecast_date, "weather_forecast_temperature": three_hours_weather_forecast_temperature,  "weather_forecast_description": three_hours_weather_forecast_description})
