import cv2
import mediapipe as mp
import threading
import time

from Module.Frame.setting import frame_setting, get_shape
from Module.Draw.draw import Draw
from Module.Draw.XY import Vertex, Body


def main():
    cap = cv2.VideoCapture(0)

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    first_rect = 400
    second_rect = 350

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # --------
        step1_img = cv2.imread('static/image/step1.png')
        step2_img = cv2.imread('static/image/step2.png')
        step3_img = cv2.imread('static/image/step3.png')

        x = 650
        y = 1

        # 이미지 크기 조정
        overlay_width = 650
        overlay_height = 130
        step1 = cv2.resize(step1_img, (overlay_width, overlay_height))
        step2 = cv2.resize(step2_img, (overlay_width, overlay_height))
        step3 = cv2.resize(step3_img, (overlay_width, overlay_height))

        # ------------

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

            right_ear = Draw(frame, width, height)
            left_ear = Draw(frame, width, height)
            nose = Draw(frame, width, height)
            right_shoulder = Draw(frame, width, height)
            left_shoulder = Draw(frame, width, height)

            right_ear.body_circle(r_ear_x, r_ear_y)
            left_ear.body_circle(l_ear_x, l_ear_y)
            nose.body_circle(nose_x, nose_y)
            right_shoulder.body_circle(right_shoulder_x, right_shoulder_y)
            left_shoulder.body_circle(left_shoulder_x, left_shoulder_y)

            center = Draw(frame, width, height)

            ear_diff_x = l_ear_x - r_ear_x
            ear_diff_y = l_ear_y - r_ear_y

            ifin_1 = (x1 <= nose_x <= x2) and (y1 <= nose_y <= y2)
            ifin_2 = (x1 <= r_ear_x <= x2) and (y1 <= r_ear_y <= y2) and (x1 <= l_ear_x <= x2) and (y1 <= l_ear_y <= y2)
            ifin_3 = (x1 <= right_shoulder_x <= x2) and (y1 <= right_shoulder_y <= y2) and (x1 <= left_shoulder_x <= x2) and (y1 <= left_shoulder_y <= y2)

            if ifin_1 and ifin_2 and ifin_3:
                if (abs(ear_diff_x) - abs(ear_diff_y)) < 32:
                    print(abs(ear_diff_x) - abs(ear_diff_y))
                    frame[y:y + overlay_height, x:x + overlay_width] = step3
                    center.center_rect(first_rect, 1)
                    center.center_rect(second_rect, 1)
                else:
                    frame[y:y + overlay_height, x:x + overlay_width] = step2
                    center.center_rect(first_rect, 1)
                    center.center_rect(second_rect, 0)
            else:
                frame[y:y + overlay_height, x:x + overlay_width] = step1
                center.center_rect(first_rect, 0)
                center.center_rect(second_rect, 0)

            nose.body_circle(nose_x, nose_y)
            right_ear.body_circle(r_ear_x, r_ear_y)
            left_ear.body_circle(l_ear_x, l_ear_y)

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

