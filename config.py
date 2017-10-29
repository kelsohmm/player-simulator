import random
import logging

### VM_CONFIGS ###
# format: (VM_NAME, SNAPSHOT_NAME, WINDOW_RECT(window_width, window_height, window_x, window_y))

_MARIO_WINDOW_RECT = (802, 607, 280, 31)
_MARIO_VM_CONFIG = ('mariosnap', 'mariosnap3', _MARIO_WINDOW_RECT)
_MARIO_SCORE_RECT = (55, 79, 214, 103)
_MARIO_USED_KEYS = ['A', 'LEFT', 'RIGHT']
_MARIO_CONTROLLER_CONFIG = (_MARIO_SCORE_RECT, _MARIO_USED_KEYS)
MARIO_CONFIG = (_MARIO_VM_CONFIG, _MARIO_CONTROLLER_CONFIG)

### GLOBAL SETTINGS ###
if not __name__ == '__main__':  # log tag for jobs started with multiprocess
    logging.basicConfig(format='%(asctime)s JOB:' + '{num:07d}'.format(num=random.randint(0, 1_000_000)) + ' %(message)s', datefmt='%H:%M:%S',  level=logging.DEBUG)
else:
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%H:%M:%S',  level=logging.DEBUG)