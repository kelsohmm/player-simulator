import gym

gym.envs.register(
    id='SuperMarioBros-1-1-v0',
    entry_point='ppaquette_gym_super_mario:MetaSuperMarioBrosEnv',
)
import gym_pull

def make_env():
    env = gym.make('SuperMarioBros-1-1-v0')
    env.reset()
    return env