import tkinter as tk

from gui.session_create.layers_builder_widget import LayersBuilderWidget
from gui.widgets.config_widget import ConfigWidget


class SessionCreateWindow(tk.Toplevel):

    def __init__(self, initial_conv_config, initial_dense_config, initial_session_config, create_session_callback):
        super().__init__(padx=3, pady=5)
        self.title('Create new session')
        self.create_session_callback = create_session_callback

        self.layer_builder = LayersBuilderWidget(self, initial_conv_config, initial_dense_config)
        self.layer_builder.pack(side=tk.LEFT, anchor=tk.N)

        config_frame = tk.Frame(self, padx=5)

        tk.Label(config_frame, text='Configure session', font=25, pady=5)\
            .pack(fill=tk.X)

        self.config = ConfigWidget(config_frame, initial_session_config, is_horizontal=False)
        self.config.pack()

        tk.Button(config_frame, text='Create session', padx=5, pady=3, command=self._notify_session_create) \
            .pack(anchor=tk.SE)

        config_frame.pack(side=tk.LEFT, anchor=tk.N)

    def _notify_session_create(self):
        session_config = self.config.get_config()
        layers_config = self.layer_builder.get_layers_config()
        self.create_session_callback(layers_config, session_config)
