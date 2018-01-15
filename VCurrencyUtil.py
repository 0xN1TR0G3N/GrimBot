import requests

API_URL = "https://api.coinmarketcap.com/v1/ticker/%s/?convert=%s"

def getJSONDataFrom(url : str, timeout=30):
    headers = {"content-type": "application/json"}
    data = requests.get(url, headers=headers, timeout=timeout).json()
    return data

async def getVCurrencyData(currency: str, convertTo: str):
    return getJSONDataFrom(API_URL % (currency, convertTo), timeout=10)

async def current_price_jpy(currency: str) -> float:
    return float(getJSONDataFrom(API_URL % (currency, 'JPY'), timeout=10)[0]['price_jpy'])

async def current_price_btc(currency: str) -> float:
    return float(getJSONDataFrom(API_URL % (currency, 'BTC'), timeout=10)[0]['price_btc'])