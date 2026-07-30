# BUILD TRAINING DATASET
import os
import glob
import json
import csv
from datetime import datetime, timedelta

# List of hours to compare.
HOURS = [
    f"{hour:02d}:00" for hour in range(24)
]

# Fecha del archivo del día anterior a hoy.
selected_date = (
    datetime.today() - timedelta(days=1)
).strftime("%Y%m%d")
print("DATE SELECTED:", selected_date)

# Creamos carpeta para el dataset
FORECAST_FOLDER = "data/forecast"
HISTORY_FOLDER = "data/history"
TRAINING_FOLDER = "data/training"
os.makedirs(TRAINING_FOLDER, exist_ok=True)

training_data = []

# Buscamos los archivos
forecast_files = glob.glob(
    f"{FORECAST_FOLDER}/weather_{selected_date}_*.json"
)
print("FORECAST FILES:", len(forecast_files))

# Recorremos todos los documentos
for forecast_file in forecast_files:
    filename = os.path.basename(forecast_file)
    location_id = filename.replace(
    f"weather_{selected_date}_",
    "")

# Buscamos historico correspondiente.
    history_file = (
        f"{HISTORY_FOLDER}/history_{selected_date}_{location_id}")

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
                "hour": int(target_hour[:2]),
                "location": forecast_data["location"]["name"],

                # Forecast features
                "forecast_temp_c": forecast_record["temp_c"],
                "forecast_feelslike_c": forecast_record["feelslike_c"],
                "forecast_wind_kph": forecast_record["wind_kph"],
                "forecast_pressure_mb": forecast_record["pressure_mb"],
                "forecast_humidity": forecast_record["humidity"],
                "forecast_cloud": forecast_record["cloud"],
                "forecast_precip_mm": forecast_record["precip_mm"],
                "forecast_chance_of_rain": forecast_record["chance_of_rain"],
                "forecast_dewpoint_c": forecast_record["dewpoint_c"],
                "forecast_uv": forecast_record["uv"],
                "forecast_vis_km": forecast_record["vis_km"],
                "forecast_is_day": forecast_record["is_day"],
                # Target
                "history_precip_mm": history_record["precip_mm"]
            }

            training_data.append(record)
    except Exception as e:
        print(f"FAIL | Error processing {forecast_file}")
        print(e)

# Guardamos dataset
json_output = (
    f"{TRAINING_FOLDER}/training_data_{selected_date}.json")

try:

    with open(json_output, "w", encoding="utf-8") as file:
        json.dump(
            training_data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nOK | Dataset created")
    print("SAVED |", json_output)

except Exception as e:
    print("FAIL | Could not save dataset")
    print(e)

# Guardamos en CSV
csv_output = (
    f"{TRAINING_FOLDER}/dataset_{selected_date}.csv")

try:
    if len(training_data) > 0:
        with open(
            csv_output,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=training_data[0].keys()
            )
# Escribimos datos en CSV
            writer.writeheader()
            writer.writerows(training_data)

        print("OK | CSV dataset created")
        print("ROWS |", len(training_data))
        print("SAVED |", csv_output)

    else:
        print("FAIL | Dataset is empty")

except Exception as e:
    print("FAIL | Could not save CSV: ", e)
