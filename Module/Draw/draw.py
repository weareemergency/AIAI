import cv2

class Draw:
    def __init__(self):
        self.red = (0, 0, 255)
        self.green = (0, 255, 0)

    def center_rect(self, frame, width, height, value, sw):
        x1, x2 = width // 2 - value, width // 2 + value
        y1, y2 = height // 2 - value, height // 2 + value

        if sw == 1:
            cv2.rectangle(frame, (x1, y1), (x2, y2), self.green, 2)
        else:
            cv2.rectangle(frame, (x1, y1), (x2, y2), self.red, 2)

    def face(self, frame, x, y):
        cv2.circle(frame, (x, y), 3, self.red, 3)


class Check:
    def __init__(self):
        pass