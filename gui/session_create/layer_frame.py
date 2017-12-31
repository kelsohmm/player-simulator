import tkinter as tk


class LayerFrame(tk.Frame):
    def __init__(self, master, remove_callback, initial_config, color, name):
        super(LayerFrame, self).__init__(master, pady=3, padx=3)

        self.remove_callback = remove_callback

        tk.Button(self, text='Remove', command=self._call_remove_callback, padx=3)\
            .pack(side=tk.LEFT)
        tk.Label(self, text=name, width=10, height=4, bg=color)\
            .pack(side=tk.LEFT)

    def _call_remove_callback(self):
        self.remove_callback(self)
