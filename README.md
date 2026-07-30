# WeatherAlongRoute

WeatherAlongRoute is a personal Python project that estimates the probability of rain along my daily route.

The project uses the WeatherAPI forecast and history endpoints to collect weather data for predefined locations and hours.

Instead of relying only on the API's chance of rain, the final goal is to train a simple model using historical data to generate a custom rain prediction.

Eventually, this project will become a simple desktop/mobile application that answers one question:

> **Should I take an umbrella today?**

---

## Weather API

This project uses the free API provided by **WeatherAPI**.

Website:
https://www.weatherapi.com/

---

## Current Scripts

- `fetch_weather.py` → Downloads weather forecasts.
- `history_weather.py` → Downloads historical weather.
- `build_dataset.py` → Builds the training dataset (JSON and CSV).

---

## How to use

1. Create a `config.json` file:

```json
{
    "WEATHER_API_KEY": "YOUR_API_KEY",
    "LOCATIONS": [
        "latitude,longitude",
        "latitude,longitude"
    ]
}
```

2. Download the forecast:

```bash
python src/fetch_weather.py
```

3. Download yesterday's historical data:

```bash
python src/history_weather.py
```

4. Generate the training dataset:

```bash
python src/build_dataset.py
```

---

## Current Status

- Forecast downloader
- Historical weather downloader
- Training dataset generation

## In Progress

- XGBoost training model
- Rain prediction algorithm
- Desktop/mobile interface