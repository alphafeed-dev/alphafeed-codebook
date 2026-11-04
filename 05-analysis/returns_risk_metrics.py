"""收益率 / 年化波动 / 最大回撤 / 夏普——一个函数全给。

后复权日线算长期收益最合适（价格连续）。无风险利率按年化 2% 举例。
"""
import numpy as np
from alphafeed import AlphaFeed

af = AlphaFeed()
df = af.klines.get("600519.SH", period="1d", count=500, adjust="backward", to_dataframe=True)
close = df["close"].astype(float)
ret = close.pct_change().dropna()

ann_return = (1 + ret.mean()) ** 252 - 1
ann_vol = ret.std() * np.sqrt(252)
sharpe = (ann_return - 0.02) / ann_vol if ann_vol else float("nan")
cummax = close.cummax()
mdd = ((close - cummax) / cummax).min()

print(f"样本 {len(ret)} 日")
print(f"年化收益  {ann_return:6.2%}")
print(f"年化波动  {ann_vol:6.2%}")
print(f"最大回撤  {mdd:6.2%}")
print(f"夏普比率  {sharpe:6.2f}  (rf=2%)")
