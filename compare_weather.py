# BUILD TRAINING DATASET

import os
import glob
import json
from datetime import datetime, timedelta

# List of hours to compare.
HOURS = [
    "04:00",
    "05:00",
    "06:00",
    "15:00",
    "16:00",
    "17:00"
]

# Fecha del archivo del día anterior a hoy.
selected_date = (
    datetime.today() - timedelta(days=1)
).strftime("%Y%m%d")
print("DATE SELECTED:", selected_date)

# Creamos carpeta para el dataset
os.makedirs("training", exist_ok=True)

training_data = []

# Buscamos los archivos
forecast_files = glob.glob(f"temp/weather_{selected_date}_*.json")
print("FORECAST FILES:", len(forecast_files))

# Recorremos todos los documentos
for forecast_file in forecast_files:
    location_id = forecast_file.replace(
        f"temp\\weather_{selected_date}_",
        ""
    )

# Buscamos historico correspondiente.
    history_file = f"temp/history_{selected_date}_{location_id}"

    if not os.path.exists(history_file):
        print("FAIL | History not found: ", history_file)
        continue

    print(f"\nCOMPARING: {location_id}")

    try:

# Abrimos archivo con predicción
        with open(forecast_file, "r", encoding="utf-8") as file:
            forecast_data = json.load(file)

# Abrimos historial correspondiente
        with open(history_file, "r", encoding="utf-8") as file:
            history_data = json.load(file)

# Extraemos horas
        forecast_hours = forecast_data["forecast"]["forecastday"][0]["hour"]
        history_hours = history_data["forecast"]["forecastday"][0]["hour"]

# Buscamos las horas de interés
        for target_hour in HOURS:

            forecast_record = None
            history_record = None

            for hour in forecast_hours:

                if hour["time"].endswith(target_hour):
                    forecast_record = hour
                    break

            for hour in history_hours:

                if hour["time"].endswith(target_hour):
                    history_record = hour
                    break

# Si no existe
            if forecast_record is None or history_record is None:
                print(f"FAIL | Hour not found: {target_hour}")
                continue

# Creamos el registro
            record = {

                "date": selected_date,

                "hour": target_hour,

                "location": forecast_data["location"]["name"],

                "forecast_humidity": forecast_record["humidity"],
                "forecast_cloud": forecast_record["cloud"],
                "forecast_chance_of_rain": forecast_record["chance_of_rain"],

                "history_humidity": history_record["humidity"],
                "history_cloud": history_record["cloud"],
                "history_precip_mm": history_record["precip_mm"]

            }

            training_data.append(record)
    except Exception as e:

        print(f"FAIL | Error processing {forecast_file}")
        print(e)

# Guardamos dataset
output_file = f"training/training_{selected_date}.json"

try:

    with open(output_file, "w", encoding="utf-8") as file:

        json.dump(
            training_data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nOK | Dataset created")
    print("SAVED | Records:", len(training_data))
    print("SAVED |", output_file)

except Exception as e:

    print("FAIL | Could not save dataset")
    print(e)