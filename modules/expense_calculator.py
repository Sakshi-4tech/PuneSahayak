import pandas as pd
from modules.fare_engine import pmpml_one_way_fare, PMPML_DAILY_PASS, PMPML_MONTHLY_PASS

def calculate_comparison(
    distance_km, commuting_days, fuel_price=111.90, peak_hours=False,
    bus_one_way_fare=None, bus_pass_type="No pass",
    metro_one_way_fare=None, metro_discount=0.0,
):
    """Estimate round-trip daily and monthly costs. Unavailable fares are omitted, never guessed."""
    days = max(1, int(commuting_days))
    distance = max(0.0, float(distance_km))
    speeds = {"Bus": 20, "Auto": 22, "Metro": 35, "Two-wheeler": 30, "Car": 25}
    mileage = {"Two-wheeler": 40, "Car": 15}
    road_factor = 1.35 if peak_hours else 1.0
    costs = {}
    basis = {}

    # PMPML: ticket stage fare OR the pass the commuter says they already hold.
    if bus_pass_type == "Daily pass (₹70/day)":
        costs["Bus"] = (PMPML_DAILY_PASS, PMPML_DAILY_PASS * days)
        basis["Bus"] = "Existing PMPML daily pass · ₹70 per travel day"
    elif bus_pass_type == "Monthly pass (₹1,500/month)":
        costs["Bus"] = (PMPML_MONTHLY_PASS / days, PMPML_MONTHLY_PASS)
        basis["Bus"] = "Existing PMPML monthly pass · ₹1,500/month"
    elif bus_one_way_fare is not None:
        daily = float(bus_one_way_fare) * 2
        costs["Bus"] = (daily, daily * days)
        basis["Bus"] = f"PMPML stage fare · ₹{float(bus_one_way_fare):.0f} one way"

    if metro_one_way_fare is not None:
        discounted = float(metro_one_way_fare) * (1 - max(0.0, min(0.30, float(metro_discount))))
        daily = discounted * 2
        costs["Metro"] = (daily, daily * days)
        basis["Metro"] = f"Station-pair chart fare · {metro_discount:.0%} eligible discount"

    # Indicative auto estimate: ₹30 first 1.5 km, then ₹20/km.
    auto_one_way = 30 + max(0, distance - 1.5) * 20
    costs["Auto"] = (round(auto_one_way) * 2, round(auto_one_way) * 2 * days)
    basis["Auto"] = "Indicative Pune meter tariff estimate"

    for mode, km_per_litre in mileage.items():
        daily = (distance * 2 / km_per_litre) * float(fuel_price)
        costs[mode] = (daily, daily * days)
        basis[mode] = f"Fuel estimate · ₹{float(fuel_price):.2f}/L × {km_per_litre} km/L reference mileage"

    rows = []
    for mode, (daily_cost, monthly_cost) in costs.items():
        factor = 1.0 if mode == "Metro" else road_factor
        travel_time = (distance * 2 / speeds[mode]) * 60 * factor
        rows.append({
            "Transport Mode": mode, "Daily Cost (₹)": round(daily_cost, 2),
            "Monthly Cost (₹)": round(monthly_cost, 2),
            "Daily Travel Time (min)": round(travel_time, 1),
            "Cost Basis": basis[mode],
        })
    return pd.DataFrame(rows).sort_values("Monthly Cost (₹)").reset_index(drop=True)
