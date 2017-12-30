from gui.session_create.session_create_window import SessionCreateWindow


class SessionCreateController:
    def __init__(self, session_path, session_created_callback):
        self.session_path = session_path
        self.session_created_callback = session_created_callback
        self.window = SessionCreateWindow(self._add_new_conv, self._add_new_dense)

    def _add_new_conv(self):
        print("Conv")

    def _add_new_dense(self):
        print("Conv")