import tensorflow as tf
import keras as K
from config import CONV_SHAPE


def loss_mse_for_known(y_true, y_pred):
    replaced = tf.where(tf.is_nan(y_true), y_pred, y_true)
    return K.backend.mean(K.backend.square(replaced - y_pred), axis=-1)


def create_network(preview_path):
    print("--- STARTING LEARNING PROCESS ---")

    frame_input = K.Input(shape=CONV_SHAPE, name='frame_input')

    conv = K.layers.Conv2D(filters=32, kernel_size=8, strides=4, name='conv_1', input_shape=CONV_SHAPE, data_format='channels_last')(frame_input)
    conv = K.layers.Conv2D(filters=64, kernel_size=4, strides=2, name='conv_2')(conv)
    conv = K.layers.Conv2D(filters=64, kernel_size=3, strides=2, name='conv_3')(conv)
    conved_frame = K.layers.Flatten()(conv)
    flat_frame = K.layers.Flatten()(frame_input)

    concat = K.layers.concatenate([conved_frame, flat_frame])
    hidden = K.layers.Dense(512, activation='relu', name='hidden_1')(concat)
    hidden = K.layers.Dense(512, activation='relu', name='hidden_2')(hidden)

    output = K.layers.Dense(6, name='output')(hidden)

    model = K.models.Model(inputs=[frame_input],
                           outputs=output)

    model.compile(optimizer=K.optimizers.Adam(), loss=loss_mse_for_known)

    try:
        K.utils.plot_model(model, show_shapes=True, to_file=preview_path)
    except:
        pass

    return model

def load_model(model_path):
    return K.models.load_model(model_path, custom_objects={'loss_mse_for_known': loss_mse_for_known})