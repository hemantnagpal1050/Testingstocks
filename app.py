import yfinance as yf
import pandas as pd

def analyze_stocks(tickers):
    results = []

    for ticker in tickers:
        try:
            df = yf.download(ticker, period='9wk', interval='1wk', auto_adjust=False)
            if len(df) < 8:
                print(f"{ticker}: Not enough data")
                continue
            
            last_week_volume = df['Volume'].iloc[-1]
            prev_7_weeks_volume_avg = df['Volume'].iloc[-8:-1].mean()
            
            latest_close = df['Close'].iloc[-1]
            prev_close = df['Close'].iloc[-2]
            
            volume_condition = last_week_volume >= 5 * prev_7_weeks_volume_avg
            price_condition = latest_close > prev_close
            
            if volume_condition and price_condition:
                results.append(ticker)
                print(f"{ticker}: Passed (Last week volume = {last_week_volume}, Prev 7 weeks avg volume = {prev_7_weeks_volume_avg}, Close: {latest_close} > {prev_close})")
            else:
                print(f"{ticker}: Failed conditions")
        
        except Exception as e:
            print(f"{ticker}: Error - {e}")
tickers = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS']
qualified_stocks = analyze_stocks(tickers)
print("\nQualified stocks:")
print(qualified_stocks)
