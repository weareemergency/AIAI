import cv2

class UserGuide():
    def __init__(self, frame):
        self.frame = frame
        self.x = 650
        self.y = 1
        self.overlay_width = 650
        self.overlay_height = 130
        self.step1_img = cv2.imread('static/image/step1.png')
        self.step2_img = cv2.imread('static/image/step2.png')
        self.step3_img = cv2.imread('static/image/step3.png')

    def position(self):
        x = self.x
        y = self.y
        overlay_width = self.overlay_width
        overlay_height = self.overlay_height

        return x, y, overlay_width, overlay_height

    def step1(self):
        step1 = cv2.resize(self.step1_img, (self.overlay_width, self.overlay_height))

        return step1

    def step2(self):
        step2 = cv2.resize(self.step2_img, (self.overlay_width, self.overlay_height))

        return step2

    def step3(self):
        step3 = cv2.resize(self.step3_img, (self.overlay_width, self.overlay_height))

        return step3

