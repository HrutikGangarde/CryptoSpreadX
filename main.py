
# main.py
import os
import time
from datetime import datetime
from utils.api import get_binance_price, get_coinbase_price
from utils.calc import detect_arbitrage, append_price_row

# ---------- CONFIG ----------
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


CSV_PATH = "data/prices.csv"
SLEEP = 15             # seconds between polls (increase if you hit rate limits)
THRESHOLD_PCT = 0.25   # percent spread to consider 'arbitrage' — tune this
# ---------------------------

def snapshot_prices():
    b = {}
    c = {}
    for s in SYMBOLS:
        try:
            b[s] = get_binance_price(BINANCE_MAP[s])
        except Exception:
            b[s] = None
        try:
            c[s] = get_coinbase_price(COINBASE_MAP[s])
        except Exception:
            c[s] = None
    return b, c

def build_row(b_prices, c_prices):
    row = {"timestamp": datetime.utcnow().isoformat()}
    for s in SYMBOLS:
        row[f"{s}_binance"] = b_prices.get(s)
        row[f"{s}_coinbase"] = c_prices.get(s)
    return row

def pretty_print(b_prices, c_prices):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    for s in SYMBOLS:
        b = b_prices.get(s)
        c = c_prices.get(s)
        arb, pct = detect_arbitrage(b, c, THRESHOLD_PCT)
        if pct is None:
            print(f"[{now}] {s}: data missing (binance={b}, coinbase={c})")
        else:
            status = "🚨 ARB" if arb else "ok"
            print(f"[{now}] {s}: Binance={b:.2f} Coinbase={c:.2f} Spread={abs(b-c):.2f} ({pct:.3f}%) -> {status}")

def ensure_data_folder():
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)

def main():
    ensure_data_folder()
    print("CryptoSpreadX tracker started. Press Ctrl+C to stop.")
    try:
        while True:
            b_prices, c_prices = snapshot_prices()
            row = build_row(b_prices, c_prices)
            append_price_row(row, CSV_PATH)
            pretty_print(b_prices, c_prices)
            time.sleep(SLEEP)
    except KeyboardInterrupt:
        print("Stopped by user. Exiting.")

if __name__ == "__main__":
    main()
