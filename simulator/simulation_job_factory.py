import sqlite3
from multiprocessing import Process
from datetime import datetime


def simulation_job_factory(db_path, model_path):
    return GameSimulationJob(db_path, model_path)

def _run_game_simulation(db_path, model_path):
    from simulator.agent.neural_network_agent import NeuralNetworkAgent
    from simulator.agent.train import ModelTraining
    from simulator.game.environment import make_env
    from simulator.agent.model import load_model
    from simulator.game.episode import Episode
    from simulator.memory.database import Database
    from simulator.memory.gamestate_repo import Repo

    with make_env() as env, sqlite3.connect(db_path) as db_conn:
        model = load_model(model_path)
        db = Database(db_conn)
        env.reset()
        repo = Repo(db)
        agent = NeuralNetworkAgent(model, repo)
        trainer = ModelTraining(model, repo)

        Episode(agent, env, trainer.train).run()

        model.save(model_path)


class GameSimulationJob:
    def __init__(self, db_path, model_path):
        self.process = Process(target=_run_game_simulation, args=(db_path, model_path))
        self._start_time = None

    def run(self):
        self.process.start()
        self._start_time = datetime.now()

    def is_running(self):
        return self.process.is_alive()

    def stop(self):
        self.process.terminate()

    def start_time(self):
        return self._start_time
