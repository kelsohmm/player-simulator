import logging


### VM_CONFIGS ###
# format: (VM_NAME, SNAPSHOT_NAME, WINDOW_RECT(window_width, window_height, window_x, window_y))
MARIO_VM_CONFIG = ('mariosnap', 'mariosnap3',
                   (802, 607, 280, 31))
MARIO_VM_SCORE_RECT = (55, 79, 214, 103)  # (335, 110, 494, 134)

### GLOBAL SETTINGS ###
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%H:%M:%S',  level=logging.DEBUG)