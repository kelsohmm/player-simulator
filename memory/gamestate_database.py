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

class GamestateDatabase:
    def __init__(self, filepath):
        self.filepath = filepath
        self.conn = sqlite3.connect(os.path.join(self.filepath, 'transitions.db'))
        self.cursor = self.conn.cursor()
        self.games_duration = {}
        self.db_size = 0
        self.cursor.execute(_DATABASE_SCHEMA)
        self.conn.commit()

    def size(self):
        return self.db_size

    def fetch_random_batch(self, batch_size):  # add fetched action idx
        return self.cursor.execute('SELECT * FROM transitions ORDER BY RANDOM() LIMIT %d' % batch_size)

    def insert_transition(self, game_id, time, curr_state, action_idx, reward, next_state):
        if game_id not in self.games_duration:
            self._init_new_game(game_id)

        self.db_size += 1
        self.games_duration[game_id] += 1
        self.cursor.execute('INSERT INTO transitions VALUES (?,?,?,?,?,?)',
                            (game_id, time, Binary(curr_state), action_idx, reward, Binary(next_state)))
        self.conn.commit()

    def _random_game_time(self, game_id):
        return random.randint(0, self.games_duration[game_id])

    def _init_new_game(self, game_id):
        self.games_duration[game_id] = 0
