"""A-share data source benchmark — AlphaFeed vs AkShare vs Baostock.

Measures real numbers on one machine, same network, back to back:
  - latency: median of N timed runs for a comparable task (120 qfq daily bars, one symbol)
  - realtime snapshot availability + latency
  - five-level depth availability
  - adjust modes and whether fields come back numeric

This is a reproducible harness, not a ranking. Run it yourself; absolute latency
depends on your network and the upstream's load. Tushare is not run here (needs a
paid-points token); its row is filled from public docs in RESULTS.md.

Usage:
    ALPHAFEED_API_KEY=... python benchmark.py
"""
from __future__ import annotations

import json
import statistics
import time
from typing import Callable

SYMBOL_AF = "600519.SH"
START, END = "2026-05-01", "2026-11-01"
RUNS = 5


def timed(fn: Callable, runs: int = RUNS) -> tuple[float, object]:
    """Warm once, then median of `runs` timed calls. Returns (median_ms, last_result)."""
    fn()  # warm (DNS, session, cache)
    samples, out = [], None
    for _ in range(runs):
        t = time.perf_counter()
        out = fn()
        samples.append((time.perf_counter() - t) * 1000)
    return round(statistics.median(samples), 1), out


def bench_alphafeed() -> dict:
    from alphafeed import AlphaFeed
    af = AlphaFeed()
    r = {"source": "AlphaFeed"}

    def daily():
        return af.klines.get(SYMBOL_AF, period="1d", count=120,
                             adjust="forward", to_dataframe=True)

    ms, df = timed(daily)
    r["daily_ms"] = ms
    r["daily_rows"] = len(df)
    r["daily_cols"] = list(df.columns)
    r["numeric_ok"] = str(df["close"].dtype) in ("float64", "float32")
    r["has_amount"] = "amount" in df.columns

    r["rt_ms"], snap = timed(lambda: af.quotes.get(symbols=SYMBOL_AF))
    r["realtime"] = "yes"
    r["depth_ms"], _ = timed(lambda: af.depth.get(SYMBOL_AF))
    r["depth"] = "yes (5-level)"
    r["adjust_modes"] = ["none", "forward", "backward",
                         "forward_additive", "backward_additive"]
    return r


def bench_akshare() -> dict:
    import akshare as ak
    r = {"source": "AkShare"}

    def daily():
        return ak.stock_zh_a_hist(symbol="600519", period="daily",
                                  start_date=START.replace("-", ""),
                                  end_date=END.replace("-", ""), adjust="qfq")

    ms, df = timed(daily)
    r["daily_ms"] = ms
    r["daily_rows"] = len(df)
    r["daily_cols"] = list(df.columns)
    r["numeric_ok"] = str(df["收盘"].dtype) in ("float64", "float32")
    r["has_amount"] = "成交额" in df.columns

    # single-symbol realtime bid/ask (scraped from EastMoney)
    try:
        r["rt_ms"], _ = timed(lambda: ak.stock_bid_ask_em(symbol="600519"))
        r["realtime"] = "yes (scraped)"
        r["depth"] = "yes (5-level, scraped)"
        r["depth_ms"] = r["rt_ms"]
    except Exception as e:  # noqa: BLE001
        r["realtime"] = f"error: {type(e).__name__}"
        r["depth"] = "n/a"
    r["adjust_modes"] = ["none", "qfq", "hfq"]
    return r


def bench_baostock() -> dict:
    import baostock as bs
    r = {"source": "Baostock"}
    bs.login()

    def daily():
        rs = bs.query_history_k_data_plus(
            "sh.600519", "date,open,high,low,close,volume,amount",
            start_date=START, end_date=END, frequency="d", adjustflag="2")
        rows = []
        while rs.error_code == "0" and rs.next():
            rows.append(rs.get_row_data())
        return rows

    ms, rows = timed(daily)
    r["daily_ms"] = ms
    r["daily_rows"] = len(rows)
    r["daily_cols"] = ["date", "open", "high", "low", "close", "volume", "amount"]
    r["numeric_ok"] = False  # baostock returns strings
    r["has_amount"] = True
    r["realtime"] = "no"
    r["depth"] = "no"
    r["adjust_modes"] = ["none", "qfq", "hfq"]
    bs.logout()
    return r


def main() -> None:
    results = []
    for fn in (bench_alphafeed, bench_akshare, bench_baostock):
        try:
            results.append(fn())
        except Exception as e:  # noqa: BLE001
            results.append({"source": fn.__name__, "error": f"{type(e).__name__}: {e}"})
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
