import tkinter as tk

class SessionWindow(tk.Frame):

    def __init__(self, numerical_stats, overall_stats_callback):
        super().__init__(padx=3)
        self.stat_vars = self.create_stat_vars(numerical_stats)
        self.overall_stats_callback = overall_stats_callback
        self.initUI()

    def create_stat_vars(self, numerical_stats):
        return {
            key: tk.DoubleVar(value=numerical_stats[key])
            for key in numerical_stats.keys()
        }

    def initUI(self):
        self.master.title("Player Simulator - session overview")

        self.init_sessions_overview()
        self.init_session_details()

        self.pack(fill=tk.BOTH, expand=True)


    def quit(self):
        self._root().destroy()

    def init_sessions_overview(self):
        overview_subframe = tk.Frame(self, relief=tk.RAISED, padx=3, pady=3)

        stats_frame = tk.Frame(overview_subframe, padx=3)

        for idx, key in enumerate(self.stat_vars.keys()):
            tk.Label(stats_frame, text=str(key)).grid(row=idx, column=0)
            tk.Label(stats_frame, textvariable=self.stat_vars[key]).grid(row=idx, column=1)

        stats_frame.pack(fill=tk.X)

        statistics_button = tk.Button(overview_subframe, text="Show charts", command=self.overall_stats_callback)
        statistics_button.pack(fill=tk.X)

        overview_subframe.pack(side=tk.LEFT)

    def init_session_details(self):
        detail_subframe = tk.Frame(self, relief=tk.RAISED, padx=3, pady=3)

        detail_subframe.pack(side=tk.LEFT)