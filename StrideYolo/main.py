from src.detection.yolo_detector import YOLODetector
from src.processing.ocr_pipeline import OCRReader
from src.detection.hybrid_detector import detectar_componentes_com_texto
from src.processing.grafo_componentes import GrafoComponentes
from src.processing.stride_engine import STRIDEEngine
from src.reports.relatorio_generator import RelatorioGenerator
import sys
import os
import glob

# =============================
#  Configurações
# =============================
IMAGE_PATH = sys.argv[1] if len(sys.argv) > 1 else "dataset/images/test/1.png"
YOLO_MODEL_PATH = "runs/detect/train/weights/best.pt"
OUTPUT_GRAPH_PATH = "runs/graph"
os.makedirs(OUTPUT_GRAPH_PATH, exist_ok=True)

# Define conexões esperadas entre componentes
DEPENDENCIAS_PADRAO = {
    "User": ["API Gateway", "Frontend"],
    "Frontend": ["API Gateway"],
    "API Gateway": ["Backend"],
    "Backend": ["Database", "Cache", "Messaging", "Storage"],
    "Auth": ["Database"],
    "Firewall": ["Backend", "Frontend", "API Gateway"],
    "Workflow Engine": ["Backend"],
    "Search": ["Database"],
    "Messaging": ["Backend"],
    "App": ["Backend"],
    "Remote Access": ["Backend"],
    "Macine Learning": ["Storage"],
    "Load Balancer": ["Frontend", "Backend"],
    "Game Server": ["Database"],
}


# =============================
#  Detecção com YOLOv8
# =============================
print("Executando detecção com YOLOv8...")
detector = YOLODetector(YOLO_MODEL_PATH)
detected_objects = detector.predict(IMAGE_PATH)
componentes_mapeados = set()
for obj in detected_objects:
    componentes_mapeados.add(obj["label"])

print(f"Detecções encontradas: {len(detected_objects)}")

# =============================
#  OCR
# =============================
print("Executando OCR...")
ocr = OCRReader()
ocr_results = ocr.read_text(IMAGE_PATH)
print(f"Textos detectados: {ocr_results}")

# =============================
#  Detecção Híbrid
# =============================

print(" Executando detecção híbrida...")
hybrid_results = detectar_componentes_com_texto(IMAGE_PATH, YOLO_MODEL_PATH, output_json=os.path.join(OUTPUT_GRAPH_PATH, "componentes_hibrido.json"))


# =============================
#  Mapeamento Semântico
# =============================
print("Mapeando componentes...")
grafo = GrafoComponentes()
for comp in componentes_mapeados:
    grafo.adicionar_componente(comp)

print(f"Componentes mapeados: {componentes_mapeados}")

# =============================
#  Construção do Grafo
# =============================
print("Construindo grafo de conexões dinâmicas...")

# Criar conexões somente entre os componentes detectados
for origem, destinos in DEPENDENCIAS_PADRAO.items():
    if origem in componentes_mapeados:
        for destino in destinos:
            if destino in componentes_mapeados:
                grafo.adicionar_conexao(origem, destino)


# Exporta visualmente o grafo
grafo.visualizar_grafo()
grafo.exportar_grafo_graphml(os.path.join(OUTPUT_GRAPH_PATH, "grafo.graphml"))
grafo.exportar_grafo_imagem(os.path.join(OUTPUT_GRAPH_PATH, "grafo.png"))

# =============================
#  STRIDE
# =============================
print(" Aplicando STRIDE...")
stride = STRIDEEngine()
relatorio_stride = stride.analisar_todos(componentes_mapeados)
print("Ameaças encontradas:")
for componente, dados in relatorio_stride.items():
    print(f"🔹 {componente}: {dados['ameacas']}")

# =============================
#  Pega a última imagem YOLO gerada
# =============================

# Detecta o último diretório runs/detect/predict*
predict_dirs = sorted(glob.glob("runs/detect/predict*"), key=os.path.getmtime)
imagem_predicao = None
if predict_dirs:
    ultima_pasta = predict_dirs[-1]
    caminho_tentado = os.path.join(ultima_pasta, "1.jpg")
    if os.path.exists(caminho_tentado):
        imagem_predicao = caminho_tentado
        print(f"Imagem para o relatório: {imagem_predicao}")
    else:
        print("Nenhuma imagem 1.jpg encontrada no último predict")

# =============================
#  Relatório PDF
# =============================
print("Gerando relatório PDF...")
relatorio = RelatorioGenerator("Relatório de Ameaças STRIDE", imagem_predicao=imagem_predicao)
relatorio.gerar_relatorio(relatorio_stride)

print("Pipeline completo com sucesso!")

