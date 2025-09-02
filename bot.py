import asyncio
from utils.api import get_binance_price, get_coinbase_price
from telegram import Bot

# ===============================
# CONFIG — EDIT THESE
# ===============================
TELEGRAM_TOKEN = "8212135076:AAEintlhnhn2_Q4JjrTOn3oAII8Ya5sQefo"
CHAT_ID = "751733092"
THRESHOLD = 0.5  # Spread % before alert
SYMBOLS = ["BTC", "ETH", "DOGE", "PEPE", "XRP", "AVAX", "GALA", "POL", "DOT", "SHIB"]
# Binance symbols must be in format BTCUSDT, Coinbase needs BTC-USD

bot = Bot(token=TELEGRAM_TOKEN)

async def check_spreads():
    while True:
        for symbol in SYMBOLS:
            try:
                binance_price = await get_binance_price(f"{symbol}USDT")
                coinbase_price = await get_coinbase_price(symbol)
                
                spread = ((coinbase_price - binance_price) / binance_price) * 100

                if abs(spread) >= THRESHOLD:
                    msg = f"🚨 {symbol} Spread Alert\nBinance: {binance_price:.4f} USD\nCoinbase: {coinbase_price:.4f} USD\nSpread: {spread:.2f}%"
                    await bot.send_message(chat_id=CHAT_ID, text=msg)

            except Exception as e:
                print(f"Error fetching {symbol}: {e}")

        await asyncio.sleep(10)  # Check every 10 seconds

if __name__ == "__main__":
    asyncio.run(check_spreads())
