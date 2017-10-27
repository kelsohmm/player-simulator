import itertools
import logging


class GameplayJob:
    def __init__(self, environment, controller, agent, log_id=None):
        self.environment = environment
        self.controller = controller
        self.agent = agent
        if log_id is None:
            self.log_id = ""
        else:
            self.log_id = "GP_JOB:" + str(log_id) + " "

    def run(self):
        try:
            self._start_environment()
            for i in itertools.count():
                state, score, screen = self.controller.get_game_state()
                logging.info(self.log_id + " Iter: %d, State: %s, Score: %d", i, state, score)
                if(state == "FINISHED"):
                    self.agent.finish(score, screen)
                    break
                else:
                    inputs = self.agent.react_to_new_game_screen(screen, score)
                    self.controller.set_active_keys(inputs)
        finally:
            self._stop_environment()

    def _stop_environment(self):
        logging.info(self.log_id + "Stopping game environment")
        self.environment.stop()

    def _start_environment(self):
        logging.info(self.log_id + "Starting game environment")
        self.environment.start()
        logging.info(self.log_id + "Game environment up and running")
