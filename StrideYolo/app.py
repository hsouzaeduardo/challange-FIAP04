import streamlit as st
import subprocess
from PIL import Image
import os
import glob
import json

st.set_page_config(layout="wide")
st.title("Analise de Diagramas de Arquitetura com STRIDE e YOLO")

uploaded_file = st.file_uploader("Faça upload de uma imagem de diagrama de arquitetura", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Salvar a imagem enviada
    img_path = f"dataset/images/test/{uploaded_file.name}"
    os.makedirs(os.path.dirname(img_path), exist_ok=True)
    with open(img_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image(uploaded_file, caption="Diagrama enviado", use_container_width=True)
    st.write("Iniciando análise...")

    # Rodar o script principal
    process = subprocess.run(["python", "main.py", img_path], capture_output=True, text=True, encoding="utf-8", errors="ignore")

    log_output = (process.stdout or "") + "\n" + (process.stderr or "")
    st.text_area("Log do processamento:", log_output, height=300)

    # Mostrar anotações diversas se existirem
    if os.path.exists("runs/graph/grafo.png"):
        st.subheader("Grafo de Componentes")
        st.image("runs/graph/grafo.png", caption="Grafo de componentes", use_container_width=True)

    # Mostrar predição YOLO mais recente
    pred_dirs = sorted(glob.glob("runs/detect/predict*"), key=os.path.getmtime, reverse=True)
    if pred_dirs:
        latest_pred_path = os.path.join(pred_dirs[0], "1.jpg")
        if os.path.exists(latest_pred_path):
            st.subheader("Resultado da Detecção com YOLO")
            st.image(latest_pred_path, caption="Componentes detectados com YOLO", use_container_width=True)

    # Mostrar relatório estruturado
    relatorio_json_path = "relatorio_stride.json"
    if os.path.exists(relatorio_json_path):
        st.subheader("Ameaças e Contramedidas por Componente")
        with open(relatorio_json_path, "r", encoding="utf-8") as f:
            relatorio_data = json.load(f)

        for componente, data in relatorio_data.items():
            st.markdown(f"###  {componente}")
            st.markdown("**Ameaças:**")
            for ameaca in data["ameacas"]:
                st.markdown(f"- {ameaca}")
            st.markdown("**Contramedidas:**")
            for medida in data["contramedidas"]:
                st.markdown(f"* {medida}")

    # Botão para baixar PDF
    relatorio_pdf_path = "relatorio_stride.pdf"
    if os.path.exists(relatorio_pdf_path):
        with open(relatorio_pdf_path, "rb") as pdf_file:
            st.download_button("Baixar Relatório STRIDE (PDF)", data=pdf_file, file_name="relatorio_stride.pdf")
