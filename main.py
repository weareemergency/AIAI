import cv2
import mediapipe as mp
import threading
import os

from Module.Frame.setting import frame_setting, get_shape
from Module.Frame.guide import UserGuide
from Module.Draw.draw import Draw
from Module.Draw.XY import Vertex, Body
from Module.detect.imagedetect import detect

result_value = []

class AI:
    def __init__(self):
        self.result = None

    def create_folder(self, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"폴더를 만들었습니다.: {folder_path}")
        else:
            print(f"폴더 존재 : {folder_path}")

    def neck_angle_value(self):
        global result_value
        result = self.main()

        try:
            if result is not None:  # 반환값이 None이 아닐 때만 더함
                result_value.extend(result) 
            else:
                pass
        except TypeError:
            pass

        print(f"neck_angle_value : {self.result}")

    def main(self):
        cap = cv2.VideoCapture(0)

        width, height = get_shape(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        vers = Vertex(width, height)
        print("width, height", width, height)
        x1, x2, y1, y2 = vers.rect_vertex()

        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose()

        self.create_folder('Result/')

        first_rect = 400
        second_rect = 350
        count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            origin_frame = frame.copy()

            frame_rgb = frame_setting(frame)
            results = pose.process(frame_rgb)

            if results.pose_landmarks:
                right_ear_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EAR]
                left_ear_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EAR]
                nose = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]
                right_shoulder_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                left_shoulder_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]

                h, w, _ = frame.shape

                right_ear = Body(int(right_ear_landmark.x * w), int(right_ear_landmark.y * h))
                left_ear = Body(int(left_ear_landmark.x * w), int(left_ear_landmark.y * h))
                nose = Body(int(nose.x * w), int(nose.y * h))
                right_shoulder = Body(int(right_shoulder_landmark.x * w), int(right_shoulder_landmark.y * h))
                left_shoulder = Body(int(left_shoulder_landmark.x * w), int(left_shoulder_landmark.y * h))

                r_ear_x, r_ear_y = right_ear.body_xy()
                l_ear_x, l_ear_y = left_ear.body_xy()
                nose_x, nose_y = nose.body_xy()
                right_shoulder_x, right_shoulder_y = right_shoulder.body_xy()
                left_shoulder_x, left_shoulder_y = left_shoulder.body_xy()

                center = Draw(frame, width, height)

                ear_diff_x = l_ear_x - r_ear_x
                ear_diff_y = l_ear_y - r_ear_y

                ifin_1 = (x1 <= nose_x <= x2) and (y1 <= nose_y <= y2)
                ifin_2 = (x1 <= r_ear_x <= x2) and (y1 <= r_ear_y <= y2) and (x1 <= l_ear_x <= x2) and (y1 <= l_ear_y <= y2)
                ifin_3 = (x1 <= right_shoulder_x <= x2) and (y1 <= right_shoulder_y <= y2) and (x1 <= left_shoulder_x <= x2) and (y1 <= left_shoulder_y <= y2)

                if ifin_1 and ifin_2 and ifin_3:
                    if (abs(ear_diff_x) - abs(ear_diff_y)) < 40: # 40 부분은 때에 따라서 무조건 수정
                        center.center_rect(first_rect, 1)
                        center.center_rect(second_rect, 1)
                        count += 1
                        if count == 40:
                            cv2.imwrite('Result/UserPicture.jpeg', origin_frame)

                        if cv2.waitKey(1) == 27 or count == 60:
                            self.result = detect()
                            break
                    else:
                        center.center_rect(first_rect, 1)
                        center.center_rect(second_rect, 0)
                else:
                    center.center_rect(first_rect, 0)
                    center.center_rect(second_rect, 0)

            cv2.imshow('Main', frame)

            if cv2.waitKey(1) == 27:
                break
        
        cap.release()
        cv2.destroyAllWindows()

def db(result_value):
    import pymysql

    host = '127.0.0.1'
    user = 'root'
    password = '1234'
    database = 'test'
    connection = pymysql.connect(host=host, user=user, password=password, database=database)

    cursor = connection.cursor()
    query = f"INSERT INTO angle (id, username, result_value) VALUES (6, '김아무개', {str(result_value)})"
    cursor.execute(query)

    connection.commit()  # 커밋을 해야 변경이 반영됨
    cursor.close()
    connection.close()

    print("DB 전송 완료")


if __name__ == "__main__":
    result_value = AI().neck_angle_value()

    print("result_value", result_value)

    

