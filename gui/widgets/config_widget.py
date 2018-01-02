import tkinter as tk


class ConfigWidget(tk.Frame):
    def __init__(self, master, stats, is_horizontal=False):
        super().__init__(master, padx=3)
        self.stat_vars = self._create_stat_vars(stats)

        for idx, key in enumerate(self.stat_vars.keys()):
            label_row, label_col, entry_row, entry_col = self._get_grid(is_horizontal, idx)
            tk.Label(self, text=str(key)).grid(row=label_row, column=label_col)
            tk.Entry(self, textvariable=self.stat_vars[key], width=6).grid(row=entry_row, column=entry_col)

    def get_config(self):
        return {
            stat_name: self.stat_vars[stat_name].get()
            for stat_name in self.stat_vars.keys()
        }

    def update_stats(self, new_stats):
        for var_name in self.stat_vars.keys():
            if var_name in new_stats:
                self.stat_vars[var_name].set(new_stats[var_name])

    def _create_stat_vars(self, stats):
        return {
            key: tk.StringVar(value=stats[key])
            for key in stats.keys()
        }

    def _get_grid(self, is_horizontal, idx):
        if is_horizontal:
            return 0, idx, 1, idx
        else:
            return idx, 0, idx, 1