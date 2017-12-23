import numpy as np
import matplotlib.pyplot as plt
import cv2
from math import floor


def _groupby_chunk(chunks):
    return lambda index: floor(index / chunks)


class PlotBuilder:
    def __init__(self, data_view, epoch_size=500):
        self._epoch_size = epoch_size
        self._data_view = data_view

    def show_average_final_score_plot(self):
        data = self._data_view.get()\
                .groupby(_groupby_chunk(self._epoch_size))['score']\
                .mean()
        plot = data.plot()

        self._show_window('Average final score per training epoch', self._get_plot_img(plot))

    def _show_window(self, window_name, img):
        cv2.imshow(window_name, img)
        cv2.waitKey(20)

    def _get_plot_img(self, plot):
        fig = plot.figure
        fig.canvas.draw()
        data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        img = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        plt.close(fig)

        return img
