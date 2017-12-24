from time import time
import cv2


class GameReplay:
    SECONDS_PER_FRAME = 1/30

    def __init__(self, game_frames):
        self.frames = [cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
                       for frame in game_frames]
        self.speed = 1.0
        self.stop()

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
            self.play()

        new_time = time()
        time_diff = new_time - self.last_time

        frames_to_move = int(time_diff / self.SECONDS_PER_FRAME * self.speed)
        if frames_to_move > 0:
            self.curr_frame += frames_to_move

            if self.curr_frame >= len(self.frames):
                self.curr_frame = 0
            self.last_time = new_time

        return self.frames[self.curr_frame]
