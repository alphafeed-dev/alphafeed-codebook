"""五档盘口 + 委比委差。

depth.get 返回 bid/ask 的价与量（买一~买五、卖一~卖五）。
委比 = (买量 - 卖量) / (买量 + 卖量)，常用来看短时买卖盘力量。
"""
from alphafeed import AlphaFeed

af = AlphaFeed()
b = af.depth.get("600519.SH")

print(f"{'档':>4} {'买价':>10} {'买量':>8}    {'卖价':>10} {'卖量':>8}")
for i in range(5):
    print(f"{i+1:>4} {b['bid_prices'][i]:>10} {b['bid_volumes'][i]:>8}    "
          f"{b['ask_prices'][i]:>10} {b['ask_volumes'][i]:>8}")

bid_vol, ask_vol = sum(b["bid_volumes"]), sum(b["ask_volumes"])
wb = (bid_vol - ask_vol) / (bid_vol + ask_vol) if (bid_vol + ask_vol) else 0
print(f"\n委比: {wb*100:.1f}%  委差: {bid_vol - ask_vol}")
