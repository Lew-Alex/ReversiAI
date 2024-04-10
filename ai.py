import neat
from game import *


def setup_ai():
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                'config-feedforward.txt')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())
    return p

def get_best_move(boards, net):
    best_score = -1000
    best_move = 0
    for board in boards:
        total_board = []
        for rows in board:
            total_board += rows
            
        score = net.activate((total_board))[0]

        if score > best_score:
            best_score = score
            best_move = boards.index(board)
    return best_move