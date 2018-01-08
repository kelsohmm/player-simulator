
class PlotBuilder:
    def __init__(self, data_view, epoch_size=500):
        self._epoch_size = epoch_size
        self._data_view = data_view

    def plot_game_score(self, game_id, ax):
        self._data_view.get_for_game(game_id)['score'].plot(ax=ax)

    def plot_render_time(self, ax):
        time_diffs = self._data_view.get().groupby('game_id')['timestamp'].diff()
        time_diffs.clip(0.0, time_diffs.std()) \
            .plot(ax=ax)

    def plot_final_scores(self, ax):
        data = self._data_view.get()\
                .groupby('game_id')['score']\
                .last()
        data.plot(ax=ax)

    def plot_action_value_predictions(self, ax):
        self._data_view.get()\
            [['pred1', 'pred2', 'pred3', 'pred4', 'pred5', 'pred6']] \
            .plot(ax=ax)

