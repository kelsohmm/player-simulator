import tkinter as tk

from gui.stats_widget import StatsWidget


class SessionWindow(tk.Toplevel):
    def __init__(self, numerical_stats, overall_stats_callback, select_game_callback):
        super().__init__(padx=3)
        self.overall_stats_callback = overall_stats_callback
        self.select_game_callback = select_game_callback
        self.initUI(numerical_stats)

    def initUI(self, stats):
        self.title("Player Simulator - session overview")

        self.init_sessions_overview(stats)
        self.init_session_details()


    def quit(self):
        self._root().destroy()

    def init_sessions_overview(self, stats):
        overview_subframe = tk.Frame(self, relief=tk.RAISED, padx=3, pady=3)

        stats_widget = StatsWidget(overview_subframe, stats)
        stats_widget.pack(fill=tk.X)

        statistics_button = tk.Button(overview_subframe, text="Show charts", command=self.overall_stats_callback)
        statistics_button.pack(fill=tk.X)

        overview_subframe.pack(side=tk.LEFT)

    def init_session_details(self):
        detail_subframe = tk.Frame(self, relief=tk.RAISED, padx=3, pady=3)

        game_id_entry = tk.Entry(detail_subframe, text="0", width=10)
        game_id_entry.pack(side=tk.LEFT)

        statistics_button = tk.Button(detail_subframe, text="Show game",
                                      command=lambda: self.select_game_callback(game_id_entry.get()))
        statistics_button.pack(side=tk.LEFT)

        detail_subframe.pack(side=tk.LEFT)