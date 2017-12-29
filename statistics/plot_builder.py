from math import floor


def _groupby_chunk(chunks):
    return lambda index: floor(index / chunks)


class PlotBuilder:
    def __init__(self, data_view, epoch_size=500):
        self._epoch_size = epoch_size
        self._data_view = data_view

    def plot_game_score(self, game_id, ax):
        data = self._data_view.get()
        data = data.loc[data['game_id'] == game_id]
        data['score'].plot(ax=ax)


    def plot_final_scores(self, ax):
        data = self._data_view.get()\
                .groupby('game_id')['score']\
                .last()
        data.plot(ax=ax)

    def plot_move_usage_distribution_per_distance(self, ax):
        data = self._data_view.get() \
            .round({'score': 0})\
            .groupby(['score'])['action_idx']\
            .count()
        data.plot.area(ax=ax)

