# data/

Raw EIA pulls and cleaned series. Raw and processed CSVs are gitignored — `make data` reproduces them.

## Sources

| Series | Code | EIA endpoint | Description |
|--------|------|--------------|-------------|
| Brent crude spot | `RBRTE` | `petroleum/pri/spt/data/?api_key=...&series_id=RBRTE` | Europe Brent spot FOB ($/bbl), daily |
| WTI Cushing spot | `RWTC` | `petroleum/pri/spt/data/?api_key=...&series_id=RWTC` | Cushing OK WTI spot FOB ($/bbl), daily |

Cross-check (not used in headline analysis):
- Yahoo Finance `BZ=F` (Brent front-month future)
- Yahoo Finance `CL=F` (WTI front-month future)

## Window

1987-05-20 → present (EIA RBRTE/RWTC inception is 1987, not 2000). Covers:
- Pre-shale baseline (~1987–2010)
- Post-shale regime (~2011+)
- Aramco drone attack (16 Sep 2019)
- Soleimani assassination (3 Jan 2020)
- Houthi Red Sea escalation (Jan 2024)
- **Operation Epic Fury / 2026 Iran war start (28 Feb 2026)**
- **Hormuz closure (4 Mar 2026)**
- US aerial campaign to reopen (19 Mar 2026)
- US counter-blockade (13 Apr 2026)

## Schema (cleaned)

`data/processed/spread.csv`

| Column | Type | Notes |
|--------|------|-------|
| `date` | ISO date | Trading day |
| `brent` | float | Brent spot close ($/bbl) |
| `wti` | float | WTI spot close ($/bbl) |
| `log_brent` | float | `log(brent)` |
| `log_wti` | float | `log(wti)` |
| `spread` | float | `brent - wti` |
| `log_spread` | float | `log_brent - log_wti` |

## Known data anomaly — negative WTI (20 Apr 2020)

On 20 Apr 2020, WTI spot (RWTC) settled at **−$36.98** during the COVID-19
demand collapse and Cushing storage saturation — a genuine historic print,
not a data error. Because `log(price)` is undefined for non-positive values
and the cointegration analysis runs on log levels, `build_spread` in
`scripts/pull_eia.py` **drops this single row** when constructing
`processed/spread.csv`. The raw `raw/RWTC.csv` retains the true value. This is
the only excluded observation; it is flagged in the paper's Limitations.

## Roll convention

EIA spot series are continuous and do not require roll adjustment. If the analysis is later extended to futures (`BZ=F`/`CL=F`), document back-adjustment convention here.

## Reproducibility

```bash
export EIA_API_KEY=...      # free registration at eia.gov/opendata
make data
```
