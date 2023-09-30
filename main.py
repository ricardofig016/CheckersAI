from cell import Cell
from board import Board

grid = [[Cell() for i in range(8)] for j in range(8)]
grid[0][2].token = "x"
grid[0][2].is_king = True
grid[1][1].token = "o"
grid[1][1].is_king = False

b = Board()
print(b)
start, end = b.convert_input_to_coords("3g 4h")
b = b.make_move(start, end)
start, end = b.convert_input_to_coords("4h 5g")
b = b.make_move(start, end)
start, end = b.convert_input_to_coords("3e d4")
b = b.make_move(start, end)
start, end = b.convert_input_to_coords("c3 d4")
b = b.make_move(start, end)
