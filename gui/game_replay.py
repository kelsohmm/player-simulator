from time import time
import cv2
from PIL import Image, ImageTk


class GameReplay:
    SECONDS_PER_FRAME = 1/30

    def __init__(self, game_frames, width, height):
        self.frames = [ImageTk.PhotoImage(
                        Image.fromarray(
                         cv2.resize(cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB), (width, height))))
                       for frame in game_frames]
        self.speed = 1.0
        self.stop()

    def seek(self, time_diff):
        frames_to_move = int(time_diff / self.SECONDS_PER_FRAME * self.speed)

        self.curr_frame += frames_to_move

        if self.curr_frame >= len(self.frames):
            self.curr_frame = len(self.frames) - 1
        elif self.curr_frame < 0:
            self.curr_frame = 0

        self.last_time = time()

    def stop(self):
        self.curr_frame = 0
        self.last_time = None

    def pause(self):
        self.last_time = None

    def play(self):
        self.last_time = time()

    def set_speed(self, speed):
        self.speed = speed

    def get_frame(self):
        if self.last_time is None:
            return self.frames[self.curr_frame]

        new_time = time()
        time_diff = new_time - self.last_time

        if time_diff > self.SECONDS_PER_FRAME:
            self.seek(time_diff)

        return self.frames[self.curr_frame]
