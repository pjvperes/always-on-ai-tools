import requests
import os
import sys
import json
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env se existir
load_dotenv()

HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")

# Verificar se a chave da API está definida
if not HUBSPOT_API_KEY:
    print("❌ Erro: HUBSPOT_API_KEY não está definida como variável de ambiente.")
    print("Para resolver isso, você pode:")
    print("1. Exportar como variável de ambiente: export HUBSPOT_API_KEY='sua_chave_aqui'")
    print("2. Criar um arquivo .env com: HUBSPOT_API_KEY=sua_chave_aqui")
    sys.exit(1)

# URL da API do HubSpot para contatos
HUBSPOT_CONTACTS_URL = 'https://api.hubapi.com/crm/v3/objects/contacts'

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {HUBSPOT_API_KEY}'
}

def get_contacts():
    """
    Recupera todos os contatos do CRM HubSpot
    """
    try:
        # Parâmetros para buscar as propriedades desejadas
        params = {
            'properties': 'firstname,lastname,jobtitle,company',
            'limit': 100  # Máximo de contatos por página
        }
        
        all_contacts = []
        after = None
        
        while True:
            if after:
                params['after'] = after
            
            response = requests.get(HUBSPOT_CONTACTS_URL, headers=HEADERS, params=params)
            
            if response.status_code == 200:
                data = response.json()
                contacts = data.get('results', [])
                all_contacts.extend(contacts)
                
                # Verificar se há mais páginas
                paging = data.get('paging', {})
                if 'next' in paging:
                    after = paging['next']['after']
                else:
                    break
            elif response.status_code == 401:
                print("❌ Erro de autenticação: Verifique se a HUBSPOT_API_KEY está correta")
                return []
            else:
                print(f"❌ Erro ao buscar contatos: {response.status_code} - {response.text}")
                return []
                
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão: {e}")
        return []
    
    return all_contacts

def format_contacts_json(contacts):
    """
    Formata os contatos em uma estrutura JSON limpa
    """
    formatted_contacts = []
    
    for contact in contacts:
        properties = contact.get('properties', {})
        
        # Extrair dados com valores padrão se não existirem
        firstname = properties.get('firstname', '')
        lastname = properties.get('lastname', '')
        nome_completo = f"{firstname} {lastname}".strip()
        cargo = properties.get('jobtitle', 'Não informado')
        empresa = properties.get('company', 'Não informado')
        
        # Garantir que nome completo não fique vazio
        if not nome_completo:
            nome_completo = 'Nome não informado'
        
        contact_data = {
            "nome": nome_completo,
            "cargo": cargo,
            "empresa": empresa
        }
        
        formatted_contacts.append(contact_data)
    
    return {
        "total_contatos": len(formatted_contacts),
        "contatos": formatted_contacts
    }

def main():
    """
    Função principal
    """
    print("🔍 Buscando contatos no HubSpot CRM...")
    contacts = get_contacts()
    
    if not contacts:
        result = {
            "total_contatos": 0,
            "contatos": []
        }
    else:
        result = format_contacts_json(contacts)
    
    # Retornar resultado em JSON
    json_output = json.dumps(result, indent=2, ensure_ascii=False)
    print("\n📋 Dados dos contatos em JSON:")
    print(json_output)
    
    return result

if __name__ == '__main__':
    main() 