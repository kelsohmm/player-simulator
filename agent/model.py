import tensorflow as tf
import keras as K
from config import CONV_SHAPE


def loss_mse_for_known(y_true, y_pred):
    nan_difference = y_true - y_pred
    difference = tf.where(tf.is_nan(nan_difference), tf.zeros_like(y_pred), nan_difference)
    res = K.backend.mean(K.backend.abs(difference), axis=0)
    # res = tf.Print(res, [res, y_true, y_pred, nan_difference, difference], 'LOSS: ', summarize=5)
    return res


def create_network(preview_path):
    frame_input = K.Input(shape=CONV_SHAPE, name='frame_input')

    conv = K.layers.Conv2D(filters=32, kernel_size=8, strides=4, name='conv_1', input_shape=CONV_SHAPE, data_format='channels_last')(frame_input)
    conv = K.layers.Conv2D(filters=64, kernel_size=4, strides=2, name='conv_2')(conv)
    conv = K.layers.Conv2D(filters=64, kernel_size=3, strides=2, name='conv_3')(conv)
    conved_frame = K.layers.Flatten()(conv)
    flat_frame = K.layers.Flatten()(frame_input)

    concat = K.layers.concatenate([conved_frame, flat_frame])
    hidden = K.layers.Dense(512, activation='relu', name='hidden_1')(concat)
    hidden = K.layers.Dense(512, activation='relu', name='hidden_2')(hidden)

    output_names = ["output_%d" % i for i in range(6)]
    output_layers = [K.layers.Dense(1, name=name)(hidden)
                     for name in output_names]

    model = K.models.Model(inputs=[frame_input],
                           outputs=output_layers)

    model.compile(optimizer=K.optimizers.Adam(lr=0.0001), loss=loss_mse_for_known)

    try:
        K.utils.plot_model(model, show_shapes=True, to_file=preview_path)
    except:
        pass

    return model

def load_model(model_path):
    return K.models.load_model(model_path, custom_objects={'loss_mse_for_known': loss_mse_for_known})