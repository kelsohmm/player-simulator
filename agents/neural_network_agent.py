import logging
import random
import numpy as np
from config import CONV_SHAPE


class NeuralNetworkAgent:
    def __init__(self, model, repo):
        self.model = model
        self.repo = repo

    def react_to_new_game_screen(self, state, score):
        predictions = self.predict_rewards(state.as_matrix())
        action_idx = self._choose_action_idx(predictions)
        self.repo.commit(state, score, action_idx)

        logging.debug('Rewards: %s, Chose: %s', str(predictions), action_idx)
        return action_idx

    def _choose_action_idx(self, predictions):
        if random.uniform(0., 1.) < 0.05 or self.repo.size() < 10000:
            return random.randint(0, 5)
        else:
            return predictions.argmax()

    def finish(self, state, score):
        self.repo.close()

    def predict_rewards(self, state):
        raw_predicts = self.model.predict(state.reshape((1,) + CONV_SHAPE))
        return np.concatenate(raw_predicts).flatten()