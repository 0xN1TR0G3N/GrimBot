import json
from abc import abstractmethod, ABCMeta

import discord
import requests
from DiscordUtil import *
from GrimUtil import *
from discord.embeds import *

from .APIConnector import *
from .CmdPatterns import CommandLengthDoesntMatchException, ArgsPatternPart
from .FXCalculator import *
import logging
from Translator import *

token = open('grimapi_token.txt').readline()
docomo_api_url = "https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue?APIKEY="
docomo_api_key = open('docomoapi_token.txt').readline()

print('Web API Token: %s' % (token[0:3] + '*' * 20))
print('Docomo API Token: %s' % (docomo_api_key[0:3] + '*' * 20))

class Command(metaclass=ABCMeta):
    def __init__(self, cmdLabel: str, argsPatternParts: Sequence[ArgsPatternPart], roomList : Sequence[str] = None):
        self.cmdLabel = cmdLabel
        self.argsPatternParts = argsPatternParts
        self.roomList = roomList

    @abstractmethod
    async def execute(self, args: Sequence[str], client, message: discord.Message):
        raise NotImplementedError()

    @abstractmethod
    def help(self) -> str:
        raise NotImplementedError()

    def isMatch(self, cmdStr: str) -> bool:
        cmdSplited = cmdStr.split(" ")
        if len(cmdSplited) == 0:
            raise AssertionError()

        cmdLabel = cmdSplited[0]
        if cmdLabel != self.cmdLabel:
            return False

        args = cmdSplited[1:]

        if len(args) < self.requiredNumberOfArgs():
            raise CommandLengthDoesntMatchException(self.requiredNumberOfArgs(), self.help())

        index = 0
        for argsPattern in self.argsPatternParts:
            if argsPattern.numberOfArgs() != -1:
                argsPattern.validateArg(args[index:index + argsPattern.numberOfArgs()], index)
                index += argsPattern.numberOfArgs()
            else:
                argsPattern.validateArg(args[index:], index)

        return True

    def requiredNumberOfArgs(self) -> int:
        sum = 0
        for argsPattern in self.argsPatternParts:
            if argsPattern.numberOfArgs() != -1:
                sum += argsPattern.numberOfArgs()
        return sum


class CreateCommand(Command):
    async def execute(self, args: Sequence[str], client, message: discord.Message):
        try:
            toId = getIdFromName(message.server, message.author.name)
            if toId != "":
                address = APIConnector.create(token, message.author.id)
                embed = Embed(description='<@%s>の"GRIMアドレス"を作成したわ。' % (toId), type='rich', colour=0x6666FF)
                embed.add_field(name='GRIM Address', value=address)
                embed.set_thumbnail(url='https://api.qrserver.com/v1/create-qr-code/?data=%s' % address)
                await client.send_message(message.channel, embed=embed)
        except APIError as err:
            await client.send_message(message.channel, "ERROR: %s" % err.message)

    def help(self):
        return ",create - ウォレットを作成します"


class AddressCommand(Command):
    async def execute(self, args: Sequence[str], client, message: discord.Message):
        try:
            toId = getIdFromName(message.server, message.author.name)
            if toId != "":
                address = APIConnector.address(token, message.author.id)
                if address != "":
                    embed = Embed(description='<@%s>の"GRIMアドレス"はこれよ。' % (toId), type='rich', colour=0x6666FF)
                    embed.add_field(name='GRIM Address', value=address)
                    embed.set_thumbnail(url='https://api.qrserver.com/v1/create-qr-code/?data=%s' % address)
                    await client.send_message(message.channel, embed=embed)
                else:
                    await client.send_message(message.channel, ',register でウォレットを作成してから出直しなさい。')
        except APIError as err:
            await client.send_message(message.channel, "ERROR: %s" % err.message)

    def help(self):
        return ",address - ウォレットアドレスを確認します"


