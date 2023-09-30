class Cell(object):
    def __init__(self, token: str = "_", is_king: bool = False) -> None:
        self.token = token
        self.is_king = is_king
        return

    def clear(self) -> None:
        self.token = "_"
        self.is_king = False
        return

    def promote(self) -> None:
        self.is_king = True
        return

    def __str__(self) -> str:
        if not self.is_king:
            return self.token
        if self.token == "x":
            return "X"
        if self.token == "o":
            return "O"
        raise Exception("Invalid token")
