# F1 Strategy Simulator

This repository contains:

- `frontend/`: Vite + React telemetry dashboard
- `backend/`: FastAPI telemetry + `/ws` + `/ai-insight`
- `integration/`: separate analytics service (does **not** provide `/ai-insight`)

For the hosted frontend, point it at the `backend/` deployment (not `integration/`), because the dashboard needs both `/ws` and `/ai-insight`.

## Local development

### 1) Run backend (`backend/`)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Optional:

```powershell
$env:GROQ_API_KEY="your-key"
```

### 2) Run frontend (`frontend/`)

Create `frontend/.env.local`:

```env
VITE_BACKEND_URL=http://localhost:8000
# Optional override. If omitted, frontend derives ws://localhost:8000/ws from VITE_BACKEND_URL
VITE_TELEMETRY_WS_URL=ws://localhost:8000/ws
```

Then run:

```powershell
cd frontend
npm ci
npm run dev
```

## Hosted/Vercel deployment configuration

Set these environment variables in the Vercel project for the frontend:

- `VITE_BACKEND_URL=https://<your-backend-origin>`
- Optional: `VITE_TELEMETRY_WS_URL=wss://<your-backend-origin-with-ws-path>/ws`

Notes:

1. If `VITE_TELEMETRY_WS_URL` is not set, the frontend derives it from `VITE_BACKEND_URL`:
   - `https://...` -> `wss://.../ws`
   - `http://...` -> `ws://.../ws`
2. Vite `VITE_*` variables are injected at build time. After changing them in Vercel, you must redeploy for changes to take effect.
3. Ensure your backend deployment exposes:
   - `POST /ai-insight`
   - `GET /` (health check)
   - `WS /ws`

## Backend CORS for hosted frontend

`backend/main.py` supports:

- `CORS_ALLOW_ORIGINS=*` (default)
- or a comma-separated allowlist, for example:
  - `CORS_ALLOW_ORIGINS=https://f1-strategy-simulator-ten.vercel.app,https://preview.example.vercel.app`

Use an allowlist in production when possible.
