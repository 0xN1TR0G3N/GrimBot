import requests
import threading
import time

API_URL = "https://api.coinmarketcap.com/v1/ticker/grimcoin/?convert=JPY"
API_URL2 = "https://api.coinmarketcap.com/v1/ticker/grimcoin/?convert=BTC"


price_jpy = 0
price_btc = 0

def updatePriceJPY():
    global price_jpy
    while True:
        headers = {"content-type": "application/json"}
        data = requests.get(API_URL, headers=headers).json()
        price_jpy = float(data[0]['price_jpy'])
        time.sleep(60)


def updatePriceBTC():
    global price_btc
    while True:
        headers = {"content-type": "application/json"}
        data = requests.get(API_URL2, headers=headers).json()
        price_btc = float(data[0]['price_btc'])
        time.sleep(60)


threadUpdatePriceJPY = threading.Thread(target=updatePriceJPY)
threadUpdatePriceBTC = threading.Thread(target=updatePriceBTC)
threadUpdatePriceJPY.start()
threadUpdatePriceBTC.start()

async def current_price_jpy() -> float:
    return price_jpy

async def current_price_btc() -> float:
    return price_btc