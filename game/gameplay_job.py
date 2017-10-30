import itertools
import logging

import time


class GameplayJob:
    _MAX_GAME_TIME_MINUTES = 5

    def __init__(self, environment, controller, agent):
        self.environment = environment
        self.controller = controller
        self.agent = agent

    def run(self):
        try:
            self._start_environment()
            for i in itertools.count():
                state, score, screen = self.controller.get_game_state()
                game_time = time.time() - self.start_time

                if self.max_time_exceeded(game_time):
                    state = 'FINISHED'
                logging.debug("Iter: %d, State: %s, Score: %d, Time: %d", i, state, score, int(game_time))

                if state == 'FINISHED':
                    self.agent.finish(score, screen)
                    break
                else:
                    inputs = self.agent.react_to_new_game_screen(screen, score, game_time)
                    self.controller.set_active_keys(inputs)
        finally:
            self._stop_environment()

    def _stop_environment(self):
        logging.info("Stopping game environment")
        self.environment.stop()

    def _start_environment(self):
        logging.info("Starting game environment")
        self.environment.start()
        logging.info("Game environment up and running")
        self.start_time = time.time()

    def max_time_exceeded(self, game_time):
        return game_time / 60. > self._MAX_GAME_TIME_MINUTES
