import numpy as np
import copy
from define import *
from game import *


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

turn = RED

print(get_valid_moves(board, turn))

def minimax1(board, depth, maximizingPlayer):
    print("Depth: ", depth, "Maximizing: ", maximizingPlayer)
    if depth == 0:
        print("Depth reached: ", get_red_score(board) - get_blue_score(board))
        return get_red_score(board) - get_blue_score(board)
    if maximizingPlayer:
        maxEval = INT_MIN
        for move in get_valid_moves(board.copy(), RED):
            new_board = make_move(board.copy(), RED, move)
            if depth == 3:
                print("Depth: ", depth)
                print(new_board)
            eval = minimax(new_board.copy(), depth - 1, False)
            if eval > maxEval:
                maxEval = eval
        print("Maximize: ", maxEval)
        return maxEval
    else:
        minEval = INT_MAX
        for move in get_valid_moves(board.copy(), BLUE):
            new_board = make_move(board.copy(), BLUE, move)
            eval = minimax(new_board.copy(), depth - 1, True)
            if eval < minEval:
                minEval = eval
        print("Minimize: ", minEval)
        return minEval
    
def pre_compute_moves(board, depth, player, tree):
    if depth == 0:
        return [get_red_score(board) - get_blue_score(board)]

    if player == RED:
        valid_moves = get_valid_moves(board, RED)
        for move in valid_moves:
            new_board = make_move(board.copy(), RED, move)

            tree.append(pre_compute_moves(new_board, depth - 1, BLUE, tree))
    else:
        valid_moves = get_valid_moves(board, BLUE)
        for move in valid_moves:
            new_board = make_move(board.copy(), BLUE, move)

            tree.append(pre_compute_moves(new_board, depth - 1, RED, tree))

    return tree


def minimax(board, depth, player, alpha, beta):
    if depth == 0:
        return evaluate_board(board), None


    possible_moves = get_valid_moves(board, player)
    if len(possible_moves) == 0:
        return evaluate_board(board), None
    

    if player == BLACK:
        best_value = float("-inf")
        best_move = None
        for move in possible_moves:
            new_board = copy.deepcopy(board)
            make_move(new_board, BLACK, move)
            value, _ = minimax(new_board, depth - 1, WHITE, alpha, beta)
            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, best_value)
            if alpha >= beta:
                break
        return best_value, best_move
    else:
        best_value = float("inf")
        best_move = None
        for move in possible_moves:
            new_board = copy.deepcopy(board)
            make_move(new_board, WHITE, move)
            value, _ = minimax(new_board, depth - 1, BLACK, alpha, beta)
            if value < best_value:
                best_value = value
                best_move = move
            beta = min(beta, best_value)
            if alpha >= beta:
                break
        return best_value, best_move       
    
