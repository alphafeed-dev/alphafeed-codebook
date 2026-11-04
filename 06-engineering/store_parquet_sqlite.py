"""把拉到的日线落地到 Parquet 和 SQLite，增量更新的底子。

研究用 Parquet（列存、省空间、读得快）；要 SQL 查就落 SQLite。
"""
import sqlite3
from pathlib import Path
from alphafeed import AlphaFeed

af = AlphaFeed()
out = Path("data"); out.mkdir(exist_ok=True)

df = af.klines.get("600519.SH", period="1d", count=250, adjust="forward", to_dataframe=True)

# Parquet
df.to_parquet(out / "600519_SH_1d.parquet", index=False)

# SQLite（按 symbol+trade_date 唯一，方便增量 upsert）
con = sqlite3.connect(out / "quotes.db")
df.to_sql("klines", con, if_exists="replace", index=False)
con.execute("CREATE INDEX IF NOT EXISTS ix_sym_date ON klines(symbol, trade_date)")
con.commit()
print("rows in sqlite:", con.execute("SELECT COUNT(*) FROM klines").fetchone()[0])
con.close()
print("已写 data/600519_SH_1d.parquet 与 data/quotes.db")
