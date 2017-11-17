import numpy as np
from config import GLOB_JOB_ID
from data_transformations import map_action_idx_from_inputs
from memory.gamestate_database import GamestateDatabase


class GamestateRepo:
    def __init__(self, file_path, inputs_len):
        self.db = GamestateDatabase(file_path)
        self.matrix = np.zeros(1, dtype=[('screen', np.ubyte, (128, 128, 3)),
                                         ('score',np.int16),
                                         ('inputs', np.ubyte, inputs_len),
                                         ('time', np.float64)])
        self.commits = []

    def get_commits(self):
        return self.commits

    def ammend(self, subfield_name, value):
        self.commits[len(self.commits)-1][subfield_name] = value

    def commit(self, screen, score, inputs, time):
        self.matrix['screen'] = screen
        self.matrix['score'] = score
        self.matrix['inputs'] = inputs
        self.matrix['time'] = time

        self.commits.append(self.matrix.copy())

    def close(self):
        transitions = []
        last_idx = len(self.commits) - 1
        for idx in range(1, len(self.commits)):
            prev_commit = self.commits[idx-1]
            curr_commit = self.commits[idx]
            transitions.append((
                GLOB_JOB_ID.job_id,
                idx-1,
                prev_commit['screen'].tostring(),
                map_action_idx_from_inputs(prev_commit['inputs']),
                curr_commit['score'] - prev_commit['score'],
                curr_commit['screen'].tostring() if idx != last_idx else None
            ))

