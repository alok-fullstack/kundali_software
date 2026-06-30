"""
Dasha-Transit Synchronization Module for Vedic Rashifal

Based on BPHS Chapter 41-46 (Dasha Effects) and Chapter 46 (Gochara Phala),
and Phaladeepika Chapter 20 and 26.

Key Principle: "Dasha phala Gochar phalena samyuktam bhavati"
(Dasha results combined with transit results manifest together)

Author: Claude Code Assistant
Date: 2026-06-28
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class DashaTransitSyncResult:
    """Result of Dasha-Transit synchronization analysis."""
    mahadasha_lord: str
    antardasha_lord: str
    pratyantardasha_lord: Optional[str]
    mahadasha_transit_house: int
    antardasha_transit_house: int
    modifier: float
    sync_type: str
    breakdown: Dict


# =============================================================================
# DASHA-TRANSIT SYNCHRONIZATION CONSTANTS (Per BPHS/Phaladeepika)
# =============================================================================

# Dasha Level Weights (must sum to ~1.0 for primary levels)
DASHA_LEVEL_WEIGHTS = {
    "mahadasha": 0.50,       # Primary weight - most significant
    "antardasha": 0.30,      # Secondary weight
    "pratyantardasha": 0.15, # Tertiary weight
    "sookshma": 0.05,        # Fine-tuning (optional)
}

# Amplification when Dasha lord is also the transiting planet
# Per BPHS: "When the Dasha lord transits favorable houses, effects amplified by half again"
DASHA_LORD_SELF_TRANSIT_AMPLIFICATION = {
    "SATURN": 1.5,    # Saturn's own transit during Saturn Dasha - MOST significant
    "JUPITER": 1.45,  # Jupiter's own transit during Jupiter Dasha
    "RAHU": 1.4,      # Rahu's own transit during Rahu Dasha
    "KETU": 1.35,     # Ketu's own transit during Ketu Dasha
    "MARS": 1.3,      # Mars own transit during Mars Dasha
    "SUN": 1.25,
    "VENUS": 1.25,
    "MOON": 1.2,
    "MERCURY": 1.2,
}

# Favorable transit houses from Moon (Gochara Phal)
FAVORABLE_TRANSIT_HOUSES = {3, 6, 10, 11}

# Unfavorable transit houses from Moon
UNFAVORABLE_TRANSIT_HOUSES = {1, 2, 4, 5, 7, 8, 9, 12}

# Natural benefic/malefic classification
NATURAL_BENEFICS = {"JUPITER", "VENUS", "MOON", "MERCURY"}
NATURAL_MALEFICS = {"SATURN", "MARS", "RAHU", "KETU", "SUN"}

# House-specific score modifications for Dasha lord transit (from Moon)
DASHA_LORD_TRANSIT_HOUSE_SCORES = {
    1: -0.5,   # Obstacles to self
    2: -0.5,   # Financial concerns
    3: +1.5,   # Victory, courage
    4: -1.0,   # Domestic troubles
    5: -0.5,   # Concerns about children/creativity
    6: +2.0,   # Victory over enemies
    7: -0.5,   # Relationship challenges
    8: -1.5,   # Transformation, obstacles (most unfavorable)
    9: 0.0,    # Mixed (trikona)
    10: +2.0,  # Career success
    11: +2.5,  # Maximum gains (most favorable)
    12: -1.0,  # Expenses, losses
}


# =============================================================================
# MAIN DASHA-TRANSIT SYNCHRONIZATION CLASS
# =============================================================================

class DashaTransitSynchronizer:
    """
    Calculates Dasha-Transit synchronization effects for Rashifal predictions.

    Usage:
        sync = DashaTransitSynchronizer(current_dasha, transit_positions, moon_rashi_num)
        modifier, breakdown = sync.calculate_sync_score()
        modified_score = base_score * modifier
    """

    def __init__(
        self,
        current_dasha: Dict,
        transit_positions: Dict,
        moon_rashi_num: int,
        lagna_rashi: str = None
    ):
        """
        Initialize the synchronizer.

        Args:
            current_dasha: Dict with mahadasha, antardasha, pratyantardasha info
            transit_positions: Current planetary positions dict
            moon_rashi_num: Natal Moon's rashi number (0-11)
            lagna_rashi: Optional Lagna rashi name for functional benefic analysis
        """
        self.current_dasha = current_dasha
        self.transit_positions = transit_positions
        self.moon_rashi_num = moon_rashi_num
        self.lagna_rashi = lagna_rashi

        # Extract dasha lords
        self.mahadasha_lord = self._normalize_planet_name(
            current_dasha.get("mahadasha", {}).get("planet", "")
        )
        self.antardasha_lord = self._normalize_planet_name(
            current_dasha.get("antardasha", {}).get("planet", "")
        )
        self.pratyantardasha_lord = self._normalize_planet_name(
            current_dasha.get("pratyantardasha", {}).get("planet", "")
        )

    def _normalize_planet_name(self, name: str) -> str:
        """Convert dasha planet names to transit planet names."""
        if not name:
            return ""
        name_map = {
            "Ketu": "KETU", "Venus": "VENUS", "Sun": "SUN",
            "Moon": "MOON", "Mars": "MARS", "Rahu": "RAHU",
            "Jupiter": "JUPITER", "Saturn": "SATURN", "Mercury": "MERCURY",
        }
        return name_map.get(name, name.upper())

    def _get_transit_house_from_moon(self, planet_name: str) -> int:
        """Get the house number of a transiting planet from natal Moon."""
        if planet_name not in self.transit_positions:
            return 1  # Default

        transit_rashi = self.transit_positions[planet_name].get("rashi_num", 0)
        return ((transit_rashi - self.moon_rashi_num) % 12) + 1

    def _is_favorable_transit(self, house: int) -> bool:
        """Check if transit house is favorable."""
        return house in FAVORABLE_TRANSIT_HOUSES

    def _is_benefic_dasha_lord(self, planet: str) -> bool:
        """Check if dasha lord is naturally benefic."""
        return planet in NATURAL_BENEFICS

    def calculate_sync_score(self) -> Tuple[float, Dict]:
        """
        Calculate the Dasha-Transit synchronization score modifier.

        Returns:
            Tuple of (modifier, detailed_breakdown)
            modifier: Float value to multiply with base transit score (0.5 to 1.5)
            detailed_breakdown: Dict with component scores
        """
        breakdown = {
            "mahadasha_component": 0.0,
            "mahadasha_transit_house": None,
            "antardasha_component": 0.0,
            "antardasha_transit_house": None,
            "pratyantardasha_component": 0.0,
            "pratyantardasha_transit_house": None,
            "self_transit_bonus": 0.0,
            "total_modifier": 1.0,
        }

        # =========================
        # MAHADASHA LORD ANALYSIS
        # =========================
        if self.mahadasha_lord:
            maha_house = self._get_transit_house_from_moon(self.mahadasha_lord)
            maha_house_score = DASHA_LORD_TRANSIT_HOUSE_SCORES.get(maha_house, 0)

            # Apply weight
            maha_contribution = maha_house_score * DASHA_LEVEL_WEIGHTS["mahadasha"]
            breakdown["mahadasha_component"] = maha_contribution
            breakdown["mahadasha_transit_house"] = maha_house

            # Check for self-transit amplification
            if self.mahadasha_lord in self.transit_positions:
                if self._is_favorable_transit(maha_house):
                    self_amp = DASHA_LORD_SELF_TRANSIT_AMPLIFICATION.get(self.mahadasha_lord, 1.0)
                    breakdown["self_transit_bonus"] += (self_amp - 1.0) * 0.5

        # =========================
        # ANTARDASHA LORD ANALYSIS
        # =========================
        if self.antardasha_lord:
            antar_house = self._get_transit_house_from_moon(self.antardasha_lord)
            antar_house_score = DASHA_LORD_TRANSIT_HOUSE_SCORES.get(antar_house, 0)

            antar_contribution = antar_house_score * DASHA_LEVEL_WEIGHTS["antardasha"]
            breakdown["antardasha_component"] = antar_contribution
            breakdown["antardasha_transit_house"] = antar_house

            # Self-transit check for antardasha
            if self.antardasha_lord in self.transit_positions:
                if self._is_favorable_transit(antar_house):
                    self_amp = DASHA_LORD_SELF_TRANSIT_AMPLIFICATION.get(self.antardasha_lord, 1.0)
                    breakdown["self_transit_bonus"] += (self_amp - 1.0) * 0.3

        # =========================
        # PRATYANTARDASHA LORD ANALYSIS
        # =========================
        if self.pratyantardasha_lord:
            pratyantar_house = self._get_transit_house_from_moon(self.pratyantardasha_lord)
            pratyantar_house_score = DASHA_LORD_TRANSIT_HOUSE_SCORES.get(pratyantar_house, 0)

            pratyantar_contribution = pratyantar_house_score * DASHA_LEVEL_WEIGHTS["pratyantardasha"]
            breakdown["pratyantardasha_component"] = pratyantar_contribution
            breakdown["pratyantardasha_transit_house"] = pratyantar_house

        # =========================
        # CALCULATE TOTAL MODIFIER
        # =========================
        component_sum = (
            breakdown["mahadasha_component"] +
            breakdown["antardasha_component"] +
            breakdown["pratyantardasha_component"] +
            breakdown["self_transit_bonus"]
        )

        # Convert to multiplier (centered around 1.0)
        # Range: approximately 0.5 to 1.5
        total_modifier = 1.0 + (component_sum / 10.0)

        # Clamp to reasonable range
        total_modifier = max(0.5, min(1.5, total_modifier))

        breakdown["total_modifier"] = round(total_modifier, 3)

        return (total_modifier, breakdown)

    def get_sync_type(self, modifier: float) -> str:
        """Classify the synchronization type based on modifier."""
        if modifier >= 1.35:
            return "highly_favorable"
        elif modifier >= 1.15:
            return "favorable"
        elif modifier >= 0.85:
            return "neutral"
        elif modifier >= 0.65:
            return "unfavorable"
        else:
            return "highly_unfavorable"


# =============================================================================
# INTEGRATION FUNCTION FOR RASHIFAL
# =============================================================================

def apply_dasha_transit_sync(
    base_score: float,
    current_dasha: Dict,
    transit_positions: Dict,
    moon_rashi_num: int,
    lagna_rashi: str = None
) -> Tuple[float, Dict]:
    """
    Apply Dasha-Transit synchronization to a base Rashifal score.

    This is the main entry point for integrating Dasha-Transit sync
    into the existing Rashifal calculation.

    Args:
        base_score: The base transit score (0-10 scale)
        current_dasha: Dict with current dasha periods
        transit_positions: Current planetary positions
        moon_rashi_num: Natal Moon rashi (0-11)
        lagna_rashi: Optional lagna rashi name

    Returns:
        Tuple of (modified_score, sync_details)

    Example:
        base_score = 6.5
        modified_score, details = apply_dasha_transit_sync(
            base_score=6.5,
            current_dasha=dasha_info,
            transit_positions=positions,
            moon_rashi_num=4  # Leo Moon
        )
        # modified_score might be 7.8 if favorable sync
    """
    synchronizer = DashaTransitSynchronizer(
        current_dasha=current_dasha,
        transit_positions=transit_positions,
        moon_rashi_num=moon_rashi_num,
        lagna_rashi=lagna_rashi
    )

    modifier, breakdown = synchronizer.calculate_sync_score()
    sync_type = synchronizer.get_sync_type(modifier)

    # Apply modifier to base score
    modified_score = base_score * modifier

    # Clamp to 1-10 range
    modified_score = max(1.0, min(10.0, modified_score))

    sync_details = {
        "base_score": round(base_score, 1),
        "modified_score": round(modified_score, 1),
        "modifier": modifier,
        "sync_type": sync_type,
        "sync_type_hindi": SYNC_TYPE_HINDI.get(sync_type, ""),
        "breakdown": breakdown,
        "mahadasha_lord": synchronizer.mahadasha_lord,
        "antardasha_lord": synchronizer.antardasha_lord,
    }

    return (round(modified_score, 1), sync_details)


# =============================================================================
# PREDICTION TEXT MODIFIERS
# =============================================================================

SYNC_TYPE_HINDI = {
    "highly_favorable": "अत्यंत अनुकूल",
    "favorable": "अनुकूल",
    "neutral": "सामान्य",
    "unfavorable": "प्रतिकूल",
    "highly_unfavorable": "अत्यंत प्रतिकूल",
}

DASHA_TRANSIT_SYNC_PREDICTIONS_HINDI = {
    "highly_favorable": [
        "दशा और गोचर का अद्भुत संयोग! महादशा स्वामी की शुभ स्थिति आपके लिए अत्यंत लाभकारी है।",
        "वर्तमान दशा स्वामी का गोचर आपके पक्ष में है। इस समय का पूर्ण लाभ उठाएं।",
        "दशा-गोचर संयोग उत्तम है। आपके प्रयास अवश्य सफल होंगे।",
    ],
    "favorable": [
        "दशा स्वामी का गोचर सामान्यतः अनुकूल है।",
        "वर्तमान ग्रह दशा सहयोगी है। धैर्य से काम लें।",
        "दशा और गोचर का मिलन शुभ है।",
    ],
    "neutral": [
        "दशा और गोचर का संतुलित प्रभाव है।",
        "न अत्यधिक लाभ न हानि। सामान्य प्रयास जारी रखें।",
        "दशा-गोचर संयोग मध्यम है।",
    ],
    "unfavorable": [
        "दशा स्वामी का गोचर प्रतिकूल है। सावधानी से आगे बढ़ें।",
        "वर्तमान समय चुनौतीपूर्ण है। बड़े फैसले टालें।",
        "दशा और गोचर का संयोग अनुकूल नहीं है।",
    ],
    "highly_unfavorable": [
        "दशा-गोचर संयोग कठिन है। विशेष सावधानी बरतें।",
        "महादशा स्वामी अशुभ भाव में है। धैर्य और संयम से काम लें।",
        "यह समय धैर्य का है। उपाय करें और सकारात्मक रहें।",
    ],
}


def get_dasha_sync_prediction(sync_type: str, seed: int = 0) -> str:
    """Get a prediction text based on Dasha-Transit sync type."""
    predictions = DASHA_TRANSIT_SYNC_PREDICTIONS_HINDI.get(sync_type, [])
    if predictions:
        return predictions[seed % len(predictions)]
    return ""
