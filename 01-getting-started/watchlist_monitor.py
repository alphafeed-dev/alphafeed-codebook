"""盯一个自选股清单：批量快照，打印最新价和涨跌幅。

放进循环(加 time.sleep)就是个最简盯盘器。快照不占多少额度。
"""
from alphafeed import AlphaFeed

af = AlphaFeed()
watchlist = ["600519.SH", "000858.SZ", "300750.SZ", "00700.HK"]

quotes = af.quotes.get(symbols=",".join(watchlist))
for q in quotes:
    name = q.get("ext", {}).get("name", "")
    pct = q.get("ext", {}).get("change_pct", 0) * 100
    print(f"{q['symbol']:<12}{name:<8}{q['last_price']:>10}  {pct:+.2f}%")
