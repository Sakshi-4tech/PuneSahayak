# PuneSahayak — Smart Pune Commute & Budget Dashboard

**Your city. Your commute. Your smarter choice.**

PuneSahayak is a Python + Streamlit student project that helps Pune commuters compare estimated travel cost and time, find PMPML and Pune Metro journey options, explore historical Pune traffic counts, and keep a simple local record of monthly commute spending.

## 1. Run the project on Windows

1. Download and extract the ZIP file.
2. Install **Python 3.10 or newer**. During installation, enable **Add Python to PATH**.
3. Open the extracted `PuneSahayak` folder.
4. Double-click `START_PUNE_SAHAYAK.bat`.
5. Wait while the required Python packages install. The dashboard should open in your browser.

If Windows blocks the script, open PowerShell in the project folder and run:

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

To stop the dashboard, return to the terminal and press `Ctrl + C`.

## 2. Main screens

| Screen | Purpose |
|---|---|
| Plan my journey | Enter origin, destination, travel days and budget; compare cheapest, fastest and balanced transport choices |
| PMPML bus journeys | Search direct and one-change bus journeys from the supplied GTFS snapshot, directly inside the journey results |
| Pune Metro journeys | Choose boarding and destination stations and see the same-corridor or interchange station sequence |
| Traffic insights | Explore historical camera counts by junction, hour and vehicle type; observations are not live congestion data |
| My commute budget | Record travel expenses, see monthly spend and export the history; no account or sign-up is required |

The navigation is intentionally short. Traffic insights are provided as a separate historical-data view so users do not confuse camera counts with live route conditions. The complete bus stop and route data remains included in the project files for the team to audit and demonstrate during the viva.

## 3. Data included

The included PMPML GTFS snapshot contains:

- **315 route records** (`routes.txt`)
- **6,745 stop records** (`stops.txt`)
- **10,128 trip records** (`trips.txt`)
- **429,302 stop-time records** (`stop_times.txt`)
- **1,030 supplemental route-catalogue rows** (`data/routes.csv`, separate from the GTFS route table)
- **32 Metro station-corridor records** in the directory CSV (including interchange references and depot entries shown by the official corridor listings)

These are counts of the files shipped in this ZIP. They are **not a guarantee that every currently operating PMPML route or stop is present**. The app displays all rows in the supplied stop file and allows the user to search/download them. See `DATA_SOURCES.md` and `data/gtfs/SOURCE_NOTES.txt` for provenance and qualifications.

## 4. Project structure

```text
PuneSahayak/
├── app.py                 # Main commuter-facing dashboard
├── START_PUNE_SAHAYAK.bat
├── run.sh
├── requirements.txt
├── modules/
│   ├── expense_calculator.py
│   ├── recommendation.py
│   ├── route_distance.py
│   ├── traffic_analysis.py
│   └── traffic_processor.py
├── bus_modules/
│   ├── data_loader.py
│   ├── route_stats.py
│   ├── journey.py
│   ├── places.py
│   ├── metro.py
│   └── scoring.py
├── data/
│   ├── gtfs/                 # PMPML GTFS + Metro station directory
│   ├── processed_traffic.csv
│   ├── routes.csv
├── tools/data_audit.py
├── tests/
├── TEAM_OF_4.md
├── VIVA_GUIDE.md
├── DATA_SOURCES.md
├── COMPETITOR_ANALYSIS.md
├── ARCHITECTURE.md
├── TEST_REPORT.md
├── AI_USAGE.md
└── PRESENTATION_OUTLINE.md
```

## 5. Validation commands

Open PowerShell in the project folder, activate `.venv`, then run:

```powershell
python tools/data_audit.py
pytest -q
```

The test suite checks core distance calculations, journey time conversions, Metro interchange suggestions, sample PMPML journeys, commute-cost comparison behaviour and historical traffic analysis.

## 6. Important limitations — explain these in your viva

- **Not live tracking:** the PMPML feed is a community-maintained GTFS snapshot. The app does not receive live bus GPS positions.
- **No service calendar:** `calendar.txt` and `calendar_dates.txt` are absent from the included feed, so a timetable entry cannot be guaranteed for a specific date or weekday.
- **Estimated times:** source timetable values and stop-to-stop estimates are not real-time arrival predictions.
- **Search limits:** the bus planner checks direct journeys and up to one bus change; a missing result does not prove that no real-world connection exists.
- **Metro:** the included file is a station/corridor directory, not a Metro GTFS timetable. Verify operating status, hours and fares with Maha Metro.
- **Traffic:** the historical camera dataset covers three junctions and eight cameras in a limited set of recording windows. Camera `a3` has unusually high recorded counts and is excluded by default in the dashboard, with an option to include it. Vehicle counts are not speed data and are not used as route-specific live congestion.
- **Cost model:** fuel price, mileage, average speed and some fares are project assumptions/reference values. Confirm current fares with operators.
- **Road distance:** area-centre road routing is approximate. The public OSRM demo endpoint may be unavailable; a labelled fallback estimate is used in that case.

## 7. Team allocation and presentation

See `TEAM_OF_4.md` for a four-person work split, `VIVA_GUIDE.md` for likely viva questions and demo flow, `COMPETITOR_ANALYSIS.md` for existing-solution comparison, `ARCHITECTURE.md` for the system workflow and `TEST_REPORT.md` for verification status. Replace placeholders with your real team names and actual contributions; do not claim work that was not completed.

## 8. Credits

- PMPML GTFS snapshot: [croyla/pmpml-gtfs](https://github.com/croyla/pmpml-gtfs), with attribution and MIT-0 terms as stated by that repository.
- Supplemental PMPML bus-stop and route directory catalogue: [OpenCity / Pune Municipal Corporation](https://data.opencity.in/dataset/pune-bus-stops-and-routes).
- Pune Metro station/corridor names: [Official Pune Metro station directory](https://www.punemetrorail.org/know-your-metro-stations) and [official route map](https://www.punemetrorail.org/route-map).
- Historical traffic data and original GoPune analysis modules are retained from the team's supplied project archive. Keep upstream student-project attribution for adapted modules where applicable.


## Unified journey locations

The journey planner provides one searchable From/To catalogue containing Pune localities, key landmarks, PMPML GTFS bus stops, and Metro stations. Bus and Metro suggestions reuse those same selections. Distance and nearest-station values are estimates based on reference coordinates; the app does not provide live tracking or walking directions.


## Fare comparison
PuneSahayak estimates PMPML single-ticket fares from the published 11-stage distance schedule, supports opt-in PMPML daily/monthly passes, and uses a bundled directional Maha Metro station-pair fare table where available. Metro discounts are applied only when a user selects a valid One Pune card/pass. Unsupported fare pairs are excluded instead of guessed. See `data/fares/README.md` for source scope and limitations.
