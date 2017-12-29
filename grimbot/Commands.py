import discord
from .APIConnector import *
from abc import abstractmethod, ABCMeta
from .CmdPatterns import CommandLengthDoesntMatchException, ArgsPatternPart
import requests
from .FXCalculator import *

token = "wLL3BnrAJq68pqkEZ8qdtUAhYQxfUT"

class Command(metaclass=ABCMeta):

    def __init__(self, cmdLabel : str, argsPatternParts : Sequence[ArgsPatternPart]):
        self.cmdLabel = cmdLabel
        self.argsPatternParts = argsPatternParts

    @abstractmethod
    async def execute(self, args : Sequence[str], client, message : discord.Message):
        raise NotImplementedError()

    @abstractmethod
    def help(self) -> str:
        raise NotImplementedError()

    def isMatch(self, cmdStr : str) -> bool:
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
            if argsPattern.numberOfArgs != -1:
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
    async def execute(self, args : Sequence[str], client, message : discord.Message):
        try:
            addr = APIConnector.create(token, message.author.id)
            await client.send_message(message.channel, "Your address is %s" % addr)
        except APIError as err:
            await client.send_message(message.channel, "ERROR: %s" % err.message)

    def help(self):
        return "!create - ウォレットを作成します"


class AddressCommand(Command):
    async def execute(self, args : Sequence[str], client, message : discord.Message):
        try:
            addr = APIConnector.address(token, message.author.id)
            if addr != "":
                await client.send_message(message.channel, "Your address is %s" % addr)
            else:
                await client.send_message(message.channel, "You haven't created your wallet yet!")
        except APIError as err:
            await client.send_message(message.channel, "ERROR: %s" % err.message)


    def help(self):
        return "!address - ウォレットアドレスを確認します"


class DepositCommand(Command):
    async def execute(self, args : Sequence[str], client, message : discord.Message):
        try:
            addr = APIConnector.address(token, message.author.id)
            if addr != "":
                await client.send_message(message.channel, "Your address is %s" % addr)
            else:
                await client.send_message(message.channel, "You haven't created your wallet yet!")
        except APIError as err:
            await client.send_message(message.channel, "ERROR: %s" % err.message)


    def help(self):
        return "!deposit - 受金用ウォレットアドレスを確認します"


class BalanceCommand(Command):
    async def execute(self, args : Sequence[str], client, message : discord.Message):
        try:
            balance = APIConnector.balance(token, message.author.id)
            await client.send_message(message.channel, "Your balance is %f GRIM" % balance)
        except APIError as err:
            await client.send_message(message.channel, "ERROR: %s" % err.message)

    def help(self):
        return "!balance - ウォレットの残高を確認します"


class WithdrawCommand(Command):
    async def execute(self, args : Sequence[str], client, message : discord.Message):
        try:
            amount = APIConnector.send(token, message.author.id, args[0], float(args[1]))
            await client.send_message(message.channel, "You send %f GRIM to %s" % (amount, args[0]))
        except APIError as err:
            await client.send_message(message.channel, "ERROR: %s" % err.message)


    def help(self):
        return "!balance (to) (amount) - 指定した金額だけ、指定したアドレスにGRIMを送金します"


class TipCommand(Command):
    async def execute(self, args : Sequence[str], client, message : discord.Message):
        try:
            APIConnector.tip(token, message.author.id, args[0], float(args[1]))
            await client.send_message(message.channel, "You send %f GRIM to %s" % (float(args[1]), args[0]))
        except APIError as err:
            await client.send_message(message.channel, "ERROR: %s" % err.message)


    def help(self):
        return "!tip (toName) (amount) - 指定した金額だけ、指定した名前の人にGRIMを送金します"


class RainCommand(Command):

    async def execute(self, args : Sequence[str], client, message : discord.Message):
        APIConnector.create("wLL3BnrAJq68pqkEZ8qdtUAhYQxfUT", "wintermaples")

    def help(self):
        return "!rain (amount) - オンラインの人に指定した数量だけGRIMを均等配分します"


class PriceCommand(Command):
    API_URL = "https://api.coinmarketcap.com/v1/ticker/grimcoin/?convert=JPY"

    def current_price(self) -> float:
        headers = {"content-type": "application/json"}
        data = requests.get(self.API_URL, headers=headers).json()
        return float(data[0]['price_jpy'])

    async def execute(self, args : Sequence[str], client, message : discord.Message):
        amount = float(args[0]) if len(args) > 0 else 1
        price = self.current_price()
        await client.send_message(message.channel, str(amount) + "GRIMは" + str(amount*price) + "円です!")

    def help(self):
        return "!grim [amount] - 現在のGRIMの価格を表示します"

class FXCalcCommand(Command):

    async def execute(self, args : Sequence[str], client, message : discord.Message):
        formula = "".join(args)
        await client.send_message(message.channel, formula + " = " + str(calc(formula)))

    def help(self):
        return "!fx lev (amount)x(magnitude) (currency) (beforePrice) to (afterPrice) with (L/S) - レバレッジをかけた時の利益と利益率を計算します"