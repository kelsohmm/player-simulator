import logging
import random
import cv2
import numpy as np
from config import RUN_MODE, PREVIEW_CONV_INPUT, MODEL_SAVE_PATH, CONV_SHAPE


def screen_preview(screen):
    if RUN_MODE == 'SHOW' and PREVIEW_CONV_INPUT:
        cv2.imshow("Agent preview", cv2.cvtColor(screen, cv2.GRAY2RGB))


class NeuralNetworkAgent:
    BATCH_SIZE = 50

    def __init__(self, model, possible_game_inputs, repo):
        self.model = model
        self.repo = repo
        self.possible_keys = possible_game_inputs
        self.frame_target = np.zeros((1,)+CONV_SHAPE, dtype=np.ubyte)

    def react_to_new_game_screen(self, screen_shot, score):
        screen_shot = cv2.cvtColor(screen_shot, cv2.COLOR_RGB2GRAY).reshape(CONV_SHAPE)
        predictions = self.predict_rewards(screen_shot)
        action_idx = self._choose_action_idx(predictions)
        self.repo.commit(screen_shot, score, action_idx)

        loss = 0
        if self.repo.size() > 1000:
            memories = self.repo.get_commits_batch_with_last(self.BATCH_SIZE)
            samples, labels = self._map_memories_to_train_data(memories)
            loss = self.model.train_on_batch(samples, np.split(labels, 6, axis=1))

        logging.debug('Rewards: %s, Chose: %s, Loss: %s', str(predictions), str(self.possible_keys[action_idx]), str(loss))
        return action_idx

    def _choose_action_idx(self, predictions):
        if random.uniform(0., 1.) < 0.05 or self.repo.size() < 10000:
            return random.randint(0, 5)
        else:
            return predictions.argmax()

    def finish(self, screen_shot, score):
        self.model.save(MODEL_SAVE_PATH)
        if not self.repo is None:
            self.repo.close()

    def predict_rewards(self, screen):
        self.frame_target[0] = screen
        raw_predicts = self.model.predict(self.frame_target)
        return np.concatenate(raw_predicts).flatten()

    def _map_memories_to_train_data(self, memories):
        no_memories = len(memories)
        samples = np.zeros((no_memories, 128, 128, 1), dtype=np.ubyte)
        labels = np.zeros((no_memories, len(self.possible_keys)))
        labels[:, :] = np.nan
        for idx in range(no_memories):
            prev_screen, action_idx, reward, next_screen = memories[idx]
            samples[idx] = prev_screen
            labels[idx, action_idx] = reward + self._highest_reward(next_screen)
        return samples, labels

    def _highest_reward(self, next_screen):
        return self.predict_rewards(next_screen).max() \
            if next_screen is not None else 0.
