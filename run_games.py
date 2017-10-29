import datetime
import os
from asyncio import sleep
from multiprocessing import Process, freeze_support
from multiprocessing.pool import Pool

from config import *
from game.gameplay_job_factory import create_vm_game_job

freeze_support()
if __name__ == '__main__':

    ### RUN CONFIG
    NO_GAMES = 100
    NO_JOBS = 2
    MODE = 'headless'  # 'headless' or 'gui'
    AGENT_NAME = 'AGENT_RANDOM'
    SAVING = True

    ### CODE
    proc_pool = Pool(NO_JOBS, maxtasksperchild=10)
    save_path = None
    if SAVING:
        save_path = os.path.join('gamestate_dumps', AGENT_NAME + '_' + datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
        if not os.path.exists(save_path):
            os.makedirs(save_path)

    proc_pool.map(create_vm_game_job,
                  [(MARIO_CONFIG, AGENT_NAME, save_path, MODE) for _ in range(NO_GAMES)],
                  chunksize=1)



