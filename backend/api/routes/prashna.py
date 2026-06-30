"""
Prashna Kundali (Horary Astrology) API Routes
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import sys
from pathlib import Path

# Ensure parent directories are in path
backend_dir = Path(__file__).resolve().parent.parent.parent
kundali_dir = backend_dir.parent
if str(kundali_dir) not in sys.path:
    sys.path.insert(0, str(kundali_dir))

try:
    from src.prashna_kundali import PrashnaCalculator, analyze_prashna, QuestionCategory
except ImportError:
    PrashnaCalculator = None
    analyze_prashna = None
    QuestionCategory = None

try:
    from src.kundali import create_kundali
except ImportError:
    create_kundali = None

router = APIRouter(prefix="/api/prashna", tags=["Prashna Kundali"])


class PrashnaRequest(BaseModel):
    """Request model for Prashna Kundali"""
    question: str
    question_type: str = "general"  # general, marriage, career, health, travel, lost_item, litigation, education, finance, pregnancy
    city: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    datetime_str: Optional[str] = None  # ISO format, defaults to current time


@router.post("/analyze")
async def analyze_prashna_kundali(request: PrashnaRequest):
    """
    Analyze a Prashna (horary) question.

    Based on:
    - Prashna Marga by Harihara
    - Prashna Tantra
    - Tajika Neelakanthi

    Generates a chart for the moment of the question and provides:
    - Answer (favorable/unfavorable)
    - Timing prediction
    - Arudha analysis
    - Favorable/unfavorable factors
    """
    if analyze_prashna is None or create_kundali is None:
        raise HTTPException(status_code=500, detail="Prashna module not available")

    try:
        # Parse datetime or use current
        if request.datetime_str:
            query_time = datetime.fromisoformat(request.datetime_str)
        else:
            query_time = datetime.now()

        # Default coordinates for common cities if not provided
        default_coords = {
            "delhi": (28.6139, 77.2090),
            "mumbai": (19.0760, 72.8777),
            "bangalore": (12.9716, 77.5946),
            "chennai": (13.0827, 80.2707),
            "kolkata": (22.5726, 88.3639),
            "hyderabad": (17.3850, 78.4867),
            "pune": (18.5204, 73.8567),
            "jaipur": (26.9124, 75.7873),
            "lucknow": (26.8467, 80.9462),
            "varanasi": (25.3176, 82.9739)
        }

        lat = request.latitude
        lon = request.longitude

        if lat is None or lon is None:
            city_lower = request.city.lower()
            if city_lower in default_coords:
                lat, lon = default_coords[city_lower]
            else:
                lat, lon = 28.6139, 77.2090  # Default to Delhi

        # Create Prashna chart
        chart = create_kundali(
            name="Prashna",
            year=query_time.year,
            month=query_time.month,
            day=query_time.day,
            hour=query_time.hour,
            minute=query_time.minute,
            city=request.city,
            latitude=lat,
            longitude=lon
        )

        # Analyze the question
        result = analyze_prashna(chart, request.question_type)

        return {
            "success": True,
            "prashna": {
                "question": request.question,
                "question_type": result.question_category.value,
                "query_time": query_time.isoformat(),
                "location": request.city,
                "primary_house": result.primary_house,
                "significators": result.significators,
                "lagna_analysis": result.lagna_analysis,
                "moon_analysis": result.moon_analysis,
                "arudha": {
                    "house": result.arudha.arudha_house,
                    "sign": result.arudha.arudha_sign,
                    "lord": result.arudha.arudha_lord,
                    "lord_house": result.arudha.arudha_lord_house,
                    "strength": result.arudha.strength
                },
                "timing": {
                    "will_happen": result.timing.will_happen,
                    "timeframe": result.timing.timeframe,
                    "timeframe_hindi": result.timing.timeframe_hindi,
                    "timing_basis": result.timing.timing_basis,
                    "confidence": result.timing.confidence
                },
                "answer": result.answer,
                "answer_hindi": result.answer_hindi,
                "confidence_level": result.confidence_level,
                "favorable_factors": result.favorable_factors,
                "unfavorable_factors": result.unfavorable_factors,
                "interpretation": result.detailed_interpretation,
                "interpretation_hindi": result.detailed_interpretation_hindi
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/question-types")
async def get_question_types():
    """Get all supported question types"""
    return {
        "success": True,
        "question_types": [
            {"value": "general", "label": "सामान्य प्रश्न / General Question"},
            {"value": "marriage", "label": "विवाह / Marriage"},
            {"value": "career", "label": "करियर / Career"},
            {"value": "health", "label": "स्वास्थ्य / Health"},
            {"value": "travel", "label": "यात्रा / Travel"},
            {"value": "lost_item", "label": "खोई वस्तु / Lost Item"},
            {"value": "litigation", "label": "मुकदमा / Litigation"},
            {"value": "education", "label": "शिक्षा / Education"},
            {"value": "finance", "label": "वित्त / Finance"},
            {"value": "pregnancy", "label": "गर्भावस्था / Pregnancy"}
        ]
    }
