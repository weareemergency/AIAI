import cv2
import mediapipe as mp
import threading
import time

from Module.Frame.setting import frame_setting, get_shape
from Module.Draw.draw import Draw
from Module.Draw.XYvalue import rect_vertex

def main():
    count = 0
    with mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as face_mesh:
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                print("웹캠을 찾을 수 없습니다.")
                continue

            frame, results = frame_setting(frame, face_mesh)

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    for idx, landmark in enumerate(face_landmarks.landmark):
                        x = int(landmark.x * frame.shape[1])
                        y = int(landmark.y * frame.shape[0])

                        center = Draw()
                        face = Draw()

                        # 코 인덱스 4번 / 귀 인덱스 234, 454번
                        if idx == 4 or idx == 234 or idx == 454:
                            face.face(frame, x, y)
                            if idx == 4:
                                if (x1 <= x <= x2) and (y1 <= y <= y2):
                                    center.center_rect(frame, width, height, value, 1)
                                else:
                                    center.center_rect(frame, width, height, value, 0)

            cv2.imshow('Frame', frame)
            if cv2.waitKey(5) == 27:
                break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    width, height = get_shape(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    mp_face_mesh = mp.solutions.face_mesh

    # 센터에 그려지는 사각형 꼭짓점 좌표를 구함
    x1, x2, y1, y2 = rect_vertex(width, height)
    value = 400

    main_thread = threading.Thread(target=main())
    main_thread.start()
