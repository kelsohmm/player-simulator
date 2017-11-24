import random

class RandomAgent:
    def __init__(self, possible_keys, repo=None):
        self.possible_keys = possible_keys
        self.repo = repo

    def react_to_new_game_screen(self, state, score, time):
        action_idx = random.randint(0, len(self.possible_keys)-1)
        self.repo.commit(state, score, action_idx)

        return action_idx

    def finish(self, state, score):
        self.repo.close()