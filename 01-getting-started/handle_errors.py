"""几种常见错误怎么接：没设 key、代码写错、网络抖动。

别裸 except 吞掉——至少把类型和消息打出来，方便定位。
"""
import os
from alphafeed import AlphaFeed

if not os.environ.get("ALPHAFEED_API_KEY"):
    raise SystemExit("先设置 ALPHAFEED_API_KEY 再跑")

af = AlphaFeed()

for sym in ["600519.SH", "999999.SH"]:  # 第二个是无效代码
    try:
        df = af.klines.get(sym, period="1d", count=3, adjust="forward", to_dataframe=True)
        print(sym, "ok, 最新收盘:", df["close"].iloc[-1])
    except Exception as e:  # noqa: BLE001 — 示例里打出类型+消息即可
        print(sym, "失败:", type(e).__name__, str(e)[:120])
