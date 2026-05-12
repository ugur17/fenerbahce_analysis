import json
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")

if not API_KEY:
    raise ValueError("Missing API_FOOTBALL_KEY environment variable")

BASE_URL = "https://v3.football.api-sports.io"
ENDPOINT = "/fixtures"
URL = BASE_URL + ENDPOINT

HEADERS = {
    "x-apisports-key": API_KEY
}

LEAGUE_ID = 203
SEASONS = [2022, 2023, 2024]

Path("data/raw/league_fixtures").mkdir(parents=True, exist_ok=True)

for season in SEASONS:
    params = {
        "league": LEAGUE_ID,
        "season": season
    }

    response = requests.get(URL, headers=HEADERS, params=params)
    data = response.json()

    print(
        f"Season {season} | "
        f"Status {response.status_code} | "
        f"Results {data.get('results')}"
    )

    output_file = f"data/raw/league_fixtures/superlig_fixtures_{season}.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    time.sleep(1)
