import requests

API_URL = "https://api.coinmarketcap.com/v1/ticker/grimcoin/?convert=JPY"
API_URL2 = "https://api.coinmarketcap.com/v1/ticker/grimcoin/?convert=BTC"


async def current_price_jpy() -> float:
    headers = {"content-type": "application/json"}
    data = await requests.get(API_URL, headers=headers).json()
    return float(data[0]['price_jpy'])


async def current_price_btc() -> float:
    headers = {"content-type": "application/json"}
    data = await requests.get(API_URL2, headers=headers).json()
    return float(data[0]['price_btc'])