class DepositCommand(Command):
    async def execute(self, args: Sequence[str], client, message: discord.Message):
        try:
            toId = getIdFromName(message.server, message.author.name)
            if toId != "":
                address = APIConnector.address(token, message.author.id)
                if address != "":
                    embed = Embed(description='<@%s>の"GRIMアドレス"はこれよ' % (toId), type='rich', colour=0x6666FF)
                    embed.add_field(name='GRIM Address', value=address)
                    embed.set_thumbnail(url='https://api.qrserver.com/v1/create-qr-code/?data=%s' % address)
                    await client.send_message(message.channel, embed=embed)
                else:
                    await client.send_message(message.channel, ',register でウォレットを作成してから出直しなさい。')
        except APIError as err:
            await client.send_message(message.channel, "ERROR: %s" % err.message)

    def help(self):
        return ",deposit - 受金用ウォレットアドレスを確認します"


class BalanceCommand(Command):
    async def execute(self, args: Sequence[str], client, message: discord.Message):
        try:
            toId = getIdFromName(message.server, message.author.name)
            if toId != "":
                priceJPY = await current_price_jpy()
                balance = APIConnector.balance(token, message.author.id)
                embed = Embed(description='<@%s>の"所持GRIM数"を表示するわ。' % (toId), type='rich', colour=0x6666FF)
                embed.add_field(name='GRIM所持数', value='%.04f GRIM' % balance, inline=True)
                embed.add_field(name='日本円換算', value='%0.04f 円' % (priceJPY * balance), inline=True)
                await client.send_message(message.channel, embed=embed)
        except APIError as err:
            await client.send_message(message.channel, "ERROR: %s" % err.message)

    def help(self):
        return ",balance - ウォレットの残高を確認します"


class WithdrawCommand(Command):
    async def execute(self, args: Sequence[str], client, message: discord.Message):
        try:
            APIConnector.send(token, message.author.id, args[0], float(args[1]))
            toId = getIdFromName(message.server, message.author.name)
            if toId != "":
                await mention(client, message.channel, message.author.name,
                              '"%s"に"%f GRIM"送金したわ。確認しなさい。' % (args[0], float(args[1])))
        except APIError as err:
            await client.send_message(message.channel, "ERROR: %s" % err.message)

    def help(self):
        return ",balance (to) (amount) - 指定した金額だけ、指定したアドレスにGRIMを送金します"


class TipCommand(Command):
    async def execute(self, args: Sequence[str], client, message: discord.Message):
        try:
            toId = getIdFromName(message.server, message.author.name)
            destId = getIdFromName(message.server, args[0])
            if destId != "":
                if toId != "":
                    APIConnector.tip(token, message.author.id, destId, float(args[1]))
                    await mention(client, message.channel, message.author.name,
                                  'から<@%s>に"%f GRIM"送金したわ。' % (destId, float(args[1])))
            else:
                await client.send_message(message.channel, "送りたい相手(%s)が見つからないわ。名前をもう一度確認しなさい。" % args[0])
        except APIError as err:
            await client.send_message(message.channel, "ERROR: %s" % err.message)

    def help(self):
        return ",tip (toName) (amount) - 指定した金額だけ、指定した名前の人にGRIMを送金します"


