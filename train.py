import os
import numpy as np
import keras

path = 'gamestate_dumps\\20171027-011506_'
dump_files = [os.path.join(path, f) for f in os.listdir(path)]

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
labels = np.zeros((no_state_dumps,), dtype=np.float16)

def calc_rewards(game_dump):
    GAMMA = 0.5
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
        inputs_this_frame[current_row] = game_dump[state_idx]['screen']
        inputs_prev_frame[current_row] = game_dump[state_idx-1]['screen']
        labels[state_idx] = rewards[state_idx]
        current_row += 1

labels /= labels.max()
labels -= labels.mean()
print(labels)

print("--- STARTING LEARNING PROCESS ---")

keys_input = keras.Input(shape=(3,))
this_frame_input = keras.Input(shape=(128, 128, 3))
prev_frame_input = keras.Input(shape=(128, 128, 3))

shared_conv = keras.layers.Conv2D(filters=8, kernel_size=(6, 6), input_shape=(128, 128, 3), data_format='channels_last')
conved_this_frame = keras.layers.Flatten()(shared_conv(this_frame_input))
conved_prev_frame = keras.layers.Flatten()(shared_conv(prev_frame_input))

hidden = keras.layers.concatenate([keys_input, conved_this_frame, conved_prev_frame], axis=-1)
hidden = keras.layers.Dense(64, activation='relu')(hidden)
hidden = keras.layers.Dense(64, activation='relu')(hidden)
main_output = keras.layers.Dense(1, name='main_output')(hidden)

model = keras.models.Model(inputs=[keys_input, this_frame_input, prev_frame_input],
                           outputs=[main_output])

model.compile(optimizer='rmsprop', loss='binary_crossentropy')

history = model.fit([inputs_keys, inputs_this_frame, inputs_prev_frame],
                      [labels],
                      epochs=3, verbose=2)

model.save('model.h5')

print('--- EVALUATING ---')

print(model.evaluate([inputs_keys, inputs_this_frame, inputs_prev_frame],
                [labels]))