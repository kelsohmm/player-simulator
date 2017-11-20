import random

class RandomAgent:
    def __init__(self, possible_keys, repo=None):
        self.possible_keys = possible_keys
        self.repo = repo

    def react_to_new_game_screen(self, screen_shot, score, time):
        action_idx = random.randint(0, len(self.possible_keys)-1)
        self.repo.commit(screen_shot, score, action_idx, time)

        return action_idx

    def finish(self, screen_shot, score):
        self.repo.close()