"""从 Baostock 迁到 AlphaFeed：常用调用对照。

Baostock 免费稳、但要 login/logout、返回字符串、无实时、无盘口、A股为主。
迁移动机通常是：要实时 / 五档 / 港美股 / 免去 login 样板。

Baostock 取日线(参考)：
  # import baostock as bs
  # bs.login()
  # rs = bs.query_history_k_data_plus("sh.600519","date,open,high,low,close,volume",
  #        start_date='2026-01-01', frequency="d", adjustflag="2")
  # ... 自己 while rs.next() 拼 DataFrame，字段是字符串要转数值
  # bs.logout()

AlphaFeed —— 无需 login，直接取，数值类型就位：
"""
from alphafeed import AlphaFeed

af = AlphaFeed()
df = af.klines.get("600519.SH", period="1d", count=20, adjust="forward", to_dataframe=True)
print("无需 login，直接拿到数值型 DataFrame:")
print(df.dtypes[["open", "close", "volume"]].to_string())

# 代码格式对照： Baostock 'sh.600519' / 'sz.000001'  -> AlphaFeed '600519.SH' / '000001.SZ'
# adjustflag: '1'后复权 '2'前复权 '3'不复权 -> AlphaFeed backward / forward / none
