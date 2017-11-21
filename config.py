import logging
import os

### RUN SETTINGS ###

RUN_MODE = 'SHOW'  # SHOW or COLLECT

COLLECTING_NO_GAMES = 100
COLLECTING_AGENT_NAME = 'AGENT_RANDOM'

PREVIEW_CONV_INPUT = RUN_MODE == 'SHOW' and True

### GLOBAL SETTINGS ###
SAVE_API_VERSION = '2.0'  # saving preprocessed frames directly

class JobIdConfig:
    def __init__(self):
        self.set(0)

    def set(self, job_id):
        self.job_id = '{num:03d}'.format(num=job_id)
        for handler in logging.root.handlers[:]:  # needed to reconfigure logging
            logging.root.removeHandler(handler)
        logging.basicConfig(format='%(asctime)s JOB:' + self.job_id + ' %(message)s', datefmt='%H:%M:%S',  level=logging.DEBUG)

GLOB_JOB_ID = JobIdConfig()
DUMPS_DIR = os.path.join('gamestate_dumps', 'api-'+SAVE_API_VERSION)
MODEL_SAVE_PATH = os.path.join(DUMPS_DIR, 'model.h5')
DATA_SAVE_PATH = os.path.join(DUMPS_DIR, 'data.npz')
MODEL_PREVIEW_PATH = os.path.join(DUMPS_DIR, 'model_preview.png')


_MARIO_POSSIBLE_MOVES = [
    [0, 0, 0, 0, 0, 0],  # NOOP
    # [1, 0, 0, 0, 0, 0],  # Up
    # [0, 0, 1, 0, 0, 0],  # Down
    [0, 1, 0, 0, 0, 0],  # Left
    [0, 1, 0, 0, 1, 0],  # Left + A
    # [0, 1, 0, 0, 0, 1],  # Left + B
    # [0, 1, 0, 0, 1, 1],  # Left + A + B
    [0, 0, 0, 1, 0, 0],  # Right
    [0, 0, 0, 1, 1, 0],  # Right + A
    # [0, 0, 0, 1, 0, 1],  # Right + B
    # [0, 0, 0, 1, 1, 1],  # Right + A + B
    [0, 0, 0, 0, 1, 0],  # A
    # [0, 0, 0, 0, 0, 1],  # B
    # [0, 0, 0, 0, 1, 1],  # A + B
]
MARIO_CONFIG = (_MARIO_POSSIBLE_MOVES)