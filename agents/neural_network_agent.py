import logging
import numpy as np
import keras

from data_transformations import map_one_state, DATA_DTYPE
from image_transformations import resize_128


class NeuralNetworkAgent:
    def __init__(self, model_path, possible_game_inputs, repo):
        logging.info("--- INITIALIZING NN AGENT FROM MODEL PATH: %s", model_path)
        self.model = keras.models.load_model(model_path)
        self.repo = repo
        self.inputs_keys = np.asarray(possible_game_inputs, dtype=np.uint8)
        self.possible_keys = possible_game_inputs
        self.target = np.zeros(1, dtype=DATA_DTYPE)

    def react_to_new_game_screen(self, screen_shot, score, time):
        screen = resize_128(screen_shot)
        self.save_state(self.possible_keys[0], score, screen, time)

        predictions = self.predict_rewards(time)

        best_inputs = self.possible_keys[predictions.argmax()]
        self.repo.ammend('inputs', best_inputs)
        logging.debug('Rewards: %s, Chose: %s', str(predictions.tolist()), str(best_inputs))

        return best_inputs

    def save_state(self, best_inputs, score, screen, time):
        if not self.repo is None:
            self.repo.commit(screen, score, best_inputs, time)

    def finish(self, screen_shot, score):
        if not self.repo is None:
            self.repo.close()

    def predict_rewards(self, time):
        map_one_state(self.repo.get_commits(), self.target[0])
        mapping = self.target.repeat(6)
        mapping[:]['inputs'] = self.inputs_keys

        return self.model.predict([mapping[:]['time'], mapping[:]['inputs'], mapping[:]['conv_input']])
