import numpy as np
import datetime
import os

class GamestateRepo:
    DUMPS_DIR = 'gamestate_dumps'

    def __init__(self, file_path):
        self.file_path = file_path
        self.file = None
        self.matrix = None

    def commit(self, screen, score, inputs):
        if self.file is None:
            self._init(screen, inputs)

        self.matrix['screen'] = screen
        self.matrix['score'] = score
        self.matrix['inputs'] = inputs

        np.save(self.file, self.matrix)

    def _init(self, screen, inputs):
        self.matrix = np.zeros(1,dtype=[('screen', screen.dtype, screen.shape),
                                        ('score',np.int16),
                                        ('inputs', np.uint16, len(inputs))])
        self.file = open(self.file_path, 'w+b')

    def close(self):
        self.file.close()

