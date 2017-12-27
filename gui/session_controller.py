import sqlite3
import numpy as np
from gui.charts_window import ChartsWindow
from gui.session_window import SessionWindow
from memory.db_commands import get_max_game_id, get_db_size, get_max_state_id, get_max_score
from session import Session


class SessionController:
    def __init__(self, session_path):
        self.session = Session(session_path)
        self.db_conn = sqlite3.connect(self.session.db_path)
        self.window = SessionWindow(self._create_overall_stats(), self._open_charts_window)

    def _open_charts_window(self):
        array = np.zeros((256, 256, 3), dtype=np.ubyte)
        ChartsWindow('charts', {'abc': array})

    def _create_overall_stats(self):
        stats = {
            'Games played': get_max_game_id(self.db_conn),
            'States count': get_db_size(self.db_conn),
            'Longest game (in states)': get_max_state_id(self.db_conn),
            'Best score': get_max_score(self.db_conn),
        }
        return stats
