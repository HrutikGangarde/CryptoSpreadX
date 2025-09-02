import aiohttp

BINANCE_URL = "https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
COINBASE_URL = "https://api.coinbase.com/v2/prices/{symbol}-USD/spot"

async def get_binance_price(symbol: str) -> float:
    async with aiohttp.ClientSession() as session:
        async with session.get(BINANCE_URL.format(symbol=symbol)) as resp:
            data = await resp.json()
            return float(data['price'])

async def get_coinbase_price(symbol: str) -> float:
    async with aiohttp.ClientSession() as session:
        async with session.get(COINBASE_URL.format(symbol=symbol)) as resp:
            data = await resp.json()
            return float(data['data']['amount'])
