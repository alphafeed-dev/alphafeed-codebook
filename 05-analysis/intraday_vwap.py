"""用日线成交额/成交量近似当日均价（VWAP 思路）。

说明：真正的 VWAP 要日内分时数据；这里用日频 amount/volume 给出当日量额加权均价，
适合做收盘复盘。amount 单位为元、volume 为股时，均价 = amount / (volume*100) 视交易所口径而定，
下面按 amount/volume 直接给比值并提示口径。
"""
from alphafeed import AlphaFeed

af = AlphaFeed()
df = af.klines.get("600519.SH", period="1d", count=10, adjust="none", to_dataframe=True)
df = df.assign(vwap_like=(df["amount"] / df["volume"]).round(3))
print(df[["trade_date", "close", "amount", "volume", "vwap_like"]].to_string(index=False))
print("\n口径提示：A股 volume 常以手(100股)计，换算真实均价时按你的数据口径乘/除 100。")
