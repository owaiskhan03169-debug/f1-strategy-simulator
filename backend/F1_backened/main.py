import safety_car
import asyncio
import json
import random
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI(title="Race Simulator Telemetry API")

# Basic health check route
@app.get("/")
async def root():
    return {"status": "online", "message": "Telemetry API is running perfectly."}

# --- JSON API Endpoints for Reporting (Abdul's request) ---

@app.get("/api/race-results")
async def get_race_results():
    return {
        "session": "Main Race",
        "winner": "Car 1",
        "fastest_lap": "1:28.145",
        "weather": "Dry"
    }

@app.get("/api/telemetry/snapshot")
async def get_telemetry_snapshot():
    return {
        "lap_time": "1:30.221",
        "tyre_wear_percent": { "FL": 24.5, "FR": 25.1, "RL": 28.0, "RR": 27.5 },
        "fuel_kg": 45.2,
        "ers_battery_percent": 82.0
    }

@app.get("/api/safety-car")
async def get_safety_car_status():
    return {
        "is_deployed": False,
        "laps_remaining": 0,
        "impact_on_strategy": "None"
    }

@app.get("/api/endpoints")
async def get_endpoints_list():
    return {
        "live_telemetry_websocket": "wss://[YOUR_RENDER_URL]/ws", 
        "race_results": "GET /api/race-results",
        "telemetry_snapshot": "GET /api/telemetry/snapshot",
        "safety_car": "GET /api/safety-car"
    }

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