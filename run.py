from multiprocessing import freeze_support
from config import SESSION_NAME, NO_GAMES
from agents.neural_network_agent import NeuralNetworkAgent
from game.environment import make_env
from game.episode import Episode
from session import Session
from training.train import ModelTraining

freeze_support()
if __name__ == '__main__':

    session = Session()
    model, repo = session.open(SESSION_NAME)
    agent = NeuralNetworkAgent(model, repo)
    trainer = ModelTraining(model, repo)

    with make_env() as env:
        for game_num in range(NO_GAMES):
            env.reset()
            repo.set_game_number(game_num)
            Episode(agent, env, trainer.train).run()
            session.save_model()

