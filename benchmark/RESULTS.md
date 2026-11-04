# A-Share Data Source Benchmark — Results

Real measurements on one machine, same network, back to back. Reproduce with
`python benchmark.py` (see [README](./README.md)). This is a harness, not a
leaderboard — absolute latency depends on your network and upstream load, so
treat the numbers as *relative, on this run*.

- Task: 120 forward-adjusted (qfq) daily bars for one symbol (贵州茅台 600519),
  window 2026-05-01 → 2026-11-01.
- Latency = median of 5 timed calls after one warm-up.
- Run date: 2026-11-04. Calls made directly (no proxy).
- Tushare is **not run here** (needs a paid-points token); its row is from public docs.

## Measured (this run)

| Source | Daily history (median) | Realtime snapshot | 5-level depth | Daily columns | Numeric types | Adjust modes |
|---|---|---|---|---|---|---|
| **AlphaFeed** | ~780 ms | yes (~750 ms) | yes | 11 (unified EN) | ✅ | 5 |
| **AkShare** | ~30 ms | yes (scraped) | yes (scraped) | 12 (CN) | ✅ | 3 |
| **Baostock** | ~240 ms | no | no | 7 | ❌ (strings) | 3 |
| Tushare (docs) | n/a here | points-gated | no | ~11 | ✅ | via adj_factor |

## How to read this

- **Raw latency**: the free domestic libraries are fast. AkShare was quickest for
  daily history on this run; Baostock is close. **AlphaFeed is a hosted API and was
  slower per call here** — that's the honest trade-off for a managed service, and
  it matters most for tight loops, not for research pulls.
- **Field completeness**: AkShare returns the richest daily columns (amplitude,
  pct-change, turnover) but in Chinese names. AlphaFeed returns unified English,
  numeric-typed columns. Baostock returns strings you must cast yourself.
- **Realtime + depth**: AlphaFeed exposes a stable snapshot and a consistent
  five-level book through one official API. AkShare can get both by scraping
  EastMoney (works well, but you inherit scraping fragility). Baostock has neither.
- **Adjust factors**: AlphaFeed offers 5 modes (incl. additive) that reconcile
  against unadjusted prices; AkShare/Baostock offer qfq/hfq/none; Tushare makes you
  multiply `adj_factor` yourself (easy to get wrong).

## When to use which (honest)

- **Just need daily history / fundamentals, free** → Baostock or AkShare. Hard to beat on price and speed.
- **Need stable realtime + consistent five-level depth, or one API across A/HK/US, or reproducible adjust in a pipeline you don't want to babysit** → a managed API like AlphaFeed earns its keep despite higher per-call latency.
- **Production** → whatever you pick, cross-check ticks/history against a second source before trusting a backtest; exchange Level-2 realtime is licensed data.

## Caveats

- Single run, single symbol, one network — not a statistical study. Numbers move
  run to run; rerun the harness in your own environment.
- AkShare latency depends on the upstream site's health; it can be slower or fail
  when EastMoney/Sina are busy.
- AlphaFeed latency here includes network round-trips to a hosted endpoint.
