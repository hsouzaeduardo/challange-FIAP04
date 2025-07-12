
from ultralytics import YOLO
import os

class YOLODetector:
    def __init__(self, model_path="yolov8n.pt"):
        self.model = YOLO(model_path)
    
    def predict(self, image_path, save=True, save_dir="runs/detect"):
        results = self.model.predict(image_path, save=save, save_dir=save_dir)
        detections = []

        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy() if result.boxes else []
            classes = result.boxes.cls.cpu().numpy() if result.boxes else []
            confidences = result.boxes.conf.cpu().numpy() if result.boxes else []

            for box, cls, conf in zip(boxes, classes, confidences):
                detections.append({
                    "bbox": box.tolist(),
                    "class_id": int(cls),
                    "confidence": float(conf),
                    "label": self.model.names[int(cls)]
                })

        return detections

if __name__ == "__main__":
    detector = YOLODetector("yolov8n.pt")  # ou caminho do seu modelo treinado
    image_path = "test_image.png"
    results = detector.predict(image_path)

    for res in results:
        print(res)
