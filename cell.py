class Cell(object):
    def __init__(self, token: str = " ", is_king: bool = False) -> None:
        self.token = token
        self.is_king = is_king
        return

    def __str__(self) -> str:
        if not self.is_king:
            return self.token
        if self.token == "x":
            return "X"
        if self.token == "o":
            return "O"
        raise Exception("Invalid token")
