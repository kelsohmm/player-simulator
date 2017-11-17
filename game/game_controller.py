import logging
from PIL import Image
from scipy import misc
import cv2


# source http://www.guguncube.com/1656/python-image-similarity-comparison-using-several-techniques
def _image_similarity_vectors_via_numpy(image1, image2):
    from numpy import average, linalg, dot

    vectors = []
    norms = []
    for image in [image1, image2]:
        vector = []
        for pixel_tuple in image:
            vector.append(average(pixel_tuple))
        vectors.append(vector)
        norms.append(linalg.norm(vector, 2))
    a, b = vectors
    a_norm, b_norm = norms
    # ValueError: matrices are not aligned !
    res = dot(a / a_norm, b / b_norm)
    return res


class GameController:
    END_GAME_PIC_PATH = "mario_end.jpg"
    THUMBNAIL_SIZE = (128, 128)
    SIMILIARITY_TRESHOLD = 0.9
    MAX_SCORE_JUMP = 2000

    def __init__(self, vm_host, controller_config):
        score_rect, key_activity_array = controller_config
        self.host = vm_host
        self.score_rect = score_rect
        self.key_activity_mapping = key_activity_array
        self.active_keys = set()
        self.end_game_pic = self._thumbnail(misc.imread(self.END_GAME_PIC_PATH))
        self.last_score = 0

    def get_game_state(self):
        screen_shot = self.host.take_screen_shot()
        score = 0

        if self._is_end_game_screen(screen_shot):
            return "FINISHED", score, screen_shot
        else:
            return "IN_PROGRESS", score, screen_shot

    def set_active_keys(self, key_activity_array):
        active_keys = self._map_key_activity_array_to_keys(key_activity_array)
        new_active_keys = set(active_keys)

        new_pressed_keys = new_active_keys.difference(self.active_keys)
        self.host.keys_down(new_pressed_keys)

        new_released_keys = self.active_keys.difference(new_active_keys)
        self.host.keys_up(new_released_keys)

        self.active_keys = new_active_keys

    def _thumbnail(self, pic):
        return misc.imresize(pic, self.THUMBNAIL_SIZE)

    def _is_end_game_screen(self, screen_shot):
        sim = _image_similarity_vectors_via_numpy(
            self.end_game_pic,
            self._thumbnail(screen_shot))
        return sim > self.SIMILIARITY_TRESHOLD

    def _map_key_activity_array_to_keys(self, key_activity_array):
        assert len(key_activity_array) == len(self.key_activity_mapping), "NOT EQUAL!!!"
        active_keys = []
        for i in range(len(key_activity_array)):
            if key_activity_array[i] == 1 or key_activity_array[i] == True:
                active_keys.append(self.key_activity_mapping[i])
        return active_keys
