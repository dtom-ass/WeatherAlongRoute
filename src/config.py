import json
from pathlib import Path

# Configuración de la estructura y rutas del programa
# Directorio Root:
ROOT_DIR = Path(__file__).resolve().parent.parent

# Archivo de configuración:
CONFIG_FILE = ROOT_DIR / "config.json"

# Directorio Data:
DATA_DIR = ROOT_DIR / "data"

FORECAST_DIR = DATA_DIR / "forecast"
HISTORY_DIR = DATA_DIR / "history"
TRAINING_DIR = DATA_DIR / "training"

# Comprobación de directorios:

for folder in (FORECAST_DIR,
               HISTORY_DIR,
               TRAINING_DIR):
    
    folder.mkdir(parents=True, exist_ok=True)
    print(f"Path: {folder}")

# Configuración API
try:
    if CONFIG_FILE.exists(): # Valida la existencia del archivo.
        with open(CONFIG_FILE, "r", encoding="utf-8") as file: 
            config = json.load(file) # Abrimos el formato.
        API_KEY = config["WEATHER_API_KEY"]
        LOCATIONS = config["LOCATIONS"]
        print("OK | API configuration loaded")
    else:
        print(f"FAIL | {CONFIG_FILE} DOES NOT EXIST.")
        exit(1) # Detenemos en caso de error.
except Exception as e:
    print(f"FAIL | Check config.json: ({type(e).__name__}): {e}")
    exit(1) # Detenemos en caso de error.