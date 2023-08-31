import cv2, pymysql

class Draw:
    def __init__(self, frame, width, hegiht):
        self.frame = frame
        self.width = width
        self.height = hegiht
        self.red = (0, 0, 255)
        self.green = (0, 255, 0)

    def center_rect(self, value, sw):
        x1, x2 = self.width // 2 - value, self.width // 2 + value
        y1, y2 = self.height // 2 - value, self.height // 2 + value

        if sw == 1:
            cv2.rectangle(self.frame, (x1, y1), (x2, y2), self.green, 2)
        else:
            cv2.rectangle(self.frame, (x1, y1), (x2, y2), self.red, 2)

    def body_circle(self, x, y):
        cv2.circle(self.frame, (x, y), 3, self.red, -1)


class Angle:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y

        self.host = '127.0.0.1'
        self.user = 'root'
        self.password = '1234'
        self.database = 'test'
        self.connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)

    def turtle_neck(self, xy_list):  # 각 ABC 일때
        flag = None
        try:
            pt1_x, pt1_y = xy_list[1][0], xy_list[1][1]  # pt1 가로 979, 320
            pt2_x, pt2_y = xy_list[0][0], xy_list[0][1]  # pt2 세로

            if pt1_x and pt1_y and pt2_x and pt2_y:
                cv2.line(self.image, (pt1_x, pt1_y), (pt1_x, pt2_y), (0, 0, 255), 2)
                cv2.line(self.image, (pt2_x, pt2_y), (pt1_x, pt2_y), (0,0,255), 2)
                cv2.putText(self.image, f"{(pt1_x, pt1_y)}", (pt1_x, pt1_y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                cv2.putText(self.image, f"{(pt2_x, pt2_y)}", (pt2_x, pt2_y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                pt1 = int(abs(pt1_x - pt2_x) * 1.7777778) # 가로
                pt2 = int(abs(pt1_y - pt2_y)) # 세로
                result = round((pt2 / pt1), 7)

                return result

        except IndexError:
            print("목 또는 귀가 탐지되지 않았습니다.")

            from main import AI 
            AI().neck_angle_value()

    def position_rect(self, x_min, y_min, x_max, y_max, number7_x, number7_y, label_text):
        cv2.rectangle(self.image, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)
        cv2.circle(self.image, (number7_x, number7_y), 3, (255, 0, 0), 2)
        cv2.putText(self.image, label_text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    def body_center_circle(self, x, y):
        cv2.circle(self.image, (x, y), 3, (255, 0, 0), 2)

    def label_text(self, label_text, x_min, y_min):
        cv2.putText(self.image, label_text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    def return_xy(self):
        return self.x, self.y
