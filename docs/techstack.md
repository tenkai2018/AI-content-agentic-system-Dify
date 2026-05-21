# Tech Stack & Setup (Clean UTF-8)

## 1. Technology Stack

### Backend / Orchestration
- Python 3.11+
- FastAPI
- LangGraph
- LangChain adapters (OpenAI / Anthropic / Ollama)
- SQLAlchemy

### Data & Memory
- PostgreSQL (task persistence)
- ChromaDB (optional long-term memory)
- File-based knowledge (`knowledge/project_context.md`, `knowledge/workflows`, `knowledge/skills`)

### Frontend
- Next.js (App Router)
- React + TypeScript
- CSS Modules

### Video Layer
- Remotion + React
- Manifest-driven scenes
- Per-scene audio + global BGM

### Infrastructure
- Docker Compose
  - Postgres
  - ChromaDB
  - n8n

## 2. Environment Requirements
- Python 3.11+
- Node.js 18+
- Docker Desktop
- Git

## 3. Setup (Recommended)

### Backend
```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host localhost --port 8080
```

### Frontend
```powershell
cd frontend
npm install
npm run dev
```

### Remotion
```powershell
cd remotion_app
npm install
npm run dev
```

### Infrastructure
```powershell
docker compose up -d
```

## 4. Runtime Notes
- N?u `npm` không n?m trong PATH c?a agent, dùng absolute path (ví d? NVM):
  - `C:\nvm4w\nodejs\npm.cmd run lint`
- N?u `backend/venv` l?i interpreter path, recreate venv.

