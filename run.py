import datetime
from multiprocessing import freeze_support
import config
from agents.neural_network_agent import NeuralNetworkAgent
from config import *
from game.environment import make_env
from game.episode import Episode
from memory.gamestate_repo import Repo
from session import Session
from training.train import ModelTraining
from training.model import create_network

freeze_support()
if __name__ == '__main__':

    session = Session()
    model, repo = session.open(SESSIONS_DIR)
    agent = NeuralNetworkAgent(model, repo)
    trainer = ModelTraining(model, repo)

    with make_env() as env:
        for game_num in range(NO_GAMES):
            env.reset()
            repo.set_game_number(game_num)
            Episode(agent, env, trainer.train).run()
            session.save_model()

