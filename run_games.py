import datetime
import os

from multiprocessing import Process, freeze_support
from config import *
from game.gameplay_job_factory import create_vm_game_job

freeze_support()

NO_GAMES = 1
MARIO_POSSIBLE_MOVES = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [1, 0, 0], [0, 0, 1], [1, 1, 0]]
DUMP_DIR = os.path.join('gamestate_dumps', datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
if not os.path.exists(DUMP_DIR):
    os.makedirs(DUMP_DIR)

if __name__ == '__main__':
    processes = []
    for game_number in range(NO_GAMES):
        logging.info("Starting job %d", game_number)
        agent_config = ('AGENT_NN', MARIO_POSSIBLE_MOVES)
        p = Process(target=create_vm_game_job, args=(MARIO_CONFIG, agent_config, str(game_number), 'gui'))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
