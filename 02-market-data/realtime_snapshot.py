"""实时快照：单只，和「全市场一次取」。

扫板、算涨跌家数、盯盘都靠这个。注意快照是最新一笔，不是逐笔流。
"""
from alphafeed import AlphaFeed

af = AlphaFeed()

# 单只 / 多只（返回 list[dict]，涨跌幅在 ext 里）
one = af.quotes.get(symbols="600519.SH")[0]
print("单只:", one["last_price"], "涨跌幅", round(one["ext"]["change_pct"] * 100, 2), "%")

# 全 A 一次取；to_dataframe 会把 ext.* 拍平成 ext.change_pct 这种列
snap = af.quotes.get(universes="CN_Stock", to_dataframe=True)
print("全A快照行列:", snap.shape)

# 本地算涨跌家数（ext.change_pct 是小数，0.01 = 1%）
pct = snap["ext.change_pct"]
up, down = (pct > 0).sum(), (pct < 0).sum()
print(f"涨 {up} / 跌 {down} / 平 {len(snap) - up - down}")
