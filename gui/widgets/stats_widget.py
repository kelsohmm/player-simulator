import tkinter as tk


class StatsWidget(tk.Frame):
    def __init__(self, master, stats):
        tk.Frame.__init__(self, master, padx=3)
        self.stat_vars = self._create_stat_vars(stats)

        for idx, key in enumerate(self.stat_vars.keys()):
            tk.Label(self, text=str(key)).grid(row=idx, column=0)
            tk.Label(self, textvariable=self.stat_vars[key]).grid(row=idx, column=1)

    def update_stats(self, new_stats):
        for var_name in self.stat_vars.keys():
            if var_name in new_stats:
                self.stat_vars[var_name].set(new_stats[var_name])

    def _create_stat_vars(self, stats):
        return {
            key: tk.StringVar(value=stats[key])
            for key in stats.keys()
        }