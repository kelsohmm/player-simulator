import itertools
import logging
import gym

gym.envs.register(
    id='SuperMarioBros-1-1-v0',
    entry_point='ppaquette_gym_super_mario:MetaSuperMarioBrosEnv',
)
import gym_pull
import time
import cv2


def resize_128(image):
    return cv2.resize(image, (128, 128))


class GameplayJob:
    _MAX_GAME_TIME_MINUTES = 5

    def __init__(self, agent):
        self.env = gym.make('SuperMarioBros-1-1-v0')
        self.agent = agent
        self.start_time = time.time()

    def run(self):
        screen = self.env.reset()
        score = 0
        done = False
        for i in itertools.count():
            screen = resize_128(screen)

            game_time = time.time() - self.start_time
            if self.max_time_exceeded(game_time):
                done = True

            logging.debug("Iter: %d, Score: %d, Time: %d", i, score, int(game_time))

            if done:
                self.agent.finish(score, screen)
                break
            else:
                action = self.agent.react_to_new_game_screen(screen, score, game_time)
                screen, score, done, _ = self.env.step(action)


    def _stop_environment(self):
        logging.info("Stopping game job")

    def _start_environment(self):
        logging.info("New game started")
        self.start_time = time.time()

    def max_time_exceeded(self, game_time):
        return game_time / 60. > self._MAX_GAME_TIME_MINUTES
