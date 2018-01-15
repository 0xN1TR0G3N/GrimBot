import requests

API_URL = "https://api.coinmarketcap.com/v1/ticker/%s/?convert=JPY"
API_URL2 = "https://api.coinmarketcap.com/v1/ticker/%s/?convert=BTC"

def getJSONDataFrom(url : str, timeout=30):
    headers = {"content-type": "application/json"}
    data = requests.get(url, headers=headers, timeout=timeout).json()
    return data

async def current_price_jpy(currency: str) -> float:
    return getJSONDataFrom(API_URL % currency, timeout=10)[0]['price_jpy']

async def current_price_btc(currency: str) -> float:
    return getJSONDataFrom(API_URL2 % currency, timeout=10)[0]['price_btc']