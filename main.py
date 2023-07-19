import cv2
import mediapipe as mp
import threading
import time

from Module.Frame.setting import frame_setting, get_shape
from Module.Draw.draw import Draw
from Module.Draw.XY import rect_vertex

def main():
    cap = cv2.VideoCapture(0)

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        overlay_image = cv2.imread('../Text.png')

        # 이미지 크기 조정
        overlay_width = 100
        overlay_height = 100
        overlay_image = cv2.resize(overlay_image, (overlay_width, overlay_height))

        # 작은 이미지 삽입할 위치
        x = 200
        y = 400

        frame_rgb = frame_setting(frame)  # BGR 이미지를 RGB로 변환합니다.
        results = pose.process(frame_rgb)

        if results.pose_landmarks:
            right_ear_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EAR]
            left_ear_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EAR]
            nose = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]

            h, w, _ = frame.shape
            right_ear_x, right_ear_y = int(right_ear_landmark.x * w), int(right_ear_landmark.y * h)
            left_ear_x, left_ear_y = int(left_ear_landmark.x * w), int(left_ear_landmark.y * h)
            nose_x, nose_y = int(nose.x * w), int(nose.y * h)

            right_ear = Draw(frame, width, height)
            left_ear = Draw(frame, width, height)
            nose = Draw(frame, width, height)
            center = Draw(frame, width, height)

            diff_x = left_ear_x - right_ear_x
            diff_y = left_ear_y - right_ear_y

            if (x1 <= nose_x <= x2) and (y1 <= nose_y <= y2):
                if diff_x < 28 and diff_y < 8:
                    center.center_rect(first_rect, 1)
                    center.center_rect(second_rect, 1)
                else:
                    center.center_rect(first_rect, 1)
                    center.center_rect(second_rect, 0)
            else:
                frame[y:y + overlay_height, x:x + overlay_width] = overlay_image # 이미지 삽입
                center.center_rect(first_rect, 0)
                center.center_rect(second_rect, 0)

            print(diff_x, diff_y)
            nose.body_circle(nose_x, nose_y)
            right_ear.body_circle(right_ear_x, right_ear_y)
            left_ear.body_circle(left_ear_x, left_ear_y)

        cv2.imshow('Main', frame)  # 결과 프레임을 보여줍니다.

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    # cap shape
    width, height = get_shape(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    x1, x2, y1, y2 = rect_vertex(width, height)
    first_rect = 400
    second_rect = 386

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    main_thread = threading.Thread(target=main())
    main_thread.start()

