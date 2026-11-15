
import requests
import streamlit as st

from modules.pune_locations import PUNE_AREAS



@st.cache_data(ttl=3600)
def get_road_distance_km(source_area, destination_area):
    if source_area == destination_area:
        return 0.0

    source = PUNE_AREAS[source_area]
    destination = PUNE_AREAS[destination_area]

    url = (
        f"https://router.project-osrm.org/route/v1/driving/"
        f"{source[1]},{source[0]};{destination[1]},{destination[0]}"
        f"?overview=false"
    )

    response = requests.get(url, timeout=15)
    response.raise_for_status()

    data = response.json()

    if data.get("code") != "Ok":
        raise ValueError("Could not calculate this route.")

    return round(data["routes"][0]["distance"] / 1000, 2)


@st.cache_data(ttl=3600)
def get_road_distance_between(source_coords, destination_coords):
    """Estimate road distance between (lat, lon) pairs using public OSRM."""
    source = (float(source_coords[0]), float(source_coords[1]))
    destination = (float(destination_coords[0]), float(destination_coords[1]))
    if source == destination:
        return 0.0
    url = (
        f"https://router.project-osrm.org/route/v1/driving/"
        f"{source[1]},{source[0]};{destination[1]},{destination[0]}?overview=false"
    )
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    data = response.json()
    if data.get("code") != "Ok" or not data.get("routes"):
        raise ValueError("Could not calculate this route.")
    return round(data["routes"][0]["distance"] / 1000, 2)
