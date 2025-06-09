import yfinance as yf
import pandas as pd
import ta  # pip install ta

# Replace with full list of Nifty Midcap 100 tickers
midcap100 = [
    :contentReference[oaicite:9]{index=9}
    :contentReference[oaicite:10]{index=10}
    :contentReference[oaicite:11]{index=11}
]

:contentReference[oaicite:12]{index=12}
    :contentReference[oaicite:13]{index=13}
    :contentReference[oaicite:14]{index=14}
        return []

    df['Vol_5d_avg'] = df['Volume'].rolling(5).mean().shift(1)
    df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()

    alerts = []
    for idx in range(5, len(df)):
        today, yesterday = df.iloc[idx], df.iloc[idx - 1]
        # Condition checks
        if (
            today['Volume'] >= 5 * today['Vol_5d_avg']
            and today['Close'] > yesterday['Close']
            and today['RSI'] < 70
        ):
            date_str = today.name.strftime('%Y-%m-%d')
            alerts.append(date_str)
    return alerts

# Run check for each ticker
:contentReference[oaicite:15]{index=15}
    :contentReference[oaicite:16]{index=16}
    if dates:
        :contentReference[oaicite:17]{index=17}
