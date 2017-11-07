import random
from image_transformations import resize_128

class RandomAgent:
    def __init__(self, possible_keys, repo=None):
        self.possible_keys = possible_keys
        self.repo = repo

    def react_to_new_game_screen(self, screen_shot, score, time):
        inputs = random.choice(self.possible_keys)
        screen = resize_128(screen_shot)
        self.repo.commit(screen, score, inputs, time)

        return inputs

    def finish(self, screen_shot, score):
        self.repo.close()