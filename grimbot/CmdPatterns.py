from typing import Sequence
import re
from abc import ABCMeta, abstractmethod


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


class NumberArgsPattern(ArgsPatternPart):

    def argsLength(self):
        return 1

    def isMatch(self, args : Sequence[str], index : int):
        try:
            float(args[0])
        except ValueError:
            raise CommandArgsPatternDoesntMatchException("%d番目の引数が数値ではありません!" % (index + 1))
        else:
            return True


class PositiveNumberArgsPattern(ArgsPatternPart):

    def argsLength(self):
        return 1

    def isMatch(self, args : Sequence[str], index : int):
        try:
            f = float(args[0])
            if f <= 0:
                raise ValueError()
        except ValueError:
            raise CommandArgsPatternDoesntMatchException("%d番目の引数が正の数値ではありません!" % (index + 1))
        else:
            return True


class StringArgsPattern(ArgsPatternPart):

    def __init__(self, s : str):
        self.s = s

    def argsLength(self):
        return 1

    def isMatch(self, args : Sequence[str], index : int):
        if args[0] != self.s:
            raise CommandArgsPatternDoesntMatchException("%d番目の引数は「%s」である必要があります!" % (index + 1, self.s))
        return True


class RegexArgsPattern(ArgsPatternPart):

    def __init__(self, regexStr : str, errorMessage : str):
        self.regex = re.compile(regexStr)
        self.errMessage = errorMessage

    def argsLength(self):
        return 1

    def isMatch(self, args : Sequence[str], index : int):
        if not self.regex.match(args[0]):
            raise CommandArgsPatternDoesntMatchException("%d番目の引数に問題があります! - %s" % (index + 1, self.errMessage))
        return True