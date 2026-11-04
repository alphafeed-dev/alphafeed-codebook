"""不装 TA-Lib，用 pandas 算 MACD / RSI / 布林带。

TA-Lib 安装麻烦；这些指标几行 pandas 就够准，也方便你改参数。
输入：AlphaFeed 前复权日线。
"""
import pandas as pd
from alphafeed import AlphaFeed

af = AlphaFeed()
df = af.klines.get("600519.SH", period="1d", count=250, adjust="forward", to_dataframe=True)
close = df["close"].astype(float)

# MACD(12,26,9)
ema12, ema26 = close.ewm(span=12).mean(), close.ewm(span=26).mean()
dif = ema12 - ema26
dea = dif.ewm(span=9).mean()
macd = (dif - dea) * 2

# RSI(14)
delta = close.diff()
gain = delta.clip(lower=0).rolling(14).mean()
loss = (-delta.clip(upper=0)).rolling(14).mean()
rsi = 100 - 100 / (1 + gain / loss)

# 布林带(20,2)
ma20 = close.rolling(20).mean()
std20 = close.rolling(20).std()
upper, lower = ma20 + 2 * std20, ma20 - 2 * std20

out = pd.DataFrame({"close": close, "DIF": dif, "DEA": dea, "MACD": macd,
                    "RSI14": rsi, "BOLL_up": upper, "BOLL_low": lower}).round(2)
print(out.tail(5).to_string())
