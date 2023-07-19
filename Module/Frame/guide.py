import cv2

class UserGuide():
    def __init__(self, frame, sw):
        self.frame = frame
        self.sw = sw
        self.step_1 = cv2.imread('static/image/First.png') # 귀와 어깨가 보이도록 서주세요

    def step_guide(self):
        if self.sw == 0:
            pass