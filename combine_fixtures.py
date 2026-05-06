# This script combines fixture data from multiple seasons into a single CSV file.
# It reads the processed fixture CSV files for each season, aggregates the rows, and saves them into a new CSV file.
# The combined CSV file can be used for analysis or as a source for database insertion.
# Note: This script assumes that the processed fixture CSV files for each season already exist in the "data/processed" directory.
# Usage:
# 1. Ensure that the processed fixture CSV files for each season are available in the "data/processed" directory.
# 2. Run this script to generate the combined CSV file "data/processed/fenerbahce_fixtures_all.csv".
# 3. The output file will contain all fixture data from the specified seasons, ready for further analysis or database insertion.
# Author: Ceyhun Ugur

import csv
from pathlib import Path

SEASONS = [2022, 2023, 2024]

OUTPUT_FILE = "data/processed/fenerbahce_fixtures_all.csv"

all_rows = []

for season in SEASONS:
    input_file = f"data/processed/fenerbahce_fixtures_{season}.csv"

    with open(input_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            all_rows.append(row)

if not all_rows:
    raise ValueError("No fixture rows found.")

Path("data/processed").mkdir(parents=True, exist_ok=True)

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=all_rows[0].keys())
    writer.writeheader()
    writer.writerows(all_rows)

print(f"Saved {len(all_rows)} rows to {OUTPUT_FILE}")