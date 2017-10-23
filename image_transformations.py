import cv2

def transform_64_bw(image):
    bw = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return cv2.resize(bw, (64, 64))
