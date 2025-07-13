# 🧠 Always On AI

## 🧐 O que é?

**Always On AI** é um sistema de IA que participa de todas as reuniões da empresa, age como um **sócio digital inteligente**, e transforma cada conversa em **decisões mais rápidas, embasadas e produtivas**.

Não é só mais um *notetaker*. Ele entende o que está sendo falado, **busca dados internos e externos em tempo real**, e pode agir por conta própria para **acelerar decisões, corrigir erros e gerar insights de impacto**.

---

## 🔧 Dois Modos de Operação

### 🧑‍💼 1. Assistant Mode (Precisa ser acionada)

~ Durante discussão para decisão estratégica.
> “Hey Sócio, o que acha sobre isso?”

Nesse modo, a IA é **ativada por uma frase** e pode responder a qualquer pergunta com base no **contexto da reunião e nos dados da empresa**.

#### Como funciona:

- Escuta ativa com buffer de 5 minutos  
- Frase de ativação → `"Fala Sócio"`  
- Abre sessão via WebSocket (Speech to Speech) 
- Acessa dados internos (CRM, Docs, etc.)  
- Responde por voz e fecha sessão automaticamente  

#### Exemplo real:

Suponha que estamos discutindo qual oferta será feita para a audiência do Adapta Summit. Ou seja, qual o melhor produto e melhor pitch a ser feito. 

> “Fala sócio, o que acha sobre isso?”

A IA já tem o contexto do que está sendo discutido, acessa **HubSpot (CRM)** para entender o público do evento, mapeia as principais dores daquela persona, confere documentações sobre seus produtos no Notion, e dá a **resposta final para decisão em segundos com insights valiosos**.

---

### ⚡ 2. Proactive Triggers (Gatilhos proativos)

> A IA entra na conversa **mesmo sem ser chamada**.

Ela detecta **palavras-chave importantes**, valida se é o momento certo de agir, e **age proativamente** trazendo **informações, alertas ou correções**.

#### Como funciona:

- Escaneia tudo que está sendo dito (<10ms)  
- Detecta keywords relevantes  
- Valida com LLM se é útil agir  
- Executa ação (dados, API, cálculo)  
- Fala com naturalidade no momento certo e em real-time. 

#### Exemplo:

Alguém do comercial diz: 
> “... creio que empresas de tecnologia representam muito pouco do nosso faturamento.”

→ A IA confere o CRM, analisa esse dado e responde:

> “Na verdade, empresas de tecnologia representam 33%, o que é uma parcela expressiva.”

---

## 🚀 Diferenciais do Produto

- ✅ **Contexto sempre presente**: Recentemente, muito tem se falado sobre **Context Engineering**.
- 🔌 **Integração plug-and-play**: a AlwaysOn só precisa ser configurada 1x, minimizando a fricção de uso por usuários.
- 🔁 **Atuação reativa + proativa**  
- 💸 **Redução extrema de custo por sessão** (de ~US$300/h para ~US$3/h): A arquitetura combina Text-to-Speech (TTS) com Speech-to-Speech, otimizando custos ao manter a IA principalmente em modo de escuta e falando apenas quando necessário.
- 📈 **Base escalável** com foco em multi-times, multi-canais e multi-setores  

---

## 🔭 Roadmap de Evolução

### ✅ Já entregue:

- IA funcional  
- Modo reativo e proativo  
- Integrações com HubSpot (CRM) + Notion (Docs internas)
- Arquitetura de custo otimizado  

### 🔜 Próximas etapas:

- Autenticação e suporte multi-equipe  
- Novas integrações: Google Meet, Slack, Teams...  
- Analytics de produtividade  
- Dashboard executivo  
- Suporte multimodal (vídeo, docs, tela...)  
- Workflows customizados por setor  
- Marketplace de agentes especializados  

---

