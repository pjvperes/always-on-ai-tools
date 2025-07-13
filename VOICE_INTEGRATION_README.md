# Voice Assistant Integration - Product Market Fit Tool

Integração completa do Product Market Fit Tool no sistema de assistente de voz com **Proactive Triggers** e **Realtime API**.

## 📋 Arquivos Criados

### 1. **Proactive Trigger System**
- `triggers/base.py` - Classe base para todos os triggers
- `triggers/builtin/product_market_fit_trigger.py` - Trigger personalizado para PMF
- `triggers/__init__.py` - Módulo de triggers
- `triggers/builtin/__init__.py` - Módulo de triggers built-in

### 2. **Realtime API Integration**
- `realtime/tools.py` - Ferramentas para o assistente
- `realtime/session_manager.py` - Gerenciador de sessões
- `realtime/__init__.py` - Módulo realtime

### 3. **Configuration & Main**
- `config.py` - Configurações do sistema
- `main.py` - Arquivo principal da aplicação
- `integration_requirements.txt` - Dependências necessárias

## 🚀 Configuração

### 1. Instalar Dependências

```bash
pip install -r integration_requirements.txt
```

### 2. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Product Market Fit API
PRODUCT_MARKET_FIT_API_URL=http://localhost:8000
PRODUCT_MARKET_FIT_ENABLED=true
PRODUCT_MARKET_FIT_TIMEOUT=30

# API Keys (necessárias para o PMF tool)
HUBSPOT_API_KEY=your_hubspot_key_here
NOTION_API_KEY=your_notion_key_here
OPENAI_API_KEY=your_openai_key_here

# Voice Assistant Configuration
DEFAULT_VOICE=alloy
DEFAULT_SPEED=1.0
VOICE_LANGUAGE=en-US

# Logging
LOG_LEVEL=INFO
LOG_TO_FILE=false
VERBOSE_LOGGING=true

# Performance
MAX_RESPONSE_TIME=30
CACHE_ENABLED=true
CACHE_TTL=300
```

### 3. Executar o Product Market Fit Tool

Primeiro, inicie o seu product market fit tool:

```bash
python product_market_fit_tool.py
```

## 🎯 Como Usar

### 1. **Proactive Triggers** (Sistema Reativo)

Inicie o sistema de triggers:

```bash
python main.py
```

**Palavras-chave que ativam o trigger:**
- "product market fit"
- "pmf analysis"
- "market analysis"
- "lead analysis"
- "hubspot analysis"
- "contact analysis"
- "business intelligence"
- "análise de mercado"
- "análise de leads"
- "inteligência de vendas"

**Exemplos de uso:**
```bash
# Análise geral
"Analyze product market fit for our leads"

# Análise de segmentos
"What segments are most promising in our database?"

# Análise de qualidade de leads
"Analyze our lead quality"

# Em português
"Faça uma análise de product market fit"
"Analise nossos leads do HubSpot"
```

### 2. **Realtime API** (Modo Assistente)

Para usar como ferramenta do assistente:

```python
from realtime.session_manager import SessionManager

# Criar sessão
session_manager = SessionManager()
session = session_manager.create_session("session_123")

# Chamar ferramenta
message = {
    "type": "tool_call",
    "tool_name": "product_market_fit_tool",
    "arguments": {
        "query": "Analyze our contact segments",
        "parameters": {
            "analysis_type": "segments",
            "context": "Análise de segmentação de mercado"
        }
    }
}

