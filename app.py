import yfinance as yf
import pandas as pd
import ta

def analyze_stock(ticker):
    df = yf.download(ticker, period='45d', interval='1d', auto_adjust=False)
    if df.empty or len(df) < 20:
        return []

    df['Vol_5d_avg'] = df['Volume'].rolling(window=5).mean().shift(1)
    df['Prev_Close'] = df['Close'].shift(1)
    df['RSI'] = ta.momentum.RSIIndicator(close=df['Close'], window=14).rsi()

    alerts = []

    for i in range(14, len(df)):  # Skip first few rows with NaN RSI
        row = df.iloc[i]
        if (
            pd.notna(row['Vol_5d_avg']) and
            pd.notna(row['Prev_Close']) and
            pd.notna(row['RSI']) and
            row['Volume'] >= 5 * row['Vol_5d_avg'] and
            row['Close'] > row['Prev_Close'] and
            row['RSI'] < 70
        ):
            alerts.append(df.index[i].strftime('%Y-%m-%d'))

    return alerts

