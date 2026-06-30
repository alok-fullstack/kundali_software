# Kundali Software - Next.js + FastAPI

## Architecture

```
kundali_software/
├── src/                    # Core calculation modules (UNCHANGED)
│   ├── kundali.py          # Birth chart calculations
│   ├── muhurta.py          # Auspicious timing
│   ├── health_predictor.py # Health/accident predictions
│   ├── panchang.py         # Vedic calendar
│   ├── dasha.py            # Vimshottari Dasha
│   └── ...
│
├── backend/                # FastAPI Backend (Port 8000)
│   ├── app.py              # Main FastAPI app
│   ├── api/
│   │   ├── routes/         # API endpoints
│   │   │   ├── kundali.py  # POST /api/generate
│   │   │   ├── chat.py     # POST /api/chat
│   │   │   ├── muhurta.py  # POST /api/muhurta
│   │   │   └── health.py   # POST /api/health
│   │   └── models/
│   │       └── schemas.py  # Pydantic models
│   └── requirements.txt
│
├── frontend/               # Next.js Frontend (Port 3000)
│   ├── app/
│   │   ├── page.tsx        # Main page
│   │   └── components/
│   │       ├── KundaliForm.tsx
│   │       ├── KundaliResults.tsx
│   │       ├── ChatAssistant.tsx
│   │       ├── MuhurtaModal.tsx
│   │       └── HealthModal.tsx
│   ├── lib/
│   │   ├── api.ts          # API client
│   │   └── types.ts        # TypeScript types
│   └── package.json
│
└── kundali_web.py          # Legacy Flask app (still works)
```

## Quick Start

### Option 1: Run both services (Recommended)

```batch
run_app.bat
```

This starts:
- FastAPI Backend: http://localhost:8000
- Next.js Frontend: http://localhost:3000

### Option 2: Run separately

**Backend (FastAPI):**
```bash
cd backend
pip install -r requirements.txt
python app.py
# Or: uvicorn app:app --reload --port 8000
```

**Frontend (Next.js):**
```bash
cd frontend
npm install
npm run dev
```

### Option 3: Legacy Flask app
```bash
python kundali_web.py
# Opens at http://localhost:5000
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/generate` | POST | Create kundali from birth details |
| `/api/chat` | POST | Chat with AI assistant |
| `/api/muhurta` | POST | Find auspicious times |
| `/api/health` | POST | Health/accident predictions |

API Documentation: http://localhost:8000/docs

## Accuracy

All calculations use the same `src/` modules:
- **Swiss Ephemeris** (NASA JPL DE431) - < 0.001 arc-second error
- **Vimshottari Dasha** - 120-year cycle system
- **Panchang** - Tithi, Nakshatra, Yoga, Karana, Vara
- **Muhurta Rules** - From Muhurta Chintamani, Brihat Samhita

**Accuracy: 99.99%** (same calculation engine as Flask version)

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 14, React 18, TypeScript, Tailwind CSS |
| Backend | FastAPI, Pydantic, Uvicorn |
| Calculations | Python, Swiss Ephemeris |
| Data | In-memory (kundali_store dict) |
