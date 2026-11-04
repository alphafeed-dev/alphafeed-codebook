"""批量取多只历史——用 SDK 自带并发，别自己写循环打接口。

klines.batch 内部控并发(max_workers)，比 for 循环稳、也不易触发限频。
默认返回 dict{symbol: 列式数据}，每个值是 {timestamp/open/high/low/close/volume/amount}
的等长数组；想直接拿合并大表就传 to_dataframe=True。
"""
from alphafeed import AlphaFeed

af = AlphaFeed()
syms = ["600519.SH", "000001.SZ", "300750.SZ", "600036.SH", "000858.SZ"]

data = af.klines.batch(syms, period="1d", count=60, adjust="forward", max_workers=5)
for sym in syms:
    bars = data[sym]
    print(f"{sym:<12} {len(bars['close'])} 根, 最新收盘 {bars['close'][-1]}")

# 想要一张合并长表(含 symbol 列)直接用 to_dataframe=True：
# df = af.klines.batch(syms, period="1d", count=60, adjust="forward", to_dataframe=True)
