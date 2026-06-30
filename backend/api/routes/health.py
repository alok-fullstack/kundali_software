"""
Health/Accident Prediction API route.

POST /api/health - Get health and accident predictions for a date range.
"""

import sys
from pathlib import Path

from fastapi import APIRouter, HTTPException, status

# Ensure parent directories are in path
backend_dir = Path(__file__).resolve().parent.parent.parent
kundali_dir = backend_dir.parent
if str(kundali_dir) not in sys.path:
    sys.path.insert(0, str(kundali_dir))

from api.models import (
    HealthRequest,
    HealthResponse,
    HealthWarningResponse,
    HealthSummary,
    ErrorResponse,
)
from src.health_predictor import HealthPredictor
from src.health_html_generator import generate_health_html
from api.routes.kundali import get_kundali

router = APIRouter(prefix="/api", tags=["Health"])


def build_warning_response(warning) -> HealthWarningResponse:
    """Convert HealthWarning to response model."""
    return HealthWarningResponse(
        start_date=warning.start_date.strftime('%Y-%m-%d'),
        end_date=warning.end_date.strftime('%Y-%m-%d'),
        event_type=warning.event_type.value,
        risk_level=warning.risk_level.value,
        reasons=warning.reasons,
        dasha_info=warning.dasha_info,
        affected_body_parts=warning.affected_body_parts,
        remedies=warning.remedies
    )


@router.post(
    "/health",
    response_model=HealthResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        404: {"model": ErrorResponse, "description": "Kundali not found"}
    },
    summary="Get Health/Accident Predictions",
    description="Predict vulnerable periods for health issues and accidents."
)
async def predict_health(request: HealthRequest) -> HealthResponse:
    """
    Predict health issues and accident-prone periods.

    This endpoint analyzes:
    - Dasha of 6th/8th/12th lords (disease, accidents, hospitalization)
    - Dasha of Maraka planets (2nd/7th lords)
    - Malefic transits (Saturn, Mars, Rahu) over sensitive points
    - Afflictions to Lagna and Moon

    Event types detected:
    - **Accident/Injury**: Sudden physical harm risk
    - **Chronic Disease**: Long-term health conditions
    - **Surgery**: Surgical procedure risk
    - **Hospitalization**: Risk of hospital stay
    - **Mental Stress**: Psychological health concerns
    - **General Health Issue**: Other health concerns

    Risk levels:
    - **Critical** (70-100): Highest concern, take precautions
    - **High** (55-69): Significant risk, be cautious
    - **Medium** (40-54): Moderate risk, monitor health
    - **Low** (0-39): Minor concerns

    Remedies are provided for each warning period.
    """
    try:
        # Get kundali from store
        kundali = get_kundali(request.kundali_id)

        # Create predictor and get predictions
        predictor = HealthPredictor(kundali)

        # Get warnings
        warnings = predictor.predict_health_issues(
            request.start_year,
            request.end_year,
            min_risk_score=request.min_risk_score
        )

        # Get summary
        summary_data = predictor.get_health_summary(request.start_year, request.end_year)

        # Build response
        warning_responses = [build_warning_response(w) for w in warnings]

        summary = HealthSummary(
            period=f"{request.start_year} - {request.end_year}",
            total_warnings=len(warnings),
            critical_periods=summary_data["critical_periods"],
            high_risk_periods=summary_data["high_risk_periods"],
            medium_risk_periods=summary_data["medium_risk_periods"],
            general_advice=summary_data["general_advice"]
        )

        # Get lagna and moon rashi for context
        lagna = kundali.lagna["rashi"]
        moon_rashi = kundali.planets["MOON"]["rashi"]

        message = ""
        if not warnings:
            message = f"No significant health concerns found for {request.start_year}-{request.end_year}"

        # Generate HTML for frontend display
        html_content = generate_health_html(
            kundali=kundali,
            start_year=request.start_year,
            end_year=request.end_year,
            min_risk_score=request.min_risk_score
        )

        return HealthResponse(
            success=True,
            kundali_id=request.kundali_id,
            start_year=request.start_year,
            end_year=request.end_year,
            lagna=lagna,
            moon_rashi=moon_rashi,
            summary=summary,
            warnings=warning_responses,
            message=message,
            html=html_content
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error predicting health: {str(e)}"
        )
