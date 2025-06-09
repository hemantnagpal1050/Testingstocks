import yfinance as yf
import pandas as pd
import ta

def check_conditions(ticker):
    df = yf.download(ticker, period='45d', interval='1d', auto_adjust=False)
    if df.empty or len(df) < 20:
        return []

    df['Vol_5d_avg'] = df['Volume'].rolling(5).mean().shift(1)
    df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
    df['Prev_Close'] = df['Close'].shift(1)

    # Filter where all conditions are met
    condition = (
        (df['Volume'] >= 5 * df['Vol_5d_avg']) &
        (df['Close'] > df['Prev_Close']) &
        (df['RSI'] < 70)
    )

    matched_days = df.loc[condition]
    return matched_days.index.strftime('%Y-%m-%d').tolist()
