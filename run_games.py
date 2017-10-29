import datetime
import os
from asyncio import sleep
from multiprocessing import Process, freeze_support
from config import *
from game.gameplay_job_factory import create_vm_game_job

freeze_support()
if __name__ == '__main__':
    NO_GAMES = 2
    AGENT_NAME = 'AGENT_NN'
    SAVING = True

    processes = []
    for game_number in range(NO_GAMES):
        logging.info("Starting job %d", game_number)

        save_path = None
        if SAVING:
            save_path = os.path.join('gamestate_dumps', AGENT_NAME + '_' + datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
            if not os.path.exists(save_path):
                os.makedirs(save_path)

        p = Process(target=create_vm_game_job, args=(MARIO_CONFIG, AGENT_NAME, save_path, 'headless'))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

