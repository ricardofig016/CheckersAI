import re
import string
from cell import Cell


class Board(object):
    def __init__(self, grid: [[Cell]] = [[]], turn="x") -> None:
        """Initialize a Board object

        Args:
            grid ([[str]], optional): matrix of size >=6 and <=26 populated
                with objects of class Cell.Defaults to initial position.
            turn (str, optional): the next player to make a move ('x' or 'o').
                Defaults to "x".
        """
        self.size = 8  # min: 6 , max: 26
        if grid and len(grid) == len(grid[0]) == 8:
            self.grid = grid
        else:
            self.grid = [[Cell() for i in range(self.size)] for j in range(self.size)]
            self.populate()
        self.turn = turn
        return

    def populate(self) -> None:
        """Populate an empty grid with x's and o's in their starting positions"""
        for i in range(self.size):
            for j in range(self.size):
                if i < 3:
                    token = "o"
                else:
                    token = "x"
                if not i in range(3, self.size - 3):
                    if i % 2 == 0:
                        if j % 2 == 1:
                            self.grid[i][j].token = token
                    else:
                        if j % 2 == 0:
                            self.grid[i][j].token = token
        return

    def convert_input_to_coords(self, input: str) -> ((int, int), (int, int)):
        regex = r"^([1-8][a-h]|[a-h][1-8]).*([1-8][a-h]|[a-h][1-8])$"
        if not bool(re.match(regex, input)):
            raise Exception("Invalid input")

        start = [-1, -1]
        end = [-1, -1]
        coords = input[:2]
        for ch in coords:
            if ch.isdigit():
                start[0] = self.size - int(ch)
            if ch.isalpha():
                start[1] = ord(ch) - ord("a")
        coords = input[-2:]
        for ch in coords:
            if ch.isdigit():
                end[0] = self.size - int(ch)
            if ch.isalpha():
                end[1] = ord(ch) - ord("a")

        if -1 in start or -1 in end:
            raise Exception("Could not read input correctly")
        return (start, end)

    def flip_turn(self) -> None:
        """flip self.turn from x to o or from o to x"""
        if self.turn == "x":
            self.turn = "o"
        else:
            self.turn = "x"
        return

    def is_valid_move(self, start: [int, int], end: [int, int]) -> bool:
        row1, col1 = start
        row2, col2 = end
        if row1 % 2 == col1 % 2 or row2 % 2 == col2 % 2:  # Illegal square
            return False
        if self.grid[row1][col1].token != self.turn:  # Wrong token
            return False
        if self.grid[row2][col2].token != " ":  # Occupied destination
            return False
        if not abs(row1 - row2) == abs(col1 - col2):  # Not on the same diagonal
            return False
        if not self.grid[row1][col1].is_king:  # Not a king piece
            if self.turn == "x":
                if row1 < row2:  # X piece going backwards
                    return False
            if self.turn == "o":
                if row1 > row2:  # O piece going backwards
                    return False
            if abs(row1 - row2) > 2:  # Distance is greater than 2
                return False
            if abs(row1 - row2) == 2:
                mid_cell = self.grid[(row1 + row2) // 2][(col1 + col2) // 2]
                if mid_cell.token == " ":  # Nothing to jump over
                    return False
                if mid_cell.token == self.turn:  # Cant jump over own token
                    return False
        else:  # Is a king piece
            pass  ## INCOMPLETE
        return True

    def is_legal_move(self, start: (int, int), end: (int, int)) -> bool:
        return True

    def available_moves(self) -> {(int, int): (int, int)}:
        return

    def make_move(self, start: (int, int), end: (int, int)) -> None:
        return

    def __str__(self) -> str:
        """Turn the grid into a board like string

        Returns:
            str: Nice representation of the grid
        """
        string = ""
        for i in range(self.size):
            string += str(self.size - i) + " "
            for elem in self.grid[i]:
                string += "|" + str(elem)
            string += "|" + "\n"
        string += "  "
        for i in range(self.size):
            string += " " + chr(ord("a") + i)
        return string
