import pygame
from time import sleep
from game import *
from define import *
from minimax import *
import pickle


def eval_genomes(genomes, config):
    print("Evaluating genomes")
    print(get_board())
    print(get_player_turn())
    
    nets = []
    g = []
    for genome_id, genome in genomes:
        nets.append(neat.nn.FeedForwardNetwork.create(genome, config))
        g.append(genome)
        genome.fitness = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # Check for mouse click
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     x, y = pygame.mouse.get_pos()
            #     x = x // 50
            #     y = y // 50
            #     if get_player_turn() == RED:
            #         check_click_player(x, y)
            #     else:
            #         get_click_ai(nets)
        if check_if_game_over():
            winner = get_winner()
            score = abs(get_winner_score())
            print("Winner is", winner, "with score", score)
            if winner == RED:
                g[0].fitness += score
            elif winner == BLUE:
                g[1].fitness += score
            else:
                g[0].fitness += score
                g[1].fitness += score
            reset_game()
            break
        elif AI:
            if get_player_turn() == RED:
                get_click_ai(nets[0])
            else:
                get_click_ai(nets[1])
                

        # if get_player_turn() == RED: print("Red's turn")
        # else: print("Blue's turn")

        screen.fill((255, 255, 255))
        draw_board(get_board())
        for i in get_valid_moves(get_board(), get_player_turn()):
            x, y = i[0]
            pygame.draw.circle(screen, (0, 255, 0), (x * 50 + 25, y * 50 + 25), 5)

        pygame.display.flip()

        sleep(0.01)


def play_minimax():
    turn = None
    while True:
        if check_if_game_over():
            print("GAME OVER")

            screen.fill((255, 255, 255))
            draw_board(get_board())
            if AI and turn != None: draw_ai_move(turn[0])
            display_score()
            for i in get_valid_moves(get_board(), get_player_turn()):
                x, y = i[0]
                pygame.draw.circle(screen, (0, 255, 0), (x * 50 + 25, y * 50 + 25), 5)

            pygame.display.flip()

            while True:
                 for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

            break
        elif AI:
            if get_player_turn() == AI_MOVES:
                turn = minimax(get_board(), AI_DEPTH, AI_MOVES, INT_MIN, INT_MAX)[1]
                make_move(get_board(), AI_MOVES, turn)
                switch_player_turn()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # Get Mouse Click
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x = x // 50
                y = y // 50
                if get_player_turn() == PLAYER_MOVES:
                    check_click_player(x, y)    
       
            # else:
            #     turn = minimax(get_board(), 6, BLACK, INT_MIN, INT_MAX)[1]
            #     print(turn)
            #     make_move(get_board(), BLACK, turn)
                # switch_player_turn()
            
                

        # if get_player_turn() == RED: print("Red's turn")
        # else: print("Blue's turn")

        screen.fill((255, 255, 255))
        draw_board(get_board())
        if AI and turn != None: draw_ai_move(turn[0])
        display_score()
        for i in get_valid_moves(get_board(), get_player_turn()):
            x, y = i[0]
            pygame.draw.circle(screen, (0, 255, 0), (x * 50 + 25, y * 50 + 25), 5)

        pygame.display.flip()

        sleep(0.01)

# p = setup_ai()

# winner = p.run(eval_genomes, 1000)
# print('\nBest genome:\n{!s}'.format(winner))
# pickle.dump(winner,open("best.pickle", "wb"))


play_minimax()