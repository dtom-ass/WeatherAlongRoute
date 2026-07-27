import time
import json
import glob

# Seleccionamos fecha y hora del archivo
target_datetime = str(time.strftime("%Y-%m-%d") + " 16:00") # HORA!

print("SEARCHING: " + target_datetime)
selected_date = "20260727"
print("DATE SELECTED: "+ selected_date)

# Leer los archivos descargados
files = glob.glob(f'temp/weather_{selected_date}_*.json')

forecast_data = []


for file_name in files:
    with open(file_name, "r") as file:
        print("FILE SELECTED: " + file_name)
        weather_data = json.load(file)
# 0 corresponde al pronóstico del día actual.
# 1 corresponde al pronóstico del día siguiente.
    hourly_forecast = weather_data["forecast"]["forecastday"][0]["hour"]

# Buscar el pronóstico correspondiente
    for hour in range(len(hourly_forecast)):
        if hourly_forecast[hour]["time"] == target_datetime:
              print("DATE FOUND: "+ target_datetime)
              print("Humidity: ", hourly_forecast[hour]["humidity"])
              print("Cloud: ", hourly_forecast[hour]["cloud"])
              print("Chance Of Rain: ", hourly_forecast[hour]["chance_of_rain"])
              # Guardamos data en un diccionario.
              forecast_data.append({
                "location": weather_data["location"]["name"],
                "humidity": hourly_forecast[hour]["humidity"],
                "cloud": hourly_forecast[hour]["cloud"],
                "chance_of_rain": hourly_forecast[hour]["chance_of_rain"]
                })
              break    
        hour += 1
