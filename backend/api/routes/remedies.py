"""
Vedic Remedies API Routes
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import sys
from pathlib import Path

# Ensure parent directories are in path
backend_dir = Path(__file__).resolve().parent.parent.parent
kundali_dir = backend_dir.parent
if str(kundali_dir) not in sys.path:
    sys.path.insert(0, str(kundali_dir))

try:
    from src.remedies import RemedyAnalyzer, get_remedies
except ImportError:
    RemedyAnalyzer = None
    get_remedies = None

router = APIRouter(prefix="/api/remedies", tags=["Remedies"])


class RemediesRequest(BaseModel):
    """Request model for remedies"""
    kundali_data: Dict[str, Any]
    doshas: Optional[Dict[str, Any]] = None


class PlanetRemedyRequest(BaseModel):
    """Request for specific planet remedy"""
    kundali_data: Dict[str, Any]
    planet: str


@router.post("/comprehensive")
async def get_comprehensive_remedies(request: RemediesRequest):
    """
    Get comprehensive Vedic remedies based on Kundali.

    Based on:
    - BPHS Graha Shanti chapter
    - Lal Kitab remedies
    - Mantra Shastra
    - Ratna Shastra

    Returns:
    - Planet-specific remedies (mantras, gemstones, charity)
    - Dosha remedies
    - Daily/weekly/monthly routines
    """
    if get_remedies is None:
        raise HTTPException(status_code=500, detail="Remedies module not available")

    try:
        result = get_remedies(request.kundali_data, request.doshas)

        return {
            "success": True,
            "remedies": {
                "planet_remedies": [
                    {
                        "planet": r.planet,
                        "planet_hindi": r.planet_hindi,
                        "is_weak": r.is_weak,
                        "is_afflicted": r.is_afflicted,
                        "mantras": r.mantras,
                        "gemstone": r.gemstone,
                        "charity": r.charity,
                        "lal_kitab": r.lal_kitab,
                        "general_tips": r.general_tips
                    }
                    for r in result.planet_remedies
                ],
                "dosha_remedies": [
                    {
                        "dosha_name": d.dosha_name,
                        "dosha_name_hindi": d.dosha_name_hindi,
                        "severity": d.severity,
                        "mantras": d.mantras,
                        "temples": d.temples,
                        "rituals": d.rituals,
                        "charity": d.charity,
                        "lifestyle": d.lifestyle,
                        "timeline": d.timeline
                    }
                    for d in result.dosha_remedies
                ],
                "house_remedies": result.house_remedies,
                "priority_remedies": result.priority_remedies,
                "priority_remedies_hindi": result.priority_remedies_hindi,
                "daily_routine": result.daily_routine,
                "weekly_routine": result.weekly_routine,
                "monthly_routine": result.monthly_routine,
                "yearly_routine": result.yearly_routine
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/planet")
async def get_planet_remedies(request: PlanetRemedyRequest):
    """
    Get remedies for a specific planet.
    """
    if RemedyAnalyzer is None:
        raise HTTPException(status_code=500, detail="Remedies module not available")

    try:
        analyzer = RemedyAnalyzer(request.kundali_data)
        result = analyzer.get_planet_remedies(request.planet.upper())

        return {
            "success": True,
            "remedy": {
                "planet": result.planet,
                "planet_hindi": result.planet_hindi,
                "is_weak": result.is_weak,
                "is_afflicted": result.is_afflicted,
                "mantras": result.mantras,
                "gemstone": result.gemstone,
                "charity": result.charity,
                "lal_kitab": result.lal_kitab,
                "general_tips": result.general_tips
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dosha/{dosha_type}")
async def get_dosha_remedies(dosha_type: str):
    """
    Get standard remedies for a specific dosha type.
    """
    dosha_remedies = {
        "manglik": {
            "name_hindi": "मांगलिक दोष उपाय",
            "mantras": [
                "ॐ क्रां क्रीं क्रौं सः भौमाय नमः - 108 बार मंगलवार को",
                "हनुमान चालीसा पाठ - मंगलवार और शनिवार"
            ],
            "temples": ["हनुमान मंदिर / Hanuman temple"],
            "rituals": ["मंगल शांति पूजा / Mangal Shanti Puja", "कुंभ विवाह / Kumbh Vivah"],
            "charity": ["मंगलवार को लाल वस्तुओं का दान", "मसूर दाल, गुड़ का दान"],
            "gemstone": "मूंगा / Red Coral"
        },
        "kaal_sarp": {
            "name_hindi": "काल सर्प दोष उपाय",
            "mantras": [
                "महा मृत्युंजय मंत्र - 1.25 लाख जाप",
                "ॐ नमः शिवाय - प्रतिदिन 108 बार"
            ],
            "temples": ["त्र्यंबकेश्वर, नासिक", "महाकालेश्वर, उज्जैन"],
            "rituals": ["काल सर्प शांति पूजा", "रुद्राभिषेक"],
            "charity": ["काले तिल का दान", "सांपों की मूर्ति पर दूध"],
            "gemstone": "गोमेद / Hessonite"
        },
        "pitra": {
            "name_hindi": "पितृ दोष उपाय",
            "mantras": ["पितृ गायत्री मंत्र", "ॐ पितृभ्यो नमः"],
            "temples": ["गया में पिंड दान", "त्रयंबकेश्वर"],
            "rituals": ["श्राद्ध", "तर्पण", "पिंड दान"],
            "charity": ["ब्राह्मण भोजन", "गौ दान"],
            "gemstone": "मोती / Pearl"
        },
        "sade_sati": {
            "name_hindi": "साढ़े साती उपाय",
            "mantras": ["शनि बीज मंत्र", "हनुमान चालीसा"],
            "temples": ["शनि शिंगणापुर", "शनि देव मंदिर, तिरुनलार"],
            "rituals": ["शनि शांति पूजा", "तैल अभिषेक"],
            "charity": ["शनिवार को काली वस्तुएं दान", "अंधों की सेवा"],
            "gemstone": "नीलम / Blue Sapphire (with caution)"
        }
    }

    dosha_lower = dosha_type.lower()
    if dosha_lower not in dosha_remedies:
        raise HTTPException(status_code=404, detail=f"Dosha {dosha_type} not found")

    return {
        "success": True,
        "dosha": dosha_lower,
        "remedies": dosha_remedies[dosha_lower]
    }
