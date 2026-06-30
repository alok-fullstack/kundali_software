"""
Vedha (Obstruction) Calculation Module - Per Classical Vedic Texts

Vedha nullifies the good effects of a planetary transit when another planet
occupies the obstruction point.

References:
- Brihat Parashara Hora Shastra
- Phaladeepika by Mantreshwara
- Uttara Kalamrita

Author: Claude Code Assistant
Date: 2026-06-28
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from .config import RASHI_LIST as RASHIS


# Vedha Points Table - Per Classical Texts
# Format: {planet: {favorable_transit_house: vedha_house}}
# If a planet transits a favorable house, but another planet is in vedha_house,
# the favorable effect is nullified.

VEDHA_POINTS: Dict[str, Dict[int, int]] = {
    "SUN": {
        3: 9,    # Sun in 3rd, vedha from 9th
        6: 12,   # Sun in 6th, vedha from 12th
        10: 4,   # Sun in 10th, vedha from 4th
        11: 5,   # Sun in 11th, vedha from 5th
    },
    "MOON": {
        1: 5,    # Moon in 1st, vedha from 5th
        3: 9,    # Moon in 3rd, vedha from 9th
        6: 12,   # Moon in 6th, vedha from 12th
        7: 2,    # Moon in 7th, vedha from 2nd
        10: 4,   # Moon in 10th, vedha from 4th
        11: 8,   # Moon in 11th, vedha from 8th
    },
    "MARS": {
        3: 12,   # Mars in 3rd, vedha from 12th
        6: 9,    # Mars in 6th, vedha from 9th
        11: 5,   # Mars in 11th, vedha from 5th
    },
    "MERCURY": {
        2: 5,    # Mercury in 2nd, vedha from 5th
        4: 3,    # Mercury in 4th, vedha from 3rd
        6: 9,    # Mercury in 6th, vedha from 9th
        8: 1,    # Mercury in 8th, vedha from 1st
        10: 8,   # Mercury in 10th, vedha from 8th
        11: 12,  # Mercury in 11th, vedha from 12th
    },
    "JUPITER": {
        2: 12,   # Jupiter in 2nd, vedha from 12th
        5: 4,    # Jupiter in 5th, vedha from 4th
        7: 3,    # Jupiter in 7th, vedha from 3rd
        9: 10,   # Jupiter in 9th, vedha from 10th
        11: 8,   # Jupiter in 11th, vedha from 8th
    },
    "VENUS": {
        1: 8,    # Venus in 1st, vedha from 8th
        2: 7,    # Venus in 2nd, vedha from 7th
        3: 1,    # Venus in 3rd, vedha from 1st
        4: 10,   # Venus in 4th, vedha from 10th
        5: 9,    # Venus in 5th, vedha from 9th
        8: 5,    # Venus in 8th, vedha from 5th
        9: 11,   # Venus in 9th, vedha from 11th
        11: 6,   # Venus in 11th, vedha from 6th
        12: 3,   # Venus in 12th, vedha from 3rd
    },
    "SATURN": {
        3: 12,   # Saturn in 3rd, vedha from 12th
        6: 9,    # Saturn in 6th, vedha from 9th
        11: 5,   # Saturn in 11th, vedha from 5th
    },
}

# Vedha Exceptions - These pairs do NOT cause vedha to each other
# Per Phaladeepika: Sun-Saturn (father-son) and Moon-Mercury are exceptions
VEDHA_EXCEPTIONS: List[Tuple[str, str]] = [
    ("SUN", "SATURN"),    # Father-son relationship
    ("SATURN", "SUN"),
    ("MOON", "MERCURY"),  # Moon and Mercury exception
    ("MERCURY", "MOON"),
]


@dataclass
class VedhaResult:
    """Result of Vedha check for a transit"""
    transit_planet: str
    transit_house: int
    has_vedha: bool
    vedha_house: Optional[int]
    vedha_planet: Optional[str]
    effect_modifier: float  # 1.0 = no vedha, 0.0 = full vedha
    description: str
    description_hindi: str


class VedhaCalculator:
    """
    Calculator for Vedha (obstruction) effects on planetary transits.

    Usage:
        calc = VedhaCalculator(natal_planets_by_house)
        result = calc.check_vedha("JUPITER", 5)  # Jupiter transiting 5th house
    """

    def __init__(self, planets_by_house: Dict[int, List[str]]):
        """
        Initialize with natal planet positions by house.

        Args:
            planets_by_house: Dict mapping house number (1-12) to list of planets in that house
        """
        self.planets_by_house = planets_by_house
        # Also create reverse mapping
        self.planet_houses: Dict[str, int] = {}
        for house, planets in planets_by_house.items():
            for planet in planets:
                self.planet_houses[planet] = house

    @classmethod
    def from_kundali(cls, kundali, moon_rashi: Optional[str] = None) -> "VedhaCalculator":
        """
        Create VedhaCalculator from Kundali object.

        Args:
            kundali: Kundali object with planets attribute
            moon_rashi: If provided, houses are calculated from Moon (for Rashifal)
                       Otherwise calculated from Lagna

        Returns:
            VedhaCalculator instance
        """
        planets_by_house: Dict[int, List[str]] = {h: [] for h in range(1, 13)}

        # Determine reference point (Moon for Rashifal, Lagna otherwise)
        if moon_rashi:
            reference_rashi_num = RASHIS.index(moon_rashi) if moon_rashi in RASHIS else 0
        else:
            lagna_rashi = kundali.lagna.get("rashi", "Mesha")
            reference_rashi_num = RASHIS.index(lagna_rashi) if lagna_rashi in RASHIS else 0

        # Map planets to houses from reference
        for planet_name, planet_data in kundali.planets.items():
            if planet_name in ["RAHU", "KETU"]:
                continue  # Rahu/Ketu don't cause vedha

            planet_rashi = planet_data.get("rashi", "Mesha")
            planet_rashi_num = RASHIS.index(planet_rashi) if planet_rashi in RASHIS else 0
            house = ((planet_rashi_num - reference_rashi_num) % 12) + 1
            planets_by_house[house].append(planet_name)

        return cls(planets_by_house)

    def check_vedha(self, transit_planet: str, transit_house: int) -> VedhaResult:
        """
        Check if a transit has vedha (obstruction).

        Args:
            transit_planet: Planet in transit
            transit_house: House the planet is transiting (1-12 from Moon)

        Returns:
            VedhaResult with details of any vedha
        """
        # Get vedha points for this planet
        vedha_points = VEDHA_POINTS.get(transit_planet, {})

        # Check if this is a favorable house with potential vedha
        vedha_house = vedha_points.get(transit_house)

        if vedha_house is None:
            # No vedha possible for this transit position
            return VedhaResult(
                transit_planet=transit_planet,
                transit_house=transit_house,
                has_vedha=False,
                vedha_house=None,
                vedha_planet=None,
                effect_modifier=1.0,
                description=f"No vedha point for {transit_planet} in house {transit_house}",
                description_hindi=f"{transit_planet} का भाव {transit_house} में कोई वेध बिंदु नहीं"
            )

        # Check if any planet is in the vedha house
        planets_in_vedha = self.planets_by_house.get(vedha_house, [])

        for vedha_planet in planets_in_vedha:
            # Check for exceptions
            if (transit_planet, vedha_planet) in VEDHA_EXCEPTIONS:
                continue

            # Vedha found!
            return VedhaResult(
                transit_planet=transit_planet,
                transit_house=transit_house,
                has_vedha=True,
                vedha_house=vedha_house,
                vedha_planet=vedha_planet,
                effect_modifier=0.0,  # Full vedha - effect nullified
                description=f"{transit_planet} in house {transit_house} has vedha from {vedha_planet} in house {vedha_house}",
                description_hindi=f"भाव {transit_house} में {transit_planet} को भाव {vedha_house} में {vedha_planet} से वेध है"
            )

        # No vedha (no planet in vedha house)
        return VedhaResult(
            transit_planet=transit_planet,
            transit_house=transit_house,
            has_vedha=False,
            vedha_house=vedha_house,
            vedha_planet=None,
            effect_modifier=1.0,
            description=f"No vedha - vedha house {vedha_house} is empty",
            description_hindi=f"कोई वेध नहीं - वेध भाव {vedha_house} खाली है"
        )

    def check_all_transits(self, transiting_planets: Dict[str, int]) -> Dict[str, VedhaResult]:
        """
        Check vedha for all current transits.

        Args:
            transiting_planets: Dict of planet name to house from Moon

        Returns:
            Dict of planet name to VedhaResult
        """
        results = {}
        for planet, house in transiting_planets.items():
            if planet in ["RAHU", "KETU"]:
                # Rahu/Ketu don't have standard vedha
                results[planet] = VedhaResult(
                    transit_planet=planet,
                    transit_house=house,
                    has_vedha=False,
                    vedha_house=None,
                    vedha_planet=None,
                    effect_modifier=1.0,
                    description=f"{planet} does not have standard vedha rules",
                    description_hindi=f"{planet} के लिए वेध नियम नहीं हैं"
                )
            else:
                results[planet] = self.check_vedha(planet, house)
        return results


def get_vedha_info(planet: str) -> Dict[int, int]:
    """
    Get vedha information for a planet.

    Args:
        planet: Planet name

    Returns:
        Dict mapping favorable house to its vedha point
    """
    return VEDHA_POINTS.get(planet, {})


def is_vedha_exception(planet1: str, planet2: str) -> bool:
    """
    Check if two planets have vedha exception.

    Args:
        planet1: First planet
        planet2: Second planet

    Returns:
        True if they have vedha exception
    """
    return (planet1, planet2) in VEDHA_EXCEPTIONS or (planet2, planet1) in VEDHA_EXCEPTIONS
