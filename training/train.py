import logging

import numpy as np
from config import BATCH_SIZE, DISCOUNT_FACTOR, CONV_SHAPE

LEARNING_START = 100
CALIBRATION_BATCH_SIZE = 250
CALIBRATION_EPOCHS = 5

class ModelTraining:
    def __init__(self, model, memories_repo):
        self.model = model
        self.repo = memories_repo
        self.no_outputs = len(model.outputs)
        self.calibrated = False

    def train(self):
        if self.repo.size() > LEARNING_START:
            if not self.calibrated:
                self._calibrate_network()
            memories = self.repo.get_commits_batch_with_last(BATCH_SIZE)
            samples, labels = self._map_memories_to_train_data(memories)
            loss = self.model.train_on_batch(x=samples,
                                             y=np.split(labels, self.no_outputs, axis=1),
                                             class_weight=self._activaty_only_trained_action_idx(memories))
            return loss
        else:
            return 0.

    def _map_memories_to_train_data(self, memories):
        no_memories = len(memories)
        samples = np.zeros((no_memories,) + CONV_SHAPE, dtype=np.ubyte)
        labels = np.zeros((no_memories, self.no_outputs))
        for idx in range(no_memories):
            prev_screen, action_idx, reward, next_screen = memories[idx]
            samples[idx] = prev_screen
            labels[idx, action_idx] = reward + (DISCOUNT_FACTOR * self._highest_reward(next_screen))
        return samples, labels

    def _highest_reward(self, next_screen):
        if next_screen is not None:
            predictions = np.concatenate(self.model.predict(next_screen.reshape((1,) + CONV_SHAPE))).flatten()
            return predictions.max()
        else:
            return 0.0

    def _equal_actions_ids(self, memories):
        _, first_action_idx, _, _ = memories[0]
        for i in range(1, len(memories)):
            _, action_idx, _, _ = memories[i]
            if first_action_idx != action_idx:
                return False
        return True

    def _trained_action_idx(self, memories):
        assert self._equal_actions_ids(memories), "All action ids must be equal"
        _, first_action_idx, _, _ = memories[0]
        return first_action_idx

    def _activaty_only_trained_action_idx(self, memories):
        trained_action_idx = self._trained_action_idx(memories)
        class_weights = [0.0] * self.no_outputs
        class_weights[trained_action_idx] = 1.0
        return class_weights

    def _calibrate_network(self):
        logging.debug("Calibrating network with batch size: %d for %d epochs" % (CALIBRATION_BATCH_SIZE, CALIBRATION_EPOCHS))
        memories = self.repo.get_commits_batch_with_last(CALIBRATION_BATCH_SIZE)
        samples, _ = self._map_memories_to_train_data(memories)
        labels = np.zeros((len(memories), self.no_outputs))
        self.model.fit(x=samples,
                       y=np.split(labels, self.no_outputs, axis=1),
                       epochs = CALIBRATION_EPOCHS)
        self.calibrated = True



