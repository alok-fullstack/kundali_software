"""
Ashtakavarga Calculation Module - Per BPHS (Brihat Parashara Hora Shastra)

This module implements authentic Vedic Ashtakavarga calculations including:
- Bhinnashtakavarga (BAV) - Individual planet bindus
- Sarvashtakavarga (SAV) - Total bindus per house
- Trikona Shodhana - Triangle reduction
- Ekadhipatya Shodhana - Single lordship reduction
- Moorti Nirnaya - Classification by bindus (Swarna/Rajata/Tamra/Loha)

References:
- Brihat Parashara Hora Shastra, Chapters 64-72
- Phaladeepika by Mantreshwara
- Jataka Parijata

Author: Claude Code Assistant
Date: 2026-06-28
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum

from .config import RASHI_LIST as RASHIS, RASHI_LORDS


class Moorti(Enum):
    """Moorti classification based on bindu count (BPHS)"""
    SWARNA = "swarna"    # Gold - 5+ bindus - Excellent
    RAJATA = "rajata"    # Silver - 4 bindus - Good
    TAMRA = "tamra"      # Copper - 3 bindus - Moderate
    LOHA = "loha"        # Iron - 0-2 bindus - Weak


# Ashtakavarga Bindu Contribution Rules from BPHS
# Key: planet receiving bindus
# Value: dict with contributing planets and their benefic house positions
ASHTAKAVARGA_RULES: Dict[str, Dict[str, List[int]]] = {
    "SUN": {
        "SUN": [1, 2, 4, 7, 8, 9, 10, 11],
        "MOON": [3, 6, 10, 11],
        "MARS": [1, 2, 4, 7, 8, 9, 10, 11],
        "MERCURY": [3, 5, 6, 9, 10, 11, 12],
        "JUPITER": [5, 6, 9, 11],
        "VENUS": [6, 7, 12],
        "SATURN": [1, 2, 4, 7, 8, 9, 10, 11],
        "LAGNA": [3, 4, 6, 10, 11, 12],
    },
    "MOON": {
        "SUN": [3, 6, 7, 8, 10, 11],
        "MOON": [1, 3, 6, 7, 10, 11],
        "MARS": [2, 3, 5, 6, 9, 10, 11],
        "MERCURY": [1, 3, 4, 5, 7, 8, 10, 11],
        "JUPITER": [1, 4, 7, 8, 10, 11, 12],
        "VENUS": [3, 4, 5, 7, 9, 10, 11],
        "SATURN": [3, 5, 6, 11],
        "LAGNA": [3, 6, 10, 11],
    },
    "MARS": {
        "SUN": [3, 5, 6, 10, 11],
        "MOON": [3, 6, 11],
        "MARS": [1, 2, 4, 7, 8, 10, 11],
        "MERCURY": [3, 5, 6, 11],
        "JUPITER": [6, 10, 11, 12],
        "VENUS": [6, 8, 11, 12],
        "SATURN": [1, 4, 7, 8, 9, 10, 11],
        "LAGNA": [1, 3, 6, 10, 11],
    },
    "MERCURY": {
        "SUN": [5, 6, 9, 11, 12],
        "MOON": [2, 4, 6, 8, 10, 11],
        "MARS": [1, 2, 4, 7, 8, 9, 10, 11],
        "MERCURY": [1, 3, 5, 6, 9, 10, 11, 12],
        "JUPITER": [6, 8, 11, 12],
        "VENUS": [1, 2, 3, 4, 5, 8, 9, 11],
        "SATURN": [1, 2, 4, 7, 8, 9, 10, 11],
        "LAGNA": [1, 2, 4, 6, 8, 10, 11],
    },
    "JUPITER": {
        "SUN": [1, 2, 3, 4, 7, 8, 9, 10, 11],
        "MOON": [2, 5, 7, 9, 11],
        "MARS": [1, 2, 4, 7, 8, 10, 11],
        "MERCURY": [1, 2, 4, 5, 6, 9, 10, 11],
        "JUPITER": [1, 2, 3, 4, 7, 8, 10, 11],
        "VENUS": [2, 5, 6, 9, 10, 11],
        "SATURN": [3, 5, 6, 12],
        "LAGNA": [1, 2, 4, 5, 6, 7, 9, 10, 11],
    },
    "VENUS": {
        "SUN": [8, 11, 12],
        "MOON": [1, 2, 3, 4, 5, 8, 9, 11, 12],
        "MARS": [3, 5, 6, 9, 11, 12],
        "MERCURY": [3, 5, 6, 9, 11],
        "JUPITER": [5, 8, 9, 10, 11],
        "VENUS": [1, 2, 3, 4, 5, 8, 9, 10, 11],
        "SATURN": [3, 4, 5, 8, 9, 10, 11],
        "LAGNA": [1, 2, 3, 4, 5, 8, 9, 11],
    },
    "SATURN": {
        "SUN": [1, 2, 4, 7, 8, 10, 11],
        "MOON": [3, 6, 11],
        "MARS": [3, 5, 6, 10, 11, 12],
        "MERCURY": [6, 8, 9, 10, 11, 12],
        "JUPITER": [5, 6, 11, 12],
        "VENUS": [6, 11, 12],
        "SATURN": [3, 5, 6, 11],
        "LAGNA": [1, 3, 4, 6, 10, 11],
    },
}

# Maximum possible bindus for each planet's BAV
MAX_BINDUS: Dict[str, int] = {
    "SUN": 48,
    "MOON": 49,
    "MARS": 39,
    "MERCURY": 54,
    "JUPITER": 56,
    "VENUS": 52,
    "SATURN": 39,
}

# Total maximum SAV bindus
MAX_SAV_TOTAL = 337

# Trikona groups for shodhana (1-indexed house numbers)
TRIKONA_GROUPS: List[List[int]] = [
    [1, 5, 9],   # Fire trikona (Dharma)
    [2, 6, 10],  # Earth trikona (Artha)
    [3, 7, 11],  # Air trikona (Kama)
    [4, 8, 12],  # Water trikona (Moksha)
]

# Single lordship pairs for Ekadhipatya Shodhana (0-indexed rashi numbers)
EKADHIPATYA_PAIRS: List[Tuple[int, int]] = [
    (0, 7),   # Mesha-Vrishchika (Mars)
    (1, 6),   # Vrishabha-Tula (Venus)
    (2, 5),   # Mithuna-Kanya (Mercury)
    (8, 11),  # Dhanu-Meena (Jupiter)
    (9, 10),  # Makara-Kumbha (Saturn)
]

# Kakshya (Sub-division) System - Per BPHS
# Each sign (30°) is divided into 8 Kakshyas of 3°45' (3.75°) each
# The lords follow this sequence within each sign
KAKSHYA_LORDS: List[str] = [
    "SATURN",   # 0°00' - 3°45'
    "JUPITER",  # 3°45' - 7°30'
    "MARS",     # 7°30' - 11°15'
    "SUN",      # 11°15' - 15°00'
    "VENUS",    # 15°00' - 18°45'
    "MERCURY",  # 18°45' - 22°30'
    "MOON",     # 22°30' - 26°15'
    "LAGNA",    # 26°15' - 30°00'
]

KAKSHYA_SPAN = 3.75  # degrees per kakshya


@dataclass
class KakshyaData:
    """Kakshya information for a planet's position"""
    kakshya_num: int  # 1-8
    kakshya_lord: str
    degree_in_sign: float
    is_benefic_kakshya: bool  # True if kakshya lord is natural benefic


