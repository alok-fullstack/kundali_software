"""
Kundali Matching (Marriage Compatibility) API route.

POST /api/match - Match two kundalis for marriage compatibility
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, field_validator

# Ensure parent directories are in path
backend_dir = Path(__file__).resolve().parent.parent.parent
kundali_dir = backend_dir.parent
if str(kundali_dir) not in sys.path:
    sys.path.insert(0, str(kundali_dir))

from src.kundali import create_kundali, Kundali
from src.kundali_matching import (
    KundaliMatcher, MatchingResult,
    RASHI_VARNA, NAKSHATRA_GANA, NAKSHATRA_NADI, NAKSHATRA_YONI
)
from src.matching_predictions import generate_matching_predictions, generate_matching_html
from src.config import NAKSHATRAS

router = APIRouter(prefix="/api", tags=["Matching"])


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class PersonDetails(BaseModel):
    """Birth details for one person."""
    name: str = Field(..., min_length=1, max_length=100, description="Person's name")
    dob: str = Field(..., description="Date of birth in YYYY-MM-DD format")
    tob: str = Field(..., description="Time of birth in HH:MM format (24-hour)")
    city: str = Field(..., min_length=1, max_length=100, description="Birth city name")
    latitude: Optional[float] = Field(None, ge=-90, le=90, description="Latitude")
    longitude: Optional[float] = Field(None, ge=-180, le=180, description="Longitude")
    timezone: str = Field("Asia/Kolkata", description="Timezone string")

    @field_validator('dob')
    @classmethod
    def validate_dob(cls, v: str) -> str:
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('dob must be in YYYY-MM-DD format')
        return v

    @field_validator('tob')
    @classmethod
    def validate_tob(cls, v: str) -> str:
        try:
            datetime.strptime(v, '%H:%M')
        except ValueError:
            raise ValueError('tob must be in HH:MM format')
        return v


class MatchRequest(BaseModel):
    """Request model for Kundali matching."""
    boy: PersonDetails = Field(..., description="Boy's birth details")
    girl: PersonDetails = Field(..., description="Girl's birth details")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "boy": {
                        "name": "Rahul",
                        "dob": "1995-03-15",
                        "tob": "10:30",
                        "city": "Delhi",
                        "timezone": "Asia/Kolkata"
                    },
                    "girl": {
                        "name": "Priya",
                        "dob": "1997-06-20",
                        "tob": "14:45",
                        "city": "Mumbai",
                        "timezone": "Asia/Kolkata"
                    }
                }
            ]
        }
    }


class KootaScore(BaseModel):
    """Individual Koota score details."""
    name: str
    name_hindi: str
    max_points: float
    obtained_points: float
    boy_value: str
    girl_value: str
    description: str
    is_auspicious: bool
    dosha: Optional[str] = None


class DoshaInfo(BaseModel):
    """Dosha information."""
    name: str
    type: str
    severity: str
    description: str
    remedies: List[str] = []
    is_cancelled: bool = False


class MarriageTiming(BaseModel):
    """Marriage timing suggestions."""
    favorable_days: List[str] = []
    favorable_months: List[str] = []
    avoid: List[str] = []
    general_advice: List[str] = []


class KootaInterpretation(BaseModel):
    """Detailed Koota interpretation for expandable UI."""
    name: str
    name_hindi: str
    score: str
    percentage: float
    boy_value: str
    girl_value: str
    is_favorable: bool
    description: str
    title: str
    detailed_interpretation: str
    effects: List[str] = []
    remedies: List[str] = []
    dosha: Optional[str] = None
    # Hindi translations
    title_hindi: str = ""
    detailed_interpretation_hindi: str = ""
    effects_hindi: List[str] = []


class MatchingScores(BaseModel):
    """Detailed matching scores."""
    varna: float
    vashya: float
    tara: float
    yoni: float
    graha_maitri: float
    gana: float
    bhakoot: float
    nadi: float


class MatchResponse(BaseModel):
    """Response model for Kundali matching."""
    success: bool
    boy_name: str
    girl_name: str
    total_points: float
    max_points: float = 36.0
    percentage: float
    compatibility_level: str
    koota_scores: List[KootaScore]
    koota_interpretations: List[KootaInterpretation] = []
    doshas: List[DoshaInfo]
    score_breakdown: MatchingScores
    recommendation: str
    remedies: List[str]
    areas_of_strength: List[str]
    areas_of_concern: List[str]
    boy_details: Dict[str, Any]
    girl_details: Dict[str, Any]
    marriage_timing: Optional[MarriageTiming] = None
    html: Optional[str] = None
    message: str = "Matching completed successfully"


class ErrorResponse(BaseModel):
    """Standard error response."""
    success: bool = False
    error: str
    detail: Optional[str] = None


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def create_kundali_from_details(details: PersonDetails) -> Kundali:
    """Create a Kundali from PersonDetails."""
    dob_parts = details.dob.split('-')
    tob_parts = details.tob.split(':')

    params = {
        'name': details.name,
        'year': int(dob_parts[0]),
        'month': int(dob_parts[1]),
        'day': int(dob_parts[2]),
        'hour': int(tob_parts[0]),
        'minute': int(tob_parts[1]),
        'city': details.city,
        'timezone': details.timezone
    }

    if details.latitude is not None and details.longitude is not None:
        params['latitude'] = details.latitude
        params['longitude'] = details.longitude

    return create_kundali(**params)


def extract_matching_data(kundali: Kundali) -> Dict[str, Any]:
    """Extract data needed for matching from a Kundali."""
    planets = kundali.planets
    lagna = kundali.lagna
    planets_in_houses = kundali.get_planets_in_houses()

    # Find Mars house from Lagna
    mars_house_from_lagna = 1
    for house, planet_list in planets_in_houses.items():
        if "MARS" in planet_list:
            mars_house_from_lagna = house
            break

    # Find Mars house from Moon
    moon_rashi_num = planets["MOON"]["rashi_num"]
    moon_nakshatra_num = planets["MOON"]["nakshatra_num"]
    mars_rashi = planets["MARS"]["rashi_num"]
    mars_house_from_moon = ((mars_rashi - moon_rashi_num) % 12) + 1

    # Get additional profile data for profile cards
    varna = RASHI_VARNA.get(moon_rashi_num)
    gana = NAKSHATRA_GANA.get(moon_nakshatra_num)
    nadi = NAKSHATRA_NADI.get(moon_nakshatra_num)
    yoni = NAKSHATRA_YONI.get(moon_nakshatra_num)
    nakshatra_lord = NAKSHATRAS[moon_nakshatra_num]["lord"] if moon_nakshatra_num < len(NAKSHATRAS) else ""

    return {
        "moon_rashi_num": moon_rashi_num,
        "moon_nakshatra_num": moon_nakshatra_num,
        "moon_degree": planets["MOON"]["rashi_degree"],
        "moon_rashi": planets["MOON"]["rashi"],
        "moon_nakshatra": planets["MOON"]["nakshatra"],
        "lagna_rashi": lagna["rashi"],
        "mars_rashi": planets["MARS"]["rashi"],
        "mars_house_from_lagna": mars_house_from_lagna,
        "mars_house_from_moon": mars_house_from_moon,
        "sun_rashi": planets["SUN"]["rashi"],
        # Additional profile data for profile cards
        "varna": varna.name if varna else "",
        "gana": gana.value if gana else "",
        "nadi": nadi.value if nadi else "",
        "yoni": yoni.value if yoni else "",
        "nakshatra_lord": nakshatra_lord,
    }


# =============================================================================
# API ENDPOINTS
# =============================================================================

@router.post(
    "/match",
    response_model=MatchResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input data"},
        500: {"model": ErrorResponse, "description": "Server error during matching"}
    },
    summary="Match two Kundalis for marriage compatibility",
    description="""
    Perform comprehensive Ashtakoot Milan (8-fold matching) for marriage compatibility.

    This endpoint analyzes compatibility across 8 factors:
    - **Varna** (1 point): Spiritual/ego compatibility
    - **Vashya** (2 points): Mutual attraction and control
    - **Tara** (3 points): Birth star compatibility, health
    - **Yoni** (4 points): Sexual/physical compatibility
    - **Graha Maitri** (5 points): Mental compatibility (Moon sign lords)
    - **Gana** (6 points): Temperament (Deva/Manushya/Rakshasa)
    - **Bhakoot** (7 points): Emotional compatibility, prosperity
    - **Nadi** (8 points): Health, genes, children

    Total: 36 points (Gunas)

    Also checks for:
    - Manglik Dosha
    - Nadi Dosha
    - Bhakoot Dosha
    - Gana Dosha

    Based on:
    - Brihat Parashara Hora Shastra
    - Muhurta Chintamani
    - Jataka Parijata
    """
)
async def match_kundalis(request: MatchRequest) -> MatchResponse:
    """
    Perform Kundali matching (Ashtakoot Milan) for two people.
    """
    try:
        # Create Kundalis for both
        boy_kundali = create_kundali_from_details(request.boy)
        girl_kundali = create_kundali_from_details(request.girl)

        # Extract matching data
        boy_data = extract_matching_data(boy_kundali)
        girl_data = extract_matching_data(girl_kundali)

        # Perform matching
        matcher = KundaliMatcher()
        result = matcher.match(
            boy_moon_rashi_num=boy_data["moon_rashi_num"],
            boy_moon_nakshatra_num=boy_data["moon_nakshatra_num"],
            boy_moon_degree=boy_data["moon_degree"],
            girl_moon_rashi_num=girl_data["moon_rashi_num"],
            girl_moon_nakshatra_num=girl_data["moon_nakshatra_num"],
            girl_moon_degree=girl_data["moon_degree"],
            boy_name=request.boy.name,
            girl_name=request.girl.name,
            boy_mars_house_from_lagna=boy_data["mars_house_from_lagna"],
            boy_mars_house_from_moon=boy_data["mars_house_from_moon"],
            boy_mars_rashi=boy_data["mars_rashi"],
            boy_lagna_rashi=boy_data["lagna_rashi"],
            girl_mars_house_from_lagna=girl_data["mars_house_from_lagna"],
            girl_mars_house_from_moon=girl_data["mars_house_from_moon"],
            girl_mars_rashi=girl_data["mars_rashi"],
            girl_lagna_rashi=girl_data["lagna_rashi"],
        )

        # Generate predictions
        predictions = generate_matching_predictions(result)

        # Generate HTML
        html_content = None
        try:
            html_content = generate_matching_html(result, predictions)
        except Exception as e:
            print(f"HTML generation error: {e}")

        # Build response
        koota_scores = [
            KootaScore(
                name=k.name,
                name_hindi=k.name_hindi,
                max_points=k.max_points,
                obtained_points=k.obtained_points,
                boy_value=k.boy_value,
                girl_value=k.girl_value,
                description=k.description,
                is_auspicious=k.is_auspicious,
                dosha=k.dosha
            )
            for k in result.koota_results
        ]

        doshas = []
        for pred_dosha in predictions.dosha_analysis:
            doshas.append(DoshaInfo(
                name=pred_dosha["name"],
                type=pred_dosha["type"],
                severity=pred_dosha["severity"],
                description=pred_dosha["description"],
                remedies=pred_dosha.get("remedies", []),
                is_cancelled=pred_dosha.get("is_cancelled", False)
            ))

        score_breakdown = MatchingScores(
            varna=result.detailed_analysis["score_breakdown"]["varna"],
            vashya=result.detailed_analysis["score_breakdown"]["vashya"],
            tara=result.detailed_analysis["score_breakdown"]["tara"],
            yoni=result.detailed_analysis["score_breakdown"]["yoni"],
            graha_maitri=result.detailed_analysis["score_breakdown"]["graha_maitri"],
            gana=result.detailed_analysis["score_breakdown"]["gana"],
            bhakoot=result.detailed_analysis["score_breakdown"]["bhakoot"],
            nadi=result.detailed_analysis["score_breakdown"]["nadi"],
        )

        # Build marriage timing
        marriage_timing_data = MarriageTiming(
            favorable_days=predictions.marriage_timing.get("favorable_days", []),
            favorable_months=predictions.marriage_timing.get("favorable_months", []),
            avoid=predictions.marriage_timing.get("avoid", []),
            general_advice=predictions.marriage_timing.get("general_advice", []),
        )

        # Build koota interpretations from predictions
        koota_interpretations = [
            KootaInterpretation(
                name=ki["name"],
                name_hindi=ki["name_hindi"],
                score=ki["score"],
                percentage=ki["percentage"],
                boy_value=ki["boy_value"],
                girl_value=ki["girl_value"],
                is_favorable=ki["is_favorable"],
                description=ki["description"],
                title=ki.get("title", ""),
                detailed_interpretation=ki.get("detailed_interpretation", ""),
                effects=ki.get("effects", []),
                remedies=ki.get("remedies", []),
                dosha=ki.get("dosha"),
                title_hindi=ki.get("title_hindi", ""),
                detailed_interpretation_hindi=ki.get("detailed_interpretation_hindi", ""),
                effects_hindi=ki.get("effects_hindi", [])
            )
            for ki in predictions.koota_interpretations
        ]

        return MatchResponse(
            success=True,
            boy_name=result.boy_name,
            girl_name=result.girl_name,
            total_points=result.total_points,
            percentage=result.percentage,
            compatibility_level=predictions.compatibility_level,
            koota_scores=koota_scores,
            koota_interpretations=koota_interpretations,
            doshas=doshas,
            score_breakdown=score_breakdown,
            recommendation=predictions.final_recommendation,
            remedies=predictions.remedies,
            areas_of_strength=predictions.areas_of_strength,
            areas_of_concern=predictions.areas_of_concern,
            boy_details={
                "name": request.boy.name,
                "dob": request.boy.dob,
                "birth_time": request.boy.tob,
                "city": request.boy.city,
                "moon_rashi": boy_data["moon_rashi"],
                "moon_nakshatra": boy_data["moon_nakshatra"],
                "lagna_rashi": boy_data["lagna_rashi"],
                "varna": boy_data["varna"],
                "gana": boy_data["gana"],
                "nadi": boy_data["nadi"],
                "yoni": boy_data["yoni"],
                "nakshatra_lord": boy_data["nakshatra_lord"],
            },
            girl_details={
                "name": request.girl.name,
                "dob": request.girl.dob,
                "birth_time": request.girl.tob,
                "city": request.girl.city,
                "moon_rashi": girl_data["moon_rashi"],
                "moon_nakshatra": girl_data["moon_nakshatra"],
                "lagna_rashi": girl_data["lagna_rashi"],
                "varna": girl_data["varna"],
                "gana": girl_data["gana"],
                "nadi": girl_data["nadi"],
                "yoni": girl_data["yoni"],
                "nakshatra_lord": girl_data["nakshatra_lord"],
            },
            marriage_timing=marriage_timing_data,
            html=html_content,
            message=f"Matching completed: {result.total_points}/36 points ({result.percentage}%)"
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during matching: {str(e)}"
        )


@router.post(
    "/match/quick",
    response_model=MatchResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input data"},
        404: {"model": ErrorResponse, "description": "Kundali not found"},
        500: {"model": ErrorResponse, "description": "Server error during matching"}
    },
    summary="Quick match using existing Kundali IDs",
    description="Match two existing kundalis by their IDs (if previously generated)."
)
async def quick_match(
    boy_kundali_id: str,
    girl_kundali_id: str
) -> MatchResponse:
    """
    Perform quick matching using existing Kundali IDs.
    """
    # Import here to avoid circular imports
    from .kundali import get_kundali, kundali_store

    try:
        boy_kundali = get_kundali(boy_kundali_id)
        girl_kundali = get_kundali(girl_kundali_id)

        # Extract matching data
        boy_data = extract_matching_data(boy_kundali)
        girl_data = extract_matching_data(girl_kundali)

        # Perform matching
        matcher = KundaliMatcher()
        result = matcher.match(
            boy_moon_rashi_num=boy_data["moon_rashi_num"],
            boy_moon_nakshatra_num=boy_data["moon_nakshatra_num"],
            boy_moon_degree=boy_data["moon_degree"],
            girl_moon_rashi_num=girl_data["moon_rashi_num"],
            girl_moon_nakshatra_num=girl_data["moon_nakshatra_num"],
            girl_moon_degree=girl_data["moon_degree"],
            boy_name=boy_kundali.birth_data.name,
            girl_name=girl_kundali.birth_data.name,
            boy_mars_house_from_lagna=boy_data["mars_house_from_lagna"],
            boy_mars_house_from_moon=boy_data["mars_house_from_moon"],
            boy_mars_rashi=boy_data["mars_rashi"],
            boy_lagna_rashi=boy_data["lagna_rashi"],
            girl_mars_house_from_lagna=girl_data["mars_house_from_lagna"],
            girl_mars_house_from_moon=girl_data["mars_house_from_moon"],
            girl_mars_rashi=girl_data["mars_rashi"],
            girl_lagna_rashi=girl_data["lagna_rashi"],
        )

        # Generate predictions
        predictions = generate_matching_predictions(result)

        # Generate HTML
        html_content = None
        try:
            html_content = generate_matching_html(result, predictions)
        except Exception as e:
            print(f"HTML generation error: {e}")

        # Build response (same as above)
        koota_scores = [
            KootaScore(
                name=k.name,
                name_hindi=k.name_hindi,
                max_points=k.max_points,
                obtained_points=k.obtained_points,
                boy_value=k.boy_value,
                girl_value=k.girl_value,
                description=k.description,
                is_auspicious=k.is_auspicious,
                dosha=k.dosha
            )
            for k in result.koota_results
        ]

        doshas = []
        for pred_dosha in predictions.dosha_analysis:
            doshas.append(DoshaInfo(
                name=pred_dosha["name"],
                type=pred_dosha["type"],
                severity=pred_dosha["severity"],
                description=pred_dosha["description"],
                remedies=pred_dosha.get("remedies", []),
                is_cancelled=pred_dosha.get("is_cancelled", False)
            ))

        score_breakdown = MatchingScores(
            varna=result.detailed_analysis["score_breakdown"]["varna"],
            vashya=result.detailed_analysis["score_breakdown"]["vashya"],
            tara=result.detailed_analysis["score_breakdown"]["tara"],
            yoni=result.detailed_analysis["score_breakdown"]["yoni"],
            graha_maitri=result.detailed_analysis["score_breakdown"]["graha_maitri"],
            gana=result.detailed_analysis["score_breakdown"]["gana"],
            bhakoot=result.detailed_analysis["score_breakdown"]["bhakoot"],
            nadi=result.detailed_analysis["score_breakdown"]["nadi"],
        )

        # Build koota interpretations from predictions
        koota_interpretations = [
            KootaInterpretation(
                name=ki["name"],
                name_hindi=ki["name_hindi"],
                score=ki["score"],
                percentage=ki["percentage"],
                boy_value=ki["boy_value"],
                girl_value=ki["girl_value"],
                is_favorable=ki["is_favorable"],
                description=ki["description"],
                title=ki.get("title", ""),
                detailed_interpretation=ki.get("detailed_interpretation", ""),
                effects=ki.get("effects", []),
                remedies=ki.get("remedies", []),
                dosha=ki.get("dosha"),
                title_hindi=ki.get("title_hindi", ""),
                detailed_interpretation_hindi=ki.get("detailed_interpretation_hindi", ""),
                effects_hindi=ki.get("effects_hindi", [])
            )
            for ki in predictions.koota_interpretations
        ]

        # Build marriage timing
        marriage_timing_data = MarriageTiming(
            favorable_days=predictions.marriage_timing.get("favorable_days", []),
            favorable_months=predictions.marriage_timing.get("favorable_months", []),
            avoid=predictions.marriage_timing.get("avoid", []),
            general_advice=predictions.marriage_timing.get("general_advice", []),
        )

        return MatchResponse(
            success=True,
            boy_name=boy_kundali.birth_data.name,
            girl_name=girl_kundali.birth_data.name,
            total_points=result.total_points,
            percentage=result.percentage,
            compatibility_level=predictions.compatibility_level,
            koota_scores=koota_scores,
            koota_interpretations=koota_interpretations,
            doshas=doshas,
            score_breakdown=score_breakdown,
            recommendation=predictions.final_recommendation,
            remedies=predictions.remedies,
            areas_of_strength=predictions.areas_of_strength,
            areas_of_concern=predictions.areas_of_concern,
            boy_details={
                "name": boy_kundali.birth_data.name,
                "dob": boy_kundali.birth_data.date.strftime("%Y-%m-%d"),
                "birth_time": boy_kundali.birth_data.time.strftime("%H:%M") if hasattr(boy_kundali.birth_data, 'time') else "",
                "city": boy_kundali.birth_data.city,
                "moon_rashi": boy_data["moon_rashi"],
                "moon_nakshatra": boy_data["moon_nakshatra"],
                "lagna_rashi": boy_data["lagna_rashi"],
                "varna": boy_data["varna"],
                "gana": boy_data["gana"],
                "nadi": boy_data["nadi"],
                "yoni": boy_data["yoni"],
                "nakshatra_lord": boy_data["nakshatra_lord"],
            },
            girl_details={
                "name": girl_kundali.birth_data.name,
                "dob": girl_kundali.birth_data.date.strftime("%Y-%m-%d"),
                "birth_time": girl_kundali.birth_data.time.strftime("%H:%M") if hasattr(girl_kundali.birth_data, 'time') else "",
                "city": girl_kundali.birth_data.city,
                "moon_rashi": girl_data["moon_rashi"],
                "moon_nakshatra": girl_data["moon_nakshatra"],
                "lagna_rashi": girl_data["lagna_rashi"],
                "varna": girl_data["varna"],
                "gana": girl_data["gana"],
                "nadi": girl_data["nadi"],
                "yoni": girl_data["yoni"],
                "nakshatra_lord": girl_data["nakshatra_lord"],
            },
            marriage_timing=marriage_timing_data,
            html=html_content,
            message=f"Matching completed: {result.total_points}/36 points ({result.percentage}%)"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during matching: {str(e)}"
        )

