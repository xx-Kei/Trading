def run_backtest(df, cost, slippage, investment):
    df["Return"] = df["Close"].pct_change()

    df["Strategy"] = df["Signal"].shift(1) * df["Return"]
    df["Trade"] = df["Signal"].diff().abs()

    df["Strategy_real"] =df["Strategy"] - df["Trade"] * (cost + slippage)
    df["Cumulative"] = df["Cumulative"] = (1 + df["Strategy_real"]).cumprod() * investment

    return df