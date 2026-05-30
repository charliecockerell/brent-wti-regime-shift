# data/

Raw EIA pulls and cleaned series. Raw and processed CSVs are gitignored — `make data` reproduces them.

## Sources

| Series | Code | EIA endpoint | Description |
|--------|------|--------------|-------------|
| Brent crude spot | `RBRTE` | `petroleum/pri/spt/data/?api_key=...&series_id=RBRTE` | Europe Brent spot FOB ($/bbl), daily |
| WTI Cushing spot | `RWTC` | `petroleum/pri/spt/data/?api_key=...&series_id=RWTC` | Cushing OK WTI spot FOB ($/bbl), daily |

## Window

1987-05-20 → present (EIA RBRTE/RWTC inception is 1987, not 2000). Covers:
- Pre-shale baseline (~1987–2010)
- Post-shale regime (~2011+)
- Aramco drone attack (16 Sep 2019)
- Soleimani assassination (3 Jan 2020)
- Houthi Red Sea escalation (Jan 2024)
- **Operation Epic Fury / 2026 Iran war start (28 Feb 2026)**
- **Hormuz closure (4 Mar 2026)**

## Processed data layout

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
`processed/spread.csv`. The raw `raw/RWTC.csv` retains the true value.

## Reproducibility

```bash
export EIA_API_KEY=...      # free registration at eia.gov/opendata
make data
```
