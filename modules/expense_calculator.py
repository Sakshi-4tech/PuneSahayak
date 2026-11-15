import pandas as pd


def calculate_comparison(
    distance_km,
    commuting_days,
    fuel_price=111.90,
    bus_fare=20,
    metro_fare=25,
    peak_hours=False
):
    """Estimate daily and monthly travel cost/time for common commute modes.

    All fares and speeds are assumptions or estimates, not live quotes.
    Auto fare uses the Pune tariff formula listed in the project README.
    """
    # Estimated average speeds in km/hour.
    speeds = {
        "Bus": 20,
        "Auto": 22,
        "Metro": 35,
        "Two-wheeler": 30,
        "Car": 25
    }

    # Vehicle mileage in km/litre.
    mileage = {
        "Two-wheeler": 40,
        "Car": 15
    }

    # The peak-hour factor applies only to road-based modes.
    road_time_factor = 1.35 if peak_hours else 1.0

    # Pune auto estimate: Rs 30 for the first 1.5 km, then Rs 20/km.
    auto_one_way = 30 + max(0, distance_km - 1.5) * 20

    # Daily costs include the outward and return journey.
    daily_costs = {
        "Bus": bus_fare * 2,
        "Auto": round(auto_one_way) * 2,
        "Metro": metro_fare * 2,
        "Two-wheeler": (distance_km * 2 / mileage["Two-wheeler"]) * fuel_price,
        "Car": (distance_km * 2 / mileage["Car"]) * fuel_price
    }

    results = []
    for mode, cost in daily_costs.items():
        # Metro is not affected by road traffic in this simplified model.
        time_factor = 1.0 if mode == "Metro" else road_time_factor
        travel_time = (distance_km * 2 / speeds[mode]) * 60 * time_factor
        results.append({
            "Transport Mode": mode,
            "Daily Cost (₹)": round(cost, 2),
            "Monthly Cost (₹)": round(cost * commuting_days, 2),
            "Daily Travel Time (min)": round(travel_time, 1)
        })

    return pd.DataFrame(results).sort_values("Monthly Cost (₹)")
