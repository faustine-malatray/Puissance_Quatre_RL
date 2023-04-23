import numpy as np

import pygame


class HumanPlayer:
    def __init__(self, name=None, board=None):
        self.name = name if name is not None else input("Enter your name: ")
        if board:
            self.board = board

    def get_action(self, obs_mask=None, epsilon=None):
        if np.where(obs_mask["action_mask"] == 1)[0] == []:
            print("You cannot play")
            return None
        controle = True
        while controle:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                return 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                action = int(posx // self.board.SQUARE_SIZE)
                if self.board.is_valid_move(self.board.board, action):
                    return action
