# relatorio_generator.py (com imagem e ordenado)
from fpdf import FPDF
import os

THREATS = {
    "API Gateway": ["Spoofing", "Tampering", "Repudiation", "DoS", "Privilege Escalation"],
    "Database": ["Tampering", "Information Disclosure", "DoS", "Privilege Escalation"],
    "Cache": ["Tampering", "DoS"],
    "Authentication": ["Spoofing", "Privilege Escalation"],
    "Load Balancer": ["DoS"],
    "Storage": ["Information Disclosure", "Tampering"],
    "Backend": ["Tampering", "DoS", "Privilege Escalation"],
    "Frontend": ["Tampering", "DoS", "Privilege Escalation"],
    "Messaging": ["Tampering", "DoS"],
    "Configuration": ["Tampering", "Information Disclosure"],
    "Networking": ["Spoofing", "Information Disclosure", "DoS"],
    "User": ["Spoofing", "Repudiation"],
    "VPC": ["Tampering", "Information Disclosure"],
    "Workflow Engine": ["Tampering", "Privilege Escalation"],
    "AI Service": ["Information Disclosure", "Tampering"],
    "Machine Learning": ["Information Disclosure", "Tampering"],
    "Search": ["Information Disclosure"],
    "Game Server": ["Tampering", "DoS"],
    "Remote Access": ["Spoofing", "Tampering"],
    "App": ["Tampering", "DoS"]
}


CONTRAMEDIDAS = {
    "Spoofing": "Use autenticação forte (MFA, tokens).",
    "Tampering": "Implemente validação de integridade e criptografia.",
    "Repudiation": "Use logs assinados e não-repudiáveis.",
    "Information Disclosure": "Use TLS e criptografia em repouso.",
    "DoS": "Implemente limites de taxa e escalabilidade automática.",
    "Privilege Escalation": "Restrinja permissões com o princípio do menor privilégio."
}

class STRIDEEngine:
    def __init__(self):
        self.ameacas = THREATS
        self.contramedidas = CONTRAMEDIDAS

    def aplicar_stride(self, componente):
        return self.ameacas.get(componente, ["Unknown"])

    def analisar_todos(self, componentes):
        resultado = {}
        for componente in componentes:
            ameacas = self.aplicar_stride(componente)
            resultado[componente] = {
                "ameacas": ameacas,
                "contramedidas": [self.contramedidas[a] for a in ameacas if a in self.contramedidas]
            }
        return resultado

class RelatorioGenerator:
    def __init__(self, titulo="Relatório STRIDE", imagem_predicao=None):
        self.pdf = FPDF()
        self.titulo = titulo
        self.imagem_predicao = imagem_predicao
        self.pdf.set_auto_page_break(auto=True, margin=15)

    def adicionar_titulo(self):
        self.pdf.set_font("Arial", 'B', 16)
        self.pdf.cell(0, 10, self.titulo, ln=True, align="C")
        self.pdf.ln(10)

    def adicionar_imagem_predicao(self):
        if self.imagem_predicao and os.path.exists(self.imagem_predicao):
            self.pdf.set_font("Arial", 'B', 12)
            self.pdf.cell(0, 10, "Imagem da Arquitetura com Detecção:", ln=True)
            self.pdf.image(self.imagem_predicao, x=10, w=180)
            self.pdf.ln(10)

    def adicionar_componente(self, componente, ameacas, contramedidas):
        self.pdf.set_font("Arial", 'B', 12)
        self.pdf.cell(0, 10, f"Componente: {componente}", ln=True)
        self.pdf.set_font("Arial", '', 11)
        self.pdf.cell(0, 8, "Ameaças:", ln=True)
        for ameaca in ameacas:
            self.pdf.cell(0, 8, f" - {ameaca}", ln=True)
        self.pdf.cell(0, 8, "Contramedidas:", ln=True)
        for cm in contramedidas:
            self.pdf.multi_cell(0, 8, f" * {cm}")
        self.pdf.ln(5)

    def gerar_relatorio(self, resultados, output_path="relatorio_stride.pdf"):
        self.pdf.add_page()
        self.adicionar_titulo()
        self.adicionar_imagem_predicao()
        for componente in sorted(resultados.keys()):
            data = resultados[componente]
            self.adicionar_componente(componente, data["ameacas"], data["contramedidas"])
        self.pdf.output(output_path)
        print(f"Relatório salvo em {output_path}")

if __name__ == "__main__":
    componentes = list(THREATS.keys())
    stride = STRIDEEngine()
    resultado = stride.analisar_todos(componentes)

    relatorio = RelatorioGenerator("Relatório de Ameaças STRIDE", imagem_predicao="runs/detect/predict5/8.jpg")
    relatorio.gerar_relatorio(resultado)
