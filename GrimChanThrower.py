from typing import Sequence
import os
import json
from urllib import request
from urllib import parse

def _postTo(url, params):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = parse.urlencode(params).encode("utf-8")

    req = request.Request(url, data=params, method="POST")
    with request.urlopen(req) as response:
        response_body = response.read().decode("utf-8")
        return response_body

class GrimChanThrower:

    def __init__(self):
        self.serverCommandsList : Sequence[ServerCommands] = []

    def isMatch(self, serverId : str, cmdStr : str):
        for serverCommands in self.serverCommandsList:
            if serverCommands.serverId == serverId:
                return serverCommands.isMatch(cmdStr)

    def transferIfMatched(self, cmdStr : str, serverId : str) -> str:
        for serverCommands in self.serverCommandsList:
            if serverCommands.serverId == serverId:
                return serverCommands.transferIfMatched(cmdStr)

class ServerCommands:

    def __init__(self, serverId : str, transferTo : str, prefix : str):
        self.serverId : str = serverId
        self.commands : Sequence[str] = []
        self.transferTo = transferTo
        self.prefix = prefix

    def isMatch(self, cmdStr : str) -> bool:
        prefix = cmdStr[0]
        if self.prefix != prefix:
            return False

        cmdStr = cmdStr[1:]

        cmdSplited = cmdStr.split(' ')
        if cmdSplited[0] in self.commands:
            return True

    def transfer(self, cmdLabel : str, cmdArgs : Sequence[str]):
        return _postTo(self.transferTo, {'label': cmdLabel, 'args': cmdArgs})

    def transferIfMatched(self, cmdStr : str) -> str:
        if self.isMatch(cmdStr):
            cmdStr = cmdStr[1:]
            cmdSplited = cmdStr.split(' ')
            return self.transfer(cmdSplited[0], cmdSplited[1:])


class ServerCommandsLoader:
    @staticmethod
    def loadFrom(file : str) -> ServerCommands:
        with open(file, mode='r') as f:
            lines = "".join(f.readlines())
            serverCommandsData = json.loads(lines)
        scs = ServerCommands(serverCommandsData['serverId'], serverCommandsData['transferTo'], serverCommandsData['prefix'])
        scs.commands = serverCommandsData['commands']
        return scs

    @staticmethod
    def loadsFrom(dir : str) -> Sequence[ServerCommands]:
        files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
        scss = []
        for file in files:
            scss.append(ServerCommandsLoader.loadFrom(os.path.join(dir, file)))
        return scss