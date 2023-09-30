import re, copy
from cell import Cell


class Board(object):
    def __init__(
        self,
        grid: [[Cell]] = [[]],
        turn: str = "x",
        is_middle_move: bool = False,
        middle_move_coords: [int, int] = [-1, -1],
    ) -> None:
        """Initialize Board object

        Args:
            grid ([[str]], optional): matrix of size >=6 and <=26 populated
                with objects of class Cell.Defaults to initial position.
            turn (str, optional): the next player to make a move ('x' or 'o').
                Defaults to "x".
            is_middle_move (bool, optional): a token has taken a piece and
                can take another one, so it has to take again next. Defaults to False.
            middle_move_coords (int, int], optional): if is_middle_move==True,
                these are the coords to the middle_piece. Defaults to [-1, -1].
        """
        self.size = 8  # min: 6 , max: 9
        if grid and len(grid) == len(grid[0]) == 8:
            self.grid = grid
        else:
            self.grid = [[Cell() for i in range(self.size)] for j in range(self.size)]
            self.populate()
        self.turn = turn
        self.is_middle_move = is_middle_move
        self.middle_move_coords = middle_move_coords
        return

    def copy(self) -> "Board":
        return copy.deepcopy(self)

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

    def convert_input_to_coords(self, input: str) -> [[int, int], [int, int]]:
        max_ch = chr(ord("a") + self.size - 1)
        max_dg = self.size
        regex = rf"^([1-{max_dg}][a-{max_ch}]|[a-{max_ch}][1-{max_dg}]).*([1-{max_dg}][a-{max_ch}]|[a-{max_ch}][1-{max_dg}])$"
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
        return [start, end]

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
        if self.grid[row1][col1].token != self.turn:  # Wrong token
            return False
        if self.grid[row2][col2].token != "_":  # Occupied destination
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
                if mid_cell.token == "_":  # Nothing to jump over
                    return False
                if mid_cell.token == self.turn:  # Cant jump over own token
                    return False
        else:  # Is a king piece
            if abs(row1 - row2) > 1:
                min_r = min(row1, row2)
                min_c = min(col1, col2)
                between_tokens = []
                for i in range(1, abs(row1 - row2)):
                    mid_cell = self.grid[min_r + i][min_c + i]
                    if mid_cell.token != "_":
                        between_tokens.append(mid_cell.token)
                if len(between_tokens) > 1:  # Cant jump over more than 1 token
                    return False
                if (
                    between_tokens and self.turn == between_tokens[0]
                ):  # Cant jump over own token
                    return False
        return True

    def available_squares(self, coords: [int, int]) -> [[int, int]]:
        x, y = coords
        av_squares = []
        if not self.grid[x][y].is_king:  # Token is not king
            if self.turn == "x":
                av_squares = [
                    [row, col]
                    for row in range(8)
                    for col in range(8)
                    if (row == x - 1 and abs(col - y) == 1)
                    or (row == x - 2 and abs(col - y) == 2)
                ]
            elif self.turn == "o":
                av_squares = [
                    [row, col]
                    for row in range(8)
                    for col in range(8)
                    if (row == x + 1 and abs(col - y) == 1)
                    or (row == x + 2 and abs(col - y) == 2)
                ]
            else:
                raise Exception("Invalid turn")
        else:  # Token is king
            av_squares = [
                [row, col]
                for row in range(8)
                for col in range(8)
                if abs(x - row) == abs(y - col)
            ]
        av_squares = [item for item in av_squares if self.is_valid_move(coords, item)]
        return av_squares

    def available_moves(self) -> [[[int, int], [int, int]]]:
        av_moves = []
        if self.is_middle_move:
            av_jumps = self.available_jumps(self.middle_move_coords)
            if av_jumps:
                av_squares = av_jumps
            else:
                av_squares = self.available_squares(self.middle_move_coords)
            for av_square in av_squares:
                av_moves.append([self.middle_move_coords, av_square])
            return av_moves

        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j].token == self.turn:
                    av_jumps = self.available_jumps([i, j])
                    if av_jumps:
                        av_squares = av_jumps
                    else:
                        av_squares = self.available_squares([i, j])
                    for av_square in av_squares:
                        av_moves.append([[i, j], av_square])
        return av_moves

    def is_jump(self, start: [int, int], end: [int, int]) -> bool:
        row1, col1 = start
        row2, col2 = end
        if not self.grid[row1][col1].is_king:  # Token is pawn
            if abs(row1 - row2) > 1:
                return True
        else:  # Token is king
            min_r = min(row1, row2)
            min_c = min(col1, col2)
            for i in range(1, abs(row1 - row2)):
                mid_cell = self.grid[min_r + i][min_c + i]
                if mid_cell.token != "_" and mid_cell.token != self.turn:
                    return True
        return False

    def available_jumps(self, coords: [int, int]) -> [[int, int]]:
        av_squares = self.available_squares(coords)
        return [square for square in av_squares if self.is_jump(coords, square)]

    def make_move(self, start: (int, int), end: (int, int)) -> "Board":
        row1, col1 = start
        row2, col2 = end
        if not [start, end] in self.available_moves():
            return
        b = self.copy()
        b.grid[row1][col1].clear()
        b.grid[row2][col2].token = self.turn
        if b.available_jumps(end):
            b.is_middle_move = True
            b.middle_move_coords = end
        else:
            b.is_middle_move = True
            b.middle_move_coords = [-1, -1]
        print(b)
        return b

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
