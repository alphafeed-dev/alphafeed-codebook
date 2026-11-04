"""确认装的 SDK 版本，和能不能连上。"""
from alphafeed import AlphaFeed, __version__

print("alphafeed", __version__)
af = AlphaFeed()
print("base_url:", af.base_url)
print("连通性自检:", af.quotes.get(symbols="600519.SH")[0]["last_price"])
