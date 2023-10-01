from board import Board


def pvp():
    b = Board()
    while not b.is_game_over():
        print(b)
        print(f"It's {b.turn.upper()} turn")
        while True:
            try:
                move = input("Your move: ")
                start, end = b.convert_input_to_coords(move)
                b = b.make_move(start, end)
                if b:
                    break
            except Exception as e:
                print("Invalid move, try again")
    print(b)


if __name__ == "__main__":
    pvp()
