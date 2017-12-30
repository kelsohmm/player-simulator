import cv2
import numpy as np

from config import FRAME_SIZE, FRAMES_STACKED, CONV_SHAPE

class State:
    def __init__(self):
        self.state_matrix = np.zeros(CONV_SHAPE, dtype=np.ubyte)
        self.curr_index = 0

    def append(self, frame):
        frame = cv2.resize(frame, FRAME_SIZE)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY).reshape((FRAME_SIZE))
        self.state_matrix[:, :, self.curr_index] = frame
        self.curr_index += 1

    def as_matrix(self):
        frames_missing = FRAMES_STACKED - self.curr_index
        if frames_missing > 0:
            self.repeat_last_frame(frames_missing)

        return self.state_matrix

    def repeat_last_frame(self, frames_missing):
        for i in range(frames_missing):
            self.state_matrix[:, :, self.curr_index + i] = self.state_matrix[:, :, self.curr_index-1]

