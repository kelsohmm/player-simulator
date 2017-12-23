import numpy as np
import cv2
import pandas as pd

class ScoreChart:
    WINDOW_NAME = 'Score chart'

    def __init__(self, data, epoch_size=500):
        self._epoch_size = epoch_size
        self._data = data

    def append(self, new_data):
        self._data = np.append(self._data, new_data)

    def _get_series(self):
        return pd.Series(self._data,
                         index=np.arange(self._data.size))

    def plot(self):
        fig = self._get_series().plot().figure
        fig.canvas.draw()
        data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        img = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))

        cv2.imshow(self.WINDOW_NAME, img)
        cv2.waitKey(20)

