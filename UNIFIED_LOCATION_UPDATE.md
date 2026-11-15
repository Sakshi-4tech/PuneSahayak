# Unified journey location update

## What changed

The main **Plan my journey** page now uses one searchable From/To catalogue containing:

- 22 Pune localities
- 3 key landmarks, including MIT-WPU, Pune Railway Station and Pune Airport
- 3,836 distinct PMPML stop names from the included GTFS feed
- 31 Metro station names

The catalogue is built from the local project data; it does not require a live location API.

## How it works

- Selecting a PMPML stop passes its associated GTFS stop IDs to the existing bus journey planner.
- Selecting a locality or landmark resolves it to matching/nearby GTFS stops.
- Selecting a Metro station uses nearby PMPML stops for bus suggestions.
- Metro suggestions reuse the same From/To selections and map them to a station in the included Metro directory.
- Road-distance estimates use the selected location coordinates. If the OSRM routing service is unavailable, the app falls back to an approximate straight-line estimate.

## Important limitations to explain in the viva

- The PMPML feed is a bundled schedule snapshot, not live bus tracking.
- Metro results are station-to-station corridor suggestions, not live train times or walking directions.
- Some locality and Metro reference coordinates are approximate. The distance shown is an estimate, not a guaranteed door-to-door route distance.
- The catalogue search is designed for typing a stop/place name rather than scrolling through every stop.
