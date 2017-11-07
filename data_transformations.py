import cv2
import numpy as np

DATA_DTYPE = [('conv_input', np.ubyte, (128, 128, 3)),
              ('inputs', np.int16, 3),
              ('time', np.float64),
              ('reward', np.float64)]

def map_one_state(states, target, index=None):
    if index is None:
        index = len(states) - 1

    frame_current = states[index]['screen'].reshape((128, 128, 3))
    frame_1_prev = states[index-1]['screen'].reshape((128, 128, 3)) if index >= 1 else frame_current
    frame_2_prev = states[index-2]['screen'].reshape((128, 128, 3)) if index >= 2 else frame_1_prev

    target['conv_input'][:, :, 0] = cv2.cvtColor(frame_current, cv2.COLOR_RGB2GRAY)
    target['conv_input'][:, :, 1] = cv2.cvtColor(frame_1_prev, cv2.COLOR_RGB2GRAY)
    target['conv_input'][:, :, 2] = cv2.cvtColor(frame_2_prev, cv2.COLOR_RGB2GRAY)

    target['inputs'] = states[index]['inputs']
    target['time'] = states[index]['time']
    target['reward'] = np.nan

    return target

def calc_rewards(states):
    GAMMA = 0.9
    no_states = len(states)
    rewards = np.zeros((no_states,), dtype=np.float64)
    rewards[no_states - 1] = states[no_states - 1]['score'] - states[no_states - 2]['score']
    for i in reversed(range(0, no_states - 1)):
        prev_score = states[i-1]['score'] if i > 0 else 0.0
        rewards[i] = states[i]['score'] - prev_score + (GAMMA * rewards[i+1])
    return rewards

def map_one_episode(states, target):
    no_states = len(states)
    rewards = calc_rewards(states)
    for i in range(no_states):
        map_one_state(states, target[i], index=i)
        target[i]['reward'] = rewards[i]

