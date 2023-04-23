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
        obs, reward, terminated, _, _ = self.env.last()
        if terminated:
            self.last_step = obs, reward, True, False, {}
        else:
            action = self.policy.get_action(obs)
            self.env.step(action)
            obs, reward, terminated, _, _ = self.env.last()
            self.last_step = obs, -reward, terminated, False, {}
        return self.last_step

    def reset(self):
        self.env.reset()
        if not(self.first_player):
            # CAD 1rst player is q-learner
            obs, _, _, _, _ = self.env.last()
            action = self.policy.get_action(obs)
            self.env.step(action)

        self.last_step = self.env.last()
        return self.last_step

    def last(self):
        return self.last_step


class EnvAgainstHuman(EnvAgainstPolicy):
    def __init__(self, env, policy=None, first_player=True):
        super().__init__(env, policy, first_player)
        self.board = Board()
        self.policy = HumanPlayer(name="faufau", board=self.board)

    def step(self, action):
        self.env.step(action)
        self.board.draw_board()
        obs, reward, terminated, _, _ = self.env.last()
        if terminated:
            self.last_step = obs, reward, True, False, {}
        else:
            action = self.policy.get_action(obs)
            self.env.step(action)
            self.board.draw_board()
            obs, reward, terminated, _, _ = self.env.last()
            self.last_step = obs, -reward, terminated, False, {}
        return self.last_step
