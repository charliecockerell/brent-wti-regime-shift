# The Brent–WTI Spread Under the 2026 US–Iran Conflict: A Tradeable Anatomy of Short- and Long-Term Oil-Market Consequences

*Onyx Research Competition 2026 — Technical Track. Draft (~1,000 words). All statistics from the reproducible pipeline at github.com/charliecockerell/brent-wti-regime-shift.*

---

## Thesis (≈60 words)

The Brent–WTI spread is a stable cointegrating relationship that dislocates sharply but transiently under Middle East supply shocks. The 2026 US–Iran conflict produced the largest such dislocation in the sample, yet the underlying relationship proved resilient. The short-term consequence is a tradeable mean-reversion; the long-term consequence, on this relationship, is negligible — locating the conflict's durable effects elsewhere in the oil complex.

## Data and the cointegrating relationship (≈190 words)

I use EIA daily spot prices for Brent (RBRTE) and WTI (RWTC), 1987–2026 (9,730 observations). The single non-positive print — WTI's −$36.98 close on 20 April 2020 — is excluded from log-level analysis but retained in the raw record.

Both log-price series are I(1) (ADF fails to reject a unit root in levels, p≈0.34; rejects in first differences, p<0.001). The Engle–Granger cointegrating regression

$$\log B_t = \alpha + \beta \log W_t + \varepsilon_t$$

gives **β = 1.094, 95% CI [1.086, 1.101]** (R²=0.993). β exceeds 1 with the unit value outside the interval: Brent, the waterborne benchmark, is marginally more elastic to price moves than landlocked WTI — itself a small but significant result. The residual is stationary (Engle–Granger p<0.001), and Johansen confirms exactly one cointegrating vector (rank 1). An error-correction model yields a correction coefficient γ=−0.028 (t=−5.2) and a **mean-reversion half-life of 24 trading days** — the load-bearing statistic for everything that follows: the spread reverts, on a month-ish timescale, toward a stable long-run relationship.

## Short-term consequence: the event study (≈230 words)

For five shocks — Aramco (Sep 2019), Soleimani (Jan 2020), Houthi (Jan 2024), Operation Epic Fury (28 Feb 2026) and the Hormuz closure (4 Mar 2026) — I measure the spread's *z*-score against a pre-event baseline, on a clean 20-day post-event horizon. (The horizon matters: a wider window lets the March-2020 COVID crash contaminate the Soleimani path, so Soleimani is censored pre-COVID.)

The result reframes the conventional "supply shocks blow out the spread" intuition. Historically, the spread barely moved: Aramco — the largest physical supply disruption of its era — shifted it by **less than one standard deviation**; Soleimani and Houthi reached only ~3σ, mixed in sign. **2026 is categorically different**: a sustained widening to **≈+12σ**, with post-event volatility **8.3× the pre-event baseline** versus ~1.2× historically. The 2026 dislocation had not renormalised by the data edge (26 May 2026).

So the short-term consequence of the conflict is a genuine, outsized, and — given the 24-day reversion half-life — *tradeable* dislocation. The historical comparables serve as the null that makes 2026 stand out: this was not "another transient blow-out" but the sharpest relative-value event in four decades of data.

## The trade, and its failure mode (≈200 words)

A naive mean-reversion rule — enter at |z|≥2, exit at |z|≤0.5, hard stop at |z|≥3.5, trailing-window *z*, next-bar execution, parameters fixed *a priori* — earns an **out-of-sample (2019–2026) Sharpe of 1.02** across 63 trades (83% hit rate, +$88/bbl), against ~0.00 for a passive always-long-spread benchmark. Train (1987–2018) Sharpe is 0.99: almost no decay.

But the strategy's worst drawdown, **−$26/bbl, is the 2026 crisis itself.** The mechanism is structural: the rule shorts the spread at +2σ and is stopped out for a loss at +3.5σ as the spread marches to +12σ — picking up pennies in front of the steamroller. Vanilla mean-reversion bleeds precisely when the dislocation is largest.

## Long-term consequence: resilience, not rupture (≈190 words)

Did the conflict permanently change the relationship? A direct pre/post-event test (58 observations each side) gives a **post-event β of 0.987, 95% CI [0.768, 1.206]** — overlapping the pre-event β (1.105), the full-sample β (1.094), and unity. The half-life shows no lengthening. Rolling-window estimates confirm it: the method clearly detects the 2011 shale break (regime-mean half-life 3.0→9.6 days), but flags **no comparable break after February 2026**.

The honest verdict: the conflict's lasting impact *on this relationship* is **negligible**. The spread dislocated violently and reverted; the cointegration that drives reversion did not break.

This is not "no long-term consequence." The Brent–WTI spread is a *relative-value* lens — US versus waterborne crude — and is silent on effects that move both legs together: a sustained war-risk premium on the outright level, a higher-volatility regime, elevated Hormuz freight and insurance (Worldscale, Lloyd's war-risk areas), and OPEC+ spare-capacity erosion. The conflict's durable footprint lives in *those* dimensions, not in the US–global crude linkage.

## A regime-adaptive philosophy (≈140 words)

The two findings combine into a trading rule: **the cointegration is the anchor; the regime decides deployment.** Because the relationship is resilient, the crisis reversion *will* come — just not on a timescale a fixed stop survives. So mean-revert in calm; in crisis (20-day realised volatility above its trailing-year 80th percentile), suppress new entries and size down.

Gating the naive strategy this way lifts OOS Sharpe **1.02→1.32** and cuts max drawdown **−$26→−$5.6**; adding inverse-volatility sizing reaches **Sharpe 1.42, drawdown −$4.6**. Absolute PnL falls (the gate forgoes some profitable reversions, as in the fast-reverting COVID-2020 case) — but a higher-Sharpe, lower-drawdown strategy can be levered to beat the naive version at equal risk. The adaptation converts the strategy's single worst failure mode — being run over in a supply shock — into flat exposure.

## Limitations (≈50 words)

Five clean events is a small sample; the 58-observation post-2026 window is wide and still unfolding. PnL is gross of financing, slippage, and roll costs, with unit position sizing and spot (not calendar-matched futures) prices. The regime gate is risk control, not prescience — it cannot tell a grinding crisis from a fast-reverting one in advance.
