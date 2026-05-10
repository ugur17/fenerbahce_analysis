# This script retrieves fixture data for Fenerbahçe from the API-Football for specified seasons and saves the raw JSON responses to files.
# It uses the requests library to make API calls and the json library to handle JSON data.
# The script also includes a delay between API calls to respect rate limits.
# Author: Ceyhun Ugur

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

TEAM_ID = 611
LEAGUE_ID = 203
SEASONS = [2022, 2023, 2024]

Path("data/raw").mkdir(parents=True, exist_ok=True)

for season in SEASONS:
    params = {
        "team": TEAM_ID,
        "league": LEAGUE_ID,
        "season": season
    }

    response = requests.get(URL, headers=HEADERS, params=params)
    data = response.json()

    print(f"Season {season} | Status {response.status_code} | Results {data.get('results')}")

    output_file = f"data/raw/fenerbahce_fixtures_{season}.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    time.sleep(1)
