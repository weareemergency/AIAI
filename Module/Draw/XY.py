# 사각형 꼭짓점의 자표

class Vertex:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def rect_vertex(self):
        x1, x2 = self.width // 2 - 400, self.width // 2 + 400
        y1, y2 = self.height // 2 - 400, self.height // 2 + 400

        return x1, x2, y1, y2


class Body:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def body_xy(self):

        return self.x, self.y
