# StrideGenAI

StrideGenAI é uma solução baseada em inteligência artificial generativa para análise de ameaças em aplicações, utilizando modelos de linguagem avançados e integração com Azure OpenAI. O backend permite o envio de imagens de diagramas e informações da aplicação, retornando um modelo de ameaças STRIDE detalhado, sugestões de melhoria e diagrama mermaidjs.

## Funcionalidades

- Análise automática de diagramas de arquitetura via IA
- Geração de modelo de ameaças STRIDE específico para cada aplicação
- Sugestões para aprimorar o modelo de ameaças
- Diagrama mermaidjs para visualização das relações entre ameaças e componentes
- API REST para integração fácil

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/hsouzaeduardo/challange-FIAP04.git
   cd StrideGenAI/backend
   ```

2. Crie um arquivo `.env` com as variáveis:
   ```
   ENDPOINT_URL=<seu-endpoint-azure-openai>
   DEPLOYMENT_NAME=<nome-do-deployment>
   AZURE_OPENAI_API_KEY=<sua-chave-azure-openai>
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

Execute o backend FastAPI:
```bash
uvicorn main:app --reload
```

Envie uma requisição para `/analyze-image/` com:
- Imagem do diagrama
- Informações da aplicação (tipo, autenticação, exposição, dados sensíveis, descrição)

Exemplo de uso via cURL:
```bash
curl -X POST "http://localhost:8000/analyze-image/" \
  -F "file=@seudiagrama.png" \
  -F "tipo_aplicacao=WebApp" \
  -F "autenticacao=OAuth2" \
  -F "acesso_internet=Sim" \
  -F "dados_sensiveis=Sim" \
  -F "descricao_aplicacao=Aplicação para gestão de usuários"
```

## Estrutura

```
StrideGenAI/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── index.html

```

## Como executar o frontend

Basta abrir o arquivo `index.html` diretamente no seu navegador.  
Não é necessário instalar Node.js ou qualquer outro servidor — o frontend funciona apenas com HTML, CSS e JavaScript

## Contribuição

1. Fork este repositório
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas alterações (`git commit -am 'Nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request


## Licença

MIT License

## Contato

Dúvidas ou sugestões? Abra uma issue ou envie um e-mail para [hsouza.eduardo@gmail.com](mailto:hsouza.eduardo@gmail.com).