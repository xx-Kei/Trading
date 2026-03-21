import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

investment = 500
window1 = 5
window2 = 10
cost = 0.001

# Download data
df = yf.download("AAPL", start="2020-01-01", end="2023-01-01")[["Close"]]

# Calculate returns and moving averages
df["Return"] = df["Close"].pct_change()
df["MA5"] = df["Close"].rolling(window=window1).mean()
df["MA10"] = df["Close"].rolling(window=window2).mean()

# Generate signals
df["Signal"] = 0
df.loc[df["MA5"] > df["MA10"], "Signal"] = 1
df["Signal"] = df["Signal"].shift(1)  # apply signal to next day

df.dropna(inplace=True)

# Calculate trades and strategy
df["Trade"] = df["Signal"].diff().abs()
df["Strategy"] = df["Signal"] * df["Return"]
df["Cumulative"] = (1 + df["Strategy"] - df["Trade"] * cost).cumprod() * investment
df["Strategy_after_cost"] = df["Strategy"] - df["Trade"] * cost
df["Cumulative_raw"] = (1+df["Strategy"]).cumprod()
df["Cumulative_cost"] = (1+df["Strategy_after_cost"]).cumprod()

# Plot price and moving averages
plt.figure(figsize=(12,5))
plt.plot(df["Close"], label="Price")
plt.plot(df["MA5"], label="MA5")
plt.plot(df["MA10"], label="MA10")
plt.legend()
plt.show()

# Plot cumulative strategy
plt.figure(figsize=(12,5))
plt.plot(df["Cumulative"], label="Cumulative Strategy")
plt.legend()
plt.show()

# Plot comparison with brokerage fees
plt.plot(df["Cumulative_raw"], label="No Cost")
plt.plot(df["Cumulative_cost"], label="With Cost")
plt.legend()
plt.show()