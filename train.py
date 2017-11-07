import numpy as np
import keras as K
from config import DATA_SAVE_PATH, MODEL_SAVE_PATH, MODEL_PREVIEW_PATH

loaded = np.load(DATA_SAVE_PATH)
inputs_keys = loaded['inputs_keys']
inputs_frame = loaded['inputs_frame']
inputs_time = loaded['inputs_time']
labels = loaded['labels']

print("--- STARTING LEARNING PROCESS ---")

time_input = K.Input(shape=(1,))
keys_input = K.Input(shape=(3,))
frame_input = K.Input(shape=(128, 128, 3))

conv = K.layers.Conv2D(filters=32, kernel_size=6, strides=2, name='conv_1', input_shape=(128, 128, 3), data_format='channels_last')(frame_input)
conv = K.layers.Conv2D(filters=64, kernel_size=3, strides=2, name='conv_2')(conv)
conved_frame = K.layers.Flatten()(conv)
# flatted_frame = K.layers.Flatten()(frame_input)

concat = K.layers.concatenate([time_input, keys_input, conved_frame], name='concat')
hidden = K.layers.Dense(512, activation='relu', name='hidden_1')(concat)
hidden = K.layers.Dense(256, activation='relu', name='hidden_2')(hidden)
main_output = K.layers.Dense(1, name='main_output')(hidden)

model = K.models.Model(inputs=[time_input, keys_input, frame_input],
                       outputs=[main_output])

model.compile(optimizer='rmsprop', loss=K.losses.mean_squared_error)

history = model.fit([inputs_time, inputs_keys, inputs_frame],
                      [labels],
                      epochs=7, verbose=2, validation_split=0.1)
print(history.history)

model.save(MODEL_SAVE_PATH)
K.utils.plot_model(model, to_file=MODEL_PREVIEW_PATH)

print('--- EVALUATING ---')

print(model.evaluate([inputs_time, inputs_keys, inputs_frame],
                     [labels]))
