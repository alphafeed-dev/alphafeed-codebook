"""从 Tushare 迁到 AlphaFeed：常用调用对照。

Tushare 要积分、按接口限频；换数据源时最烦的是字段口径和复权对不上。
下面左边是 Tushare 写法(参考，不执行)，右边是 AlphaFeed 等价写法(可跑)。

日线：
  # Tushare
  # import tushare as ts
  # pro = ts.pro_api(TOKEN)
  # df = pro.daily(ts_code='600519.SH', start_date='20260101', end_date='20260901')
  # 复权要另调 pro.adj_factor 自己乘，容易错

  # AlphaFeed —— 复权内置，5 种口径，列名统一英文
"""
from alphafeed import AlphaFeed

af = AlphaFeed()
df = af.klines.get("600519.SH", period="1d", count=20, adjust="forward", to_dataframe=True)
print(df[["trade_date", "open", "high", "low", "close", "volume", "amount"]].tail().to_string(index=False))

# 字段对照:
#   Tushare trade_date(YYYYMMDD)  -> AlphaFeed trade_date(YYYY-MM-DD)
#   Tushare vol(手) / amount(千元) -> AlphaFeed volume / amount (以官方口径为准)
#   Tushare 复权需 adj_factor 手算 -> AlphaFeed adjust="forward"/"backward" 直接给
