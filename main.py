from fastapi import FastAPI, Request
from supabase_client import supabase
from parsers import parse_tally_payload

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/webhook")
async def receive_webhook(request: Request):
    raw = await request.json()
    parsed = parse_tally_payload(raw)
    
    supabase.table("leads").insert(parsed).execute()
    
    return {"message": "lead received"}

@app.get("/analytics")
def analytics():
    response = supabase.table("leads").select("source_tag, utm_source").execute()
    
    data = response.data
    counts = {}
    
    for row in data:
        key = f"{row.get('source_tag')} / {row.get('utm_source')}"
        counts[key] = counts.get(key, 0) + 1
    
    return counts