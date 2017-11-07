import numpy as np
from config import DATA_SAVE_PATH, MODEL_SAVE_PATH, MODEL_PREVIEW_PATH
import keras as K

loaded = np.load(DATA_SAVE_PATH)
inputs_keys = loaded['inputs_keys']
inputs_frame = loaded['inputs_frame']
inputs_time = loaded['inputs_time']
labels = loaded['labels']

print("--- STARTING LEARNING PROCESS ---")

time_input = K.Input(shape=(1,))
keys_input = K.Input(shape=(3,))
frame_input = K.Input(shape=(128, 128, 3))

conv = K.layers.Conv2D(filters=64, kernel_size=(4, 4), input_shape=(128, 128, 3), data_format='channels_last')
conved_frame = K.layers.Flatten()(conv(frame_input))

hidden = K.layers.concatenate([time_input, keys_input, conved_frame])
hidden = K.layers.Dense(64, activation='relu')(hidden)
hidden = K.layers.Dense(32, activation='relu')(hidden)
main_output = K.layers.Dense(1, name='main_output')(hidden)

model = K.models.Model(inputs=[time_input, keys_input, frame_input],
                           outputs=[main_output])

model.compile(optimizer='rmsprop', loss='mean_squared_error')

history = model.fit([inputs_time, inputs_keys, inputs_frame],
                      [labels],
                      epochs=7, verbose=2, validation_split=0.1)
print(history.history)

model.save(MODEL_SAVE_PATH)
K.utils.plot_model(model, to_file=MODEL_PREVIEW_PATH)

print('--- EVALUATING ---')

print(model.evaluate([inputs_time, inputs_keys, inputs_frame],
                     [labels]))
