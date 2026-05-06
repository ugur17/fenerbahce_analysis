import json
import time
from pathlib import Path

import requests

BASE_URL = "https://v3.football.api-sports.io"
ENDPOINT = "/fixtures"
URL = BASE_URL + ENDPOINT

HEADERS = {
    "x-apisports-key": "b35e7620a9492b3b7bcfb0049d6f4b1b"
}

TEAM_ID = 611
LEAGUE_ID = 203
SEASONS = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

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