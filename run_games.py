import datetime
from multiprocessing import freeze_support
import config
from agents.agent_factory import agent_factory
from config import *
from game.environment import make_env
from game.episode import Episode

freeze_support()
if __name__ == '__main__':
    NO_GAMES = COLLECTING_NO_GAMES
    MODE = 'headless'  # 'headless' or 'gui'
    AGENT_NAME = COLLECTING_AGENT_NAME

    if RUN_MODE == 'SHOW':
        NO_GAMES = 100
        MODE = 'gui'  # 'headless' or 'gui'
        AGENT_NAME = 'AGENT_NN'

    save_path = os.path.join(DUMPS_DIR, AGENT_NAME + '_' + datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    os.makedirs(save_path)

    model = None
    if AGENT_NAME == 'AGENT_NN':
        from training.model import create_network
        model = create_network()

    agent = agent_factory(AGENT_NAME, MARIO_CONFIG, save_path, model)
    env = make_env()
    for game_num in range(NO_GAMES):
        env.reset()
        config.GLOB_JOB_ID.set(game_num)

        Episode(agent, env).run()

