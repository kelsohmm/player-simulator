import sqlite3
import numpy as np
from gui.charts_window import ChartsWindow
from gui.session_window import SessionWindow
from session import Session
from statistics.plot_builder import PlotBuilder
from statistics.statistics_view import StatisticsView


class SessionController:
    def __init__(self, session_path):
        self.session = Session(session_path)
        self.db_conn = sqlite3.connect(self.session.db_path)
        self.data_view = StatisticsView(self.db_conn)
        self.charts_builder = PlotBuilder(self.data_view)
        self.window = SessionWindow(self._create_overall_stats(), self._open_charts_window)

    def _open_charts_window(self):
        self.charts_window = ChartsWindow('charts', {
            'move usage distribution per distance': self.charts_builder.get_move_usage_distribution_per_distance(),
            'final scores': self.charts_builder.get_final_scores_plot()
        })

    def _create_overall_stats(self):
        stats = {
            'Games played': self.data_view.get()['game_id'].max(),
            'States count': self.data_view.get()['state_id'].count(),
            'Longest game (in states)': self.data_view.get()['state_id'].max(),
            'Best score': self.data_view.get()['score'].max(),
        }
        return stats
