from ultralytics import YOLO

# Script para treinar um modelo YOLOv8 usando o pacote ultralytics
#
# - O modelo utilizado é o yolov8m (medium), recomendado para melhor desempenho em datasets pequenos.
# - O arquivo de configuração do dataset está em 'dataset/images/data.yaml'.
# - O número de épocas está ajustado para 150, permitindo mais iterações de treino.
# - A resolução das imagens foi aumentada para 960x960 para melhorar a qualidade do treinamento.
# - O batch size está reduzido para 4, ideal para máquinas com pouca VRAM.
# - O número de workers está definido como 2 para otimizar o carregamento dos dados.
# - O parâmetro patience está em 30, permitindo early stopping caso não haja melhora.

if __name__ == "__main__":
    # Inicializa o modelo YOLOv8 medium
    model = YOLO('models/yolov8m.pt')  # use o medium em vez do nano

    # Inicia o treinamento do modelo com os parâmetros definidos acima
    model.train(
        data='dataset/images/data.yaml',
        epochs=150,      # mais treino se o dataset for pequeno
        imgsz=960,       # aumentar resolução
        batch=4,         # reduzir se estiver com pouco VRAM
        workers=2,       # número de processos para carregar dados
        patience=30      # parar cedo se não melhorar
    )
