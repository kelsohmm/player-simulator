import tkinter as tk

from gui.session_create.layers_builder_widget import LayersBuilderWidget


class SessionCreateWindow(tk.Toplevel):

    def __init__(self, initial_conv_config, initial_dense_config):
        super().__init__(padx=3, pady=5)
        self.title('Create new session')

        self.layer_builder = LayersBuilderWidget(self, initial_conv_config, initial_dense_config)
        self.layer_builder.pack(side=tk.LEFT)