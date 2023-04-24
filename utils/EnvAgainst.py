from utils.Board import Board
from agents.human import HumanPlayer


class EnvAgainstPolicy:
    def __init__(self, env, policy, first_player=True):
        if policy:
            self.policy = policy
        self.env = env
        self.first_player = first_player
        self.reset()

    def step(self, action):
        self.env.step(action)
        print("2")
        obs, reward, terminated, _, _ = self.env.last()
        if terminated:
            self.last_step = obs, reward, True, False, {}
        else:
            action = self.policy.get_action(obs)
            self.env.step(action)
            print("3")
            obs, reward, terminated, _, _ = self.env.last()
            self.last_step = obs, -reward, terminated, False, {}
        return self.last_step

    def reset(self):
        self.env.reset()
        if not(self.first_player):
            # CAD 1rst player is human opponent
            obs, _, _, _, _ = self.env.last()
            action = self.policy.get_action(obs)
            self.board.drop_piece(self.board.board, self.board.get_next_row(
                self.board.board, action), action, 2)
            self.board.draw_board()
            print("1")
            self.step(action)
        self.last_step = self.env.last()
        return self.last_step

    def last(self):
        return self.last_step


class EnvAgainstHuman(EnvAgainstPolicy):
    def __init__(self, env, policy=None, first_player=True, board=None):
        self.board = board
        self.policy = HumanPlayer(name="faufau", board=board)
        self.first_player = first_player
        super().__init__(env, policy, first_player)

    def step(self, action):
        # q-learner plays
        self.env.step(action)
        self.board.drop_piece(self.board.board, self.board.get_next_row(
            self.board.board, action), action, 1)
        self.board.draw_board()
        obs, reward, terminated, _, _ = self.env.last()
        if terminated:
            self.last_step = obs, reward, True, False, {}
        else:
            # human plays
            action = self.policy.get_action(obs)
            self.env.step(action)
            self.board.drop_piece(self.board.board, self.board.get_next_row(
                self.board.board, action), action, 2)
            self.board.draw_board()
            obs, reward, terminated, _, _ = self.env.last()
            self.last_step = obs, -reward, terminated, False, {}
        return self.last_step
    
class EnvAgainstChat(EnvAgainstPolicy):
    def __init__(self, env, policy=None, first_player=True, board=None):
        self.board = board
        self.policy = HumanPlayer(name="faufau", board=board)
        self.first_player = first_player
        super().__init__(env, policy, first_player)

    def step(self, action):
        if self.first_player:
            # Q-learner plays
            print("action : ",action)
            print("board : ",self.board)
            print("env : ",self.env.step(action))
            self.env.step(action)
            obs, reward, terminated, _, _ = self.env.step(action)
            self.board.drop_piece(self.board.board, self.board.get_next_row(self.board.board, action), action, 1)
            self.board.draw_board()
        else:
            # Human plays
            obs = self.env.last()[0]
            action = self.policy.get_action(obs)
            if action is None:
                return obs, 0, True, False, {}
            obs, reward, terminated, _, _ = self.env.step(action)
            self.board.drop_piece(self.board.board, self.board.get_next_row(self.board.board, action), action, 2)
            self.board.draw_board()

        self.first_player = not self.first_player
        return obs, -reward, terminated, False, {}

