import os
from gui.session_control.session_controller import SessionController
from gui.session_create.session_create_controller import SessionCreateController
from gui.session_select.session_select_controller import SessionSelectController


class ProgramController:
    def __init__(self, session_path=None):
        self.session_path = session_path
        if session_path is None:
            self._active_controller = SessionSelectController(session_selected_callback=self.session_path_selected)
        else:
            self.session_path_selected(session_path)

    def session_path_selected(self, session_path):
        self.session_path = session_path
        if len(os.listdir(session_path)) == 0:
            self._active_controller = SessionCreateController(session_path, session_created_callback=self.new_session_created)
        else:
            self._active_controller = SessionController(session_path)

    def new_session_created(self):
        self._active_controller = SessionController(self.session_path)


