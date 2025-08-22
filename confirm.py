from ultralytics import YOLO

# Load a model
model = YOLO("runs/detect/train/weights/best.pt")  # load a custom model

if __name__ == '__main__':
# Validate the model
    metrics = model.val()  # no arguments needed, dataset and settings remembered
