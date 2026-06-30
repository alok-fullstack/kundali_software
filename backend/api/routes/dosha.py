"""
Dosha Analysis API Routes
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import sys
from pathlib import Path

# Ensure parent directories are in path
backend_dir = Path(__file__).resolve().parent.parent.parent
kundali_dir = backend_dir.parent
if str(kundali_dir) not in sys.path:
    sys.path.insert(0, str(kundali_dir))

try:
    from src.dosha_analysis import DoshaAnalyzer, analyze_doshas as analyze_doshas_func
except ImportError:
    DoshaAnalyzer = None
    analyze_doshas_func = None

router = APIRouter(prefix="/api/dosha", tags=["Dosha Analysis"])


class DoshaRequest(BaseModel):
    """Request model for dosha analysis"""
    kundali_data: Dict[str, Any]


class ManglikCheckRequest(BaseModel):
    """Request for Manglik dosha check only"""
    kundali_data: Dict[str, Any]


@router.post("/analyze")
async def analyze_doshas_endpoint(request: DoshaRequest):
    """
    Analyze all doshas in a Kundali.

    Returns analysis for:
    - Kaal Sarp Dosha (12 types)
    - Pitra Dosha
    - Sade Sati (3 phases)
    - Guru Chandal Yoga
    - Grahan Dosha
    - Manglik Dosha

    All content in Hindi/Hinglish.
    """
    if analyze_doshas_func is None:
        raise HTTPException(status_code=500, detail="Dosha analysis module not available")

    try:
        result = analyze_doshas_func(request.kundali_data)

        def safe_dosha(dosha, extra_fields=None):
            """Safely extract dosha fields"""
            if not dosha:
                return None
            base = {
                "is_present": getattr(dosha, 'is_present', False),
                "severity": str(getattr(dosha, 'severity', 'Unknown')),
                "effects": getattr(dosha, 'effects', []),
                "effects_hindi": getattr(dosha, 'effects_hindi', []),
                "remedies": getattr(dosha, 'remedies', []),
                "remedies_hindi": getattr(dosha, 'remedies_hindi', [])
            }
            if extra_fields:
                for field in extra_fields:
                    base[field] = getattr(dosha, field, None)
            return base

        return {
            "success": True,
            "dosha_analysis": {
                "kaal_sarp": safe_dosha(result.kaal_sarp, ['kaal_sarp_type', 'type_hindi']) if result.kaal_sarp else None,
                "pitra_dosha": safe_dosha(result.pitra_dosha, ['causes_hindi']) if result.pitra_dosha else None,
                "sade_sati": {
                    "is_active": getattr(result.sade_sati, 'is_active', False),
                    "phase": getattr(result.sade_sati, 'current_phase', ''),
                    "phase_hindi": getattr(result.sade_sati, 'phase_hindi', ''),
                    "effects": getattr(result.sade_sati, 'effects', []),
                    "effects_hindi": getattr(result.sade_sati, 'effects_hindi', []),
                    "remedies": getattr(result.sade_sati, 'remedies', []),
                    "remedies_hindi": getattr(result.sade_sati, 'remedies_hindi', [])
                } if result.sade_sati else None,
                "guru_chandal": safe_dosha(result.guru_chandal) if result.guru_chandal else None,
                "grahan_dosha": safe_dosha(result.grahan_dosha, ['grahan_type']) if result.grahan_dosha else None,
                "manglik": {
                    "is_manglik": getattr(result.manglik_dosha, 'is_present', False),
                    "severity": str(getattr(result.manglik_dosha, 'severity', 'None')),
                    "mars_house": getattr(result.manglik_dosha, 'mars_house', None),
                    "effects": getattr(result.manglik_dosha, 'effects', []),
                    "effects_hindi": getattr(result.manglik_dosha, 'effects_hindi', []),
                    "remedies": getattr(result.manglik_dosha, 'remedies', []),
                    "remedies_hindi": getattr(result.manglik_dosha, 'remedies_hindi', []),
                    "cancellation": getattr(result.manglik_dosha, 'cancellation_factors', [])
                } if result.manglik_dosha else None,
                "summary": result.summary,
                "summary_hindi": result.summary_hindi,
                "total_doshas": result.total_doshas_found,
                "severity_score": str(result.overall_severity) if result.overall_severity else "None"
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/manglik")
async def check_manglik(request: ManglikCheckRequest):
    """
    Check only Manglik dosha for marriage compatibility.
    """
    if DoshaAnalyzer is None:
        raise HTTPException(status_code=500, detail="Dosha analysis module not available")

    try:
        analyzer = DoshaAnalyzer(request.kundali_data)
        result = analyzer.check_manglik_dosha()

        return {
            "success": True,
            "manglik": {
                "is_manglik": getattr(result, 'is_present', False),
                "severity": str(getattr(result, 'severity', 'None')),
                "mars_house": getattr(result, 'mars_house', None),
                "effects": getattr(result, 'effects', []),
                "effects_hindi": getattr(result, 'effects_hindi', []),
                "remedies": getattr(result, 'remedies', []),
                "remedies_hindi": getattr(result, 'remedies_hindi', []),
                "cancellation_factors": getattr(result, 'cancellation_factors', [])
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
