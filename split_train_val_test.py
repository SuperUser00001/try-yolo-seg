import os
import random

# 数据集路径
base_path = os.path.dirname(os.path.abspath(__file__))
origin_image_dir = os.path.join(base_path, "origin_dataset", "images")
origin_label_dir = os.path.join(base_path, "origin_dataset", "yolo_labels")

train_image_dir = os.path.join(base_path, "dataset", "train", "images");os.makedirs(train_image_dir, exist_ok=True)
train_label_dir = os.path.join(base_path, "dataset", "train", "labels");os.makedirs(train_label_dir, exist_ok=True)
valid_image_dir = os.path.join(base_path, "dataset", "valid", "images");os.makedirs(valid_image_dir, exist_ok=True)
valid_label_dir = os.path.join(base_path, "dataset", "valid", "labels");os.makedirs(valid_label_dir, exist_ok=True)
test_image_dir = os.path.join(base_path, "dataset", "test", "images");os.makedirs(test_image_dir, exist_ok=True)
test_label_dir = os.path.join(base_path, "dataset", "test", "labels");os.makedirs(test_label_dir, exist_ok=True)

# 获取所有图片文件
image_file_names = [f for f in os.listdir(origin_image_dir) if f.endswith(".jpg")]
label_file_names = []
for image_file_name in image_file_names:
    label_file_name = ".".join(image_file_name.split(".")[:-1] + ["txt"])
    label_file_names.append(label_file_name)
image_label_pairs = list(zip(image_file_names, label_file_names))
random.shuffle(image_label_pairs)

# 按比例拆分（80% 训练，10% 验证，5% 测试）
train_ratio = 0.85
val_ratio = 0.1
test_ratio = 0.05
num_train = int(len(image_label_pairs) * train_ratio)
num_val = int(len(image_label_pairs) * val_ratio)

train_pairs = image_label_pairs[:num_train]
val_pairs = image_label_pairs[num_train:num_train + num_val]
test_pairs = image_label_pairs[num_train + num_val:]

def _clear_old_data(folder_path):
    """only remove txt and jpg
    """
    if not os.path.isdir(folder_path):
        raise FileNotFoundError(folder_path)
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                print(f"file {file_path} will be removed.")
                os.remove(file_path)
def clear_old_data(dest_image_dir, dest_label_dir):
    _clear_old_data(dest_image_dir)
    _clear_old_data(dest_label_dir)
def copy_new_data(pairs, dest_image_dir, dest_label_dir):
    for pair in pairs:
        image_file_name, label_file_name = pair
        src_image_file_path = os.path.join(origin_image_dir, image_file_name)
        src_label_file_path = os.path.join(origin_label_dir, label_file_name)
        dest_image_file_path = os.path.join(dest_image_dir, image_file_name)
        dest_label_file_path = os.path.join(dest_label_dir, label_file_name)
        with open(src_image_file_path, "rb") as fin, open(dest_image_file_path, "wb") as fout:
            fin.seek(0)
            fout.seek(0)
            fout.write(fin.read())
        with open(src_label_file_path, "rb") as fin, open(dest_label_file_path, "wb") as fout:
            fin.seek(0)
            fout.seek(0)
            fout.write(fin.read())



clear_old_data(train_image_dir, train_label_dir)
copy_new_data(train_pairs, train_image_dir, train_label_dir)
clear_old_data(valid_image_dir, valid_label_dir)
copy_new_data(val_pairs, valid_image_dir, valid_label_dir)
clear_old_data(test_image_dir, test_label_dir)
copy_new_data(test_pairs, test_image_dir, test_label_dir)

print(train_pairs)
print(val_pairs)
print(test_pairs)


# random.shuffle(images)  # 随机打乱数据
#
# # 按比例拆分（80% 训练，10% 验证，5% 测试）
# train_ratio = 0.85
# val_ratio = 0.1
# test_ratio = 0.05
#
# num_train = int(len(images) * train_ratio)
# num_val = int(len(images) * val_ratio)
#
# train_images = images[:num_train]
# val_images = images[num_train:num_train + num_val]
# test_images = images[num_train + num_val:]
#
# # 写入文件
# def write_list(filename, data):
#     with open(filename, "w") as f:
#         for img in data:
#             f.write(f"images/{img}\n")
#
# write_list(train_file, train_images)
# write_list(val_file, val_images)
# write_list(test_file, test_images)
#
# print(f"train.txt: {len(train_images)} images")
# print(f"val.txt: {len(val_images)} images")
# print(f"test.txt: {len(test_images)} images")
