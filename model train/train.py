from ultralytics import YOLO

model = YOLO('yolov8m.pt')

model.train(data='yolo_common.yaml',workers=0, epochs=200,batch=8,imgsz=512)