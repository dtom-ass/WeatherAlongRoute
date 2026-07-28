from datetime import datetime, timedelta
import json
import csv

selected_date = (
    datetime.today() - timedelta(days=1)
).strftime("%Y%m%d")
print("DATE SELECTED:", selected_date)

INPUT = f"data/training/training_data_{selected_date}.json"
OUTPUT = f"data/training/dataset_{selected_date}.csv"

# Abrimos archivo de con comparación para el entrenamiento.
with open(INPUT, "r") as file:
    data = json.load(file)
print("OPEN FILE: ", INPUT)

rows = []

for item in data:

    row = {

        "hour": item["hour"], # Datos por hora.

        "forecast_temp_c":
            item["forecast_temp_c"],

        "forecast_feelslike_c":
            item["forecast_feelslike_c"],

        "forecast_wind_kph":
            item["forecast_wind_kph"],

        "forecast_pressure_mb":
            item["forecast_pressure_mb"],

        "forecast_humidity":
            item["forecast_humidity"],

        "forecast_cloud":
            item["forecast_cloud"],

        "forecast_precip_mm":
            item["forecast_precip_mm"],

        "forecast_chance_of_rain":
            item["forecast_chance_of_rain"],

        "forecast_dewpoint_c":
            item["forecast_dewpoint_c"],

        "forecast_uv":
            item["forecast_uv"],

        "forecast_vis_km":
            item["forecast_vis_km"],

        "forecast_is_day":
            item["forecast_is_day"],

        # Target
        "history_precip_mm":
            item["history_precip_mm"]

    }

    rows.append(row)

with open(OUTPUT,"w",newline="") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=rows[0].keys()
    )

    writer.writeheader()
    writer.writerows(rows)


print("OK | CSV created")