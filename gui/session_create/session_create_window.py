import tkinter as tk

from gui.session_create.layer_frame import LayerFrame


class SessionCreateWindow(tk.Toplevel):

    def __init__(self, initial_conv_config, initial_dense_config):
        super().__init__(padx=3, pady=5)
        self.path_var = tk.StringVar()
        self.initial_conv_config = initial_conv_config
        self.initial_dense_config = initial_dense_config
        self.conv_frames = []
        self.dense_frames = []

        self.conv_container = tk.Frame(self, relief=tk.RAISED, padx=5, pady=3)
        self.conv_container.pack(fill=tk.X)
        tk.Button(self, text='Add convolution layer', command=self._add_new_conv)\
            .pack()

        self.dense_container = tk.Frame(self, relief=tk.RAISED, padx=5, pady=3)
        self.dense_container.pack(fill=tk.X)
        tk.Button(self, text='Add dense layer', command=self._add_new_dense) \
            .pack()

        self._add_new_conv()
        self._add_new_dense()

    def _add_new_conv(self):
        layer_frame = LayerFrame(self.conv_container, lambda: print("del"), {}, '#FFC107', 'conv')
        self.conv_frames.append(layer_frame)
        layer_frame.pack(fill=tk.X)

    def _add_new_dense(self):
        layer_frame = LayerFrame(self.dense_container, lambda: print("del"), {}, '#3F51B5', 'dense')
        self.dense_frames.append(layer_frame)
        layer_frame.pack(fill=tk.X)