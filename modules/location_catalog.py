"""Unified searchable location catalogue for PuneSahayak's journey planner."""
from __future__ import annotations

import pandas as pd

from modules.pune_locations import PUNE_AREAS

# Reference coordinates for Metro stations. Used only for broad route-distance
# estimates and nearest-station suggestions; they are not walking directions.
METRO_COORDS = {
    "PCMC": (18.6297, 73.7997),
    "Sant Tukaram Nagar": (18.6184, 73.8134),
    "Bhosari [Nashik Phata]": (18.6139, 73.8216),
    "Kasarwadi": (18.6054, 73.8218),
    "Phugewadi": (18.5947, 73.8270),
    "Dapodi": (18.5808, 73.8337),
    "Bopodi": (18.5697, 73.8367),
    "Khadki": (18.5620, 73.8392),
    "Range Hill Depot": (18.5505, 73.8402),
    "Range Hill": (18.5414, 73.8414),
    "Shivaji Nagar": (18.5306, 73.8478),
    "District Court (Civil Court)": (18.5286, 73.8555),
    "Kasba Peth": (18.5231, 73.8598),
    "Mahatma Phule Mandai": (18.5149, 73.8590),
    "Swargate": (18.5017, 73.8635),
    "Hill View Park Car Depot": (18.4930, 73.8120),
    "Vanaz": (18.5078, 73.8073),
    "Anand Nagar": (18.4998, 73.8190),
    "Paud Phata": (18.5096, 73.8266),
    "S.N.D.T College": (18.5158, 73.8335),
    "Garware College": (18.5186, 73.8370),
    "Deccan Gymkhana": (18.5161, 73.8396),
    "Chhatrapati Sambhaji Udyan": (18.5206, 73.8416),
    "PMC": (18.5193, 73.8541),
    "R.T.O Pune": (18.5259, 73.8664),
    "Pune Rly. Station": (18.5286, 73.8744),
    "Ruby Hall Clinic": (18.5331, 73.8773),
    "Bund Garden": (18.5390, 73.8810),
    "Yerawada": (18.5482, 73.8840),
    "Kalyani Nagar": (18.5485, 73.9025),
    "Ramwadi": (18.5672, 73.9155),
}

LANDMARKS = {
    "MIT-WPU": (18.5182, 73.8153),
    "Pune Railway Station": (18.5289, 73.8744),
    "Pune Airport (Lohegaon)": (18.5793, 73.9089),
}


def _label(kind: str, name: str) -> str:
    return f"{kind} · {name}"


def build_location_catalog(stops: pd.DataFrame, metro: pd.DataFrame) -> dict:
    """Return display-label -> metadata for localities, landmarks, stops, stations."""
    catalog = {}
    for name, coords in PUNE_AREAS.items():
        catalog[_label("Area", name)] = {
            "name": name, "kind": "area", "coords": coords, "stop_ids": (), "metro_station": None
        }
    for name, coords in LANDMARKS.items():
        catalog[_label("Landmark", name)] = {
            "name": name, "kind": "landmark", "coords": coords, "stop_ids": (), "metro_station": None
        }

    # Group duplicate stop names so a selected name resolves to all matching
    # GTFS stop IDs while retaining a representative coordinate for distance.
    valid = stops.dropna(subset=["stop_name", "stop_lat", "stop_lon"]).copy()
    valid["stop_name"] = valid["stop_name"].astype(str).str.strip()
    valid["stop_lat"] = pd.to_numeric(valid["stop_lat"], errors="coerce")
    valid["stop_lon"] = pd.to_numeric(valid["stop_lon"], errors="coerce")
    valid = valid.dropna(subset=["stop_lat", "stop_lon"])
    for name, group in valid.groupby("stop_name", sort=True):
        if not name:
            continue
        catalog[_label("Bus stop", name)] = {
            "name": name, "kind": "bus_stop",
            "coords": (float(group.stop_lat.mean()), float(group.stop_lon.mean())),
            "stop_ids": tuple(group.stop_id.unique()), "metro_station": None,
        }

    if not metro.empty:
        for _, row in metro.drop_duplicates("station").iterrows():
            name = str(row["station"]).strip()
            if not name:
                continue
            coords = METRO_COORDS.get(name)
            # Prefer a matching GTFS stop centroid if the feed contains one.
            key = name.casefold()
            matches = valid[valid.stop_name.str.casefold().str.contains(key, regex=False)]
            if not matches.empty:
                coords = (float(matches.stop_lat.mean()), float(matches.stop_lon.mean()))
            if coords is None:
                continue
            catalog[_label("Metro", name)] = {
                "name": name, "kind": "metro", "coords": coords,
                "stop_ids": (), "metro_station": name,
            }
    return catalog


def bus_stop_ids(location: dict, stops: pd.DataFrame) -> set:
    """Resolve a selected catalogue item to exact or nearby PMPML stop IDs."""
    if location.get("kind") == "bus_stop":
        return set(location.get("stop_ids", ()))
    if location.get("kind") == "metro":
        from bus_modules.route_stats import haversine
        lat, lon = location["coords"]
        nearby = stops[stops.apply(
            lambda row: haversine(lat, lon, row["stop_lat"], row["stop_lon"]) <= 0.65,
            axis=1,
        )]
        return set(nearby["stop_id"])
    from bus_modules.places import resolve_place
    resolved = resolve_place(location["name"], stops)
    if resolved:
        return resolved
    # A landmark without a matching stop name can still connect to nearby stops.
    if location.get("kind") == "landmark":
        from bus_modules.route_stats import haversine
        lat, lon = location["coords"]
        nearby = stops[stops.apply(
            lambda row: haversine(lat, lon, row["stop_lat"], row["stop_lon"]) <= 1.25,
            axis=1,
        )]
        return set(nearby["stop_id"])
    return set()


def nearest_metro_station(location: dict, metro: pd.DataFrame) -> str | None:
    """Map a selected location to an exact or nearest station in the directory."""
    if location.get("kind") == "metro":
        return location.get("metro_station")
    name = str(location.get("name", "")).casefold()
    hints = {
        "kothrud": "Vanaz", "mit-wpu": "Vanaz", "pimpri": "PCMC",
        "chinchwad": "PCMC", "swargate": "Swargate", "deccan": "Deccan Gymkhana",
        "f.c. road": "Garware College", "shivajinagar": "Shivaji Nagar",
        "pune station": "Pune Rly. Station", "pune railway station": "Pune Rly. Station",
        "yerawada": "Yerawada", "viman nagar": "Ramwadi", "katraj": "Swargate",
        "aundh": "Range Hill", "baner": "Vanaz", "camp": "Ruby Hall Clinic",
        "hadapsar": "Ramwadi", "kharadi": "Ramwadi", "hinjawadi": "PCMC",
        "hinjewadi": "PCMC", "wakad": "PCMC", "magarpatta": "Ramwadi",
        "kondhwa": "Swargate", "lohegaon": "Ramwadi", "pimple saudagar": "PCMC",
        "pune airport (lohegaon)": "Ramwadi",
    }
    if name in hints:
        return hints[name]
    coords = location.get("coords")
    if coords is None or metro.empty:
        return None
    # Coordinates are approximate station references, not pedestrian routing.
    from bus_modules.route_stats import haversine
    choices = []
    for station, station_coords in METRO_COORDS.items():
        if (metro.station == station).any():
            choices.append((haversine(coords[0], coords[1], station_coords[0], station_coords[1]), station))
    return min(choices)[1] if choices else None
