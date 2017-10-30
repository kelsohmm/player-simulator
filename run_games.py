import datetime
import os
from asyncio import sleep
from multiprocessing import Process, freeze_support
from multiprocessing.pool import Pool

from agents.gamestate_repo import GamestateRepo
from config import *
from game.gameplay_job_factory import create_vm_game_job

freeze_support()
if __name__ == '__main__':

    ### RUN CONFIG
    NO_GAMES = 1
    NO_JOBS = 1
    MODE = 'gui'  # 'headless' or 'gui'
    AGENT_NAME = 'AGENT_RANDOM'
    SAVING = False

    ### CODE
    proc_pool = Pool(NO_JOBS, maxtasksperchild=10)
    repo = None
    if SAVING:
        save_path = os.path.join(DUMPS_DIR, AGENT_NAME + '_' + datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
        repo = GamestateRepo(save_path)
        if not os.path.exists(save_path):
            os.makedirs(save_path)

    proc_pool.map(create_vm_game_job,
                  [(job_number+1, MARIO_CONFIG, AGENT_NAME, repo, MODE) for job_number in range(NO_GAMES)],
                  chunksize=1)



