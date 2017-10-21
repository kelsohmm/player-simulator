from datetime import datetime
from time import sleep

import itertools

from config import *
from game_controller import GameController
from random_agent import RandomAgent
from vm_host import VmHost

import logging
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%H:%M:%S',  level=logging.DEBUG)

class GameplayJob:
    def __init__(self, environment, controller, player, log_id=None):
        self.environment = environment
        self.controller = controller
        self.player = player
        if log_id is None:
            self.log_id = ""
        else:
            self.log_id = "GP_JOB:" + str(log_id)

    def run(self):
        try:
            self._start_environment()
            for i in itertools.count():
                state, score, screen = self.controller.get_game_state()
                logging.info(self.log_id + " Iter: %d, State: %s, Score: %d", i, state, score)
                if(state == "FINISHED"):
                    break
                else:
                    inputs = player.react_to_new_game_screen(screen)
                    self.controller.set_active_keys(inputs)
                    sleep(0.1)
        finally:
            self._stop_environment()

    def _stop_environment(self):
        logging.info(self.log_id + "Stopping game environment")
        self.environment.stop()

    def _start_environment(self):
        logging.info(self.log_id + "Starting game environment")
        self.environment.start()
        logging.info(self.log_id + "Game environment up and running")

game_vm = VmHost(MARIO_VM_CONFIG, mode='gui')
controller = GameController(game_vm, MARIO_VM_SCORE_RECT, ['A', 'LEFT', 'RIGHT'])
player = RandomAgent(3)

job = GameplayJob(game_vm, controller, player, "12")
job.run()