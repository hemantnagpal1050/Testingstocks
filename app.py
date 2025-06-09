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
            last_week_volume = df['Volume'].iloc[-1]
            
            # Calculate average volume of previous 7 weeks
            prev_7_weeks_volume_avg = df['Volume'].iloc[-8:-1].mean()
            
            # Check latest close and previous close
            latest_close = df['Close'].iloc[-1]
            prev_close = df['Close'].iloc[-2]
            
            # Condition checks
            volume_condition = last_week_volume >= 5 * prev_7_weeks_volume_avg
            price_condition = latest_close > prev_close
            
            if volume_condition and price_condition:
                results.append(ticker)
                print(f"{ticker}: Passed (Last week volume = {last_week_volume}, Prev 7 weeks avg volume = {prev_7_weeks_volume_avg}, Close: {latest_close} > {prev_close})")
            else:
                print(f"{ticker}: Failed conditions")
        
        except Exception as e:
            print(f"{ticker}: Error - {e}")
    
    return results


# Example usage:
tickers = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS']  # Replace with your list of 100 stocks
qualified_stocks = analyze_stocks(tickers)
print("\nStocks where last week's volume is 5x avg of previous 7 weeks and latest close is positive:")
print(qualified_stocks)
