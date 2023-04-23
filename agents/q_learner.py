import random
import numpy as np

class QLearningAgent:
    def __init__(self, alpha=0.5, epsilon=0.1, gamma=0.99, epsilon_min=0.00001, epsilon_step=0.001):
        self.name = "Q-Learning Agent"
        self.q_table = {}
        self.alpha = alpha # learning rate
        self.epsilon = epsilon # exploration rate
        self.gamma = gamma # discount rate
        self.rng = np.random.default_rng() # random number generator

        self.epsilon_min = epsilon_min
        self.epsilon_step = epsilon_step

    def get_action(self, obs_mask, epsilon=None):
        if epsilon is None:
            epsilon = self.epsilon
        if random.random() < epsilon:
            return self.random_choice_with_mask(np.arange(7), obs_mask["action_mask"])
        else:
            return self.best_choice_with_mask(np.arange(7), obs_mask["action_mask"], obs_mask["observation"])

    def random_choice_with_mask(self, arr, mask):
        masked_arr = np.ma.masked_array(arr, mask=1 - mask)
        if masked_arr.count() == 0:
            return None
        return self.rng.choice(masked_arr.compressed())
    
    def best_choice_with_mask(self, arr, mask, obs):
        """
        Selects the action with the highest Q-value
        """
        masked_arr = np.ma.masked_array(arr, mask=1 - mask)
        if masked_arr.count() == 0:
            return None
        q_values = [self.q_table.get((tuple(obs.flatten()), action), 0) for action in masked_arr.compressed()]
        max_q = max(q_values)
        choice = np.random.choice([action for action, q in zip(masked_arr.compressed(), q_values) if q == max_q])
        return choice

    def update(self, state, action, reward, done, next_state):
        obs = state["observation"]
        next_obs = next_state["observation"]

        if (tuple(obs.flatten()), action) not in self.q_table:
            self.q_table[(tuple(obs.flatten()), action)] = 0

        if (tuple(next_obs.flatten()), action) not in self.q_table:
            self.q_table[(tuple(next_obs.flatten()), action)] = 0

        # Q-learning update
        q_next = max([self.q_table.get((tuple(next_obs.flatten()), a), 0) for a in range(7)])
        self.q_table[(tuple(obs.flatten()), action)] += self.alpha * (reward + self.gamma * q_next - self.q_table[(tuple(obs.flatten()), action)])

        self.epsilon_decay()
        
    def epsilon_decay(self):
        self.epsilon = max(self.epsilon - self.epsilon_step, self.epsilon_min)