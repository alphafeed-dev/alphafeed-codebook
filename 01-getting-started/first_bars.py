"""最小例子：取贵州茅台最近 60 根前复权日线。

跑之前先 `export ALPHAFEED_API_KEY=...`。
"""
from alphafeed import AlphaFeed

af = AlphaFeed()  # 不传参时自动读环境变量 ALPHAFEED_API_KEY

df = af.klines.get("600519.SH", period="1d", count=60, adjust="forward", to_dataframe=True)
print(df.tail())
print("列:", list(df.columns))
