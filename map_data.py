import numpy as np
from config import DUMPS_DIR, DATA_SAVE_PATH
from training.utils import find_all_filepaths, read_episode_files

dump_files = find_all_filepaths(DUMPS_DIR, shuffle=True)
print('GAMEDUMPS FOUND: ', dump_files)

game_dumps = read_episode_files(dump_files)
print('EPISODES:', len(game_dumps))

no_state_dumps = sum(map(lambda x: len(x), game_dumps)) \
                 - len(game_dumps)  # dropping first frame in each game dump
print('STATES:', no_state_dumps)

inputs_shape = game_dumps[0][0]['inputs'].shape
screen_shape = game_dumps[0][0]['screen'].shape
inputs_keys = np.zeros((no_state_dumps, 3), dtype=np.uint8)
inputs_this_frame = np.zeros((no_state_dumps, 128, 128, 3), dtype=np.uint8)
inputs_prev_frame = np.zeros((no_state_dumps, 128, 128, 3), dtype=np.uint8)
inputs_time = np.zeros((no_state_dumps, 1), dtype=np.float64)
labels = np.zeros((no_state_dumps,), dtype=np.float64)

def calc_rewards(game_dump):
    GAMMA = 0.8
    rewards = np.zeros((len(game_dump),), dtype=np.float16)
    rewards[len(game_dump) - 1] = game_dump[len(game_dump) - 1]['score'] - game_dump[len(game_dump) - 2]['score']
    for i in reversed(range(1, len(game_dump) - 1)):
        rewards[i] = game_dump[i]['score'] - game_dump[i-1]['score'] + (GAMMA * rewards[i+1])
    return rewards

print('--- MAPPING GAME DUMPS ---')

current_row = 0
for game_dump in game_dumps:
    rewards = calc_rewards(game_dump)
    for state_idx in range(1, len(game_dump)-1):
        inputs_keys[current_row] = game_dump[state_idx]['inputs']
        inputs_time[current_row] = game_dump[state_idx]['time']
        inputs_this_frame[current_row] = game_dump[state_idx]['screen']
        inputs_prev_frame[current_row] = game_dump[state_idx-1]['screen']
        labels[current_row] = rewards[state_idx]
        current_row += 1
print('NANs at: ', np.argwhere(np.isnan(labels)).tolist())
print('max reward:', labels.max())
if labels.max() != 0.:
    labels /= labels.max()
print('Labels: ', labels.tolist())

np.savez_compressed(DATA_SAVE_PATH,
                    inputs_keys=inputs_keys,
                    inputs_this_frame=inputs_this_frame,
                    inputs_prev_frame=inputs_prev_frame,
                    inputs_time=inputs_time,
                    labels=labels)