# This script processes raw player statistics data for Fenerbahçe from JSON files and converts it into a structured CSV file.
# It reads the raw JSON files for each season, extracts relevant information about each player's performance in each fixture, and saves the data into a single CSV file for easier analysis and database insertion.
# The script also handles cases where the JSON files may contain errors or be empty, ensuring that only valid data is processed. 
# Author: Ceyhun Ugur

import csv
import glob
import json
from pathlib import Path

SEASONS = [2022, 2023, 2024]
OUTPUT_FILE = "data/processed/fenerbahce_player_stats_all.csv"

Path("data/processed").mkdir(parents=True, exist_ok=True)

all_rows = []


def value_or_zero(value):
    if value is None:
        return 0
    return value


def value_or_blank(value):
    if value is None:
        return ""
    return value


for season in SEASONS:
    files = glob.glob(f"data/raw/player_stats/{season}/*.json")

    print(f"Season {season}: found {len(files)} JSON files")

    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if data.get("errors"):
            print(f"Skipping bad file: {file_path}")
            continue

        if not data.get("response"):
            print(f"Skipping empty file: {file_path}")
            continue

        fixture_id = Path(file_path).stem.replace("fixture_", "").replace("_players", "")

        for team_block in data["response"]:
            team = team_block["team"]

            for player_block in team_block["players"]:
                player = player_block["player"]

                if not player_block.get("statistics"):
                    continue

                stats = player_block["statistics"][0]

                row = {
                    "season": season,
                    "fixture_id": fixture_id,

                    "team_id": team.get("id"),
                    "team_name": team.get("name"),

                    "player_id": player.get("id"),
                    "player_name": player.get("name"),

                    "minutes": value_or_zero(stats["games"].get("minutes")),
                    "shirt_number": value_or_blank(stats["games"].get("number")),
                    "position": value_or_blank(stats["games"].get("position")),
                    "rating": value_or_blank(stats["games"].get("rating")),
                    "captain": stats["games"].get("captain"),
                    "substitute": stats["games"].get("substitute"),

                    "offsides": value_or_zero(stats.get("offsides")),

                    "shots_total": value_or_zero(stats["shots"].get("total")),
                    "shots_on": value_or_zero(stats["shots"].get("on")),

                    "goals": value_or_zero(stats["goals"].get("total")),
                    "goals_conceded": value_or_zero(stats["goals"].get("conceded")),
                    "assists": value_or_zero(stats["goals"].get("assists")),
                    "saves": value_or_zero(stats["goals"].get("saves")),

                    "passes_total": value_or_zero(stats["passes"].get("total")),
                    "passes_key": value_or_zero(stats["passes"].get("key")),
                    "passes_accuracy": value_or_blank(stats["passes"].get("accuracy")),

                    "tackles_total": value_or_zero(stats["tackles"].get("total")),
                    "tackles_blocks": value_or_zero(stats["tackles"].get("blocks")),
                    "tackles_interceptions": value_or_zero(stats["tackles"].get("interceptions")),

                    "duels_total": value_or_zero(stats["duels"].get("total")),
                    "duels_won": value_or_zero(stats["duels"].get("won")),

                    "dribbles_attempts": value_or_zero(stats["dribbles"].get("attempts")),
                    "dribbles_success": value_or_zero(stats["dribbles"].get("success")),
                    "dribbles_past": value_or_zero(stats["dribbles"].get("past")),

                    "fouls_drawn": value_or_zero(stats["fouls"].get("drawn")),
                    "fouls_committed": value_or_zero(stats["fouls"].get("committed")),

                    "yellow_cards": value_or_zero(stats["cards"].get("yellow")),
                    "red_cards": value_or_zero(stats["cards"].get("red")),

                    "penalty_won": value_or_zero(stats["penalty"].get("won")),
                    "penalty_committed": value_or_zero(stats["penalty"].get("commited")),
                    "penalty_scored": value_or_zero(stats["penalty"].get("scored")),
                    "penalty_missed": value_or_zero(stats["penalty"].get("missed")),
                    "penalty_saved": value_or_zero(stats["penalty"].get("saved")),
                }

                all_rows.append(row)

if not all_rows:
    raise ValueError("No player rows found. Check your raw JSON files.")

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=all_rows[0].keys())
    writer.writeheader()
    writer.writerows(all_rows)

print(f"Saved {len(all_rows)} rows to {OUTPUT_FILE}")