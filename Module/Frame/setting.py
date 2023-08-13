import cv2


def frame_setting(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame


def get_shape(width, height):
    width = width
    height = height

    return width, height
