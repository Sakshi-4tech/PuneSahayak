# PuneSahayak — Presentation Notes (12 slides)

## Before presenting
- Replace `[Team Member 1–4]` with the actual names.
- On slide 11, replace the three labelled frames with fresh screenshots from the final local application run: Home, Journey Planner results, and Traffic Insights or Budget. Do not use old screenshots that show the previously reported date-field contrast issue.
- Confirm the app launches on the presentation laptop and use a fresh, non-personal test expense entry.

## Short speaker guide

1. **Title:** Introduce PuneSahayak as a Python + Streamlit decision-support prototype for Pune commuters.
2. **Problem:** Explain the everyday choice between travel time, cost and public-transport connections. Avoid unsupported city-wide statistics.
3. **Why Pune:** Explain that commuters use a mix of PMPML, Metro, auto and private vehicles; planning information and costs are spread across sources.
4. **Solution:** Show how journey comparison, dataset-based public transport options, historical traffic analysis and local expense tracking fit together.
5. **Objectives:** Explain that the project aims to support decisions, not replace official navigation or transport operators.
6. **MVP features:** Walk through the five implemented areas and explain that values are estimates where appropriate.
7. **Technology:** Python is the core logic; Pandas loads and analyses data; Streamlit provides UI; Plotly displays charts; pytest validates helper functions.
8. **Data:** Explain GTFS tables and counts. Note that calendar files are missing and the traffic file covers only a small historical sample.
9. **Architecture:** Follow the user input → data loading → Python calculations/search → recommendations/charts → local CSV flow.
10. **Competitors:** Acknowledge that Google Maps, Apli PMPML and Moovit already provide stronger live navigation features. Our focused student-project difference is transparent cost/time assumptions, monthly expense logging and explainable local data analysis.
11. **Demo:** Use the real app screenshots and live app. Demonstrate one journey, one bus search, one traffic filter and one budget entry.
12. **Limitations/conclusion:** Be honest about non-live data and explain the next steps: official calendar data, verified fare inputs and current service feeds.

## Demo script (about 2 minutes)
1. Home → Plan my journey.
2. Choose Kothrud → Pimpri, 22 travel days and a sample budget; run comparison.
3. Explain Cheapest, Fastest and Balanced, then open PMPML bus journeys and search a route.
4. Open Traffic insights; compare junctions and explain the camera `a3` outlier toggle.
5. Open My commute budget; add a small test entry, show the monthly total and CSV export. Delete the test entry afterwards.

## Sources linked from the slides
- PMPML GTFS snapshot: https://github.com/croyla/pmpml-gtfs
- Supplemental route catalogue: https://data.opencity.in/dataset/pune-bus-stops-and-routes
- Pune Metro station directory: https://www.punemetrorail.org/know-your-metro-stations
- Pune Metro route map: https://www.punemetrorail.org/route-map
- Google Maps directions: https://support.google.com/maps/answer/144339
- Apli PMPML: https://play.google.com/store/apps/details?id=in.chartr.pmpml
- Moovit: https://play.google.com/store/apps/details?id=com.tranzmate
