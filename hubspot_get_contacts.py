from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from typing import List
import os, time, requests

load_dotenv()
app = FastAPI()

BASE = "https://api.hubapi.com"

def get_token() -> str:
    token = os.getenv("HUBSPOT_API_KEY")
    if not token:
        raise HTTPException(status_code=500, detail="HUBSPOT_API_KEY não definido.")
    return token

@app.get("/contacts/summary")
def get_contacts_summary():
    headers = {
        "Authorization": f"Bearer {get_token()}",
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
        res = requests.get(f"{BASE}/crm/v3/objects/contacts", headers=headers, params=params)
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