@dataclass
class BinduData:
    """Bindu data for a single house/sign"""
    house: int
    rashi: str
    bindus: int
    moorti: Moorti

    @property
    def is_favorable(self) -> bool:
        return self.bindus >= 4

    @property
    def strength_percentage(self) -> float:
        return (self.bindus / 8) * 100


@dataclass
class BhinnashtakavargaResult:
    """Result of Bhinnashtakavarga calculation for a single planet"""
    planet: str
    bindus_by_house: Dict[int, int]  # house (1-12) -> bindu count
    total_bindus: int
    max_possible: int

    def get_moorti(self, house: int) -> Moorti:
        bindus = self.bindus_by_house.get(house, 0)
        return get_moorti(bindus)

    def get_bindu_data(self, house: int, rashi: str) -> BinduData:
        bindus = self.bindus_by_house.get(house, 0)
        return BinduData(
            house=house,
            rashi=rashi,
            bindus=bindus,
            moorti=get_moorti(bindus)
        )


@dataclass
class SarvashtakavargaResult:
    """Result of Sarvashtakavarga calculation"""
    bindus_by_house: Dict[int, int]  # house (1-12) -> total bindu count
    total_bindus: int
    average_per_house: float

    def get_strength(self, house: int) -> str:
        """Get strength classification for a house"""
        bindus = self.bindus_by_house.get(house, 0)
        if bindus >= 30:
            return "excellent"
        elif bindus >= 28:
            return "good"
        elif bindus >= 25:
            return "average"
        else:
            return "weak"


