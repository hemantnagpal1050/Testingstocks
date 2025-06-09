import yfinance as yf
import pandas as pd

def analyze_stocks(tickers):
    results = []

    for ticker in tickers:
        try:
            # Download 8 weeks of data (we need last week + previous 7 weeks)
            # Use '1wk' interval to get weekly data
            df = yf.download(ticker, period='9wk', interval='1wk', auto_adjust=False)
            
            # Check if we have enough data
            if len(df) < 8:
                print(f"{ticker}: Not enough data")
                continue
            
            # Calculate total volume for last week (most recent row)
            last_week_volume = df['Volume'].iloc[-]()
