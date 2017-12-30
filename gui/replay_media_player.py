import os
import tkinter as tk
from gui.game_replay import GameReplay

PLAY_ICON = os.path.join('gui', 'resources', 'play.png')
PAUSE_ICON = os.path.join('gui', 'resources', 'pause.png')
STOP_ICON = os.path.join('gui', 'resources', 'stop.png')

class ReplayMediaPlayer(tk.Toplevel):
    REFRESH_TIME_MS = 20
    WIDTH = 256
    HEIGHT = 256

    def __init__(self, game_frames):
        super().__init__()
        self.resizable(width=False, height=False)
        self.replay = GameReplay(game_frames, self.WIDTH, self.HEIGHT)
        self.replay.play()

        self._initUI()
        self.update_view()

    def update_view(self):
        self.image_label.configure(image=self.replay.get_frame())
        self.after(self.REFRESH_TIME_MS, self.update_view)

    def _initUI(self):
        self.image_label = tk.Label(self, image=self.replay.get_frame())
        self.image_label.pack(fill=tk.BOTH)

        self.play_photo = tk.PhotoImage(file=PLAY_ICON).subsample(2)
        tk.Button(self, image=self.play_photo, command=self.replay.play).pack(side=tk.LEFT)

        self.pause_photo = tk.PhotoImage(file=PAUSE_ICON).subsample(2)
        tk.Button(self, image=self.pause_photo, command=self.replay.pause).pack(side=tk.LEFT)

        self.stop_photo = tk.PhotoImage(file=STOP_ICON).subsample(2)
        tk.Button(self, image=self.stop_photo, command=self.replay.stop).pack(side=tk.LEFT)

        tk.Button(self, text='-5s', width=4, height=1, command=self._replay_backward_5s).pack(side=tk.LEFT)
        tk.Button(self, text='+5s', width=4, height=1, command=self._replay_forward_5s).pack(side=tk.LEFT)

    def _replay_forward_5s(self):
        self.replay.seek(5)

    def _replay_backward_5s(self):
        self.replay.seek(-5)
