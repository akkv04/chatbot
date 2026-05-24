from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .brain import brain
import os

import json

app = FastAPI(title="Chatbot API")

# Configure CORS
origins_str = os.getenv("CORS_ORIGINS", '["*"]')
try:
    origins = json.loads(origins_str)
except Exception:
    origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str
    sources: list[str]

@app.on_event("startup")
async def startup_event():
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    brain.index_documents(data_dir)

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        answer, sources = brain.ask(request.message)
        return ChatResponse(answer=answer, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}
