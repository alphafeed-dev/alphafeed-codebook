"""复权一致性自检：用不复权价 × 复权因子应能还原复权价。

做增量库时最容易出错的一步。这里对同一段同时取 none 和 forward，
检查比例是否稳定（除权日外应接近常数比例关系）。
"""
from alphafeed import AlphaFeed

af = AlphaFeed()
none_df = af.klines.get("600519.SH", period="1d", count=120, adjust="none", to_dataframe=True)
fwd_df = af.klines.get("600519.SH", period="1d", count=120, adjust="forward", to_dataframe=True)

ratio = (fwd_df["close"].astype(float) / none_df["close"].astype(float))
print("前复权/不复权 收盘比例:")
print("  最新:", round(ratio.iloc[-1], 6))
print("  最早:", round(ratio.iloc[0], 6))
print("  比例变动次数(≈除权事件):", int((ratio.round(6).diff().abs() > 1e-6).sum()))
print("提示：两次取数要同一 count/区间，否则对不齐；除权日比例会跳变，属正常。")
