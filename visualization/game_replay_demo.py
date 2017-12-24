import cv2

from visualization.game_frames_view import GameFramesView
from visualization.game_replay import GameReplay

game_id = 14
view = GameFramesView()
replay = GameReplay(view.get_for_game_id(game_id))
replay.set_speed(5.0)
while True:
    cv2.imshow('Replay', replay.get_frame())
    cv2.waitKey(20)