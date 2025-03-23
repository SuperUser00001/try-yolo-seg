import os
from ultralytics import YOLO

# print(os.environ["OLLAMA_MODELS"])

# 检查是否能正确加载YOLOv12
model = YOLO("./yolo12-seg.yaml") # 预训练模型只是用于检查能否正确加载
print(model)