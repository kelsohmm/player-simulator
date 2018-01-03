from gui.session_select.session_select_window import SessionSelectWindow
from gui.utils import show_error
from session import verify_session_path

class SessionSelectController:
    def __init__(self, session_selected_callback):
        self.callback = session_selected_callback
        self.window = SessionSelectWindow(self._session_selected)

    def finish(self):
        self.window.destroy()
        self.window = None

    def _session_selected(self, path):
        if verify_session_path(path):
            self.callback(path)
            self.finish()
        else:
            show_error("Select empty directory to create a new session, or reopen existing session directory.")