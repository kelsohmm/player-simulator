import tensorflow as tf
import keras as K

def loss_mse_for_known(y_true, y_pred):
    replaced = tf.where(tf.is_nan(y_true), y_pred, y_true)
    return K.backend.mean(K.backend.square(replaced - y_pred), axis=-1)

if __name__ == '__main__':
    import numpy as np
    from config import DATA_SAVE_PATH, MODEL_SAVE_PATH, MODEL_PREVIEW_PATH

    loaded = np.load(DATA_SAVE_PATH)
    inputs_frame = loaded['inputs_frame']
    labels = loaded['labels']

    print("--- STARTING LEARNING PROCESS ---")

    frame_input = K.Input(shape=(128, 128, 3))

    conv = K.layers.Conv2D(filters=32, kernel_size=6, strides=2, name='conv_1', input_shape=(128, 128, 3), data_format='channels_last')(frame_input)
    conv = K.layers.Conv2D(filters=64, kernel_size=3, strides=2, name='conv_2')(conv)
    conved_frame = K.layers.Flatten()(conv)
    # flatted_frame = K.layers.Flatten()(frame_input)

    hidden = K.layers.Dense(512, activation='relu', name='hidden_1')(conved_frame)
    hidden = K.layers.Dense(256, activation='relu', name='hidden_2')(hidden)
    main_output = K.layers.Dense(6, name='main_output')(hidden)

    model = K.models.Model(inputs=[frame_input],
                           outputs=[main_output])

    model.compile(optimizer='rmsprop', loss=loss_mse_for_known)

    history = model.fit([inputs_frame],
                        [labels],
                        epochs=7, verbose=2, validation_split=0.1)
    print(history.history)

    model.save(MODEL_SAVE_PATH)
    K.utils.plot_model(model, to_file='model.png')

    print('--- EVALUATING ---')

    print(model.evaluate([inputs_frame],
                         [labels]))
