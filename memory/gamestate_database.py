import random
import sqlite3
import os
from config import GLOB_JOB_ID


class GamestateDatabase:
    def __init__(self, filepath):
        self.filepath = filepath
        self.conn = sqlite3.connect(os.path.join(self.filepath, 'transitions.db'))
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE transitions
                                 (game_id INT,
                                  time INT,
                                  curr_state TEXT NOT NULL, 
                                  action_idx INT NOT NULL,
                                  reward REAL NOT NULL, 
                                  next_state TEXT,
                                  PRIMARY KEY (game_id, time))''')
        self.games_duration = {}
        self.conn.commit()

    def _fetch_transitions(self, game_times):
        return self.cursor.executemany('SELECT curr_state, action_idx, reward, next_state'
                                       'WHERE game_id=? AND time=?'
                                       'LIMIT 1', game_times)

    def _random_game_time(self, game_id):
        return random.randint(0, self.games_duration[game_id])

    def fetch_random_batch(self, batch_size):  # add fetched action idx
        games = random.sample(self.games_duration.keys(), batch_size)
        game_times = [(game_id, self._random_game_time(game_id)) for game_id in games]
        return self._fetch_transitions(game_times)

    def _init_new_game(self, game_id):
        self.conn.commit()
        self.games_duration[game_id] = 0

    def insert_transition(self, game_id, curr_state, action_idx, reward, next_state):
        if game_id not in self.games_duration:
            self._init_new_game(game_id)

        self.games_duration[game_id] += 1
        self.conn.execute('INSERT INTO transitions VALUES (?,?,?,?,?,?)',
                          (game_id, self.games_duration[game_id], curr_state, action_idx, reward, next_state))