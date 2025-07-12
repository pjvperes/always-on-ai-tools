from fastapi import FastAPI
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")
HUBSPOT_API_URL = "https://api.hubapi.com/crm/v3/objects/deals"

class PromptRequest(BaseModel):
    prompt: str

@app.post("/deals/all")
async def get_all_deals(payload: PromptRequest):
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    params = {
        "properties": "dealname,amount,dealstage,closedate",
        "limit": 100,
        "archived": False
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(HUBSPOT_API_URL, headers=headers, params=params)

    if response.status_code != 200:
        return {"error": f"Failed to fetch deals: {response.text}"}

    all_deals = response.json().get("results", [])

    return {
        "prompt_received": payload.prompt,
        "all_deals": all_deals
    }
