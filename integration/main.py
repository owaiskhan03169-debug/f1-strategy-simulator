import asyncio
import json
import random
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="Race Simulator Telemetry API")

# Serve frontend static assets if they exist (built Vite output)
frontend_dist = Path(__file__).resolve().parent.parent / 'frontend' / 'dist'
if frontend_dist.exists():
    app.mount('/', StaticFiles(directory=str(frontend_dist), html=True), name='frontend')

# Basic health check route (kept separate so static mount can serve the app at root)
@app.get('/health')
async def health():
    return {"status": "online", "message": "Telemetry API is running perfectly."}

# Real-time WebSocket endpoint
@app.websocket("/ws")
async def websocket_telemetry(websocket: WebSocket):
    await websocket.accept()
    print("Frontend client connected to telemetry stream!")
    try:
        while True:
            # Generating dummy telemetry data for testing
            telemetry_data = {
                "speed_kmh": random.randint(100, 330),
                "engine_rpm": random.randint(5000, 12500),
                "gear": random.randint(1, 8),
                "throttle_percent": round(random.uniform(0.0, 100.0), 1)
            }
            
            # Sending the data as a JSON string
            await websocket.send_text(json.dumps(telemetry_data))
            
            # Pause for 1 second before sending the next update
            await asyncio.sleep(1)
            
    except WebSocketDisconnect:
        print("Frontend client disconnected.")
