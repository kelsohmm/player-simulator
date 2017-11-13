import numpy as np
import cv2
from config import DATA_SAVE_PATH

print("--- LOADING DATA ---")
loaded = np.load(DATA_SAVE_PATH)
inputs_frame = loaded['inputs_frame']
labels = loaded['labels']

print("--- SHOWING DATA ---")
current_idx = 0
while True:
    cv2.imshow("data.npz preview", inputs_frame[current_idx])
    print("Showing idx: %d, rewards: " % (current_idx,),  labels[current_idx].tolist())
    k = cv2.waitKey(0)
    if k == ord('.'):
        current_idx += 1
    elif k == ord(','):
        current_idx += -1
    elif k == ord('\''):
        current_idx += 10
    elif k == ord(';'):
        current_idx += -10
    elif k == ord('q'):
        break
    else:
        continue


cv2.destroyAllWindows()

