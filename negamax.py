import bisect
from copy import deepcopy
import math


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
def get_new_board(board, player, move):
    new_board = deepcopy(board)
    make_move(new_board, player, move)
    return new_board


def evaluate(board, player):
    score = 0

    count = get_score(board)
    player_count = count[player]
    opponent_count = count[-player]

    if player_count > opponent_count:
        score += (player_count - opponent_count) * 10
    elif player_count < opponent_count:
        score -= (opponent_count - player_count) * 10

    # position_values = [
    #     [100, -20, 10, 5, 5, 10, -20, 100],
    #     [-20, -50, -2, -2, -2, -2, -50, -20],
    #     [10, -2, -1, -1, -1, -1, -2, 10],
    #     [5, -2, -1, -1, -1, -1, -2, 5],
    #     [5, -2, -1, -1, -1, -1, -2, 5],
    #     [10, -2, -1, -1, -1, -1, -2, 10],
    #     [-20, -50, -2, -2, -2, -2, -50, -20],
    #     [100, -20, 10, 5, 5, 10, -20, 100],
    # ]

    # for i in range(8):
    #     for j in range(8):
    #         if board[i][j] == player:
    #             score += position_values[i][j]
    #         elif board[i][j] == -player:
    #             score -= position_values[i][j]

    return score


def get_move_priority(move):
    """Tính độ ưu tiên của một nước đi"""

    # Các nước đi ở giữa bàn cờ có độ ưu tiên cao hơn
    x, y = move
    priority = abs(x - 3.5) + abs(y - 3.5)

    # Nếu nước đi góc hoặc cạnh, độ ưu tiên thấp hơn
    if x == 0 or x == 7 or y == 0 or y == 7:
        priority -= 1

    return priority


def order_moves(moves):
    """Sắp xếp các nước đi dựa trên độ ưu tiên"""
    ordered_moves = []
    for move in moves:
        priority = get_move_priority(move)
        bisect.insort(ordered_moves, (priority, move))
    return [move for _, move in ordered_moves]


def negamax(board, player, depth, alpha, beta, color, transposition_table):
    # Kiểm tra trạng thái đã được tính toán trước đó trong Transposition table
    transposition_key = hash(tuple(tuple(row) for row in board))
    if transposition_key in transposition_table:
        return transposition_table[transposition_key]

    # Nếu độ sâu bằng 0 hoặc bàn cờ đã kết thúc, tính giá trị heuristic và trả về kết quả
    if depth == 0 or is_game_over(board):
        return color * evaluate(board, player)

    best_value = -math.inf
    for move in order_moves(get_valid_move(board, player)):
        new_board = get_new_board(board, player, move)

        value = -negamax(
            new_board, player, depth - 1, -beta, -alpha, -color, transposition_table
        )

        # Nếu giá trị tốt hơn giá trị tốt nhất hiện tại, cập nhật giá trị tốt nhất
        if value > best_value:
            best_value = value

        # Cập nhật giá trị alpha
        alpha = max(alpha, value)

        # Kiểm tra điều kiện cắt Alpha-beta pruning
        if alpha >= beta:
            break

    # Lưu trạng thái vào Transposition table
    transposition_table[transposition_key] = best_value
    return best_value


def get_best_move(board, player, depth=5):
    alpha = -math.inf
    beta = math.inf

    transposition_table = {}

    best_move = None
    best_value = -math.inf

    for move in order_moves(get_valid_move(board, player)):
        new_board = get_new_board(board, player, move)

        value = negamax(
            new_board, player, depth - 1, -beta, -alpha, -1, transposition_table
        )
        value = -value

        # Nếu giá trị tốt hơn giá trị tốt nhất hiện tại, cập nhật giá trị tốt nhất và nước đi tốt nhất
        if value > best_value:
            best_value = value
            best_move = move

        # Cập nhật giá trị alpha
        alpha = max(alpha, value)

    return best_move


def select_move(cur_state, player_to_move, remain_time=1):
    return get_best_move(cur_state, player_to_move)
