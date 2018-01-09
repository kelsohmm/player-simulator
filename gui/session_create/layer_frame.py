import tkinter as tk

from gui.widgets.config_widget import ConfigWidget


class LayerFrame(tk.Frame):
    def __init__(self, master, remove_callback, initial_config, color, name):
        tk.Frame.__init__(self, master, pady=3, padx=3)

        self.remove_callback = remove_callback

        tk.Button(self, text='X', command=self._call_remove_callback)\
            .pack(side=tk.LEFT)
        tk.Label(self, text=name, width=10, height=3, bg=color)\
            .pack(side=tk.LEFT)

        self.config = ConfigWidget(self, initial_config, is_horizontal=True)
        self.config.pack()

    def _call_remove_callback(self):
        self.remove_callback(self)
