"""标的元数据：tick、涨跌停价、股本、上市日。

算涨跌停、流通市值、换手要用到这些，别硬编码。
"""
from alphafeed import AlphaFeed

af = AlphaFeed()
meta = af.instruments.get("600519.SH")
ext = meta.get("ext", {})
for k in ["tick_size", "limit_up", "limit_down", "total_shares", "float_shares", "listing_date"]:
    print(f"{k:<14} {ext.get(k)}")
