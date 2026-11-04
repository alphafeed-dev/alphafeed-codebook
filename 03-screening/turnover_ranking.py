"""成交额榜：全A按成交额排序取前 N。

看资金往哪去最直接的一张表。
"""
from alphafeed import AlphaFeed

af = AlphaFeed()
df = af.quotes.get(universes="CN_Stock", to_dataframe=True)
top = df.sort_values("amount", ascending=False).head(20)
top = top.assign(amount_yi=(top["amount"] / 1e8).round(2))
print(top[["symbol", "ext.name", "last_price", "ext.change_pct", "amount_yi"]].to_string(index=False))
