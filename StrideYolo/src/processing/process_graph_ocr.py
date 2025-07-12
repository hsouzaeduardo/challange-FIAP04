import json
import os
import networkx as nx
from shapely.geometry import Polygon


def load_graph(graph_path):
    return nx.read_graphml(graph_path)


def load_ocr(ocr_folder='runs/ocr_results'):
    ocr_data = {}
    for file_name in os.listdir(ocr_folder):
        if file_name.endswith('.json'):
            image_name = os.path.splitext(file_name)[0]
            file_path = os.path.join(ocr_folder, file_name)

            with open(file_path, 'r', encoding='utf-8') as f:
                ocr_data[image_name] = json.load(f)

    return ocr_data


def bbox_to_polygon(bbox):
    # Se for lista de 4 pontos [[x, y], ...]
    if isinstance(bbox[0], (list, tuple)):
        return Polygon(bbox)

    # Se for formato [x_min, y_min, x_max, y_max]
    x_min, y_min, x_max, y_max = bbox
    return Polygon([
        (x_min, y_min),
        (x_max, y_min),
        (x_max, y_max),
        (x_min, y_max)
    ])


def associate_ocr_to_components(graph, ocr_data):
    result = {}

    for node_id, data in graph.nodes(data=True):
        node_bbox = eval(data.get('bbox', '[]'))  # String para lista
        node_type = data.get('label', 'Unknown')

        node_poly = bbox_to_polygon(node_bbox)

        matched_texts = []

        image_key = node_id.split('_')[0]  # Matcha pelo nome da imagem
        ocr_items = ocr_data.get(image_key, {}).get('ocr', [])

        for ocr_item in ocr_items:
            ocr_bbox = ocr_item.get('bbox', [])
            if not ocr_bbox:
                continue

            ocr_poly = bbox_to_polygon(ocr_bbox)

            if node_poly.intersects(ocr_poly):
                matched_texts.append(ocr_item.get('text', ''))

        result[node_id] = {
            'type': node_type,
            'label': ' '.join(matched_texts).strip() if matched_texts else None,
            'connections': []
        }

    for source, target in graph.edges():
        result[source]['connections'].append(target)

    return result


def save_json(data, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    graph_path = 'runs/graph/graph.graphml'
    ocr_path = 'runs/ocr_results'
    output_path = 'runs/components_data.json'

    print('Carregando grafo...')
    graph = load_graph(graph_path)

    print('Carregando dados de OCR...')
    ocr_data = load_ocr(ocr_path)

    print('Associando textos aos componentes...')
    result = associate_ocr_to_components(graph, ocr_data)

    print('Salvando resultado em JSON...')
    save_json(result, output_path)

    print(f'Processamento concluído. Resultado salvo em {output_path}')
