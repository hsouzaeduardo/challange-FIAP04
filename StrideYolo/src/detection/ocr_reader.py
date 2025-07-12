
import easyocr

class OCRReader:
    def __init__(self, languages=['en']):
        self.reader = easyocr.Reader(languages)

    def read_text(self, image_path):
        results = self.reader.readtext(image_path)

        texts = []
        for (bbox, text, prob) in results:
            texts.append({
                'text': text,
                'bbox': bbox,
                'confidence': prob
            })

        return texts


if __name__ == "__main__":
    ocr = OCRReader()
    image_path = "test_image.png"
    results = ocr.read_text(image_path)

    for res in results:
        print(f"Texto: {res['text']} - Confiança: {res['confidence']} - BBox: {res['bbox']}")
