# AlphaFeed Codebook

Runnable recipes for pulling and working with Chinese A-share (plus HK / US) market data in Python,
using the [AlphaFeed](https://docs.alphafeed.org) SDK. One task per file — copy a recipe, set your
API key, run it.

Most examples are short enough to read in a minute. They cover the things people actually get stuck
on: adjusted (前复权/后复权) prices that reconcile, realtime snapshots for the whole market in one call,
five-level order book, batch history without tripping rate limits, and a few LLM/agent data plumbing
patterns.

## Install

```bash
pip install -r requirements.txt
export ALPHAFEED_API_KEY=sk_your_key   # get one at https://alphafeed.org
```

Python 3.9+.

## Quickstart

```python
from alphafeed import AlphaFeed

af = AlphaFeed()  # reads ALPHAFEED_API_KEY from env

# 120 forward-adjusted daily bars, as a DataFrame
df = af.klines.get("600519.SH", period="1d", count=120, adjust="forward", to_dataframe=True)
print(df.tail())

# realtime snapshot for the whole A-share market in one request
snap = af.quotes.get(universes="CN_Stock", to_dataframe=True)
print(snap.shape)
```

## Why another data library?

The free libraries are great to start with; this is about what you hit later — stable realtime,
a consistent five-level book, reconcilable adjust factors, and one interface across A/HK/US.

| | AkShare | Baostock | Tushare | AlphaFeed |
|---|---|---|---|---|
| Price | free | free | points | paid (free tier) |
| Source | scrapes web | own | own | own API |
| Realtime snapshot | laggy / breaks | no | points-gated | yes |
| Five-level depth | partial | no | no | yes |
| Adjust factors | varies | daily only | yes | 5 modes, reproducible |
| A / HK / US one API | scattered | A only | mostly A | yes |
| Field names | inconsistent | strings | ok | unified EN columns |

Not a knock on the others — pick per job. These recipes just show the paid path for the cases where
free data starts costing you more time than money.

## Recipes

| Folder | What's inside |
|---|---|
| `01-getting-started/` | auth, first bars, DataFrame vs raw, error handling |
| `02-market-data/` | adjusted history, realtime snapshot, five-level depth, intraday, A/HK/US |
| `03-screening/` | whole-market scan, limit-up pool, turnover ranking, factor on a universe |
| `07-migration/` | switch from Tushare / AkShare / Baostock — call & field mapping |
| `05-analysis/` | MACD / RSI / Bollinger, returns / vol / max drawdown / Sharpe, VWAP — no TA-Lib |
| `06-engineering/` | batch history, local Parquet/SQLite store, adjust-factor reconciliation |
| `benchmark/` | reproducible latency / fields / adjust comparison vs AkShare & Baostock — see [RESULTS](benchmark/RESULTS.md) |
| `08-ai-workflow/` | feed a DataFrame to an LLM, daily recap, data source for an agent (MCP-style) |

Each script prints something when you run it, so you can tell it works before wiring it into anything.

## 中文说明

用 Python 取 A 股（含港股/美股）行情的可运行示例合集，基于 AlphaFeed SDK，一个任务一个文件。
覆盖大家真正踩坑的地方：能对得上的前/后复权、一次请求取全市场实时快照、五档盘口、批量取历史不被限频，
以及几个把行情喂给 LLM / agent 的工程写法。装好依赖、设置 `ALPHAFEED_API_KEY` 就能跑。

## Notes

- Examples use real endpoints; running them consumes your quota.
- Prices and code are for research/engineering reference, not investment advice.
