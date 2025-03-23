import os
import json
import glob

# 配置路径
labelme_dir = "./dataset/labelme_labels"  # LabelMe 标注的 JSON 文件目录
output_dir = "./dataset/yolo_labels"  # YOLO 目标分割标签的保存目录
class_mapping = {"orange": 0, "pear": 1}  # 类别映射

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# 处理所有 JSON 文件
json_files = glob.glob(os.path.join(labelme_dir, "*.json"))
for json_file in json_files:
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    image_name = os.path.basename(data["imagePath"]).replace("\\", "/").split("/")[-1]

    image_height, image_width = data.get("imageHeight", 1), data.get("imageWidth", 1)
    # print(f"{image_name=}, {image_height=}, {image_width=}")

    txt_filename = os.path.splitext(os.path.basename(json_file))[0] + ".txt"
    txt_filepath = os.path.join(output_dir, txt_filename)
    # print(f"{txt_filename=}, {txt_filepath=}")

    with open(txt_filepath, "w") as f:
        for shape in data["shapes"]:
            label = shape["label"]
            if label not in class_mapping:
                print(f"{json_file=}: {label=} does not exist ")
                continue
            label_id = class_mapping[label]
            points = shape["points"]

            # 归一化坐标
            normalized_points = [
                (x / image_width, y / image_height) for x, y in points
            ]
            flattened_points = [coord for point in normalized_points for coord in point]

            # 写入 YOLO 格式: class_id x1 y1 x2 y2 ... xn yn
            f.write(f"{label_id} " + " ".join(map(str, flattened_points)) + "\n")

    print(f"✅ 处理完成：{txt_filename}")
