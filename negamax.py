import numpy as np


# CÁC HÀM CHUNG CỦA REVERSI
def is_valid_move(board, player, move):
    x, y = move

    if not board[x][y] == 0:
        return False

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    for d in directions:
        c, r = x + d[0], y + d[1]

        if 0 <= c < 8 and 0 <= r < 8 and board[c][r] == -player:
            c, r = c + d[0], r + d[1]

            while 0 <= c < 8 and 0 <= r < 8 and board[c][r] == -player:
                c, r = c + d[0], r + d[1]

            if 0 <= c < 8 and 0 <= r < 8 and board[c][r] == player:
                return True

    return False


def make_move(board, player, move):
    x, y = move
    board[x][y] = player

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

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


def get_valid_move(board, player):
    valid_moves = []
    for i in range(8):
        for j in range(8):
            if is_valid_move(board, player, (i, j)):
                valid_moves.append((i, j))
    return valid_moves


def get_score(board):
    score_dict = {-1: 0, 0: 0, 1: 0}
    for c in range(8):
        for r in range(8):
            score_dict[board[c][r]] += 1
    return score_dict


def is_game_over(board):
    score = get_score(board)

    # Trường hợp bàn cờ đã lắp đầy
    if score[1] + score[-1] == 64:
        return True

    # Trường hợp cả hai không có nước đi hợp lệ
    if not get_valid_move(board, 1) and not get_valid_move(board, -1):
        return True

    return False


# CÁC HÀM CHO AGENT
def evaluate(board, player):
    score = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == player:
                score += 1
            elif board[i][j] == -player:
                score -= 1
    return score


def negamax(board, player, depth, alpha, beta, trans_table):
    if depth == 0 or is_game_over(board):
        return evaluate(board, player)

    valid_moves = get_valid_move(board, player)
    if not valid_moves:
        return negamax(board, -player, depth - 1, -beta, -alpha, trans_table)

    best_score = -np.inf
    for move in valid_moves:
        new_board = np.copy(board)
        make_move(new_board, player, move)

        trans_key = hash(tuple(tuple(row) for row in new_board))
        if trans_key in trans_table:
            score = trans_table[trans_key]
        else:
            score = -negamax(new_board, -player, depth - 1, -beta, -alpha, trans_table)
            trans_table[trans_key] = score

        best_score = max(best_score, score)

        alpha = max(alpha, score)
        if alpha >= beta:
            break

    return best_score


def find_best_move(board, player, depth=5):
    alpha = -np.inf
    beta = np.inf

    trans_table = {}

    best_move = None
    best_score = -np.inf

    valid_moves = get_valid_move(board, player)

    for move in valid_moves:
        if move in [(0, 0), (0, 7), (7, 0), (7, 7)]:
            return move

    for move in valid_moves:
        new_board = np.copy(board)
        make_move(new_board, player, move)

        trans_key = hash(tuple(tuple(row) for row in new_board))
        if trans_key in trans_table:
            score = trans_table[trans_key]
        else:
            score = -negamax(new_board, -player, depth - 1, -beta, -alpha, trans_table)
            trans_table[trans_key] = score

        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def select_move(cur_state, player_to_move, remain_time=60):
    return find_best_move(cur_state, player_to_move)
