"""同一个接口，要 DataFrame 还是原始 list[dict]。

做研究用 DataFrame 方便；塞进别的服务里、或不想装 pandas 时，用原始结构更轻。
"""
from alphafeed import AlphaFeed

af = AlphaFeed()

# to_dataframe=True -> pandas.DataFrame
df = af.klines.get("000001.SZ", period="1d", count=5, adjust="forward", to_dataframe=True)
print(type(df).__name__)
print(df)

# 默认 -> 原始记录，列名和 DataFrame 一致
raw = af.klines.get("000001.SZ", period="1d", count=5, adjust="forward")
print(type(raw).__name__, "len=", len(raw))
print(raw[-1])
