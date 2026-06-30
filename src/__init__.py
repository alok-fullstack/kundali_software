"""
Kundali Software - Vedic Astrology Calculator
High accuracy planetary calculations using Swiss Ephemeris (NASA JPL DE431)
"""

__version__ = "1.0.0"
__author__ = "Alok Yadav"

# Public API exports
from .config import Planet, RASHIS, NAKSHATRAS, BHAVA_NAMES
from .planets import PlanetaryCalculator, format_degree
from .kundali import Kundali, BirthData, create_kundali, get_coordinates
from .dasha import VimshottariDasha
from .transit import TransitCalculator, TransitEvent, TransitAspect, get_transit_calculator
from .event_predictor import EventPredictor, PredictionPeriod
from .panchang import PanchangCalculator, PanchangData, TithiData, YogaData, KaranaData, VaraData
from .muhurta_rules import EventType, InauspiciousPeriod
from .muhurta import MuhurtaCalculator, MuhurtaWindow, find_best_muhurtas
from .muhurta_html_generator import generate_muhurta_html, open_muhurta_in_browser
from .health_predictor import HealthPredictor, HealthWarning, RiskLevel, HealthEventType
from .health_html_generator import generate_health_html
from .divisional_charts import (
    DivisionalChartCalculator, DivisionalChart, DivisionalPosition,
    VargaChart, VimshopakaBala,
    get_varga_chart_for_kundali, get_all_varga_charts_for_kundali,
    get_planet_vimshopaka_bala
)
from .varga_predictions import (
    VargaPrediction, NavamsaPredictor, DasamsaPredictor,
    SaptamsaPredictor, VargaPredictionEngine
)
from .rashifal import (
    RashifalCalculator, RashifalPrediction, RashifalPeriod,
    PredictionCategory, CategoryPrediction,
    get_rashifal, get_all_rashifal, get_rashi_list,
    RASHI_HINDI_NAMES
)
from .gemstone_recommendations import (
    GemstoneAdvisor, GemstoneRecommendation, GemstoneInfo,
    PLANET_GEMSTONE_MAP, CONFLICTING_STONES,
    get_gemstone_for_planet, get_all_gemstones, check_stone_compatibility
)
from .numerology import (
    NumerologyCalculator, NumerologyResult, NumerologySystem,
    NameCorrectionSuggestion, CompatibilityResult,
    calculate_numerology, get_compatibility,
    suggest_name_correction, analyze_business_name
)
from .dosha_analysis import (
    DoshaAnalyzer, DoshaResult, KaalSarpResult, SadeSatiResult,
    CompleteDoshaAnalysis, analyze_doshas
)
from .career_finance import (
    CareerFinanceAnalyzer, CareerAnalysis, DhanaYogaAnalysis,
    CareerFinanceReport, YogaResult, analyze_career_finance
)
from .remedies import (
    RemedyAnalyzer, PlanetRemedies, DoshaRemedyPlan,
    ComprehensiveRemedyReport, get_remedies
)
from .prashna_kundali import (
    PrashnaCalculator, PrashnaAnalysis, PrashnaChart,
    ArudhaResult, TimingResult, QuestionCategory, analyze_prashna
)
from .sade_sati_rashifal import (
    SadeSatiPhase, DhaiyaType, SadeSatiStatus, DhaiyaStatus,
    SaturnTransitAnalysis, SadeSatiRashifalCalculator,
    SADE_SATI_PHASE_EFFECTS, DHAIYA_EFFECTS, SADE_SATI_MODIFIERS,
    BPHS_SADE_SATI_RULES, SATURN_YOGAKARAKA_LAGNAS,
    check_sade_sati_for_moon_sign, get_sade_sati_affected_rashis,
    get_dhaiya_affected_rashis
)