result = session_manager.handle_message("session_123", message)
```

### 3. **Modo Demo**

Para testar sem voz:

```bash
python main.py demo
```

## 🔧 Ferramentas Disponíveis

### 1. **product_market_fit_tool**
Ferramenta principal para análise de PMF

**Parâmetros:**
- `query`: Pergunta/solicitação do usuário
- `parameters`: Parâmetros opcionais
  - `analysis_type`: "segments", "lead_quality", "market_fit", "strategy"
  - `context`: Contexto da análise

### 2. **get_contact_segments**
Análise específica de segmentos de contatos

### 3. **get_lead_quality_analysis**
Análise de qualidade de leads

### 4. **get_market_fit_analysis**
Análise de product market fit

### 5. **get_marketing_strategy**
Recomendações de estratégia de marketing

## 📊 Exemplos de Análises

### Análise de Segmentos
```python
result = await product_market_fit_tool(
    "Analyze contact segments",
    {"analysis_type": "segments"}
)
```

### Análise de Qualidade de Leads
```python
result = await product_market_fit_tool(
    "Analyze lead quality",
    {"analysis_type": "lead_quality"}
)
```

### Estratégia de Marketing
```python
result = await product_market_fit_tool(
    "Develop marketing strategy",
    {"analysis_type": "strategy"}
)
```

## 🛠️ Personalização

### 1. **Adicionar Novas Palavras-chave**

Edite `triggers/builtin/product_market_fit_trigger.py`:

```python
keywords=[
    "product market fit", "pmf analysis", "market analysis",
    "sua nova palavra-chave aqui",
    # ... outras palavras-chave
]
```

### 2. **Configurar Novos Tipos de Análise**

Edite `realtime/tools.py`:

```python
def _refine_prompt_for_assistant(query: str, analysis_type: str) -> str:
    # Adicione novos tipos de análise
    if analysis_type == "seu_novo_tipo":
        return "Seu prompt personalizado aqui"
```

### 3. **Ajustar Configurações de Voz**

Edite `config.py`:

```python
VOICE_CONFIG = {
    "default_voice": "nova_voz",
    "default_speed": 1.2,
    "business_analysis_voice": {
        "voice": "alloy",
        "speed": 0.8  # Mais devagar para análises
    }
}
```

## 🔍 Debugging

### 1. **Logs Detalhados**

Configure no `.env`:
```env
LOG_LEVEL=DEBUG
VERBOSE_LOGGING=true
```

### 2. **Teste de API**

```bash
# Teste se a API está funcionando
curl -X POST http://localhost:8000/dashboard/data \
  -H "Content-Type: application/json" \
  -d '{
    "context": "Teste de integração",
    "prompt": "Análise rápida dos contatos"
  }'
```

### 3. **Teste de Triggers**

```python
python -c "
from main import VoiceAssistant
app = VoiceAssistant()
result = app.process_voice_input('analyze product market fit')
print(result)
"
```

## 📈 Performance

### 1. **Timeout Configuration**
- Trigger timeout: 30 segundos
- API timeout: 30 segundos
- Session timeout: 1 hora

### 2. **Caching**
- Cache habilitado por padrão
- TTL: 5 minutos
- Pode ser desabilitado no `.env`

### 3. **Rate Limiting**
- 60 requests por minuto
- 1000 requests por hora
- Configurável no `config.py`

## 🔐 Security

### 1. **API Keys**
- Todas as chaves são carregadas via variáveis de ambiente
- Nunca hardcode chaves no código

### 2. **CORS**
- Configurado para aceitar origens específicas
- Pode ser restringido no `config.py`

### 3. **Rate Limiting**
- Implementado por padrão
- Configurável por IP

## 🚨 Troubleshooting

### 1. **API não responde**
```bash
# Verifique se o product_market_fit_tool está rodando
curl http://localhost:8000/dashboard/data
```

### 2. **Trigger não ativa**
- Verifique se a palavra-chave está na lista
- Confirme que o trigger está habilitado no `config.py`
- Verifique os logs para erros

### 3. **Erro de configuração**
```python
from config import validate_config
validate_config()  # Mostra erros de configuração
```

## 📝 Próximos Passos

1. **Integrar com sistema de voz real**
2. **Adicionar mais triggers personalizados**
3. **Implementar cache Redis**
4. **Adicionar métricas e monitoring**
5. **Criar interface web para gerenciar triggers**

## 🤝 Contribuindo

1. Adicione novos triggers em `triggers/builtin/`
2. Teste com `python main.py demo`
3. Documente novas funcionalidades
4. Siga o padrão Conventional Commits

## 📚 Referências

- [Conventional Commits](https://www.conventionalcommits.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI Realtime API](https://platform.openai.com/docs/guides/realtime)
- [HubSpot API](https://developers.hubspot.com/docs/api/overview)
- [Notion API](https://developers.notion.com/) 