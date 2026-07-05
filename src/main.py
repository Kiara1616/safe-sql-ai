from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from .agent import run_agent

load_dotenv()

app = FastAPI(title="Safe SQL AI - Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str
    provider: str = "mock"

@app.post("/api/query")
async def process_query(request: QueryRequest):
    if not request.question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
        
    try:
        answer, sql, data = run_agent(request.question, request.provider)
        return {
            "question": request.question,
            "answer": answer,
            "sql": sql,
            "data": data,
            "provider": request.provider
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if os.path.exists("frontend"):
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