@dataclass
class AshtakavargaResult:
    """Complete Ashtakavarga calculation result"""
    bav: Dict[str, BhinnashtakavargaResult]  # planet -> BAV result
    sav: SarvashtakavargaResult
    sav_after_reduction: Optional[SarvashtakavargaResult] = None


def get_moorti(bindus: int) -> Moorti:
    """Classify bindu count into Moorti category per BPHS"""
    if bindus >= 5:
        return Moorti.SWARNA
    elif bindus == 4:
        return Moorti.RAJATA
    elif bindus == 3:
        return Moorti.TAMRA
    else:
        return Moorti.LOHA


def get_house_from_reference(planet_rashi_num: int, reference_rashi_num: int) -> int:
    """
    Calculate house number of planet from reference point.
    Both inputs are 0-indexed rashi numbers.
    Returns 1-indexed house number (1-12).
    """
    house = ((planet_rashi_num - reference_rashi_num) % 12) + 1
    return house


class AshtakavargaCalculator:
    """
    Calculator for Ashtakavarga system per BPHS.

    Usage:
        calc = AshtakavargaCalculator(kundali)
        result = calc.calculate()

        # Get bindus for Jupiter in 5th house
        jupiter_bav = result.bav["JUPITER"]
        bindus = jupiter_bav.bindus_by_house[5]

        # Get SAV for 10th house
        sav_10th = result.sav.bindus_by_house[10]
    """

    PLANETS = ["SUN", "MOON", "MARS", "MERCURY", "JUPITER", "VENUS", "SATURN"]

    def __init__(self, kundali):
        """
        Initialize with a Kundali object.

        Args:
            kundali: Kundali object with lagna and planets attributes
        """
        self.kundali = kundali
        self._planet_positions: Dict[str, int] = {}  # planet -> rashi_num (0-indexed)
        self._lagna_rashi_num: int = 0
        self._extract_positions()

    def _extract_positions(self):
        """Extract planet and lagna positions from kundali"""
        # Get lagna rashi number
        lagna_rashi = self.kundali.lagna.get("rashi", "Mesha")
        self._lagna_rashi_num = RASHIS.index(lagna_rashi) if lagna_rashi in RASHIS else 0

        # Get planet positions
        planets = self.kundali.planets
        for planet in self.PLANETS:
            if planet in planets:
                planet_rashi = planets[planet].get("rashi", "Mesha")
                self._planet_positions[planet] = RASHIS.index(planet_rashi) if planet_rashi in RASHIS else 0

    def calculate_bhinnashtakavarga(self, target_planet: str) -> BhinnashtakavargaResult:
        """
        Calculate Bhinnashtakavarga for a single planet.

        Args:
            target_planet: Planet name (SUN, MOON, MARS, etc.)

        Returns:
            BhinnashtakavargaResult with bindus per house
        """
        if target_planet not in ASHTAKAVARGA_RULES:
            raise ValueError(f"Invalid planet: {target_planet}")

        rules = ASHTAKAVARGA_RULES[target_planet]
        bindus_by_house: Dict[int, int] = {h: 0 for h in range(1, 13)}

        # For each of the 12 houses (signs)
        for house in range(1, 13):
            # Convert house to rashi number (0-indexed)
            target_rashi_num = (self._lagna_rashi_num + house - 1) % 12
            bindu_count = 0

            # Check contribution from each planet and lagna
            for contributor, benefic_houses in rules.items():
                if contributor == "LAGNA":
                    reference_rashi_num = self._lagna_rashi_num
                else:
                    reference_rashi_num = self._planet_positions.get(contributor, 0)

                # Calculate house of target from contributor
                house_from_contributor = get_house_from_reference(target_rashi_num, reference_rashi_num)

                # Check if this position gives a bindu
                if house_from_contributor in benefic_houses:
                    bindu_count += 1

            bindus_by_house[house] = bindu_count

        total = sum(bindus_by_house.values())

        return BhinnashtakavargaResult(
            planet=target_planet,
            bindus_by_house=bindus_by_house,
            total_bindus=total,
            max_possible=MAX_BINDUS.get(target_planet, 48)
        )

    def calculate_sarvashtakavarga(self, bav_results: Dict[str, BhinnashtakavargaResult]) -> SarvashtakavargaResult:
        """
        Calculate Sarvashtakavarga by summing all BAV values.

        Args:
            bav_results: Dictionary of BAV results for all planets

        Returns:
            SarvashtakavargaResult with total bindus per house
        """
        sav_by_house: Dict[int, int] = {h: 0 for h in range(1, 13)}

        for planet, bav in bav_results.items():
            for house, bindus in bav.bindus_by_house.items():
                sav_by_house[house] += bindus

        total = sum(sav_by_house.values())

        return SarvashtakavargaResult(
            bindus_by_house=sav_by_house,
            total_bindus=total,
            average_per_house=total / 12
        )

    def apply_trikona_shodhana(self, bav: BhinnashtakavargaResult) -> BhinnashtakavargaResult:
        """
        Apply Trikona Shodhana (triangle reduction) to BAV.

        Args:
            bav: Original BAV result

        Returns:
            New BAV result with reduction applied
        """
        reduced_bindus = dict(bav.bindus_by_house)

        for trikona in TRIKONA_GROUPS:
            # Get bindus in the three houses of this trikona
            values = [reduced_bindus[h] for h in trikona]
            min_val = min(values)

            # Subtract minimum from all three
            for h in trikona:
                reduced_bindus[h] -= min_val

        return BhinnashtakavargaResult(
            planet=bav.planet,
            bindus_by_house=reduced_bindus,
            total_bindus=sum(reduced_bindus.values()),
            max_possible=bav.max_possible
        )

    def apply_ekadhipatya_shodhana(self, sav: SarvashtakavargaResult) -> SarvashtakavargaResult:
        """
        Apply Ekadhipatya Shodhana (single lordship reduction) to SAV.

        Args:
            sav: Original SAV result

        Returns:
            New SAV result with reduction applied
        """
        reduced_bindus = dict(sav.bindus_by_house)

        for rashi1, rashi2 in EKADHIPATYA_PAIRS:
            # Convert rashi numbers to houses from lagna
            house1 = ((rashi1 - self._lagna_rashi_num) % 12) + 1
            house2 = ((rashi2 - self._lagna_rashi_num) % 12) + 1

            # Get bindus in both houses
            val1 = reduced_bindus[house1]
            val2 = reduced_bindus[house2]
            min_val = min(val1, val2)

            # Subtract minimum from both
            reduced_bindus[house1] -= min_val
            reduced_bindus[house2] -= min_val

        total = sum(reduced_bindus.values())

        return SarvashtakavargaResult(
            bindus_by_house=reduced_bindus,
            total_bindus=total,
            average_per_house=total / 12
        )

    def calculate(self, apply_reductions: bool = False) -> AshtakavargaResult:
        """
        Calculate complete Ashtakavarga.

        Args:
            apply_reductions: If True, also calculate reduced SAV

        Returns:
            AshtakavargaResult with BAV for all planets and SAV
        """
        # Calculate BAV for all planets
        bav_results: Dict[str, BhinnashtakavargaResult] = {}
        for planet in self.PLANETS:
            bav_results[planet] = self.calculate_bhinnashtakavarga(planet)

        # Calculate SAV
        sav = self.calculate_sarvashtakavarga(bav_results)

        # Apply reductions if requested
        sav_reduced = None
        if apply_reductions:
            sav_reduced = self.apply_ekadhipatya_shodhana(sav)

        return AshtakavargaResult(
            bav=bav_results,
            sav=sav,
            sav_after_reduction=sav_reduced
        )

    def get_transit_strength(self, transit_planet: str, transit_rashi: str) -> Dict:
        """
        Get Ashtakavarga-based strength for a planet's transit.

        This is the KEY method for Rashifal predictions.

        Args:
            transit_planet: Planet in transit (SUN, MOON, MARS, etc.)
            transit_rashi: Rashi the planet is transiting through

        Returns:
            Dictionary with bindu count, moorti, and strength assessment
        """
        if transit_planet not in self.PLANETS:
            return {"bindus": 4, "moorti": Moorti.RAJATA, "strength": "average"}

        # Calculate BAV for the transit planet
        bav = self.calculate_bhinnashtakavarga(transit_planet)

        # Find the house number for the transit rashi
        transit_rashi_num = RASHIS.index(transit_rashi) if transit_rashi in RASHIS else 0
        house = ((transit_rashi_num - self._lagna_rashi_num) % 12) + 1

        bindus = bav.bindus_by_house[house]
        moorti = get_moorti(bindus)

        # Determine strength
        if bindus >= 5:
            strength = "excellent"
        elif bindus == 4:
            strength = "good"
        elif bindus == 3:
            strength = "moderate"
        else:
            strength = "weak"

        return {
            "bindus": bindus,
            "moorti": moorti,
            "moorti_name": moorti.value,
            "strength": strength,
            "house": house,
            "max_bindus": 8,
            "percentage": (bindus / 8) * 100
        }

    def get_transit_strength_from_moon(self, transit_planet: str, transit_rashi: str, moon_rashi: str) -> Dict:
        """
        Get Ashtakavarga-based transit strength from Moon sign (for Rashifal).

        Args:
            transit_planet: Planet in transit
            transit_rashi: Rashi the planet is transiting through
            moon_rashi: Natal Moon's rashi

        Returns:
            Dictionary with bindu count and strength from Moon's perspective
        """
        if transit_planet not in self.PLANETS:
            return {"bindus": 4, "moorti": Moorti.RAJATA, "strength": "average"}

        # Calculate BAV for the transit planet
        bav = self.calculate_bhinnashtakavarga(transit_planet)

        # Find house from Moon
        transit_rashi_num = RASHIS.index(transit_rashi) if transit_rashi in RASHIS else 0
        moon_rashi_num = RASHIS.index(moon_rashi) if moon_rashi in RASHIS else 0
        house_from_moon = ((transit_rashi_num - moon_rashi_num) % 12) + 1

        # Map house_from_moon to actual house in BAV
        # BAV is calculated from Lagna, so we need to adjust
        actual_house = ((transit_rashi_num - self._lagna_rashi_num) % 12) + 1

        bindus = bav.bindus_by_house[actual_house]
        moorti = get_moorti(bindus)

        # Determine strength
        if bindus >= 5:
            strength = "excellent"
        elif bindus == 4:
            strength = "good"
        elif bindus == 3:
            strength = "moderate"
        else:
            strength = "weak"

        return {
            "bindus": bindus,
            "moorti": moorti,
            "moorti_name": moorti.value,
            "strength": strength,
            "house_from_moon": house_from_moon,
            "house_from_lagna": actual_house,
            "max_bindus": 8,
            "percentage": (bindus / 8) * 100
        }


