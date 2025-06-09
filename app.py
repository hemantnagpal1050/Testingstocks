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

stock_input = st.text_area(
    "Enter up to 100 stock symbols (comma separated):",
    "ACC.NS, ABCAPITAL.NS, ABFRL.NS, ALKEM.NS, APLAPOLLO.NS, APOLLOTYRE.NS, ASHOKLEY.NS, BALKRISIND.NS, BHARATFORG.NS, EXIDEIND.NS, COLPAL.NS, CGPOWER.NS, NLCINDIA.NS, BANKINDIA.NS, DELHIVERY.NS, LICHSGFIN.NS, POLYCAB.NS, COCHINSHIP.NS, MAHINDCIE.NS, IDFCFIRSTB.NS, INDHOTEL.NS, CROMPTON.NS, AUBANK.NS, AIAENG.NS, ENGINERSIN.NS, TV18BRDCST.NS, ADANIPOWER.NS, PAGEIND.NS, ICICIGI.NS, CANBK.NS, ARVIND.NS, JINDALSAW.NS, M&MFIN.NS, TORNTPOWER.NS, CENTRALBK.NS, VOLTAS.NS, NATIONALUM.NS, CHOLAFIN.NS, TATAPOWER.NS, JUBLFOOD.NS, MANAPPURAM.NS, RPOWER.NS, IRB.NS, MPHASIS.NS, CESC.NS, WHIRLPOOL.NS, BHEL.NS, UBL.NS, SANOFI.NS, INDIAMART.NS, GSPL.NS, ASTRAL.NS, CUMMINSIND.NS, GUJGASLTD.NS, IEX.NS, IOB.NS, JKCEMENT.NS, LODHA.NS, NAM-INDIA.NS, OBEROIRLTY.NS, PFIZER.NS, PERSISTENT.NS, RAIN.NS, RCF.NS, SCHAEFFLER.NS, SUNTV.NS, SUPRAJIT.NS, TRENT.NS, UNIONBANK.NS, VGUARD.NS, VSTIND.NS, ZEEL.NS, UCOBANK.NS, INDIGOPNTS.NS, IRCON.NS, NBCC.NS, NHPC.NS, SJVN.NS, HUDCO.NS, ITI.NS, EIHOTEL.NS, FINCABLES.NS, IDFC.NS, JMFINANCIL.NS, KEC.NS, KRBL.NS, NAVINFLUOR.NS, NBVENTURES.NS, NOCIL.NS, PGHH.NS, RADICO.NS, RITES.NS, SAREGAMA.NS, SKFINDIA.NS, SPARC.NS, TATAELXSI.NS, TEAMLEASE.NS, VAKRANGEE.NS"
)


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
