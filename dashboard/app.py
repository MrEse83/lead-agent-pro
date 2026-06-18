"""
app.py — Lead Agent Pro Dashboard
Multi-industry outreach platform.
Run: python dashboard/app.py
Open: http://localhost:8000
"""

import os
import sys

# Fix: add BOTH scripts/ and project root to path so all imports resolve
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "scripts"))
sys.path.insert(0, BASE_DIR)  # This is the key fix — email_sender.py lives here

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from db import get_connection
from dotenv import load_dotenv

load_dotenv(os.path.join(BASE_DIR, ".env"))  # Always load from project root

app = FastAPI()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

@app.get("/", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    status: str = "all",
    priority: str = "all",
    city: str = "all",
    industry: str = "all",
    msg: str = "",
):
    conn = get_connection()
    with conn.cursor() as cur:
        filters = ["1=1"]
        params = []
        if status != "all":
            filters.append("lead_status = %s"); params.append(status)
        if priority != "all":
            filters.append("priority = %s"); params.append(priority)
        if city != "all":
            filters.append("city = %s"); params.append(city)
        if industry != "all":
            filters.append("source LIKE %s"); params.append(f"serpapi_{industry}%")

        where = " AND ".join(filters)
        cur.execute(f"""
            SELECT id, name, city, category, phone, email, website,
                   whatsapp_number, has_whatsapp, has_chatbot,
                   instagram_handle, runs_ads,
                   automation_score, priority, lead_status,
                   ai_summary, score_reason,
                   outreach_email, outreach_whatsapp,
                   contacted_at, contact_channel, notes
            FROM leads
            WHERE {where}
            ORDER BY automation_score DESC NULLS LAST
            LIMIT 200
        """, params)
        leads = cur.fetchall()

        cur.execute("SELECT COUNT(*) as n FROM leads"); total = cur.fetchone()["n"]
        cur.execute("SELECT COUNT(*) as n FROM leads WHERE priority='hot'"); hot = cur.fetchone()["n"]
        cur.execute("SELECT COUNT(*) as n FROM leads WHERE lead_status='contacted'"); contacted = cur.fetchone()["n"]
        cur.execute("SELECT COUNT(*) as n FROM leads WHERE outreach_email IS NOT NULL AND contacted_at IS NULL"); ready = cur.fetchone()["n"]
        cur.execute("SELECT DISTINCT city FROM leads WHERE city IS NOT NULL ORDER BY city")
        cities = [r["city"] for r in cur.fetchall()]

        # Pull distinct industries from source column
        cur.execute("SELECT DISTINCT source FROM leads WHERE source IS NOT NULL ORDER BY source")
        industries = [
            r["source"].replace("serpapi_", "")
            for r in cur.fetchall()
            if r["source"].startswith("serpapi_")
        ]

    conn.close()
    return templates.TemplateResponse("dashboard.html", {
        "request": request, "leads": leads,
        "total": total, "hot": hot, "contacted": contacted, "ready": ready,
        "cities": cities, "industries": industries,
        "current_status": status, "current_priority": priority,
        "current_city": city, "current_industry": industry,
        "flash": msg,
    })


@app.post("/send-email/{lead_id}")
async def send_email(lead_id: int, custom_message: str = Form(default=None)):
    from email_sender import send_single
    try:
        success = send_single(lead_id, custom_message=custom_message)
        msg = "Email sent successfully!" if success else "Failed to send. Check GMAIL config in .env"
    except Exception as e:
        msg = f"Error: {str(e)}"
    return RedirectResponse(f"/?msg={msg}", status_code=303)


@app.post("/send-batch")
async def send_batch(limit: int = Form(default=30)):
    from email_sender import run_batch
    try:
        run_batch(limit=limit)
        msg = "Batch send complete. Check terminal for details."
    except Exception as e:
        msg = f"Batch failed: {str(e)}"
    return RedirectResponse(f"/?msg={msg}", status_code=303)


@app.post("/update-status/{lead_id}")
async def update_status(lead_id: int, status: str = Form(...)):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("UPDATE leads SET lead_status=%s WHERE id=%s", (status, lead_id))
    conn.commit(); conn.close()
    return RedirectResponse("/", status_code=303)


@app.post("/update-notes/{lead_id}")
async def update_notes(lead_id: int, notes: str = Form(...)):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("UPDATE leads SET notes=%s WHERE id=%s", (notes, lead_id))
    conn.commit(); conn.close()
    return RedirectResponse("/", status_code=303)


@app.post("/mark-contacted/{lead_id}")
async def mark_contacted_route(lead_id: int, channel: str = Form(...)):
    from datetime import datetime
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE leads SET
                lead_status='contacted', contacted_at=%s, contact_channel=%s
            WHERE id=%s
        """, (datetime.now(), channel, lead_id))
    conn.commit(); conn.close()
    return RedirectResponse("/", status_code=303)


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)