def calculate_ashtakavarga(kundali) -> AshtakavargaResult:
    """
    Convenience function to calculate Ashtakavarga.

    Args:
        kundali: Kundali object

    Returns:
        AshtakavargaResult
    """
    calc = AshtakavargaCalculator(kundali)
    return calc.calculate()


# =============================================================================
# KAKSHYA (Sub-division) Functions
# =============================================================================

def calculate_kakshya(longitude: float) -> KakshyaData:
    """
    Calculate Kakshya information for a given longitude.

    Per BPHS, each sign is divided into 8 Kakshyas of 3°45' each.
    The Kakshya lord sequence is: Saturn, Jupiter, Mars, Sun, Venus, Mercury, Moon, Lagna.

    Args:
        longitude: Planet's longitude in degrees (0-360)

    Returns:
        KakshyaData with kakshya number, lord, and benefic status
    """
    # Get degree within the sign (0-30)
    degree_in_sign = longitude % 30

    # Calculate which kakshya (1-8)
    kakshya_num = int(degree_in_sign / KAKSHYA_SPAN) + 1
    kakshya_num = min(kakshya_num, 8)  # Ensure max is 8

    # Get kakshya lord
    kakshya_lord = KAKSHYA_LORDS[kakshya_num - 1]

    # Determine if benefic (Jupiter, Venus, Mercury, Moon are natural benefics)
    natural_benefics = ["JUPITER", "VENUS", "MERCURY", "MOON"]
    is_benefic = kakshya_lord in natural_benefics

    return KakshyaData(
        kakshya_num=kakshya_num,
        kakshya_lord=kakshya_lord,
        degree_in_sign=round(degree_in_sign, 2),
        is_benefic_kakshya=is_benefic
    )


