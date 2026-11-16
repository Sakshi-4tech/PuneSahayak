import requests
import streamlit as st

PUNE_AREAS = {
    "Aundh": (18.5600, 73.8077),
    "Baner": (18.5590, 73.7868),
    "Camp": (18.5130, 73.8790),
    "Chinchwad": (18.6298, 73.7997),
    "Deccan": (18.5165, 73.8410),
    "F.C. Road": (18.5236, 73.8417),
    "Hadapsar": (18.5089, 73.9260),
    "Hinjawadi": (18.5912, 73.7389),
    "Kharadi": (18.5515, 73.9348),
    "Kondhwa": (18.4635, 73.8710),
    "Kothrud": (18.5074, 73.8077),
    "Katraj": (18.4529, 73.8670),
    "Lohegaon": (18.5990, 73.9160),
    "Magarpatta": (18.5158, 73.9270),
    "Pimpri": (18.6298, 73.7997),
    "Pimple Saudagar": (18.5980, 73.7970),
    "Pune Station": (18.5289, 73.8744),
    "Shivajinagar": (18.5308, 73.8475),
    "Swargate": (18.5018, 73.8636),
    "Viman Nagar": (18.5679, 73.9143),
    "Wakad": (18.5996, 73.7625),
    "Yerawada": (18.5525, 73.8780),
}


@st.cache_data(ttl=3600)
def get_road_distance_between(source_coords, destination_coords):
    """Get driving distance in km from OSRM using (latitude, longitude)."""

    lat1, lon1 = map(float, source_coords)
    lat2, lon2 = map(float, destination_coords)

    if (lat1, lon1) == (lat2, lon2):
        return 0.0

    url = (
        "https://router.project-osrm.org/route/v1/driving/"
        f"{lon1},{lat1};{lon2},{lat2}"
        "?overview=false"
    )

    response = requests.get(url, timeout=15)
    response.raise_for_status()

    data = response.json()

    if data.get("code") != "Ok" or not data.get("routes"):
        raise ValueError("Could not calculate this road route.")

    return round(data["routes"][0]["distance"] / 1000, 2)
