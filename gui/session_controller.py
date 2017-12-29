import sqlite3
from gui.charts_window import ChartsWindow
from gui.session_window import SessionWindow
from gui.utils import show_error
from session import Session
from statistics.plot_builder import PlotBuilder
from statistics.statistics_view import StatisticsView


class SessionController:
    def __init__(self, session_path):
        self.session = Session(session_path)
        self.db_conn = sqlite3.connect(self.session.db_path)
        self.data_view = StatisticsView(self.db_conn)
        self.charts_builder = PlotBuilder(self.data_view)
        self.game_id = None
        initial_game_stats = self._game_stats_dict('Not selected', 'None', 'None')
        self.window = SessionWindow(self._create_overall_stats(), initial_game_stats,
                                    self._open_overall_charts_window, self._game_id_selected, self._open_game_charts_window)

    def _open_game_charts_window(self):
        if self.game_id is not None:
            ChartsWindow('charts', {
                'move usage distribution per distance': lambda ax: self.charts_builder.plot_game_score(self.game_id, ax),
            })
        else:
            show_error('Game not selected.')

    def _open_overall_charts_window(self):
        ChartsWindow('charts', {
            'move usage distribution per distance': self.charts_builder.plot_move_usage_distribution_per_distance,
            'final scores': self.charts_builder.plot_final_scores
        })

    def _game_id_selected(self, game_id):
        if len(game_id) > 0 and int(game_id) in self.data_view.get()['game_id'].unique():
            self.game_id = int(game_id)
            self.window.set_game_details(self._create_game_stats(self.game_id))
        else:
            show_error('Game id not found.')


    def _create_game_stats(self, game_id):
        data = self.data_view.get()
        data = data.loc[data['game_id'] == game_id]
        return self._game_stats_dict(game_id, data['state_id'].max(), data['score'].max())

    def _game_stats_dict(self, game_id, game_length, final_score):
        return {'Game id': str(game_id),
                'Game length': str(game_length),
                'Final score': str(final_score)
        }

    def _create_overall_stats(self):
        data = self.data_view.get()
        stats = {
            'Games played': str(data['game_id'].max() + 1),
            'States count': str(data['state_id'].count()),
            'Longest game (in states)': str(data['state_id'].max()),
            'Best score': str(data['score'].max()),
        }
        return stats
