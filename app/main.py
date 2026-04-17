import os
import httpx
import tempfile
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class AnalyzeRequest(BaseModel):
    song_id: str
    signed_file_url: str

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    try:
        # Download audio file
        async with httpx.AsyncClient() as client:
            response = await client.get(request.signed_file_url)
            response.raise_for_status()
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(response.content)
            tmp_path = tmp.name
        
        try:
            # Placeholder analysis - will integrate Essentia later
            return {
                "song_id": request.song_id,
                "bpm": 120.0,
                "key": "C",
                "scale": "major",
                "energy": 0.85,
                "danceability": 0.72,
                "intensity": 0.65,
                "duration": 180.5
            }
        finally:
            os.unlink(tmp_path)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
