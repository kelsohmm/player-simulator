import itertools
import logging
import time
import cv2
from config import _MARIO_POSSIBLE_MOVES

def resize_128(image):
    return cv2.resize(image, (128, 128))


class GameplayJob:
    _MAX_GAME_TIME_MINUTES = 5

    def __init__(self, agent, env):
        self.env = env
        self.agent = agent
        self.start_time = time.time()

    def run(self):
        action_idx = 0
        start_time = time.time()
        for i in itertools.count():
            screen, score, done, _ = self.env.step(_MARIO_POSSIBLE_MOVES[action_idx])
            screen = resize_128(screen)
            action_idx = self.agent.react_to_new_game_screen(screen, score)

            game_time = time.time() - start_time
            logging.debug("Iter: %d, Score: %d, Time: %d", i, score, int(game_time))
            if done or self.max_time_exceeded(game_time):
                self.agent.finish(score, screen)
                break

    def max_time_exceeded(self, game_time):
        return game_time / 60. > self._MAX_GAME_TIME_MINUTES