__all__ = [
    # Config
    "Planet",
    "RASHIS",
    "NAKSHATRAS",
    "BHAVA_NAMES",
    # Planets
    "PlanetaryCalculator",
    "format_degree",
    # Kundali
    "Kundali",
    "BirthData",
    "create_kundali",
    "get_coordinates",
    # Dasha
    "VimshottariDasha",
    # Transit
    "TransitCalculator",
    "TransitEvent",
    "TransitAspect",
    "get_transit_calculator",
    # Event Predictor
    "EventPredictor",
    "PredictionPeriod",
    # Panchang
    "PanchangCalculator",
    "PanchangData",
    "TithiData",
    "YogaData",
    "KaranaData",
    "VaraData",
    # Muhurta
    "MuhurtaCalculator",
    "MuhurtaWindow",
    "EventType",
    "InauspiciousPeriod",
    "find_best_muhurtas",
    # Muhurta HTML
    "generate_muhurta_html",
    "open_muhurta_in_browser",
    # Health Predictor
    "HealthPredictor",
    "HealthWarning",
    "RiskLevel",
    "HealthEventType",
    # Health HTML
    "generate_health_html",
    # Divisional Charts
    "DivisionalChartCalculator",
    "DivisionalChart",
    "DivisionalPosition",
    "VargaChart",
    "VimshopakaBala",
    "get_varga_chart_for_kundali",
    "get_all_varga_charts_for_kundali",
    "get_planet_vimshopaka_bala",
    # Varga Predictions
    "VargaPrediction",
    "NavamsaPredictor",
    "DasamsaPredictor",
    "SaptamsaPredictor",
    "VargaPredictionEngine",
    # Rashifal (Horoscope)
    "RashifalCalculator",
    "RashifalPrediction",
    "RashifalPeriod",
    "PredictionCategory",
    "CategoryPrediction",
    "get_rashifal",
    "get_all_rashifal",
    "get_rashi_list",
    "RASHI_HINDI_NAMES",
    # Gemstone Recommendations
    "GemstoneAdvisor",
    "GemstoneRecommendation",
    "GemstoneInfo",
    "PLANET_GEMSTONE_MAP",
    "CONFLICTING_STONES",
    "get_gemstone_for_planet",
    "get_all_gemstones",
    "check_stone_compatibility",
    # Numerology (Ank Jyotish)
    "NumerologyCalculator",
    "NumerologyResult",
    "NumerologySystem",
    "NameCorrectionSuggestion",
    "CompatibilityResult",
    "calculate_numerology",
    "get_compatibility",
    "suggest_name_correction",
    "analyze_business_name",
    # Dosha Analysis
    "DoshaAnalyzer",
    "DoshaResult",
    "KaalSarpResult",
    "SadeSatiResult",
    "CompleteDoshaAnalysis",
    "analyze_doshas",
    # Career & Finance
    "CareerFinanceAnalyzer",
    "CareerAnalysis",
    "DhanaYogaAnalysis",
    "CareerFinanceReport",
    "YogaResult",
    "analyze_career_finance",
    # Remedies
    "RemedyAnalyzer",
    "PlanetRemedies",
    "DoshaRemedyPlan",
    "ComprehensiveRemedyReport",
    "get_remedies",
    # Prashna Kundali
    "PrashnaCalculator",
    "PrashnaAnalysis",
    "PrashnaChart",
    "ArudhaResult",
    "TimingResult",
    "QuestionCategory",
    "analyze_prashna",
    # Sade Sati Rashifal Integration
    "SadeSatiPhase",
    "DhaiyaType",
    "SadeSatiStatus",
    "DhaiyaStatus",
    "SaturnTransitAnalysis",
    "SadeSatiRashifalCalculator",
    "SADE_SATI_PHASE_EFFECTS",
    "DHAIYA_EFFECTS",
    "SADE_SATI_MODIFIERS",
    "BPHS_SADE_SATI_RULES",
    "SATURN_YOGAKARAKA_LAGNAS",
    "check_sade_sati_for_moon_sign",
    "get_sade_sati_affected_rashis",
    "get_dhaiya_affected_rashis",
]
