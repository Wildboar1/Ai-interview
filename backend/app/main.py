import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Simple health check
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Placeholder for LiveKit WebSocket bridge (to be implemented)
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_text()
            # Echo back for now
            await ws.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        pass
