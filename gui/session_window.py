import tkinter as tk

from gui.stats_widget import StatsWidget


class SessionWindow(tk.Toplevel):
    def __init__(self, overall_stats, game_stats, overall_stats_callback, select_game_callback, game_stats_callback):
        super().__init__(padx=3)
        self.overall_stats_callback = overall_stats_callback
        self.select_game_callback = select_game_callback
        self.game_stats_callback = game_stats_callback
        self.initUI(overall_stats, game_stats)

    def initUI(self, overall_stats, game_stats):
        self.title("Player Simulator - session overview")

        self.init_sessions_overview(overall_stats)
        self.init_session_details(game_stats)

    def set_game_details(self, game_stats):
        self.game_stats_widget.update_stats(game_stats)

    def quit(self):
        self._root().destroy()

    def init_sessions_overview(self, stats):
        overview_subframe = tk.Frame(self, relief=tk.RAISED, padx=3, pady=3)

        stats_widget = StatsWidget(overview_subframe, stats)
        stats_widget.pack(fill=tk.X)

        statistics_button = tk.Button(overview_subframe, text="Show overall charts", command=self.overall_stats_callback)
        statistics_button.pack(fill=tk.X)

        overview_subframe.pack(side=tk.LEFT)

    def init_session_details(self, stats):
        detail_subframe = tk.Frame(self, relief=tk.RAISED, padx=3)

        select_subframe = tk.Frame(detail_subframe)
        game_id_entry = tk.Entry(select_subframe, text="0", width=10)
        game_id_entry.pack(side=tk.LEFT)

        statistics_button = tk.Button(select_subframe, text="Show game",
                                      command=lambda: self.select_game_callback(game_id_entry.get()))
        statistics_button.pack(side=tk.LEFT)
        select_subframe.pack(fill=tk.X)

        self.game_stats_widget = StatsWidget(detail_subframe, stats)
        self.game_stats_widget.pack(fill=tk.X)

        statistics_button = tk.Button(detail_subframe, text="Show game charts", command=self.game_stats_callback)
        statistics_button.pack(fill=tk.X)

        replay_button = tk.Button(detail_subframe, text="Show game replay", command=lambda: print("replay clicked!"))
        replay_button.pack(fill=tk.X)

        detail_subframe.pack(side=tk.LEFT)