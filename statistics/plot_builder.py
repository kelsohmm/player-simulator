import numpy as np
import pandas as pd


class PlotBuilder:
    def __init__(self, data_view, epoch_size=500):
        self._epoch_size = epoch_size
        self._data_view = data_view

    def plot_game_action_idxs(self, game_id, ax):
        data = self._data_view.get_for_game(game_id)
        data['state_id'] = pd.to_numeric(data['state_id'], errors='coerce')
        data.plot.scatter(x='score', y='state_id', c='action_idx', ax=ax, edgecolors='k')

    def plot_game_score(self, game_id, ax):
        self._data_view.get_for_game(game_id)\
            .plot(x='state_id', y='score', ax=ax)
        ax.set_xlabel('state_id')
        ax.set_ylabel('score')

    def plot_game_action_value_predictions(self, game_id, ax):
        self._data_view.get_for_game(game_id) \
            .rename(index=str, columns={"pred1": "idle", "pred2": "left", "pred3": "left+jump", "pred4": "right", "pred5": "right+jump", "pred6": "jump"}) \
            .plot(x='state_id', y=['idle', 'left', 'left+jump', 'right', 'right+jump', 'jump'], ax=ax)
        ax.set_xlabel('state_id')
        ax.set_ylabel('Q values')

    def plot_game_reward_rolling_sum(self, game_id, ax):
        self._data_view.get_for_game(game_id)\
            ['score'] \
            .diff() \
            .apply(np.sign) \
            .rolling(window=20, center=True).sum() \
            .plot(x='state_id', ax=ax)
        ax.set_xlabel('state_id')
        ax.set_ylabel('rewards sum')

    def plot_render_time(self, ax):
        time_diffs = self._data_view.get().groupby('game_id')['timestamp'].diff()
        time_diffs.clip(0.0, time_diffs.std()) \
            .plot(ax=ax)
        ax.set_xlabel('memory')
        ax.set_ylabel('render time [s]')

    def plot_final_scores(self, ax):
        data = self._data_view.get()\
                .groupby('game_id')['score']\
                .last()
        data.plot(ax=ax)
        ax.set_xlabel('game')
        ax.set_ylabel('final score')

    def plot_action_value_predictions(self, ax):
        self._data_view.get()\
            [['pred1', 'pred2', 'pred3', 'pred4', 'pred5', 'pred6']] \
            .rename(index=str, columns={"pred1": "idle", "pred2": "left", "pred3": "left+jump", "pred4": "right", "pred5": "right+jump", "pred6": "jump"})\
            .plot(ax=ax)
        ax.set_xlabel('memory')
        ax.set_ylabel('Q value')

    def plot_reward_rolling_sum(self, ax):
        self._data_view.get()\
            ['score']\
            .diff()\
            .apply(np.sign)\
            .rolling(window=10000, center=True).sum()\
            .plot(ax=ax)
        ax.set_xlabel('memory')
        ax.set_ylabel('rewards sum')

