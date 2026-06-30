"""
Panchang API Routes - Daily Vedic Almanac

Provides endpoints for:
- Daily Panchang (Five Limbs: Tithi, Nakshatra, Yoga, Karana, Vara)
- Choghadiya (Auspicious/Inauspicious time periods)
- Rahu Kaal, Yamaghantaka, Gulika Kaal
- Sunrise, Sunset, Moonrise, Moonset
"""

from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import pytz

from src.panchang import PanchangCalculator


router = APIRouter(prefix="/api/panchang", tags=["Panchang"])

# Initialize calculator
panchang_calculator = PanchangCalculator()


class PanchangRequest(BaseModel):
    """Request model for Panchang calculation."""
    date: str = Field(..., description="Date in YYYY-MM-DD format")
    latitude: Optional[float] = Field(28.6139, description="Latitude (default: Delhi)")
    longitude: Optional[float] = Field(77.2090, description="Longitude (default: Delhi)")
    timezone: Optional[str] = Field("Asia/Kolkata", description="Timezone")
    location: Optional[str] = Field("Delhi", description="Location name for display")

    class Config:
        json_schema_extra = {
            "example": {
                "date": "2026-06-28",
                "latitude": 28.6139,
                "longitude": 77.2090,
                "timezone": "Asia/Kolkata",
                "location": "Delhi"
            }
        }


class ChoghadiyaRequest(BaseModel):
    """Request model for Choghadiya calculation."""
    date: str = Field(..., description="Date in YYYY-MM-DD format")
    latitude: Optional[float] = Field(28.6139, description="Latitude")
    longitude: Optional[float] = Field(77.2090, description="Longitude")
    timezone: Optional[str] = Field("Asia/Kolkata", description="Timezone")


