import logging
import random
from config import CONV_SHAPE, MIN_MEMORIES, EXPLORATION_FACTOR


class NeuralNetworkAgent:
    def __init__(self, model, repo):
        self.model = model
        self.repo = repo

    def react_to_new_game_screen(self, state, score):
        predictions = self.model.predict(state.reshape((1,) + CONV_SHAPE))
        action_idx = self._choose_action_idx(predictions)
        self.repo.commit(state, score, action_idx, predictions.tolist()[0])

        logging.debug('AGENT:   Rewards: %s, Chose: %s', str(list(predictions)), action_idx)
        return action_idx

    def _choose_action_idx(self, predictions):
        if random.uniform(0., 1.) < EXPLORATION_FACTOR or self.repo.size() <= MIN_MEMORIES:
            return random.randint(0, 5)
        else:
            return predictions.argmax()

    def finish(self):
        self.repo.close()
