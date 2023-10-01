from board import Board


def evaluate_board(board: Board, maximizing_player: bool) -> int:
    eval = 0
    for i in range(board.size):
        for cell in board.grid[i]:
            if cell.token == "o":
                if cell.is_king:
                    eval += 10
                else:
                    eval += board.size - i
            elif cell.token == "x":
                if cell.is_king:
                    eval -= 10
                else:
                    eval -= i + 1
    if maximizing_player:
        return eval
    return -eval


def minimax(board: Board, depth: int = 3, maximizing_player: bool = True) -> int:
    if depth == 0 or board.is_game_over():
        return evaluate_board(board, maximizing_player)

    if maximizing_player:
        max_eval = float("-inf")
        for move in board.get_possible_moves(maximizing_player):
            board_copy = board.copy()
            board_copy.make_move(move)
            eval = minimax(board_copy, depth - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float("inf")
        for move in board.get_possible_moves(
            opponent_player
        ):  # Define opponent_player accordingly
            board_copy = board.copy()
            board_copy.make_move(move)
            eval = minimax(board_copy, depth - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval


def get_best_move(board, depth, maximizing_player):
    best_move = None
    best_eval = float("-inf") if maximizing_player else float("inf")

    for move in board.get_possible_moves(maximizing_player):
        board_copy = board.copy()
        board_copy.make_move(move)
        eval = minimax(board_copy, depth - 1, not maximizing_player)

        if maximizing_player and eval > best_eval:
            best_eval = eval
            best_move = move

        if not maximizing_player and eval < best_eval:
            best_eval = eval
            best_move = move

    return best_move


# Example usage
if __name__ == "__main__":
    # Assuming you have a Board instance called 'current_board'
    depth = 3  # Adjust the depth based on your requirements
    ai_move = get_best_move(current_board, depth, maximizing_player=True)
    print("AI's best move:", ai_move)
