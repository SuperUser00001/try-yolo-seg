## Step 1: 进行labelme标注
将图片放入 ./origin_dataset/images 下
对应的图像分割标注文件放入 ./origin_dataset/labelme_labels 下

## Step 2: 转换为yolo标注格式
用labelme2yolo.py将标注文件转为yolo格式，并放入 ./origin_dataset/yolo_labels 下

可以使用 visual_check_labels.py 脚本确认标注是正确的

## Step 3: 编写数据集说明
编写 dataset/dataset.yaml、dataset/train.txt、dataset/val.txt、dataset/test.txt

可以使用 split_train_val_test.py 脚本随机划分数据集

## Step 4: 训练模型
```bash
yolo task=segment mode=train model=yolo12-seg.yaml data=dataset.yaml epochs=500 imgsz=1024 mosaic=1 name=my_yolo12_from_scratch pretrained=False
```

```bash
yolo task=segment mode=train model=yolo12-seg.yaml data=dataset.yaml epochs=500 imgsz=1024 mosaic=1 name=my_yolo12_from_scratch resume=True
```

### 基于官方与预训练模型训练
```bash
yolo task=segment mode=train model=yolo12-seg.pt data=dataset.yaml epochs=100 imgsz=640
```
- `yolo`：调用 YOLO 训练命令（Ultralytics 版本）。
- `task=segment`：指定任务类型为 **实例分割**。
- `mode=train`：进入 **训练模式**。
- `model=yolo12-seg.pt`：**使用 `yolo12-seg.pt` 作为预训练模型**（不想用预训练模型的话需要改）。
- `data=dataset.yaml`：指定 **数据集配置文件**。
- `epochs=100`：训练 **100 轮**。
- `imgsz=640`：训练时图片输入大小为 **640x640**。

### 使用模型结构从头训练
```bash
yolo task=segment mode=train model=yolo12-seg.yaml data=dataset.yaml epochs=500 imgsz=1024 mosaic=1 name=my_yolo12_from_scratch
```
- `model=yolo12-seg.yaml`：**指定模型结构文件**，不加载预训练权重。
- `name=my_yolo12_from_scratch`：**指定输出模型的名字**，最终生成的 `.pt` 文件会保存在 `runs/segment/train_my_yolo12_from_scratch/weights/best.pt`。

### 从自己生成的模型继续训练
```bash
yolo task=segment mode=train model=runs/segment/train_my_yolo12_from_scratch/weights/best.pt data=dataset.yaml epochs=50 imgsz=640 name=my_yolo12_continue
```
- `model=runs/segment/train_my_yolo12_from_scratch/weights/best.pt`：**基于已有模型继续训练**。
- `epochs=50`：再继续训练 **50 轮**。
- `name=my_yolo12_continue`：新的训练结果会存到 `runs/segment/train_my_yolo12_continue/weights/best.pt`。


## Step 5: 测试、继续训练模型
### **问题 1：使用刚刚训练出的最优 `pt` 文件，对 `test` 集进行测试，并展示图片的标注效果**

#### **执行测试命令**
你可以使用以下命令，对 `test` 数据集进行推理，并保存预测结果：
```bash
yolo task=segment mode=val model=runs/segment/my_yolo12_from_scratch/weights/best.pt data=dataset.yaml split=test save=True save_txt=True
```
**解释：**
- `task=segment`：进行实例分割任务。
- `mode=val`：使用验证模式（但由于 `data=dataset.yaml` 里 `test:` 指向了测试集，所以实际是测试）。
- `model=runs/segment/my_yolo12_from_scratch/weights/best.pt`：使用刚训练好的最优模型进行测试。
- `data=dataset.yaml`：数据集描述文件，确保 `test:` 配置正确。
- `split=test`：指定使用测试集进行推理。
- `save=True`：保存预测后的标注图片。
- `save_txt=True`：保存检测结果的文本文件（可用于后续评估）。

#### **结果查看**
运行完成后，你可以在 `runs/segment/my_yolo12_from_scratch/test/` 目录下找到：
- **标注过的预测图片**（已画出分割掩码）。
- **预测结果的 `.txt` 文件**（格式和 YOLO 格式的标注文件相同）。

