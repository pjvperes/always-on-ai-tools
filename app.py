from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import httpx
import os
import time
import requests
from typing import List, Dict, Any
from notion_client import Client
from openai import OpenAI

load_dotenv()

app = FastAPI(title="AI Tools API", version="1.0.0")

# Environment variables
HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NOTION_API_KEY = os.getenv("NOTION_API_KEY")

# API URLs
HUBSPOT_API_URL = "https://api.hubapi.com/crm/v3/objects/deals"
HUBSPOT_CONTACTS_URL = "https://api.hubapi.com/crm/v3/objects/contacts"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

# Models
class PromptRequest(BaseModel):
    context: str
    prompt: str

# ------------------- VERIFY DATA ENDPOINT -------------------

@app.post("/verify-data")
async def verify_data(payload: PromptRequest):
    headers_hubspot = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    headers_openai = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    params = {
        "properties": "dealname,amount,dealstage,closedate",
        "limit": 100,
        "archived": False
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        # Fetch HubSpot deals
        response = await client.get(HUBSPOT_API_URL, headers=headers_hubspot, params=params)

        if response.status_code != 200:
            return {"error": f"Erro ao buscar deals: {response.text}"}

        deals = response.json().get("results", [])

        # Format deals for prompt
        deals_text = "\n".join([
            f"- {d['properties'].get('dealname')} | {d['properties'].get('dealstage')} | R$ {d['properties'].get('amount')} | {d['properties'].get('closedate')}"
            for d in deals
        ])

        final_prompt = f"""
[Dados do CRM]
{deals_text}

[Contexto]
{payload.context}

[Prompt]
{payload.prompt}
        """

        # Call OpenAI
        body = {
            "model": "gpt-4.1-mini",
            "messages": [
                {"role": "system", "content": "Você é um assistente que ajuda a analisar dados de vendas. Se alguém citar um dado, você deve analisar os dados no Hubspot e corrigir imediatamente se estiver errado. Seja objetivo na correção e cite dados."},
                {"role": "user", "content": final_prompt}   
            ],
            "temperature": 0.5
        }

        response_llm = await client.post(OPENAI_API_URL, headers=headers_openai, json=body)

        if response_llm.status_code != 200:
            return {"error": f"Erro ao chamar LLM: {response_llm.text}"}

        llm_output = response_llm.json()["choices"][0]["message"]["content"]

        return {
            "response": llm_output
        }

# ------------------- PRODUCT MARKET FIT FUNCTIONS -------------------

def get_contacts_summary() -> List[Dict[str, Any]]:
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Accept": "application/json"
    }

    wanted_props = ["firstname", "lastname", "segmento_da_empresa", "numemployees"]
    params = {
        "limit": 100,
        "properties": ",".join(wanted_props),
        "archived": "false"
    }

    all_contacts = []
    while True:
        res = requests.get(HUBSPOT_CONTACTS_URL, headers=headers, params=params)
        if res.status_code != 200:
            raise HTTPException(status_code=res.status_code, detail=res.text)

        data = res.json()
        all_contacts.extend(data["results"])

        next_page = data.get("paging", {}).get("next")
        if not next_page:
            break
        params["after"] = next_page["after"]
        time.sleep(0.2)

    summary = []
    for c in all_contacts:
        p = c.get("properties", {})
        full_name = " ".join(filter(None, [p.get("firstname"), p.get("lastname")])).strip()
        summary.append({
            "id": c["id"],
            "nome": full_name or None,
            "segmento_da_empresa": p.get("segmento_da_empresa"),
            "numemployees": p.get("numemployees")
        })

    return summary

# ------------------- NOTION FUNCTIONS -------------------

def get_notion_client() -> Client:
    if not NOTION_API_KEY:
        raise HTTPException(status_code=500, detail="NOTION_API_KEY não definido.")
    return Client(auth=NOTION_API_KEY)

def extract_rich_text(rich_text_array: List[Dict[str, Any]]) -> str:
    if not rich_text_array:
        return ""
    text_parts = []
    for text_obj in rich_text_array:
        if text_obj.get("type") == "text":
            text_parts.append(text_obj.get("text", {}).get("content", ""))
        else:
            text_parts.append(text_obj.get("plain_text", ""))
    return "".join(text_parts)

def get_all_blocks(client: Client, page_id: str) -> List[Dict[str, Any]]:
    all_blocks = []
    start_cursor = None
    while True:
        response = client.blocks.children.list(block_id=page_id, start_cursor=start_cursor, page_size=100)
        blocks = response.get("results", [])
        all_blocks.extend(blocks)
        if not response.get("has_more", False):
            break
        start_cursor = response.get("next_cursor")
    return all_blocks

def extract_block_text(block: Dict[str, Any]) -> str:
    block_type = block["type"]
    if block_type not in block:
        return ""
    block_content = block[block_type]
    if "rich_text" in block_content:
        return extract_rich_text(block_content["rich_text"])
    elif "cells" in block_content:  # table_row
        return " | ".join([extract_rich_text(cell) for cell in block_content["cells"]])
    return ""

def get_page_text(page_id: str) -> str:
    client = get_notion_client()
    page_info = client.pages.retrieve(page_id)
    title = ""
    if "properties" in page_info:
        for prop_data in page_info["properties"].values():
            if prop_data["type"] == "title":
                title = extract_rich_text(prop_data.get("title", []))
                break
    blocks = get_all_blocks(client, page_id)
    text_parts = []
    if title:
        text_parts.append(title)
    for block in blocks:
        text = extract_block_text(block)
        if text.strip():
            text_parts.append(text)
    return "\n\n".join(text_parts)

# ------------------- LLM INTEGRATION -------------------

def get_openai_client() -> OpenAI:
    """Initialize OpenAI client"""
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY não definido.")
    return OpenAI(api_key=OPENAI_API_KEY)

def call_llm(context: str, prompt: str, hubspot_data: List[Dict[str, Any]], notion_text: str) -> str:
    """Call OpenAI LLM with the provided data"""
    client = get_openai_client()
    
    # Prepare the system message with all data
    system_message = f"""
    Seja um especialista em Marketing e Produto que está em uma reunião estratégica e tem acesso aos seguintes dados:
    
    CONTEXTO: {context}
    
    DADOS DO HUBSPOT (Contatos):
    {hubspot_data}
    
    DADOS DOS PRODUTO (Página Notion):
    {notion_text}
    
    Use essas informações para responder às solicitações do usuário de forma precisa e contextual.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao chamar LLM: {str(e)}")

# ------------------- PRODUCT MARKET FIT ENDPOINT -------------------

@app.post("/dashboard/data")
def get_dashboard_data(request: PromptRequest):
    try:
        # Fetch HubSpot contacts and Notion data
        hubspot_contacts = get_contacts_summary()
        notion_text = get_page_text("22f96f42586680eabeb1ddc80400c8a5")
        
        # Call LLM with the data
        llm_response = call_llm(
            context=request.context,
            prompt=request.prompt,
            hubspot_data=hubspot_contacts,
            notion_text=notion_text
        )
        
        return {
            "llm_response": llm_response,
            "hubspot_contacts": hubspot_contacts,
            "notion_page_text": notion_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar solicitação: {str(e)}")

# ------------------- MAIN -------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3001)