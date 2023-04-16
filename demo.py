from negamax import get_valid_move, make_move, get_score, select_move
import time
import random


def display_board(board):
    result = "  a b c d e f g h\n"
    for i in range(8):
        result += str(i + 1) + "|"
        for j in range(8):
            if board[i][j] == 1:
                result += "\u25CF|"
            elif board[i][j] == -1:
                result += "\u25CB|"
            else:
                result += " |"
        result += "\n"
    return result


def check_game_over(board):
    score = get_score(board)
    result = (
        "Tie"
        if score[1] == score[-1]
        else "Black Wins"
        if score[1] > score[-1]
        else "White Wins"
    )

    # Trường hợp bàn cờ đã được lắp đầy
    if score[1] + score[-1] == 64:
        return result

    # Trường hợp cả hai không có nước đi hợp lệ
    if not get_valid_move(board, 1) and not get_valid_move(board, -1):
        return "No valid move both. " + result

    return None


if __name__ == "__main__":
    board = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, -1, 1, 0, 0, 0],
        [0, 0, 0, 1, -1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]

    player = 1
    remain_time = 60.0

    turn = input("Choose color for agent (b or w): ")
    ft = open("time.txt", "w")
    fd = open("demo.txt", "w")

    fd.write(display_board(board) + "\n")

    while True:
        if turn == "b" and player == -1 or turn == "w" and player == 1:
            valid_move = get_valid_move(board, player)
            if valid_move:
                make_move(board, player, random.choice(valid_move))
            else:
                print("Black" if player == 1 else "White", "has no valid move.")
            player = -player
        elif turn == "b" and player == 1 or turn == "w" and player == -1:
            start_time = time.perf_counter()
            best_move = select_move(board, player, remain_time)
            agent_time = time.perf_counter() - start_time
            remain_time -= agent_time
            ft.write(str(agent_time) + "\n")
            if best_move:
                make_move(board, player, best_move)
            else:
                print("Black" if player == 1 else "White", "has no valid move.")
            player = -player

        fd.write(display_board(board) + "\n")

        result = check_game_over(board)
        if result:
            print(result)
            break

    ft.write("Total: " + str(60.0 - remain_time) + "\n")
    ft.close()
    fd.close()
