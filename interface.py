from agents.human import HumanPlayer
from agents.q_learner import QLearningAgent
import pickle
import pygame
import numpy as np
from utils.EnvAgainst import EnvAgainstHuman
from utils.Board import Board
from pettingzoo.classic import connect_four_v3

env = connect_four_v3.env(render_mode="rgb_array")
env.reset()


def game_user_player(env, agent):
    board = Board()
    board.draw_board()

    # also creates the human object
    # if true, you play yellow
    eval_env = EnvAgainstHuman(env, first_player=False, board=board)
    done = False
    eval_env.reset()
    obs, _, _, _, _ = eval_env.last()

    # Game loop
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Our q-learner agent plays
                action = agent.get_action(obs, epsilon=0)
                if action is None:
                    # The agent cannot play: draw?
                    return 0
                eval_env.step(action)
                next_obs, reward, done, _, _ = eval_env.last()
                # We update the agent's Q-table
                agent.update(obs, action, reward, done, next_obs)

                if done and reward == 1:
                    # The agent won
                    return 1
                elif done and reward == -1:
                    # The agent lost
                    return -1

                obs = next_obs

    # Quit Pygame
    pygame.quit()

    # The game ended in a draw
    return 0


q_learning_agent = QLearningAgent()
with open("training/agent_q_learner.pkl", 'rb') as f:
    q_learning_agent.q_table = pickle.load(f)

game_user_player(env, q_learning_agent)
