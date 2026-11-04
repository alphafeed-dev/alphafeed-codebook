"""在一个股票池上算因子并排序——这里用 20 日动量举例。

流程：全A快照取成交额前 N 做池 -> 批量取 60 日线 -> 本地算 20 日涨幅 -> 排序。
换成你自己的因子(波动率/均线乖离/量比)同理。
"""
from alphafeed import AlphaFeed

af = AlphaFeed()

# 1) 用成交额前 50 当池（也可换成指数成分）
snap = af.quotes.get(universes="CN_Stock", to_dataframe=True)
pool = snap.sort_values("amount", ascending=False).head(50)["symbol"].tolist()

# 2) 批量取历史
data = af.klines.batch(pool, period="1d", count=60, adjust="forward", max_workers=8)

# 3) 本地算 20 日动量
rows = []
for sym in pool:
    c = data[sym]["close"]
    if len(c) > 21:
        rows.append((sym, round((c[-1] / c[-21] - 1) * 100, 2)))
rows.sort(key=lambda x: -x[1])
print("20 日动量 Top10（成交额前50池内）:")
for sym, mom in rows[:10]:
    print(f"  {sym:<12} {mom:+.2f}%")
