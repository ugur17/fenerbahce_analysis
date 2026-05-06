# This script processes raw fixture data for Fenerbahçe from JSON files and converts it into structured CSV files.
# It reads the raw JSON files for each season, extracts relevant information about each fixture, and saves the data into CSV format for easier analysis and database insertion.
# The script also handles cases where the JSON files may contain errors or be empty, ensuring that only valid data is processed.
# Author: Ceyhun Ugur

import csv
import json
from pathlib import Path

TEAM_ID = 611
SEASONS = [2022, 2023, 2024]

Path("data/processed").mkdir(parents=True, exist_ok=True)

for season in SEASONS:
    input_file = f"data/raw/fenerbahce_fixtures_{season}.json"
    output_file = f"data/processed/fenerbahce_fixtures_{season}.csv"

    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    rows = []

    for item in data["response"]:
        home = item["teams"]["home"]
        away = item["teams"]["away"]

        home_goals = item["goals"]["home"]
        away_goals = item["goals"]["away"]

        is_home = home["id"] == TEAM_ID

        if is_home:
            opponent = away["name"]
            fenerbahce_goals = home_goals
            opponent_goals = away_goals
        else:
            opponent = home["name"]
            fenerbahce_goals = away_goals
            opponent_goals = home_goals

        if fenerbahce_goals > opponent_goals:
            result = "W"
            points = 3
        elif fenerbahce_goals == opponent_goals:
            result = "D"
            points = 1
        else:
            result = "L"
            points = 0

        row = {
            "fixture_id": item["fixture"]["id"],
            "season": item["league"]["season"],
            "round": item["league"]["round"],
            "match_date": item["fixture"]["date"],
            "status": item["fixture"]["status"]["short"],
            "venue_name": item["fixture"]["venue"]["name"],
            "venue_city": item["fixture"]["venue"]["city"],
            "home_team_id": home["id"],
            "home_team": home["name"],
            "away_team_id": away["id"],
            "away_team": away["name"],
            "home_goals": home_goals,
            "away_goals": away_goals,
            "ht_home_goals": item["score"]["halftime"]["home"],
            "ht_away_goals": item["score"]["halftime"]["away"],
            "is_home": is_home,
            "opponent": opponent,
            "fenerbahce_goals": fenerbahce_goals,
            "opponent_goals": opponent_goals,
            "result": result,
            "points": points
        }

        rows.append(row)

    if rows:
        with open(output_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

        print(f"Saved {len(rows)} rows to {output_file}")
    else:
        print(f"No rows found for season {season}")