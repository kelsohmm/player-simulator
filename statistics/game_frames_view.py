import sqlite3
import numpy as np
from config import CONV_SHAPE, FRAMES_STACKED

_SELECT_HISTORY_QUERY = 'SELECT state FROM history WHERE game_id = %d ORDER BY state_id ASC'


class GameFramesView:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def get_for_game_id(self, game_id):
        self.cursor.execute(_SELECT_HISTORY_QUERY % game_id)
        data = []

        records = self.cursor.fetchall()
        for (state_text,) in records:
            data = data + self._split_into_frames(state_text)

        return data

    def _screen_from_text(self, screen_text):
        return np.fromstring(screen_text, dtype=np.ubyte).reshape(CONV_SHAPE) \
            if screen_text is not None else None

    def _split_into_frames(self, state_text):
        state = self._screen_from_text(state_text)
        return np.split(state, FRAMES_STACKED, axis=2)
