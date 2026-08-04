import json
import requests
from config import * # Importamos configuración

WEATHER_API_URL = "http://api.weatherapi.com/v1/forecast.json"
request_params = { # Parametros de Weather API:
    "key": API_KEY,
    "days": 2,
    "aqi": "no",
    "alerts": "no",
}

# OBTENER DATOS DE CADA PUNTO
for location in LOCATIONS:
    print(f"\n[+] | Getting weather for: {location}")
# Actualizar coordenadas
    request_params["q"] = location
    try:
        response = requests.get(
            WEATHER_API_URL,
            params=request_params)

        if response.status_code == 200:
            print("OK | Request accepted")

# Convertir la respuesta a JSON
            weather_data = response.json()

# Obtener la fecha para el nombre del archivo
            forecast_date = weather_data["forecast"]["forecastday"][0]["date"]

# Limpiar nombre del archivo
            clean_location = location.replace(",", "_")
            clean_date = forecast_date.replace("-", "")

            filename = FORECAST_DIR / f"weather_{clean_date}_{clean_location}.json"

# Guardar JSON completo
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(
                    weather_data,
                    file,
                    indent=4,
                    ensure_ascii=False)

            print(f"OK | Data saved: {filename}")

        else:
            print(f"FAIL | HTTP Error: {response.status_code}")

    except Exception as e:
        print(f"FAIL | Connection error: {e}")