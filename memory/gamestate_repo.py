import numpy as np
from config import CONV_SHAPE

MIN_TO_COMMIT = 5


class Repo:
    def __init__(self, database):
        self.db = database
        self.initial_db_size = self.db.size()
        self.game_number = self.db.get_free_game_id()
        self.commit_number = 0
        self.last_action_idx = 0

    def size(self):
        return self.initial_db_size + self.commit_number

    def get_commits_batch(self, batch_size):
        return list(map(self._memory_from_commit,
                        self.db.fetch_by_action_idx(self.last_action_idx, batch_size)))

    def commit(self, screen, score, action_idx, predictions):
        self.commit_number += 1
        self.db.insert(self.game_number,
                       self.commit_number,
                       screen.tostring(),
                       action_idx,
                       score,
                       predictions)
        self.last_action_idx = action_idx

    def close(self):
        if self.commit_number > MIN_TO_COMMIT:
            self.db.commit_changes()
        else:
            self.db.rollback_changes()

    def _memory_from_commit(self, commit):
        prev_screen_text, action_idx, prev_score, next_score, next_screen_text = commit
        return self._screen_from_text(prev_screen_text), action_idx, prev_score, next_score, self._screen_from_text(next_screen_text)

    def _screen_from_text(self, screen_text):
        return np.fromstring(screen_text, dtype=np.ubyte).reshape(CONV_SHAPE) \
            if screen_text is not None else None
