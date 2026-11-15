"""Print a reproducible integrity summary for the supplied transport datasets."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
GTFS = ROOT / "data" / "gtfs"


def main():
    print("PuneSahayak dataset audit")
    print("=" * 48)
    for name in ["routes", "trips", "stops", "stop_times"]:
        path = GTFS / f"{name}.txt"
        df = pd.read_csv(path, low_memory=False)
        print(f"{name:12} rows={len(df):>9,} columns={len(df.columns):>2}")
        id_col = {"routes":"route_id", "trips":"trip_id", "stops":"stop_id", "stop_times":None}[name]
        if id_col and id_col in df:
            print(f"  unique {id_col}: {df[id_col].nunique():,}; duplicate IDs: {df[id_col].duplicated().sum():,}")
    stops = pd.read_csv(GTFS / "stops.txt")
    print(f"Stops with coordinates: {stops[['stop_lat','stop_lon']].notna().all(axis=1).sum():,}/{len(stops):,}")
    supplemental = pd.read_csv(ROOT / "data" / "routes.csv")
    print(f"Supplemental route catalogue rows: {len(supplemental):,}")
    metro = pd.read_csv(GTFS / "metro_stations.csv")
    print(f"Metro station-corridor records: {len(metro):,}; unique names: {metro['station'].nunique():,}")
    print("Service calendar files present:", (GTFS/"calendar.txt").exists() or (GTFS/"calendar_dates.txt").exists())
    print("NOTE: counts describe this included snapshot, not a guarantee of every active service.")

if __name__ == "__main__":
    main()
