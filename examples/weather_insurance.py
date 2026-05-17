# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import json
import typing


class WeatherInsurance(gl.Contract):
    """
    Parametric weather insurance example.
    Create a policy with a temperature threshold, then check
    if real weather data triggers the payout.

    Deploy in GenLayer Studio and try:
      create_policy("Dubai", "25.2048", "55.2708", "45")
      check_policy("Dubai")
      get_policy("Dubai")
    """
    policies: TreeMap[str, str]

    def __init__(self):
        pass

    @gl.public.write
    def create_policy(
        self, city_name: str, latitude: str,
        longitude: str, temperature_threshold: str
    ) -> typing.Any:
        policy = {
            "city": city_name,
            "latitude": latitude,
            "longitude": longitude,
            "threshold_c": float(temperature_threshold),
            "triggered": False,
            "last_temp": None,
            "status": "active",
        }
        self.policies[city_name] = json.dumps(policy)

    @gl.public.write
    def check_policy(self, city_name: str) -> typing.Any:
        stored = self.policies.get(city_name, "")
        if stored == "":
            return "No policy for this city"

        policy = json.loads(stored)
        if policy["triggered"]:
            return "Policy already triggered"

        lat = policy["latitude"]
        lon = policy["longitude"]
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m"
        )

        def fetch_temp() -> str:
            response = gl.nondet.web.get(url)
            data = json.loads(response.body.decode("utf-8"))
            return str(data["current"]["temperature_2m"])

        temp_str = gl.eq_principle.strict_eq(fetch_temp)
        current_temp = float(temp_str)

        policy["last_temp"] = current_temp
        if current_temp > policy["threshold_c"]:
            policy["triggered"] = True
            policy["status"] = "TRIGGERED"
        else:
            policy["status"] = "active"

        self.policies[city_name] = json.dumps(policy)

    @gl.public.view
    def get_policy(self, city_name: str) -> str:
        stored = self.policies.get(city_name, "")
        if stored == "":
            return f"No policy for {city_name}"
        return stored

    @gl.public.view
    def is_triggered(self, city_name: str) -> str:
        stored = self.policies.get(city_name, "")
        if stored == "":
            return f"No policy for {city_name}"
        policy = json.loads(stored)
        if policy["triggered"]:
            return f"YES — Policy for {city_name} was triggered"
        return f"NO — Policy for {city_name} is still active"
