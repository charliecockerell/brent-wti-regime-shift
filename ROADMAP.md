# Onyx Research Competition — Brent/WTI Regime-Shift Study

**Status:** 🟢 Active (CV-feeding, Quant Project #2)
**Started:** 2026-05-30 (roadmap)
**Track:** Technical
**Prompt:** "Evaluate the short and long-term consequences of the recent US–Iran conflict on the oil market."
**Deliverable:** 1,000-word paper (PDF) + 2-min video walkthrough + public GitHub repo

## Forcing function (LOCKED)
- **Submission deadline:** 23 July 2026.
- **Target ship date:** 23 June 2026 (one-month buffer; never trust your own deadline).
- **Working runway:** ~24 calendar days from today (30 May → 23 June). Roadmap below fits inside that window.
- Register / sign ToS / confirm submission format — Phase 0 task.

## Locked decisions (30 May 2026)
| # | Decision | Locked value |
|---|----------|-------------|
| 1 | Submission deadline | 23 July 2026 (target 23 June, one-month buffer) |
| 2 | Focal event | **28 Feb 2026** — Operation Epic Fury (US/Israel coordinated strikes, conflict start). Secondary anchor: **4 Mar 2026** — Iranian closure of Strait of Hormuz. Both treated in the event study; conflict start is t=0. |
| 3 | Data source | EIA daily series — RBRTE (Brent), RWTC (WTI). Yahoo `BZ=F`/`CL=F` only as cross-check. |
| 4 | Repo name | `brent-wti-regime-shift` (public). Names the methodology, readable on CV. |
| 5 | Stack | Python 3.11+, pandas, statsmodels, matplotlib + **seaborn** (visuals — see note below), jupyter. `requirements.txt` minimal. |

**Viz library note (re: "sea thingy"):** yes — seaborn is the right call here. It's a thin matplotlib wrapper, so you keep full matplotlib control when you need it, but gain much better defaults out of the box and statistical-plot helpers. Specifically, `seaborn.lineplot` does the event-study money plot for free — median spread-z path across events with a shaded IQR band. Plotly was the alternative; it's interactive, which is wasted on a PDF and over-engineered for a 2-min screen-recording. **Lock: matplotlib + seaborn, one shared style sheet set at the top of every notebook so the paper, repo, and video all look consistent.**

## Thesis (lock before writing code)
> The Brent–WTI spread is a stable cointegrating relationship in normal regimes but blows out sharply and transiently under Middle East supply shocks. This creates an exploitable mean-reversion trade on a defined timescale, with a long-term decay risk if the Hormuz transit-risk premium becomes structurally priced and the cointegrating vector permanently reprices.

Short-term consequence = the trade. Long-term consequence = the regime shift. Both halves of the prompt covered.

## Scope discipline (quant-signal filter)
1,000 words is brutal — the paper is the asset, the code exists to back it up. Apply the filter ruthlessly:
- ✅ **Signal:** Engle-Granger cointegration, ECM half-life, event-study spread-z paths, out-of-sample backtested PnL, rolling-β regime drift chart.
- ⚠️ **Borderline:** polished plotly dashboards, video production value. Cap at 1 day total or cut.
- ❌ **Out:** ML overlays, RL agent on the spread, multi-asset extension (gas/cracks), broker-grade execution sim. Kill on sight — they steal narrative oxygen and don't survive the word count.

## Phase 0 — Frame & register (Day 0–1)
- Register on Onyx site / sign ToS / confirm submission format (PDF + video upload mechanics).
- Add 23 June (target submit) and 23 July (hard deadline) to Calendar with reminders.
- Read prior Onyx Technical-track winners if public — they are the rubric.
- Create the GitHub repo `brent-wti-regime-shift` (public, MIT licence). Push README skeleton + thesis statement on commit #1 — public from the start.

## Phase 1 — Data (Day 2–3)
- **Sources:** EIA daily series — RBRTE (Brent), RWTC (WTI). Pull via `https://api.eia.gov/v2/...` or direct CSV. Yahoo `BZ=F`/`CL=F` cross-check only.
- **Window:** 1987–present (EIA RBRTE/RWTC inception). Captures Aramco drone (Sep 2019), Soleimani strike (Jan 2020), Houthi Red Sea (2024), and the 2026 Hormuz crisis inside one continuous series. Note: 20 Apr 2020 negative-WTI print dropped from the processed log-level series (see `data/README.md`).
- **Front-month vs continuous:** continuous back-adjusted series; document the roll convention in `data/README.md`. Real quant artifact vs Yahoo Finance hobby plot.
- **Event list (locked):**
  - 16 Sep 2019 — Aramco Abqaiq drone strike
  - 3 Jan 2020 — Soleimani assassination
  - 19 Jan 2024 — Houthi Red Sea attacks intensify (use as ambient escalation control)
  - **28 Feb 2026 — Operation Epic Fury (primary focal event, t=0)**
  - **4 Mar 2026 — Hormuz closure announced (secondary anchor; supply-shock trigger)**
  - 19 Mar 2026 — US aerial reopen campaign
  - 13 Apr 2026 — US counter-blockade
- Commit raw + cleaned data with `data/README.md` provenance section. Reproducibility is a quant signal in itself.

## Phase 2 — Cointegration baseline (Day 4–7)
- ADF on `log(Brent)` and `log(WTI)` — confirm both I(1).
- **Engle-Granger step 1:** OLS `log(Brent)_t = α + β·log(WTI)_t + ε_t`. Report β with confidence interval. β ≈ 1 is the null; any deviation is itself news worth interpreting.
- **Engle-Granger step 2:** ADF on residuals — reject unit root → cointegrated.
- **Cross-check Johansen** (one-rank vs two-rank). Light-touch but reviewers like to see it.
- **Fit ECM:** `Δlog(Brent)_t = γ·ε_{t-1} + lags + u_t`. Headline number: **half-life of mean reversion = −log(2)/log(1+γ)**. This is the load-bearing statistic for the trade thesis.
- Output: `notebooks/01_cointegration.ipynb`. One tight section per test.

## Phase 3 — Event study (Day 8–11)
- For each shock, window `[T−20, T+60]` trading days. Compute spread-z path: `z_t = (spread_t − μ_60d)/σ_60d` anchored on the pre-event window.
- **Per-event metrics table:** peak |z|, days-to-peak, days-to-renormalisation (|z|<1), residual variance pre vs post, ECM half-life pre vs post.
- **Money plot:** all events stacked on one chart, spread-z vs days-from-event, with median path. This single figure carries half the paper.
- Output: `notebooks/02_event_study.ipynb`.

## Phase 4 — Trade rule + backtest (Day 12–14)
- **Rule (simple, defensible):** enter long Brent / short WTI when spread-z < −2 AND a flagged event occurred in the last 5 trading days. Exit when z ∈ [−0.5, 0.5] or after N days, whichever first. Hard stop at z < −3.5.
- **Honest reporting:** parameters picked on 2010–2018, tested 2019–present. State this explicitly. Zero in-sample peeking.
- **Headline metrics:** trade count, hit rate, mean PnL per trade, OOS Sharpe, max drawdown, average holding period. Benchmark vs naive "always-long spread."
- Output: `notebooks/03_backtest.ipynb` + clean PnL curve for the paper.

## Phase 5 — Long-term repricing (Day 15–16)
- Don't skip — the prompt asks for *short and long-term* consequences. Most entrants will half-answer this and tank their score.
- **Hypothesis:** if Hormuz transit risk becomes structurally priced (war-risk insurance premia, sustained tanker rate spread, OPEC+ Saudi spare capacity erosion), the cointegrating β shifts permanently, half-life lengthens, and the mean-reversion trade decays.
- **The 2026 angle that's uniquely strong:** the IEA called this "the largest supply disruption in the history of the global oil market." Unlike past Middle East shocks that produced *transient* spread blow-outs, the 2026 event may be the structural repricing event itself, observed in real-time. The paper should test this explicitly — compare 2019–2020 events (transient) against 2026 (potentially structural) and ask whether β/half-life have stayed shifted through May 2026, not just spiked and returned.
- **Evidence:** rolling 2-year β and rolling half-life over 1987–present. Three regime overlays: pre-shale, post-shale (~2011+), post-Feb-2026. If post-Feb-2026 β is visibly different, that's the headline qualitative claim.
- Citations to chase: Lloyd's Joint War Committee listed-area risk premia, TankerTrackers Hormuz throughput data, Worldscale flat rates, IEA *Oil Market Report* for the 2026 disruption framing.

## Phase 6 — Paper (Day 17–20)
1,000 words. Tight allocation:
- Thesis (50w)
- Spread regime + cointegration table (200w)
- Event study + money plot + per-event metrics (250w)
- Trade rule + OOS PnL (250w)
- Long-term repricing + rolling-β chart (200w)
- Limitations (50w)

Every figure earns its caption budget. Cut adjectives. Render via `docx` skill once content is final, then export PDF.

## Phase 7 — Video (Day 21)
2 minutes ≈ 280–320 spoken words. Storyboard:
- 0:00–0:20 — hook + thesis
- 0:20–0:50 — cointegration setup + β + half-life
- 0:50–1:20 — event study money plot
- 1:20–1:50 — OOS backtest result
- 1:50–2:00 — long-term repricing + close

Screen-record over the notebooks. Don't over-produce — quant-signal flag: if the deadline tightens, ship a strong paper without a polished video before shipping a weak paper with a great video.

## Phase 8 — Repo polish (Day 22)
- README: thesis, headline numbers (β, half-life, OOS Sharpe), how to run, methodology, what's *not* in scope.
- Notebooks pinned in execution order. `requirements.txt` minimal. `make all` reproduces end-to-end.
- Tag `v1.0-onyx`. Link paper PDF in README.
- This is the CV asset. A reviewer should grok the thesis in 30 seconds and the methodology in 5 minutes.

## Phase 9 — Submit + log (Day 23)
- Submit. Screenshot confirmation, save to `Resources/`.
- Tracker: log to Pipeline tab (Onyx — Internship + Research Comp, both ticked).
- Calendar: announcement date as event with reminder.

## Pushback / things to challenge
- **Event sample size is tiny.** 4–5 events doesn't support strong inference. Frame in Limitations honestly; reviewers spot oversold stats instantly.
- **Front-month-only is a shortcut.** Real Brent–WTI spread trading uses calendar-matched contracts (M+1 vs M+1) to avoid contango/backwardation noise. Acknowledge in Limitations, or upgrade in Phase 1 if deadline allows.
- **Cointegration may have already broken.** Post-shale-revolution (~2011 onward) the Brent–WTI relationship is well-known to have structurally shifted once. If the rolling-β chart shows the relationship is currently *unstable*, the trade thesis weakens — write that honestly rather than burying it.
- **Quant-signal infrastructure-vs-signal flag:** repo CI, Docker, fancy dashboards = infrastructure. Cointegration test, ECM, OOS Sharpe, regime-drift chart = signal. Default to cutting infrastructure.

## Decisions owed before Phase 1
~~All five locked 30 May 2026 — see "Locked decisions" table above. Phase 1 is unblocked.~~

## New angle worth flagging (post-event-research)
The 2026 Hormuz crisis is *uniquely* large vs the historical comparables (Aramco 2019, Soleimani 2020) — IEA "largest supply disruption in history of global oil market." This changes the paper's centre of gravity:
- **Old framing:** "Spread blow-outs are transient; trade the mean reversion." Long-term repricing is hypothetical.
- **New framing:** "2019–2020 events were transient blow-outs (proof of the mean-reversion trade). 2026 may be the structural repricing itself, observable in real-time." The trade thesis still holds for the smaller historical events, but the live 2026 case is the long-term repricing story.

This is a stronger, more defensible paper: short-term consequence = the mean-reversion trade backtested on historical shocks; long-term consequence = the regime change happening now. Both halves of the prompt land hard. Update Phase 5 reflects this.

## Success criteria (submission day)
- Cointegration result with β, ECM half-life, Johansen cross-check.
- Event study covering ≥4 shocks with stacked spread-z plot.
- OOS backtest with reported Sharpe, drawdown, hit rate; train/test split explicit.
- Rolling-β regime-drift chart with honest read on current stability.
- 1,000-word paper, 2-min video, public repo with reproducible `make all`.
- Onyx submission confirmed; row logged in Pipeline tab.
