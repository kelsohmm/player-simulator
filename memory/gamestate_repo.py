import numpy as np
from config import CONV_SHAPE


class Repo:
    END_GAME_REWARD = 0.

    def __init__(self, database):
        self.db = database
        self.prev_screen = None
        self.initial_db_size = self.db.size()
        self.game_number = self.db.get_free_game_id()
        self.commit_number = 0
        self.prev_action_idx = 0

    def size(self):
        return self.initial_db_size + self.commit_number

    def get_commits_batch(self, batch_size):
        return list(map(self._memory_from_commit,
                        self.db.fetch_random_batch(batch_size, self.prev_action_idx)))

    def commit(self, screen, score, action_idx):
        if self.prev_screen is not None:
            self._push_commit_to_database(score)

        self._update_prevs(screen, action_idx)

    def _push_commit_to_database(self, score):
        commit = (
            self.game_number,
            self.commit_number,
            self.prev_screen.as_matrix().tostring(),
            self.prev_action_idx,
            score,
        )
        self.commit_number += 1
        self.db.insert_transition(*commit)

    def close(self):
        self._push_commit_to_database(self.END_GAME_REWARD)

    def _memory_from_commit(self, commit):
        prev_screen_text, action_idx, reward, next_screen_text = commit
        return self._screen_from_text(prev_screen_text), action_idx, reward, self._screen_from_text(next_screen_text)

    def _screen_from_text(self, screen_text):
        return np.fromstring(screen_text, dtype=np.ubyte).reshape(CONV_SHAPE) \
            if screen_text is not None else None

    def _update_prevs(self, screen, action_idx):
        self.prev_screen = screen
        self.prev_action_idx = action_idx


