"""五档盘口：买一~买五 / 卖一~卖五。

算委比委差、封板金额、盘口压力用。免费网页源的盘口通常延迟高/缺档，这里是完整五档。
"""
from alphafeed import AlphaFeed

af = AlphaFeed()
book = af.depth.get("600519.SH")
print(book)
