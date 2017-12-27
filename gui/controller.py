from gui.session_select_window import SessionSelectWindow
from gui.session_window import SessionWindow
from session import Session


class Controller:
    def __init__(self, session_path=None):
        if session_path is None:
            self._current_window = SessionSelectWindow(callback=self.session_path_selected)
        else:
            self.open_session_window(session_path)

    def session_path_selected(self, session_path):
        self._current_window.quit()
        self.open_session_window(session_path)

    def open_session_window(self, session_path):
        stats = {
            'game_length': 50,
            'avg. score': 2.15
        }
        self._current_window = SessionWindow(stats)