class RainCommand(Command):
    async def execute(self, args: Sequence[str], client, message: discord.Message):
        try:
            amount = float(args[0])
            if not self.balanceIsMoreThan(message.author.id, amount):
                await client.send_message(message.channel,
                                          '所持"GRIM"が足りないわ。あなたの残高は"%fGRIM"よ。' % APIConnector.balance(token,
                                                                                                    message.author.id))
                return

            onlineMembersId = [member.id for member in message.server.members if member.status == discord.Status.online and not member.is_afk] # オンラインの人のID取得
            ownerIdListOfWallets = [wallet['name'] for wallet in APIConnector.list(token)] # ウォレット一覧取得
            onlineMembersIdWhoHasWallet = [memberId for memberId in onlineMembersId if memberId in ownerIdListOfWallets] # オンラインの人の中から、ウォレットを持ってる人のID一覧取得

            pricePerOne = amount / len(onlineMembersIdWhoHasWallet)

            APIConnector.rain(token, message.author.id, onlineMembersIdWhoHasWallet, pricePerOne)

            toId = getIdFromName(message.server, message.author.name)

            await client.send_message(message.channel,
                                      '<@%s> から"%f GRIM"を受け取ったわ。恵みの雨を受け取りなさい。一人"%.04f GRIM"よ。' % (toId, amount, pricePerOne))
        except APIError as err:
            await client.send_message(message.channel, "ERROR: %s" % err.message)

    def balanceIsMoreThan(self, id: str, amount: float):
        if APIConnector.balance(token, id) >= amount:
            return True
        return False

    def help(self):
        return ",rain (amount) - オンラインの人に指定した数量だけGRIMを均等配分します"


class PriceCommand(Command):
    async def execute(self, args: Sequence[str], client, message: discord.Message):
        amount = float(args[0]) if len(args) > 0 else 1
        price = await current_price_jpy()
        priceBTC = await current_price_btc()
        embed = Embed(description='「そう。私に読めるのは"GRIM"の価値だけ」', type='rich', colour=0x6666FF)
        embed.add_field(name="GRIM/BTC", value="%.10f BTC" % priceBTC, inline=True)
        embed.add_field(name="GRIM/JPY", value="%.10f JPY" % price, inline=True)
        if amount != 1:
            embed.add_field(name="ㅤ", value="ㅤ", inline=False)
            embed.add_field(name="%.04f GRIM/BTC" % amount, value="%.10f BTC" % (priceBTC * amount), inline=True)
            embed.add_field(name="%.04f GRIM/JPY" % amount, value="%.10f JPY" % (price * amount), inline=True)
        embed.set_footer(text='https://coinmarketcap.com/currencies/grimcoin/')
        embed.set_thumbnail(
            url='http://files.coinmarketcap.com.s3-website-us-east-1.amazonaws.com/static/img/coins/200x200/grimcoin.png')
        await client.send_message(message.channel, embed=embed)

    def help(self):
        return ",grim [amount] - 現在のGRIMの価格を表示します"


class FXCalcCommand(Command):
    async def execute(self, args: Sequence[str], client, message: discord.Message):
        formula = "".join(args)
        await client.send_message(message.channel, formula + " = " + str(calc(formula)))

    def help(self):
        return ",fx lev (amount)x(magnitude) (currency) (beforePrice) to (afterPrice) with (L/S) - レバレッジをかけた時の利益と利益率を計算します"


class TalkCommand(Command):

    context_dic = {}

    async def execute(self, args: Sequence[str], client, message: discord.Message):
        contents = " ".join(args)
        headers = {
            "Content-Type": "application/json"
        }
        params = json.dumps({
            "utt": contents,
            "context": self.context_dic[message.author.id] if message.author.id in self.context_dic.keys() else "",
            "mode": "dialog"
        }).encode('utf-8')
        res = requests.post(docomo_api_url + docomo_api_key, data=params, headers=headers)
        data = res.json()
        self.context_dic.update({message.author.id: data["context"]})
        await mention(client, message.channel, message.author.name, data["utt"])

    def help(self):
        return ",talk (contents) - ぐりむちゃんと会話します"


class TranslateJPIntoENCommand(Command):
    async def execute(self, args: Sequence[str], client, message: discord.Message):
        await mention(client, message.channel, message.author.name, translate(' '.join(args), 'jp', 'en'))

    def help(self):
        return ',trjp (japanese) - 日本語から英語に翻訳します'


class TranslateENIntoJPCommand(Command):
    async def execute(self, args: Sequence[str], client, message: discord.Message):
        await mention(client, message.channel, message.author.name, translate(' '.join(args), 'en', 'jp'))

    def help(self):
        return ',tren (english) - 英語から日本語に翻訳します'