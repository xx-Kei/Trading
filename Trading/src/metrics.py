def calculate_metrics(df, short, long):
    total_return = df["Cumulative"].iloc[-1] - 1

    sharpe = (
        df["Strategy_real"].mean() /
        df["Strategy_real"].std()
    ) * (252 ** 0.5)

    cum = df["Cumulative"]
    peak = cum.cummax()
    drawdown = (cum - peak) / peak
    max_drawdown = drawdown.min()
    strategy_name = f"MA{short}/{long}"

    return {strategy_name: {
        "Total Return": round(total_return, 2),
        "Sharpe Ratio": round(sharpe, 3),
        "Max Drawdown": round(max_drawdown, 3)
    }}