---

### **问题 2：基于刚刚训练出的模型继续训练，并且保存不同阶段的模型**
你希望：
1. **基于当前最优模型 (`best.pt`) 继续训练**，而不是从头开始。
2. **每次训练生成的模型不会覆盖之前的模型**，并且能够看到训练顺序关系。

#### **继续训练的命令**
```bash
yolo task=segment mode=train model=runs/segment/my_yolo12_from_scratch/weights/best.pt data=dataset.yaml epochs=200 imgsz=1024 mosaic=1 name=my_yolo12_finetune_1 pretrained=True
```
**解释：**
- `model=runs/segment/my_yolo12_from_scratch/weights/best.pt`：以之前训练的 `best.pt` 为初始权重，继续训练。
- `name=my_yolo12_finetune_1`：设置新的训练名称，防止覆盖旧的模型。

每次继续训练时，修改 `name`，例如：
```bash
yolo task=segment mode=train model=runs/segment/my_yolo12_finetune_1/weights/best.pt data=dataset.yaml epochs=200 imgsz=1024 mosaic=1 name=my_yolo12_finetune_2 pretrained=True
```
这样你可以清楚地看到：
```
runs/segment/my_yolo12_from_scratch/weights/best.pt  →  初始模型
runs/segment/my_yolo12_finetune_1/weights/best.pt  →  第一次微调
runs/segment/my_yolo12_finetune_2/weights/best.pt  →  第二次微调
```

---

### **问题 3：如何在 `test` 集上量化评估不同模型的效果**
你希望**不仅仅依赖人眼查看预测结果**，还想用定量指标评估模型的好坏。

#### **测试不同模型的性能**
可以使用以下命令，分别对不同训练阶段的 `pt` 文件进行测试：
```bash
yolo task=segment mode=val model=runs/segment/my_yolo12_from_scratch/weights/best.pt data=dataset.yaml split=test
```
```bash
yolo task=segment mode=val model=runs/segment/my_yolo12_finetune_1/weights/best.pt data=dataset.yaml split=test
```
```bash
yolo task=segment mode=val model=runs/segment/my_yolo12_finetune_2/weights/best.pt data=dataset.yaml split=test
```

#### **查看具体指标**
每次运行后，你会看到类似的输出：
```
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95)     Mask(P          R      mAP50  mAP50-95)
                   all          2          5      0.964          1      0.995      0.962      0.964          1      0.995      0.995
                orange          2          2      0.968          1      0.995      0.995      0.968          1      0.995      0.995
                  pear          2          3      0.961          1      0.995       0.93      0.961          1      0.995      0.995
```
**关键评估指标：**
- `Box(P, R, mAP50, mAP50-95)`：目标检测（Bounding Box）的性能指标
  - `P`（Precision）：精确率
  - `R`（Recall）：召回率
  - `mAP50`：IoU=0.5 时的均值平均精度
  - `mAP50-95`：不同 IoU 阈值的均值平均精度
- `Mask(P, R, mAP50, mAP50-95)`：分割掩码的性能指标

通过**对比不同 `pt` 文件的这些指标**，你可以量化评估各个训练阶段的性能提升。

---

### **总结**
1. **对 `test` 集推理，保存预测结果**
   ```bash
   yolo task=segment mode=val model=runs/segment/my_yolo12_from_scratch/weights/best.pt data=dataset.yaml split=test save=True save_txt=True
   ```
2. **继续训练，不覆盖之前模型**
   ```bash
   yolo task=segment mode=train model=runs/segment/my_yolo12_from_scratch/weights/best.pt data=dataset.yaml epochs=200 imgsz=1024 mosaic=1 name=my_yolo12_finetune_1 pretrained=True
   ```
3. **对不同模型进行定量评估**
   ```bash
   yolo task=segment mode=val model=runs/segment/my_yolo12_finetune_1/weights/best.pt data=dataset.yaml split=test
   ```

这样你可以不断优化模型，并清晰追踪训练进度🚀