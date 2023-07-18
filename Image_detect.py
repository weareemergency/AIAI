import torch
import cv2
import numpy as np

path = "Weight file path"
model = torch.hub.load('ultralytics/yolov5', 'custom', path, force_reload=True)

image_path = "Image file path"

image = cv2.imread(image_path)

result = model(image)
predictions = result.pandas().xyxy[0]  # 예측된 박스와 레이블 정보를 가져온다.

# 클래스 이름을 가져오는 코드
class_names = model.module.names if hasattr(model, 'module') else model.names

for _, row in predictions.iterrows():
    label = row['name']
    confidence = row['confidence']
    bbox = row[['xmin', 'ymin', 'xmax', 'ymax']].values

    x_min, y_min, x_max, y_max = bbox.astype(np.int)

    if confidence > 0.51111:
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)
        label_text = f"{label}: {confidence:.2f}"
        cv2.putText(image, label_text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

cv2.imshow("frame", image)
cv2.waitKey(0)

cv2.destroyAllWindows()