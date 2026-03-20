import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

investment = 500
window1 = 50
window2 = 200
df = yf.download("AAPL", start="2020-01-01", end="2023-01-01")
df = df[["Close"]]

df["Return"] = df["Close"].pct_change()
df["MA5"] = df["Close"].rolling(window=window1).mean()
df["MA10"] = df["Close"].rolling(window=window2).mean()

df["Signal"] = 0
df.loc[df["MA5"] > df["MA10"], "Signal"] = 1
df["Signal"] = df["Signal"].shift(1)

df.dropna(inplace=True)

df["Strategy"] = df["Signal"] * df["Return"]
df["Cumulative"] = (1 + df["Strategy"]).cumprod() * investment

plt.figure(figsize=(12,5))
plt.plot(df["Close"], label="Price")
plt.plot(df["MA5"], label="MA5")
plt.plot(df["MA10"], label="MA10")
plt.legend()
plt.show()

plt.figure(figsize=(12,5))
plt.plot(df["Cumulative"], label="Cumulative Strategy")
plt.legend()
plt.show()