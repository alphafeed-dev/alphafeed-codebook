"""每日复盘数据块：本地算好涨跌家数/成交额榜，交给 LLM 写成人话。

统计全在本地做（可复现、不幻觉），LLM 只负责把结构化事实写成复盘段落。
"""
from alphafeed import AlphaFeed

af = AlphaFeed()
df = af.quotes.get(universes="CN_Stock", to_dataframe=True)
pct = df["ext.change_pct"]

recap = {
    "date": df["trade_date"].mode().iloc[0],
    "count": int(len(df)),
    "up": int((pct > 0).sum()),
    "down": int((pct < 0).sum()),
    "limit_up_approx": int((pct >= 0.098).sum()),
    "amount_top": df.sort_values("amount", ascending=False)
                    .head(5)[["ext.name", "amount"]].to_dict("records"),
}
print("喂给 LLM 的结构化复盘事实:")
print(recap)
# prompt = f"根据以下盘后统计写一段中性复盘(禁止编造消息面):\n{recap}"
