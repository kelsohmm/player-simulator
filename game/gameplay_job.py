import itertools
import logging
import time
import cv2
from config import _MARIO_POSSIBLE_MOVES, FRAME_SIZE


def resize(image):
    return cv2.resize(image, FRAME_SIZE)

class GameplayJob:
    _MAX_GAME_TIME_MINUTES = 5

    def __init__(self, agent, env):
        self.env = env
        self.agent = agent
        self.start_time = time.time()

    def run(self):
        action_idx = 0
        start_time = time.time()
        screen = score = done = None
        for i in itertools.count():
            for _ in range(3):
                screen, reward, done, info = self.env.step(_MARIO_POSSIBLE_MOVES[action_idx])
            screen = resize(screen)
            action_idx = self.agent.react_to_new_game_screen(screen, score)

            game_time = time.time() - start_time
            logging.debug("Iter: %d, Score: %d, Time: %d", i, score, int(game_time))
            if done:
                self.agent.finish(score, screen)
                break

    def max_time_exceeded(self, game_time):
        return game_time / 60. > self._MAX_GAME_TIME_MINUTES
