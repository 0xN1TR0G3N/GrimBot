class APIConnector:
    def get_address(token : str, id : str) -> str:
        return "ADDR"

    def get_balance(token : str, id : str) -> float:
        return 1000.12

    def send(token : str, id : str, sendTo : str, amount : float) -> bool:
        return True