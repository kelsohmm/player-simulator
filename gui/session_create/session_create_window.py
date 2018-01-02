import tkinter as tk

from gui.session_create.layers_builder_widget import LayersBuilderWidget
from gui.widgets.config_widget import ConfigWidget


class SessionCreateWindow(tk.Toplevel):

    def __init__(self, initial_conv_config, initial_dense_config, initial_session_config):
        super().__init__(padx=3, pady=5)
        self.title('Create new session')

        self.layer_builder = LayersBuilderWidget(self, initial_conv_config, initial_dense_config)
        self.layer_builder.pack(side=tk.LEFT, anchor=tk.N)

        config_frame = tk.Frame(self, padx=5)

        tk.Label(config_frame, text='Configure session', font=25, pady=5)\
            .pack(fill=tk.X)

        self.config = ConfigWidget(config_frame, initial_session_config, is_horizontal=False)
        self.config.pack()

        config_frame.pack(side=tk.LEFT, anchor=tk.N)
