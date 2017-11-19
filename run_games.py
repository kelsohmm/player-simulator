import datetime
from multiprocessing import freeze_support
import config
from agents.agent_factory import agent_factory
from config import *
from game.game_controller import GameController
from game.gameplay_job import GameplayJob
from game.vm_host import VmHost
from training.model import loss_mse_for_known, create_network

freeze_support()
if __name__ == '__main__':
    NO_GAMES = COLLECTING_NO_GAMES
    MODE = 'headless'  # 'headless' or 'gui'
    AGENT_NAME = COLLECTING_AGENT_NAME

    if RUN_MODE == 'SHOW':
        NO_GAMES = 1
        MODE = 'gui'  # 'headless' or 'gui'
        AGENT_NAME = 'AGENT_NN'

    save_path = os.path.join(DUMPS_DIR, AGENT_NAME + '_' + datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    os.makedirs(save_path)

    model = None
    if AGENT_NAME == 'AGENT_NN':
        import keras
        model = create_network()

    for game_num in range(NO_GAMES):
        vm_config, controller_config, possible_moves = MARIO_CONFIG
        config.GLOB_JOB_ID.set(game_num)

        vm = VmHost(vm_config, MODE)
        controller = GameController(vm, controller_config)
        agent = agent_factory(AGENT_NAME, possible_moves, save_path, model)

        GameplayJob(vm, controller, agent).run()

