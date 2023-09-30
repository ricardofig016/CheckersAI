from board import Board

b = Board()
print(b)
start, end = b.convert_input_to_coords("3a-4k")
print(b.turn)
print(start, end)
print(b.is_valid_move(start, end))
