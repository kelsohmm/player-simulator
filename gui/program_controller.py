from gui.session_controller import SessionController
from gui.session_select import SessionSelectWindow


class ProgramController:
    def __init__(self, session_path=None):
        self.session = None
        if session_path is None:
            self._active_controller = SessionSelectWindow(callback=self.session_path_selected)
        else:
            self.session_path_selected(session_path)

    def session_path_selected(self, session_path):
        self._active_controller = SessionController(session_path)

