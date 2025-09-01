from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from urllib.parse import urlencode
import Weather_Forecast
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
WeatherForecast = Weather_Forecast.Weather_Forecast()

@app.get("/", response_class=HTMLResponse)
def show_form(request: Request):
    return templates.TemplateResponse(
        "index.html", 
        {"request": request}
    )

@app.post("/submit")
def submit_form(request: Request, city: str = Form(...)):
    params = urlencode({"city": city})
    return RedirectResponse(url=f"/result?{params}", status_code=303)

@app.get("/result", response_class=HTMLResponse)
def result_page(request: Request, city: str):
    five_day_weather_forecast = WeatherForecast.get_weather_forecast(city)
    return templates.TemplateResponse("result.html", {"request": request, "five_day_weather_forecast": five_day_weather_forecast})

