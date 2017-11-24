from memory.gamestate_repo import Repo

def _createNNAgent(possible_keys, repo, model):
    from agents.neural_network_agent import NeuralNetworkAgent
    return NeuralNetworkAgent(model, possible_keys, repo)

def agent_factory(agent_name, possible_keys, save_path, model):

    repo = Repo(save_path)

    return {
        'AGENT_NN' : lambda: _createNNAgent(possible_keys, repo, model)
    }[agent_name]()
