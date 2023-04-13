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


def get_new_state(cur_state, player, move):
    new_state = deepcopy(cur_state)
    make_move(new_state, player, move)
    return new_state


def alphabeta(cur_state, player, depth, alpha, beta, maximizing_player):
    valid_move = get_valid_move(cur_state, player)

    if depth == 0 or not valid_move:
        return evaluate(cur_state, player)

    # Nếu đang tìm kiếm cho người chơi tối đa (agent)
    if maximizing_player:
        max_val = -math.inf
        # Thử các nước đi có thể có
        for move in valid_move:
            # Tạo một trạng thái mới dựa trên nước đi hiện tại
            new_state = get_new_state(cur_state, player, move)

            # Tìm kiếm đệ quy trên trạng thái mới
            val = alphabeta(new_state, player, depth - 1, alpha, beta, False)

            # Cập nhật giá trị tối đa và alpha
            max_val = max(max_val, val)
            alpha = max(alpha, max_val)

            # Kiểm tra điều kiện cắt tỉa
            if beta <= alpha:
                break

        return max_val
    # Nếu đang tìm kiếm cho người chơi tối thiểu
    else:
        min_val = math.inf

        for move in valid_move:
            new_state = get_new_state(cur_state, player, move)

            val = alphabeta(new_state, player, depth - 1, alpha, beta, True)

            # Cập nhật giá trị tối thiểu và beta
            min_val = min(min_val, val)
            beta = min(beta, min_val)

            if beta <= alpha:
                break

        return min_val


def get_best_move(cur_state, player, depth=5):
    best_move = None
    best_score = -math.inf
    alpha, beta = -math.inf, math.inf

    for move in get_valid_move(cur_state, player):
        new_state = get_new_state(cur_state, player, move)
        score = alphabeta(new_state, player, depth - 1, alpha, beta, True)

        if score > best_score:
            best_move, best_score = move, score

        alpha = max(alpha, best_score)

    return best_move


def select_move(cur_state, player_to_move, remain_time=1):
    return get_best_move(cur_state, player_to_move)
