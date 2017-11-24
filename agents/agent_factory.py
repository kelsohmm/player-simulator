
def _createNNAgent(repo, model):
    from agents.neural_network_agent import NeuralNetworkAgent
    return NeuralNetworkAgent(model, repo)

def agent_factory(agent_name, repo, model):


    return {
        'AGENT_NN' : lambda: _createNNAgent(repo, model)
    }[agent_name]()
