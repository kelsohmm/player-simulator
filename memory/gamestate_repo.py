import numpy as np
from config import CONV_SHAPE


class Repo:
    def __init__(self, database):
        self.db = database
        self.initial_db_size = self.db.size()
        self.game_number = self.db.get_free_game_id()
        self.commit_number = 0

    def size(self):
        return self.initial_db_size + self.commit_number

    def get_commits_batch(self, batch_size):
        return list(map(self._memory_from_commit,
                        self.db.fetch_random_batch(batch_size)))

    def commit(self, screen, score, action_idx):
        commit = (
            self.game_number,
            self.commit_number,
            screen.tostring(),
            action_idx,
            score,
        )
        self.commit_number += 1
        self.db.insert(*commit)

    def _memory_from_commit(self, commit):
        prev_screen_text, action_idx, prev_score, next_score, next_screen_text = commit
        return self._screen_from_text(prev_screen_text), action_idx, prev_score, next_score, self._screen_from_text(next_screen_text)

    def _screen_from_text(self, screen_text):
        return np.fromstring(screen_text, dtype=np.ubyte).reshape(CONV_SHAPE) \
            if screen_text is not None else None
