# Benchmark

A small, reproducible harness comparing A-share data sources (AlphaFeed, AkShare,
Baostock) on the same machine and network: latency, field completeness, realtime /
depth availability, and adjust modes.

## Run

```bash
python -m venv .venv && . .venv/bin/activate
pip install alphafeed akshare baostock pandas
export ALPHAFEED_API_KEY=sk_your_key
python benchmark.py          # prints JSON; see RESULTS.md for a written summary
```

Latency is median of 5 timed calls after a warm-up. It depends on your network and
the upstream's load — rerun it yourself rather than trusting one person's numbers.
See [RESULTS.md](./RESULTS.md) for a sample run and how to read it.
