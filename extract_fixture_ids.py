import csv
import json
import time
from pathlib import Path

import requests

API_KEY = "b35e7620a9492b3b7bcfb0049d6f4b1b"

BASE_URL = "https://v3.football.api-sports.io"
ENDPOINT = "/fixtures/players"
URL = BASE_URL + ENDPOINT

headers = {
    "x-apisports-key": API_KEY
}

fixture_ids = []

with open("data/processed/fenerbahce_fixtures_2024.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        fixture_ids.append(row["fixture_id"])

Path("data/raw/player_stats").mkdir(parents=True, exist_ok=True)

for fixture_id in fixture_ids:
    print(f"Fetching player stats for fixture {fixture_id}...")

    params = {
        "fixture": fixture_id
    }

    response = requests.get(URL, headers=headers, params=params)
    data = response.json()

    output_file = f"data/raw/player_stats/fixture_{fixture_id}_players.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    print(f"Status: {response.status_code} | Results: {data.get('results')}")
    print(f"Saved: {output_file}")

    time.sleep(1)