# Always-On AI Tools

API unificada que combina dados do HubSpot e Notion com processamento via LLM para análises inteligentes.

## 🚀 Funcionalidades

- **Integração HubSpot**: Busca contatos com informações relevantes
- **Integração Notion**: Extrai texto da página do produto Adapta AI
- **Processamento LLM**: Usa OpenAI GPT-3.5-turbo para análises contextuais
- **API POST**: Recebe context e prompt para análises personalizadas

## 📋 Requisitos

- Python 3.8+
- Variáveis de ambiente configuradas:
  - `HUBSPOT_API_KEY`
  - `NOTION_API_KEY`
  - `OPENAI_API_KEY`

## 🔧 Instalação

```bash
pip install -r requirements.txt
```

## 🎯 Uso

### Executar o servidor:
```bash
python hubspot_get_contacts.py
```

### Fazer requisições POST:

```bash
curl -X POST http://localhost:8000/dashboard/data \
  -H "Content-Type: application/json" \
  -d '{
    "context": "Análise de leads",
    "prompt": "Identifique os 3 leads mais promissores"
  }'
```

### Exemplo com Python:
```python
import requests

response = requests.post("http://localhost:8000/dashboard/data", json={
    "context": "Estou analisando leads potenciais para o produto Adapta AI",
    "prompt": "Com base nos dados de contatos do HubSpot e nas informações do produto, identifique os 3 leads mais promissores e sugira uma estratégia de abordagem para cada um."
})

data = response.json()
print(data["llm_response"])
```

## 📊 Resposta da API

```json
{
  "llm_response": "Análise gerada pela LLM com base nos dados...",
  "hubspot_contacts": [...],
  "notion_page_text": "Conteúdo da página Notion..."
}
```

## 🔍 Exemplos de Prompts

1. **Análise de segmentos**: "Quais são os segmentos de empresa mais representados nos nossos contatos?"
2. **Estratégia de marketing**: "Que tipo de conteúdo seria mais eficaz para cada segmento?"
3. **Qualificação de leads**: "Identifique contatos que seriam um bom fit para o produto B2B"

## 🛠️ Desenvolvimento

Para testar localmente, execute:
```bash
python api_example.py
```

## 📝 Estrutura do Projeto

```
├── hubspot_get_contacts.py  # API principal
├── requirements.txt         # Dependências
├── api_example.py          # Exemplo de uso
└── README.md               # Este arquivo
```

## 🔐 Configuração das Variáveis

Crie um arquivo `.env` na raiz do projeto:

```env
HUBSPOT_API_KEY=your_hubspot_key_here
NOTION_API_KEY=your_notion_key_here
OPENAI_API_KEY=your_openai_key_here
```

## 📚 Documentação da API

Acesse `http://localhost:8000/docs` para ver a documentação automática do FastAPI. 