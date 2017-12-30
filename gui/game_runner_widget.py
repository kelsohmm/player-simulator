import tkinter as tk


class GameRunnerWidget(tk.Frame):
    SIMULATION_CHECK_CLOCK_MS = 1000
    def __init__(self, master, game_run_factory):
        super().__init__(master)
        self.game_run_factory = game_run_factory
        self.simulation_job = None

        tk.Label(self, text='Games left:')\
            .pack(side=tk.LEFT)

        self.games_left_var = tk.IntVar(value=1)
        self.button_text_var = tk.StringVar(value='Run')

        self.games_left_entry = tk.Entry(self, textvariable=self.games_left_var, width=3)
        self.games_left_entry.pack(side=tk.LEFT)

        tk.Button(self, textvariable=self.button_text_var, command=self._button_callback)\
            .pack(side=tk.LEFT)

    def _button_callback(self):
        games_left = self.games_left_var.get()
        self.games_left_var.set(games_left)
        if self.simulation_job is None:
            if games_left > 0:
                self._disable_entry()
                self._start_new_simulation_job()


    def _start_new_simulation_job(self):
        if self.simulation_job is not None:
            self.simulation_job.stop()

        self.simulation_job = self.game_run_factory()
        self.simulation_job.run()
        self.after(self.SIMULATION_CHECK_CLOCK_MS, self._watch_simulation_job)

    def _watch_simulation_job(self):
        if not self.simulation_job.is_running():
            games_left = self.games_left_var.get()
            if games_left > 0:
                self.games_left_var.set(games_left - 1)
                self._start_new_simulation_job()
            else:
                self._enable_entry()
        else:
            self.after(self.SIMULATION_CHECK_CLOCK_MS, self._watch_simulation_job)

    def _enable_entry(self):
        self.games_left_entry.config(state=tk.NORMAL)
        self.button_text_var.set('Run')

    def _disable_entry(self):
        self.games_left_entry.config(state=tk.DISABLED)
        self.button_text_var.set('Stop')
