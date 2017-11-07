import numpy as np
from config import DUMPS_DIR, DATA_SAVE_PATH
from data_transformations import DATA_DTYPE, map_one_episode
from training.utils import find_all_filepaths, read_episode_files

dump_files = find_all_filepaths(DUMPS_DIR, shuffle=True)
print('GAMEDUMPS FOUND: ', dump_files)

game_dumps = read_episode_files(dump_files)
print('EPISODES:', len(game_dumps))

no_state_dumps = sum(map(lambda episode: len(episode), game_dumps))
print('STATES:', no_state_dumps)

print('--- MAPPING GAME DUMPS ---')
data = np.zeros(no_state_dumps, dtype=DATA_DTYPE)
current_row = 0
for game_dump in game_dumps:
    no_states = len(game_dump)
    map_one_episode(game_dump, data[current_row:current_row+no_states])
    current_row += no_states

print('max reward:', data[:]['reward'].max())
if data[:]['reward'].max() != 0.:
    data[:]['reward'] /= data[:]['reward'].max()
print('Rewards: ', data[:]['reward'].tolist())

print('--- SAVING MAPPED DATA ---')
np.savez_compressed(DATA_SAVE_PATH,
                    inputs_keys=data[:]['inputs'],
                    inputs_frame=data[:]['conv_input'],
                    inputs_time=data[:]['time'],
                    labels=data[:]['reward'])
