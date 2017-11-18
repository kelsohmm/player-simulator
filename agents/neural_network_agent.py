import logging
import cv2
import numpy as np
from config import RUN_MODE, PREVIEW_CONV_INPUT, MODEL_SAVE_PATH
from data_transformations import map_one_state, DATA_DTYPE, map_rewards_to_inputs


def screen_preview(screen):
    if RUN_MODE == 'SHOW' and PREVIEW_CONV_INPUT:
        cv2.imshow("Agent preview", screen)

class NeuralNetworkAgent:
    def __init__(self, model, possible_game_inputs, repo):
        self.model = model
        self.repo = repo
        self.inputs_keys = np.asarray(possible_game_inputs, dtype=np.uint8)
        self.possible_keys = possible_game_inputs
        self.target = np.zeros(1, dtype=DATA_DTYPE)

    def react_to_new_game_screen(self, screen_shot, score, time):
        self.save_state(self.possible_keys[0], score, screen_shot, time)

        predictions = self.predict_rewards()
        best_inputs = map_rewards_to_inputs(predictions)

        logging.debug('Rewards: %s, Chose: %s', str(predictions), str(best_inputs))

        return best_inputs

    def save_state(self, best_inputs, score, screen, time):
        if not self.repo is None:
            self.repo.commit(screen, score, best_inputs, time)

    def finish(self, screen_shot, score):
        self.model.save(MODEL_SAVE_PATH)
        if not self.repo is None:
            self.repo.close()

    def predict_rewards(self):
        map_one_state(self.repo.get_commits(), self.target[0])

        screen_preview(self.target[0]['conv_input'])

        raw_predicts = self.model.predict([self.target[0]['conv_input'].reshape((1, 128, 128, 3))])
        return np.concatenate(raw_predicts).flatten()
