import tkinter as tk

from gui.session_create.layer_frame import LayerFrame


class LayersBuilderWidget(tk.Frame):

    def __init__(self, master, initial_conv_config, initial_dense_config):
        super().__init__(master, padx=3, pady=5)

        tk.Label(self, text='Configure neural network layers', font=25, pady=5) \
            .pack(fill=tk.X)

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

    def get_layers_config(self):
        return ([frame.config.get_config() for frame in self.conv_frames],
                [frame.config.get_config() for frame in self.dense_frames])

    def _add_new_conv(self):
        layer_frame = LayerFrame(self.conv_container, self._remove_conv, self.initial_conv_config, '#FFC107', 'conv')
        self.conv_frames.append(layer_frame)
        layer_frame.pack(fill=tk.X)

    def _add_new_dense(self):
        layer_frame = LayerFrame(self.dense_container, self._remove_dense, self.initial_dense_config, '#3F51B5', 'dense')
        self.dense_frames.append(layer_frame)
        layer_frame.pack(fill=tk.X)

    def _remove_conv(self, layer_frame):
        if layer_frame in self.conv_frames and len(self.conv_frames) > 1:
            self.conv_frames.remove(layer_frame)
            layer_frame.destroy()


    def _remove_dense(self, layer_frame):
        if layer_frame in self.dense_frames and len(self.dense_frames) > 1:
            self.dense_frames.remove(layer_frame)
            layer_frame.destroy()
