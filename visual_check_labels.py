from ultralytics import YOLO
import numpy as np
import cv2

img_path = "./dataset/images/00000020.jpg"
label_path = "./dataset/yolo_labels/00000020.txt"  # 你的标注文件路径

img = cv2.imread(img_path)
h, w, _ = img.shape

with open(label_path, "r") as f:
    labels = f.readlines()

for label in labels:
    label = label.strip().split()
    class_id = int(label[0])
    polygon = [float(x) for x in label[1:]]

    # 反归一化坐标
    polygon = [(int(polygon[i] * w), int(polygon[i + 1] * h)) for i in range(0, len(polygon), 2)]

    # 画多边形
    cv2.polylines(img, [np.array(polygon)], isClosed=True, color=(0, 255, 0), thickness=2)

cv2.imshow("Visualization", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
