"""
Gemstone Recommendations API Routes
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import sys
from pathlib import Path

# Ensure parent directories are in path
backend_dir = Path(__file__).resolve().parent.parent.parent
kundali_dir = backend_dir.parent
if str(kundali_dir) not in sys.path:
    sys.path.insert(0, str(kundali_dir))

try:
    from src.gemstone_recommendations import GemstoneAdvisor, get_gemstone_for_planet, get_all_gemstones
except ImportError:
    GemstoneAdvisor = None
    get_gemstone_for_planet = None
    get_all_gemstones = None

try:
    from api.routes.kundali import get_kundali
except ImportError:
    get_kundali = None

router = APIRouter(prefix="/api/gemstone", tags=["Gemstone"])


class GemstoneRequest(BaseModel):
    """Request model for gemstone recommendations"""
    kundali_data: Dict[str, Any]


@router.post("/recommend")
async def recommend_gemstones(request: GemstoneRequest):
    """
    Get personalized gemstone recommendations based on Kundali.

    Based on:
    - Garuda Purana gemstone-planet mapping
    - Ratna Shastra principles
    - Weak/afflicted planet analysis

    Returns primary and substitute gemstones with wearing instructions.
    """
    if GemstoneAdvisor is None:
        raise HTTPException(status_code=500, detail="Gemstone module not available")

    try:
        advisor = GemstoneAdvisor(request.kundali_data)
        recommendations = advisor.get_primary_recommendations()

        return {
            "success": True,
            "recommendations": {
                "primary_gemstones": [
                    {
                        "planet": rec.planet,
                        "planet_hindi": rec.planet_hindi,
                        "gemstone": rec.gemstone.name_english,
                        "gemstone_hindi": rec.gemstone.name_hindi,
                        "substitute": rec.gemstone.alternative_stones,
                        "weight": f"{rec.gemstone.minimum_weight_ratti} रत्ती / {rec.gemstone.minimum_weight_carat} carat",
                        "metal": rec.gemstone.metal_hindi,
                        "finger": rec.gemstone.finger_hindi,
                        "day_to_wear": rec.gemstone.day_hindi,
                        "mantra": rec.gemstone.mantra,
                        "benefits": rec.gemstone.benefits,
                        "benefits_hindi": rec.gemstone.benefits,
                        "precautions": rec.gemstone.precautions,
                        "precautions_hindi": rec.gemstone.precautions,
                        "reason": rec.reason,
                        "reason_hindi": rec.reason_hindi,
                        "priority": rec.priority_label_hindi
                    }
                    for rec in recommendations
                ],
                "general_advice": "Consult a qualified astrologer before wearing gemstones.",
                "general_advice_hindi": "रत्न धारण करने से पहले योग्य ज्योतिषी से परामर्श लें।"
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class GemstoneByIdRequest(BaseModel):
    """Request model for gemstone by kundali_id"""
    kundali_id: str


@router.post("/analyze")
async def analyze_gemstones(request: GemstoneByIdRequest):
    """
    Get personalized gemstone recommendations using kundali_id.

    This endpoint uses the proper Kundali object for accurate analysis.
    """
    if GemstoneAdvisor is None:
        raise HTTPException(status_code=500, detail="Gemstone module not available")

    if get_kundali is None:
        raise HTTPException(status_code=500, detail="Kundali module not available")

    try:
        # Get the Kundali object
        kundali = get_kundali(request.kundali_id)

        # Get recommendations using the Kundali object
        advisor = GemstoneAdvisor(kundali)
        recommendations = advisor.get_primary_recommendations()

        return {
            "success": True,
            "recommendations": {
                "primary_gemstones": [
                    {
                        "planet": rec.planet,
                        "planet_hindi": rec.planet_hindi,
                        "gemstone": rec.gemstone.name_english,
                        "gemstone_hindi": rec.gemstone.name_hindi,
                        "substitute": rec.gemstone.alternative_stones,
                        "weight": f"{rec.gemstone.minimum_weight_ratti} रत्ती / {rec.gemstone.minimum_weight_carat} carat",
                        "metal": rec.gemstone.metal_hindi,
                        "finger": rec.gemstone.finger_hindi,
                        "day_to_wear": rec.gemstone.day_hindi,
                        "mantra": rec.gemstone.mantra,
                        "benefits": rec.gemstone.benefits,
                        "benefits_hindi": rec.gemstone.benefits,
                        "precautions": rec.gemstone.precautions,
                        "precautions_hindi": rec.gemstone.precautions,
                        "reason": rec.reason,
                        "reason_hindi": rec.reason_hindi,
                        "priority": rec.priority_label_hindi
                    }
                    for rec in recommendations
                ],
                "general_advice": "Consult a qualified astrologer before wearing gemstones.",
                "general_advice_hindi": "रत्न धारण करने से पहले योग्य ज्योतिषी से परामर्श लें।"
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/planet/{planet}")
async def get_planet_gemstone(planet: str):
    """
    Get gemstone information for a specific planet.
    """
    planet_gemstones = {
        "SUN": {
            "primary": "Ruby / माणिक्य",
            "substitute": ["Garnet / गार्नेट", "Red Spinel / लाल स्पिनेल"],
            "metal": "Gold / सोना",
            "finger": "Ring finger / अनामिका",
            "day": "Sunday / रविवार",
            "weight": "3-6 carats"
        },
        "MOON": {
            "primary": "Pearl / मोती",
            "substitute": ["Moonstone / मूनस्टोन"],
            "metal": "Silver / चांदी",
            "finger": "Little finger / कनिष्ठा",
            "day": "Monday / सोमवार",
            "weight": "4-6 carats"
        },
        "MARS": {
            "primary": "Red Coral / मूंगा",
            "substitute": ["Carnelian / कार्नेलियन"],
            "metal": "Gold or Copper / सोना या तांबा",
            "finger": "Ring finger / अनामिका",
            "day": "Tuesday / मंगलवार",
            "weight": "6-9 carats"
        },
        "MERCURY": {
            "primary": "Emerald / पन्ना",
            "substitute": ["Peridot / पेरीडॉट", "Green Tourmaline"],
            "metal": "Gold / सोना",
            "finger": "Little finger / कनिष्ठा",
            "day": "Wednesday / बुधवार",
            "weight": "3-6 carats"
        },
        "JUPITER": {
            "primary": "Yellow Sapphire / पुखराज",
            "substitute": ["Citrine / सिट्रीन", "Yellow Topaz"],
            "metal": "Gold / सोना",
            "finger": "Index finger / तर्जनी",
            "day": "Thursday / गुरुवार",
            "weight": "3-5 carats"
        },
        "VENUS": {
            "primary": "Diamond / हीरा",
            "substitute": ["White Zircon / सफेद जिरकॉन", "White Sapphire"],
            "metal": "Platinum or Gold / प्लैटिनम या सोना",
            "finger": "Middle finger / मध्यमा",
            "day": "Friday / शुक्रवार",
            "weight": "1-2 carats"
        },
        "SATURN": {
            "primary": "Blue Sapphire / नीलम",
            "substitute": ["Amethyst / अमेथिस्ट", "Blue Topaz"],
            "metal": "Iron or Panchdhatu / लोहा या पंचधातु",
            "finger": "Middle finger / मध्यमा",
            "day": "Saturday / शनिवार",
            "weight": "4-7 carats"
        },
        "RAHU": {
            "primary": "Hessonite / गोमेद",
            "substitute": ["Spessartite Garnet"],
            "metal": "Ashtadhatu / अष्टधातु",
            "finger": "Middle finger / मध्यमा",
            "day": "Saturday / शनिवार",
            "weight": "5-7 carats"
        },
        "KETU": {
            "primary": "Cat's Eye / लहसुनिया",
            "substitute": ["Tiger Eye / टाइगर आई"],
            "metal": "Panchdhatu / पंचधातु",
            "finger": "Middle finger / मध्यमा",
            "day": "Tuesday / मंगलवार",
            "weight": "4-6 carats"
        }
    }

    planet_upper = planet.upper()
    if planet_upper not in planet_gemstones:
        raise HTTPException(status_code=404, detail=f"Planet {planet} not found")

    return {
        "success": True,
        "planet": planet_upper,
        "gemstone": planet_gemstones[planet_upper]
    }
