# 사각형 꼭짓점의 자표

class Vertex:
    def __init__(self):
        self.first_rect = 400
        self.second_rect = 386


    def rect_vertex(self, width, height):
        x1, x2 = width // 2 - 400, width // 2 + 400
        y1, y2 = height // 2 - 400, height // 2 + 400

        return x1, x2, y1, y2



