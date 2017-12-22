from .CommandManager import ArgsPatternPart, CommandArgsPatternDoesntMatchException
from typing import Sequence
import re

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