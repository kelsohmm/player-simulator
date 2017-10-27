
def agent_factory(agent_name, possible_keys):
    from agents.random_agent import RandomAgent
    from agents.neural_network_agent import NeuralNetworkAgent
    return {
        'AGENT_RANDOM': lambda keys: RandomAgent(keys),
        'AGENT_NN' : lambda keys: NeuralNetworkAgent('model.h5', keys)
    }[agent_name](possible_keys)
