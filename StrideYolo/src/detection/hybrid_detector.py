import os
import json
import cv2
import easyocr
from ultralytics import YOLO


def detectar_componentes_com_texto(image_path, model_path='yolov8n.pt', output_json='runs/graph/componentes_hibrido.json'):
    os.makedirs(os.path.dirname(output_json), exist_ok=True)

    # Carregar modelo e imagem
    model = YOLO(model_path)
    image = cv2.imread(image_path)
    reader = easyocr.Reader(['en'], gpu=False)

    # Realiza a detecção com YOLO
    results = model.predict(image_path, save=False)
    componentes = []

    for r in results:
        for box, cls in zip(r.boxes.xyxy.cpu().numpy(), r.boxes.cls.cpu().numpy()):
            x1, y1, x2, y2 = map(int, box)
            label_icones = model.names[int(cls)]

            # Expandir um pouco a região para pegar texto ao redor
            pad = 20
            roi = image[max(0, y1 - pad):y2 + pad, max(0, x1 - pad):x2 + pad]

            textos = reader.readtext(roi)
            texto_final = textos[0][1] if textos else "<sem texto>"

            componentes.append({
                "icone": label_icones,
                "text": texto_final,
                "bbox": [x1, y1, x2, y2]
            })

    # Salvar resultado
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(componentes, f, indent=2, ensure_ascii=False)

    print(f"Resultado salvo em {output_json}")
    return componentes


# Exemplo de uso:
if __name__ == "__main__":
    caminho_imagem = "test_image.png"
    modelo_treinado = "runs/detect/train/weights/best.pt"  # Substitua se precisar

    componentes_detectados = detectar_componentes_com_texto(
        image_path=caminho_imagem,
        model_path=modelo_treinado
    )
