import logging
import os

### RUN SETTINGS ###
NO_GAMES = 100
SESSION_NAME = "session1"

### LEARNING PARAMETERS ###
FRAME_SIZE = (128, 128)
FRAMES_STACKED = 4
CONV_SHAPE = FRAME_SIZE + (FRAMES_STACKED,)
BATCH_SIZE = 50
DISCOUNT_FACTOR = 0.99
MIN_MEMORIES = 1000

### GLOBAL SETTINGS ###
SESSION_DIR = os.path.join('saved_sessions', SESSION_NAME)


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