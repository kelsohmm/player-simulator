from config_builder import SESSION_CONFIG_VALIDATIORS, build_validated, CONV_LAYERS_CONFIG_VALIDATORS, \
    DENSE_LAYERS_CONFIG_VALIDATORS
from gui.session_create.session_create_window import SessionCreateWindow
from gui.utils import show_error
from simulator.agent.model import build_network_from_layers_config

_CONVOLUTION_INITIAL_CONFIG = {
    'Filters': 64,
    'Kernel size': 64,
    'Strides': 64,
}
_DENSE_INITIAL_CONFIG = {
    'Units': 256,
    'Activation': 'relu'
}
_SESSION_INITIAL_CONFIG = {
    'Frame width': 128,
    'Frame height': 128,
    'Frames stacked': 4,
    'Learning rate': 0.001,
    'LR Decay': 0.9,
}

_SESSION_CONFIG_FIELD_NAME_MAPPING = {
    'Frame width': 'frame_width',
    'Frame height': 'frame_height',
    'Frames stacked': 'frames_stacked',
    'Learning rate': 'learning_rate',
    'LR Decay': 'lr_decay',
}

class SessionCreateController:
    def __init__(self, session_path, session_created_callback):
        self.session_path = session_path
        self.session_created_callback = session_created_callback
        self.window = SessionCreateWindow(_CONVOLUTION_INITIAL_CONFIG, _DENSE_INITIAL_CONFIG, _SESSION_INITIAL_CONFIG, self.create_session)

    def create_session(self, layers_config, session_config):
        conv_configs, dense_configs = layers_config
        session_config = self._remap_config_names(session_config, _SESSION_CONFIG_FIELD_NAME_MAPPING)

        try:
            session_config = build_validated(session_config, SESSION_CONFIG_VALIDATIORS)
            conv_configs = [build_validated(conv_config, CONV_LAYERS_CONFIG_VALIDATORS) for conv_config in conv_configs]
            dense_configs = [build_validated(dense_config, DENSE_LAYERS_CONFIG_VALIDATORS) for dense_config in dense_configs]

            model = build_network_from_layers_config(session_config, conv_configs, dense_configs)

            print(model)
        except _ as e:
            show_error(str(e))

    def _remap_config_names(self, config, mapping):
        return {
            mapping[original_name]: config[original_name]
            for original_name in config.keys()
        }
