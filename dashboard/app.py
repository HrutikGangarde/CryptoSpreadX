# dashboard/app.py
import streamlit as st
import os
import matplotlib.pyplot as plt
import seaborn as sns

from utils.api import get_binance_price, get_coinbase_price
from utils.calc import load_and_correlate

st.set_page_config(page_title="CryptoSpreadX", layout="wide")
st.title("CryptoSpreadX 🚀 — Real-time Arb & Correlation")

CSV_PATH = "data/prices.csv"
SYMBOLS = ['BTC', 'ETH', 'SOL', 'DOGE', 'PEPE', 'XRP', 'AVAX', 'GALA', 'DOT', 'SHIB']
BINANCE_MAP = {
    'BTC':'BTCUSDT','ETH':'ETHUSDT','SOL':'SOLUSDT',
    'DOGE':'DOGEUSDT','PEPE':'PEPEUSDT','XRP':'XRPUSDT',
    'AVAX':'AVAXUSDT','GALA':'GALAUSDT','DOT':'DOTUSDT','SHIB':'SHIBUSDT'
}
COINBASE_MAP = {
    'BTC':'BTC-USD','ETH':'ETH-USD','SOL':'SOL-USD',
    'DOGE':'DOGE-USD','PEPE':'PEPE-USD','XRP':'XRP-USD',
    'AVAX':'AVAX-USD','GALA':'GALA-USD','DOT':'DOT-USD','SHIB':'SHIB-USD'
}


st.sidebar.header("Controls")
exchange = st.sidebar.selectbox("Correlation data source", ["binance","coinbase"])

# Current prices + spreads area
st.subheader("Live prices (spot)")
cols = st.columns(len(SYMBOLS))
for i, s in enumerate(SYMBOLS):
    b = get_binance_price(BINANCE_MAP[s])
    c = get_coinbase_price(COINBASE_MAP[s])
    with cols[i]:
        st.metric(label=f"{s} Binance", value=f"{b:.2f}" if b else "n/a")
        st.metric(label=f"{s} Coinbase", value=f"{c:.2f}" if c else "n/a")
        if b and c:
            spread = abs(b-c)
            pct = abs(b-c)/((b+c)/2)*100
            st.write(f"Spread: {spread:.2f} ({pct:.3f}%)")

st.markdown("---")
st.subheader("Correlation heatmap (log returns)")
if os.path.exists(CSV_PATH):
    try:
        corr = load_and_correlate(CSV_PATH, exchange=exchange)
        fig, ax = plt.subplots(figsize=(6,6))
        sns.heatmap(corr, annot=True, ax=ax, cmap="coolwarm")
        st.pyplot(fig)
    except Exception as e:
        st.error(str(e))
else:
    st.info("No historical data yet. Run `python main.py` to start logging prices to data/prices.csv.")
