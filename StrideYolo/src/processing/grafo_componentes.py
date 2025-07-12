import os
import json
import networkx as nx
import matplotlib.pyplot as plt
import cv2


class GrafoComponentes:
    def __init__(self):
        self.graph = nx.DiGraph()

    def carregar_dados_yolo(self, results_path='runs/detect/predict/predict.json'):
        with open(results_path, 'r', encoding='utf-8') as f:
            self.yolo_data = json.load(f)

    def adicionar_componente(self, nome, bbox=None, tipo=None):
        self.graph.add_node(nome, bbox=bbox, tipo=tipo)

    def adicionar_conexao(self, origem, destino, tipo="conexao"):
        self.graph.add_edge(origem, destino, tipo=tipo)

    def criar_grafo(self):
        for item in self.yolo_data:
            image_name = item['image']
            detections = item['detections']

            for i, det in enumerate(detections):
                label = det['class']
                bbox = det['box']
                node_id = f"{image_name}_{label}_{i}"

                self.graph.add_node(node_id, label=label, bbox=bbox)

            for i, source in enumerate(detections):
                for j, target in enumerate(detections):
                    if i != j:
                        x1, y1 = source['box'][:2]
                        x2, y2 = target['box'][:2]

                        distancia = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                        if distancia < 300:
                            source_id = f"{image_name}_{source['class']}_{i}"
                            target_id = f"{image_name}_{target['class']}_{j}"

                            if not self.graph.has_edge(source_id, target_id):
                                self.graph.add_edge(source_id, target_id)

    def visualizar_grafo(self):
        plt.figure(figsize=(15, 10))
        pos = nx.spring_layout(self.graph, k=0.5)
        labels = nx.get_node_attributes(self.graph, 'label')

        nx.draw(
            self.graph,
            pos,
            with_labels=True,
            labels=labels if labels else None,
            node_size=1500,
            node_color='lightblue',
            font_size=10,
            arrows=True
        )

        plt.title('Grafo dos Componentes Detectados')
        plt.show()

    def exportar_grafo_imagem(self, path='runs/graph/grafo.png'):
        os.makedirs(os.path.dirname(path), exist_ok=True)

        plt.figure(figsize=(15, 10))
        pos = nx.spring_layout(self.graph, k=0.5)
        labels = nx.get_node_attributes(self.graph, 'label')

        nx.draw(
            self.graph,
            pos,
            with_labels=True,
            labels=labels if labels else None,
            node_size=1500,
            node_color='lightblue',
            font_size=10,
            arrows=True
        )

        plt.title('Grafo dos Componentes Detectados')
        plt.savefig(path, format='png')
        plt.close()
        print(f'Grafo salvo como imagem em {path}')

    def exportar_grafo_graphml(self, path='runs/graph/graph.graphml'):
        os.makedirs(os.path.dirname(path), exist_ok=True)

        for node, data in self.graph.nodes(data=True):
            for key in list(data.keys()):
                if data[key] is None:
                    del data[key]
                elif isinstance(data[key], list):
                    data[key] = ', '.join(map(str, data[key]))

        for u, v, data in self.graph.edges(data=True):
            for key in list(data.keys()):
                if data[key] is None:
                    del data[key]
                elif isinstance(data[key], list):
                    data[key] = ', '.join(map(str, data[key]))

        nx.write_graphml(self.graph, path)
        print(f'Grafo salvo em {path} (formato .graphml)')

    @staticmethod
    def desenhar_componentes_na_imagem(image_path, objetos, output_path="runs/graph/annotated.png"):
        def convert_bbox_polygon_to_rect(bbox):
            if isinstance(bbox[0], list):
                x_coords = [point[0] for point in bbox]
                y_coords = [point[1] for point in bbox]
                x = int(min(x_coords))
                y = int(min(y_coords))
                x2 = int(max(x_coords))
                y2 = int(max(y_coords))
                return x, y, x2 - x, y2 - y
            return map(int, bbox)

        if not os.path.exists(image_path):
            print(f"Imagem não encontrada: {image_path}")
            return

        image = cv2.imread(image_path)

        for obj in objetos:
            bbox = obj.get("bbox", [])
            if len(bbox) != 4:
                continue

            try:
                x, y, w, h = convert_bbox_polygon_to_rect(bbox)
                x1, y1 = x, y
                x2, y2 = x + w, y + h

                label = obj.get("label", obj.get("icone", "Unknown"))
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(image, label, (x1, max(y1 - 10, 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (36, 255, 12), 2)
            except Exception as e:
                print(f"Erro ao desenhar bbox {bbox}: {e}")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(output_path, image)
        print(f"Imagem anotada salva em: {output_path}")

    @staticmethod
    def desenhar_yolo(image_path, detections, output_path="runs/graph/yolo_only.png"):
        img = cv2.imread(image_path)

        for obj in detections:
            bbox = obj["bbox"]
            label = obj["label"]

            x, y, w, h = map(int, bbox)
            x1, y1, x2, y2 = x, y, x + w, y + h

            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, label, (x1, max(y1 - 10, 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (36, 255, 12), 2)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(output_path, img)
        print(f"YOLO anotado salvo em {output_path}")

    @staticmethod
    def desenhar_ocr(image_path, ocr_results, output_path="runs/graph/ocr_only.png"):
        def convert_bbox_polygon_to_rect(bbox):
            x_coords = [point[0] for point in bbox]
            y_coords = [point[1] for point in bbox]
            x = int(min(x_coords))
            y = int(min(y_coords))
            x2 = int(max(x_coords))
            y2 = int(max(y_coords))
            return x, y, x2 - x, y2 - y

        img = cv2.imread(image_path)

        for item in ocr_results:
            bbox = item.get("bbox")
            texto = item.get("text") or item.get("texto") or "<sem texto>"

            if bbox and len(bbox) == 4:
                try:
                    x, y, w, h = convert_bbox_polygon_to_rect(bbox)
                    x1, y1, x2, y2 = x, y, x + w, y + h
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.putText(img, texto, (x1, max(y1 - 10, 10)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                except Exception as e:
                    print(f"Erro ao processar bbox {bbox}: {e}")
            else:
                print(f"OCR item ignorado, bbox inválido: {bbox}")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(output_path, img)
        print(f"OCR anotado salvo em {output_path}")


# Execução de teste
if __name__ == '__main__':
    grafo = GrafoComponentes()
    grafo.carregar_dados_yolo('runs/detect/predict/predict.json')
    grafo.criar_grafo()
    grafo.visualizar_grafo()
    grafo.exportar_grafo_imagem()
    grafo.exportar_grafo_graphml()
