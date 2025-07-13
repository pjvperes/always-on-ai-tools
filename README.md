# 🧠 Always On AI - Backend API

## 🔧 Backend para AI Tools

**API backend em FastAPI** que fornece acesso programático a dados do HubSpot e Notion para alimentar sistemas de IA conversacional. Processa consultas contextuais e retorna respostas enriquecidas com dados empresariais em tempo real.

---

## 🚀 Endpoints Disponíveis

### 📊 `/verify-data` - Verificação de Dados

Valida informações mencionadas em conversas com dados reais do CRM.

**Método:** `POST`  
**Payload:**
```json
{
  "context": "Contexto da conversa atual",
  "prompt": "Pergunta ou afirmação a ser verificada"
}
```

**Funcionalidade:**
- Busca deals ativos no HubSpot CRM
- Compara dados mencionados com informações reais
- Corrige afirmações incorretas automaticamente
- Retorna resposta contextualizada via GPT-4
- É acionada quando um dado é citado. Se o dado estiver incorreto, ela faz a correção. Caso o dado esteja correto, ele deixa a conversa rolar.
---

### 🎯 `/dashboard/data` - Análise de Market Fit

Fornece insights sobre adequação produto-mercado baseado em dados da nossa base de clientes (Hubspot CRM) e documentações internas sobre produto, marketing, estratégia e etc que estejam disponíveis no Notion.

**Método:** `POST`  
**Payload:**
```json
{
  "context": "Contexto da análise",
  "prompt": "Pergunta sobre market fit ou estratégia"
}
```

**Funcionalidade:**
- Analisa base de contatos do HubSpot
- Extrai informações de produto e marketing do Notion
- Gera insights sobre segmentação e market fit
- Retorna análise completa + dados brutos

---

## 🔌 Integrações

### HubSpot CRM
- **Deals:** Nome, valor, estágio, data de fechamento e etc.
- **Contatos:** Nome, segmento da empresa, número de funcionários e etc.
- **API Rate Limiting:** Implementado com delays entre requests

### Notion
- **Extração de conteúdo:** Páginas completas com blocos aninhados
- **Processamento de rich text:** Formatação preservada
- **Suporte a tabelas:** Dados estruturados convertidos para texto

### OpenAI
- **Modelo:** GPT-4.1-mini
- **Temperatura:** Configurável por endpoint
- **Context Engineering:** Prompts otimizados para cada caso de uso

---

## ⚙️ Configuração

### Variáveis de Ambiente
```env
HUBSPOT_API_KEY=your_hubspot_key
OPENAI_API_KEY=your_openai_key
NOTION_API_KEY=your_notion_key
```

### Execução
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar servidor
python app.py
# ou
uvicorn app:app --host 0.0.0.0 --port 3001
```

---

## 🛠️ Arquitetura Técnica

### Stack
- **Framework:** FastAPI
- **HTTP Client:** httpx (async)
- **Integrações:** hubspot-api-client, notion-client, openai
- **Validação:** Pydantic models

### Características
- **Assíncrono:** Requests paralelos para melhor performance
- **Error Handling:** Tratamento robusto de falhas de API
- **Type Safety:** Validação de schemas com Pydantic
- **Rate Limiting:** Respeita limites das APIs externas

---

## 📋 Dependências

```
fastapi
pydantic
python-dotenv
httpx
requests
notion-client
openai
uvicorn
```

