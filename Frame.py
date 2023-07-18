import cv2
import mediapipe as mp

from Drawline import Draw_Center, Frame_Setting

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv2.VideoCapture(0)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

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

        # frame 설정
        # frame.flags.writeable = False # 픽셀값 수정 불가능
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # frame = cv2.flip(frame, 1)
        # results = face_mesh.process(frame)
        #
        # frame.flags.writeable = True
        # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame, results = Frame_Setting(frame, face_mesh)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                for idx, landmark in enumerate(face_landmarks.landmark):
                    x = int(landmark.x * frame.shape[1])
                    y = int(landmark.y * frame.shape[0])

                    Draw_Center(frame, width, height)

                    # 코 인덱스 4번
                    if idx == 4:
                        cv2.circle(frame, (x, y), 3, (0, 0, 255), 3)

                    # 귀 인덱스 234, 454번
                    if idx == 234 or idx == 454:
                        cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)

        cv2.imshow('Frame', frame)
        if cv2.waitKey(5) == 27:
            break
cap.release()
cv2.destroyAllWindows()