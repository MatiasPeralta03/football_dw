"""
Ingesta de datos abiertos de StatsBomb a DuckDB.

Baja competencias, partidos y eventos de una competencia elegida
y los carga en el schema `raw` de un archivo DuckDB local.

Uso:
    uv run python ingestion/load_statsbomb.py
"""

import duckdb
import pandas as pd
from statsbombpy import sb

# ── Config ────────────────────────────────────────────────
DB_PATH = "data/football.duckdb"

# Mundial Qatar 2022 (datos abiertos de StatsBomb)
# Para ver otras opciones: print(sb.competitions())
COMPETITION_ID = 43  
# FIFA World Cup
SEASON_ID = 106       # 2022
# ──────────────────────────────────────────────────────────


def main():
    con = duckdb.connect(DB_PATH)
    con.execute("CREATE SCHEMA IF NOT EXISTS raw")

    # 1. Competencias disponibles
    print("Bajando competencias...")
    competitions = sb.competitions()
    con.execute("CREATE OR REPLACE TABLE raw.competitions AS SELECT * FROM competitions")
    print(f"  -> {len(competitions)} competencias cargadas")

    # 2. Partidos de la competencia elegida
    print("Bajando partidos...")
    matches = sb.matches(competition_id=COMPETITION_ID, season_id=SEASON_ID)
    con.execute("CREATE OR REPLACE TABLE raw.matches AS SELECT * FROM matches")
    print(f"  -> {len(matches)} partidos cargados")

    # 3. Eventos de cada partido (esto tarda unos minutos)
    print("Bajando eventos partido por partido...")
    all_events = []
    match_ids = matches["match_id"].tolist()

    for i, match_id in enumerate(match_ids, start=1):
        events = sb.events(match_id=match_id)
        all_events.append(events)
        print(f"  [{i}/{len(match_ids)}] match {match_id}: {len(events)} eventos")

    events_df = pd.concat(all_events, ignore_index=True)

    # Las columnas con listas/dicts (ej: location) se guardan como string
    # en raw; la limpieza fina la hacemos despues en dbt (staging).
    for col in events_df.columns:
        if events_df[col].apply(lambda x: isinstance(x, (list, dict))).any():
            events_df[col] = events_df[col].astype(str)

    con.execute("CREATE OR REPLACE TABLE raw.events AS SELECT * FROM events_df")
    print(f"  -> {len(events_df)} eventos totales cargados")

    # Resumen final
    print("\nTablas en el schema raw:")
    print(con.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'raw'").df())

    con.close()
    print(f"\nListo. Warehouse en {DB_PATH}")


if __name__ == "__main__":
    main()
