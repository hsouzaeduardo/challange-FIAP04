THREATS = {'AI Service': ['Information Disclosure', 'Tampering'], 'API Gateway': ['Spoofing', 'Tampering', 'Repudiation', 'DoS', 'Privilege Escalation'], 'Auth': ['Spoofing', 'Privilege Escalation'], 'Backend': ['Tampering', 'DoS', 'Privilege Escalation'], 'Cache': ['Tampering', 'DoS'], 'Configuration': ['Tampering', 'Information Disclosure'], 'Database': ['Tampering', 'Information Disclosure', 'DoS', 'Privilege Escalation'], 'Firewall': ['DoS', 'Information Disclosure'], 'Frontend': ['Tampering', 'Spoofing'], 'Game Server': ['DoS', 'Tampering'], 'Load Balancer': ['DoS'], 'Macine Learning': ['Information Disclosure', 'Tampering'], 'Messaging': ['Tampering', 'DoS'], 'Networking': ['DoS', 'Information Disclosure'], 'Remote Access': ['Spoofing', 'Tampering'], 'Search': ['Information Disclosure'], 'Storage': ['Information Disclosure', 'Tampering'], 'User': ['Repudiation', 'Spoofing'], 'VPC': ['Tampering', 'DoS'], 'Workflow Engine': ['Repudiation', 'DoS']}

CONTRAMEDIDAS = {'Spoofing': 'Use autenticação forte (MFA, tokens).', 'Tampering': 'Implemente validação de integridade e criptografia.', 'Repudiation': 'Use logs assinados e não-repudiáveis.', 'Information Disclosure': 'Use TLS e criptografia em repouso.', 'DoS': 'Implemente limites de taxa e escalabilidade automática.', 'Privilege Escalation': 'Restrinja permissões com o princípio do menor privilégio.'}


class STRIDEEngine:
    def __init__(self):
        self.ameacas = THREATS
        self.CONTRAMEDIDAS = CONTRAMEDIDAS

    def aplicar_stride(self, componente):
        return self.ameacas.get(componente, ["Unknown"])

    def analisar_todos(self, componentes):
        resultado = {}
        for componente in componentes:
            ameacas = self.aplicar_stride(componente)
            resultado[componente] = {
                "ameacas": ameacas,
                "contramedidas": [self.CONTRAMEDIDAS[a] for a in ameacas if a in self.CONTRAMEDIDAS]
            }
        return resultado


if __name__ == "__main__":
    stride = STRIDEEngine()
    componentes = ['AI Service', 'API Gateway', 'Auth', 'Backend', 'Cache', 'Configuration', 'Database', 'Firewall', 'Frontend', 'Game Server', 'Load Balancer', 'Macine Learning', 'Messaging', 'Networking', 'Remote Access', 'Search', 'Storage', 'User', 'VPC', 'Workflow Engine']

    relatorio = stride.analisar_todos(componentes)

    for comp, data in relatorio.items():
        print(f"Componente: {comp}")
        print("Ameaças:")
        for a in data["ameacas"]:
            print(f" - {a}")
        print("Contramedidas:")
        for c in data["contramedidas"]:
            print(f"   * {c}")
        print("---------------------------")