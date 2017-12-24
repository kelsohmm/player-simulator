import logging

import numpy as np
from config import BATCH_SIZE, DISCOUNT_FACTOR, CONV_SHAPE, MIN_MEMORIES

END_GAME_REWARD = -1.0


class ModelTraining:
    def __init__(self, model, memories_repo):
        self.model = model
        self.repo = memories_repo
        self.no_outputs = len(model.outputs)

    def train(self):
        if self.repo.size() > MIN_MEMORIES:
            memories = self.repo.get_commits_batch(BATCH_SIZE)
            samples, labels = self._map_memories_to_train_data(memories)
            losses = self.model.train_on_batch(x=samples,
                                               y=np.split(labels, self.no_outputs, axis=1))
            logging.debug('TRAIN:    losses: %s, labels: %s' % (str(losses), str(list(labels.flatten()))))
            return losses
        else:
            return 0.

    def _map_memories_to_train_data(self, memories):
        no_memories = len(memories)
        samples = np.zeros((no_memories,) + CONV_SHAPE, dtype=np.ubyte)
        labels = np.zeros((no_memories, self.no_outputs))
        labels[:, :] = np.nan
        for idx in range(no_memories):
            prev_screen, action_idx, prev_score, next_score, next_screen = memories[idx]
            reward = self._calc_reward(prev_score, next_score)
            samples[idx] = prev_screen
            labels[idx, action_idx] = reward + (DISCOUNT_FACTOR * self._highest_reward(next_screen))
        return samples, labels

    def _highest_reward(self, next_screen):
        if next_screen is not None:
            predictions = np.concatenate(self.model.predict(next_screen.reshape((1,) + CONV_SHAPE))).flatten()
            return predictions.max()
        else:
            return 0.0

    def _calc_reward(self, prev_score, next_score):
        if next_score is None:
            return END_GAME_REWARD
        else:
            return np.sign(next_score - prev_score)
