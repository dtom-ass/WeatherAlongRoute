# WeatherAlongRoute

WeatherAlongRoute is a personal Python project that estimates the probability of rain along my daily route.

The project uses the WeatherAPI forecast and history endpoints to collect weather data for predefined locations and hours.

Instead of relying only on the API's chance of rain, the final goal is to train a simple model using historical data to generate a custom rain prediction.

Eventually, this project will become a simple desktop/mobile application that answers one question:

> **Should I take an umbrella today?**

---

## Current Files

### `fetch_weather.py`

Downloads the weather forecast for all configured locations and stores the complete JSON response.

### `history_weather.py`

Downloads the historical weather data from the previous day for the same locations.

### `compare_weather.py`

Compares forecast and historical data, then generates a training dataset for future model training.

### `extraction_data.py`

Extracts weather variables for a selected date and hour. Used for testing and data exploration.

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
python fetch_weather.py
```

3. Download yesterday's historical data:

```bash
python history_weather.py
```

4. Generate the training dataset:

```bash
python compare_weather.py
```

---

## Current Status

- Forecast downloader
- Historical weather downloader
- Automatic training dataset generation

In Progress

- Training model
- Rain prediction algorithm
- Graphical interface