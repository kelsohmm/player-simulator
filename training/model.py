import keras as K
from config import MODEL_PREVIEW_PATH, CONV_SHAPE


def create_network():
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

    output_names = ["output_%d" % i for i in range(6)]
    output_layers = [K.layers.Dense(1, name=name)(hidden)
                     for name in output_names]

    model = K.models.Model(inputs=[frame_input],
                           outputs=output_layers)

    model.compile(optimizer=K.optimizers.Adam(), loss={name: K.losses.mean_squared_error for name in output_names})

    try:
        K.utils.plot_model(model, show_shapes=True, to_file=MODEL_PREVIEW_PATH)
    except:
        pass

    return model
