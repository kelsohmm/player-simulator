import numpy as np
import datetime
import os

class GamestateRepo:
    DUMPS_DIR = 'gamestate_dumps'

    def __init__(self, file_id):
        self.file_path = os.path.join(
            self.DUMPS_DIR,
            datetime.datetime.now().strftime("%Y%m%d-%H%M%S_") + file_id + ".npy")
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

