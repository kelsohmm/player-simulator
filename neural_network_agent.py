import numpy as np
import keras
from image_transformations import transform_64_bw


class NeuralNetworkAgent:
    def __init__(self, model_path, possible_game_inputs, repo = None):
        print("--- INITIALIZING NN AGENT FROM MODEL PATH: ", model_path)
        self.model = keras.models.load_model(model_path)
        self.repo = repo
        self.no_inputs = len(possible_game_inputs)
        self.inputs_keys = np.asarray([inputs for inputs in possible_game_inputs], dtype=np.uint8)
        self.inputs_this_frame = np.zeros((self.no_inputs, 1, 64, 64), dtype=np.uint8)
        self.inputs_prev_frame = None
        self.possible_keys = possible_game_inputs

    def react_to_new_game_screen(self, screen_shot, score):
        screen = transform_64_bw(screen_shot)
        self.inputs_this_frame = screen.reshape((1, 1, 64, 64)).repeat(self.no_inputs, axis=0)
        self.guard_prev_screen(screen)

        predictions = self.predict_rewards()

        best_inputs = self.possible_keys[predictions.argmax()]
        print(predictions.tolist(), " Chose: ", best_inputs)

        self.save_state(best_inputs, score, screen)
        return best_inputs

    def save_state(self, best_inputs, score, screen):
        if not self.repo is None:
            self.repo.commit(screen, score, best_inputs)
        self.inputs_prev_frame = self.inputs_this_frame

    def finish(self, screen_shot, score):
        if not self.repo is None:
            self.repo.close()

    def guard_prev_screen(self, screen_shot):
        if self.inputs_prev_frame is None:
            self.inputs_prev_frame = self.inputs_this_frame

    def predict_rewards(self):
        return self.model.predict([self.inputs_keys, self.inputs_this_frame, self.inputs_prev_frame])