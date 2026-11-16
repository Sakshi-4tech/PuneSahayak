"""PuneSahayak fare lookups. Missing source data is never guessed."""
from pathlib import Path
import math
import pandas as pd
from functools import lru_cache

ROOT = Path(__file__).resolve().parents[1]
FARE_DIR = ROOT / "data" / "fares"

# PMPML revised 11-stage adult fare table, effective 1 June 2025.
PMPML_STAGES = [
    (5, 10), (10, 20), (15, 30), (20, 40), (25, 50), (30, 60),
    (40, 70), (50, 80), (60, 90), (70, 100), (80, 120),
]
PMPML_DAILY_PASS = 70.0
PMPML_MONTHLY_PASS = 1500.0

def pmpml_one_way_fare(distance_km):
    """Return published stage fare for estimated one-way distance; None beyond 80 km."""
    try:
        distance = float(distance_km)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(distance) or distance < 0 or distance > 80:
        return None
    distance = max(distance, 0.01)
    for upper_km, fare in PMPML_STAGES:
        if distance <= upper_km:
            return float(fare)
    return None

@lru_cache(maxsize=1)
def _metro_fare_table():
    path = FARE_DIR / "metro_fares_mahametro.csv"
    if not path.exists():
        return pd.DataFrame(columns=["from_station", "to_station", "one_way_fare_inr", "status"])
    df = pd.read_csv(path)
    df["from_station"] = df["from_station"].astype(str).str.casefold().str.strip()
    df["to_station"] = df["to_station"].astype(str).str.casefold().str.strip()
    return df

ALIASES = {
    "district court (civil court)": "district court", "civil court": "district court",
    "bhosari [nashik phata]": "nashik phata (bhosari)", "nashik phata": "nashik phata (bhosari)",
    "s.n.d.t college": "s. n. d. t. college", "s.n.d.t. college": "s. n. d. t. college",
    "pune rly. station": "pune railway station", "pune station": "pune railway station",
    "yerawada": "yerwada", "mandai": "mahatma phule mandai",
}

def _normalise_station(name):
    key = str(name or "").casefold().strip()
    return ALIASES.get(key, key)

def metro_one_way_fare(from_station, to_station):
    """Exact directional Maha Metro fare; returns None if pair isn't in bundled chart data."""
    origin, destination = _normalise_station(from_station), _normalise_station(to_station)
    if not origin or not destination or origin == destination:
        return None
    table = _metro_fare_table()
    hit = table[(table.from_station == origin) & (table.to_station == destination)]
    if hit.empty:
        return None
    row = hit.iloc[0]
    if row.get("status") != "published_chart_transcription":
        return None
    return float(row.one_way_fare_inr)

def metro_discount_rate(choice):
    return {
        "No pass / full fare": 0.0,
        "One Pune Vidyarthi Pass (30% every day)": 0.30,
        "One Pune NCMC card (10% weekdays)": 0.10,
        "One Pune NCMC card (30% weekends)": 0.30,
    }.get(choice, 0.0)
