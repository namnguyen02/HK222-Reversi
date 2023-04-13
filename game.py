import pygame
from algorithm import is_valid_move, get_valid_move, make_move, get_score, select_move
import time


def check_game_over(board):
    score = get_score(board)

    # Trường hợp bàn cờ đã được lắp đầy
    if score[1] + score[-1] == 64:
        return (
            "Tie"
            if score[1] == score[-1]
            else "Black Wins"
            if score[1] > score[-1]
            else "White Wins"
        )

    # Trường hợp cả hai không có nước đi hợp lệ
    if not get_valid_move(board, 1) and not get_valid_move(board, -1):
        return "No valid move both. Tie."

    return None


# Thiết lập màu sắc, kích thước
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)

SQUARE = 80
MARGIN = 2
RADIUS = SQUARE / 2 - SQUARE / 10

WINDOW_SIZE = [SQUARE * 8 + MARGIN * 9, SQUARE * 8 + MARGIN * 9]


def draw_board(board, player, turn):
    for col in range(8):
        for row in range(8):
            # Vị trí của ô vuông
            x1 = (MARGIN + SQUARE) * col + MARGIN
            y1 = (MARGIN + SQUARE) * row + MARGIN

            # Tâm của quân cờ
            x2 = x1 + SQUARE / 2
            y2 = y1 + SQUARE / 2

            # Vẽ ô vuông
            pygame.draw.rect(screen, GREEN, (x1, y1, SQUARE, SQUARE))

            # Vẽ quân cờ
            if board[col][row] == 1:
                pygame.draw.circle(screen, BLACK, (x2, y2), RADIUS)
            elif board[col][row] == -1:
                pygame.draw.circle(screen, WHITE, (x2, y2), RADIUS)

            # Vẽ bước đi khả thi
            for c, r in get_valid_move(board, player):
                # Vị trí của ô vuông
                x = (MARGIN + SQUARE) * c + MARGIN
                y = (MARGIN + SQUARE) * r + MARGIN

                # Điểm bắt đầu và kết thúc của đoạn thẳng
                start_pos = (x + 3 * SQUARE / 8, y + SQUARE / 2)
                end_pos = (x + 5 * SQUARE / 8, y + SQUARE / 2)

                # Vẽ đoạn thẳng
                if player == 1 and turn == "B":
                    pygame.draw.line(screen, BLACK, start_pos, end_pos, 2)
                elif player == -1 and turn == "W":
                    pygame.draw.line(screen, WHITE, start_pos, end_pos, 2)

    # pygame.display.flip()
    pygame.display.update()


def get_position(pos):
    x, y = pos
    col = x // (MARGIN + SQUARE)
    row = y // (MARGIN + SQUARE)
    return col, row


if __name__ == "__main__":
    # Thiết lập bàn cờ và chế độ chơi
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
    turn = input("Choose your turn (B or W): ")
    f = open("agent_time.txt", "w")
    total_agent_time = 0

    # Khởi tạo game
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Reversi Game")

    done = False
    clock = pygame.time.Clock()

    if turn == "W":
        draw_board(board, player, turn)
        pygame.time.wait(500)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif turn == "B" and player == 1 or turn == "W" and player == -1:
                valid_move = get_valid_move(board, player)
                if valid_move:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        move = get_position(pos)
                        if is_valid_move(board, player, move):
                            make_move(board, player, move)
                            player = -player
                else:
                    print("Black" if player == 1 else "White", "has no valid move.")
                    player = -player
            elif turn == "B" and player == -1 or turn == "W" and player == 1:
                start_time = time.time()
                best_move = select_move(board, player)
                agent_time = round(time.time() - start_time, 6)
                total_agent_time += agent_time
                f.write(str(agent_time) + "\n")
                if best_move:
                    make_move(board, player, best_move)
                else:
                    print("Black" if player == 1 else "White", "has no valid move.")
                player = -player

        draw_board(board, player, turn)

        clock.tick(60)

        result = check_game_over(board)
        if result:
            print(result)
            done = True

    pygame.quit()

    f.write("Total: " + str(total_agent_time) + "\n")
    f.close()
