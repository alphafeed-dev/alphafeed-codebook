"""从 AkShare 迁到 AlphaFeed：常用调用对照。

AkShare 免费、覆盖广，但抓网页源、字段中文且不统一、实时易断。
迁移时把「中文列 + 不稳定实时」换成「统一英文列 + 稳定接口」。

历史日线：
  # AkShare
  # import akshare as ak
  # df = ak.stock_zh_a_hist(symbol='600519', period='daily', adjust='qfq')
  # 列是中文：日期/开盘/收盘/最高/最低/成交量...

  # AlphaFeed —— 统一英文列、复权参数对齐
"""
from alphafeed import AlphaFeed

af = AlphaFeed()
df = af.klines.get("600519.SH", period="1d", count=20, adjust="forward", to_dataframe=True)
print("统一英文列:", list(df.columns))

# 实时快照：
#   AkShare  ak.stock_zh_a_spot_em()      # 全A，但依赖东财网页，偶发断/延迟
#   AlphaFeed af.quotes.get(universes="CN_Stock", to_dataframe=True)
# 复权口径对照： qfq->forward, hfq->backward, 不复权->none
