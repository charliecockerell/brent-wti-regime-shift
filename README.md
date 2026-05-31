# brent-wti-regime-shift

**Status:** 🟢 In progress · target submission 23 June 2026 · hard deadline 23 July 2026
**Author:** Charlie Cockerell · Durham University · [LinkedIn / CV]
**Submission:** Onyx Research Competition 2026 — Technical Track

---

## Thesis

> The Brent–WTI spread is a stable cointegrating relationship in normal regimes but blows out sharply and transiently under Middle East supply shocks. This creates an exploitable mean-reversion trade on a defined timescale, with a long-term decay risk if the Hormuz transit-risk premium becomes structurally priced and the cointegrating vector permanently reprices.

**Prompt addressed:** *"Evaluate the short and long-term consequences of the recent US–Iran conflict on the oil market."*
- Short-term consequence → the mean-reversion trade, backtested on historical shocks (Aramco 2019, Soleimani 2020).
- Long-term consequence → the structural regime change observable in real-time after Operation Epic Fury (28 Feb 2026) and the Hormuz closure (4 Mar 2026).

---

## Headline numbers

> Placeholders — replaced as each phase completes.

| Metric | Value | Source |
|--------|-------|--------|
| Cointegration β (log-Brent on log-WTI) | 1.094 (95% CI [1.086, 1.101]) | `notebooks/01_cointegration.ipynb` |
| ECM half-life of mean reversion | 24.1 days | `notebooks/01_cointegration.ipynb` |
| Engle-Granger cointegration p-value | < 0.001 (Johansen rank 1) | `notebooks/01_cointegration.ipynb` |
| Peak spread-z [0,+20]: historical vs 2026 | ≤ 3.1σ (median 2.95) vs ≈ +12σ | `notebooks/02_event_study.ipynb` |
| Post-event vol ratio: historical vs 2026 | ~1.2× vs ~8.3× | `notebooks/02_event_study.ipynb` |
| 2026 renormalisation | not observed in-sample (data ends 2026-05-26) | `notebooks/02_event_study.ipynb` |
| OOS Sharpe (2019–2026), 63 trades, 83% hit | 1.02 (vs ~0.00 always-long) | `notebooks/03_backtest.ipynb` |
| Max drawdown, OOS (avg hold 9.4d) | −$26.0/bbl | `notebooks/03_backtest.ipynb` |
| Post-Feb-2026 rolling β vs pre-event | TBD | `notebooks/04_regime_drift.ipynb` |

---

## Method

1. **Data** — EIA daily series RBRTE (Brent) and RWTC (WTI), 1987–present (EIA series inception). Continuous spot series; roll convention and the single dropped observation (negative WTI, 20 Apr 2020) documented in `data/README.md`.
2. **Cointegration** — Engle-Granger two-step (ADF on log levels, OLS, ADF on residuals), cross-checked with Johansen. Error-correction model for half-life.
3. **Event study** — 81-day window `[T−20, T+60]` around five shocks (Aramco 2019, Soleimani 2020, Houthi 2024, Operation Epic Fury 28 Feb 2026, Hormuz closure 4 Mar 2026). Spread-z paths stacked with median + IQR band.
4. **Backtest** — Trigger: spread-z < −2 within 5 days of a flagged event. Exit on z ∈ [−0.5, 0.5] or N-day timeout. Stop at z < −3.5. Parameters fit on 2010–2018, evaluated 2019–present. Zero in-sample peeking.
5. **Regime drift** — Rolling 2-year β and rolling half-life over 1987–present. Three regime overlays: pre-shale, post-shale (~2011+), post-Feb-2026.

---

## Run

```bash
# Setup
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Reproduce end-to-end
make all
```

Pipeline order: `data → cointegration → events → backtest → regime`. Each notebook is reproducible standalone given the data layer.

---

## Repo layout

```
brent-wti-regime-shift/
├── README.md                  ← this file
├── ROADMAP.md                 ← full project plan, phased
├── requirements.txt
├── Makefile                   ← `make all` reproduces everything
├── data/
│   ├── README.md              ← provenance, roll conventions, schema
│   ├── raw/                   ← EIA pulls (gitignored)
│   └── processed/             ← cleaned series (gitignored)
├── notebooks/
│   ├── 00_data_pull.ipynb     ← EIA → cleaned CSVs
│   ├── 01_cointegration.ipynb ← Engle-Granger, Johansen, ECM half-life
│   ├── 02_event_study.ipynb   ← Spread-z paths, stacked money plot
│   ├── 03_backtest.ipynb      ← OOS PnL, Sharpe, drawdown
│   └── 04_regime_drift.ipynb  ← Rolling β, post-2026 regime test
├── scripts/
│   └── pull_eia.py            ← Standalone EIA data pull
├── paper/
│   └── outline.md             ← 1,000-word paper outline + draft
└── video/
    └── script.md              ← 2-min walkthrough script + storyboard
```

---

## Scope

**In scope:** statistical inference on the spread, event-study quantification, OOS-backtested trade rule, regime-drift evidence.

**Explicitly out of scope** (deliberate, not oversight):
- Machine-learning overlays on the spread
- RL-based execution
- Multi-asset extension (natural gas, gasoline cracks)
- High-frequency / intraday data
- Broker-grade execution simulation (slippage, commissions, financing)

The paper acknowledges these as limitations rather than pretending they're handled.

---

## License

MIT. See `LICENSE`.
