import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

def fetch_stock_data(stock_name, days=30):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=days*2)
    df = yf.download(stock_name, start=start_date, end=end_date)
    df = df[['Close', 'Volume']].dropna()
    df = df[-days:]
    df['Stock'] = stock_name
    return df

def check_volume_price_action(stock_df):
    if len(stock_df) < 21:
        return False
    recent_volume = stock_df['Volume'].iloc[-1]
    avg_volume = stock_df['Volume'].iloc[-21:-1].mean()
    recent_price = stock_df['Close'].iloc[-1]
    previous_price = stock_df['Close'].iloc[-2]
    price_change = (recent_price - previous_price) / previous_price * 100
    return recent_volume >= 2 * avg_volume and price_change > 2

st.title("📈 Volume + Price Action Stock Alert")

stock_input = st.text_area("Enter up to 100 stock symbols (comma separated):", "RELIANCE.NS, TCS.NS, INFY.NS")

if st.button("Check Alerts"):
    stock_list = [s.strip().upper() for s in stock_input.split(',') if s.strip()]
    alerts = []
    progress = st.progress(0)

    for i, stock in enumerate(stock_list):
        try:
            df = fetch_stock_data(stock)
            if check_volume_price_action(df):
                alerts.append(stock)
        except Exception as e:
            st.warning(f"{stock}: Error - {e}")
        progress.progress((i + 1) / len(stock_list))

    if alerts:
        st.success("📢 Stocks triggering alert:")
        st.write(alerts)
    else:
        st.info("No stock matched the alert condition.")
