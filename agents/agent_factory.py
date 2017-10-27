
def agent_factory(agent_config):
    from agents.random_agent import RandomAgent
    from agents.neural_network_agent import NeuralNetworkAgent

    agent_name, possible_keys = agent_config
    return {
        'AGENT_RANDOM': lambda: RandomAgent(possible_keys),
        'AGENT_NN' : lambda: NeuralNetworkAgent('model.h5', possible_keys)
    }[agent_name]()
