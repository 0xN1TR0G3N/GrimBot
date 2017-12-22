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

        addresses = list()
        for member in message.server.members:
            if member.status == discord.Status.online:
                address = APIConnector.get_address("", member.id)
                if address is not None:
                    addresses.append(address)

        pricePerOne = amount / len(addresses)

        for address in addresses:
            APIConnector.send("", message.author.id, address, pricePerOne)

        await client.send_message(message.channel, "%f Grimを%d人に、一人あたり%f Grimずつ送りました!" % (amount, len(addressDict), pricePerOne))

    def balanceIsMoreThan(self, id : str, amount : float):
        if APIConnector.get_balance("", id) >= amount:
            return True
        return False