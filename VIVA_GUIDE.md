# PuneSahayak — Viva Preparation

## 60-second project explanation
PuneSahayak is a Python-based Pune commute decision-support dashboard. It combines a PMPML bus-network directory, a schedule-based bus journey search, a Pune Metro station directory, estimated cost/time comparisons and a personal commute budget tracker. Its main value is that it makes the cost-versus-time trade-off visible and explains why an option is recommended.

## Architecture
- **Streamlit:** page navigation, user inputs, interactive tables and charts.
- **Pandas / NumPy:** loading, joining, filtering and analysing transport datasets.
- **Plotly:** interactive cost and historical traffic visualisations.
- **GTFS tables:** routes, trips, stops and stop_times.
- **Python modules:** bus route planning, distance calculations, fare/time estimates and recommendation scoring.
- **CSV persistence:** local commute expense history.

## Likely viva questions

### 1. What problem are you solving?
Daily commuters compare modes across separate sources. PuneSahayak puts transport options and estimated monthly affordability together so users can make a more informed choice.

### 2. What is GTFS?
General Transit Feed Specification is a common format for public-transport data. In this project, routes describe services, trips describe individual runs, stops describe boarding/alighting locations and stop_times describe the time at each stop.

### 3. How does the bus planner work?
It loads the GTFS tables, builds ordered route-stop sequences, matches selected places to stop IDs, checks direct journeys and then checks one-transfer journeys within a configured walking distance. It returns schedule-derived estimated steps.

### 4. Why are times called estimates?
The included source feed is community-maintained, stop times are not live vehicle observations, and service-calendar files are missing. A timetable row cannot guarantee that a bus is operating at the time selected.

### 5. How is distance calculated?
For route geometry between consecutive stop coordinates, the project uses the Haversine formula to estimate segment distance over the Earth's surface. Road-mode comparison uses an OpenStreetMap routing service when reachable; otherwise it uses a labelled fallback estimate.

### 6. How is the recommendation chosen?
Cheapest sorts estimated monthly cost, Fastest sorts estimated travel time, and Balanced combines normalised cost and time scores with equal weights. This is our transparent decision model, not an official operator score.

### 7. How is monthly expense calculated?
The estimated daily round-trip cost is multiplied by the user's commuting days per month. In Budget Studio, manually entered expense records are summed for the selected calendar month.

### 8. What is the limitation of the traffic data?
The historical data covers a limited set of camera junctions. Counts by vehicle type do not directly measure speed or route delay, so it is not used as live route-specific traffic.

### 9. Why not claim all PMPML stops?
The app includes every row in the supplied GTFS stops file and makes the complete-in-file directory searchable. A snapshot is not proof of current network completeness; the team documents provenance and validates against updated operator data before making a complete-network claim.

### 10. What makes the project different from Google Maps?
The differentiator is the student-oriented affordability layer: monthly commute budgeting, expense logging, mode-wise spending patterns and transparent cost/time recommendations. It is a prototype and does not claim to replace live navigation.

## Demo path
1. Open Overview and explain the project.
2. Journey Planner: choose Kothrud → Pimpri, set a budget and compare modes.
3. Search a PMPML journey and show boarding/alighting instructions.
4. PMPML Network: search for a stop and open Route Explorer.
5. Metro Network: show corridor station ordering.
6. Budget Studio: add an expense and show the monthly chart.
7. Traffic Insights: explain historical counts and their limitation.

## Before presenting
- Run `pytest -q`.
- Run `python tools/data_audit.py` and note the actual counts.
- Verify internet availability for OpenStreetMap road-distance requests.
- Confirm current PMPML and Metro fares/service status independently.
- Do not describe the project as live tracking, real-time congestion prediction or a complete official route planner.
