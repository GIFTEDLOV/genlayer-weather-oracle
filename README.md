# GenLayer Weather Oracle

A reusable helper library for GenLayer Intelligent Contracts to fetch real-time weather data directly on-chain — no API keys, no oracles, no middlemen.

Built on [Open-Meteo](https://open-meteo.com/), a free and open-source weather API.

## Features

- **Current weather** — temperature, humidity, wind speed, conditions
- **Multi-city support** — store and retrieve weather data for multiple locations
- **WMO weather code decoder** — human-readable weather descriptions
- **Parametric insurance example** — trigger payouts based on real weather
- **GenVM-lint compliant** — uses `TreeMap`, `DynArray`, and `u32` storage types
- **Consensus-friendly** — uses `gl.eq_principle.strict_eq` for validator agreement
- **No API key required** — Open-Meteo is completely free

## Quick Start

1. Open [GenLayer Studio](https://studio.genlayer.com)
2. Copy `contracts/weather_oracle.py` into the editor
3. Click **Deploy**
4. Call `get_weather` with latitude, longitude, and city name

```python
# Fetch weather for Lagos
get_weather("6.5244", "3.3792", "Lagos")

# Read the stored data
read_weather("Lagos")

# Get just the temperature
get_temperature("Lagos")

# Get all tracked cities
get_all_cities()
```

## Project Structure

```
genlayer-weather-oracle/
├── README.md
├── LICENSE
├── contracts/
│   └── weather_oracle.py          # Main contract (TreeMap + DynArray storage)
├── examples/
│   ├── basic_weather.py           # Minimal single-city example
│   └── weather_insurance.py       # Parametric insurance example
└── utils/
    └── city_coordinates.py        # Common city lat/long reference
```

## Storage Types Used

This library uses GenLayer's required persistent storage types:

| GenLayer Type | Replaces | Used For |
|---------------|----------|----------|
| `TreeMap[str, str]` | `dict` | Weather data per city (JSON-serialized) |
| `DynArray[str]` | `list` | List of tracked city names |
| `u32` | `int` | City count |
| `str` | `str` | Simple text fields |

## API Methods

| Method | Type | Description |
|--------|------|-------------|
| `get_weather(lat, lon, city)` | write | Fetches and stores current weather |
| `read_weather(city)` | view | Returns stored weather JSON |
| `get_all_cities()` | view | Returns JSON list of all cities |
| `get_temperature(city)` | view | Returns temperature string |
| `get_conditions(city)` | view | Returns weather conditions |
| `decode_weather_code(code)` | view | Converts WMO code to description |

## Use Cases

- **Parametric insurance** — automatic payouts based on weather conditions
- **Supply chain** — logistics adjustments based on weather
- **DeFi** — weather-based prediction markets
- **Agriculture** — on-chain crop insurance tied to rainfall and temperature

## Resources

- [GenLayer Docs](https://docs.genlayer.com)
- [GenLayer Studio](https://studio.genlayer.com)
- [Open-Meteo API](https://open-meteo.com/en/docs)
- [GenLayer Builder Program](https://portal.genlayer.foundation)

## License

MIT License — see [LICENSE](LICENSE)
