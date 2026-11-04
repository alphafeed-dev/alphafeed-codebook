"""限频/抖动的通用重试：指数退避，别写死循环猛打。

对任何接口调用包一层：失败等 0.5s、1s、2s... 最多几次，还不行就抛。
"""
import time
from alphafeed import AlphaFeed

af = AlphaFeed()

def with_retry(fn, tries=4, base=0.5):
    for i in range(tries):
        try:
            return fn()
        except Exception as e:  # noqa: BLE001
            if i == tries - 1:
                raise
            wait = base * (2 ** i)
            print(f"第{i+1}次失败({type(e).__name__})，{wait}s 后重试")
            time.sleep(wait)

df = with_retry(lambda: af.klines.get("600519.SH", period="1d", count=5,
                                      adjust="forward", to_dataframe=True))
print("取到", len(df), "根")
