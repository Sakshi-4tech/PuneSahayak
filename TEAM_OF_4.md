# PuneSahayak — Team Work Split (4 Members)

Use this as a practical work allocation. Each person should understand the whole product, but own one technical area deeply. Update names and actual contributions honestly before submission.

## Member 1 — Transport Data & Data Quality
- Own `data/gtfs/`, `data/routes.csv`, `data/processed_traffic.csv` and `tools/data_audit.py`.
- Explain the difference between routes, trips, stops and stop-times in GTFS.
- Validate row counts, missing coordinates, duplicate IDs, source notes and license attribution.
- Maintain the searchable stop directory and export tests.
- Viva focus: dataset provenance, data cleaning, completeness limitations and why calendar files matter.

## Member 2 — Journey Planning & Network Logic
- Own `bus_modules/` and the PMPML / Metro Network pages in `app.py`.
- Explain direct-route search, one-change search, stop matching, Haversine distance and timetable-derived arrival estimates.
- Test representative journeys such as Katraj → Hadapsar and Vanaz → Swargate.
- Record where the model cannot find a route; never claim that no real-world service exists based only on a failed dataset match.
- Viva focus: algorithm, route graph, transfer constraints, time complexity and limitations.

## Member 3 — Cost Model & Budget Studio
- Own `modules/expense_calculator.py`, `modules/recommendation.py` and the Budget Studio page.
- Explain fare assumptions, fuel reference, mileage, average speeds, monthly calculation and cost/time scoring.
- Test budget boundaries and compare Cheapest, Fastest and Balanced priorities.
- Validate expense logging, monthly projection and CSV export.
- Viva focus: formulas, normalisation, assumptions and how users can interpret the recommendation.

## Member 4 — UI, Integration & Quality Assurance
- Own the overall Streamlit experience, theme, navigation, Plotly charts, launcher and release packaging.
- Test all pages from a clean unzip on a second computer.
- Run `pytest -q` and `python tools/data_audit.py` before each release.
- Maintain README, screenshots, presentation flow and demo sequence.
- Viva focus: Python/Streamlit architecture, interaction design, integration, testing and user experience.

## Shared responsibilities
- All four members should run the app, complete one end-to-end journey test, review the assumptions and practise the demo.
- Use individual GitHub accounts and genuine commits/pull requests. Do not fabricate contribution history.
- Each member should be able to explain the problem statement, data sources, recommendation model and limitations.
