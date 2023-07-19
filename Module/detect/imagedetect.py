import torch
import cv2
import numpy as np

def detect():
    path = "weights/Version_1.pt"
    image_path = "Result/result.jpeg"

    model = torch.hub.load('ultralytics/yolov5', 'custom', path, force_reload=True)
    image = cv2.imread(image_path)

    height, width, _ = image.shape
    result = model(image)

    predictions = result.pandas().xyxy[0]  # 예측된 박스와 레이블 정보를 가져온다.

    # 클래스 이름을 가져오는 코드
    class_names = model.module.names if hasattr(model, 'module') else model.names

    # 경추 7번이 보이는가? 사람 귀가 보이는가? 에 대한 질문을 하는 변수
    count = 0

    for _, row in predictions.iterrows():
        label = row['name']
        confidence = row['confidence']
        bbox = row[['xmin', 'ymin', 'xmax', 'ymax']].values

        x_min, y_min, x_max, y_max = bbox.astype(np.int)

        if confidence > 0.51111:
            if label == 'number7' or label == 'ear':
                count += 1

            label_text = f"{label}: {confidence:.2f}"
            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)
            cv2.putText(image, label_text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return count
    # cv2.imshow("frame", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

result = detect()
print(result)