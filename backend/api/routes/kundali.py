"""
Kundali generation API route.

POST /api/generate - Create a new kundali from birth details.
"""

import sys
from pathlib import Path
import secrets
from datetime import datetime
from typing import Dict

from fastapi import APIRouter, HTTPException, status

# Ensure parent directories are in path
backend_dir = Path(__file__).resolve().parent.parent.parent
kundali_dir = backend_dir.parent
if str(kundali_dir) not in sys.path:
    sys.path.insert(0, str(kundali_dir))

from api.models import (
    KundaliRequest,
    KundaliGenerateResponse,
    KundaliResponse,
    PlanetPosition,
    HouseInfo,
    MahadashaInfo,
    ErrorResponse,
)
from src.kundali import create_kundali, Kundali
from src.config import PLANET_NAMES, Planet, BHAVA_NAMES, RASHIS
from api.html_generator import generate_kundali_html

router = APIRouter(prefix="/api", tags=["Kundali"])

# In-memory storage for kundalis (in production, use Redis or a database)
kundali_store: Dict[str, Kundali] = {}
kundali_params: Dict[str, dict] = {}  # Store params for recreation


def get_kundali(kundali_id: str) -> Kundali:
    """Get kundali from store or raise 404."""
    if kundali_id not in kundali_store:
        # Try to recreate from params
        if kundali_id in kundali_params:
            params = kundali_params[kundali_id]
            kundali = create_kundali(**params)
            kundali_store[kundali_id] = kundali
            return kundali
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Kundali with id '{kundali_id}' not found. Please generate a new kundali."
        )
    return kundali_store[kundali_id]


def build_kundali_response(kundali: Kundali) -> KundaliResponse:
    """Build KundaliResponse from Kundali object."""
    planets = kundali.planets
    lagna = kundali.lagna
    planets_in_houses = kundali.get_planets_in_houses()
    houses = kundali.houses
    current_dasha = kundali.get_current_dasha()
    mahadashas = kundali.get_mahadashas(years=100)
    birth = kundali.birth_data

    # Build planet positions with house numbers
    planet_positions = {}
    for p_name, p_data in planets.items():
        # Find house for this planet
        house_num = 1
        for h, p_list in planets_in_houses.items():
            if p_name in p_list:
                house_num = h
                break

        planet_positions[p_name] = PlanetPosition(
            name=p_name,
            rashi=p_data["rashi"],
            rashi_english=p_data.get("rashi_english", p_data["rashi"]),
            rashi_degree=round(p_data["rashi_degree"], 4),
            nakshatra=p_data["nakshatra"],
            pada=p_data["pada"],
            longitude=round(p_data["longitude"], 4),
            is_retrograde=p_data["is_retrograde"],
            house=house_num
        )

    # Build house info
    house_info_list = []
    lagna_num = lagna["rashi_num"]
    for i in range(1, 13):
        rashi_num = (lagna_num + i - 1) % 12
        rashi_data = RASHIS[rashi_num]
        house_planets = planets_in_houses.get(i, [])

        house_info_list.append(HouseInfo(
            house=i,
            name=BHAVA_NAMES[i]["name"],
            significance=BHAVA_NAMES[i]["significance"],
            rashi=rashi_data["name"],
            rashi_english=rashi_data["english"],
            planets=house_planets
        ))

    # Build mahadasha list
    maha_list = []
    for m in mahadashas[:10]:  # First 10 mahadashas
        maha_list.append(MahadashaInfo(
            planet=m.planet,
            start_date=m.start_date.strftime("%Y-%m-%d"),
            end_date=m.end_date.strftime("%Y-%m-%d")
        ))

    # Convert planets_in_houses keys to strings for JSON
    pih_str_keys = {str(k): v for k, v in planets_in_houses.items()}

    return KundaliResponse(
        name=birth.name,
        birth_date=birth.date.strftime("%Y-%m-%d"),
        birth_time=birth.date.strftime("%H:%M"),
        birth_city=birth.city,
        latitude=birth.latitude,
        longitude=birth.longitude,
        timezone=birth.timezone,
        lagna_rashi=lagna["rashi"],
        lagna_rashi_english=lagna["rashi_english"],
        lagna_degree=round(lagna["rashi_degree"], 4),
        lagna_nakshatra=lagna["nakshatra"],
        lagna_pada=lagna["pada"],
        moon_rashi=planets["MOON"]["rashi"],
        moon_nakshatra=planets["MOON"]["nakshatra"],
        moon_pada=planets["MOON"]["pada"],
        sun_rashi=planets["SUN"]["rashi"],
        planets=planet_positions,
        houses=house_info_list,
        planets_in_houses=pih_str_keys,
        current_dasha=current_dasha,
        full_dasha=current_dasha["full_dasha"],
        mahadashas=maha_list
    )


