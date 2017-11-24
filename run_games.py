import datetime
from multiprocessing import freeze_support
import config
from agents.neural_network_agent import NeuralNetworkAgent
from config import *
from game.environment import make_env
from game.episode import Episode
from memory.gamestate_repo import Repo
from training.train import ModelTraining
from training.model import create_network

freeze_support()
if __name__ == '__main__':

    save_path = os.path.join(DUMPS_DIR, datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    os.makedirs(save_path)

    model = create_network()
    repo = Repo(save_path)
    agent = NeuralNetworkAgent(model, repo)
    trainer = ModelTraining(model, repo)
    env = make_env()

    for game_num in range(NO_GAMES):
        env.reset()
        config.GLOB_JOB_ID.set(game_num)

        Episode(agent, env, trainer.train).run()
        model.save(MODEL_SAVE_PATH)

