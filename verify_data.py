from fastapi import FastAPI
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

HUBSPOT_API_URL = "https://api.hubapi.com/crm/v3/objects/deals"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

class PromptRequest(BaseModel):
    context: str
    prompt: str

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
        # 1. Buscar dados do HubSpot
        response = await client.get(HUBSPOT_API_URL, headers=headers_hubspot, params=params)

        if response.status_code != 200:
            return {"error": f"Erro ao buscar deals: {response.text}"}

        deals = response.json().get("results", [])

        # 2. Formatar os dados para o prompt
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

        # 3. Chamar a OpenAI
        body = {
            "model": "gpt-4o",
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
