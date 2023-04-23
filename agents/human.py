import numpy as np

import pygame


class HumanPlayer:
    def __init__(self, name=None, board=None):
        self.name = name if name is not None else input("Enter your name: ")
        if board:
            self.board = board

    def get_action(self, obs_mask=None, epsilon=None):
        # if np.where(obs_mask["action_mask"] == 1)[0] == []:
        #     print("You cannot play")
        #     return None
        # print("Action mask (moves available): ", obs_mask["action_mask"])
        # action = int(input("Enter your action (a number between 0 and 6): "))
        # while action not in np.where(obs_mask["action_mask"] == 1)[0]:
        #     print("Invalid action")
        #     action = int(
        #         input("Enter your action (a number between 0 and 6): "))

        # return action

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get the column that the user clicked
                posx = event.pos[0]
                col = int(posx // self.board.SQUARE_SIZE)

                # Make the move if it's valid
                if self.board.is_valid_move(self.board, col):
                    return col
                else:
                    # unvalid move
                    return 0
