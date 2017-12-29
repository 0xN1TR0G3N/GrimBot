from typing import Sequence
import re
from abc import ABCMeta, abstractmethod


class ArgsPatternPart(metaclass=ABCMeta):

    @abstractmethod
    def numberOfArgs(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def validateArg(self, args : Sequence[str], index : int) -> bool:
        raise NotImplementedError()


# コマンドの引数の長さが一致しなかった時に発生させる例外です
class CommandLengthDoesntMatchException(Exception):
    def __init__(self, length : int, help : str):
        self.length = length
        self.help = help

    def __str__(self):
        return "このコマンドは、少なくとも%d個の引数が必要です!" % self.length


# コマンドのパターンが一致しなかった時に発生させる例外です
class CommandArgsPatternDoesntMatchException(Exception):
    def __init__(self, message : str):
        self.message = message

    def __str__(self):
        return self.message


class NumberArgsPattern(ArgsPatternPart):

    def __init__(self, numberOfArgs_=1):
        self.numberOfArgs_ = numberOfArgs_

    def numberOfArgs(self):
        return self.numberOfArgs_

    def validateArg(self, args : Sequence[str], index : int):
        try:
            i = 0
            for arg in args:
                float(arg)
            i += 1
        except ValueError:
            raise CommandArgsPatternDoesntMatchException("%d番目の引数が数値ではありません!" % (index + i + 1))
        else:
            return True


class PositiveNumberArgsPattern(ArgsPatternPart):

    def __init__(self, numberOfArgs_=1):
        self.numberOfArgs_ = numberOfArgs_

    def numberOfArgs(self):
        return self.numberOfArgs_

    def validateArg(self, args : Sequence[str], index : int):
        try:
            i = 0
            for arg in args:
                f = float(arg)
                if f <= 0:
                    raise ValueError()
                i += 1
        except ValueError:
            raise CommandArgsPatternDoesntMatchException("%d番目の引数が正の数値ではありません!" % (index + 1))
        else:
            return True


class StringArgsPattern(ArgsPatternPart):

    def __init__(self, s : str):
        self.s = s

    def numberOfArgs(self):
        return 1

    def validateArg(self, args : Sequence[str], index : int):
        if args[0] != self.s:
            raise CommandArgsPatternDoesntMatchException("%d番目の引数は「%s」である必要があります!" % (index + 1, self.s))
        return True


class RegexArgsPattern(ArgsPatternPart):

    def __init__(self, regexStr : str, errorMessage : str):
        self.regex = re.compile(regexStr)
        self.errMessage = errorMessage

    def numberOfArgs(self):
        return 1

    def validateArg(self, args : Sequence[str], index : int):
        if not self.regex.match(args[0]):
            raise CommandArgsPatternDoesntMatchException("%d番目の引数に問題があります! - %s" % (index + 1, self.errMessage))
        return True