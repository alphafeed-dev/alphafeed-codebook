"""全市场扫描：一次取全A快照，本地筛出想要的票。

例子：筛「涨幅>3% 且 换手>5%」。全部本地算，不占额度。
"""
from alphafeed import AlphaFeed

af = AlphaFeed()
df = af.quotes.get(universes="CN_Stock", to_dataframe=True)

hot = df[(df["ext.change_pct"] > 0.03) & (df["ext.turnover_rate"] > 0.05)]
cols = ["symbol", "ext.name", "last_price", "ext.change_pct", "ext.turnover_rate"]
print(f"命中 {len(hot)} 只:")
print(hot[cols].sort_values("ext.change_pct", ascending=False).head(20).to_string(index=False))
