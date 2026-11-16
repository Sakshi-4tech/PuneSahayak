# GoPune — quick teacher Q&A notes

Use these answers in your own words. Do not claim features that are not implemented.

## 1. What problem does GoPune solve?
It gives Pune commuters a simple way to compare estimated travel cost and time across common modes, and to find a direct PMPML bus or a bus journey with one change between supported areas.

## 2. What is GTFS?
GTFS means General Transit Feed Specification. It is a standard way of organising public-transport information into tables such as routes, trips, stops and stop times.

## 3. What data did we use?
The supplied community PMPML GTFS dataset contains 315 route records, 10,128 trips, 6,745 stops and 429,302 stop-time records. The project also has an existing historical traffic-count CSV and a manually compiled Metro station list.

## 4. What does each GTFS file mean?
- `routes.txt`: route IDs and route names.
- `trips.txt`: individual trips that belong to routes.
- `stops.txt`: stop names and latitude/longitude.
- `stop_times.txt`: the order and scheduled/estimated time at each stop for a trip.

## 5. How does the bus planner work?
First, pandas loads the four GTFS tables. We join trip and stop information to build an ordered list of stops for each route and direction. The selected area names are matched to stop names. Then the algorithm checks whether one route visits both areas in the correct order. If not, it looks for two routes whose transfer stops are within 300 metres. The app shows the bus numbers, boarding/alighting stops and estimated times.

## 6. What is the Haversine formula?
It estimates the straight-line distance between two points on Earth using their latitude and longitude. We use it for approximate distances between bus stops and for checking whether two transfer stops are close enough to walk between.

## 7. Why is a transfer limited to 300 metres?
It is a simple project rule so the planner only suggests transfers that are reasonably close to walk. The code assumes a walking speed of 4.5 km/h and adds a 3-minute transfer buffer. These are assumptions, not official PMPML rules.

## 8. Are bus arrival times live or exact?
No. They are estimates derived from the supplied GTFS data. The feed's README says travel times are estimates, and the supplied folder does not include `calendar.txt` or `calendar_dates.txt`. So the app cannot confirm service for a particular date or weekday, and it does not track live bus GPS.

## 9. How does Metro planning work?
The Metro helper uses a manually compiled station list for the Purple and Aqua lines. It checks whether the origin and destination match stations on the same line or can connect through District Court. It does not calculate live train times or fares.

## 10. How is traffic used?
The historical traffic file contains vehicle counts from only three junctions over a limited morning period. Vehicle counts are not the same as vehicle speed, and these records are not mapped to every route. So we do not pretend they provide live route-specific congestion. The commute comparison uses a clearly stated 1.35 peak-hour multiplier for road modes only. Metro is not affected by this road-traffic multiplier.

## 11. How are costs estimated?
The comparison uses project assumptions for bus and Metro fares, mileage for private vehicles and a fuel-price reference value. Auto fare is estimated using the Pune rate announced for 1 September 2026: ₹30 for the first 1.5 km and ₹20 per additional kilometre. The estimate does not model every meter rounding rule or night surcharge. These are comparison estimates, not guaranteed quotes.

## 12. Why is the project not the same as Google Maps?
GoPune is a small student prototype focused on transparent comparison assumptions and showing the bus number, boarding stop, alighting stop and a possible one-change journey. It is not a replacement for Google Maps or official transport apps, and it has fewer routes and features.

## 13. What are the main limitations?
- No live bus GPS.
- No GTFS service calendar in the supplied files.
- Only direct bus journeys and one bus change are searched.
- Place matching depends on stop names and a limited alias list.
- Metro times and fares are not integrated.
- Traffic counts cannot produce reliable route-specific travel times.
- Some costs and speeds are assumptions.

## 14. What can be improved next?
Add an updated official GTFS feed with service calendars, validate fares against official tariff data, add reliable Metro timetable data, improve place matching, and connect route-specific traffic/speed data if a trustworthy source becomes available.

## 15. What should we say about borrowed code/data?
The bus-planner modules were adapted from the supplied Pune CommuteWise student project, and the bus data is from the community `croyla/pmpml-gtfs` feed. We acknowledge both sources in the README and presentation. We should not claim that those original modules or datasets were created by our team.


### How are public-transport fares estimated?
PMPML fares use the revised 11-stage schedule (estimated from the selected road distance) or the daily/monthly pass the commuter explicitly selects. Metro fares use the bundled station-pair chart entries; eligible One Pune Vidyarthi/NCMC discounts are applied only when selected by the user. Missing Metro fare pairs are not guessed.
