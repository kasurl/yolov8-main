from ultralytics import YOLO

model = YOLO('yolov8n.pt')

model.train(data='yolo_common.yaml',workers=0, epochs=70,batch=16)