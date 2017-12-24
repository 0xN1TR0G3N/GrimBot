from typing import Sequence

class APIConnector:
    def create(token: str, id: str) -> str:
        return ""

    def address(token : str, id : str) -> str:
        return "ADDR"

    def move(self, token : str, fromAddr : str, toAddr : str, amount : float) -> float:
        return 0.0

    def send(token : str, id : str, to : str, amount : float) -> bool:
        return True

    def balance(token : str, id : str) -> float:
        return 1000.12

    def delete(token : str, id : str) -> bool:
        return True

    def list(token : str) -> Sequence[str]:
        return list()

