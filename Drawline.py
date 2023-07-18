import cv2

def Frame_Setting(frame, face_mesh):
    frame.flags.writeable = False  # 픽셀값 수정 불가능
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.flip(frame, 1)
    results = face_mesh.process(frame)

    frame.flags.writeable = True
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    return frame, results

def Draw_Center(frame, x, y):
    center_x = x // 2
    center_y = y // 2

    cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

