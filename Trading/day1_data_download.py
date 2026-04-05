import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import numpy as np

from src.strategy import moving_average_strategy
from src.backtest import run_backtest
from src.metrics import calculate_metrics

tickers = {
    1: "AIR.NZ",   # Air New Zealand NZX
    2: "AAPL",     # Apple 
    3: "TSLA",     # Tesla 
    4: "^GSPC",    # SP500
    5: "MSTR",     # Micro
    6: "LLY",      # Eli Lily
    7: "INTC",     # Intel
}

choice = 4
start = "2024-01-01"
end   = "2026-04-02"

df_base = yf.download(tickers[choice], start=start, end=end)[["Close"]]

investment = 500

strategies = []
for short in range(5, 51, 5):
    for long in range(10, 201, 10):
        if short >= long: 
            continue
        else:
            strategies.append((short, long))

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
   
def generate_brief_report(metrics_df):
    top_name = metrics_df.index[0]
    bottom_name = metrics_df.index[-1]
    
    top_row = metrics_df.iloc[0]
    bottom_row = metrics_df.iloc[-1]

    report = (
        f"Best Strategy: {top_name} \n"
        f"Worst Strategy: {bottom_name}."
    )
    
    return report

report_text = generate_brief_report(output_sorted)
print(report_text)

plt.figure(figsize=(12, 8))
plt.plot(df["Close"], label="Price")
plt.title(f"{name} - Price & Moving Averages")
plt.legend()

initial = investment

short_vals = sorted({int(name.split("/")[0].replace("MA", "")) for name in results})
long_vals  = sorted({int(name.split("/")[1]) for name in results})

heatmap = np.full((len(short_vals), len(long_vals)), np.nan)

for i, s in enumerate(short_vals):
    for j, l in enumerate(long_vals):
        key = f"MA{s}/{l}"
        if key in output.index:
            heatmap[i, j] = output.loc[key, "return"] / initial

plt.figure(figsize=(12, 8))
img = plt.imshow(heatmap, aspect='auto', cmap='RdYlGn')

plt.xticks(ticks=np.arange(len(long_vals)), labels=long_vals, rotation=45)
plt.yticks(ticks=np.arange(len(short_vals)), labels=short_vals)

plt.xlabel("Long")
plt.ylabel("Short")
plt.title("MA Strategy Heatmap (Return)")

cbar = plt.colorbar(img)
cbar.ax.set_ylabel("ROI multiplier")

plt.tight_layout()


short_vals = sorted({int(name.split("/")[0].replace("MA", "")) for name in results})
long_vals  = sorted({int(name.split("/")[1]) for name in results})

heatmap_sharpe = np.full((len(short_vals), len(long_vals)), np.nan)

for i, s in enumerate(short_vals):
    for j, l in enumerate(long_vals):
        key = f"MA{s}/{l}"
        if key in output.index:
            heatmap_sharpe[i, j] = output.loc[key, "sharpe"]

plt.figure(figsize=(12, 8))
img = plt.imshow(heatmap_sharpe, aspect='auto', cmap='RdYlGn')

plt.xticks(ticks=np.arange(len(long_vals)), labels=long_vals, rotation=45)
plt.yticks(ticks=np.arange(len(short_vals)), labels=short_vals)

plt.xlabel("Long")
plt.ylabel("Short")
plt.title("MA Strategy Heatmap (Sharpe)")

cbar = plt.colorbar(img)
cbar.ax.set_ylabel("Sharpe Ratio")

plt.tight_layout()
plt.show()