# PuneSahayak fare data

## PMPML bus
`pmpml_fare_stages.csv` stores the revised 11-stage adult fare schedule reported as approved by PMPML/RTA and effective 1 June 2025. The planner estimates the one-way stage from its road-distance estimate, then calculates round-trip and monthly totals. This is a route-distance proxy, not an exact fare for the actual bus path.

The unified PMPML daily pass is ₹70 and the monthly pass is ₹1,500. The user must select a pass they actually hold; the app never applies one by default. No blanket college-student discount is assumed. School-specific subsidy schemes have separate grade/school/locality eligibility and are not treated as a universal student concession.

## Maha Metro
`metro_fares_mahametro.csv` contains directional station-pair fares transcribed from station tables that attribute the values to Maha Metro's published fare chart image (checked 11 November 2026). The bundled lookup currently covers 12 origin stations and the matching destinations listed in the CSV. The app uses only exact directional pairs present in the file. It does not reverse a fare automatically because the source notes some directional differences; chart entries flagged as unconfirmed are excluded. Unsupported pairs are omitted from the cost ranking rather than guessed. Pink Line / PITCMRL is not included in this dataset; it is a separate operator with separate ticketing and its own fare chart.

Discount choices are opt-in: One Pune Vidyarthi Pass (30% every day), One Pune NCMC card (10% weekdays or 30% weekends). The user must select the applicable card/pass. Discounts are not stacked.

## Personal vehicles and auto
Fuel reference is ₹111.90/L for Pune on 16 November 2026 (reference only; petrol prices can change). Two-wheeler 40 km/L and car 15 km/L are prototype mileage assumptions, not vehicle facts. Auto uses the indicative Pune tariff formula (₹30 first 1.5 km + ₹20 per additional km); actual meter and current tariff card prevail.

## Important limitations
- PMPML GTFS supplies routes/stops/times, not an official fare feed (`fare_attributes.txt` is not included).
- Bus stage is estimated from road distance between selected places, not the exact distance along the bus route.
- Metro fare matrix coverage is limited to the bundled directional entries. Missing entries are not fabricated.
- Fare values and eligibility can change; confirm with operators before purchase.
