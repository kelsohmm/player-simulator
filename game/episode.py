import itertools
import logging
import time
from config import _MARIO_POSSIBLE_MOVES, FRAMES_STACKED
from game.state import State


class Episode:
    _MAX_GAME_TIME_MINUTES = 5

    def __init__(self, agent, env, train_fun):
        self.env = env
        self.agent = agent
        self.train_callback = train_fun
        self.start_time = time.time()

    def run(self):
        action_idx = 0
        start_time = time.time()
        for i in itertools.count():
            state, reward, done, info = self.repeat_action(action_idx)
            action_idx = self.agent.react_to_new_game_screen(state.as_matrix(), reward)
            self.train_callback()

            logging.debug("Iter: %d, Score: %f, Time: %d", i, info['total_reward'], int(time.time() - start_time))
            if done:
                self.agent.finish(reward, state)
                break

    def repeat_action(self, action_idx):
        done = info = None
        accumulated_reward = 0
        state = State()
        for _ in range(FRAMES_STACKED):
            screen, reward, done, info = self.env.step(_MARIO_POSSIBLE_MOVES[action_idx])
            accumulated_reward += reward
            state.append(screen)

        return state, accumulated_reward, done, info