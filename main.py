import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
RED = (255, 0, 0)
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)

# Board
board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Fonts
END_FONT = pygame.font.SysFont('courier', 40)


def print_board(board):
    for row in board:
        print("|".join(row))
        print("-" * 5)


def check_winner(board):
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != ' ':
            return row[0]
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != ' ':
            return board[0][col]
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return board[0][2]
    return None


def is_board_full(board):
    for row in board:
        if ' ' in row:
            return False
    return True


def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == 'O':
        return 1
    elif winner == 'X':
        return -1
    elif is_board_full(board):
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    eval = minimax(board, depth + 1, False)
                    board[i][j] = ' '
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = math.inf
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    eval = minimax(board, depth + 1, True)
                    board[i][j] = ' '
                    min_eval = min(min_eval, eval)
        return min_eval


def find_best_move(board):
    best_move = None
    best_value = -math.inf
    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLS):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                move_value = minimax(board, 0, False)
                board[i][j] = ' '
                if move_value > best_value:
                    best_value = move_value
                    best_move = (i, j)
    return best_move


def draw_lines():
    # Horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Vertical lines
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)


def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE / 2),
                                                          int(row * SQUARE_SIZE + SQUARE_SIZE / 2)),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)


def draw_winner_line(board):
    winner = check_winner(board)
    if winner:
        # Horizontal line
        if board[0][0] == board[0][1] == board[0][2] == winner:
            pygame.draw.line(screen, RED, (0, SQUARE_SIZE / 2), (WIDTH, SQUARE_SIZE / 2), LINE_WIDTH)
        elif board[1][0] == board[1][1] == board[1][2] == winner:
            pygame.draw.line(screen, RED, (0, 3 * SQUARE_SIZE / 2), (WIDTH, 3 * SQUARE_SIZE / 2), LINE_WIDTH)
        elif board[2][0] == board[2][1] == board[2][2] == winner:
            pygame.draw.line(screen, RED, (0, 5 * SQUARE_SIZE / 2), (WIDTH, 5 * SQUARE_SIZE / 2), LINE_WIDTH)
        # Vertical line
        elif board[0][0] == board[1][0] == board[2][0] == winner:
            pygame.draw.line(screen, RED, (SQUARE_SIZE / 2, 0), (SQUARE_SIZE / 2, HEIGHT), LINE_WIDTH)
        elif board[0][1] == board[1][1] == board[2][1] == winner:
            pygame.draw.line(screen, RED, (3 * SQUARE_SIZE / 2, 0), (3 * SQUARE_SIZE / 2, HEIGHT), LINE_WIDTH)
        elif board[0][2] == board[1][2] == board[2][2] == winner:
            pygame.draw.line(screen, RED, (5 * SQUARE_SIZE / 2, 0), (5 * SQUARE_SIZE / 2, HEIGHT), LINE_WIDTH)
        # Diagonal lines
        elif board[0][0] == board[1][1] == board[2][2] == winner:
            pygame.draw.line(screen, RED, (0, 0), (WIDTH, HEIGHT), LINE_WIDTH)
        elif board[0][2] == board[1][1] == board[2][0] == winner:
            pygame.draw.line(screen, RED, (0, HEIGHT), (WIDTH, 0), LINE_WIDTH)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


def restart():
    screen.fill(BG_COLOR)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = ' '


# Game loop
player = 'X'
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and player == 'X':
            mouseX = event.pos[0]  # x
            mouseY = event.pos[1]  # y

            clicked_row = int(mouseY // SQUARE_SIZE)
            clicked_col = int(mouseX // SQUARE_SIZE)

            if board[clicked_row][clicked_col] == ' ':
                board[clicked_row][clicked_col] = player

                if check_winner(board):
                    game_over = True
                elif is_board_full(board):
                    game_over = True

                player = 'O'

        elif player == 'O' and not game_over:
            # AI's move
            ai_move = find_best_move(board)
            if ai_move:
                board[ai_move[0]][ai_move[1]] = 'O'

                if check_winner(board):
                    game_over = True
                elif is_board_full(board):
                    game_over = True

                player = 'X'

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                game_over = False
                player = 'X'

    screen.fill(BG_COLOR)
    draw_lines()
    draw_figures()
    draw_winner_line(board)

    if game_over:
        winner = check_winner(board)
        if winner:
            draw_text(f"{winner} wins! Press 'R' to restart", END_FONT, RED, screen, WIDTH // 2, HEIGHT // 2)
        else:
            draw_text("It's a draw! Press 'R' to restart", END_FONT, RED, screen, WIDTH // 2, HEIGHT // 2)

    pygame.display.update()
