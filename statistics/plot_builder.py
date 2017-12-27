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

    def get_final_scores_plot(self):
        data = self._data_view.get()\
                .groupby('game_id')['score']\
                .last()
        plot = data.plot()
        return self._get_plot_img(plot)

    def show_final_scores_plot(self):
        self._show_window('Final scores', self.get_final_scores_plot())

    def get_move_usage_distribution_per_distance(self):
        data = self._data_view.get() \
            .round({'score': 0})\
            .groupby(['score'])['action_idx']\
            .count()
        data.describe()
        plot = data.plot.area()
        return self._get_plot_img(plot)

    def show_move_usage_distribution_per_distance(self):
        self._show_window('Move usage distribution', self.get_move_usage_distribution_per_distance())


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
