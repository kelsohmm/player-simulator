import sqlite3

from gui.session_control.replay_media_player import ReplayMediaPlayer
from gui.session_control.session_window import SessionWindow

from gui.session_control.charts_window import ChartsWindow
from gui.utils import show_error
from session import Session
from simulator.simulation_job_factory import simulation_job_factory
from statistics.game_frames_view import GameFramesView
from statistics.plot_builder import PlotBuilder
from statistics.statistics_view import StatisticsView


class SessionController:
    def __init__(self, session_path):
        self.session = Session(session_path)
        self.db_conn = sqlite3.connect(self.session.db_path)
        self.frames_view = GameFramesView(self.db_conn)
        self.data_view = StatisticsView(self.db_conn)
        self.charts_builder = PlotBuilder(self.data_view)
        self.game_id = None
        self.simulation_job = None
        initial_game_stats = self._game_stats_dict('Not selected', 'None', 'None')
        self.window = SessionWindow(self._create_overall_stats(), initial_game_stats,
                                    self._start_simulation_job,
                                    self._open_overall_charts_window, self._game_id_selected, self._open_game_charts_window, self._open_replay_window)

    def finish(self):
        self.window.destroy()
        self.window = None

    def _start_simulation_job(self):
        return simulation_job_factory(self.session.db_path, self.session.model_path)

    def _open_replay_window(self):
        if self.game_id is not None:
            ReplayMediaPlayer(self.frames_view.get_for_game_id(self.game_id))
        else:
            show_error('Game not selected.')

    def _open_game_charts_window(self):
        if self.game_id is not None:
            ChartsWindow('charts', {
                'Game score': lambda ax: self.charts_builder.plot_game_score(self.game_id, ax),
            })
        else:
            show_error('Game not selected.')

    def _open_overall_charts_window(self):
        ChartsWindow('charts', {
            'Action value predictions': self.charts_builder.plot_action_value_predictions,
            'Final scores': self.charts_builder.plot_final_scores,
            'Render time': self.charts_builder.plot_render_time,
            'Reward rolling sum': self.charts_builder.plot_reward_rolling_sum,
        })

    def _game_id_selected(self, game_id):
        if len(game_id) > 0 and int(game_id) in self.data_view.get()['game_id'].unique():
            self.game_id = int(game_id)
            self.window.set_game_details(self._create_game_stats(self.game_id))
        else:
            show_error('Game id not found.')


    def _create_game_stats(self, game_id):
        data = self.data_view.get_for_game(game_id)
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
