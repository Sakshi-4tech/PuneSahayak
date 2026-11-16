# Fare data integration notes — 16 November 2026

This patch replaces flat assumed bus/Metro fares with automatic PMPML distance-stage fare calculation and directional Maha Metro station-pair lookup. It adds explicit pass/card selectors; no concession is applied unless selected.

PMPML GTFS is not a fare dataset. The 2025 revised adult stage schedule and unified pass prices are included as a separate fare reference. The bus fare is estimated from the road-distance proxy, not an exact route-shape distance.

Metro station-pair coverage is limited to the included chart transcription. Unsupported station pairs are omitted from the comparison rather than assigned an invented fare. Pink Line / PITCMRL fares are not included because it is a separate operator and the current app's station network is Purple/Aqua.

Traffic Insights remains historical only; it is not labelled as live traffic.
