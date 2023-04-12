from copy import deepcopy
import math


# Các hàm chung
def is_valid_move(board, player, move):
    x, y = move

    if not board[x][y] == 0:
        return False

    directions = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0),
        (1, 1),
        (-1, -1),
        (1, -1),
        (-1, 1),
    ]

    for d in directions:
        c, r = x + d[0], y + d[1]

        if 0 <= c < 8 and 0 <= r < 8 and board[c][r] == -player:
            c, r = c + d[0], r + d[1]

            while 0 <= c < 8 and 0 <= r < 8 and board[c][r] == -player:
                c, r = c + d[0], r + d[1]

            if 0 <= c < 8 and 0 <= r < 8 and board[c][r] == player:
                return True

    return False


def get_valid_move(board, player):
    valid_moves = []
    for col in range(8):
        for row in range(8):
            if is_valid_move(board, player, (col, row)):
                valid_moves.append((col, row))
    return valid_moves


def make_move(board, player, move):
    x, y = move
    board[x][y] = player

    directions = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0),
        (1, 1),
        (-1, -1),
        (1, -1),
        (-1, 1),
    ]

    for d in directions:
        c, r = x + d[0], y + d[1]

        if 0 <= c < 8 and 0 <= r < 8 and board[c][r] == -player:
            c, r = c + d[0], r + d[1]

            while 0 <= c < 8 and 0 <= r < 8 and board[c][r] == -player:
                c, r = c + d[0], r + d[1]

            if 0 <= c < 8 and 0 <= r < 8 and board[c][r] == player:
                c, r = x + d[0], y + d[1]

                while board[c][r] == -player:
                    board[c][r] = player
                    c, r = c + d[0], r + d[1]


def get_score(board):
    score_dict = {-1: 0, 0: 0, 1: 0}
    for c in range(8):
        for r in range(8):
            score_dict[board[c][r]] += 1
    return score_dict


# Các hàm cho agent
def evaluate(board, player):
    score = 0

    count = get_score(board)
    player_count = count[player]
    opponent_count = count[-player]

    score += player_count - opponent_count

    weight_board = [
        [120, -20, 20, 5, 5, 20, -20, 120],
        [-20, -40, -5, -5, -5, -5, -40, -20],
        [20, -5, 15, 3, 3, 15, -5, 20],
        [5, -5, 3, 3, 3, 3, -5, 5],
        [5, -5, 3, 3, 3, 3, -5, 5],
        [20, -5, 15, 3, 3, 15, -5, 20],
        [-20, -40, -5, -5, -5, -5, -40, -20],
        [120, -20, 20, 5, 5, 20, -20, 120],
    ]

    for i in range(8):
        for j in range(8):
            if board[i][j] == player:
                score += weight_board[i][j]
            elif board[i][j] == -player:
                score -= weight_board[i][j]

    return score


def alphabeta(cur_state, player_to_move, depth, alpha, beta):
    valid_move = get_valid_move(cur_state, player_to_move)

    if depth == 0 or not valid_move:
        return evaluate(cur_state, player_to_move)

    if player_to_move == -1:
        max_score = -math.inf

        for move in valid_move:
            new_board = deepcopy(cur_state)
            make_move(new_board, player_to_move, move)

            opponent = -player_to_move
            score = alphabeta(new_board, opponent, depth - 1, alpha, beta)
            max_score = max(max_score, score)

            alpha = max(alpha, max_score)
            if alpha >= beta:
                break

        return max_score

    else:
        min_score = math.inf

        for move in valid_move:
            new_board = deepcopy(cur_state)
            make_move(new_board, 1, move)

            opponent = -player_to_move
            score = alphabeta(new_board, opponent, depth - 1, alpha, beta)
            min_score = min(min_score, score)

            beta = min(beta, min_score)
            if alpha >= beta:
                break

        return min_score


def get_best_move(cur_state, player_to_move, depth=5):
    best_move = None
    best_score = -math.inf
    alpha, beta = -math.inf, math.inf

    for move in get_valid_move(cur_state, player_to_move):
        new_board = deepcopy(cur_state)
        make_move(new_board, player_to_move, move)

        score = alphabeta(new_board, player_to_move, depth - 1, alpha, beta)
        if score > best_score:
            best_move, best_score = move, score

        alpha = max(alpha, best_score)

    return best_move


def select_move(cur_state, player_to_move, remain_time=1):
    return get_best_move(cur_state, player_to_move)
