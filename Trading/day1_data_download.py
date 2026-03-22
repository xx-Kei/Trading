import matplotlib.pyplot as plt
import yfinance as yf

from src.strategy import moving_average_strategy
from src.backtest import run_backtest
from src.metrics import calculate_metrics


df_base = yf.download("SPY", start="2020-01-01", end="2025-01-01")[["Close"]]

investment = 500

strategies = [
    (5, 10),
    (10, 20),
    (20, 50),
    (50, 200)
]


results = {}

for short, long in strategies:
    df = df_base.copy()

    df = moving_average_strategy(df, short, long)
    df = run_backtest(df)

    name = f"MA{short}/{long}"
    results[name] = df

    metrics = calculate_metrics(df)
    print(f"\n{name}")
    for a, b in metrics.items():
        print(f"{a}: {b:.4f}")

for name, df in results.items():
    short, long = map(int, name.replace("MA", "").split("/"))
    
    plt.figure(figsize=(10, 5))
    plt.plot(df["Close"], label="Price")
    plt.plot(df["MA_short"], label=f"MA{short}")
    plt.plot(df["MA_long"], label=f"MA{long}")
    plt.title(f"{name} - Price & Moving Averages")
    plt.legend()
    
plt.figure(figsize=(12, 6))
for name, df in results.items():
    plt.plot(df["Cumulative"], label=name)

plt.title("Cumulative Returns for All Strategies")
plt.legend()
plt.show()