def get_kakshya_modifier(kakshya: KakshyaData, natal_planet_status: Dict[str, str] = None) -> float:
    """
    Get Kakshya-based modifier for transit strength.

    Per BPHS:
    - Transit in benefic-ruled Kakshya enhances positive effects
    - Transit in malefic-ruled Kakshya reduces positive effects
    - If Kakshya lord is strong in natal chart, effect is enhanced

    Args:
        kakshya: KakshyaData for the transit
        natal_planet_status: Optional dict with planet -> "strong"/"weak"/"neutral"

    Returns:
        Modifier value (-0.2 to +0.2)
    """
    base_modifier = 0.0

    # Benefic kakshya gives positive modifier
    if kakshya.is_benefic_kakshya:
        base_modifier = 0.1
    else:
        # Malefic kakshya (Saturn, Mars, Sun) gives slight negative
        if kakshya.kakshya_lord in ["SATURN", "MARS"]:
            base_modifier = -0.1
        elif kakshya.kakshya_lord == "SUN":
            base_modifier = 0.0  # Sun is neutral
        else:  # LAGNA
            base_modifier = 0.05  # Lagna kakshya is slightly positive

    # Enhance based on natal planet status if provided
    if natal_planet_status and kakshya.kakshya_lord in natal_planet_status:
        status = natal_planet_status[kakshya.kakshya_lord]
        if status == "strong":
            base_modifier += 0.1
        elif status == "weak":
            base_modifier -= 0.05

    return max(-0.2, min(0.2, base_modifier))


