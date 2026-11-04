"""周线 / 月线：period 换成 1w / 1M / 1Q / 1Y 即可。

长周期择时、月度复盘用。复权口径和日线一致。
"""
from alphafeed import AlphaFeed

af = AlphaFeed()
for p in ["1w", "1M", "1Q"]:
    df = af.klines.get("600519.SH", period=p, count=6, adjust="forward", to_dataframe=True)
    print(f"[{p}] 最近 {len(df)} 根, 最新收盘 {float(df['close'].iloc[-1])}")
