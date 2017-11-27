import random
import sqlite3
from sqlite3 import Binary
import os

_DATABASE_SCHEMA = '''CREATE TABLE transitions
                                 (game_id INT,
                                  time INT,
                                  curr_state BLOB NOT NULL, 
                                  action_idx INT NOT NULL,
                                  reward REAL NOT NULL, 
                                  next_state BLOB,
                                  PRIMARY KEY (game_id, time))'''

class Database:
    def __init__(self, filepath):
        self.filepath = filepath
        self.conn = sqlite3.connect(os.path.join(self.filepath, 'transitions.db'))
        self.cursor = self.conn.cursor()
        self.cursor.execute(_DATABASE_SCHEMA)
        self.conn.commit()
        self.db_size = self._query_transitions_count()

    def size(self):
        return self.db_size

    def fetch_random_batch(self, batch_size, action_idx):
        return list(self.cursor.execute('SELECT * FROM transitions WHERE action_idx=%d ORDER BY RANDOM() LIMIT %d' % (batch_size, action_idx)))

    def insert_transition(self, game_id, time, curr_state, action_idx, reward, next_state):
        self.db_size += 1
        curr_state = Binary(curr_state)
        next_state = Binary(next_state) if next_state is not None else None
        self.cursor.execute('INSERT INTO transitions VALUES (?,?,?,?,?,?)',
                            (game_id, time, curr_state, action_idx, reward, next_state))
        self.conn.commit()

    def _query_transitions_count(self):
        res = self.cursor.execute('SELECT COUNT(*) FROM transitions')
        (count, ) = list(res)[0]
        return count
