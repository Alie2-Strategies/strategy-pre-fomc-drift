"""Pre-FOMC drift on SPY (Lucca-Moench 2015, NY Fed SR 512)."""
from __future__ import annotations
from typing import Any
import pandas as pd

# FOMC announcement dates 2020-01-01 through 2024-12-31
FOMC_DATES = pd.to_datetime([
    "2020-01-29","2020-03-03","2020-03-15","2020-04-29","2020-06-10","2020-07-29","2020-09-16","2020-11-05","2020-12-16",
    "2021-01-27","2021-03-17","2021-04-28","2021-06-16","2021-07-28","2021-09-22","2021-11-03","2021-12-15",
    "2022-01-26","2022-03-16","2022-05-04","2022-06-15","2022-07-27","2022-09-21","2022-11-02","2022-12-14",
    "2023-02-01","2023-03-22","2023-05-03","2023-06-14","2023-07-26","2023-09-20","2023-11-01","2023-12-13",
    "2024-01-31","2024-03-20","2024-05-01","2024-06-12","2024-07-31","2024-09-18","2024-11-07","2024-12-18",
], utc=True).normalize()

def run(spec: dict[str, Any], bars: pd.DataFrame) -> pd.Series:
    """Hold SPY from close(T-1) to close(T) where T is an FOMC day."""
    if bars.empty:
        return pd.Series(dtype=float)
    df = bars.copy()
    df.index = df.index.normalize()
    half_spread = float(spec.get("half_spread_bps", 1.0)) / 10000.0
    cost = 2.0 * half_spread

    # Mark FOMC days that exist in our data
    fomc_in_window = [d for d in FOMC_DATES if d in df.index]
    out = {}
    for fomc_day in fomc_in_window:
        idx = df.index.get_loc(fomc_day)
        if idx < 1:
            continue
        prev_close = float(df.iloc[idx - 1]["close"])
        fomc_close = float(df.loc[fomc_day]["close"])
        ret = fomc_close / prev_close - 1.0 - cost
        out[fomc_day] = ret
    return pd.Series(out, name="ret").sort_index()
