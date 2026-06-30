"""
Career and Finance Analysis API Routes
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
    from src.career_finance import CareerFinanceAnalyzer, analyze_career_finance
except ImportError:
    CareerFinanceAnalyzer = None
    analyze_career_finance = None

router = APIRouter(prefix="/api/career", tags=["Career & Finance"])


class CareerRequest(BaseModel):
    """Request model for career analysis"""
    kundali_data: Dict[str, Any]


@router.post("/analyze")
async def analyze_career(request: CareerRequest):
    """
    Analyze career and finance based on Kundali.

    Based on:
    - BPHS Dhana Yoga chapter
    - Phaladeepika Raja Yoga and Dhana Yoga
    - 10th house and its lord analysis

    Returns:
    - Career recommendations
    - Dhana Yogas present
    - Wealth potential
    - Government/Business/Foreign career yogas
    """
    if analyze_career_finance is None:
        raise HTTPException(status_code=500, detail="Career finance module not available")

    try:
        result = analyze_career_finance(request.kundali_data)

        return {
            "success": True,
            "career_finance": {
                "career_analysis": {
                    "tenth_house_sign": result.career_analysis.tenth_house_sign,
                    "tenth_house_lord": result.career_analysis.tenth_house_lord,
                    "tenth_lord_house": result.career_analysis.tenth_lord_house,
                    "planets_in_tenth": result.career_analysis.planets_in_tenth,
                    "recommended_careers": result.career_analysis.recommended_careers,
                    "career_traits": result.career_analysis.career_traits,
                    "career_timing": result.career_analysis.career_timing,
                    "career_timing_hindi": result.career_analysis.career_timing_hindi,
                    "government_job_yoga": result.career_analysis.government_job_yoga,
                    "business_yoga": result.career_analysis.business_yoga,
                    "foreign_career_yoga": result.career_analysis.foreign_career_yoga
                },
                "dhana_yoga_analysis": {
                    "yogas_present": [
                        {
                            "name": y.name,
                            "name_hindi": y.name_hindi,
                            "strength": y.strength,
                            "description": y.description,
                            "description_hindi": y.description_hindi,
                            "effects": y.effects,
                            "effects_hindi": y.effects_hindi,
                            "planets_involved": y.planets_involved
                        }
                        for y in result.dhana_yoga_analysis.yogas_present
                    ],
                    "wealth_potential": result.dhana_yoga_analysis.wealth_potential,
                    "wealth_potential_hindi": result.dhana_yoga_analysis.wealth_potential_hindi,
                    "best_wealth_periods": result.dhana_yoga_analysis.best_wealth_periods,
                    "wealth_sources": result.dhana_yoga_analysis.wealth_sources,
                    "wealth_sources_hindi": result.dhana_yoga_analysis.wealth_sources_hindi,
                    "poverty_yogas": [
                        {
                            "name": y.name,
                            "name_hindi": y.name_hindi,
                            "description": y.description
                        }
                        for y in result.dhana_yoga_analysis.poverty_yogas
                    ]
                },
                "overall_career_score": result.overall_career_score,
                "overall_wealth_score": result.overall_wealth_score,
                "summary": result.summary,
                "summary_hindi": result.summary_hindi,
                "recommendations": result.recommendations,
                "recommendations_hindi": result.recommendations_hindi
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
