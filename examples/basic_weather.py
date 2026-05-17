# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import json
import typing


class BasicWeather(gl.Contract):
    """
    Minimal example: fetch and store temperature for one city.
    Deploy in GenLayer Studio and call:
      fetch_temperature("40.7128", "-74.0060", "New York")
    """
    city: str
    temperature: str

    def __init__(self):
        self.city = ""
        self.temperature = ""

    @gl.public.write
    def fetch_temperature(self, latitude: str, longitude: str, city_name: str) -> typing.Any:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={latitude}&longitude={longitude}"
            f"&current=temperature_2m"
        )

        def get_temp() -> str:
            response = gl.nondet.web.get(url)
            data = json.loads(response.body.decode("utf-8"))
            temp = data["current"]["temperature_2m"]
            return str(temp)

        temp_str = gl.eq_principle.strict_eq(get_temp)
        self.city = city_name
        self.temperature = f"{temp_str}°C"

    @gl.public.view
    def read_temperature(self) -> str:
        if self.city == "":
            return "No temperature fetched yet"
        return f"{self.city}: {self.temperature}"
