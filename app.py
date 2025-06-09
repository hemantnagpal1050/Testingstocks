import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

def is_close_to_high(stock_name, days=30, threshold=0.02):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=days * 2)

    df = yf.download(stock_name, start=start_date, end=end_date)
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    df = df[['Close']].dropna()
    df = df[-days:]

    if len(df) < 2:
        return False

    recent_high = df['Close'].max()
    last_two_closes = df['Close'].iloc[-2:]

    for price in last_two_closes:
        if (recent_high - price) / recent_high > threshold:
            return False
    return True


st.title("📊 Filter Stocks Close to Recent High")

stock_input = st.text_area(
    "Enter up to 100 stock symbols (comma separated):",
    "ACC.NS, ABCAPITAL.NS, ABFRL.NS, ALKEM.NS, APLAPOLLO.NS, APOLLOTYRE.NS, ASHOKLEY.NS, BALKRISIND.NS, BHARATFORG.NS, EXIDEIND.NS, COLPAL.NS, CGPOWER.NS, NLCINDIA.NS, BANKINDIA.NS, DELHIVERY.NS, LICHSGFIN.NS, POLYCAB.NS, COCHINSHIP.NS, MAHINDCIE.NS, IDFCFIRSTB.NS, INDHOTEL.NS, CROMPTON.NS, AUBANK.NS, AIAENG.NS, ENGINERSIN.NS, TV18BRDCST.NS, ADANIPOWER.NS, PAGEIND.NS, ICICIGI.NS, CANBK.NS, ARVIND.NS, JINDALSAW.NS, M&MFIN.NS, TORNTPOWER.NS, CENTRALBK.NS, VOLTAS.NS, NATIONALUM.NS, CHOLAFIN.NS, TATAPOWER.NS, JUBLFOOD.NS, MANAPPURAM.NS, RPOWER.NS, IRB.NS, MPHASIS.NS, CESC.NS, WHIRLPOOL.NS, BHEL.NS, UBL.NS, SANOFI.NS, INDIAMART.NS, GSPL.NS, ASTRAL.NS, CUMMINSIND.NS, GUJGASLTD.NS, IEX.NS, IOB.NS, JKCEMENT.NS, LODHA.NS, NAM-INDIA.NS, OBEROIRLTY.NS, PFIZER.NS, PERSISTENT.NS, RAIN.NS, RCF.NS, SCHAEFFLER.NS, SUNTV.NS, SUPRAJIT.NS, TRENT.NS, UNIONBANK.NS, VGUARD.NS, VSTIND.NS, ZEEL.NS, UCOBANK.NS, INDIGOPNTS.NS, IRCON.NS, NBCC.NS, NHPC.NS, SJVN.NS, HUDCO.NS, ITI.NS, EIHOTEL.NS, FINCABLES.NS, IDFC.NS, JMFINANCIL.NS, KEC.NS, KRBL.NS, NAVINFLUOR.NS, NBVENTURES.NS, NOCIL.NS, PGHH.NS, RADICO.NS, RITES.NS, SAREGAMA.NS, SKFINDIA.NS, SPARC.NS, TATAELXSI.NS, TEAMLEASE.NS, VAKRANGEE.NS"
)

threshold = st.slider("Threshold % below recent high", min_value=0.0, max_value=10.0, value=2.0, step=0.1)

if st.button("Filter Stocks"):
    stock_list = [s.strip().upper() for s in stock_input.split(",") if s.strip()]
    alerts = []
    progress = st.progress(0)

    for i, stock in enumerate(stock_list):
        try:
            if is_close_to_high(stock, threshold=threshold / 100):
                alerts.append(stock)
        except Exception as e:
            st.warning(f"{stock}: Error - {e}")
        progress.progress((i + 1) / len(stock_list))

    if alerts:
        st.success("Stocks with last 2 days close to recent high:")
        st.write(alerts)
    else:
        st.info("No stocks matched the condition.")



