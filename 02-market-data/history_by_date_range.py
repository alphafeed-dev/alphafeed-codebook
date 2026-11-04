"""按日期区间取历史：start_time / end_time 用毫秒时间戳。

要固定区间做回测、对账时用，比 count 更精确。
"""
import datetime as dt
from alphafeed import AlphaFeed

af = AlphaFeed()

def ms(y, m, d):  # 'YYYY-MM-DD' -> 毫秒
    return int(dt.datetime(y, m, d).timestamp() * 1000)

df = af.klines.get("600519.SH", period="1d",
                   start_time=ms(2026, 9, 1), end_time=ms(2026, 9, 30),
                   adjust="forward", to_dataframe=True)
print(f"2026-09 区间取到 {len(df)} 个交易日")
print(df[["trade_date", "close"]].head().to_string(index=False))
