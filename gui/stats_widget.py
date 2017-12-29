import tkinter as tk


class StatsWidget(tk.Frame):
    def __init__(self, master, stats):
        super().__init__(master, padx=3)
        self.stat_vars = self._create_stat_vars(stats)

        for idx, key in enumerate(self.stat_vars.keys()):
            tk.Label(self, text=str(key)).grid(row=idx, column=0)
            tk.Label(self, textvariable=self.stat_vars[key]).grid(row=idx, column=1)


    def _create_stat_vars(self, stats):
        return {
            key: tk.DoubleVar(value=stats[key])
            for key in stats.keys()
        }