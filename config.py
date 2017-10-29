import random
import logging

### VM_CONFIGS ###
# format: (VM_NAME, SNAPSHOT_NAME, WINDOW_RECT(window_width, window_height, window_x, window_y))

_MARIO_WINDOW_RECT = (802, 607, 280, 31)
_MARIO_VM_CONFIG = ('mariosnap', 'mariosnap3', _MARIO_WINDOW_RECT)
_MARIO_SCORE_RECT = (55, 79, 214, 103)
_MARIO_USED_KEYS = ['A', 'LEFT', 'RIGHT']
_MARIO_CONTROLLER_CONFIG = (_MARIO_SCORE_RECT, _MARIO_USED_KEYS)
_MARIO_POSSIBLE_MOVES = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [1, 0, 0], [0, 0, 1], [1, 1, 0]]
MARIO_CONFIG = (_MARIO_VM_CONFIG, _MARIO_CONTROLLER_CONFIG, _MARIO_POSSIBLE_MOVES)

### GLOBAL SETTINGS ###

class JobIdConfig:
    def __init__(self):
        self.set(0)

    def set(self, job_id):
        self.job_id = '{num:03d}'.format(num=job_id)
        for handler in logging.root.handlers[:]:  # needed to reconfigure logging
            logging.root.removeHandler(handler)
        logging.basicConfig(format='%(asctime)s JOB:' + self.job_id + ' %(message)s', datefmt='%H:%M:%S',  level=logging.DEBUG)

GLOB_JOB_ID = JobIdConfig()

