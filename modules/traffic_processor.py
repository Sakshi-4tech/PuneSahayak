
from pathlib import Path
import pandas as pd

VEHICLES = ["car", "motorbike", "bus", "truck"]


def process_traffic_file(file_path, cutoff_time=None):
    file_path = Path(file_path)

    df = pd.read_csv(file_path)

    df = df.dropna(subset=["Time", "Direction"]).copy()

    for col in VEHICLES:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=VEHICLES)

    # Keep the last observation for each timestamp and direction.
    df = (
        df.groupby(["Time", "Direction"], sort=False)
        .tail(1)
        .copy()
    )

    df["Time"] = pd.to_timedelta(df["Time"])

    df = df.sort_values(["Direction", "Time"]).reset_index(drop=True)

    # Calculate increments before applying any overlap cutoff.
    volume_columns = []

    for col in VEHICLES:
        volume_col = col + "_volume"
        volume_columns.append(volume_col)

        df[volume_col] = df.groupby("Direction")[col].diff()
        df[volume_col] = df[volume_col].fillna(df[col])

    if (df[volume_columns] < 0).any().any():
        raise ValueError(
            f"Negative derived counts found in {file_path.name}"
        )

    df["Total_Vehicles"] = df[volume_columns].sum(axis=1)

    # Remove overlapping timestamps only AFTER calculating increments.
    if cutoff_time is not None:
        cutoff = pd.to_timedelta(cutoff_time)
        df = df[df["Time"] > cutoff].copy()

    # Aggregate into one-minute intervals.
    df["Minute"] = df["Time"].dt.floor("min")

    minute_data = (
        df.groupby("Minute")[volume_columns + ["Total_Vehicles"]]
        .sum()
        .reset_index()
    )

    minute_data["Source_File"] = file_path.name
    minute_data["Camera"] = file_path.stem.split("_")[0]
    minute_data["Junction"] = file_path.parent.parent.name
    minute_data["Recording_Day"] = file_path.stem.split("_")[1]

    return minute_data
