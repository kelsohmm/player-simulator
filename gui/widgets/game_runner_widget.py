import tkinter as tk
from datetime import datetime

from gui.widgets.config_widget import ConfigWidget
from gui.widgets.stats_widget import StatsWidget


class GameRunnerWidget(tk.Frame):
    SIMULATION_CHECK_CLOCK_MS = 1000
    ACTIVE_STYLE = {'text': 'SIMULATION RUNNING', 'bg': '#DCEDC8', 'fg': '#4CAF50'}
    INACTIVE_STYLE = {'text': 'STOPPED', 'bg': '#FFCDD2', 'fg': '#F44336'}
    INACTIVE_STATS = {'Start time': '---', 'Duration': '---'}

    def __init__(self, master, game_run_factory):
        super().__init__(master)
        self.game_run_factory = game_run_factory
        self.simulation_job = None

        self.games_left_var = tk.IntVar(value=1)
        self.button_text_var = tk.StringVar(value='Run')

        config_defaults = {
            'Discount factor': 0.99,
            'Batch size': 30,
            'Exploration factor': 0.05,
        }
        self.config = ConfigWidget(self, config_defaults)\
            .pack(fill=tk.X)

        entry_frame = tk.Frame(self)

        tk.Label(entry_frame, text='Games left:') \
            .pack(side=tk.LEFT)

        self.games_left_entry = tk.Entry(entry_frame, textvariable=self.games_left_var, width=3)
        self.games_left_entry.pack(side=tk.LEFT)

        tk.Button(entry_frame, textvariable=self.button_text_var, command=self._button_callback) \
            .pack(side=tk.LEFT)

        entry_frame.pack(fill=tk.X)

        self.active_label = tk.Label(self, **self.INACTIVE_STYLE)
        self.active_label.pack(fill=tk.X)

        self.stats = StatsWidget(self, self.INACTIVE_STATS)
        self.stats.pack(fill=tk.X)

    def _button_callback(self):
        games_left = self.games_left_var.get()
        self.games_left_var.set(games_left)
        if self.simulation_job is None:
            if games_left > 0:
                self._disable_ui()
                self._start_new_simulation_job()
        else:
            self._enable_ui()
            self._stop_simulation_job()


    def _start_new_simulation_job(self):
        if self.simulation_job is not None:
            self.simulation_job.stop()

        self.simulation_job = self.game_run_factory()
        self.simulation_job.run()
        self.after(self.SIMULATION_CHECK_CLOCK_MS, self._watch_simulation_job)

    def _watch_simulation_job(self):
        if self.simulation_job is not None:
            if not self.simulation_job.is_running():
                games_left = self.games_left_var.get()
                if games_left > 0:
                    self.games_left_var.set(games_left - 1)
                    self._start_new_simulation_job()
                else:
                    self.simulation_job = None
                    self._enable_ui()
            else:
                self._update_simulation_stats()
                self.after(self.SIMULATION_CHECK_CLOCK_MS, self._watch_simulation_job)

    def _enable_ui(self):
        self.active_label.config(**self.INACTIVE_STYLE)
        self.games_left_entry.config(state=tk.NORMAL)
        self.button_text_var.set('Run')

    def _disable_ui(self):
        self.active_label.config(**self.ACTIVE_STYLE)
        self.games_left_entry.config(state=tk.DISABLED)
        self.button_text_var.set('Stop')

    def _stop_simulation_job(self):
        self.stats.update_stats(self.INACTIVE_STATS)
        self.simulation_job.stop()
        self.simulation_job = None

    def _update_simulation_stats(self):
        if self.simulation_job is not None and self.simulation_job.start_time() is not None:
            self.stats.update_stats({
                'Start time': '{:%Y-%m-%d %H:%M:%S}'.format(self.simulation_job.start_time()),
                'Duration':  str(datetime.now() - self.simulation_job.start_time()).split(".")[0]
            })
