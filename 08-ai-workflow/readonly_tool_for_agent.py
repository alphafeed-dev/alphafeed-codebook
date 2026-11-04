"""给 Agent 的只读数据工具：清晰 schema + 紧凑返回 + 只读边界。

把行情能力包成函数给 agent/function-calling 用。要点：
  - 参数和返回有明确结构，省得模型瞎猜；
  - 只读（不下单、不写文件），边界清楚；
  - 返回裁剪过的紧凑结果，省 token。
这就是 MCP/工具封装的通用模式（非官方组件）。
"""
from alphafeed import AlphaFeed

af = AlphaFeed()


def get_recent_bars(symbol: str, days: int = 20) -> dict:
    """取最近 N 根前复权日线的紧凑结果。agent 可直接调用。

    Args:
        symbol: 如 "600519.SH" / "AAPL.US"
        days: 根数，默认 20
    Returns:
        {symbol, last_close, bars:[{d,c}...]} —— 只含必要字段
    """
    df = af.klines.get(symbol, period="1d", count=days, adjust="forward", to_dataframe=True)
    return {
        "symbol": symbol,
        "last_close": round(float(df["close"].iloc[-1]), 2),
        "bars": [{"d": d, "c": round(float(c), 2)}
                 for d, c in zip(df["trade_date"], df["close"])],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(get_recent_bars("600519.SH", 5), ensure_ascii=False, indent=2))