@router.post(
    "/generate",
    response_model=KundaliGenerateResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input data"},
        500: {"model": ErrorResponse, "description": "Server error during kundali generation"}
    },
    summary="Generate a new Kundali",
    description="Create a complete Vedic birth chart (Kundali) from birth details."
)
async def generate_kundali(request: KundaliRequest) -> KundaliGenerateResponse:
    """
    Generate a new Kundali (Vedic birth chart).

    This endpoint creates a complete horoscope with:
    - Lagna (Ascendant) calculation
    - All 9 planet positions (Navagraha)
    - 12 house positions (Bhava)
    - Vimshottari Dasha periods
    - Nakshatra details

    The generated kundali is stored in memory with a unique ID for use in
    subsequent chat, muhurta, and health prediction requests.
    """
    try:
        # Parse date and time
        dob_parts = request.dob.split('-')
        tob_parts = request.tob.split(':')

        year = int(dob_parts[0])
        month = int(dob_parts[1])
        day = int(dob_parts[2])
        hour = int(tob_parts[0])
        minute = int(tob_parts[1])

        # Build params dict for storage/recreation
        params = {
            'name': request.name,
            'year': year,
            'month': month,
            'day': day,
            'hour': hour,
            'minute': minute,
            'city': request.city,
            'timezone': request.timezone
        }

        if request.latitude is not None and request.longitude is not None:
            params['latitude'] = request.latitude
            params['longitude'] = request.longitude

        # Create kundali
        kundali = create_kundali(**params)

        # Generate unique ID and store
        kundali_id = secrets.token_hex(8)
        kundali_store[kundali_id] = kundali
        kundali_params[kundali_id] = params

        # Build response
        kundali_response = build_kundali_response(kundali)

        # Generate HTML for frontend display
        html_content = None
        try:
            html_content = generate_kundali_html(kundali)
        except Exception as e:
            print(f"HTML generation error: {e}")  # Log error but continue

        return KundaliGenerateResponse(
            success=True,
            kundali_id=kundali_id,
            kundali=kundali_response,
            html=html_content,
            message=f"Kundali for {request.name} generated successfully"
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating kundali: {str(e)}"
        )


@router.get(
    "/kundali/{kundali_id}",
    response_model=KundaliGenerateResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Kundali not found"}
    },
    summary="Get an existing Kundali",
    description="Retrieve a previously generated Kundali by its ID."
)
async def get_kundali_by_id(kundali_id: str) -> KundaliGenerateResponse:
    """Get an existing kundali by ID."""
    kundali = get_kundali(kundali_id)
    kundali_response = build_kundali_response(kundali)

    return KundaliGenerateResponse(
        success=True,
        kundali_id=kundali_id,
        kundali=kundali_response,
        message="Kundali retrieved successfully"
    )


def get_kundali_analysis_data(kundali: Kundali) -> Dict:
    """
    Convert Kundali object to dictionary format expected by analysis modules.

    Returns a dict with planets, lagna, houses data suitable for
    dosha analysis, remedies, career analysis etc.
    """
    planets_dict = {}
    for p_name, p_data in kundali.planets.items():
        planets_dict[p_name] = {
            "rashi": p_data["rashi"],
            "rashi_num": p_data.get("rashi_num", 0),
            "rashi_degree": p_data["rashi_degree"],
            "nakshatra": p_data["nakshatra"],
            "nakshatra_num": p_data.get("nakshatra_num", 0),
            "pada": p_data["pada"],
            "longitude": p_data["longitude"],
            "is_retrograde": p_data["is_retrograde"],
            "is_debilitated": p_data.get("is_debilitated", False),
            "is_exalted": p_data.get("is_exalted", False),
            "dignity": p_data.get("dignity", ""),
            "is_combust": p_data.get("is_combust", False)
        }

    lagna = kundali.lagna
    houses = kundali.get_planets_in_houses()

    return {
        "planets": planets_dict,
        "lagna": {
            "rashi": lagna["rashi"],
            "rashi_num": lagna.get("rashi_num", 0),
            "rashi_degree": lagna["rashi_degree"],
            "nakshatra": lagna["nakshatra"],
            "pada": lagna["pada"]
        },
        "houses": {str(k): v for k, v in houses.items()},
        "birth_data": {
            "name": kundali.birth_data.name,
            "date": kundali.birth_data.date.isoformat(),
            "city": kundali.birth_data.city,
            "latitude": kundali.birth_data.latitude,
            "longitude": kundali.birth_data.longitude
        }
    }


@router.get(
    "/kundali/{kundali_id}/data",
    summary="Get Kundali data for analysis",
    description="Get raw Kundali data in format suitable for dosha, career, remedies analysis."
)
async def get_kundali_data(kundali_id: str):
    """Get kundali data dictionary for analysis modules."""
    kundali = get_kundali(kundali_id)
    return {
        "success": True,
        "kundali_id": kundali_id,
        "kundali_data": get_kundali_analysis_data(kundali)
    }
