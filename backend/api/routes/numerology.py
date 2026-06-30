"""
Numerology (Ank Jyotish) API routes.

POST /api/numerology/analyze - Get complete numerology analysis
POST /api/numerology/compatibility - Check compatibility between two people
POST /api/numerology/business - Analyze business name compatibility
POST /api/numerology/suggest-name - Get name correction suggestions
"""

import sys
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

# Ensure parent directories are in path
backend_dir = Path(__file__).resolve().parent.parent.parent
kundali_dir = backend_dir.parent
if str(kundali_dir) not in sys.path:
    sys.path.insert(0, str(kundali_dir))

from src.numerology import (
    NumerologyCalculator,
    calculate_numerology,
    get_compatibility,
    suggest_name_correction,
    analyze_business_name,
)

router = APIRouter(prefix="/api/numerology", tags=["Numerology"])


# =============================================================================
# Request/Response Models
# =============================================================================

class NumerologyRequest(BaseModel):
    """Request for numerology analysis."""
    name: str = Field(..., min_length=1, description="Person's full name")
    birth_date: str = Field(..., description="Date of birth in YYYY-MM-DD format")


class CompatibilityRequest(BaseModel):
    """Request for compatibility analysis."""
    person1_name: str = Field(..., min_length=1, description="First person's name")
    person1_dob: str = Field(..., description="First person's DOB (YYYY-MM-DD)")
    person2_name: str = Field(..., min_length=1, description="Second person's name")
    person2_dob: str = Field(..., description="Second person's DOB (YYYY-MM-DD)")


class BusinessNameRequest(BaseModel):
    """Request for business name analysis."""
    business_name: str = Field(..., min_length=1, description="Business name")
    owner_dob: str = Field(..., description="Owner's DOB (YYYY-MM-DD)")


class NameSuggestionRequest(BaseModel):
    """Request for name correction suggestions."""
    name: str = Field(..., min_length=1, description="Current name")
    birth_date: str = Field(..., description="DOB (YYYY-MM-DD)")
    target_number: Optional[int] = Field(None, ge=1, le=9, description="Target number (1-9)")


# =============================================================================
# API Endpoints
# =============================================================================

@router.post(
    "/analyze",
    summary="Complete Numerology Analysis",
    description="""
    Get complete numerology analysis including:
    - Moolank (Root Number) from birth date
    - Bhagyank (Destiny Number) from full DOB
    - Namank (Name Number) using Chaldean & Pythagorean systems
    - Personality traits based on Moolank
    - Life path description based on Bhagyank
    - Lucky numbers, colors, days, and gemstone
    - Friendly and unfriendly numbers
    - Detailed name analysis with letter breakdown
    """
)
async def analyze_numerology(request: NumerologyRequest):
    """
    Calculate complete numerology analysis for a person.

    Based on:
    - Vedic Numerology (Ank Shastra)
    - Cheiro's Numerology
    - Indian Ank Jyotish traditions
    """
    try:
        result = calculate_numerology(request.name, request.birth_date)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid date format. Use YYYY-MM-DD. Error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Numerology calculation failed: {str(e)}"
        )


@router.post(
    "/compatibility",
    summary="Number Compatibility Analysis",
    description="""
    Calculate numerological compatibility between two people.

    Analyzes:
    - Moolank (Root Number) compatibility
    - Bhagyank (Destiny Number) compatibility
    - Name Number compatibility

    Returns:
    - Compatibility score (0-100%)
    - Compatibility level (Excellent/Good/Average/Low)
    - Strengths and challenges
    - Remedies if needed
    """
)
async def check_compatibility(request: CompatibilityRequest):
    """
    Check numerological compatibility between two people.

    Uses Vedic number relationships based on planetary friendships.
    """
    try:
        result = get_compatibility(
            request.person1_name, request.person1_dob,
            request.person2_name, request.person2_dob
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid date format. Use YYYY-MM-DD. Error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Compatibility calculation failed: {str(e)}"
        )


@router.post(
    "/business",
    summary="Business Name Analysis",
    description="""
    Analyze a business name for numerological compatibility with the owner.

    Checks:
    - Business name number (Chaldean & Pythagorean)
    - Compatibility with owner's Moolank and Bhagyank
    - Whether the number is auspicious for business (1, 3, 5, 6, 9)

    Returns:
    - Compatibility level
    - Ruling planet of business name
    - Recommendations for improvement
    - Lucky days and colors for business
    """
)
async def analyze_business(request: BusinessNameRequest):
    """
    Analyze business name compatibility with owner.

    Based on Vedic numerology principles for business success.
    """
    try:
        result = analyze_business_name(request.business_name, request.owner_dob)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid date format. Use YYYY-MM-DD. Error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Business name analysis failed: {str(e)}"
        )


@router.post(
    "/suggest-name",
    summary="Name Correction Suggestions",
    description="""
    Suggest name corrections for better numerological vibration.

    Strategies used:
    - Adding letters at the end
    - Adding letters at the beginning
    - Doubling letters

    If target_number is not specified, suggestions are made
    to make the name compatible with Moolank and Bhagyank.

    Returns top 5 unique suggestions with:
    - Original and suggested name
    - Original and new number
    - Change description
    - Benefit of the change
    """
)
async def suggest_names(request: NameSuggestionRequest):
    """
    Get name correction suggestions for better numerology.

    Helps improve name vibration by targeting auspicious numbers.
    """
    try:
        suggestions = suggest_name_correction(
            request.name,
            request.birth_date,
            request.target_number
        )
        return suggestions
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid date format. Use YYYY-MM-DD. Error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Name suggestion failed: {str(e)}"
        )


@router.get(
    "/number/{number}",
    summary="Get Number Details",
    description="Get detailed information about a specific number (1-9)."
)
async def get_number_info(number: int):
    """
    Get detailed information about a specific number.

    Includes:
    - Ruling planet
    - Personality traits
    - Lucky colors, days
    - Gemstone
    - Friendly and unfriendly numbers
    """
    if number < 1 or number > 9:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Number must be between 1 and 9"
        )

    calculator = NumerologyCalculator()

    planet = calculator.get_planet_for_number(number)
    personality = calculator.get_personality_traits(number)
    life_path = calculator.get_life_path_description(number)
    colors = calculator.get_lucky_colors(number)
    days = calculator.get_lucky_days(number)
    gemstone = calculator.get_lucky_gemstone(number)
    friends = calculator.get_friendly_numbers(number)
    enemies = calculator.get_unfriendly_numbers(number)

    return {
        "number": number,
        "planet": {
            "name": planet["planet"],
            "sanskrit": planet["sanskrit"],
            "hindi": planet["hindi"],
        },
        "personality": {
            "traits": personality["traits"],
            "description": personality["description"],
        },
        "life_path": life_path,
        "lucky_elements": {
            "colors": colors,
            "days": days,
            "gemstone": {
                "name": gemstone["name"],
                "sanskrit": gemstone["sanskrit"],
                "planet": gemstone["planet"],
            },
        },
        "relationships": {
            "friendly_numbers": friends,
            "unfriendly_numbers": enemies,
        },
    }
