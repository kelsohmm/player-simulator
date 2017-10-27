import datetime
import os
from agents.agent_factory import agent_factory
from config import *
from game.gameplay_job_factory import create_vm_game_job

NO_GAMES = 200
MARIO_POSSIBLE_MOVES = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [1, 0, 0], [0, 0, 1], [1, 1, 0]]
DUMP_DIR = os.path.join('gamestate_dumps', datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
if not os.path.exists(DUMP_DIR):
    os.makedirs(DUMP_DIR)

for game_number in range(NO_GAMES):
    logging.info("Starting job %d", game_number)
    player = agent_factory('AGENT_NN', MARIO_POSSIBLE_MOVES)
    job = create_vm_game_job(MARIO_CONFIG, player, str(game_number))
    job.run()
