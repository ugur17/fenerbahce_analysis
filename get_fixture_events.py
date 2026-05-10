import csv
import json
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")

if not API_KEY:
    raise ValueError("Missing API_FOOTBALL_KEY")

BASE_URL = "https://v3.football.api-sports.io"
ENDPOINT = "/fixtures/events"
URL = BASE_URL + ENDPOINT

HEADERS = {
    "x-apisports-key": API_KEY
}

SEASONS = [2022, 2023, 2024]


def is_bad_file(file_path):
    if not Path(file_path).exists():
        return False

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return bool(data.get("errors"))

    except Exception:
        return True


for season in SEASONS:
    fixture_csv = f"data/processed/fenerbahce_fixtures_{season}.csv"
    output_folder = f"data/raw/events/{season}"

    Path(output_folder).mkdir(parents=True, exist_ok=True)

    fixture_ids = []

    with open(fixture_csv, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            fixture_ids.append(row["fixture_id"])

    print(f"\nSeason {season}: {len(fixture_ids)} fixtures")

    for fixture_id in fixture_ids:
        output_file = f"{output_folder}/fixture_{fixture_id}_events.json"

        if Path(output_file).exists() and not is_bad_file(output_file):
            print(f"Skipping fixture {fixture_id}, good file already exists")
            continue

        if Path(output_file).exists() and is_bad_file(output_file):
            print(f"Replacing bad file for fixture {fixture_id}")
            Path(output_file).unlink()

        params = {
            "fixture": fixture_id
        }

        max_retries = 5
        data = None

        for attempt in range(1, max_retries + 1):
            response = requests.get(URL, headers=HEADERS, params=params)
            data = response.json()

            if data.get("errors") and "rateLimit" in data["errors"]:
                print(
                    f"Rate limit for fixture {fixture_id}. "
                    f"Attempt {attempt}/{max_retries}. Waiting 20 seconds..."
                )
                time.sleep(20)
                continue

            if data.get("errors"):
                print(f"ERROR for fixture {fixture_id}: {data['errors']}")
                data = None
                break

            break

        if data is None:
            print(f"Skipping fixture {fixture_id} because request failed.")
            continue

        if data.get("errors"):
            print(f"Skipping fixture {fixture_id} after retries.")
            continue

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

        print(
            f"Season {season} | Fixture {fixture_id} | "
            f"Status {response.status_code} | Events: {data.get('results')}"
        )

        time.sleep(7)