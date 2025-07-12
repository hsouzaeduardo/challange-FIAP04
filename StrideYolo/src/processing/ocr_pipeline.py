import json
import os
import cv2
import easyocr
import numpy as np
from pathlib import Path


class OCRReader:
    def __init__(self, languages=['en']):
        self.reader = easyocr.Reader(languages)

    def read_text(self, image_path):
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        results = self.reader.readtext(gray)

        texts = []
        for (bbox, text, prob) in results:
            # Convertendo para tipos Python puros
            bbox_list = [[float(coord) for coord in point] for point in bbox]

            texts.append({
                'text': text,
                'bbox': bbox_list,
                'confidence': float(prob)
            })

        return texts


def run_ocr():
    # Caminhos
    yolo_json_path = 'runs/detect/predict/predict.json'
    image_folder = 'dataset/images/test'
    output_folder = 'runs/ocr_results'

    os.makedirs(output_folder, exist_ok=True)

    # Carregar dados YOLO
    with open(yolo_json_path, 'r', encoding='utf-8') as f:
        yolo_data = json.load(f)

    # Iniciar OCR
    ocr = OCRReader(languages=['en'])

    # Processar cada imagem
    for item in yolo_data:
        image_name = item['image']
        detections = item['detections']

        image_path = os.path.join(image_folder, image_name)

        if not os.path.exists(image_path):
            print(f"Imagem não encontrada: {image_path}")
            continue

        print(f"🔍 Processando {image_name}...")

        ocr_results = ocr.read_text(image_path)

        result = {
            'image': image_name,
            'detections': detections,
            'ocr': ocr_results
        }

        output_path = os.path.join(output_folder, f"{Path(image_name).stem}_ocr.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

    print(f"OCR concluído. Resultados salvos em {output_folder}")


if __name__ == "__main__":
    run_ocr()
