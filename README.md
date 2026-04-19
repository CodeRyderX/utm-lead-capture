# UTM Lead Capture API

A lightweight FastAPI service that receives form submissions from multiple sources, extracts UTM parameters, and stores structured lead data in Supabase — so you always know which campaign drove which lead.

## The Problem

Most form tools (Tally, Typeform, etc.) either drop UTM parameters or require paid plugins to capture them. When leads come in from multiple campaigns across multiple platforms, you lose visibility on what's actually working.

This API sits between your forms and your database, captures everything, and gives you a clean analytics endpoint to query by source and campaign.

## How It Works

```
Form submission (Tally + UTM params in URL)
        ↓
POST /webhook receives raw payload
        ↓
Parser normalises fields across form sources
        ↓
Supabase insert with source tag + UTM data
        ↓
GET /analytics returns lead counts by source
```

## Features

- Accepts webhooks from any form tool
- Extracts all 5 UTM parameters automatically
- Tags each submission by source (tally, typeform, etc.)
- `/analytics` endpoint returns lead counts grouped by source and campaign
- Easy to extend with new form parsers

## Tech Stack

- Python + FastAPI
- Supabase (PostgreSQL)
- Pydantic
- uvicorn

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/CodeRyderX/utm-lead-capture
cd utm-lead-capture
```

**2. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add environment variables**

Create a `.env` file:
```
SUPABASE_URL=your_project_url
SUPABASE_KEY=your_anon_key
```

**5. Create Supabase table**
```sql
create table leads (
  id uuid default gen_random_uuid() primary key,
  email text,
  name text,
  message text,
  utm_source text,
  utm_medium text,
  utm_campaign text,
  utm_content text,
  utm_term text,
  source_tag text,
  created_at timestamptz default now()
);
```

**6. Run the server**
```bash
uvicorn main:app --reload --port 8080
```

## API Endpoints

**Health check**
```
GET /health
→ {"status": "ok"}
```

**Receive webhook**
```
POST /webhook
Content-Type: application/json

{
  "data": {
    "fields": [
      {"label": "Name", "value": "John"},
      {"label": "Email", "value": "john@example.com"},
      {"label": "utm_source", "value": "instagram"},
      {"label": "utm_medium", "value": "social"},
      {"label": "utm_campaign", "value": "portfolio_launch"}
    ]
  }
}

→ {"message": "lead received"}
```

**Analytics**
```
GET /analytics
→ {
    "tally / instagram": 4,
    "tally / linkedin": 2,
    "tally / email": 1
  }
```

## Testing with a real form

Add UTM parameters to your Tally form URL:

```
https://tally.so/r/yourform?utm_source=instagram&utm_medium=social&utm_campaign=portfolio_launch
```

Then point your Tally webhook at `/webhook` using ngrok for local testing.