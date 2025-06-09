import yfinance as yf
import pandas as pd

def analyze_stocks(tickers):
    results = []

    for ticker in tickers:
        try:
            df = yf.download(ticker, period='9wk', interval='1wk', auto_adjust=False)
            
            if df.empty or len(df) < 8:
                print(f"{ticker}: Not enough data or empty DataFrame")
                continue
            
            if df[['Volume', 'Close']].isnull().any().any():
                print(f"{ticker}: Skipped due to NaN values")
                continue
            
            last_week_volume = df['Volume'].iloc[-1]
            prev_7_weeks_volume_avg = df['Volume'].iloc[-8:-1].mean()
            
            latest_close = df['Close'].iloc[-1]
            prev_close = df['Close'].iloc[-2]
            
            volume_condition = last_week_volume >= 5 * prev_7_weeks_volume_avg
            price_condition = latest_close > prev_close

            if volume_condition and price_condition:
                results.append(ticker)
                print(f"{ticker}: Passed ✅ (Vol: {last_week_volume}, AvgVol: {prev_7_weeks_volume_avg}, Close: {latest_close} > {prev_close})")
            else:
                print(f"{ticker}: Failed ❌")

        except Exception as e:
            print(f"{ticker}: Error - {e}")

    return results


# List of 100 Nifty stocks (or any others of your interest)
tickers = [
    'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'LT.NS', 'KOTAKBANK.NS', 'SBIN.NS', 'AXISBANK.NS', 'ITC.NS',
    'HINDUNILVR.NS', 'BAJFINANCE.NS', 'BHARTIARTL.NS', 'HCLTECH.NS', 'WIPRO.NS', 'SUNPHARMA.NS', 'TITAN.NS', 'MARUTI.NS', 'ASIANPAINT.NS', 'ULTRACEMCO.NS',
    'POWERGRID.NS', 'NTPC.NS', 'ONGC.NS', 'JSWSTEEL.NS', 'TATASTEEL.NS', 'TECHM.NS', 'ADANIENT.NS', 'ADANIPORTS.NS', 'COALINDIA.NS', 'GRASIM.NS',
    'NESTLEIND.NS', 'BAJAJ-AUTO.NS', 'EICHERMOT.NS', 'M&M.NS', 'HEROMOTOCO.NS', 'DRREDDY.NS', 'CIPLA.NS', 'DIVISLAB.NS', 'BRITANNIA.NS', 'BPCL.NS',
    'IOC.NS', 'HINDPETRO.NS', 'SHREECEM.NS', 'DABUR.NS', 'GODREJCP.NS', 'PIDILITIND.NS', 'DMART.NS', 'HAVELLS.NS', 'UBL.NS', 'TORNTPHARM.NS',
    'INDUSINDBK.NS', 'PNB.NS', 'BANKBARODA.NS', 'FEDERALBNK.NS', 'CANBK.NS', 'IDFCFIRSTB.NS', 'AUROPHARMA.NS', 'BIOCON.NS', 'LUPIN.NS', 'ABBOTINDIA.NS',
    'ICICIPRULI.NS', 'HDFCLIFE.NS', 'SBILIFE.NS', 'BAJAJFINSV.NS', 'CHOLAFIN.NS', 'MUTHOOTFIN.NS', 'LICHSGFIN.NS', 'HDFCAMC.NS', 'ICICIGI.NS', 'MFSL.NS',
    'BEL.NS', 'BHEL.NS', 'IRCTC.NS', 'IRFC.NS', 'NHPC.NS', 'GAIL.NS', 'TATAPOWER.NS', 'ADANIGREEN.NS', 'ADANITRANS.NS', 'RECLTD.NS',
    'SRF.NS', 'VOLTAS.NS', 'WHIRLPOOL.NS', 'TVSMOTOR.NS', 'PAGEIND.NS', 'TRENT.NS', 'CONCOR.NS', 'ZOMATO.NS', 'PAYTM.NS', 'POLYCAB.NS',
    'LTTS.NS', 'LTI.NS', 'NAUKRI.NS', 'COFORGE.NS', 'PERSISTENT.NS', 'MPHASIS.NS', 'TATAELXSI.NS', 'RVNL.NS', 'IRCON.NS', 'HAL.NS'
]

qualified_stocks = analyze_stocks(tickers)

print("\n✅ Final List: Stocks where last week's volume is 5× avg of previous 7 weeks and latest close is positive:")
print(qualified_stocks)
