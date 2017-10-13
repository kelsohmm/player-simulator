import random


class RandomAgent:
    def __init__(self, number_of_game_inputs):
        self.no_inputs = number_of_game_inputs

    def react_to_new_game_screen(self, screen_shot):
        return [random.choice([0, 1]) for _ in range(self.no_inputs)]
