import os
PREVIEW_FILENAME = 'model_preview.png'
DB_FILENAME = 'history.db'
MODEL_FILENAME = 'model.h5'

### RUN SETTINGS ###
NO_GAMES = 100
SESSION_NAME = "session1"

### LEARNING PARAMETERS ###
FRAME_SIZE = (128, 128)
FRAMES_STACKED = 4
BATCH_SIZE = 32
DISCOUNT_FACTOR = 0.99
EXPLORATION_FACTOR = 0.05
MIN_MEMORIES = 9000

### GLOBAL SETTINGS ###
SESSION_DIR = os.path.join('saved_sessions', SESSION_NAME)
CONV_SHAPE = FRAME_SIZE + (FRAMES_STACKED,)


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
