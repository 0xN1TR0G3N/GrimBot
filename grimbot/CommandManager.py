from abc import ABCMeta, abstractmethod
from typing import Sequence
import discord
import asyncio

class ArgsPatternPart(metaclass=ABCMeta):

    @abstractmethod
    def argsLength(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def isMatch(self, args : Sequence[str], index : int) -> bool:
        raise NotImplementedError()


# コマンドの引数の長さが一致しなかった時に発生させる例外です
class CommandLengthDoesntMatchException(Exception):
    def __init__(self, length : int):
        self.length = length

    def __str__(self):
        return "このコマンドは、少なくとも%d個の引数が必要です!" % self.length

# コマンドのパターンが一致しなかった時に発生させる例外です
class CommandArgsPatternDoesntMatchException(Exception):
    def __init__(self, message : str):
        self.message = message

    def __str__(self):
        return self.message

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
            if command.isMatch(cmdStr):
                await command.execute(cmdStr.split(" ")[1:], client, message)
                return True

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

        if self.requiredArgsLength() > len(args):
            raise CommandLengthDoesntMatchException(self.requiredArgsLength())

        index = 0
        for argsPattern in self.argsPatternParts:
            if argsPattern.argsLength != -1:
                if argsPattern.isMatch(args[index:index + argsPattern.argsLength()], index):
                    pass # 一致しなければ例外が発生するのでそれにまかせる
                index += argsPattern.argsLength()
            else:
                if argsPattern.isMatch(args[index:]):
                    pass # 一致しなければ例外が発生するのでそれにまかせる

        return True

    def requiredArgsLength(self) -> int:
        sum = 0
        for argsPattern in self.argsPatternParts:
            if argsPattern.argsLength != -1:
                sum += argsPattern.argsLength()
        return sum