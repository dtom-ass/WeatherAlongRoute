import json
import os
import requests

# CARGAR API KEY
try:
    with open("config.json", "r") as file:
        config = json.load(file)

    API_KEY = config["WEATHER_API_KEY"]
    # DEFINIR RUTA
    locations = config["LOCATIONS"]
    print("OK | API Key loaded")

except Exception as e:
    print("FAIL | Check config.json:", e)
    API_KEY = None

# CONFIGURAR API
WEATHER_API_URL = "http://api.weatherapi.com/v1/forecast.json"

request_params = {
    "key": API_KEY,
    "days": 2,
    "aqi": "no",
    "alerts": "no",
}

# CREAR CARPETA TEMPORAL
os.makedirs("data/forecast", exist_ok=True)

# OBTENER DATOS DE CADA PUNTO
for location in locations:

    print(f"\n[+] Getting weather for: {location}")

# Actualizar coordenadas
    request_params["q"] = location

    try:
        response = requests.get(
            WEATHER_API_URL,
            params=request_params,
        )

        if response.status_code == 200:

            print("OK | Request accepted")

# Convertir la respuesta a JSON
            weather_data = response.json()

# Obtener la fecha para el nombre del archivo
            forecast_date = weather_data["forecast"]["forecastday"][0]["date"]

# Limpiar nombre del archivo
            clean_location = location.replace(",", "_")
            clean_date = forecast_date.replace("-", "")

            filename = f"data/forecast/weather_{clean_date}_{clean_location}.json"

# Guardar JSON completo
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(
                    weather_data,
                    file,
                    indent=4,
                    ensure_ascii=False,
                )

            print(f"OK | Data saved: {filename}")

        else:
            print(f"FAIL | HTTP Error: {response.status_code}")

    except Exception as e:
        print(f"FAIL | Connection error: {e}")