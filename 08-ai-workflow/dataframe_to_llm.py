"""把行情 DataFrame 喂给 LLM 的正确姿势：数值本地算，模型只做解读。

关键点：别让模型「算」指标（会幻觉），本地算好、压成紧凑文本再喂，
prompt 里写死口径。下面用标准库拼 prompt，换成任意 LLM SDK 都行。
"""
from alphafeed import AlphaFeed

af = AlphaFeed()
df = af.klines.get("600519.SH", period="1d", count=60, adjust="forward", to_dataframe=True)
close = df["close"].astype(float)

facts = {
    "symbol": "600519.SH",
    "last_close": round(float(close.iloc[-1]), 2),
    "ret_20d": round(float(close.iloc[-1] / close.iloc[-21] - 1) * 100, 2),
    "ma20": round(float(close.tail(20).mean()), 2),
    "ma60": round(float(close.mean()), 2),
}
prompt = (
    "你是严谨的行情助手。只根据下面已算好的事实作答，不要自己重算或编造数字。\n"
    f"事实(JSON): {facts}\n"
    "请用两句话点评该股近期趋势与均线位置，不得给出投资建议。"
)
print(prompt)
# 然后: resp = your_llm_client.chat(prompt)   # OpenAI/Claude/Bedrock 均可
