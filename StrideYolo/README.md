
# 🛡️ STRIDE IA – Análise Inteligente de Ameaças a partir de Diagramas de Arquitetura

## 💡 Objetivo

Analisar automaticamente **diagramas de arquitetura de software** (AWS, Azure, Oracle, etc.) e gerar um **Relatório de Ameaças STRIDE** usando visão computacional.  
A ideia é simplificar a segurança, automatizando o processo e gerando insights rápidos e acionáveis.

---

## ⚙️ Como Funciona (Pipeline)

1️⃣ **Detecção com YOLOv8** — identifica os componentes na imagem.  
2️⃣ **Interpretação automática** — sem OCR ou mapeamento manual.  
3️⃣ **Geração do grafo de conexões** — dinâmica e visual.  
4️⃣ **Aplicação do STRIDE** — análise completa de ameaças.  
5️⃣ **Geração do relatório** — com imagem, lista de ameaças e contramedidas.

---

## 🧰 Tecnologias

- Python 3.12.6
- YOLOv8 (Ultralytics)
- OpenCV
- EasyOCR (opcional, para leitura híbrida)
- NetworkX + Matplotlib
- FPDF (PDF do relatório)
- Streamlit (interface web)

---

## 🗂️ Estrutura do Projeto

```
strideyolo/
├── dataset/
│   └── images/test/         # Imagens para análise
├── models/                  # Modelos YOLOv8
├── outputs/                 # Saídas futuras
├── runs/
│   ├── detect/             # Predições YOLO
│   └── graph/             # Grafos e imagens anotadas
├── src/
│   ├── detection/         # Detecção YOLO e híbrida
│   ├── processing/       # STRIDE, grafo, OCR
│   └── reports/          # Relatórios PDF e JSON
├── main.py               # Pipeline principal
├── app.py                # Interface Streamlit
├── requirements.txt
├── README.md
```

---

## 🚀 Como Rodar

### 1️⃣ Clone o projeto

```bash
git clone https://github.com/hsouzaeduardo/challange-FIAP04.git
cd strideyolo
```

### 2️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

### 3️⃣ Para execução manual adicione sua imagem

Coloque o diagrama em:  
`dataset/images/test/1.png`

### 4️⃣ Execute a análise

```bash
python main.py
```

---

## 💻 Interface Web com upload

Se quiser usar uma interface amigável com Streamlit:

```bash
streamlit run app.py
```

### O que dá pra fazer na interface?

- Subir imagens
- Visualizar o grafo
- Conferir ameaças STRIDE por componente
- Baixar o relatório em PDF

---

## ✅ O que você vai receber

- `relatorio_stride.pdf` — relatório com imagem, ameaças e contramedidas
- `relatorio_stride.json` — dados estruturados
- `runs/graph/grafo.png` — grafo de conexões
- `runs/detect/predict*/1.jpg` — imagem anotada

---

## 👨‍💻 Autor

**Henrique Eduardo Souza **

---

## 📝 Licença

MIT License
