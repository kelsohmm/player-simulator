from agents.gamestate_repo import GamestateRepo
from config import MODEL_SAVE_PATH

def _createNNAgent(possible_keys, repo):
    from agents.neural_network_agent import NeuralNetworkAgent
    return NeuralNetworkAgent(MODEL_SAVE_PATH, possible_keys, repo)

def agent_factory(agent_name, possible_keys, save_path):
    from agents.random_agent import RandomAgent

    repo = None
    if isinstance(save_path, str):
        repo = GamestateRepo(save_path, len(possible_keys[0]))

    return {
        'AGENT_RANDOM': lambda: RandomAgent(possible_keys, repo),
        'AGENT_NN' : lambda: _createNNAgent(possible_keys, repo)
    }[agent_name]()
