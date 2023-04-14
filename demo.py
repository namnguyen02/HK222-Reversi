from negamax import get_valid_move, make_move, get_score, select_move
import time
import random


def display_board(board):
    print("   ", end="")
    for i in range(8):
        print(i + 1, "  ", end="")
    print()
    print("  +---+---+---+---+---+---+---+---+")
    for i in range(8):
        print(chr(ord("a") + i), "|", end="")
        for j in range(8):
            if board[i][j] == 1:
                print(" X ", end="|")
            elif board[i][j] == -1:
                print(" O ", end="|")
            else:
                print("   ", end="|")
        print("\n  +---+---+---+---+---+---+---+---+")


def check_game_over(board):
    score = get_score(board)

    # Trường hợp bàn cờ đã được lắp đầy
    if score[1] + score[-1] == 64:
        return (
            "Tie"
            if score[1] == score[-1]
            else "Player X Wins"
            if score[1] > score[-1]
            else "Player O Wins"
        )

    # Trường hợp cả hai không có nước đi hợp lệ
    if not get_valid_move(board, 1) and not get_valid_move(board, -1):
        return "No valid move both. Tie."

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
    total_agent_time = 0

    turn = input("Choose turn for agent (X or O): ")
    f = open("time.txt", "w")

    # display_board(board)

    while True:
        if turn == "X" and player == -1 or turn == "O" and player == 1:
            valid_move = get_valid_move(board, player)
            if valid_move:
                make_move(board, player, random.choice(valid_move))
            else:
                print("Player X" if player == 1 else "Player O", "has no valid move.")
            player = -player
        elif turn == "X" and player == 1 or turn == "O" and player == -1:
            start_time = time.time()
            best_move = select_move(board, player)
            agent_time = round(time.time() - start_time, 6)
            total_agent_time += agent_time
            f.write(str(agent_time) + "\n")
            if best_move:
                make_move(board, player, best_move)
            else:
                print("Player X" if player == 1 else "Player O", "has no valid move.")
            player = -player

        # display_board(board)

        result = check_game_over(board)
        if result:
            print(result)
            break

    f.write("\nTotal: " + str(round(total_agent_time, 6)) + "\n")
    f.close()
