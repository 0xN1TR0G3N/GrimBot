from typing import Sequence
from urllib import request
from urllib import parse
import json
import enum

apiUrl = "https://wallet.api.grimjp.club/"

def _postToAPI(api, params):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = parse.urlencode(params).encode("utf-8")

    req = request.Request(apiUrl + api, data=params, method="POST")
    with request.urlopen(req) as response:
        response_body = response.read().decode("utf-8")
        return response_body

class APIConnector:

    def create(token: str, id: str) -> str:
        data = json.loads(_postToAPI("wallet/create",
            {
                "token": token,
                "id": id
            }
        ))
        if data["status"] != APIConnector.Status.SUCCESS.value:
            raise APIError(data["message"])
        return data["result"]


    def address(token : str, id : str) -> str:
        data = json.loads(_postToAPI("wallet/address",
            {
                "token": token,
                "id": id
            }
        ))
        if data["status"] != 0:
            raise APIError(data["message"])
        if len(data["result"]) == 0:
            return ""
        return data["result"][0]["address"]

    def tip(token : str, fromId : str, toId : str, amount : float) -> bool:
        data = json.loads(_postToAPI("wallet/tip",
            {
                "token": token,
                "from": fromId,
                "to": toId,
                "amount": amount
            }
        ))
        if data["status"] != APIConnector.Status.SUCCESS.value:
            raise APIError(data["message"])
        return True

    def send(token : str, fromId : str, toAddr : str, amount : float) -> bool:
        data = json.loads(_postToAPI("wallet/send",
            {
                "token": token,
                "from": fromId,
                "to": toAddr,
                "amount": amount
            }
        ))
        if data["status"] != APIConnector.Status.SUCCESS.value:
            raise APIError(data["message"])
        return True

    def balance(token : str, id : str) -> float:
        data = json.loads(_postToAPI("wallet/balance",
            {
                "token": token,
                "id": id,
            }
        ))
        if data["status"] != APIConnector.Status.SUCCESS.value:
            raise APIError(data["message"])
        return float(data["result"])

    def delete(token : str, id : str) -> bool:
        data = json.loads(_postToAPI("wallet/delete",
            {
                "token": token,
                "id": id,
            }
        ))
        if data["status"] != APIConnector.Status.SUCCESS.value:
            raise APIError(data["message"])
        return True

    def list(token : str) -> Sequence[str]:
        data = json.loads(_postToAPI("wallet/list",
            {
                "token": token,
            }
        ))
        if data["status"] != APIConnector.Status.SUCCESS.value:
            raise APIError(data["message"])
        return data["result"]

    def rain(token : str, id : str, amount : float) -> bool:
        pass

    class Status(enum.Enum):
        SUCCESS = '0'
        WALLET_NOT_FOUND = '114514-1'
        INSUFFICIENT_FUNDS = '114514-2'

class APIError(Exception):

    def __init__(self, message : str):
        self.message = message