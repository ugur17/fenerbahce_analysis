import json
import csv
from pathlib import Path

INPUT_FILE = "data/raw/player_stats/fixture_1074607_players.json"
OUTPUT_FILE = "data/processed/fixture_1074607_player_stats.csv"

Path("data/processed").mkdir(parents=True, exist_ok=True)

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)

rows = []

for team_block in data["response"]:
    team = team_block["team"]

    for player_block in team_block["players"]:
        player = player_block["player"]
        stats = player_block["statistics"][0]

        row = {
            "fixture_id": 1074607,
            "team_id": team["id"],
            "team_name": team["name"],
            "player_id": player["id"],
            "player_name": player["name"],
            "minutes": stats["games"]["minutes"],
            "position": stats["games"]["position"],
            "rating": stats["games"]["rating"],
            "captain": stats["games"]["captain"],
            "substitute": stats["games"]["substitute"],
            "shots_total": stats["shots"]["total"],
            "shots_on": stats["shots"]["on"],
            "goals": stats["goals"]["total"],
            "assists": stats["goals"]["assists"],
            "passes_total": stats["passes"]["total"],
            "passes_key": stats["passes"]["key"],
            "passes_accuracy": stats["passes"]["accuracy"],
            "tackles_total": stats["tackles"]["total"],
            "duels_total": stats["duels"]["total"],
            "duels_won": stats["duels"]["won"],
            "dribbles_attempts": stats["dribbles"]["attempts"],
            "dribbles_success": stats["dribbles"]["success"],
            "yellow_cards": stats["cards"]["yellow"],
            "red_cards": stats["cards"]["red"],
        }

        rows.append(row)

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Saved {len(rows)} player rows to {OUTPUT_FILE}")