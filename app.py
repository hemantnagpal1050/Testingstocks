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

    try:
        price_change = (recent_price - previous_price) / previous_price * 100
    except ZeroDivisionError:
        return False

    is_volume_spike = float(recent_volume) >= 2 * float(avg_volume)
    is_price_spike = float(price_change) > 2

    return is_volume_spike and is_price_spike

st.title("📈 Volume + Price Action Stock Alert")

stock_input = st.text_area(
    "Enter up to 100 stock symbols (comma separated):",
    "ACC.NS, ABCAPITAL.NS, ABFRL.NS, ALKEM.NS, APLAPOLLO.NS, APOLLOTYRE.NS, ASHOKLEY.NS, BALKRISIND.NS, BHARATFORG.NS, EXIDEIND.NS, COLPAL.NS, CGPOWER.NS, NLCINDIA.NS, BANKINDIA.NS, DELHIVERY.NS, LICHSGFIN.NS, POLYCAB.NS, COCHINSHIP.NS, MAHINDCIE.NS, IDFCFIRSTB.NS, INDHOTEL.NS, CROMPTON.NS, AUBANK.NS, AIAENG.NS, ENGINERSIN.NS, TV18BRDCST.NS, ADANIPOWER.NS, PAGEIND.NS, ICICIGI.NS, CANBK.NS, ARVIND.NS, JINDALSAW.NS, M&MFIN.NS, TORNTPOWER.NS, CENTRALBK.NS, VOLTAS.NS, NATIONALUM.NS, CHOLAFIN.NS, TATAPOWER.NS, JUBLFOOD.NS, MANAPPURAM.NS, RPOWER.NS, IRB.NS, MPHASIS.NS, CESC.NS, WHIRLPOOL.NS, BHEL.NS, UBL.NS, SANOFI.NS, INDIAMART.NS, GSPL.NS, ASTRAL.NS, CUMMINSIND.NS, GUJGASLTD.NS
)
