import os
import random

# 数据集路径
image_dir = "dataset/images"
train_file = "dataset/train.txt"
val_file = "dataset/val.txt"
test_file = "dataset/test.txt"

# 获取所有图片文件
images = [f for f in os.listdir(image_dir) if f.endswith(".jpg")]
random.shuffle(images)  # 随机打乱数据

# 按比例拆分（80% 训练，10% 验证，5% 测试）
train_ratio = 0.85
val_ratio = 0.1
test_ratio = 0.05

num_train = int(len(images) * train_ratio)
num_val = int(len(images) * val_ratio)

train_images = images[:num_train]
val_images = images[num_train:num_train + num_val]
test_images = images[num_train + num_val:]

# 写入文件
def write_list(filename, data):
    with open(filename, "w") as f:
        for img in data:
            f.write(f"images/{img}\n")

write_list(train_file, train_images)
write_list(val_file, val_images)
write_list(test_file, test_images)

print(f"train.txt: {len(train_images)} images")
print(f"val.txt: {len(val_images)} images")
print(f"test.txt: {len(test_images)} images")
