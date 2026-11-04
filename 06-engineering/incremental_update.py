"""增量更新本地库：只补新交易日，不重拉全量。

思路：库里查该票最后一个 trade_date -> 从它之后取 -> upsert。
用 symbol+trade_date 唯一键去重，跑多少遍结果都一致（幂等）。
"""
import sqlite3
from pathlib import Path
from alphafeed import AlphaFeed

af = AlphaFeed()
Path("data").mkdir(exist_ok=True)
con = sqlite3.connect("data/quotes.db")
con.execute("""CREATE TABLE IF NOT EXISTS klines(
    symbol TEXT, trade_date TEXT, open REAL, high REAL, low REAL, close REAL,
    volume REAL, amount REAL, PRIMARY KEY(symbol, trade_date))""")

sym = "600519.SH"
last = con.execute("SELECT MAX(trade_date) FROM klines WHERE symbol=?", (sym,)).fetchone()[0]
print("库内最后日期:", last)

df = af.klines.get(sym, period="1d", count=30, adjust="forward", to_dataframe=True)
new = df if last is None else df[df["trade_date"] > last]
print("需补:", len(new), "行")

cols = ["symbol", "trade_date", "open", "high", "low", "close", "volume", "amount"]
con.executemany(
    f"INSERT OR REPLACE INTO klines({','.join(cols)}) VALUES ({','.join('?'*len(cols))})",
    new[cols].itertuples(index=False, name=None))
con.commit()
print("库内总行:", con.execute("SELECT COUNT(*) FROM klines WHERE symbol=?", (sym,)).fetchone()[0])
con.close()
