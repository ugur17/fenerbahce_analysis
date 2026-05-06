import requests
import json
from pathlib import Path

API_KEY = "b35e7620a9492b3b7bcfb0049d6f4b1b"
FIXTURE_ID = 1074607

url = "https://v3.football.api-sports.io/fixtures/players"

headers = {
    "x-apisports-key": API_KEY
}

params = {
    "fixture": FIXTURE_ID
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

print("Status:", response.status_code)
print("Errors:", data["errors"])
print("Results:", data["results"])
print(data["response"][0].keys() if data["response"] else "No response")

Path("data/raw/player_stats").mkdir(parents=True, exist_ok=True)

with open("data/raw/player_stats/fixture_1074607_players.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2, ensure_ascii=False)