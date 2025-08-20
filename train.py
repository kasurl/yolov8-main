from ultralytics import YOLO

model = YOLO('runs/detect/train/weights/last.pt')

model.train(data='D:/codes/py/yolov8-main/ray_infrarred.yaml',workers=0, epochs=120,batch=16,imgsz=512,resume=True)