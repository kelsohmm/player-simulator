import random


class RandomSavingAgent:
    def __init__(self, number_of_game_inputs, repo):
        self.no_inputs = number_of_game_inputs
        self.repo = repo

    def react_to_new_game_screen(self, screen_shot, score):
        inputs = [random.choice([0, 1]) for _ in range(self.no_inputs)]

        self.repo.commit(screen_shot, score, inputs)

        return inputs

    def finish(self, screen_shot, score):
        self.repo.close()