import sqlite3

from gui.session_select_window import SessionSelectWindow
from gui.session_window import SessionWindow
from memory.db_commands import get_max_game_id, get_db_size, get_max_state_id, get_max_score
from session import Session


class ProgramController:
    def __init__(self, session_path=None):
        self.session = None
        if session_path is None:
            self._current_window = SessionSelectWindow(callback=self.session_path_selected)
        else:
            self.open_session_window(session_path)

    def session_path_selected(self, session_path):
        self._current_window.quit()
        self.open_session_window(session_path)

    def open_session_window(self, session_path):
        self.session = Session(session_path)
        self.db_conn = sqlite3.connect(self.session.db_path)
        self._current_window = SessionWindow(self._create_overall_stats())

    def _create_overall_stats(self):
        stats = {
            'Games played': get_max_game_id(self.db_conn),
            'States count': get_db_size(self.db_conn),
            'Longest game (in states)': get_max_state_id(self.db_conn),
            'Best score': get_max_score(self.db_conn),
        }
        return stats