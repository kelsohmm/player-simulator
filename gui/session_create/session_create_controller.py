from gui.session_create.session_create_window import SessionCreateWindow

_CONVOLUTION_INITIAL_CONFIG = {
    'Filters': 64,
    'Kernel size': 64,
    'Strides': 64,
}
_DENSE_INITIAL_CONFIG = {
    'Units': 256,
}

class SessionCreateController:
    def __init__(self, session_path, session_created_callback):
        self.session_path = session_path
        self.session_created_callback = session_created_callback
        self.window = SessionCreateWindow(_CONVOLUTION_INITIAL_CONFIG, _DENSE_INITIAL_CONFIG)

