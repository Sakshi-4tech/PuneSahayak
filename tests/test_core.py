"""Basic checks for the route-planning helpers. Run: pytest -q"""
from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bus_modules.route_stats import haversine, overview_table
from bus_modules.scoring import to_score, add_convenience_score
from bus_modules.journey import hms_to_sec, sec_to_hm
from bus_modules.metro import load_metro, metro_options
from bus_modules.data_loader import load_gtfs
from bus_modules.places import resolve_place


def test_haversine_same_point_is_zero():
    assert haversine(18.5, 73.8, 18.5, 73.8) == 0


def test_haversine_known_distance():
    assert 110 < haversine(18.0, 73.8, 19.0, 73.8) < 112


def test_time_conversion_including_after_midnight():
    assert hms_to_sec("08:30:00") == 30600
    assert hms_to_sec("25:00:00") == 90000
    assert sec_to_hm(30600) == "08:30"


def test_score_between_zero_and_100():
    df = pd.DataFrame({"route_name": ["a", "b", "c"], "stops_between": [5, 10, 20],
                       "distance_km": [3.0, 6.0, 9.0], "trips": [40, 20, 5]})
    scored = add_convenience_score(df)
    assert scored["convenience_score"].between(0, 100).all()
    assert scored.iloc[0]["route_name"] == "a"


def test_equal_values_get_equal_score():
    assert (to_score(pd.Series([4, 4, 4]), higher_is_better=True) == 100).all()


def test_metro_interchange_suggestion():
    metro = load_metro(ROOT / "data" / "gtfs" / "metro_stations.csv")
    options = metro_options("Vanaz", "Swargate", metro)
    assert options and "District Court" in options[0]["text"]


def test_overview_counts_one_direction_only():
    routes = pd.DataFrame({"route_id": ["1"], "route_short_name": ["1"], "route_long_name": ["A - B"]})
    trips = pd.DataFrame({"route_id": ["1", "1"], "trip_id": ["t0", "t1"], "direction_id": [0, 1]})
    rows = pd.DataFrame({"route_id": ["1"] * 5, "direction_id": [0, 0, 0, 1, 1],
                         "stop_sequence": [1, 2, 3, 1, 2], "cum_km": [0, 1, 2, 0, 1.5]})
    result = overview_table({"routes": routes, "trips": trips}, rows)
    assert result.iloc[0]["n_stops"] == 3
    assert result.iloc[0]["length_km"] == 2


def test_real_data_load_and_place_match():
    data = load_gtfs(ROOT / "data" / "gtfs")
    assert len(data["routes"]) == 315
    assert resolve_place("Katraj", data["stops"])


def test_real_data_has_direct_katraj_to_hadapsar_route():
    from bus_modules.route_stats import build_route_stops
    from bus_modules.journey import build_network, plan_journeys
    data = load_gtfs(ROOT / "data" / "gtfs")
    route_stops = build_route_stops(data)
    network = build_network(data, route_stops)
    from_ids = resolve_place("Katraj", data["stops"])
    to_ids = resolve_place("Hadapsar Gadital", data["stops"])
    plans = plan_journeys(network, from_ids, to_ids, 9 * 3600)
    assert plans
    assert plans[0]["changes"] == 0


def test_comparison_includes_auto_and_peak_only_affects_road_modes():
    from modules.expense_calculator import calculate_comparison
    normal = calculate_comparison(10, 20, peak_hours=False)
    peak = calculate_comparison(10, 20, peak_hours=True)
    normal = normal.set_index("Transport Mode")
    peak = peak.set_index("Transport Mode")
    assert {"Bus", "Auto", "Metro", "Two-wheeler", "Car"}.issubset(normal.index)
    assert peak.loc["Bus", "Daily Travel Time (min)"] > normal.loc["Bus", "Daily Travel Time (min)"]
    assert peak.loc["Auto", "Daily Travel Time (min)"] > normal.loc["Auto", "Daily Travel Time (min)"]
    assert peak.loc["Metro", "Daily Travel Time (min)"] == normal.loc["Metro", "Daily Travel Time (min)"]


def test_metro_directory_contains_official_corridor_listing_records():
    metro = load_metro(ROOT / "data" / "gtfs" / "metro_stations.csv")
    assert len(metro) == 32
    assert set(metro["line"]) == {"Purple", "Aqua"}
    assert (metro["station"] == "District Court (Civil Court)").sum() == 2


def test_included_bus_stop_and_supplemental_route_data_counts():
    data = load_gtfs(ROOT / "data" / "gtfs")
    assert len(data["stops"]) == 6745
    supplemental = pd.read_csv(ROOT / "data" / "routes.csv")
    assert len(supplemental) == 1030


def test_traffic_dataset_load_and_hourly_summary():
    from modules.traffic_analysis import load_traffic_data, traffic_summary, hourly_traffic
    traffic = load_traffic_data(ROOT / "data" / "processed_traffic.csv")
    assert len(traffic) == 11592
    assert traffic["Hour"].between(0, 23).all()
    summary = traffic_summary(traffic[traffic["Camera"] != "a3"])
    assert summary["vehicles"] > 0
    assert summary["junctions"] == 3
    assert summary["peak_hour"] is not None
    assert not hourly_traffic(traffic).empty


def test_traffic_distribution_uses_all_four_vehicle_types():
    from modules.traffic_analysis import load_traffic_data, vehicle_distribution
    traffic = load_traffic_data(ROOT / "data" / "processed_traffic.csv")
    result = vehicle_distribution(traffic)
    assert set(result.index) == {"Cars", "Motorbikes", "Buses", "Trucks"}
    assert (result >= 0).all()
