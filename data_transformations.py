import cv2
import numpy as np
from config import _MARIO_POSSIBLE_MOVES

DATA_DTYPE = [('conv_input', np.ubyte, (128, 128, 3)),
              ('rewards', np.float32, len(_MARIO_POSSIBLE_MOVES))]


def argmax(collection):
    maxval = collection[0]
    maxidx = 0
    for idx in range(1, len(collection)):
        if collection[idx] > maxval:
            maxval = collection[idx]
            maxidx = idx
    return maxidx


def map_rewards_to_inputs(rewards):
    return _MARIO_POSSIBLE_MOVES[argmax(rewards)]

def map_action_idx_from_inputs(inputs):
    return _MARIO_POSSIBLE_MOVES.index(inputs.tolist()[0])

def map_rewards_from_inputs(reward, inputs, target):
    target[:] = np.nan
    target[_MARIO_POSSIBLE_MOVES.index(inputs.tolist()[0])] = reward


def map_one_state(states, target, index=None):
    if index is None:
        index = len(states) - 1

    frame_current = states[index]['screen'].reshape((128, 128, 3))
    frame_1_prev = states[index - 1]['screen'].reshape((128, 128, 3)) if index >= 1 else frame_current
    frame_2_prev = states[index - 2]['screen'].reshape((128, 128, 3)) if index >= 2 else frame_1_prev

    target['conv_input'][:, :, 0] = cv2.cvtColor(frame_current, cv2.COLOR_RGB2GRAY)
    target['conv_input'][:, :, 1] = cv2.cvtColor(frame_1_prev, cv2.COLOR_RGB2GRAY)
    target['conv_input'][:, :, 2] = cv2.cvtColor(frame_2_prev, cv2.COLOR_RGB2GRAY)

    target['rewards'][:] = np.nan

    return target


def calc_rewards(states):
    GAMMA = 0.99
    no_states = len(states)
    rewards = np.zeros((no_states,), dtype=np.float32)
    rewards[no_states - 1] = states[no_states - 1]['score'] - states[no_states - 2]['score']
    for i in reversed(range(0, no_states - 1)):
        prev_score = states[i - 1]['score'] if i > 0 else 0.0
        current_score = states[i]['score'] - prev_score
        score = 1.0 if current_score > 0.0 else 0.0
        rewards[i] = score + (GAMMA * rewards[i + 1])
    return rewards


def map_one_episode(states, target):
    no_states = len(states)
    rewards = calc_rewards(states)
    for i in range(no_states):
        map_one_state(states, target[i], index=i)
        map_rewards_from_inputs(rewards[i], states[i]['inputs'], target[i]['rewards'])
