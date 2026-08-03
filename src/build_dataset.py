# BUILD TRAINING DATASET
import json
from datetime import datetime, timedelta
import pandas as pd
from pathlib import Path

# Fecha del archivo del día anterior
selected_date = (datetime.today() - timedelta(days=1)).strftime("%Y%m%d")
print("DATE SELECTED:", selected_date)

# Creamos carpeta para el dataset
THIS_FILE = Path(__file__).resolve()
BASE_DIR = THIS_FILE.parent.parent  # Sube de 'src/' a la raíz del proyecto
DATA_DIR = BASE_DIR / "data"

FORECAST_FOLDER = DATA_DIR / "forecast"
HISTORY_FOLDER = DATA_DIR / "history"
TRAINING_FOLDER = DATA_DIR / "training"
# Crear directorio de salida si no existe
TRAINING_FOLDER.mkdir(parents=True, exist_ok=True)

training_data = []

# Buscamos los archivos
forecast_files = list(
    FORECAST_FOLDER.glob(f"weather_{selected_date}_*.json")
)
print("FORECAST FILES:", len(forecast_files))

# Recorremos todos los documentos
for forecast_file in forecast_files:
    # Obtener el ID de la ubicación usando las propiedades de Path
    filename = forecast_file.name
    location_id = filename.replace(f"weather_{selected_date}_", "")

    # Buscamos histórico correspondiente
    history_file = HISTORY_FOLDER / f"history_{selected_date}_{location_id}"

    if not history_file.exists():
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
# Iteración paralela $O(N)$ usando zip
        for f_hour, h_hour in zip(forecast_hours, history_hours):
 # Extraemos la hora como entero (ej. "2026-08-02 14:00" -> 14)
            hour_int = int(f_hour["time"].split()[-1].split(":")[0])

            record = {
                "date": selected_date,
                "hour": hour_int,
                "location": forecast_data["location"]["name"],
# Forecast features
                "forecast_temp_c": f_hour.get("temp_c"),
                "forecast_feelslike_c": f_hour.get("feelslike_c"),
                "forecast_wind_kph": f_hour.get("wind_kph"),
                "forecast_pressure_mb": f_hour.get("pressure_mb"),
                "forecast_humidity": f_hour.get("humidity"),
                "forecast_cloud": f_hour.get("cloud"),
                "forecast_precip_mm": f_hour.get("precip_mm"),
                "forecast_chance_of_rain": f_hour.get("chance_of_rain"),
                "forecast_dewpoint_c": f_hour.get("dewpoint_c"),
                "forecast_uv": f_hour.get("uv"),
                "forecast_vis_km": f_hour.get("vis_km"),
                "forecast_is_day": f_hour.get("is_day"),
# Target
                "history_precip_mm": h_hour.get("precip_mm"),
            }

            training_data.append(record)
    except Exception as e:
        print(f"FAIL | Error processing {forecast_file}: {e}")

# Guardamos datasetif training_data:
if training_data:
    df = pd.DataFrame(training_data)

# Deduplicación segura basada en la clave única (Fecha, Ubicación, Hora)
    initial_rows = len(df)
    df_clean = df.drop_duplicates(
        subset=["date", "location", "hour"], keep="first"
    )
    removed_rows = initial_rows - len(df_clean)

    print(f"\n--- RESUME ---")
    print(f"Rows: {initial_rows}")
    print(f"Deleted: {removed_rows}")
    print(f"Rows cleaned: {len(df_clean)}")

# RUTAS DE SALIDA
    json_clean_output = TRAINING_FOLDER / f"training_data_{selected_date}.json"
    csv_clean_output = TRAINING_FOLDER / f"dataset_{selected_date}.csv"

# GUARDAR JSON LIMPIO
    df_clean.to_json(
        json_clean_output, orient="records", indent=4, force_ascii=False
    )
    print(f"SAVED JSON | {json_clean_output}")

# GUARDAR CSV LIMPIO
    df_clean.to_csv(csv_clean_output, index=False, encoding="utf-8")
    print(f"SAVED CSV  | {csv_clean_output}")

else:
    print("\nFAIL | No data collected. Dataset is empty.")