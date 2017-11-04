import os
import random
import numpy as np
from config import DUMPS_DIR, MODEL_SAVE_PATH, MODEL_PREVIEW_PATH

api_subdirs = [api_subdir
               for api_subdir in os.listdir(DUMPS_DIR)
               if os.path.isdir(os.path.join(DUMPS_DIR, api_subdir))]

dump_files = [os.path.join(DUMPS_DIR, api_subdir, filename)
              for api_subdir in api_subdirs
              for filename in os.listdir(os.path.join(DUMPS_DIR, api_subdir))][:5]
random.shuffle(dump_files)
print('GAMEDUMPS FOUND: ', dump_files)


print("--- LOADING FILE DUMPS ---")

game_dumps = []
for filepath in dump_files:
    state_dumps = []
    with open(filepath, 'rb+') as f:
        try:
            while True:
                state_dumps.append(np.load(f))
        except:
            pass
    game_dumps.append(state_dumps)

no_state_dumps = sum(map(lambda x: len(x), game_dumps)) \
                 - len(game_dumps)  # dropping first frame in each game dump

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
        labels[state_idx] = rewards[state_idx]
        current_row += 1
print('NANs at: ', np.argwhere(np.isnan(labels)).tolist())
labels /= labels.max()
print('Labels: ', labels.tolist())

print("--- STARTING LEARNING PROCESS ---")

import keras as K

time_input = K.Input(shape=(1,))
keys_input = K.Input(shape=(3,))
this_frame_input = K.Input(shape=(128, 128, 3))
prev_frame_input = K.Input(shape=(128, 128, 3))

shared_conv = K.layers.Conv2D(filters=64, kernel_size=(4, 4), input_shape=(128, 128, 3), data_format='channels_last')
conved_this_frame = K.layers.Flatten()(shared_conv(this_frame_input))
conved_prev_frame = K.layers.Flatten()(shared_conv(prev_frame_input))

hidden = K.layers.concatenate([time_input, keys_input, conved_this_frame, conved_prev_frame], axis=-1)
hidden = K.layers.Dense(64, activation='relu')(hidden)
hidden = K.layers.Dense(32, activation='relu')(hidden)
main_output = K.layers.Dense(1, name='main_output')(hidden)

model = K.models.Model(inputs=[time_input, keys_input, this_frame_input, prev_frame_input],
                           outputs=[main_output])

model.compile(optimizer='rmsprop', loss='mean_squared_error')

history = model.fit([inputs_time, inputs_keys, inputs_this_frame, inputs_prev_frame],
                      [labels],
                      epochs=3 , verbose=2, validation_split=0.1)
print(history.history)

model.save(MODEL_SAVE_PATH)
K.utils.plot_model(model, to_file=MODEL_PREVIEW_PATH)

print('--- EVALUATING ---')

print(model.evaluate([inputs_time, inputs_keys, inputs_this_frame, inputs_prev_frame],
                     [labels]))
