"""
Rashifal (Horoscope) API Routes
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import sys
from pathlib import Path

# Ensure parent directories are in path
backend_dir = Path(__file__).resolve().parent.parent.parent
kundali_dir = backend_dir.parent
if str(kundali_dir) not in sys.path:
    sys.path.insert(0, str(kundali_dir))

try:
    from src.rashifal import get_rashifal, get_all_rashifal, RashifalPeriod
except ImportError as e:
    print(f"Rashifal import error: {e}")
    get_rashifal = None
    get_all_rashifal = None
    RashifalPeriod = None

router = APIRouter(prefix="/api/rashifal", tags=["Rashifal"])

# Rashi name to number mapping
RASHI_NAME_TO_NUM = {
    "mesha": 0, "aries": 0,
    "vrishabha": 1, "taurus": 1,
    "mithuna": 2, "gemini": 2,
    "karka": 3, "cancer": 3,
    "simha": 4, "leo": 4,
    "kanya": 5, "virgo": 5,
    "tula": 6, "libra": 6,
    "vrishchika": 7, "scorpio": 7,
    "dhanu": 8, "sagittarius": 8,
    "makara": 9, "capricorn": 9,
    "kumbha": 10, "aquarius": 10,
    "meena": 11, "pisces": 11
}


class RashifalRequest(BaseModel):
    """Request model for rashifal"""
    moon_sign: str  # e.g., "Mesha", "Vrishabha", etc.
    period: str = "daily"  # daily, weekly, monthly, yearly
    date: Optional[str] = None  # YYYY-MM-DD format


@router.get("/")
async def get_horoscope_get(
    rashi: int = Query(..., ge=0, le=11, description="Rashi number (0-11)"),
    period: str = Query("daily", description="Period: daily, weekly, monthly, yearly"),
    date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format (past or future)")
):
    """
    Get Rashifal (horoscope) for a rashi by number (GET method).

    Args:
        rashi: Rashi number (0=Mesha/Aries, 1=Vrishabha/Taurus, ...)
        period: daily, weekly, monthly, yearly
        date: Optional date for prediction (YYYY-MM-DD format)

    Returns:
        Rashifal predictions in Hindi/Hinglish
    """
    if get_rashifal is None:
        raise HTTPException(status_code=500, detail="Rashifal module not available")

    try:
        # Parse date if provided
        target_date = None
        if date:
            try:
                target_date = datetime.fromisoformat(date)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid date format: {date}. Use YYYY-MM-DD")

        result = get_rashifal(
            rashi_num=rashi,
            period=period.lower(),
            date=target_date
        )
        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/all")
async def get_all_horoscopes(
    period: str = Query("daily", description="Period: daily, weekly, monthly, yearly"),
    date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format (past or future)")
):
    """
    Get Rashifal for all 12 rashis.

    Args:
        period: daily, weekly, monthly, yearly
        date: Optional date for prediction (YYYY-MM-DD format)

    Returns:
        List of Rashifal predictions for all rashis
    """
    if get_all_rashifal is None:
        raise HTTPException(status_code=500, detail="Rashifal module not available")

    try:
        # Parse date if provided
        target_date = None
        if date:
            try:
                target_date = datetime.fromisoformat(date)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid date format: {date}. Use YYYY-MM-DD")

        results = get_all_rashifal(period=period.lower(), date=target_date)
        return results

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
async def get_horoscope_post(request: RashifalRequest):
    """
    Get Rashifal (horoscope) for a moon sign (POST method).

    Args:
        request: RashifalRequest with moon_sign and period

    Returns:
        Rashifal predictions in Hindi/Hinglish
    """
    if get_rashifal is None:
        raise HTTPException(status_code=500, detail="Rashifal module not available")

    try:
        # Convert moon_sign to rashi number
        rashi_num = RASHI_NAME_TO_NUM.get(request.moon_sign.lower())
        if rashi_num is None:
            # Try parsing as number
            try:
                rashi_num = int(request.moon_sign)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid moon sign: {request.moon_sign}")

        # Parse date if provided
        target_date = None
        if request.date:
            target_date = datetime.fromisoformat(request.date)

        result = get_rashifal(
            rashi_num=rashi_num,
            period=request.period.lower(),
            date=target_date
        )

        return {
            "success": True,
            "rashifal": result
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/signs")
async def get_all_signs():
    """Get all zodiac signs with Hindi names"""
    return {
        "success": True,
        "signs": [
            {"name": "Mesha", "hindi": "मेष", "english": "Aries", "number": 0},
            {"name": "Vrishabha", "hindi": "वृषभ", "english": "Taurus", "number": 1},
            {"name": "Mithuna", "hindi": "मिथुन", "english": "Gemini", "number": 2},
            {"name": "Karka", "hindi": "कर्क", "english": "Cancer", "number": 3},
            {"name": "Simha", "hindi": "सिंह", "english": "Leo", "number": 4},
            {"name": "Kanya", "hindi": "कन्या", "english": "Virgo", "number": 5},
            {"name": "Tula", "hindi": "तुला", "english": "Libra", "number": 6},
            {"name": "Vrishchika", "hindi": "वृश्चिक", "english": "Scorpio", "number": 7},
            {"name": "Dhanu", "hindi": "धनु", "english": "Sagittarius", "number": 8},
            {"name": "Makara", "hindi": "मकर", "english": "Capricorn", "number": 9},
            {"name": "Kumbha", "hindi": "कुंभ", "english": "Aquarius", "number": 10},
            {"name": "Meena", "hindi": "मीन", "english": "Pisces", "number": 11}
        ]
    }
