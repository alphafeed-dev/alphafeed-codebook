"""实时快照：单只，和「全市场一次取」。

扫板、算涨跌家数、盯盘都靠这个。注意快照是最新一笔，不是逐笔流。
"""
from alphafeed import AlphaFeed

af = AlphaFeed()

# 单只 / 多只
one = af.quotes.get(symbols="600519.SH")
print("单只:", one[0]["last_price"])

# 全 A 一次取（universes 省去自己维护代码表）
snap = af.quotes.get(universes="CN_Stock", to_dataframe=True)
print("全A快照行列:", snap.shape)

# 本地算涨跌家数（change_pct 是小数，0.01 = 1%）
up = (snap["change_pct"] > 0).sum()
down = (snap["change_pct"] < 0).sum()
print(f"涨 {up} / 跌 {down} / 平 {len(snap) - up - down}")
