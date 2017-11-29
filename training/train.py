import logging

import numpy as np
from config import BATCH_SIZE, DISCOUNT_FACTOR, CONV_SHAPE, MIN_MEMORIES

CALIBRATION_BATCH_SIZE = MIN_MEMORIES
CALIBRATION_EPOCHS = 500

class ModelTraining:
    def __init__(self, model, memories_repo):
        self.model = model
        self.repo = memories_repo
        self.no_outputs = 6
        self.calibrated = False

    def train(self):
        if self.repo.size() > MIN_MEMORIES:
            if not self.calibrated:
                self._calibrate_network()
            memories = self.repo.get_commits_batch_with_last(BATCH_SIZE)
            samples, labels = self._map_memories_to_train_data(memories)
            loss = self.model.train_on_batch(x=samples,
                                             y=labels)
            return loss
        else:
            return 0.

    def _map_memories_to_train_data(self, memories):
        no_memories = len(memories)
        samples = np.zeros((no_memories,) + CONV_SHAPE, dtype=np.ubyte)
        labels = np.zeros((no_memories, self.no_outputs))
        labels[:, :] = np.nan
        for idx in range(no_memories):
            prev_screen, action_idx, reward, next_screen = memories[idx]
            samples[idx] = prev_screen
            labels[idx, action_idx] = reward + (DISCOUNT_FACTOR * self._highest_reward(next_screen))
        return samples, labels

    def _highest_reward(self, next_screen):
        if next_screen is not None:
            predictions = self.model.predict(next_screen.reshape((1,) + CONV_SHAPE))
            return predictions.max()
        else:
            return 0.0

    def _calibrate_network(self):
        logging.debug("Calibrating network with batch size: %d for %d epochs" % (CALIBRATION_BATCH_SIZE, CALIBRATION_EPOCHS))
        memories = self.repo.get_commits_batch_with_last(CALIBRATION_BATCH_SIZE)
        samples, _ = self._map_memories_to_train_data(memories)
        labels = np.zeros((len(memories), self.no_outputs))
        self.model.fit(x=samples,
                       y=labels,
                       epochs=CALIBRATION_EPOCHS)
        self.calibrated = True



