import tkinter as tk
from gui.game_replay import GameReplay


class ReplayMediaPlayer(tk.Toplevel):
    REFRESH_TIME_MS = 20
    WIDTH = 300
    HEIGHT = 300

    def __init__(self, game_frames):
        super().__init__()
        self.resizable(width=False, height=False)
        self.replay = GameReplay(game_frames, self.WIDTH, self.HEIGHT)
        self.replay.play()

        self._initUI()
        self.update_image_label()

    def update_image_label(self):
        self.image_label.configure(image=self.replay.get_frame())
        self.after(self.REFRESH_TIME_MS, self.update_image_label)

    def _initUI(self):
        self.image_label = tk.Label(self, image=self.replay.get_frame())
        self.image_label.pack(fill=tk.BOTH)