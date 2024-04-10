import pygame
from define import *
from ai import *

# setup Pygame

pygame.init()
screen = pygame.display.set_mode((400, 450))
pygame.display.set_caption("Reversi")



# Initialize the game (Reversi)

board = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, BLACK, WHITE, 0, 0, 0],
    [0, 0, 0, WHITE, BLACK, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

player_turn = BLACK


def reset_game():
    global board, player_turn
    board = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, BLACK, WHITE, 0, 0, 0],
        [0, 0, 0, WHITE, BLACK, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    player_turn = BLACK

def draw_board(board):
    counter = 0
    for y in range(8):
        for x in range(8):
            if board[y][x] == BLACK:
                counter += 1
                pygame.draw.circle(screen, (0, 0, 0), (x * 50 + 25, y * 50 + 25), 20)
            elif board[y][x] == WHITE:
                counter += 1
                pygame.draw.circle(screen, (200, 200, 200), (x * 50 + 25, y * 50 + 25), 20)

def check_if_game_over():
    global board

    if (get_valid_moves(board, player_turn) == []):
        return True

    for y in range(8):
        for x in range(8):
            if board[y][x] == 0:
                return False
    return True

def get_winner():
    global board
    black = 0
    white = 0
    for y in range(8):
        for x in range(8):
            if board[y][x] == BLACK:
                black += 1
            elif board[y][x] == WHITE:
                white += 1
    if black > white:
        return BLACK
    elif white > black:
        return WHITE
    else:
        return 0

def get_winner_score():
    global board
    black = 0
    white = 0
    for y in range(8):
        for x in range(8):
            if board[y][x] == BLACK:
                black += 1
            elif board[y][x] == WHITE:
                white += 1
    return abs(black - white)

def evaluate_board(board):
    b = 0
    w = 0
    for y in range(8):
        for x in range(8):
            if board[y][x] == BLACK:
                b += 1
            elif board[y][x] == WHITE:
                w += 1
    return b - w


def get_black_score(board):
    black = 0
    for y in range(8):
        for x in range(8):
            if board[y][x] == BLACK:
                black += 1
    return black

def get_white_score(board):
    white = 0
    for y in range(8):
        for x in range(8):
            if board[y][x] == WHITE:
                white += 1
    return white

def get_open_cells(board):
    open_cells = []
    for y in range(8):
        for x in range(8):
            if board[y][x] == 0:
                open_cells.append((x, y))
    return open_cells

def get_board():
    global board
    return board

def get_valid_dir(board, coord, dir, player_turn):
    x, y = coord
    dx, dy = dir
    x += dx
    y += dy
    past_1 = False
    change = []
    while 0 <= x < 8 and 0 <= y < 8:
        if board[y][x] == 0 or board[y][x] == player_turn and not past_1:
            return False
        if board[y][x] == player_turn and past_1:
            return change
        change.append((x, y))
        x += dx
        y += dy
        past_1 = True
    return False


def get_valid_moves(board, player):
    valid_moves = []
    for y in range(8):
        for x in range(8):
            if board[y][x] != 0:
                continue
            
            valid = False
            change = []
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dy == 0 and dx == 0:
                        continue

                    dir = get_valid_dir(board, (x, y), (dx, dy), player)
                    
                    if dir != False:
                        valid = True
                        change += dir
            
            if valid:
                valid_moves.append(((x, y), change))

    return valid_moves


def check_click_player(x, y):
    global player_turn
    for i in get_valid_moves(board, player_turn):
        if (x, y) == i[0]:
            board[y][x] = player_turn
            for j in i[1]:
                board[j[1]][j[0]] = player_turn
            player_turn = BLACK if player_turn == WHITE else WHITE
            break

def get_click_ai(net):
    global player_turn, board
    boards = []
    valid_moves = get_valid_moves(board, player_turn)
    for i in valid_moves:
        board_copy = [row.copy() for row in board]
        x, y = i[0]
        board_copy[y][x] = player_turn
        for j in i[1]:
            board_copy[j[1]][j[0]] = player_turn
        boards.append(board_copy)
    
    best_move = get_best_move(boards, net)

    for i in valid_moves[best_move][1]:
        board[i[1]][i[0]] = player_turn
    x, y = valid_moves[best_move][0]
    board[y][x] = player_turn

    player_turn = BLACK if player_turn == WHITE else WHITE

def get_player_turn():
    return player_turn

def switch_player_turn():
    global player_turn
    player_turn = BLACK if player_turn == WHITE else WHITE
    
def make_move(board, player_turn, move):

    x, y = move[0]

    board[y][x] = player_turn
    for i in move[1]:
        board[i[1]][i[0]] = player_turn
    
    return board


def display_score():
    black_score = get_black_score(board)
    white_score = get_white_score(board)
    font = pygame.font.Font(None, 36)
    text = font.render("Black: " + str(black_score) + " White: " + str(white_score), True, (0, 0, 0))
    screen.blit(text, (0, 410))

def draw_ai_move(move):
    pygame.draw.circle(screen, (255, 0, 0), (move[0] * 50 + 25, move[1] * 50 + 25), 5)
    