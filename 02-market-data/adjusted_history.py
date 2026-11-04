"""前复权/后复权到底差多少——5 种口径一次看清。

复权对不上是回测结果不可复现的头号原因。AlphaFeed 给 5 种口径：
  none              不复权（看真实历史价位用）
  forward           前复权（最常用，最新价为基准）
  backward          后复权（最早价为基准，长期收益连续）
  forward_additive  前复权-加法（价差而非比例）
  backward_additive 后复权-加法
同一只票拉出来对一眼就知道该用哪种。
"""
from alphafeed import AlphaFeed

af = AlphaFeed()
sym = "600519.SH"

last = {}
for adj in ["none", "forward", "backward", "forward_additive", "backward_additive"]:
    df = af.klines.get(sym, period="1d", count=250, adjust=adj, to_dataframe=True)
    last[adj] = round(float(df["close"].iloc[-1]), 3)

print(f"{sym} 最新一根在不同复权口径下的收盘:")
for k, v in last.items():
    print(f"  {k:<18} {v}")
print("\n提示：回测请固定一种口径，别混用；比例复权看收益率，加法复权看价差策略。")
