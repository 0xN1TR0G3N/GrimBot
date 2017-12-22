from .CommandManager import Command
import discord
from typing import Sequence
from .APIConnector import *

class RainCommand(Command):

    async def execute(self, args : Sequence[str], client, message : discord.Message):
        amount = float(args[0])
        if not self.balanceIsMoreThan(message.author.id, amount):
            await client.send_message(message.channel, "配布金額が残高を超えています!")
            return

        addressDict = dict()
        for member in message.server.members:
            if member.status == discord.Status.online:
                address = APIConnector.get_address("", member.id)
                if address is not None:
                    addressDict.update({member.id: address})

        pricePerOne = amount / len(addressDict)

        for memberId in addressDict:
            address = addressDict[memberId]
            APIConnector.send("", message.author.id, address)

        await client.send_message(message.channel, "%f Grimを%d人に、一人あたり%f Grimずつ送りました!" % (amount, len(addressDict), pricePerOne))

    def balanceIsMoreThan(self, id : str, amount : float):
        if APIConnector.get_balance("", id) >= amount:
            return True
        return False