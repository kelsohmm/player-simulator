import tensorflow as tf
import keras as K


def loss_mse_for_known(y_true, y_pred):
    nan_difference = y_pred - y_true
    difference = tf.where(tf.is_nan(nan_difference), tf.zeros_like(y_pred), nan_difference)
    sum = K.backend.sum(difference, axis=1)
    res = K.backend.mean(K.backend.square(sum))
    res = tf.Print(res, [res, y_true, y_pred, sum, difference], 'LOSS: ', summarize=7)
    return res

def build_network_from_layers_config(session_config, conv_configs, dense_configs):
    conv_shape = (session_config['frame_width'],) + (session_config['frame_height'],) + (session_config['frames_stacked'],)
    frame_input = K.Input(shape=conv_shape, name='frame_input')

    conv_config_head, conv_configs_tail = conv_configs[0], conv_configs[1:]
    network = K.layers.Conv2D(filters=conv_config_head['Filters'], kernel_size=conv_config_head['Kernel size'], strides=conv_config_head['Strides'],
                            name='conv_1', input_shape=conv_shape, data_format='channels_last')(frame_input)

    for idx, conv_layer in enumerate(conv_configs_tail, start=1):
        network = K.layers.Conv2D(filters=conv_layer['Filters'], kernel_size=conv_layer['Kernel size'], strides=conv_layer['Strides'],name='conv_%d'%idx)(network)

    conved_frame = K.layers.Flatten()(network)
    flat_frame = K.layers.Flatten()(frame_input)
    network = K.layers.concatenate([conved_frame, flat_frame])

    for idx, dense_layer in enumerate(dense_configs):
        network = K.layers.Dense(dense_layer['Units'], activation=dense_layer['Activation'], name='hidden_%d'%idx)(network)

    output = K.layers.Dense(6, name='output')(network)

    model = K.models.Model(inputs=[frame_input],
                           outputs=output)

    model.compile(optimizer=K.optimizers.Adam(lr=session_config['learning_rate'], decay=session_config['lr_decay']),
                  loss=loss_mse_for_known)

    return model


def plot_model(preview_path, model):
    try:
        K.utils.plot_model(model, show_shapes=True, to_file=preview_path)
    except:
        pass


def create_network(preview_path):
    conv_layers_config = [
        {'Filters': 32, 'Kernel size': 8, 'Strides': 4},
        {'Filters': 64, 'Kernel size': 4, 'Strides': 2},
        {'Filters': 64, 'Kernel size': 3, 'Strides': 2},
    ]
    dense_layers_config = [
        {'Units': 512, 'Activation': 'relu'},
        {'Units': 512, 'Activation': 'relu'},
    ]
    session_config = {
        'Frame width': 128,
        'Frame height': 128,
        'Frames stacked': 4,
        'Learning rate': 0.00001,
        'LR Decay': 0.9,
    }

    model = build_network_from_layers_config(session_config, conv_layers_config, dense_layers_config)

    plot_model(preview_path, model)

    return model

def load_model(model_path):
    return K.models.load_model(model_path, custom_objects={'loss_mse_for_known': loss_mse_for_known})