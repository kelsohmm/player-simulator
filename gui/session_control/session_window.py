import tkinter as tk

from gui.widgets.game_runner_widget import GameRunnerWidget
from gui.widgets.stats_widget import StatsWidget


class SessionWindow(tk.Toplevel):
    def __init__(self, overall_stats, game_stats,
                 simulation_factory,
                 overall_stats_callback, select_game_callback,
                 game_stats_callback, replay_callback):
        super().__init__(padx=3)
        self.overall_stats_callback = overall_stats_callback
        self.select_game_callback = select_game_callback
        self.game_stats_callback = game_stats_callback
        self.replay_callback = replay_callback
        self.initUI(simulation_factory, overall_stats, game_stats)

    def initUI(self, simulation_factory, overall_stats, game_stats):
        self.title("Player Simulator - session overview")

        self.init_simulation_runner(simulation_factory)
        self.init_sessions_overview(overall_stats)
        self.init_session_details(game_stats)

    def set_game_details(self, game_stats):
        self.game_stats_widget.update_stats(game_stats)

    def init_simulation_runner(self, simulation_factory):
        runner_subframe = tk.Frame(self, relief=tk.RAISED, padx=5, pady=3)

        tk.Label(runner_subframe, text='Simulator controller', font=25, pady=5) \
            .pack(fill=tk.X)

        GameRunnerWidget(runner_subframe, simulation_factory)\
            .pack(fill=tk.BOTH)

        runner_subframe.pack(side=tk.LEFT)


    def init_sessions_overview(self, stats):
        overview_subframe = tk.Frame(self, relief=tk.RAISED, padx=5, pady=3)

        tk.Label(overview_subframe, text='Session overview', font=25, pady=5)\
            .pack(fill=tk.X)

        StatsWidget(overview_subframe, stats)\
            .pack(fill=tk.X)

        tk.Button(overview_subframe, text="Show overall charts", command=self.overall_stats_callback)\
            .pack(fill=tk.X)

        overview_subframe.pack(side=tk.LEFT)

    def init_session_details(self, stats):
        detail_subframe = tk.Frame(self, relief=tk.RAISED, padx=5, pady=3)

        tk.Label(detail_subframe, text='Games history', font=25, pady=5)\
            .pack(fill=tk.X)

        select_subframe = tk.Frame(detail_subframe)
        game_id_entry = tk.Entry(select_subframe, text="0", width=10)
        game_id_entry.pack(side=tk.LEFT)

        statistics_button = tk.Button(select_subframe, text="Show game",
                                      command=lambda: self.select_game_callback(game_id_entry.get()))
        statistics_button.pack(side=tk.LEFT)
        select_subframe.pack(fill=tk.X)

        self.game_stats_widget = StatsWidget(detail_subframe, stats)
        self.game_stats_widget.pack(fill=tk.X)

        tk.Button(detail_subframe, text="Show game charts", command=self.game_stats_callback)\
            .pack(fill=tk.X)

        tk.Button(detail_subframe, text="Show game replay", command=self.replay_callback)\
            .pack(fill=tk.X)

        detail_subframe.pack(side=tk.LEFT)