"""
FastAPI Backend for Kundali Software

This is the main entry point for the FastAPI application.
It provides REST API endpoints for:
- Kundali generation
- Chat with AI assistant
- Muhurta (auspicious timing) calculations
- Health/Accident predictions

Run with:
    uvicorn backend.main:app --reload --port 8000

Or directly:
    python -m backend.main
"""

import os
import sys
from pathlib import Path

# Ensure parent directory is in path for src imports
parent_dir = Path(__file__).resolve().parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.routes import (
    kundali_router, chat_router, muhurta_router, health_router,
    matching_router, divisional_charts_router, panchang_router,
    pdf_router, numerology_router, rashifal_router, dosha_router,
    gemstone_router, career_router, remedies_router, prashna_router
)

# Create FastAPI app
app = FastAPI(
    title="Kundali Software API",
    description="""
## Vedic Astrology API

This API provides accurate Vedic astrological calculations based on:
- **Swiss Ephemeris** (NASA JPL DE431) for planetary positions
- **Vimshottari Dasha** system for timing predictions
- **Classical texts**: Brihat Parashara Hora Shastra, Muhurta Chintamani, etc.

### Features

1. **Kundali Generation** (`/api/generate`)
   - Complete birth chart with 9 planets
   - 12 house positions
   - Nakshatra details
   - Vimshottari Dasha periods

2. **AI Chat Assistant** (`/api/chat`)
   - Ask questions in Hindi/English
   - Career, Marriage, Health predictions
   - Dasha analysis
   - Remedies and lucky elements

3. **Muhurta Finder** (`/api/muhurta`)
   - Find auspicious times for events
   - Marriage, Career, Property, Travel
   - Panchang-based selection
   - Personal compatibility (Tarabala, Chandrabala)

4. **Health Predictions** (`/api/health`)
   - Accident-prone periods
   - Health risk analysis
   - Dasha and transit-based predictions
   - Remedies for vulnerable periods

5. **Kundali Matching** (`/api/match`)
   - Ashtakoot Milan (8-fold matching)
   - Total 36 Gunas analysis
   - Manglik, Nadi, Bhakoot Dosha detection
   - Detailed compatibility report with remedies

6. **Divisional Charts** (`/api/varga`)
   - All 16 Varga charts (D-1 to D-60)
   - Navamsa (D-9) analysis for marriage
   - Dasamsa (D-10) analysis for career
   - Vimshopaka Bala planetary strength

7. **Panchang** (`/api/panchang`)
   - Daily Panchang (Five Limbs)
   - Choghadiya (Day and Night)
   - Rahu Kaal, Yamaghantaka, Gulika Kaal
   - Sunrise/Sunset/Moonrise/Moonset
   - Auspicious time recommendations

8. **Numerology - Ank Jyotish** (`/api/numerology`)
   - Moolank (Root Number) from birth date
   - Bhagyank (Destiny Number) from full DOB
   - Namank (Name Number) - Chaldean & Pythagorean
   - Personality traits and life path
   - Lucky numbers, colors, days, gemstones
   - Name correction suggestions
   - Compatibility analysis
   - Business name analysis

9. **PDF Export** (`/api/kundali/{id}/pdf`, `/api/matching/pdf`)
   - Professional Kundali PDF reports
   - Marriage compatibility PDF reports
   - Bilingual (Hindi/English) format
   - Traditional Vedic styling with saffron theme
   - Charts, tables, yogas, doshas, remedies

10. **Rashifal - Daily Horoscope** (`/api/rashifal`)
    - Daily, Weekly, Monthly, Yearly predictions
    - Moon sign based (Gochar analysis)
    - Health, Career, Finance, Relationships
    - Lucky numbers, colors, days

11. **Dosha Analysis** (`/api/dosha`)
    - Kaal Sarp Dosha (12 types)
    - Pitra Dosha, Manglik Dosha
    - Sade Sati, Guru Chandal, Grahan Dosha
    - Severity assessment and remedies

12. **Gemstone Recommendations** (`/api/gemstone`)
    - Based on Ratna Shastra & Garuda Purana
    - Planet-gemstone mapping
    - Wearing instructions (weight, metal, finger, day)
    - Substitute gemstones

13. **Career & Finance** (`/api/career`)
    - 10th house and lord analysis
    - Dhana Yogas (wealth combinations)
    - Career recommendations by sign
    - Government/Business/Foreign career yogas

14. **Vedic Remedies** (`/api/remedies`)
    - Planet-specific remedies (mantras, gems, charity)
    - Dosha remedies from BPHS
    - Lal Kitab practical remedies
    - Daily/Weekly/Monthly routines

15. **Prashna Kundali** (`/api/prashna`)
    - Horary Astrology based on Prashna Marga
    - Question-specific analysis
    - Timing predictions
    - Arudha calculations

### Accuracy

Planetary positions are calculated with Swiss Ephemeris accuracy:
- Less than 0.001 arc-second error
- Sub-milli-arc-second precision (0.001 arc-seconds)
""",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS middleware for Next.js frontend
# Get allowed origins from environment variable or use defaults
allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",") if os.getenv("ALLOWED_ORIGINS") else []
allowed_origins.extend([
    "http://localhost:3000",      # Next.js dev server
    "http://127.0.0.1:3000",
    "http://localhost:3001",      # Alternative port
    "http://localhost:5173",      # Vite dev server
    "http://localhost:5000",      # Flask dev server (for testing)
])
# Remove empty strings and duplicates
allowed_origins = list(set(filter(None, allowed_origins)))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unhandled exceptions."""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": str(exc)
        }
    )


# Include routers
app.include_router(kundali_router)
app.include_router(chat_router)
app.include_router(muhurta_router)
app.include_router(health_router)
app.include_router(matching_router)
app.include_router(divisional_charts_router)
app.include_router(panchang_router)
app.include_router(pdf_router)
app.include_router(numerology_router)
app.include_router(rashifal_router)
app.include_router(dosha_router)
app.include_router(gemstone_router)
app.include_router(career_router)
app.include_router(remedies_router)
app.include_router(prashna_router)


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Kundali Software API",
        "version": "1.0.0",
        "description": "Vedic Astrology REST API",
        "docs": "/docs",
        "endpoints": {
            "generate": "POST /api/generate - Create kundali",
            "chat": "POST /api/chat - Chat with assistant",
            "muhurta": "POST /api/muhurta - Find auspicious times",
            "health": "POST /api/health - Health predictions",
            "match": "POST /api/match - Kundali matching for marriage",
            "varga": "GET /api/varga/charts/{id} - Divisional charts",
            "panchang": "POST /api/panchang/daily - Daily Panchang",
            "numerology": "POST /api/numerology/analyze - Numerology analysis",
            "pdf_kundali": "GET /api/kundali/{id}/pdf - Download Kundali PDF",
            "pdf_matching": "POST /api/matching/pdf - Download Matching PDF",
            "rashifal": "POST /api/rashifal - Daily/Weekly/Monthly horoscope",
            "dosha": "POST /api/dosha/analyze - Dosha analysis (Kaal Sarp, Manglik, etc.)",
            "gemstone": "POST /api/gemstone/recommend - Gemstone recommendations",
            "career": "POST /api/career/analyze - Career & finance analysis",
            "remedies": "POST /api/remedies/comprehensive - Vedic remedies",
            "prashna": "POST /api/prashna/analyze - Prashna Kundali (Horary)"
        }
    }


# Health check endpoint
@app.get("/health", tags=["Root"])
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "service": "kundali-api"}


if __name__ == "__main__":
    import uvicorn

    print("\n" + "=" * 60)
    print("   KUNDALI SOFTWARE - FastAPI Backend")
    print("   Open: http://localhost:8000")
    print("   Docs: http://localhost:8000/docs")
    print("   Auto-reload: ENABLED")
    print("=" * 60 + "\n")

    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=[".", "..\\src"]
    )
