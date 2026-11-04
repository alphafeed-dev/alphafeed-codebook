"""A股 / 港股 / 美股，一套代码取历史。

跨市场组合、A/H 比价、海外对比不用再换库换字段。
"""
from alphafeed import AlphaFeed

af = AlphaFeed()
for sym in ["600519.SH", "00700.HK", "AAPL.US"]:
    df = af.klines.get(sym, period="1d", count=20, adjust="forward", to_dataframe=True)
    print(f"{sym:<12} 取到 {len(df)} 根, 最新收盘 {float(df['close'].iloc[-1])}")
    # 注意：港股/美股的 amount(成交额) 字段可能为 0，如需成交额以官方口径为准
