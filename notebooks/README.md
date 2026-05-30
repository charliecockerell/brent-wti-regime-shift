# notebooks/

Pipeline order (each builds on the previous):

| # | Notebook | Phase | Output |
|---|----------|-------|--------|
| 00 | `00_data_pull.ipynb` | 1 | `data/processed/spread.csv` |
| 01 | `01_cointegration.ipynb` | 2 | β, ECM half-life, Johansen rank, ADF results |
| 02 | `02_event_study.ipynb` | 3 | Spread-z paths, per-event metrics table, money plot |
| 03 | `03_backtest.ipynb` | 4 | OOS PnL curve, Sharpe, drawdown, hit rate |
| 04 | `04_regime_drift.ipynb` | 5 | Rolling β, rolling half-life, post-Feb-2026 regime test |
| 05 | `05_regime_adaptive.ipynb` | 6 | Regime-gated + vol-scaled overlay; Sharpe/drawdown vs naive |

Each notebook starts with the shared style block:

```python
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="whitegrid", context="paper", palette="deep")
plt.rcParams["figure.dpi"] = 120
plt.rcParams["savefig.dpi"] = 300
```

Run via `make all` (top of repo) or `jupyter nbconvert --execute --to notebook --inplace notebooks/0X_*.ipynb` individually.
