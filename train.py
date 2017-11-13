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

    frame_input = K.Input(shape=(128, 128, 3), name='frame_input')

    conv = K.layers.Conv2D(filters=32, kernel_size=8, strides=4, name='conv_1', input_shape=(128, 128, 3), data_format='channels_last')(frame_input)
    conv = K.layers.Conv2D(filters=64, kernel_size=4, strides=2, name='conv_2')(conv)
    conv = K.layers.Conv2D(filters=64, kernel_size=3, strides=2, name='conv_3')(conv)
    conved_frame = K.layers.Flatten()(conv)
    flat_frame = K.layers.Flatten()(frame_input)

    concat = K.layers.concatenate([conved_frame, flat_frame])
    hidden = K.layers.Dense(2048, activation='relu', name='hidden_1')(concat)
    hidden = K.layers.Dense(512, activation='relu', name='hidden_2')(hidden)

    output_names = ["output_%d" % i for i in range(6)]
    output_layers = [K.layers.Dense(1, name=name)(
                        K.layers.Dense(128)(hidden)
                     )
                     for name in output_names]

    model = K.models.Model(inputs=[frame_input],
                           outputs=output_layers)

    model.compile(optimizer=K.optimizers.Adamax(lr=0.0005), loss={name: loss_mse_for_known for name in output_names})

    try:
        K.utils.plot_model(model, show_shapes=True, to_file=MODEL_PREVIEW_PATH)
    except:
        pass

    history = model.fit([inputs_frame],
                        [labels[:, i] for i in range(6)],
                        epochs=7, verbose=2, validation_split=0.3)
    print(history.history)

    model.save(MODEL_SAVE_PATH)

    print('--- EVALUATING ---')

    print(model.evaluate([inputs_frame],
                         [labels[:, i] for i in range(6)]))
