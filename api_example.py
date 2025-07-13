import requests
import json

# Configuração da API
API_URL = "http://localhost:8000/dashboard/data"

# Exemplo de uso da nova API POST
def call_dashboard_api():
    # Dados da requisição
    request_data = {
        "context": "Estou analisando leads potenciais para o produto Adapta AI",
        "prompt": "Com base nos dados de contatos do HubSpot e nas informações do produto, identifique os 3 leads mais promissores e sugira uma estratégia de abordagem para cada um."
    }
    
    # Fazer a requisição POST
    response = requests.post(API_URL, json=request_data)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Resposta da LLM:")
        print(data["llm_response"])
        print("\n" + "="*50 + "\n")
        print(f"📊 Total de contatos HubSpot: {len(data['hubspot_contacts'])}")
        print(f"📄 Texto da página Notion: {len(data['notion_page_text'])} caracteres")
    else:
        print(f"❌ Erro: {response.status_code}")
        print(response.text)

# Exemplo de diferentes tipos de prompts
def example_prompts():
    examples = [
        {
            "context": "Análise de vendas",
            "prompt": "Quais são os segmentos de empresa mais representados nos nossos contatos?"
        },
        {
            "context": "Estratégia de marketing",
            "prompt": "Com base no produto Adapta AI, que tipo de conteúdo seria mais eficaz para cada segmento de contatos?"
        },
        {
            "context": "Qualificação de leads",
            "prompt": "Identifique contatos que seriam um bom fit para o produto B2B da Adapta AI"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n📝 Exemplo {i}:")
        print(f"Context: {example['context']}")
        print(f"Prompt: {example['prompt']}")
        print("-" * 50)

if __name__ == "__main__":
    print("🚀 Exemplo de uso da API Dashboard com LLM")
    print("="*50)
    
    # Mostrar exemplos de prompts
    example_prompts()
    
    # Fazer uma chamada de exemplo
    print("\n🔄 Fazendo chamada para a API...")
    call_dashboard_api() 