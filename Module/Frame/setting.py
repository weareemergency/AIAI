import cv2

def frame_setting(frame, face_mesh):
    frame.flags.writeable = False  # 픽셀값 수정 불가능
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.flip(frame, 1)
    results = face_mesh.process(frame)

    frame.flags.writeable = True
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    return frame, results

def get_shape(width, height):
    width = width
    height = height

    return width, height
