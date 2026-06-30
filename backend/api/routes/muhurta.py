"""
Muhurta API route.

POST /api/muhurta - Find auspicious times (muhurtas) for events.
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException, status

# Ensure parent directories are in path
backend_dir = Path(__file__).resolve().parent.parent.parent
kundali_dir = backend_dir.parent
if str(kundali_dir) not in sys.path:
    sys.path.insert(0, str(kundali_dir))

from api.models import (
    MuhurtaRequest,
    MuhurtaResponse,
    MuhurtaWindowResponse,
    PanchangInfo,
    InauspiciousPeriodInfo,
    ErrorResponse,
)
from src.muhurta import MuhurtaCalculator
from src.muhurta_rules import EventType
from src.muhurta_html_generator import generate_muhurta_html
from api.routes.kundali import get_kundali

router = APIRouter(prefix="/api", tags=["Muhurta"])


# Map string event types to EventType enum
EVENT_TYPE_MAP = {
    'marriage': EventType.MARRIAGE,
    'career': EventType.CAREER,
    'property': EventType.PROPERTY,
    'travel': EventType.TRAVEL,
    'griha_pravesh': EventType.GRIHA_PRAVESH,
    'education': EventType.EDUCATION,
    'general': EventType.GENERAL,
}


def build_muhurta_response(muhurta) -> MuhurtaWindowResponse:
    """Convert MuhurtaWindow to response model."""
    # Build panchang info
    panchang_info = PanchangInfo(
        tithi=muhurta.panchang.tithi.name,
        tithi_paksha=muhurta.panchang.tithi.paksha,
        nakshatra=muhurta.panchang.nakshatra.name,
        nakshatra_pada=muhurta.panchang.nakshatra.pada,
        yoga=muhurta.panchang.yoga.name,
        yoga_is_inauspicious=muhurta.panchang.yoga.is_inauspicious,
        karana=muhurta.panchang.karana.name,
        vara=muhurta.panchang.vara.name,
        vara_english=muhurta.panchang.vara.english
    )

    # Build inauspicious periods list
    inauspicious_list = []
    for p in muhurta.inauspicious_periods:
        inauspicious_list.append(InauspiciousPeriodInfo(
            name=p.name,
            start_time=p.start_time.strftime('%H:%M'),
            end_time=p.end_time.strftime('%H:%M'),
            severity=p.severity
        ))

    # Format abhijit muhurta
    abhijit_str = None
    if muhurta.abhijit_muhurta:
        abhijit_str = f"{muhurta.abhijit_muhurta[0].strftime('%H:%M')} - {muhurta.abhijit_muhurta[1].strftime('%H:%M')}"

    return MuhurtaWindowResponse(
        date=muhurta.date.strftime('%Y-%m-%d'),
        weekday=muhurta.panchang.vara.english,
        start_time=muhurta.start_time.strftime('%H:%M'),
        end_time=muhurta.end_time.strftime('%H:%M'),
        score=muhurta.score,
        panchang=panchang_info,
        tarabala_num=muhurta.tarabala_num,
        tarabala_name=muhurta.tarabala_name,
        tarabala_score=muhurta.tarabala_score,
        chandrabala_house=muhurta.chandrabala_house,
        chandrabala_score=muhurta.chandrabala_score,
        dasha_info=muhurta.dasha_info or "",
        abhijit_muhurta=abhijit_str,
        hora_lord=muhurta.hora_lord,
        reasons=muhurta.reasons,
        warnings=muhurta.warnings,
        inauspicious_periods=inauspicious_list
    )


@router.post(
    "/muhurta",
    response_model=MuhurtaResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        404: {"model": ErrorResponse, "description": "Kundali not found"}
    },
    summary="Find Auspicious Muhurtas",
    description="Find auspicious time windows for important life events."
)
async def find_muhurtas(request: MuhurtaRequest) -> MuhurtaResponse:
    """
    Find auspicious muhurtas (electional astrology) for an event.

    This endpoint finds the best times for:
    - **marriage**: Wedding ceremonies
    - **career**: Job changes, promotions, business launches
    - **property**: Real estate purchases
    - **griha_pravesh**: House warming ceremonies
    - **travel**: Important journeys
    - **education**: Starting courses, exams
    - **general**: Other important events

    The analysis includes:
    - Panchang factors (Tithi, Nakshatra, Yoga, Karana, Vara)
    - Personal compatibility (Tarabala from birth nakshatra)
    - Chandrabala (Moon house transit)
    - Dasha/Transit analysis
    - Inauspicious periods to avoid (Rahu Kala, Yamaghantaka, etc.)

    Results are scored from 0-100 and sorted by score.
    """
    try:
        # Get kundali from store
        kundali = get_kundali(request.kundali_id)

        # Get event type enum
        event_type = EVENT_TYPE_MAP.get(request.event_type)
        if not event_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid event_type: {request.event_type}"
            )

        # Create calculator and find muhurtas
        calc = MuhurtaCalculator(kundali)

        start_date = datetime(request.year, 1, 1)
        end_date = datetime(request.year, 12, 31)

        muhurtas = calc.find_muhurtas(
            event_type=event_type,
            start_date=start_date,
            end_date=end_date,
            use_event_predictor=True,
            min_score=request.min_score,
            top_n=request.top_n
        )

        # Build response
        muhurta_responses = [build_muhurta_response(m) for m in muhurtas]

        # Get birth nakshatra and moon rashi for context
        birth_nakshatra = kundali.planets["MOON"]["nakshatra"]
        moon_rashi = kundali.planets["MOON"]["rashi"]

        message = ""
        if not muhurtas:
            message = f"No muhurtas found with score >= {request.min_score} for {request.event_type} in {request.year}"

        # Generate HTML for frontend display
        html_content = generate_muhurta_html(
            kundali=kundali,
            event_type=request.event_type,
            start_date=start_date,
            end_date=end_date,
            top_n=request.top_n,
            min_score=request.min_score
        )

        return MuhurtaResponse(
            success=True,
            kundali_id=request.kundali_id,
            event_type=request.event_type,
            year=request.year,
            birth_nakshatra=birth_nakshatra,
            moon_rashi=moon_rashi,
            muhurtas=muhurta_responses,
            total_found=len(muhurta_responses),
            message=message,
            html=html_content
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error finding muhurtas: {str(e)}"
        )
