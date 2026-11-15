# Data Sources & Attribution

| Data | Included file(s) | Source / attribution | Use in PuneSahayak |
|---|---|---|---|
| PMPML GTFS snapshot | `data/gtfs/routes.txt`, `trips.txt`, `stops.txt`, `stop_times.txt` | Community-maintained [croyla/pmpml-gtfs](https://github.com/croyla/pmpml-gtfs), described as MIT-0 in its repository | Bus route directory, stop directory and schedule-derived route search |
| PMPML route list | `data/routes.csv` | [Pune Bus Stops and Routes — OpenCity](https://data.opencity.in/dataset/pune-bus-stops-and-routes) / Pune Municipal Corporation source catalogue | Supplemental route reference |
| Pune Metro corridor station names | `data/gtfs/metro_stations.csv` | [Official Pune Metro station directory](https://www.punemetrorail.org/know-your-metro-stations) and [route map](https://www.punemetrorail.org/route-map) | Station/corridor name reference only |
| Historical road traffic | `data/processed_traffic.csv` | Retained from the team's supplied GoPune project dataset | Historical camera-count visualisations and hourly aggregation via `modules/traffic_analysis.py` |
| Road distance | Runtime OSRM request in `modules/route_distance.py` | OpenStreetMap routing ecosystem via public OSRM demo endpoint | Approximate area-centre road distance when service is reachable |

## Important data qualifications
- The PMPML feed is a community snapshot, not a live PMPML API connection.
- The included feed has no `calendar.txt` or `calendar_dates.txt`; weekday/date validity cannot be confirmed.
- The stop directory displays all records in the included `stops.txt`; it does not prove that the snapshot contains every currently active PMPML stop.
- The Metro CSV is a corridor directory, not a Metro GTFS timetable. Some official route-map entries may represent depots or stations with changing operational status.
- Traffic observations are historical counts, not route speed or travel-time data. Camera `a3` has unusually high counts in this file; the dashboard excludes it by default but lets the user include it for inspection.
- Fares, speeds, mileage and fuel price in the comparison are explicitly labelled project assumptions/reference values.
