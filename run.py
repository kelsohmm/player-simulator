import logging
from multiprocessing import freeze_support

from simulator.agent.neural_network_agent import NeuralNetworkAgent
from simulator.game.environment import make_env

from config import NO_GAMES, SESSION_DIR
from session import Session
from simulator.agent.train import ModelTraining
from simulator.game.episode import Episode
from simulator.memory.gamestate_repo import Repo

for handler in logging.root.handlers[:]:  # needed to reconfigure logging
    logging.root.removeHandler(handler)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%H:%M:%S',  level=logging.DEBUG)

freeze_support()
if __name__ == '__main__':
    with make_env() as env, Session(SESSION_DIR) as session:
        model = session.get_model()
        db = session.get_db()
        for _ in range(NO_GAMES):
            env.reset()
            repo = Repo(db)
            agent = NeuralNetworkAgent(model, repo)
            trainer = ModelTraining(model, repo)

            Episode(agent, env, trainer.train).run()
            session.save_model()

