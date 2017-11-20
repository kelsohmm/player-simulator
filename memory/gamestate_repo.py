import numpy as np
from config import GLOB_JOB_ID
from data_transformations import map_action_idx_from_inputs
from memory.gamestate_database import GamestateDatabase


class GamestateRepo:
    END_GAME_REWARD = 0.

    def __init__(self, file_path):
        self.db = GamestateDatabase(file_path)
        self.last_transition = None
        self.prev_screen = None
        self.commit_number = 0

    def size(self):
        return self.db.size()

    def get_last_commit(self):
        return self._memory_from_commit(self.last_transition)

    def get_random_commits(self, batch_size):
        return list(map(self._memory_from_commit,
                        self.db.fetch_random_batch(batch_size)))

    def commit(self, screen, score, inputs, _time):
        if self.prev_screen is not None:
            print(np.count_nonzero(self.prev_screen))
            self.last_transition = (
                GLOB_JOB_ID.job_id,
                self._postincremented_commit_number(),
                self.prev_screen.tostring(),
                self.prev_action_idx,
                score - self.prev_score,
                screen.tostring()
            )
            self.db.insert_transition(*self.last_transition)

        self._update_prevs(screen, score, inputs)

    def close(self):
        self.last_transition = (
            GLOB_JOB_ID.job_id,
            self._postincremented_commit_number(),
            self.prev_screen.tostring(),
            self.prev_action_idx,
            self.END_GAME_REWARD,
            None
        )
        self.db.insert_transition(*self.last_transition)

    def _memory_from_commit(self, commit):
        _, _, prev_screen_text, action_idx, reward, next_screen_text = commit
        return self._screen_from_text(prev_screen_text), action_idx, reward, self._screen_from_text(next_screen_text)

    def _screen_from_text(self, screen_text):
        return np.fromstring(screen_text, dtype=np.ubyte).reshape((128, 128, 1)) \
            if screen_text is not None else None

    def _update_prevs(self, screen, score, inputs):
        self.prev_screen = screen
        self.prev_score = score
        self.prev_action_idx = map_action_idx_from_inputs(inputs)

    def _postincremented_commit_number(self):
        self.commit_number += 1
        return self.commit_number - 1

