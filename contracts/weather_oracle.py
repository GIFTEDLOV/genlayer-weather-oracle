# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import json
import typing


# WMO Weather Code descriptions
WEATHER_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    80: "Slight rain showers", 81: "Moderate rain showers",
    82: "Violent rain showers", 95: "Thunderstorm",
    96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail",
}


class WeatherOracle(gl.Contract):
    weather_data: TreeMap[str, str]
    cities: DynArray[str]
    city_count: u32

    def __init__(self):
        self.city_count = u32(0)

    @gl.public.write
    def get_weather(self, latitude: str, longitude: str, city_name: str) -> typing.Any:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={latitude}&longitude={longitude}"
            f"&current=temperature_2m,relative_humidity_2m,"
            f"apparent_temperature,weather_code,wind_speed_10m"
        )

        def fetch_weather() -> str:
            response = gl.nondet.web.get(url)
            raw = response.body.decode("utf-8")
            data = json.loads(raw)
            current = data["current"]
            temp = current.get("temperature_2m", 0)
            feels = current.get("apparent_temperature", 0)
            humidity = current.get("relative_humidity_2m", 0)
            wind = current.get("wind_speed_10m", 0)
            code = current.get("weather_code", 0)
            conditions = WEATHER_CODES.get(code, f"Unknown ({code})")
            result = {
                "city": city_name,
                "temperature_c": temp,
                "feels_like_c": feels,
                "humidity_percent": humidity,
                "wind_speed_kmh": wind,
                "weather_code": code,
                "conditions": conditions,
            }
            return json.dumps(result)

        weather_json = gl.eq_principle.strict_eq(fetch_weather)
        self.weather_data[city_name] = weather_json

        already_tracked = False
        for c in self.cities:
            if c == city_name:
                already_tracked = True
                break
        if not already_tracked:
            self.cities.append(city_name)
            self.city_count = u32(self.city_count + 1)

    @gl.public.view
    def read_weather(self, city_name: str) -> str:
        stored = self.weather_data.get(city_name, "")
        if stored == "":
            return f"No weather data for {city_name}. Call get_weather first."
        return stored

    @gl.public.view
    def get_all_cities(self) -> str:
        result = [c for c in self.cities]
        return json.dumps(result)

    @gl.public.view
    def get_temperature(self, city_name: str) -> str:
        stored = self.weather_data.get(city_name, "")
        if stored == "":
            return f"No data for {city_name}"
        data = json.loads(stored)
        return f"{data['temperature_c']}°C"

    @gl.public.view
    def get_conditions(self, city_name: str) -> str:
        stored = self.weather_data.get(city_name, "")
        if stored == "":
            return f"No data for {city_name}"
        data = json.loads(stored)
        return data["conditions"]

    @gl.public.view
    def decode_weather_code(self, code: u32) -> str:
        return WEATHER_CODES.get(int(code), f"Unknown code: {code}")
