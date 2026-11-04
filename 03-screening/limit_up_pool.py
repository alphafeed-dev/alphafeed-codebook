"""涨停池：用快照价逼近涨停价来判定。

涨停价来自 instruments 元数据；这里对快照里接近涨停的票做二次确认。
注意：ST/科创/创业板涨跌幅限制不同，严谨做法按板块规则，这里给通用近似。
"""
from alphafeed import AlphaFeed

af = AlphaFeed()
df = af.quotes.get(universes="CN_Stock", to_dataframe=True)

# 近似：涨幅 >= 9.8% 视为涨停候选（主板 10%）
cand = df[df["ext.change_pct"] >= 0.098]
print(f"涨停候选 {len(cand)} 只:")
print(cand[["symbol", "ext.name", "last_price", "ext.change_pct"]]
      .sort_values("ext.change_pct", ascending=False).head(30).to_string(index=False))
