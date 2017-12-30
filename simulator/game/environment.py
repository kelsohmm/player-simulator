import gym

gym.envs.register(
    id='SuperMarioBros-1-1-v0',
    entry_point='ppaquette_gym_super_mario:MetaSuperMarioBrosEnv',
)
import gym_pull


class EnvWrapper:
    def __enter__(self):
        self.env = gym.make('SuperMarioBros-1-1-v0')
        return self.env

    def __exit__(self, type, value, traceback):
        self.env.close()


def make_env():
    return EnvWrapper()
