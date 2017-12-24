import discord
from typing import Sequence
from .APIConnector import *
from abc import abstractmethod, ABCMeta
from .CmdPatterns import CommandLengthDoesntMatchException, ArgsPatternPart


class Command(metaclass=ABCMeta):

    def __init__(self, cmdLabel : str, argsPatternParts : Sequence[ArgsPatternPart]):
        self.cmdLabel = cmdLabel
        self.argsPatternParts = argsPatternParts

    @abstractmethod
    async def execute(self, args : Sequence[str], client, message : discord.Message):
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
            raise CommandLengthDoesntMatchException(self.requiredNumberOfArgs())

        index = 0
        for argsPattern in self.argsPatternParts:
            if argsPattern.numberOfArgs != -1:
                argsPattern.validateArg(args[index:index + argsPattern.numberOfArgs()], index)
                index += argsPattern.numberOfArgs()
            else:
                argsPattern.validateArg(args[index:])

        return True

    def requiredNumberOfArgs(self) -> int:
        sum = 0
        for argsPattern in self.argsPatternParts:
            if argsPattern.numberOfArgs != -1:
                sum += argsPattern.numberOfArgs()
        return sum


class RainCommand(Command):

    async def execute(self, args : Sequence[str], client, message : discord.Message):
        amount = float(args[0])
        if not self.balanceIsMoreThan(message.author.id, amount):
            await client.send_message(message.channel, "配布金額が残高を超えています!")
            return

        addresses = list()
        for member in message.server.members:
            if member.status == discord.Status.online:
                address = APIConnector.address("", member.id)
                if address is not None:
                    addresses.append(address)

        pricePerOne = amount / len(addresses)

        for address in addresses:
            APIConnector.send("", message.author.id, address, pricePerOne)

        await client.send_message(message.channel, "%f Grimを%d人に、一人あたり%f Grimずつ送りました!" % (amount, len(addresses), pricePerOne))

    def balanceIsMoreThan(self, id : str, amount : float):
        if APIConnector.balance("", id) >= amount:
            return True
        return False