from agents.human import HumanPlayer
from agents.q_learner import QLearningAgent
import pickle
import pygame
import numpy as np
from utils.EnvAgainst import EnvAgainstHuman, EnvAgainstChat
from utils.Board import Board
from pettingzoo.classic import connect_four_v3

env = connect_four_v3.env(render_mode="rgb_array")
env.reset()


def game_user_player_come(env, agent):
    board = Board()

    # Game loop
    # also creates the human object
    # if first_player: le q-player commence
    # sinon: l'humain commence
    first_player = True
    eval_env = EnvAgainstChat(env, first_player=first_player, board=board)
    print("eval_env created")
    player = HumanPlayer(name="faufau",board=board) if first_player else agent
    print('our player is {}'.format(player))
    done = False
    eval_env.reset()
    obs, _, _, _, _ = eval_env.last()
    print("let's get the last status of the board")
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if isinstance(player, HumanPlayer):
            # Human plays
            print("human plays")
            action = player.get_action(obs)
            next_obs, reward, done, _, _ = eval_env.last()
            print('next_obs created')
        else:
            # Q-agent plays
            print("Q-agent plays")
            print("PLAYER :",player)
            action = player.get_action(obs, epsilon=0)
            print("ACTION FROM AGENT : ",action)
            if action is None:
                # The agent cannot play: draw?
                return 0
            eval_env.step(action)
            next_obs, reward, done, _, _ = eval_env.last()
        
            if isinstance(player, QLearningAgent):
                player.update(obs, action, reward, done, next_obs)
        
        if done and reward == 1:
            # L'agent a gagné
            return 1 if isinstance(player, QLearningAgent) else -1
        elif done and reward == -1:
            # L'agent a perdu
            return -1 if isinstance(player, QLearningAgent) else 1
        print("update obs")
        obs = next_obs
        
        # On échange les rôles
        print("let's change roles")
        first_player = not first_player
        player = agent if isinstance(player, HumanPlayer) else HumanPlayer(name="faufau",board = board)
            


    # Quit Pygame
    pygame.quit()

    # The game ended in a draw
    return 0

def game_user_player(env, agent):
    board = Board()

    # Game loop
    # also creates the human object
    # if first_player: le q-player commence
    # sinon: l'humain commence
    eval_env = EnvAgainstHuman(env, first_player=True, board=board)
    done = False
    eval_env.reset()
    obs, _, _, _, _ = eval_env.last()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
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
                # Quit Pygame
                pygame.quit()
                return 1
            elif done and reward == -1:
                # The agent lost
                # Quit Pygame
                pygame.quit()
                return -1
            obs = next_obs

    # Quit Pygame
    pygame.quit()

    # The game ended in a draw
    return 0

import matplotlib.pyplot as plt

def train_from_human(env, agent, N_episodes=20, N_games=20):
    # 
    # We print the evolution of the agent's statistics, and at the end we plot the evolution of the win rate
    print(f"{'Episode':<10} {'Win':<10} {'Loss':<10} {'Draw':<10}")
    win_rate = []
    for i in range(N_episodes):
        win = 0
        loss = 0
        draw = 0
        for _ in range(N_games):
            result = game_user_player(env, agent)
            if result == 1:
                win += 1
            elif result == -1:
                loss += 1
            else:
                draw += 1
        print(f"{i:<10} {win:<10} {loss:<10} {draw:<10}")
        win_rate.append(win / N_games)

    plt.plot(win_rate)
    #calculate equation for trendline
    x = np.linspace(0, N_episodes-1, N_episodes)
    z = np.polyfit(x, win_rate, 1)
    p = np.poly1d(z)
    #add trendline to plot
    plt.plot(x, p(x))
    #legends
    plt.xlabel("Episode")
    plt.ylabel("Win rate")
    plt.title("Evolution of the win rate for {} against human player".format(agent.name))
    plt.show()


q_learning_agent = QLearningAgent()
with open("training/agent_q_learner.pkl", 'rb') as f:
    q_learning_agent.q_table = pickle.load(f)



train_from_human(env, q_learning_agent)

# game_user_player_come(env, q_learning_agent)