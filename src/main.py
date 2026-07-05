from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from .agent import run_agent

load_dotenv()

app = FastAPI(title="Safe SQL AI - Backend API")

# Permitir CORS para la UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.post("/api/query")
async def process_query(request: QueryRequest):
    if not request.question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
        
    # Verificar si el token está configurado
    if not os.getenv("HF_TOKEN"):
        raise HTTPException(status_code=500, detail="HF_TOKEN not configured in environment")
        
    answer = run_agent(request.question)
    
    return {
        "question": request.question,
        "answer": answer
    }

# Montar el frontend estático
if os.path.exists("frontend"):
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
