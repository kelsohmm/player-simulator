import tkinter as tk


class SessionCreateWindow(tk.Toplevel):

    def __init__(self, add_conv_callback, add_dense_callback):
        super().__init__(padx=3, pady=5)
        self.path_var = tk.StringVar()
        self.add_conv_callback = add_conv_callback
        self.add_dense_callback = add_dense_callback

