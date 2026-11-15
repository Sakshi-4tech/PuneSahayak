
def get_recommendations(df):
    """
    Compare transport options based on cost and travel time.
    Lower cost and lower travel time receive better scores.
    """

    result = df.copy()

    min_cost = result["Monthly Cost (₹)"].min()
    max_cost = result["Monthly Cost (₹)"].max()

    min_time = result["Daily Travel Time (min)"].min()
    max_time = result["Daily Travel Time (min)"].max()

    # Score: 100 means best, 0 means worst
    if max_cost == min_cost:
        result["Cost Score"] = 100
    else:
        result["Cost Score"] = (
            (max_cost - result["Monthly Cost (₹)"])
            / (max_cost - min_cost) * 100
        )

    if max_time == min_time:
        result["Time Score"] = 100
    else:
        result["Time Score"] = (
            (max_time - result["Daily Travel Time (min)"])
            / (max_time - min_time) * 100
        )

    # Equal importance to cost and time
    result["Balanced Score"] = (
        result["Cost Score"] + result["Time Score"]
    ) / 2

    cheapest = result.loc[
        result["Monthly Cost (₹)"].idxmin(), "Transport Mode"
    ]

    fastest = result.loc[
        result["Daily Travel Time (min)"].idxmin(), "Transport Mode"
    ]

    balanced = result.loc[
        result["Balanced Score"].idxmax(), "Transport Mode"
    ]

    return {
        "cheapest": cheapest,
        "fastest": fastest,
        "balanced": balanced,
        "details": result
    }
