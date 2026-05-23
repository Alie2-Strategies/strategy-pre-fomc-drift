# strategy-pre-fomc-drift

> **Edge thesis.** Lucca & Moench (NY Fed Staff Report 512, 2015) document a robust ~49 bps average S&P 500 return in the 24 hours immediately preceding scheduled FOMC announcements over 1994-2011. The …

Strategy repository for the Alie2 Strategies Factory.

## Idea

## Pre-FOMC Drift on SPY (Lucca & Moench 2015)

**Edge thesis.** Lucca & Moench (NY Fed Staff Report 512, 2015) document a robust ~49 bps average S&P 500 return in the 24 hours immediately preceding scheduled FOMC announcements over 1994-2011. The drift is large, statistically distinct from zero, and disproportionately responsible for the equity risk premium on those dates. It is widely cited but has not faded uniformly post-publication, making it a credible candidate for a low-frequency systematic trade with a clean economic narrative (resolution of policy uncertainty / pre-announcement information leakage).

**Implementation (daily-bar approximation).** Buy SPY at the close on day **T-1** (the trading day before a scheduled FOMC announcement) and sell at the close on day **T** (the FOMC announcement day itself). This is the cleanest mapping of the 24-hour Lucca-Moench window onto daily OHLCV data — finer bars would tighten the window to the published "2pm-on-T-minus-one to 2pm-on-T" interval but introduce execution complexity that is not appropriate for the first pass. Universe: SPY only. Frequency: ~8 trades/yr (one per scheduled FOMC meeting). Cost model: **1 bp half-spread per side** (2 bps round-trip). FOMC dates hard-coded from the official Federal Reserve calendar 2020-01-01 → 2024-12-31.

**Falsification.** The idea is rejected if (a) the deflated-Sharpe z-score on the in-sample window (2020-01 → 2024-11) is below the 1.96 gate after applying the multi-testing inflation counter, OR (b) the per-window Sharpe is unstable across non-overlapping walk-forward sub-windows (concentrated strength in one regime = post-publication luck, not edge). The 2020-2024 window includes the COVID emergency cuts, the 2022 hiking cycle, and the 2024 easing pivot — a real pre-announcement drift should survive all three regimes. If it does not, archive as "documented anomaly that did not persist out-of-sample post-publication."

## Status

| Field | Value |
|---|---|
| Lifecycle | _(set by Quant via lifecycle_transition)_ |
| Trade idea KB doc | `132f53aa-449b-4b15-9209-ce3fe1474b0f` |
| Backtests | See `results/` and `public.backtest_runs` in Supabase |

## How this repo gets backtested

The Alie2 `backtest-worker` shallow-clones this repo at a pinned commit
SHA when Quant or Cassandra calls `run_backtest_at`. It imports
`strategy.py`'s `run(spec, bars) -> pd.Series` function, runs it
against the OHLCV bars fetched from Polygon for the requested period,
and persists the metrics into `public.backtest_runs` with the
`strategy_repo_commit_sha` populated so any result is reproducible.

`backtest.json` carries defaults the worker merges into the spec
(caller wins on conflicts).

## Authority

This repo is auto-managed by **Quant** (the ADK agent). She has full
read / write / merge authority here, scoped to `strategy-*` repos
under `Marvins-Organization`. Promotion of the strategy to a live
Railway monitor is reserved for human approval.
