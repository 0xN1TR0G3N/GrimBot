import discord
from discord.ext import commands
import requests
import json
import shlex

API_URL = "https://api.coinmarketcap.com/v1/ticker/grimcoin/?convert=JPY"
client = discord.Client()

def current_price():
    headers = {"content-type": "application/json"}
    data = requests.get(API_URL, headers=headers).json()
    return (data[0]['price_jpy'])

def talk(message):
    payload = {
        'apikey':'apikey',
        'query':message
    }
    r = requests.post('https://api.a3rt.recruit-tech.co.jp/talk/v1/smalltalk', data=payload).json()
    return str(r['results'][0]['reply'])

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if client.user != message.author:
        split = message.content.split()

        """ いくらコマンド """
        if split[0].startswith("?いくら") or split[0].startswith("？いくら"):
            if len(split) == 1:
                m = str(message.author.mention) + " " + "1GRIMは" + str(current_price()) + "円です！"
                await client.send_message(message.channel, m)
            elif split[1].isdigit():
                m = str(message.author.mention) + " " + \
                    str(split[1]) + "GRIMは" + str(float(current_price()) * float(split[1])) + "円です！"
                await client.send_message(message.channel, m)

        """ イクラコマンド """
        if split[0].startswith("?イクラ") or split[0].startswith("？イクラ"):
            if len(split) == 1:
                m = "それはイクラです"
                await client.send_message(message.channel, m)
            elif split[1].isdigit():
                m = "それはイクラです"
                await client.send_message(message.channel, m)

        """ トークコマンド """
        if split[0].find("?トーク") != -1 or split[0].find("？トーク") != -1:
            m = str(message.author.mention) + " " + talk(split[1])
            await client.send_message(message.channel, m)

client.run("TOKEN")
