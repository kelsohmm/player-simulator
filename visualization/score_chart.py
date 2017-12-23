import numpy as np
import matplotlib.pyplot as plt
import cv2
from math import floor

def groupby_chunk(chunks):
    return lambda index: floor(index / chunks)

class ScoreChart:
    WINDOW_NAME = 'Score chart'

    def __init__(self, data_view, epoch_size=500):
        self._epoch_size = epoch_size
        self._data_view = data_view

    def plot(self):
        data = self._data_view.get() \
                              .groupby(groupby_chunk(self._epoch_size))['score']\
                              .mean()

        fig = data.plot().figure
        fig.canvas.draw()
        data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        img = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        plt.close(fig)

        cv2.imshow(self.WINDOW_NAME, img)
        cv2.waitKey(20)

