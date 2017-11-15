from agents.gamestate_repo import GamestateRepo
from config import MODEL_SAVE_PATH

def _createNNAgent(possible_keys, repo, model):
    from agents.neural_network_agent import NeuralNetworkAgent
    return NeuralNetworkAgent(model, possible_keys, repo)

def agent_factory(agent_name, possible_keys, save_path, model):
    from agents.random_agent import RandomAgent

    repo = GamestateRepo(save_path, len(possible_keys[0]))

    return {
        'AGENT_RANDOM': lambda: RandomAgent(possible_keys, repo),
        'AGENT_NN' : lambda: _createNNAgent(possible_keys, repo, model)
    }[agent_name]()
