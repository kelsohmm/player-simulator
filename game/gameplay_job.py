import itertools
import logging


class GameplayJob:
    def __init__(self, environment, controller, agent):
        self.environment = environment
        self.controller = controller
        self.agent = agent

    def run(self):
        try:
            self._start_environment()
            for i in itertools.count():
                state, score, screen = self.controller.get_game_state()
                logging.debug("Iter: %d, State: %s, Score: %d", i, state, score)
                if(state == "FINISHED"):
                    self.agent.finish(score, screen)
                    break
                else:
                    inputs = self.agent.react_to_new_game_screen(screen, score)
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
