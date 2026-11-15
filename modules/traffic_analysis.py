"""Simple analysis helpers for the included historical Pune traffic counts."""
from pathlib import Path
import pandas as pd

VEHICLE_COLUMNS = ["car_volume", "motorbike_volume", "bus_volume", "truck_volume"]


def load_traffic_data(file_path):
    """Load and validate the processed traffic CSV shipped with the project."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Traffic dataset not found: {path}")
    data = pd.read_csv(path)
    required = {"Junction", "Camera", "Recording_Day", "Minute", "Total_Vehicles", *VEHICLE_COLUMNS}
    missing = required.difference(data.columns)
    if missing:
        raise ValueError("Traffic dataset is missing columns: " + ", ".join(sorted(missing)))
    for column in VEHICLE_COLUMNS + ["Total_Vehicles"]:
        data[column] = pd.to_numeric(data[column], errors="coerce").fillna(0)
    data["Hour"] = pd.to_timedelta(data["Minute"], errors="coerce").dt.components.hours
    data = data.dropna(subset=["Hour"]).copy()
    data["Hour"] = data["Hour"].astype(int)
    return data


def traffic_summary(data):
    """Return transparent summary values for the selected observations."""
    if data.empty:
        return {"vehicles": 0, "junctions": 0, "cameras": 0, "peak_hour": None}
    hourly = data.groupby("Hour")["Total_Vehicles"].sum()
    return {
        "vehicles": int(data["Total_Vehicles"].sum()),
        "junctions": int(data["Junction"].nunique()),
        "cameras": int(data["Camera"].nunique()),
        "peak_hour": int(hourly.idxmax()),
    }


def hourly_traffic(data):
    return data.groupby("Hour", as_index=False)["Total_Vehicles"].sum().sort_values("Hour")


def vehicle_distribution(data):
    return data[VEHICLE_COLUMNS].sum().rename({
        "car_volume": "Cars", "motorbike_volume": "Motorbikes",
        "bus_volume": "Buses", "truck_volume": "Trucks"
    }).sort_values(ascending=False)
