"""
Divisional Charts (Varga) API routes.

Endpoints for calculating and retrieving divisional charts based on BPHS.
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel, Field

# Ensure parent directories are in path
backend_dir = Path(__file__).resolve().parent.parent.parent
kundali_dir = backend_dir.parent
if str(kundali_dir) not in sys.path:
    sys.path.insert(0, str(kundali_dir))

from api.routes.kundali import get_kundali
from src.divisional_charts import (
    DivisionalChartCalculator, VargaChart, DivisionalChart,
    get_varga_chart_for_kundali, get_all_varga_charts_for_kundali,
    get_planet_vimshopaka_bala, VimshopakaBala
)
from src.varga_predictions import VargaPredictionEngine


router = APIRouter(prefix="/api/varga", tags=["Divisional Charts"])


# =============================================================================
# RESPONSE MODELS
# =============================================================================

class DivisionalPositionResponse(BaseModel):
    """Position of a planet in a divisional chart."""
    planet: str
    original_longitude: float
    original_rashi: str
    original_degree: float
    varga_rashi: str
    varga_rashi_english: str
    varga_degree: float
    division_number: int
    is_own_sign: bool
    is_exalted: bool
    is_debilitated: bool


class DivisionalChartResponse(BaseModel):
    """Complete divisional chart data."""
    varga_name: str
    varga_description: str
    division_count: int
    lagna: DivisionalPositionResponse
    planets: Dict[str, DivisionalPositionResponse]
    planets_in_houses: Dict[str, List[str]]


class VargaListResponse(BaseModel):
    """Response for listing all varga charts."""
    success: bool
    kundali_id: str
    charts: Dict[str, DivisionalChartResponse]
    message: str = ""


class SingleVargaResponse(BaseModel):
    """Response for a single varga chart."""
    success: bool
    kundali_id: str
    varga_type: str
    chart: DivisionalChartResponse
    message: str = ""


class VimshopakaBalaDetail(BaseModel):
    """Detail for one varga in Vimshopaka calculation."""
    rashi: str
    dignity_points: float
    weight: float
    weighted_points: float


class PlanetVimshopakaBala(BaseModel):
    """Vimshopaka strength for a single planet."""
    total_points: float
    max_points: float
    percentage: float
    details: Dict[str, VimshopakaBalaDetail]


class VimshopakaBalaResponse(BaseModel):
    """Response for Vimshopaka Bala calculation."""
    success: bool
    kundali_id: str
    planets: Dict[str, Dict[str, PlanetVimshopakaBala]]
    message: str = ""


class VargaPredictionItem(BaseModel):
    """Single prediction from varga analysis."""
    category: str
    aspect: str
    prediction: str
    strength: str
    is_favorable: bool
    supporting_factors: List[str]
    remedies: List[str]


class NavamsaAnalysisResponse(BaseModel):
    """Navamsa (D-9) analysis response."""
    success: bool
    kundali_id: str
    navamsa_lagna: Dict
    spouse_characteristics: Dict
    marriage_timing_factors: Dict
    marriage_quality: Dict
    spiritual_aspects: Dict
    predictions: List[VargaPredictionItem]
    message: str = ""


class DasamsaAnalysisResponse(BaseModel):
    """Dasamsa (D-10) analysis response."""
    success: bool
    kundali_id: str
    career_lagna: Dict
    tenth_house_analysis: Dict
    career_indicators: List[Dict]
    professional_strengths: Dict
    career_timing: Dict
    predictions: List[VargaPredictionItem]
    message: str = ""


class CompleteVargaAnalysisResponse(BaseModel):
    """Complete varga analysis combining all predictors."""
    success: bool
    kundali_id: str
    navamsa_analysis: Dict
    dasamsa_analysis: Dict
    saptamsa_analysis: Dict
    vimshopaka_bala: Dict
    summary: Dict
    message: str = ""


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def divisional_position_to_response(pos) -> DivisionalPositionResponse:
    """Convert DivisionalPosition to response model."""
    return DivisionalPositionResponse(
        planet=pos.planet,
        original_longitude=round(pos.original_longitude, 4),
        original_rashi=pos.original_rashi,
        original_degree=round(pos.original_degree, 4),
        varga_rashi=pos.varga_rashi,
        varga_rashi_english=pos.varga_rashi_english,
        varga_degree=round(pos.varga_degree, 4),
        division_number=pos.division_number,
        is_own_sign=pos.is_own_sign,
        is_exalted=pos.is_exalted,
        is_debilitated=pos.is_debilitated,
    )


def divisional_chart_to_response(chart: DivisionalChart) -> DivisionalChartResponse:
    """Convert DivisionalChart to response model."""
    return DivisionalChartResponse(
        varga_name=chart.varga_name,
        varga_description=chart.varga_description,
        division_count=chart.division_count,
        lagna=divisional_position_to_response(chart.lagna),
        planets={
            name: divisional_position_to_response(pos)
            for name, pos in chart.planets.items()
        },
        planets_in_houses={
            str(house): planets
            for house, planets in chart.planets_in_houses.items()
        },
    )


# =============================================================================
# ENDPOINTS
# =============================================================================

@router.get(
    "/charts/{kundali_id}",
    response_model=VargaListResponse,
    summary="Get all divisional charts",
    description="Calculate and return all 16 divisional charts for a kundali."
)
async def get_all_varga_charts(kundali_id: str) -> VargaListResponse:
    """
    Get all 16 divisional charts for a kundali.

    Returns D-1 through D-60 with planet positions and house placements.
    """
    try:
        kundali = get_kundali(kundali_id)
        all_charts = get_all_varga_charts_for_kundali(kundali)

        charts_response = {
            name: divisional_chart_to_response(chart)
            for name, chart in all_charts.items()
        }

        return VargaListResponse(
            success=True,
            kundali_id=kundali_id,
            charts=charts_response,
            message=f"Calculated all 16 divisional charts successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating divisional charts: {str(e)}"
        )


@router.get(
    "/chart/{kundali_id}/{varga_type}",
    response_model=SingleVargaResponse,
    summary="Get specific divisional chart",
    description="Calculate a specific divisional chart (D-1 to D-60)."
)
async def get_single_varga_chart(
    kundali_id: str,
    varga_type: str
) -> SingleVargaResponse:
    """
    Get a specific divisional chart.

    Parameters:
    - varga_type: The divisional chart to calculate (e.g., D9_NAVAMSA)
    """
    try:
        kundali = get_kundali(kundali_id)

        # Validate varga type
        try:
            varga = VargaChart[varga_type.upper()]
        except KeyError:
            valid_types = [v.name for v in VargaChart]
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid varga_type. Must be one of: {', '.join(valid_types)}"
            )

        chart = get_varga_chart_for_kundali(kundali, varga)

        return SingleVargaResponse(
            success=True,
            kundali_id=kundali_id,
            varga_type=varga_type.upper(),
            chart=divisional_chart_to_response(chart),
            message=f"{chart.varga_name} chart calculated successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating {varga_type} chart: {str(e)}"
        )


@router.get(
    "/navamsa/{kundali_id}",
    response_model=SingleVargaResponse,
    summary="Get Navamsa (D-9) chart",
    description="Get the Navamsa chart - most important divisional chart for marriage and dharma."
)
async def get_navamsa_chart(kundali_id: str) -> SingleVargaResponse:
    """Get Navamsa (D-9) chart for marriage and spiritual analysis."""
    return await get_single_varga_chart(kundali_id, "D9_NAVAMSA")


@router.get(
    "/dasamsa/{kundali_id}",
    response_model=SingleVargaResponse,
    summary="Get Dasamsa (D-10) chart",
    description="Get the Dasamsa chart for career and profession analysis."
)
async def get_dasamsa_chart(kundali_id: str) -> SingleVargaResponse:
    """Get Dasamsa (D-10) chart for career analysis."""
    return await get_single_varga_chart(kundali_id, "D10_DASAMSA")


@router.get(
    "/vimshopaka/{kundali_id}",
    response_model=VimshopakaBalaResponse,
    summary="Get Vimshopaka Bala",
    description="Calculate planetary strength across divisional charts (20-point strength)."
)
async def get_vimshopaka_bala(kundali_id: str) -> VimshopakaBalaResponse:
    """
    Calculate Vimshopaka Bala (20-point strength) for all planets.

    Returns both Shadvarga (6-chart) and Shodashavarga (16-chart) strengths.
    """
    try:
        kundali = get_kundali(kundali_id)
        bala_results = get_planet_vimshopaka_bala(kundali)

        return VimshopakaBalaResponse(
            success=True,
            kundali_id=kundali_id,
            planets=bala_results,
            message="Vimshopaka Bala calculated for all planets"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating Vimshopaka Bala: {str(e)}"
        )


@router.get(
    "/analysis/navamsa/{kundali_id}",
    response_model=NavamsaAnalysisResponse,
    summary="Get Navamsa analysis for marriage",
    description="Get detailed marriage and spouse predictions from Navamsa chart."
)
async def get_navamsa_analysis(kundali_id: str) -> NavamsaAnalysisResponse:
    """
    Get comprehensive Navamsa (D-9) analysis.

    Includes:
    - Spouse characteristics prediction
    - Marriage timing factors
    - Marriage quality assessment
    - Spiritual nature analysis
    """
    try:
        kundali = get_kundali(kundali_id)
        engine = VargaPredictionEngine()

        # Get just the navamsa analysis
        calculator = DivisionalChartCalculator()
        d9_chart = calculator.calculate_complete_varga_chart(
            VargaChart.D9_NAVAMSA,
            kundali.lagna["longitude"],
            kundali.planets
        )

        analysis = engine.navamsa_predictor.analyze_navamsa(d9_chart)

        # Convert predictions to response format
        prediction_responses = [
            VargaPredictionItem(
                category=p.category,
                aspect=p.aspect,
                prediction=p.prediction,
                strength=p.strength,
                is_favorable=p.is_favorable,
                supporting_factors=p.supporting_factors,
                remedies=p.remedies,
            )
            for p in analysis["predictions"]
        ]

        return NavamsaAnalysisResponse(
            success=True,
            kundali_id=kundali_id,
            navamsa_lagna=analysis["navamsa_lagna"],
            spouse_characteristics=analysis["spouse_characteristics"],
            marriage_timing_factors=analysis["marriage_timing_factors"],
            marriage_quality=analysis["marriage_quality"],
            spiritual_aspects=analysis["spiritual_aspects"],
            predictions=prediction_responses,
            message="Navamsa analysis completed successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing Navamsa: {str(e)}"
        )


@router.get(
    "/analysis/dasamsa/{kundali_id}",
    response_model=DasamsaAnalysisResponse,
    summary="Get Dasamsa analysis for career",
    description="Get detailed career and profession predictions from Dasamsa chart."
)
async def get_dasamsa_analysis(kundali_id: str) -> DasamsaAnalysisResponse:
    """
    Get comprehensive Dasamsa (D-10) analysis.

    Includes:
    - Career direction
    - Suitable professions
    - Professional strengths and weaknesses
    - Career growth timing
    """
    try:
        kundali = get_kundali(kundali_id)
        engine = VargaPredictionEngine()

        calculator = DivisionalChartCalculator()
        d10_chart = calculator.calculate_complete_varga_chart(
            VargaChart.D10_DASAMSA,
            kundali.lagna["longitude"],
            kundali.planets
        )

        analysis = engine.dasamsa_predictor.analyze_dasamsa(d10_chart)

        prediction_responses = [
            VargaPredictionItem(
                category=p.category,
                aspect=p.aspect,
                prediction=p.prediction,
                strength=p.strength,
                is_favorable=p.is_favorable,
                supporting_factors=p.supporting_factors,
                remedies=p.remedies,
            )
            for p in analysis["predictions"]
        ]

        return DasamsaAnalysisResponse(
            success=True,
            kundali_id=kundali_id,
            career_lagna=analysis["career_lagna"],
            tenth_house_analysis=analysis["10th_house_analysis"],
            career_indicators=analysis["career_indicators"],
            professional_strengths=analysis["professional_strengths"],
            career_timing=analysis["career_timing"],
            predictions=prediction_responses,
            message="Dasamsa analysis completed successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing Dasamsa: {str(e)}"
        )


@router.get(
    "/analysis/complete/{kundali_id}",
    response_model=CompleteVargaAnalysisResponse,
    summary="Get complete varga analysis",
    description="Get comprehensive analysis from all major divisional charts."
)
async def get_complete_varga_analysis(kundali_id: str) -> CompleteVargaAnalysisResponse:
    """
    Get complete analysis from all major divisional charts.

    Includes:
    - Navamsa analysis (marriage, spouse, dharma)
    - Dasamsa analysis (career, profession)
    - Saptamsa analysis (children)
    - Vimshopaka Bala (planetary strength)
    - Summary of key findings
    """
    try:
        kundali = get_kundali(kundali_id)
        engine = VargaPredictionEngine()

        analysis = engine.get_complete_varga_analysis(kundali)

        # Convert predictions in nested analysis
        for key in ["navamsa_analysis", "dasamsa_analysis", "saptamsa_analysis"]:
            if "predictions" in analysis[key]:
                analysis[key]["predictions"] = [
                    {
                        "category": p.category,
                        "aspect": p.aspect,
                        "prediction": p.prediction,
                        "strength": p.strength,
                        "is_favorable": p.is_favorable,
                        "supporting_factors": p.supporting_factors,
                        "remedies": p.remedies,
                    }
                    for p in analysis[key]["predictions"]
                ]

        return CompleteVargaAnalysisResponse(
            success=True,
            kundali_id=kundali_id,
            navamsa_analysis=analysis["navamsa_analysis"],
            dasamsa_analysis=analysis["dasamsa_analysis"],
            saptamsa_analysis=analysis["saptamsa_analysis"],
            vimshopaka_bala=analysis["vimshopaka_bala"],
            summary=analysis["summary"],
            message="Complete varga analysis completed successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating complete analysis: {str(e)}"
        )


@router.get(
    "/types",
    summary="List available varga chart types",
    description="Get list of all 16 divisional chart types with descriptions."
)
async def list_varga_types():
    """List all available divisional chart types."""
    varga_info = {
        "D1_RASHI": {"name": "Rashi", "description": "Main birth chart - overall life patterns", "divisions": 1},
        "D2_HORA": {"name": "Hora", "description": "Wealth and financial prosperity", "divisions": 2},
        "D3_DREKKANA": {"name": "Drekkana", "description": "Siblings, courage, and short journeys", "divisions": 3},
        "D4_CHATURTHAMSA": {"name": "Chaturthamsa", "description": "Property, home, and fortune", "divisions": 4},
        "D7_SAPTAMSA": {"name": "Saptamsa", "description": "Children and progeny", "divisions": 7},
        "D9_NAVAMSA": {"name": "Navamsa", "description": "Marriage, spouse, and dharma - MOST IMPORTANT", "divisions": 9},
        "D10_DASAMSA": {"name": "Dasamsa", "description": "Career and profession", "divisions": 10},
        "D12_DWADASAMSA": {"name": "Dwadasamsa", "description": "Parents and ancestry", "divisions": 12},
        "D16_SHODASAMSA": {"name": "Shodasamsa", "description": "Vehicles and comforts", "divisions": 16},
        "D20_VIMSAMSA": {"name": "Vimsamsa", "description": "Spiritual progress and worship", "divisions": 20},
        "D24_CHATURVIMSAMSA": {"name": "Siddhamsa", "description": "Education and learning", "divisions": 24},
        "D27_BHAMSA": {"name": "Bhamsa", "description": "Physical strength and weakness", "divisions": 27},
        "D30_TRIMSAMSA": {"name": "Trimsamsa", "description": "Evils and misfortunes (5 unequal divisions)", "divisions": 5},
        "D40_KHAVEDAMSA": {"name": "Khavedamsa", "description": "Auspicious/inauspicious effects", "divisions": 40},
        "D45_AKSHAVEDAMSA": {"name": "Akshavedamsa", "description": "General life indications", "divisions": 45},
        "D60_SHASHTIAMSA": {"name": "Shashtiamsa", "description": "Past life karma - VERY IMPORTANT", "divisions": 60},
    }

    return {
        "success": True,
        "varga_types": varga_info,
        "total_count": len(varga_info),
        "message": "Based on Brihat Parashara Hora Shastra (BPHS)"
    }
