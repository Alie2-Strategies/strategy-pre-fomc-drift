# Dockerfile placeholder — only filled in once this strategy graduates
# to a live Railway monitor. Built backtests run inside the shared
# backtest-worker service; no per-strategy image is needed during
# research.
#
# When Marvin approves 'paper_traded → live', Quant rewrites this file
# to ship the strategy as its own Railway service that polls Polygon
# on a cron schedule and fires alerts when its signal triggers.
