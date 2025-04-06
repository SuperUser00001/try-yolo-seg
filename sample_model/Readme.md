# How to test
```bash
yolo task=segment mode=val model=sample_model/best.pt data=sample_model/dataset.yaml split=test save=True save_txt=True
```