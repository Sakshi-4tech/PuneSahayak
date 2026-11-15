# PuneSahayak — QA Report

**Review date:** 15 November 2026  
**Source package:** `PuneSahayak_Final(2).zip`  
**Updated scope:** Historical traffic insights added to the existing dashboard.

## Automated checks performed

| Check | Result |
|---|---|
| Python AST / syntax parse for all `.py` files | Passed |
| Unit and integration tests (`python -m pytest -q`) | 14 passed |
| GTFS row-count and ID audit (`python tools/data_audit.py`) | Passed |
| Routes | 315 rows; 315 unique route IDs |
| Trips | 10,128 rows; 10,128 unique trip IDs |
| Stops | 6,745 rows; 6,745 unique stop IDs; all have coordinates |
| Stop times | 429,302 rows |
| Supplemental route catalogue | 1,030 rows |
| Metro directory | 32 corridor records; 31 unique station names |
| Service calendar | Not present; documented as a limitation |
| Traffic dataset | 11,592 rows; 3 junctions; 8 cameras |

## Important uncompleted verification

The review container did not have Streamlit installed and could not reach the package index to install it. Therefore a browser launch, visual regression pass and end-to-end interaction test were **not performed in this environment**. Run the Windows launch and manual checklist in `README.md` on the target computer before presenting.

## Manual acceptance checklist for the target computer

- [ ] `START_PUNE_SAHAYAK.bat` launches the app.
- [ ] Home page and sidebar navigation load.
- [ ] Route comparison returns five transport modes.
- [ ] PMPML direct / one-change search returns dataset-backed results.
- [ ] Metro corridor suggestion displays the station sequence.
- [ ] Traffic Insights loads, junction filter works and `a3` toggle changes the sample.
- [ ] Budget expense can be saved, listed, exported and deleted.
- [ ] Date input and all form labels have readable contrast.
- [ ] No local expense file or secrets are unintentionally committed.
