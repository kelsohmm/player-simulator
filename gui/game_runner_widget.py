import tkinter as tk


class GameRunnerWidget(tk.Frame):
    def __init__(self, master, game_run_factory):
        super().__init__(master)
        self.game_run_factory = game_run_factory

        tk.Label(self, text='Games left:')\
            .pack(side=tk.LEFT)

        self.games_left_var = tk.IntVar(value=1)
        self.button_text_var = tk.StringVar(value='Run')

        tk.Entry(self, textvariable=self.games_left_var, width=3)\
            .pack(side=tk.LEFT)

        tk.Button(self, textvariable=self.button_text_var, command=self._button_callback)\
            .pack(side=tk.LEFT)

    def _button_callback(self):
        print(self.games_left_var.get())
        self.games_left_var.set(self.games_left_var.get())
