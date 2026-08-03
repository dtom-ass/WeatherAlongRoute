import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

# Seleccionamos fecha previa.
history_date = (
    datetime.today() - timedelta(days=1)
).strftime("%Y-%m-%d")

# Path absoluto del .py
THIS_FILE = Path(__file__).resolve()
BASE_DIR = THIS_FILE.parent.parent # Ruta anterior (/src)

# CARGAR API KEY
try:
    config_path = BASE_DIR / "config.json"
    with open(config_path, "r") as file:
        config = json.load(file)

    API_KEY = config["WEATHER_API_KEY"]
# DEFINIR RUTA
    locations = config["LOCATIONS"]
    print("OK | API Key loaded")

except Exception as e:
    print("FAIL | Check config.json:", e)
    API_KEY = None

# CONFIGURAR API
WEATHER_API_URL = "http://api.weatherapi.com/v1/history.json"

request_params = {
    "key": API_KEY,
    "aqi": "no",
    "alerts": "no",
    "dt": history_date
}

# CREAR CARPETA TEMPORAL
DATA_DIR = BASE_DIR / "data" / "history"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# OBTENER DATOS DE CADA PUNTO
for location in locations:

    print(f"\n[+] Getting history for: {location}")

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

            filename = DATA_DIR / f"history_{clean_date}_{clean_location}.json"

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