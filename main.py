import cv2
import mediapipe as mp
import threading
import os

from Module.Frame.setting import frame_setting, get_shape
from Module.Frame.guide import UserGuide
from Module.Draw.draw import Draw
from Module.Draw.XY import Vertex, Body
from Image_detect import detect

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"폴더를 만들었습니다.: {folder_path}")
    else:
        print(f"폴더 존재 : {folder_path}")

def main():
    cap = cv2.VideoCapture(0)
    folder_path = 'Result/'
    create_folder(folder_path)

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    first_rect = 400
    second_rect = 350
    count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        guide = UserGuide(frame)
        x, y, overlay_width, overlay_height = guide.position()

        step1 = guide.step1()
        step2 = guide.step2()
        step3 = guide.step3()
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
                if (abs(ear_diff_x) - abs(ear_diff_y)) < 40:
                    frame[y:y + overlay_height, x:x + overlay_width] = step3
                    center.center_rect(first_rect, 1)
                    center.center_rect(second_rect, 1)
                    count += 1
                    if count == 40:
                        cv2.imwrite('Result/UserPicture.jpeg', origin_frame)

                    if cv2.waitKey(1) == 27 or count == 60:
                        detect()
                        break
                else:
                    frame[y:y + overlay_height, x:x + overlay_width] = step2
                    center.center_rect(first_rect, 1)
                    center.center_rect(second_rect, 0)
            else:
                frame[y:y + overlay_height, x:x + overlay_width] = step1
                center.center_rect(first_rect, 0)
                center.center_rect(second_rect, 0)

        cv2.imshow('Main', frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    # cap shape
    width, height = get_shape(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    # print(width, height) 1920 1080

    vers = Vertex(width, height)
    x1, x2, y1, y2 = vers.rect_vertex()
    # print(x1, x2, y1, y2) 560 1360 140 940

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    main_thread = threading.Thread(target=main())
    main_thread.start()