# =============================================================================
# SADE SATI Functions
# =============================================================================

def check_sade_sati(saturn_rashi_num: int, moon_rashi_num: int) -> Dict:
    """
    Check if a person is undergoing Sade Sati or Dhaiya.

    Sade Sati: Saturn in 12th, 1st, or 2nd from Moon (7.5 years total)
    Dhaiya (Small Panoti): Saturn in 4th or 8th from Moon (~2.5 years each)

    Args:
        saturn_rashi_num: Saturn's current rashi (0-11)
        moon_rashi_num: Natal Moon's rashi (0-11)

    Returns:
        Dict with sade_sati status, phase, and severity
    """
    house_from_moon = ((saturn_rashi_num - moon_rashi_num) % 12) + 1

    result = {
        "is_sade_sati": False,
        "is_dhaiya": False,
        "phase": None,
        "phase_hindi": None,
        "severity": 0.0,  # 0.0 to 1.0
        "house_from_moon": house_from_moon,
        "description": "",
        "description_hindi": "",
    }

    if house_from_moon == 12:
        # First phase - Rising Sade Sati
        result["is_sade_sati"] = True
        result["phase"] = "rising"
        result["phase_hindi"] = "आरोही (प्रथम चरण)"
        result["severity"] = 0.6
        result["description"] = "First phase of Sade Sati - mental stress, expenses increase"
        result["description_hindi"] = "साढ़े साती का पहला चरण - मानसिक तनाव, व्यय वृद्धि"

    elif house_from_moon == 1:
        # Second phase - Peak Sade Sati (Saturn over Moon)
        result["is_sade_sati"] = True
        result["phase"] = "peak"
        result["phase_hindi"] = "शिखर (द्वितीय चरण)"
        result["severity"] = 1.0  # Most intense
        result["description"] = "Peak of Sade Sati - maximum challenges, health and career issues"
        result["description_hindi"] = "साढ़े साती का शिखर - अधिकतम चुनौतियां, स्वास्थ्य और करियर समस्याएं"

    elif house_from_moon == 2:
        # Third phase - Setting Sade Sati
        result["is_sade_sati"] = True
        result["phase"] = "setting"
        result["phase_hindi"] = "अस्त (तृतीय चरण)"
        result["severity"] = 0.7
        result["description"] = "Final phase of Sade Sati - financial stress, family issues"
        result["description_hindi"] = "साढ़े साती का अंतिम चरण - आर्थिक तनाव, पारिवारिक समस्याएं"

    elif house_from_moon == 4:
        # Dhaiya - Saturn in 4th (Kantak Shani)
        result["is_dhaiya"] = True
        result["phase"] = "fourth_house"
        result["phase_hindi"] = "कंटक शनि (चतुर्थ भाव)"
        result["severity"] = 0.5
        result["description"] = "Dhaiya - domestic troubles, mother's health, property issues"
        result["description_hindi"] = "ढैय्या - गृह कष्ट, माता स्वास्थ्य, संपत्ति समस्याएं"

    elif house_from_moon == 8:
        # Dhaiya - Saturn in 8th (Ashtama Shani)
        result["is_dhaiya"] = True
        result["phase"] = "eighth_house"
        result["phase_hindi"] = "अष्टम शनि"
        result["severity"] = 0.6
        result["description"] = "Dhaiya - obstacles, sudden troubles, chronic health issues"
        result["description_hindi"] = "ढैय्या - बाधाएं, आकस्मिक कष्ट, दीर्घकालिक स्वास्थ्य समस्याएं"

    return result


def get_sade_sati_score_modifier(sade_sati_info: Dict, saturn_is_yogakaraka: bool = False) -> float:
    """
    Get score modifier based on Sade Sati status.

    Per classical texts:
    - Sade Sati generally reduces positive predictions
    - But if Saturn is Yogakaraka (Taurus, Libra lagna), effects are less severe
    - Saturn in own sign/exalted during Sade Sati is also less harmful

    Args:
        sade_sati_info: Result from check_sade_sati()
        saturn_is_yogakaraka: True if Saturn is Yogakaraka for the lagna

    Returns:
        Score modifier (-3.0 to 0.0)
    """
    if not sade_sati_info["is_sade_sati"] and not sade_sati_info["is_dhaiya"]:
        return 0.0

    base_modifier = -sade_sati_info["severity"] * 3.0  # Max -3.0 for peak

    # Reduce severity if Saturn is Yogakaraka
    if saturn_is_yogakaraka:
        base_modifier *= 0.5  # 50% reduction in negative effect

    return base_modifier
