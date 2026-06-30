"""
Sade Sati Integration for Rashifal Predictions

This module integrates Sade Sati (Saturn's 7.5 year transit) and Dhaiya (Small Panoti)
into Rashifal predictions with score modifiers and specialized prediction text.

Classical References:
- Brihat Parashara Hora Shastra (BPHS) - Chapters on Gochar (Transit)
- Phaladeepika by Mantreshwara - Transit effects
- Brihat Samhita by Varahamihira
- Jataka Parijata

Author: Kundali Software
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum


# =============================================================================
# ENUMS AND CONSTANTS
# =============================================================================

class SadeSatiPhase(Enum):
    """Sade Sati phases with position from Moon."""
    RISING = "rising"      # Saturn in 12th from Moon
    PEAK = "peak"          # Saturn over Moon (1st from Moon)
    SETTING = "setting"    # Saturn in 2nd from Moon
    NONE = "none"          # Not in Sade Sati


class DhaiyaType(Enum):
    """Dhaiya (Small Panoti) types."""
    KANTAK = "kantak"      # Saturn in 4th from Moon
    ASHTAMA = "ashtama"    # Saturn in 8th from Moon
    NONE = "none"          # Not in Dhaiya


# =============================================================================
# SADE SATI PHASE EFFECTS - From BPHS and Phaladeepika
# =============================================================================

SADE_SATI_PHASE_EFFECTS = {
    SadeSatiPhase.RISING: {
        "name_hindi": "उदय चरण (12वां भाव)",
        "name_english": "Rising Phase (12th House)",
        "duration_years": 2.5,
        "score_modifier": -1.5,  # Moderate impact
        "intensity": 0.65,  # 65% intensity compared to peak
        "primary_effects": [
            "Increased expenses and financial outflow",
            "Sleep disturbances and insomnia",
            "Hidden enemies become active",
            "Hospitalization possibilities",
            "Foreign travel/settlement",
            "Spiritual awakening begins",
        ],
        "primary_effects_hindi": [
            "खर्चों में वृद्धि",
            "नींद में परेशानी",
            "छुपे शत्रु सक्रिय",
            "अस्पताल जाने की संभावना",
            "विदेश यात्रा/बसाव",
            "आध्यात्मिक जागृति की शुरुआत",
        ],
        "affected_areas": ["expenses", "health", "sleep", "spirituality"],
        "prediction_templates": [
            "साढ़े साती का पहला चरण चल रहा है। खर्चों पर नियंत्रण रखें। नींद और स्वास्थ्य का ध्यान दें।",
            "शनि 12वें भाव में हैं। व्यय बढ़ सकता है। विदेश यात्रा के योग हैं। आध्यात्मिक कार्यों में रुचि बढ़ेगी।",
            "साढ़े साती शुरू हो चुकी है। छुपी समस्याएं सामने आ सकती हैं। धैर्य और संयम से काम लें।",
        ],
    },
    SadeSatiPhase.PEAK: {
        "name_hindi": "शिखर चरण (चंद्र पर)",
        "name_english": "Peak Phase (Over Moon)",
        "duration_years": 2.5,
        "score_modifier": -2.5,  # Maximum impact
        "intensity": 1.0,  # 100% intensity - most challenging
        "primary_effects": [
            "Maximum mental stress and anxiety",
            "Career setbacks or major changes",
            "Health issues, especially chronic",
            "Family responsibilities increase",
            "Emotional turbulence",
            "Major life transformations",
            "Relationship challenges",
        ],
        "primary_effects_hindi": [
            "अधिकतम मानसिक तनाव और चिंता",
            "करियर में बाधा या बड़े बदलाव",
            "स्वास्थ्य समस्या, विशेषकर पुरानी",
            "पारिवारिक जिम्मेदारियां बढ़ना",
            "भावनात्मक उथल-पुथल",
            "जीवन में बड़े परिवर्तन",
            "रिश्तों में चुनौती",
        ],
        "affected_areas": ["mental_health", "career", "family", "relationships", "health"],
        "prediction_templates": [
            "साढ़े साती का शिखर चरण है - सबसे कठिन समय। मानसिक शांति के लिए ध्यान और पूजा-पाठ करें। बड़े फैसले टालें।",
            "शनि चंद्र राशि में हैं। यह साढ़े साती का सबसे प्रभावशाली समय है। करियर और स्वास्थ्य पर विशेष ध्यान दें।",
            "साढ़े साती चरम पर है। जीवन में बड़े बदलाव संभव। धैर्य रखें, शनि के उपाय नियमित करें।",
        ],
    },
    SadeSatiPhase.SETTING: {
        "name_hindi": "अस्त चरण (2वां भाव)",
        "name_english": "Setting Phase (2nd House)",
        "duration_years": 2.5,
        "score_modifier": -1.5,  # Moderate impact
        "intensity": 0.70,  # 70% intensity
        "primary_effects": [
            "Financial pressures continue",
            "Family conflicts or responsibilities",
            "Speech-related issues",
            "Challenges begin to ease gradually",
            "Integration of lessons learned",
            "Eye or face-related health issues",
        ],
        "primary_effects_hindi": [
            "आर्थिक दबाव जारी",
            "पारिवारिक कलह या जिम्मेदारियां",
            "वाणी संबंधी समस्या",
            "चुनौतियां धीरे-धीरे कम होने लगती हैं",
            "सीखे गए पाठों का समावेश",
            "आंख या चेहरे की स्वास्थ्य समस्या",
        ],
        "affected_areas": ["finance", "family", "speech", "eyes"],
        "prediction_templates": [
            "साढ़े साती का अंतिम चरण है। धन और परिवार पर ध्यान दें। स्थिति धीरे-धीरे सुधर रही है।",
            "शनि 2वें भाव में हैं। आर्थिक मामलों में सावधानी बरतें। परिवार में सामंजस्य बनाए रखें।",
            "साढ़े साती समाप्त होने वाली है। सब्र रखें, कुछ और समय की आवश्यकता है।",
        ],
    },
}

# =============================================================================
# DHAIYA (SMALL PANOTI) EFFECTS
# =============================================================================

DHAIYA_EFFECTS = {
    DhaiyaType.KANTAK: {
        "name_hindi": "कांटक शनि (4वां भाव)",
        "name_english": "Kantak Shani (4th House)",
        "duration_years": 2.5,
        "score_modifier": -1.2,  # Less severe than Sade Sati
        "intensity": 0.55,  # 55% of Sade Sati peak
        "primary_effects": [
            "Domestic troubles and unrest",
            "Mother's health concerns",
            "Vehicle-related problems",
            "Property disputes",
            "Mental peace disturbed",
            "Educational setbacks",
        ],
        "primary_effects_hindi": [
            "घरेलू अशांति और परेशानी",
            "माता की स्वास्थ्य चिंता",
            "वाहन संबंधी समस्या",
            "संपत्ति विवाद",
            "मानसिक शांति में कमी",
            "शैक्षिक बाधा",
        ],
        "affected_areas": ["home", "mother", "vehicle", "property", "education"],
        "prediction_templates": [
            "कांटक शनि चल रही है। घरेलू मामलों में सावधानी बरतें। माता का ख्याल रखें।",
            "शनि 4वें भाव में हैं। गृह सुख में कमी हो सकती है। वाहन सावधानी से चलाएं।",
        ],
    },
    DhaiyaType.ASHTAMA: {
        "name_hindi": "अष्टम शनि (8वां भाव)",
        "name_english": "Ashtama Shani (8th House)",
        "duration_years": 2.5,
        "score_modifier": -1.8,  # More severe than Kantak
        "intensity": 0.75,  # 75% of Sade Sati peak
        "primary_effects": [
            "Health issues and chronic problems",
            "Accidents and injuries risk",
            "Financial losses through unexpected events",
            "Legal troubles possible",
            "Transformation and research",
            "In-laws related issues",
        ],
        "primary_effects_hindi": [
            "स्वास्थ्य समस्या और पुरानी बीमारी",
            "दुर्घटना और चोट का खतरा",
            "अप्रत्याशित घटनाओं से आर्थिक हानि",
            "कानूनी समस्या संभव",
            "परिवर्तन और शोध",
            "ससुराल पक्ष से समस्या",
        ],
        "affected_areas": ["health", "accidents", "finances", "legal", "in_laws"],
        "prediction_templates": [
            "अष्टम शनि का प्रभाव है। स्वास्थ्य और दुर्घटना से सावधान रहें। बीमा करवा लें।",
            "शनि 8वें भाव में हैं। यह छोटी पनौती का कठिन रूप है। सावधानी और उपाय आवश्यक।",
        ],
    },
}

# =============================================================================
# SATURN YOGAKARAKA CONSIDERATIONS - When Sade Sati is LESS Harmful
# =============================================================================

# Lagnas for which Saturn is Yogakaraka (beneficial)
SATURN_YOGAKARAKA_LAGNAS = ["Vrishabha", "Tula"]  # Taurus and Libra

# Saturn's own signs - Sade Sati less harmful when Saturn transits its own sign
SATURN_OWN_SIGNS = ["Makara", "Kumbha"]  # Capricorn and Aquarius

# Saturn's exaltation sign - Sade Sati less harmful
SATURN_EXALTED_SIGN = "Tula"  # Libra

# Saturn's debilitation sign - Sade Sati more harmful
SATURN_DEBILITATED_SIGN = "Mesha"  # Aries

# Saturn's Mooltrikona sign
SATURN_MOOLTRIKONA_SIGN = "Kumbha"  # Aquarius


# =============================================================================
# REMEDIAL FACTOR MODIFIERS - From BPHS
# =============================================================================

SADE_SATI_MODIFIERS = {
    # When Saturn is in its own sign during transit
    "saturn_own_sign": {
        "modifier": 0.3,  # Reduces negative effect by 30%
        "description": "Saturn in own sign reduces Sade Sati harshness",
        "description_hindi": "शनि स्वराशि में होने से साढ़े साती का प्रभाव कम",
    },
    # When Saturn is exalted during transit
    "saturn_exalted": {
        "modifier": 0.4,  # Reduces negative effect by 40%
        "description": "Saturn exalted reduces Sade Sati effects significantly",
        "description_hindi": "शनि उच्च राशि में - साढ़े साती प्रभाव काफी कम",
    },
    # When Saturn is debilitated during transit
    "saturn_debilitated": {
        "modifier": -0.2,  # Increases negative effect by 20%
        "description": "Saturn debilitated increases Sade Sati harshness",
        "description_hindi": "शनि नीच राशि में - साढ़े साती अधिक कठिन",
    },
    # When lagna is Saturn Yogakaraka
    "yogakaraka_lagna": {
        "modifier": 0.35,  # Reduces negative effect by 35%
        "description": "Saturn is Yogakaraka for this lagna - Sade Sati gives mixed results",
        "description_hindi": "इस लग्न के लिए शनि योगकारक है - मिश्रित फल",
    },
    # When natal Saturn is strong (in own/exalted/friend's sign)
    "natal_saturn_strong": {
        "modifier": 0.25,  # Reduces negative effect by 25%
        "description": "Strong natal Saturn provides resilience",
        "description_hindi": "जन्म कुंडली में शनि बली - प्रतिरोधक क्षमता अधिक",
    },
    # When Jupiter aspects Moon during Sade Sati
    "jupiter_protection": {
        "modifier": 0.3,  # Jupiter's grace reduces suffering
        "description": "Jupiter's aspect on Moon provides protection",
        "description_hindi": "गुरु की चंद्र पर दृष्टि से रक्षा",
    },
    # Saturn retrograde during Sade Sati - mixed effects
    "saturn_retrograde": {
        "modifier": 0.1,  # Slightly reduces as effects are internalized
        "description": "Retrograde Saturn - internal transformation emphasized",
        "description_hindi": "वक्री शनि - आंतरिक परिवर्तन पर जोर",
    },
}


# =============================================================================
# CLASSICAL BPHS SADE SATI RULES
# =============================================================================

BPHS_SADE_SATI_RULES = {
    # BPHS states these Moon signs experience Sade Sati differently
    "severe_for_moon_signs": ["Karka", "Simha", "Vrishchika"],  # Cancer, Leo, Scorpio
    "moderate_for_moon_signs": ["Mesha", "Mithuna", "Kanya", "Dhanu", "Meena"],
    "milder_for_moon_signs": ["Vrishabha", "Tula", "Makara", "Kumbha"],  # Saturn friendly

    # Age-based severity (traditional view)
    "age_severity": {
        "first_cycle": {  # Ages 0-30 approximately
            "description": "First Sade Sati - transformation of self-identity",
            "modifier": 0.0,  # Standard effect
        },
        "second_cycle": {  # Ages 30-60 approximately
            "description": "Second Sade Sati - career and family challenges",
            "modifier": -0.1,  # Slightly more challenging
        },
        "third_cycle": {  # Ages 60+ approximately
            "description": "Third Sade Sati - health and spiritual focus",
            "modifier": 0.1,  # Focus shifts to spiritual, can be easier
        },
    },

    # When Sade Sati can give GOOD results (per BPHS)
    "beneficial_conditions": [
        "Saturn is Yogakaraka for the lagna",
        "Saturn transits its own or exalted sign",
        "Jupiter aspects Saturn during transit",
        "Saturn is in Pushya, Anuradha, or Uttara Bhadrapada nakshatra (Saturn's nakshatras)",
        "Person is running Saturn Mahadasha/Antardasha (karma already active)",
        "Native has strong 6th, 8th, 12th house - used to challenges",
    ],
    "beneficial_conditions_hindi": [
        "शनि लग्न के लिए योगकारक है",
        "शनि स्वराशि या उच्च राशि में गोचर कर रहा है",
        "गोचर में गुरु की शनि पर दृष्टि है",
        "शनि पुष्य, अनुराधा या उत्तर भाद्रपद नक्षत्र में है",
        "शनि की महादशा/अंतर्दशा चल रही है",
        "जातक के 6, 8, 12 भाव मजबूत हैं",
    ],
}


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class SadeSatiStatus:
    """Complete Sade Sati status for a person."""
    is_active: bool
    phase: SadeSatiPhase
    phase_name_hindi: str
    phase_name_english: str

    # Score modification
    base_score_modifier: float
    adjusted_score_modifier: float  # After applying remedial factors

    # Intensity and duration
    intensity: float
    estimated_remaining_months: int

    # Effects
    primary_effects: List[str]
    primary_effects_hindi: List[str]
    affected_areas: List[str]

    # Remedial factors applied
    remedial_factors: List[Dict]

    # Prediction text
    prediction_text_hindi: str
    prediction_text_english: str

    # Additional info
    saturn_rashi: str
    saturn_rashi_hindi: str
    is_saturn_retrograde: bool
    is_yogakaraka_lagna: bool

    # For API/display
    display_badge: str  # e.g., "साढ़े साती - शिखर चरण"
    severity_level: str  # "high", "medium", "low"


@dataclass
class DhaiyaStatus:
    """Dhaiya (Small Panoti) status."""
    is_active: bool
    dhaiya_type: DhaiyaType
    name_hindi: str
    name_english: str

    score_modifier: float
    intensity: float

    primary_effects: List[str]
    primary_effects_hindi: List[str]
    affected_areas: List[str]

    prediction_text_hindi: str
    saturn_rashi: str


@dataclass
class SaturnTransitAnalysis:
    """Complete Saturn transit analysis combining Sade Sati and Dhaiya."""
    # Main status
    sade_sati: Optional[SadeSatiStatus]
    dhaiya: Optional[DhaiyaStatus]

    # Combined score modifier for Rashifal
    total_score_modifier: float

    # Whether any Saturn transit affliction is active
    has_affliction: bool

    # Combined prediction text
    combined_prediction_hindi: str
    combined_prediction_english: str

    # Remedies (common for both)
    remedies: List[str]
    remedies_hindi: List[str]


# =============================================================================
# MAIN SADE SATI CALCULATOR CLASS
# =============================================================================

class SadeSatiRashifalCalculator:
    """
    Calculator for Sade Sati and Dhaiya effects on Rashifal predictions.

    Integrates classical Vedic rules for Saturn transit with score modification
    for horoscope predictions.
    """

    def __init__(self):
        """Initialize the calculator."""
        pass

    def get_saturn_position_from_moon(
        self,
        saturn_rashi_num: int,
        moon_rashi_num: int
    ) -> int:
        """
        Calculate Saturn's house position from Moon.

        Args:
            saturn_rashi_num: Saturn's current rashi number (0-11)
            moon_rashi_num: Natal Moon's rashi number (0-11)

        Returns:
            House number from Moon (1-12)
        """
        return ((saturn_rashi_num - moon_rashi_num) % 12) + 1

    def detect_sade_sati_phase(
        self,
        saturn_house_from_moon: int
    ) -> SadeSatiPhase:
        """
        Detect current Sade Sati phase based on Saturn's position from Moon.

        Args:
            saturn_house_from_moon: Saturn's house from Moon (1-12)

        Returns:
            SadeSatiPhase enum
        """
        if saturn_house_from_moon == 12:
            return SadeSatiPhase.RISING
        elif saturn_house_from_moon == 1:
            return SadeSatiPhase.PEAK
        elif saturn_house_from_moon == 2:
            return SadeSatiPhase.SETTING
        else:
            return SadeSatiPhase.NONE

    def detect_dhaiya_type(
        self,
        saturn_house_from_moon: int
    ) -> DhaiyaType:
        """
        Detect if Dhaiya (Small Panoti) is active.

        Args:
            saturn_house_from_moon: Saturn's house from Moon (1-12)

        Returns:
            DhaiyaType enum
        """
        if saturn_house_from_moon == 4:
            return DhaiyaType.KANTAK
        elif saturn_house_from_moon == 8:
            return DhaiyaType.ASHTAMA
        else:
            return DhaiyaType.NONE

    def calculate_remedial_factors(
        self,
        saturn_rashi: str,
        lagna_rashi: str,
        is_saturn_retrograde: bool = False,
        natal_saturn_rashi: str = None,
        jupiter_aspecting_moon: bool = False
    ) -> Tuple[float, List[Dict]]:
        """
        Calculate remedial factors that reduce Sade Sati severity.

        Returns:
            Tuple of (total_modifier, list of applied factors)
        """
        total_modifier = 0.0
        applied_factors = []

        # Check Saturn in own sign
        if saturn_rashi in SATURN_OWN_SIGNS:
            factor = SADE_SATI_MODIFIERS["saturn_own_sign"]
            total_modifier += factor["modifier"]
            applied_factors.append({
                "type": "saturn_own_sign",
                "modifier": factor["modifier"],
                "description": factor["description"],
                "description_hindi": factor["description_hindi"],
            })

        # Check Saturn exalted
        if saturn_rashi == SATURN_EXALTED_SIGN:
            factor = SADE_SATI_MODIFIERS["saturn_exalted"]
            total_modifier += factor["modifier"]
            applied_factors.append({
                "type": "saturn_exalted",
                "modifier": factor["modifier"],
                "description": factor["description"],
                "description_hindi": factor["description_hindi"],
            })

        # Check Saturn debilitated
        if saturn_rashi == SATURN_DEBILITATED_SIGN:
            factor = SADE_SATI_MODIFIERS["saturn_debilitated"]
            total_modifier += factor["modifier"]
            applied_factors.append({
                "type": "saturn_debilitated",
                "modifier": factor["modifier"],
                "description": factor["description"],
                "description_hindi": factor["description_hindi"],
            })

        # Check Yogakaraka lagna
        if lagna_rashi in SATURN_YOGAKARAKA_LAGNAS:
            factor = SADE_SATI_MODIFIERS["yogakaraka_lagna"]
            total_modifier += factor["modifier"]
            applied_factors.append({
                "type": "yogakaraka_lagna",
                "modifier": factor["modifier"],
                "description": factor["description"],
                "description_hindi": factor["description_hindi"],
            })

        # Check natal Saturn strength
        if natal_saturn_rashi and natal_saturn_rashi in SATURN_OWN_SIGNS + [SATURN_EXALTED_SIGN]:
            factor = SADE_SATI_MODIFIERS["natal_saturn_strong"]
            total_modifier += factor["modifier"]
            applied_factors.append({
                "type": "natal_saturn_strong",
                "modifier": factor["modifier"],
                "description": factor["description"],
                "description_hindi": factor["description_hindi"],
            })

        # Check Jupiter protection
        if jupiter_aspecting_moon:
            factor = SADE_SATI_MODIFIERS["jupiter_protection"]
            total_modifier += factor["modifier"]
            applied_factors.append({
                "type": "jupiter_protection",
                "modifier": factor["modifier"],
                "description": factor["description"],
                "description_hindi": factor["description_hindi"],
            })

        # Check Saturn retrograde
        if is_saturn_retrograde:
            factor = SADE_SATI_MODIFIERS["saturn_retrograde"]
            total_modifier += factor["modifier"]
            applied_factors.append({
                "type": "saturn_retrograde",
                "modifier": factor["modifier"],
                "description": factor["description"],
                "description_hindi": factor["description_hindi"],
            })

        return (total_modifier, applied_factors)

    def analyze_sade_sati(
        self,
        moon_rashi_num: int,
        saturn_rashi_num: int,
        saturn_rashi: str,
        lagna_rashi: str = None,
        is_saturn_retrograde: bool = False,
        natal_saturn_rashi: str = None,
        jupiter_aspecting_moon: bool = False
    ) -> Optional[SadeSatiStatus]:
        """
        Analyze Sade Sati status with all modifiers.

        Args:
            moon_rashi_num: Natal Moon's rashi number (0-11)
            saturn_rashi_num: Current Saturn's rashi number (0-11)
            saturn_rashi: Saturn's rashi name
            lagna_rashi: Lagna rashi name (optional, for Yogakaraka check)
            is_saturn_retrograde: Whether Saturn is retrograde
            natal_saturn_rashi: Natal Saturn's rashi (optional)
            jupiter_aspecting_moon: Whether Jupiter aspects Moon

        Returns:
            SadeSatiStatus or None if not in Sade Sati
        """
        # Rashi Hindi names
        RASHI_HINDI = {
            0: "मेष", 1: "वृषभ", 2: "मिथुन", 3: "कर्क",
            4: "सिंह", 5: "कन्या", 6: "तुला", 7: "वृश्चिक",
            8: "धनु", 9: "मकर", 10: "कुंभ", 11: "मीन"
        }

        saturn_house = self.get_saturn_position_from_moon(saturn_rashi_num, moon_rashi_num)
        phase = self.detect_sade_sati_phase(saturn_house)

        if phase == SadeSatiPhase.NONE:
            return None

        phase_data = SADE_SATI_PHASE_EFFECTS[phase]

        # Calculate remedial factors
        remedial_modifier, remedial_factors = self.calculate_remedial_factors(
            saturn_rashi=saturn_rashi,
            lagna_rashi=lagna_rashi,
            is_saturn_retrograde=is_saturn_retrograde,
            natal_saturn_rashi=natal_saturn_rashi,
            jupiter_aspecting_moon=jupiter_aspecting_moon
        )

        # Calculate adjusted score modifier
        base_modifier = phase_data["score_modifier"]
        # Apply remedial factors (they reduce the negative impact)
        adjusted_modifier = base_modifier * (1 - remedial_modifier)

        # Determine severity level
        if abs(adjusted_modifier) >= 2.0:
            severity_level = "high"
        elif abs(adjusted_modifier) >= 1.0:
            severity_level = "medium"
        else:
            severity_level = "low"

        # Select prediction template
        import random
        prediction_hindi = random.choice(phase_data["prediction_templates"])

        # Create display badge
        display_badge = f"साढ़े साती - {phase_data['name_hindi'].split('(')[0].strip()}"

        return SadeSatiStatus(
            is_active=True,
            phase=phase,
            phase_name_hindi=phase_data["name_hindi"],
            phase_name_english=phase_data["name_english"],
            base_score_modifier=base_modifier,
            adjusted_score_modifier=round(adjusted_modifier, 2),
            intensity=phase_data["intensity"],
            estimated_remaining_months=int(phase_data["duration_years"] * 12 / 2),  # Approximate
            primary_effects=phase_data["primary_effects"],
            primary_effects_hindi=phase_data["primary_effects_hindi"],
            affected_areas=phase_data["affected_areas"],
            remedial_factors=remedial_factors,
            prediction_text_hindi=prediction_hindi,
            prediction_text_english=f"Sade Sati {phase_data['name_english']} is active. Be patient and follow remedies.",
            saturn_rashi=saturn_rashi,
            saturn_rashi_hindi=RASHI_HINDI.get(saturn_rashi_num, saturn_rashi),
            is_saturn_retrograde=is_saturn_retrograde,
            is_yogakaraka_lagna=lagna_rashi in SATURN_YOGAKARAKA_LAGNAS if lagna_rashi else False,
            display_badge=display_badge,
            severity_level=severity_level
        )

    def analyze_dhaiya(
        self,
        moon_rashi_num: int,
        saturn_rashi_num: int,
        saturn_rashi: str
    ) -> Optional[DhaiyaStatus]:
        """
        Analyze Dhaiya (Small Panoti) status.

        Args:
            moon_rashi_num: Natal Moon's rashi number (0-11)
            saturn_rashi_num: Current Saturn's rashi number (0-11)
            saturn_rashi: Saturn's rashi name

        Returns:
            DhaiyaStatus or None if not in Dhaiya
        """
        saturn_house = self.get_saturn_position_from_moon(saturn_rashi_num, moon_rashi_num)
        dhaiya_type = self.detect_dhaiya_type(saturn_house)

        if dhaiya_type == DhaiyaType.NONE:
            return None

        dhaiya_data = DHAIYA_EFFECTS[dhaiya_type]

        import random
        prediction_hindi = random.choice(dhaiya_data["prediction_templates"])

        return DhaiyaStatus(
            is_active=True,
            dhaiya_type=dhaiya_type,
            name_hindi=dhaiya_data["name_hindi"],
            name_english=dhaiya_data["name_english"],
            score_modifier=dhaiya_data["score_modifier"],
            intensity=dhaiya_data["intensity"],
            primary_effects=dhaiya_data["primary_effects"],
            primary_effects_hindi=dhaiya_data["primary_effects_hindi"],
            affected_areas=dhaiya_data["affected_areas"],
            prediction_text_hindi=prediction_hindi,
            saturn_rashi=saturn_rashi
        )

    def get_common_remedies(self) -> Tuple[List[str], List[str]]:
        """Get common remedies for Sade Sati and Dhaiya."""
        remedies = [
            "Recite Shani Chalisa and Shani Stotra on Saturdays",
            "Chant 'Om Sham Shanaishcharaya Namah' 108 times daily",
            "Donate black sesame seeds (til), mustard oil, black cloth on Saturdays",
            "Feed crows (Saturn's vehicle) with cooked rice daily",
            "Light mustard oil lamp under Peepal tree on Saturday evenings",
            "Visit Shani temple on Saturdays",
            "Worship Lord Hanuman - recite Hanuman Chalisa",
            "Wear iron ring on middle finger (Saturday)",
            "Practice patience, humility, and help the elderly",
            "Avoid alcohol, non-vegetarian food on Saturdays",
        ]

        remedies_hindi = [
            "शनिवार को शनि चालीसा और शनि स्तोत्र पढ़ें",
            "'ॐ शं शनैश्चराय नमः' रोज़ 108 बार जपें",
            "शनिवार को काले तिल, सरसों तेल, काला कपड़ा दान करें",
            "रोज़ कौओं को पके हुए चावल खिलाएं",
            "शनिवार शाम को पीपल के पेड़ के नीचे सरसों तेल का दीपक जलाएं",
            "शनिवार को शनि मंदिर जाएं",
            "हनुमान जी की पूजा करें - हनुमान चालीसा पढ़ें",
            "मध्यमा उंगली में लोहे की अंगूठी (शनिवार को) पहनें",
            "धैर्य रखें, विनम्रता से काम लें, बुजुर्गों की सेवा करें",
            "शनिवार को मांस-मदिरा का त्याग करें",
        ]

        return (remedies, remedies_hindi)

    def get_complete_saturn_analysis(
        self,
        moon_rashi_num: int,
        saturn_rashi_num: int,
        saturn_rashi: str,
        lagna_rashi: str = None,
        is_saturn_retrograde: bool = False,
        natal_saturn_rashi: str = None,
        jupiter_aspecting_moon: bool = False
    ) -> SaturnTransitAnalysis:
        """
        Get complete Saturn transit analysis including Sade Sati and Dhaiya.

        Args:
            moon_rashi_num: Natal Moon's rashi number (0-11)
            saturn_rashi_num: Current Saturn's rashi number (0-11)
            saturn_rashi: Saturn's rashi name
            lagna_rashi: Lagna rashi name (optional)
            is_saturn_retrograde: Whether Saturn is retrograde
            natal_saturn_rashi: Natal Saturn's rashi (optional)
            jupiter_aspecting_moon: Whether Jupiter aspects Moon

        Returns:
            SaturnTransitAnalysis with complete data
        """
        # Check for Sade Sati
        sade_sati = self.analyze_sade_sati(
            moon_rashi_num=moon_rashi_num,
            saturn_rashi_num=saturn_rashi_num,
            saturn_rashi=saturn_rashi,
            lagna_rashi=lagna_rashi,
            is_saturn_retrograde=is_saturn_retrograde,
            natal_saturn_rashi=natal_saturn_rashi,
            jupiter_aspecting_moon=jupiter_aspecting_moon
        )

        # Check for Dhaiya (only if not in Sade Sati)
        dhaiya = None
        if sade_sati is None:
            dhaiya = self.analyze_dhaiya(
                moon_rashi_num=moon_rashi_num,
                saturn_rashi_num=saturn_rashi_num,
                saturn_rashi=saturn_rashi
            )

        # Calculate total score modifier
        total_modifier = 0.0
        if sade_sati:
            total_modifier = sade_sati.adjusted_score_modifier
        elif dhaiya:
            total_modifier = dhaiya.score_modifier

        # Build combined prediction
        if sade_sati:
            combined_hindi = sade_sati.prediction_text_hindi
            combined_english = sade_sati.prediction_text_english
        elif dhaiya:
            combined_hindi = dhaiya.prediction_text_hindi
            combined_english = f"Dhaiya ({dhaiya.name_english}) is active. Take precautions."
        else:
            combined_hindi = "शनि गोचर सामान्य है। कोई विशेष प्रभाव नहीं।"
            combined_english = "Saturn transit is normal. No special affliction."

        # Get remedies
        remedies, remedies_hindi = self.get_common_remedies()

        has_affliction = sade_sati is not None or dhaiya is not None

        return SaturnTransitAnalysis(
            sade_sati=sade_sati,
            dhaiya=dhaiya,
            total_score_modifier=round(total_modifier, 2),
            has_affliction=has_affliction,
            combined_prediction_hindi=combined_hindi,
            combined_prediction_english=combined_english,
            remedies=remedies if has_affliction else [],
            remedies_hindi=remedies_hindi if has_affliction else []
        )

    def modify_rashifal_score(
        self,
        base_score: float,
        saturn_analysis: SaturnTransitAnalysis
    ) -> float:
        """
        Modify Rashifal score based on Sade Sati/Dhaiya analysis.

        Args:
            base_score: Original Rashifal score (1-10)
            saturn_analysis: Complete Saturn transit analysis

        Returns:
            Modified score (clamped to 1-10)
        """
        modified_score = base_score + saturn_analysis.total_score_modifier
        return max(1.0, min(10.0, modified_score))


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def check_sade_sati_for_moon_sign(
    moon_rashi_num: int,
    saturn_rashi_num: int,
    saturn_rashi: str
) -> Dict:
    """
    Quick check for Sade Sati status.

    Args:
        moon_rashi_num: Natal Moon's rashi number (0-11)
        saturn_rashi_num: Current Saturn's rashi number (0-11)
        saturn_rashi: Saturn's rashi name

    Returns:
        Dict with is_active, phase, and basic info
    """
    calculator = SadeSatiRashifalCalculator()
    analysis = calculator.get_complete_saturn_analysis(
        moon_rashi_num=moon_rashi_num,
        saturn_rashi_num=saturn_rashi_num,
        saturn_rashi=saturn_rashi
    )

    return {
        "has_affliction": analysis.has_affliction,
        "is_sade_sati": analysis.sade_sati is not None,
        "sade_sati_phase": analysis.sade_sati.phase.value if analysis.sade_sati else None,
        "is_dhaiya": analysis.dhaiya is not None,
        "dhaiya_type": analysis.dhaiya.dhaiya_type.value if analysis.dhaiya else None,
        "score_modifier": analysis.total_score_modifier,
        "prediction_hindi": analysis.combined_prediction_hindi,
    }


def get_sade_sati_affected_rashis(saturn_rashi_num: int) -> Dict[str, int]:
    """
    Get all rashis currently affected by Sade Sati for given Saturn position.

    Args:
        saturn_rashi_num: Saturn's current rashi number (0-11)

    Returns:
        Dict mapping phase name to affected Moon rashi number
    """
    return {
        "rising": (saturn_rashi_num + 1) % 12,   # Moon sign for which Saturn is in 12th
        "peak": saturn_rashi_num,                 # Moon sign same as Saturn
        "setting": (saturn_rashi_num - 1) % 12,  # Moon sign for which Saturn is in 2nd
    }


def get_dhaiya_affected_rashis(saturn_rashi_num: int) -> Dict[str, int]:
    """
    Get rashis currently affected by Dhaiya for given Saturn position.

    Args:
        saturn_rashi_num: Saturn's current rashi number (0-11)

    Returns:
        Dict mapping dhaiya type to affected Moon rashi number
    """
    return {
        "kantak": (saturn_rashi_num - 3) % 12,   # Moon sign for which Saturn is in 4th
        "ashtama": (saturn_rashi_num - 7) % 12,  # Moon sign for which Saturn is in 8th
    }


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
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
