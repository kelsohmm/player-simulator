import numpy as np
import os
from config import GLOB_JOB_ID


class GamestateRepo:
    def __init__(self, file_path, inputs_len):
        self.file_path = os.path.join(file_path, GLOB_JOB_ID.job_id + '.npy')
        self.matrix = np.zeros(1, dtype=[('screen', np.ubyte, (128, 128, 3)),
                                         ('score',np.int16),
                                         ('inputs', np.ubyte, inputs_len),
                                         ('time', np.float64)])
        self.commits = []

    def commit(self, screen, score, inputs, time):
        self.matrix['screen'] = screen
        self.matrix['score'] = score
        self.matrix['inputs'] = inputs
        self.matrix['time'] = time

        self.commits.append(self.matrix.copy())

    def close(self):
        file = open(self.file_path, 'w+b')
        for commit in self.commits:
            np.save(file, commit)
        file.close()

