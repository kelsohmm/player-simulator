import datetime
from multiprocessing import freeze_support
from multiprocessing.pool import Pool
from config import *
from game.gameplay_job_factory import create_vm_game_job

freeze_support()
if __name__ == '__main__':
    NO_JOBS = 2
    NO_GAMES = COLLECTING_NO_GAMES
    MODE = 'headless'  # 'headless' or 'gui'
    AGENT_NAME = COLLECTING_AGENT_NAME
    SAVING = True

    if RUN_MODE == 'SHOW':
        NO_GAMES = 1
        MODE = 'gui'  # 'headless' or 'gui'
        AGENT_NAME = 'AGENT_NN'
        SAVING = False


    ### CODE
    proc_pool = Pool(NO_JOBS, maxtasksperchild=10)
    save_path = None
    if SAVING:
        save_path = os.path.join(DUMPS_DIR, AGENT_NAME + '_' + datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
        if not os.path.exists(save_path):
            os.makedirs(save_path)

    proc_pool.map(create_vm_game_job,
                  [(job_number+1, MARIO_CONFIG, AGENT_NAME, save_path, MODE) for job_number in range(NO_GAMES)],
                  chunksize=1)