@router.post("/daily")
async def get_daily_panchang(request: PanchangRequest):
    """
    Get complete daily Panchang data.

    Returns all five limbs (Panch Ang):
    - **Tithi**: Lunar day (1-30)
    - **Nakshatra**: Moon's constellation (1-27)
    - **Yoga**: Sun-Moon combination (1-27)
    - **Karana**: Half-tithi (1-11)
    - **Vara**: Weekday with planetary lord

    Plus:
    - Sunrise/Sunset/Moonrise/Moonset times
    - Day and Night Choghadiya
    - Rahu Kaal, Yamaghantaka, Gulika Kaal
    - Abhijit Muhurta
    - Overall auspiciousness assessment
    """
    try:
        # Parse date
        dt = datetime.strptime(request.date, "%Y-%m-%d")
        tz = pytz.timezone(request.timezone)
        dt = tz.localize(dt.replace(hour=12, minute=0))  # Noon for day calculations

        # Get complete Panchang summary
        panchang_data = panchang_calculator.get_panchang_summary(
            dt=dt,
            latitude=request.latitude,
            longitude=request.longitude,
            timezone=request.timezone,
            location=request.location
        )

        return {
            "success": True,
            "data": panchang_data,
            "message": "Panchang calculated successfully"
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating Panchang: {str(e)}")


@router.get("/today")
async def get_today_panchang(
    latitude: float = 28.6139,
    longitude: float = 77.2090,
    timezone: str = "Asia/Kolkata",
    location: str = "Delhi"
):
    """
    Get Panchang for today.

    Quick endpoint without needing to specify date.
    Uses current date in the specified timezone.
    """
    try:
        tz = pytz.timezone(timezone)
        today = datetime.now(tz)

        panchang_data = panchang_calculator.get_panchang_summary(
            dt=today,
            latitude=latitude,
            longitude=longitude,
            timezone=timezone,
            location=location
        )

        return {
            "success": True,
            "data": panchang_data,
            "message": "Today's Panchang calculated successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating Panchang: {str(e)}")


@router.post("/choghadiya")
async def get_choghadiya(request: ChoghadiyaRequest):
    """
    Get Choghadiya (auspicious time periods) for a specific date.

    Choghadiya divides the day into 8 parts (sunrise to sunset)
    and night into 8 parts (sunset to next sunrise).

    Types:
    - **Amrit**: Most Auspicious (Moon)
    - **Shubh**: Auspicious (Jupiter)
    - **Labh**: Gain (Mercury)
    - **Char**: Good for travel (Venus)
    - **Udveg**: Anxiety - Inauspicious (Sun)
    - **Kaal**: Death - Inauspicious (Saturn)
    - **Rog**: Disease - Inauspicious (Mars)
    """
    try:
        dt = datetime.strptime(request.date, "%Y-%m-%d")
        tz = pytz.timezone(request.timezone)
        dt = tz.localize(dt.replace(hour=12, minute=0))

        panchang = panchang_calculator.get_panchang(
            dt=dt,
            latitude=request.latitude,
            longitude=request.longitude,
            timezone=request.timezone
        )

        # Format Choghadiya data
        def format_chog(chog_list):
            return [
                {
                    "name": c.name,
                    "hindi": c.hindi,
                    "start_time": c.start_time.strftime("%H:%M"),
                    "end_time": c.end_time.strftime("%H:%M"),
                    "quality": c.quality,
                    "lord": c.lord,
                    "nature": c.nature,
                    "is_auspicious": c.is_auspicious
                }
                for c in chog_list
            ]

        current_chog = None
        if panchang.current_choghadiya:
            current_chog = {
                "name": panchang.current_choghadiya.name,
                "hindi": panchang.current_choghadiya.hindi,
                "start_time": panchang.current_choghadiya.start_time.strftime("%H:%M"),
                "end_time": panchang.current_choghadiya.end_time.strftime("%H:%M"),
                "quality": panchang.current_choghadiya.quality,
                "is_auspicious": panchang.current_choghadiya.is_auspicious
            }

        return {
            "success": True,
            "data": {
                "date": request.date,
                "sunrise": panchang.timings.sunrise.strftime("%H:%M"),
                "sunset": panchang.timings.sunset.strftime("%H:%M"),
                "day_choghadiya": format_chog(panchang.day_choghadiya),
                "night_choghadiya": format_chog(panchang.night_choghadiya),
                "current_choghadiya": current_chog
            },
            "message": "Choghadiya calculated successfully"
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating Choghadiya: {str(e)}")


@router.post("/inauspicious-periods")
async def get_inauspicious_periods(request: ChoghadiyaRequest):
    """
    Get all inauspicious periods for a date.

    Returns:
    - **Rahu Kaal**: Period ruled by Rahu (most inauspicious)
    - **Yamaghantaka**: Period ruled by Yama (god of death)
    - **Gulika Kaal**: Period of Gulika/Mandi (son of Saturn)

    Also returns **Abhijit Muhurta** - the most auspicious time of the day.
    """
    try:
        dt = datetime.strptime(request.date, "%Y-%m-%d")
        tz = pytz.timezone(request.timezone)
        dt = tz.localize(dt.replace(hour=12, minute=0))

        panchang = panchang_calculator.get_panchang(
            dt=dt,
            latitude=request.latitude,
            longitude=request.longitude,
            timezone=request.timezone
        )

        abhijit = None
        if panchang.abhijit_muhurta:
            abhijit = {
                "start": panchang.abhijit_muhurta[0].strftime("%H:%M"),
                "end": panchang.abhijit_muhurta[1].strftime("%H:%M"),
                "description": "Most auspicious time for all works / सभी कार्यों के लिए सर्वोत्तम समय"
            }

        return {
            "success": True,
            "data": {
                "date": request.date,
                "rahu_kaal": {
                    "name": "Rahu Kaal",
                    "hindi": panchang.rahu_kaal.hindi,
                    "start": panchang.rahu_kaal.start_time.strftime("%H:%M"),
                    "end": panchang.rahu_kaal.end_time.strftime("%H:%M"),
                    "severity": panchang.rahu_kaal.severity,
                    "description": panchang.rahu_kaal.description
                },
                "yamaghantaka": {
                    "name": "Yamaghantaka",
                    "hindi": panchang.yamaghantaka.hindi,
                    "start": panchang.yamaghantaka.start_time.strftime("%H:%M"),
                    "end": panchang.yamaghantaka.end_time.strftime("%H:%M"),
                    "severity": panchang.yamaghantaka.severity,
                    "description": panchang.yamaghantaka.description
                },
                "gulika_kaal": {
                    "name": "Gulika Kaal",
                    "hindi": panchang.gulika_kaal.hindi,
                    "start": panchang.gulika_kaal.start_time.strftime("%H:%M"),
                    "end": panchang.gulika_kaal.end_time.strftime("%H:%M"),
                    "severity": panchang.gulika_kaal.severity,
                    "description": panchang.gulika_kaal.description
                },
                "abhijit_muhurta": abhijit
            },
            "message": "Inauspicious periods calculated successfully"
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating periods: {str(e)}")


@router.post("/auspicious-times")
async def get_auspicious_times(request: ChoghadiyaRequest):
    """
    Get all auspicious time windows for a date.

    Returns time windows that are:
    - Not in Rahu Kaal
    - In auspicious Choghadiya (Amrit, Shubh, Labh, Char)
    - Including Abhijit Muhurta
    """
    try:
        dt = datetime.strptime(request.date, "%Y-%m-%d")
        tz = pytz.timezone(request.timezone)
        dt = tz.localize(dt.replace(hour=12, minute=0))

        auspicious_times = panchang_calculator.get_auspicious_times(
            dt=dt,
            latitude=request.latitude,
            longitude=request.longitude,
            timezone=request.timezone
        )

        return {
            "success": True,
            "data": {
                "date": request.date,
                "auspicious_windows": auspicious_times
            },
            "message": "Auspicious times calculated successfully"
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating auspicious times: {str(e)}")


@router.get("/tithi/{date}")
async def get_tithi(
    date: str,
    timezone: str = "Asia/Kolkata"
):
    """
    Get just the Tithi for a specific date.

    Useful for quick lookups of lunar day information.
    """
    try:
        dt = datetime.strptime(date, "%Y-%m-%d")
        tz = pytz.timezone(timezone)
        dt = tz.localize(dt.replace(hour=12, minute=0))

        tithi = panchang_calculator.get_tithi_for_date(dt, timezone)

        return {
            "success": True,
            "data": {
                "date": date,
                "tithi": {
                    "number": tithi.number,
                    "name": tithi.name,
                    "hindi": tithi.hindi,
                    "paksha": tithi.paksha,
                    "paksha_hindi": tithi.paksha_hindi,
                    "lord": tithi.lord,
                    "is_rikta": tithi.is_rikta,
                    "is_purnima": tithi.is_purnima,
                    "is_amavasya": tithi.is_amavasya,
                    "percentage_elapsed": tithi.percentage_elapsed
                }
            },
            "message": "Tithi calculated successfully"
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating Tithi: {str(e)}")


@router.get("/nakshatra/{date}")
async def get_nakshatra(
    date: str,
    timezone: str = "Asia/Kolkata"
):
    """
    Get Moon's Nakshatra for a specific date.

    Returns nakshatra name, lord, deity, and pada.
    """
    try:
        dt = datetime.strptime(date, "%Y-%m-%d")
        tz = pytz.timezone(timezone)
        dt = tz.localize(dt.replace(hour=12, minute=0))

        nakshatra_data = panchang_calculator.get_nakshatra_for_date(dt, timezone)

        return {
            "success": True,
            "data": {
                "date": date,
                "nakshatra": nakshatra_data
            },
            "message": "Nakshatra calculated successfully"
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating Nakshatra: {str(e)}")
