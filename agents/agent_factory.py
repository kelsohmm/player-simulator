from agents.gamestate_repo import GamestateRepo
from config import MODEL_PATH

def _createNNAgent(possible_keys, repo):
    from agents.neural_network_agent import NeuralNetworkAgent
    return NeuralNetworkAgent(MODEL_PATH, possible_keys, repo)

def agent_factory(agent_name, possible_keys, repo):
    from agents.random_agent import RandomAgent

    return {
        'AGENT_RANDOM': lambda: RandomAgent(possible_keys, repo),
        'AGENT_NN' : lambda: _createNNAgent(possible_keys, repo)
    }[agent_name]()
