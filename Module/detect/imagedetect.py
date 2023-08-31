import torch
import cv2
import numpy as np

from Module.Draw.draw import Angle

def detect():
    result_value = []
    xy_list = []
    path = "weights/Version_1.pt"
    image_path = "Result/UserPicture.jpeg"

    model = torch.hub.load('ultralytics/yolov5', 'custom', path, force_reload=True)
    image = cv2.imread(image_path)
    result = model(image)

    predictions = result.pandas().xyxy[0]  # 예측된 박스와 레이블 정보를 가져온다.

    for _, row in predictions.iterrows():
        label = row['name']
        confidence = row['confidence']
        bbox = row[['xmin', 'ymin', 'xmax', 'ymax']].values

        x_min, y_min, x_max, y_max = bbox.astype(int)

        if confidence > 0.51111:
            # print(len(label))
            if label == 'number7' or label == 'ear':
                if label == 'number7':
                    number7 = Angle(image, int((x_min + x_max) / 2), int((y_min + y_max) / 2))
                    number7_x, number7_y = number7.return_xy()
                    number7.position_rect(x_min, y_min, x_max, y_max, number7_x, number7_y, f"{label}: {confidence:.2f}")
                    xy_list.append([number7_x, number7_y]) # 측정된 박스 좌표를 건네줌

                if label == 'ear':
                    ear = Angle(image, int((x_min + x_max) / 2), int((y_min + y_max) / 2))
                    ear_x, ear_y = ear.return_xy()
                    ear.position_rect(x_min, y_min, x_max, y_max, ear_x, ear_y, f"{label}: {confidence:.2f}")
                    xy_list.append([ear_x, ear_y])

    turtle_angel = Angle(image, _, _)

    result_value = turtle_angel.turtle_neck(xy_list)

    print(f"result_value : {result_value}")

    cv2.imwrite('Result/Result.jpeg', image)
    cv2.destroyAllWindows()

    return result_value