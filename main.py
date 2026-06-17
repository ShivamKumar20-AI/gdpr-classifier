from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, validator
from classifier import classify
import logging
import sqlite3
import datetime
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Database setup ---
DB_PATH = "requests.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS classifications (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp   TEXT,
            input_text  TEXT,
            request_type TEXT,
            gdpr_article TEXT,
            action      TEXT,
            priority    TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_to_db(input_text, result):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO classifications
        (timestamp, input_text, request_type, gdpr_article, action, priority)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.datetime.utcnow().isoformat(),
        input_text,
        result["request_type"],
        result["gdpr_article"],
        result["action"],
        result["priority"]
    ))
    conn.commit()
    conn.close()

# --- App setup ---
app = FastAPI(
    title="GDPR Request Classifier",
    description="Classifies data subject requests and maps them to the relevant GDPR article.",
    version="1.2.0"
)

init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# --- Models ---
class RequestInput(BaseModel):
    text: str

    @validator("text")
    def text_must_not_be_empty(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Request text cannot be empty.")
        if len(v) < 5:
            raise ValueError("Request text is too short to classify.")
        if len(v) > 5000:
            raise ValueError("Request text exceeds the 5000 character limit.")
        return v

class ClassificationResult(BaseModel):
    request_type: str
    gdpr_article: str
    action: str
    priority: str

# --- Routes ---
@app.get("/", tags=["Frontend"])
def serve_frontend():
    return FileResponse("static/index.html")

@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}

@app.post("/classify", response_model=ClassificationResult, tags=["Classify"])
def classify_request(input: RequestInput):
    try:
        logger.info(f"Classifying: {input.text[:80]}...")
        result = classify(input.text)
        log_to_db(input.text, result)
        return result
    except Exception as e:
        logger.error(f"Classification failed: {e}")
        raise HTTPException(status_code=500, detail="Classification failed.")

@app.get("/history", tags=["History"])
def get_history(limit: int = 20):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM classifications ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]