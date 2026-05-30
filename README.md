# brent-wti-regime-shift

**Author:** Charlie Cockerell · Durham University · https://www.linkedin.com/in/charliecockerell/
**Submission:** Onyx Research Competition 2026
**Paper:** [Read the full write-up (PDF)](https://raw.githubusercontent.com/charliecockerell/brent-wti-regime-shift/main/paper/paper.pdf)

---

## Thesis

> The Brent–WTI spread is a cointegrating relationship in normal regimes. However, there is precedent of supply changes affecting this relationship. Despite the strong dislocation caused by the US-Iran conflict, there is evidence to suggest no structural change yet.

---

## Headline numbers

| Metric | Value | Source |
|--------|-------|--------|
| Cointegration β (full sample) | 1.094 [1.086, 1.101] | `notebooks/01_cointegration.ipynb` |
| ECM half-life (full sample) | 24.2 days | `notebooks/01_cointegration.ipynb` |
| EG cointegration p-value | < 0.001 (Johansen rank 1 confirmed) | `notebooks/01_cointegration.ipynb` |
| Post-event vol ratio: historical vs 2026 | ~1.2× vs ~8–9× (Levene W=76.7, p<0.001) | `notebooks/02_event_study.ipynb` |
| Post-2026 β (resilience test) | 1.012 [CI spans unity] — no structural break detected | `notebooks/04_regime_drift.ipynb` |
| Rolling 2-yr half-life post-conflict | ≤ 8.4 days (vs 147 days at 2011 shale break) | `notebooks/04_regime_drift.ipynb` |
| Naive OOS Sharpe / max DD | 1.02 / −$26.0/bbl | `notebooks/03_backtest.ipynb` |
| OOS Sharpe significance | block-bootstrap 95% CI [0.33, 1.65]; permutation p<0.001 | `notebooks/03_backtest.ipynb` |
| Gated + vol-scaled Sharpe / max DD | 1.42 / −$4.6/bbl (82% DD reduction) | `notebooks/05_regime_adaptive.ipynb` |

---

## Method

1. **Data** — EIA daily series RBRTE (Brent) and RWTC (WTI), 1987–present.

2. **Cointegration** — Engle-Granger two-step (ADF on log levels, OLS on log(Brent) ~ log(WTI), ADF on residuals), cross-checked with Johansen. Error-correction model for the full-sample half-life. Robustness: Zivot-Andrews unit-root test allowing one break; Gregory-Hansen cointegration test with an endogenous regime break; Chow breakpoint and predictive-failure tests at 28 Feb 2026; subsample stability across five windows.

3. **Event study** — 81-day display window [T−20, T+60] around five shocks (Aramco 2019, Soleimani 2020, Houthi 2024, Operation Epic Fury 28 Feb 2026, Hormuz closure 4 Mar 2026). Spread-z normalised against a 60-day estimation window ending 20 days before each event. Soleimani window censored at 20 Feb 2020 to exclude the COVID demand crash. Peak metrics computed on [0, +20]. Paths stacked with median + IQR band.

4. **Backtest** — Enter long spread when rolling 60-day spread-z < −2; exit when |z| ≤ 0.5 or after timeout; hard stop at |z| ≥ 3.5. Parameters set a priori on the full 1987–2018 in-sample period, evaluated on 2019–present. Zero in-sample peeking. Regime-adaptive extension (notebook 05) gates new entries during crisis-vol regimes (20-day realised vol above its trailing 80th percentile) and applies inverse-vol position sizing.

5. **Regime drift** — Rolling 2-year β and rolling half-life (from AR(1) autocorrelation on ECM residuals) over 1987–present. Three regime overlays: pre-shale (<2011), post-shale (2011–Feb 2026), post-Epic-Fury (≥Feb 2026).

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

### Key Visualizations

* Stacked event-study paths with median + IQR bands are saved to `figures/fig_money_plot.png`, and the 2026 dislocation in isolation to `figures/fig_shock_2026.png`.
* The out-of-sample equity curve is exported to `figures/fig_backtest_oos.png`, and the regime-gated, vol-scaled comparison to `figures/fig_regime_adaptive.png`.

---

## Inspiration

What interested me most in my reading were advanced estimation methods such as the hidden Markov model of Fanelli, Fontana & Rotondi (2023, arXiv:2309.00875). I'd like to apply similar estimation machinery to other instruments — such as the options contracts I started to explore during Imc's Prosperity challenge.

---

## License

MIT. See `LICENSE`.
