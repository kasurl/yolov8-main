from ultralytics import YOLO
yolo = YOLO("runs/detect/train/weights/best.pt", task="detect")
result = yolo(source="datasets/mytrain/check_val/val_512", save=True)
