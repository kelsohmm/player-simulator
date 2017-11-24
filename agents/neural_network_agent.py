import logging
import random
import cv2
import numpy as np
from config import RUN_MODE, PREVIEW_CONV_INPUT, BATCH_SIZE, CONV_SHAPE, DISCOUNT_FACTOR


def screen_preview(screen):
    if RUN_MODE == 'SHOW' and PREVIEW_CONV_INPUT:
        cv2.imshow("Agent preview", cv2.cvtColor(screen, cv2.GRAY2RGB))


class NeuralNetworkAgent:
    def __init__(self, model, possible_game_inputs, repo):
        self.model = model
        self.repo = repo
        self.possible_keys = possible_game_inputs

    def react_to_new_game_screen(self, state, score):
        predictions = self.predict_rewards(state.as_matrix())
        action_idx = self._choose_action_idx(predictions)
        self.repo.commit(state, score, action_idx)

        loss = self.train_model(self.model, self.repo)

        logging.debug('Rewards: %s, Chose: %s, Loss: %s', str(predictions), str(self.possible_keys[action_idx]), str(loss))
        return action_idx

    def train_model(self, model, repo):
        loss = 0
        if repo.size() > 100:
            memories = repo.get_commits_batch_with_last(BATCH_SIZE)
            samples, labels = self._map_memories_to_train_data(memories)
            loss = model.train_on_batch(samples, np.split(labels, 6, axis=1))
        return loss

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

    def _map_memories_to_train_data(self, memories):
        no_memories = len(memories)
        samples = np.zeros((no_memories,) + CONV_SHAPE, dtype=np.ubyte)
        labels = np.zeros((no_memories, len(self.possible_keys)))
        labels[:, :] = np.nan
        for idx in range(no_memories):
            prev_screen, action_idx, reward, next_screen = memories[idx]
            samples[idx] = prev_screen
            labels[idx, action_idx] = reward + (DISCOUNT_FACTOR * self._highest_reward(next_screen))
        return samples, labels

    def _highest_reward(self, next_screen):
        return self.predict_rewards(next_screen).max() \
            if next_screen is not None else 0.
