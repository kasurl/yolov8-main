from ultralytics import YOLO

model = YOLO('yolov8m.pt')

model.train(data='yolo_common.yaml',workers=0, epochs=150,batch=16,imgsz=512)