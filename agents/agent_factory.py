from agents.gamestate_repo import GamestateRepo
from config import MODEL_PATH


def agent_factory(agent_name, possible_keys, save_path):
    from agents.random_agent import RandomAgent
    from agents.neural_network_agent import NeuralNetworkAgent

    repo = None
    if isinstance(save_path, str):
        repo = GamestateRepo(save_path)

    return {
        'AGENT_RANDOM': lambda: RandomAgent(possible_keys, repo),
        'AGENT_NN' : lambda: NeuralNetworkAgent(MODEL_PATH, possible_keys, repo)
    }[agent_name]()
