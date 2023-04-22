import numpy as np

class HumanPlayer:
    def __init__(self, name=None):
        self.name = name if name is not None else input("Enter your name: ")

    def get_action(self, obs_mask, epsilon=None):
        if np.where(obs_mask["action_mask"] == 1)[0] == []:
            print("You cannot play")
            return None
        print("Action mask (moves available): ", obs_mask["action_mask"])
        action = int(input("Enter your action (a number between 0 and 6): "))
        while action not in np.where(obs_mask["action_mask"] == 1)[0]:
            print("Invalid action")
            action = int(input("Enter your action (a number between 0 and 6): "))

        return action