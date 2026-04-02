import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd

from src.strategy import moving_average_strategy
from src.backtest import run_backtest
from src.metrics import calculate_metrics

tickers = {
    1: "AIR.NZ",   # Air New Zealand NZX
    3: "AAPL",     # Apple 
    4: "TSLA",      # Tesla 
    4: "WBC.NZ",   # Westpace NZ
    5: "FCG.NZ",   # Fonterra NZ
    6: "^GSPC"  #SP500
}

choice = 6
start = "2020-01-01"
end = "2025-01-01"

df_base = yf.download(tickers[choice], start=start, end=end)[["Close"]]

investment = 500

strategies = [
    (5, 10),
    (10, 20),
    (20, 50),
    (50, 200)
]


results = {}

all_metrics = {}
for short, long in strategies:
    df = df_base.copy()

    df = moving_average_strategy(df, short, long)
    df = run_backtest(df, cost = 0.001, slippage = 0.0005, investment = investment)

    name = f"MA{short}/{long}"
    results[name] = df
    
    metrics = calculate_metrics(df, short, long)
    all_metrics.update(metrics)
output = pd.DataFrame.from_dict(all_metrics, orient='index')
output = output.rename(columns={
    "Total Return": "return",
    "Sharpe Ratio": "sharpe",
    "Max Drawdown": "drawdown"
})
output_sorted = output.sort_values(by="return", ascending=False)
print(output_sorted)
   
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