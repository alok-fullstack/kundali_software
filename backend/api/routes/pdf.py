"""
PDF Export API Routes

Provides endpoints for downloading Kundali and Matching reports as PDF.

Endpoints:
- GET /api/kundali/{kundali_id}/pdf - Download Kundali PDF
- POST /api/matching/pdf - Download Matching PDF
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response
from pydantic import BaseModel, Field, field_validator

# Ensure parent directories are in path
backend_dir = Path(__file__).resolve().parent.parent.parent
kundali_dir = backend_dir.parent
if str(kundali_dir) not in sys.path:
    sys.path.insert(0, str(kundali_dir))

from src.kundali import create_kundali, Kundali
from src.kundali_matching import KundaliMatcher
from src.pdf_generator import generate_kundali_pdf, generate_matching_pdf
from src.matching_predictions import generate_matching_predictions

# Import kundali store from kundali routes
from .kundali import get_kundali, kundali_store, kundali_params

router = APIRouter(prefix="/api", tags=["PDF Export"])


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class PersonDetailsForPDF(BaseModel):
    """Birth details for one person (for PDF generation)."""
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


class MatchingPDFRequest(BaseModel):
    """Request model for generating Matching PDF."""
    boy: PersonDetailsForPDF = Field(..., description="Boy's birth details")
    girl: PersonDetailsForPDF = Field(..., description="Girl's birth details")

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


class ErrorResponse(BaseModel):
    """Standard error response."""
    success: bool = False
    error: str
    detail: Optional[str] = None


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def create_kundali_from_details(details: PersonDetailsForPDF) -> Kundali:
    """Create a Kundali from PersonDetailsForPDF."""
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
    from src.kundali_matching import RASHI_VARNA, NAKSHATRA_GANA, NAKSHATRA_NADI, NAKSHATRA_YONI
    from src.config import NAKSHATRAS

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

    # Get additional profile data
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
        "varna": varna.name if varna else "",
        "gana": gana.value if gana else "",
        "nadi": nadi.value if nadi else "",
        "yoni": yoni.value if yoni else "",
        "nakshatra_lord": nakshatra_lord,
    }


# =============================================================================
# API ENDPOINTS
# =============================================================================

@router.get(
    "/kundali/{kundali_id}/pdf",
    responses={
        200: {
            "content": {"application/pdf": {}},
            "description": "PDF file containing the Kundali report"
        },
        404: {"model": ErrorResponse, "description": "Kundali not found"},
        500: {"model": ErrorResponse, "description": "Server error during PDF generation"}
    },
    summary="Download Kundali PDF Report",
    description="""
    Generate and download a professional PDF report for a previously generated Kundali.

    The PDF includes:
    - Birth details with coordinates
    - Visual Lagna Kundali (North Indian chart)
    - Planet positions table
    - Vimshottari Dasha periods
    - Yoga analysis (Panch Mahapurusha, Dhana yogas, etc.)
    - Dosha detection and status
    - Life areas summary (Career, Marriage, Health, Wealth)
    - Recommended remedies
    - Traditional Vedic styling with orange/saffron theme

    The report is bilingual (Hindi/English) and includes:
    - Om symbol header
    - Page numbers
    - Generation timestamp
    - Disclaimer
    """
)
async def download_kundali_pdf(kundali_id: str):
    """
    Download Kundali report as PDF.

    Args:
        kundali_id: The ID of a previously generated Kundali

    Returns:
        PDF file as response
    """
    try:
        # Get the kundali
        kundali = get_kundali(kundali_id)
        print(f"PDF: Got kundali for {kundali.birth_data.name}")

        # Generate PDF
        try:
            pdf_bytes = generate_kundali_pdf(kundali)
            print(f"PDF: Generated {len(pdf_bytes)} bytes")
        except Exception as pdf_error:
            print(f"PDF generation error: {pdf_error}")
            import traceback
            traceback.print_exc()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"PDF generation failed: {str(pdf_error)}"
            )

        # Create filename
        name_safe = kundali.birth_data.name.replace(' ', '_')[:20]
        filename = f"Kundali_{name_safe}_{datetime.now().strftime('%Y%m%d')}.pdf"

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"PDF endpoint error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating PDF: {str(e)}"
        )


@router.post(
    "/kundali/pdf",
    responses={
        200: {
            "content": {"application/pdf": {}},
            "description": "PDF file containing the Kundali report"
        },
        400: {"model": ErrorResponse, "description": "Invalid input data"},
        500: {"model": ErrorResponse, "description": "Server error during PDF generation"}
    },
    summary="Generate Kundali PDF from parameters",
    description="Generate PDF by providing birth details directly (no kundali_id needed)"
)
async def generate_kundali_pdf_direct(request: PersonDetailsForPDF):
    """
    Generate Kundali PDF directly from birth parameters.
    This is useful when the stored kundali is no longer available.
    """
    try:
        # Parse date and time
        dob_parts = request.dob.split('-')
        tob_parts = request.tob.split(':')

        # Create kundali
        kundali = create_kundali(
            name=request.name,
            year=int(dob_parts[0]),
            month=int(dob_parts[1]),
            day=int(dob_parts[2]),
            hour=int(tob_parts[0]),
            minute=int(tob_parts[1]),
            city=request.city,
            latitude=request.latitude,
            longitude=request.longitude,
            timezone=request.timezone
        )

        print(f"PDF Direct: Created kundali for {request.name}")

        # Generate PDF
        try:
            pdf_bytes = generate_kundali_pdf(kundali)
            print(f"PDF Direct: Generated {len(pdf_bytes)} bytes")
        except Exception as pdf_error:
            print(f"PDF generation error: {pdf_error}")
            import traceback
            traceback.print_exc()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"PDF generation failed: {str(pdf_error)}"
            )

        # Create filename
        name_safe = request.name.replace(' ', '_')[:20]
        filename = f"Kundali_{name_safe}_{datetime.now().strftime('%Y%m%d')}.pdf"

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"PDF direct endpoint error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating PDF: {str(e)}"
        )


@router.post(
    "/matching/pdf",
    responses={
        200: {
            "content": {"application/pdf": {}},
            "description": "PDF file containing the Matching report"
        },
        400: {"model": ErrorResponse, "description": "Invalid input data"},
        500: {"model": ErrorResponse, "description": "Server error during PDF generation"}
    },
    summary="Download Kundali Matching PDF Report",
    description="""
    Generate and download a professional PDF report for Kundali matching (marriage compatibility).

    The PDF includes:
    - Both persons' birth details side by side
    - Compatibility score gauge with percentage
    - Detailed Ashtakoot Milan table (8 Kootas)
    - Individual Koota analysis with interpretations
    - Dosha detection (Manglik, Nadi, Bhakoot)
    - Marriage timing suggestions
    - Final recommendation
    - Areas of strength and concern
    - Recommended remedies
    - Traditional Vedic styling

    The report is bilingual (Hindi/English) and includes:
    - Om symbol header
    - Page numbers
    - Generation timestamp
    - Disclaimer

    Based on:
    - Brihat Parashara Hora Shastra
    - Muhurta Chintamani
    - Jataka Parijata
    """
)
async def download_matching_pdf(request: MatchingPDFRequest):
    """
    Generate and download Kundali Matching report as PDF.

    Args:
        request: Birth details for boy and girl

    Returns:
        PDF file as response
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

        # Build match result dictionary for PDF generator
        match_result = {
            "total_points": result.total_points,
            "max_points": 36.0,
            "percentage": result.percentage,
            "compatibility_level": predictions.compatibility_level,
            "koota_scores": [
                {
                    "name": k.name,
                    "name_hindi": k.name_hindi,
                    "max_points": k.max_points,
                    "obtained_points": k.obtained_points,
                    "boy_value": k.boy_value,
                    "girl_value": k.girl_value,
                    "description": k.description,
                    "is_auspicious": k.is_auspicious,
                    "dosha": k.dosha
                }
                for k in result.koota_results
            ],
            "koota_interpretations": predictions.koota_interpretations,
            "doshas": predictions.dosha_analysis,
            "recommendation": predictions.final_recommendation,
            "remedies": predictions.remedies,
            "areas_of_strength": predictions.areas_of_strength,
            "areas_of_concern": predictions.areas_of_concern,
            "marriage_timing": predictions.marriage_timing,
        }

        # Build boy details for PDF
        boy_details = {
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
        }

        # Build girl details for PDF
        girl_details = {
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
        }

        # Generate PDF
        pdf_bytes = generate_matching_pdf(match_result, boy_details, girl_details)

        # Create filename
        boy_name_safe = request.boy.name.replace(' ', '_')[:10]
        girl_name_safe = request.girl.name.replace(' ', '_')[:10]
        filename = f"Matching_{boy_name_safe}_{girl_name_safe}_{datetime.now().strftime('%Y%m%d')}.pdf"

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating PDF: {str(e)}"
        )


@router.post(
    "/kundali/pdf",
    responses={
        200: {
            "content": {"application/pdf": {}},
            "description": "PDF file containing the Kundali report"
        },
        400: {"model": ErrorResponse, "description": "Invalid input data"},
        500: {"model": ErrorResponse, "description": "Server error during PDF generation"}
    },
    summary="Generate Kundali PDF from birth details",
    description="""
    Generate and download a Kundali PDF report directly from birth details
    (without requiring a pre-generated kundali_id).

    Useful for one-off PDF generation without storing the kundali.
    """
)
async def generate_kundali_pdf_direct(request: PersonDetailsForPDF):
    """
    Generate Kundali PDF directly from birth details.

    Args:
        request: Birth details

    Returns:
        PDF file as response
    """
    try:
        # Create Kundali
        kundali = create_kundali_from_details(request)

        # Generate PDF
        pdf_bytes = generate_kundali_pdf(kundali)

        # Create filename
        name_safe = request.name.replace(' ', '_')[:20]
        filename = f"Kundali_{name_safe}_{datetime.now().strftime('%Y%m%d')}.pdf"

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating PDF: {str(e)}"
        )
