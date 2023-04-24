import numpy as np
import random as rd
import utils as u

def is_blunder(board, i):
    'This function check if tthere is a win in one move for the opponent'
    is_blunder = False
    board_after_i = u.new_move(board, i)
    board_after_i_for_opponent = - board_after_i
    for i in range(7):
        if board_after_i_for_opponent[0,i] == 0:
            if u.get_move_score(board_after_i_for_opponent, i) > 500 :
                is_blunder = True
    return is_blunder

def get_move_score_with_blunder(board, i, random_percentage):
    if is_blunder(board, i):
        return -1000
    if rd.random() < random_percentage:
        return - 10
    return u.get_move_score(board, i)

class MalynxAvoidingBlunder:
    def __init__(self, random_percentage = 0):
        self.name = "Malynx Avoiding Blunder"
        self.random_percentage = random_percentage
    def get_action(self, obs_mask, epsilon=None):
        if np.sum(obs_mask['observation']) == 0:
            return 3
        if np.sum(obs_mask['observation']) == 3:
            for i in range(7):
                if np.sum(obs_mask['observation'][:i]) == 2:
                    if i < 4:
                        return i + 1
                    return i-1
        board = obs_mask['observation'][:, :, 0]- obs_mask['observation'][:, :, 1]
        best_move_score = - 10000
        best_move = []
        for i, legal in enumerate(obs_mask["action_mask"]):
            if legal:
                move_score = get_move_score_with_blunder(board, i, self.random_percentage)
                if move_score == best_move_score:
                    best_move.append(i)
                if move_score > best_move_score:
                    best_move_score = move_score
                    best_move = [i]
        return rd.choice(best_move)