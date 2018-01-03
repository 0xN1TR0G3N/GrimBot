import discord

class CommandManager():

    commands = list()

    def __init__(self, cmdPrefix : str):
        self.cmdPrefix = cmdPrefix

    async def execute(self, cmdStr : str, client, message : discord.Message):
        prefix = cmdStr[0]
        if self.cmdPrefix != prefix:
            return False

        cmdStr = cmdStr[1:]
        for command in self.commands:
            if command.roomList is not None and not message.channel.name in command.roomList:
                continue
            if command.isMatch(cmdStr):
                await command.execute(cmdStr.split(" ")[1:], client, message)
                return True
