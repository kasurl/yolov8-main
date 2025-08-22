from ultralytics import YOLO

model = YOLO('yolov8m.pt')

model.train(data='D:/codes/py/yolov8-main/ray_infrarred.yaml',workers=0, epochs=120,batch=24,imgsz=512,resume=True)