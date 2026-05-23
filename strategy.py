"""Strategy entry point for strategy-pre-fomc-drift.

`run(spec, bars)` is the contract every strategy repo must export.
Called by Alie2's backtest-worker after a shallow-clone at a pinned
commit SHA. The worker fetches OHLCV bars from Polygon based on
spec.ticker / spec.start / spec.end, then calls this function.

Return a pandas Series of per-trade decimal returns AFTER costs.
Empty Series == zero trades fired, which the metrics layer handles
cleanly (reported as 0 trades, no edge).
"""

from __future__ import annotations

from typing import Any

import pandas as pd


def run(spec: dict[str, Any], bars: pd.DataFrame) -> pd.Series:
    """Per-trade returns for idea:pre-fomc-drift-spy.

    spec carries:
      ticker, start, end          — also in the worker call, repeated here
      half_spread_bps             — slippage / cost model parameter
      <strategy-specific params>  — e.g. lookback, threshold

    bars is the OHLCV DataFrame indexed by timestamp. Columns:
      open, high, low, close, volume, vwap, n_transactions
    """
    if bars.empty:
        return pd.Series(dtype=float)

    # TODO: implement the strategy. The trivial scaffold below — buy
    # at the open, sell at the close every bar — exists so the repo
    # backtests cleanly the moment it's created. Replace with the
    # actual signal once Quant has written it.
    df = bars.copy()
    half_spread_bps = float(spec.get("half_spread_bps", 1.0))
    cost = 2.0 * (half_spread_bps / 10000.0)
    intraday = df["close"] / df["open"] - 1.0 - cost
    out = intraday.dropna()
    out.name = "ret"
    return out
