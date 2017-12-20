import logging
from multiprocessing import freeze_support

from agent.neural_network_agent import NeuralNetworkAgent
from agent.train import ModelTraining
from config import NO_GAMES, SESSION_DIR
from game.environment import make_env
from game.episode import Episode
from memory.gamestate_repo import Repo
from session import Session

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

