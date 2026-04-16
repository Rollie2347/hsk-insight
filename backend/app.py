from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

from chain import get_wallet_data
from ai import analyze_wallet, chat_about_wallet

app = FastAPI(title="HSK Insight", description="AI-Powered HashKey Chain Wallet Analytics")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = Path(__file__).parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

@app.get("/")
async def root():
    return FileResponse(str(FRONTEND_DIR / "index.html"))

class WalletRequest(BaseModel):
    address: str
    testnet: bool = False

class ChatRequest(BaseModel):
    address: str
    testnet: bool = False
    message: str
    history: List[dict] = []

wallet_cache = {}

@app.post("/api/analyze")
async def analyze(req: WalletRequest):
    try:
        data = get_wallet_data(req.address, req.testnet)
        wallet_cache[req.address] = data
        analysis = analyze_wallet(data)
        return {"success": True, "wallet": data, "analysis": analysis}
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=f"Chain connection error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/chat")
async def chat(req: ChatRequest):
    try:
        data = wallet_cache.get(req.address) or get_wallet_data(req.address, req.testnet)
        wallet_cache[req.address] = data
        reply = chat_about_wallet(data, req.history, req.message)
        return {"success": True, "reply": reply}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "HSK Insight"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)
