"""
Ingestion of StatsBomb open data into DuckDB.

Downloads competitions, matches, and events for a selected competition
and loads them into the `raw` schema of a local DuckDB file.

Usage:
    uv run python ingestion/load_statsbomb.py
"""

import duckdb
import pandas as pd
from statsbombpy import sb

# ── Config ────────────────────────────────────────────────
DB_PATH = "data/football.duckdb"

# FIFA World Cup Qatar 2022 (StatsBomb open data)
# To explore other options: print(sb.competitions())
COMPETITION_ID = 43  
# FIFA World Cup
SEASON_ID = 106       # 2022
# ──────────────────────────────────────────────────────────


def main():
    con = duckdb.connect(DB_PATH)
    con.execute("CREATE SCHEMA IF NOT EXISTS raw")

    # 1. Available competitions
    print("Downloading competitions...")
    competitions = sb.competitions()
    con.execute("CREATE OR REPLACE TABLE raw.competitions AS SELECT * FROM competitions")
    print(f"  -> {len(competitions)} competitions loaded")

    # 2. Matches for the selected competition
    print("Downloading matches...")
    matches = sb.matches(competition_id=COMPETITION_ID, season_id=SEASON_ID)
    con.execute("CREATE OR REPLACE TABLE raw.matches AS SELECT * FROM matches")
    print(f"  -> {len(matches)} matches loaded")

    # 3. Events for each match (this takes a few minutes)
    print("Downloading events match by match...")
    all_events = []
    match_ids = matches["match_id"].tolist()

    for i, match_id in enumerate(match_ids, start=1):
        events = sb.events(match_id=match_id)
        all_events.append(events)
        print(f"  [{i}/{len(match_ids)}] match {match_id}: {len(events)} events")

    events_df = pd.concat(all_events, ignore_index=True)

    # Columns with lists/dicts (e.g. location) are stored as strings
    # in raw; fine-grained cleaning is handled later in dbt (staging).
    for col in events_df.columns:
        if events_df[col].apply(lambda x: isinstance(x, (list, dict))).any():
            events_df[col] = events_df[col].astype(str)

    con.execute("CREATE OR REPLACE TABLE raw.events AS SELECT * FROM events_df")
    print(f"  -> {len(events_df)} total events loaded")

    # Final summary
    print("\nTables in the raw schema:")
    print(con.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'raw'").df())

    con.close()
    print(f"\nDone. Warehouse at {DB_PATH}")


if __name__ == "__main__":
    main()
