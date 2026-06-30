"""
Shadbala (Six-fold Planetary Strength) Calculator

Based on BPHS Chapter 27 "Shadbala Adhyaya"

The six sources of planetary strength:
1. Sthana Bala - Positional Strength (exaltation, own sign, etc.)
2. Dig Bala - Directional Strength (house position)
3. Kaala Bala - Temporal Strength (day/night, season, etc.)
4. Chesta Bala - Motional Strength (speed, retrograde)
5. Naisargika Bala - Natural Strength (inherent planetary strength)
6. Drik Bala - Aspectual Strength (aspects from benefics/malefics)

Each component gives 0-60 Shashtiamsas (sixtieths of a Rupa)
Total maximum = 360 Shashtiamsas

Author: Kundali Software
Reference: BPHS Chapter 27, Phaladeepika Chapter 7
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import math

from .config import (
    PLANET_DIGNITIES, NAISARGIKA_BALA, DIG_BALA_HOUSES,
    EXALTATION_DEGREES, RASHIS, RASHI_LIST
)


@dataclass
class ShadbalaResult:
    """Result of Shadbala calculation for a planet."""
    planet: str
    sthana_bala: float      # Positional strength (0-60)
    dig_bala: float         # Directional strength (0-60)
    kaala_bala: float       # Temporal strength (0-60)
    chesta_bala: float      # Motional strength (0-60)
    naisargika_bala: float  # Natural strength (0-60)
    drik_bala: float        # Aspectual strength (0-60)
    total: float            # Total (0-360)
    strength_percent: float # Percentage (0-100)
    strength_level: str     # "weak", "average", "strong", "very_strong"


class ShadbalaCalculator:
    """
    Calculate Shadbala (six-fold strength) for all planets in a Kundali.

    Usage:
        calc = ShadbalaCalculator(kundali)
        results = calc.get_all_shadbala()
        # results["SUN"].total gives Sun's total Shadbala
    """

    # Minimum required Shadbala for each planet (in Rupas = Shashtiamsas / 60)
    MINIMUM_REQUIRED = {
        "SUN": 390,      # 6.5 Rupas
        "MOON": 360,     # 6.0 Rupas
        "MARS": 300,     # 5.0 Rupas
        "MERCURY": 420,  # 7.0 Rupas
        "JUPITER": 390,  # 6.5 Rupas
        "VENUS": 330,    # 5.5 Rupas
        "SATURN": 300,   # 5.0 Rupas
    }

    def __init__(self, kundali=None, planets_data: Dict = None, houses_data: Dict = None):
        """
        Initialize with either a Kundali object or raw planetary data.

        Args:
            kundali: Kundali object with planets and houses
            planets_data: Dict of planet positions {name: {longitude, rashi, speed, ...}}
            houses_data: Dict of house cusps {1: degree, 2: degree, ...}
        """
        if kundali is not None:
            self.planets = kundali.planets
            self.houses = getattr(kundali, 'houses', {})
            self.lagna_rashi = kundali.lagna.get('rashi', 'Mesha')
            # birth_data is a dataclass, access .date.hour
            birth_data = getattr(kundali, 'birth_data', None)
            if birth_data and hasattr(birth_data, 'date'):
                self.birth_hour = birth_data.date.hour
            else:
                self.birth_hour = 12
        else:
            self.planets = planets_data or {}
            self.houses = houses_data or {}
            self.lagna_rashi = 'Mesha'
            self.birth_hour = 12

    def calculate_sthana_bala(self, planet: str) -> float:
        """
        Calculate Sthana Bala (Positional Strength).

        Components:
        - Uchcha Bala: Strength from exaltation (max at exact exaltation degree)
        - Saptavargaja Bala: Strength from 7 divisional charts (simplified)
        - Ojayugma Bala: Odd/even rashi and navamsa
        - Kendradi Bala: Angular position from Lagna
        - Drekkana Bala: Decanate position

        Returns: 0-60 Shashtiamsas
        """
        if planet not in self.planets or planet in ["RAHU", "KETU"]:
            return 30.0  # Default for nodes

        planet_data = self.planets[planet]
        longitude = planet_data.get('longitude', 0)
        rashi = planet_data.get('rashi', 'Mesha')

        total_sthana = 0.0

        # 1. UCHCHA BALA (Exaltation Strength) - Max 60 at exaltation, 0 at debilitation
        if planet in EXALTATION_DEGREES:
            exalt_deg = EXALTATION_DEGREES[planet]
            distance = abs(longitude - exalt_deg)
            if distance > 180:
                distance = 360 - distance
            # Max 60 at exaltation, 0 at 180° away (debilitation)
            uchcha_bala = 60 * (1 - distance / 180)
            total_sthana += uchcha_bala * 0.4  # 40% weight

        # 2. SAPTAVARGAJA BALA (Simplified: Own/Exalted/Debilitated)
        dignity = PLANET_DIGNITIES.get(planet, {})
        if rashi == dignity.get('exalted'):
            sapta_bala = 60
        elif rashi in dignity.get('own', []):
            sapta_bala = 45
        elif rashi == dignity.get('mooltrikona'):
            sapta_bala = 50
        elif rashi == dignity.get('debilitated'):
            sapta_bala = 5
        else:
            sapta_bala = 25  # Neutral
        total_sthana += sapta_bala * 0.3  # 30% weight

        # 3. KENDRADI BALA (Angular Strength)
        # Planets in Kendra (1,4,7,10) = 60, Panapara (2,5,8,11) = 30, Apoklima (3,6,9,12) = 15
        house_num = self._get_house_from_lagna(rashi)
        if house_num in [1, 4, 7, 10]:  # Kendra
            kendradi = 60
        elif house_num in [2, 5, 8, 11]:  # Panapara
            kendradi = 30
        else:  # Apoklima
            kendradi = 15
        total_sthana += kendradi * 0.3  # 30% weight

        return min(60.0, total_sthana)

    def calculate_dig_bala(self, planet: str) -> float:
        """
        Calculate Dig Bala (Directional Strength).

        Each planet has a direction where it's strongest:
        - Sun/Mars: 10th house (South)
        - Moon/Venus: 4th house (North)
        - Mercury/Jupiter: 1st house (East)
        - Saturn: 7th house (West)

        Returns: 0-60 Shashtiamsas
        """
        if planet not in self.planets or planet in ["RAHU", "KETU"]:
            return 30.0

        optimal_house = DIG_BALA_HOUSES.get(planet, 1)
        rashi = self.planets[planet].get('rashi', 'Mesha')
        current_house = self._get_house_from_lagna(rashi)

        # Distance from optimal house (0 = same, 6 = opposite)
        distance = abs(current_house - optimal_house)
        if distance > 6:
            distance = 12 - distance

        # Max 60 at optimal house, 0 at opposite
        dig_bala = 60 * (1 - distance / 6)

        return max(0.0, dig_bala)

    def calculate_kaala_bala(self, planet: str) -> float:
        """
        Calculate Kaala Bala (Temporal Strength).

        Components:
        - Natonnata Bala: Day/Night strength
        - Paksha Bala: Waxing/Waning Moon strength
        - Hora Bala: Planetary hour strength
        - Ayana Bala: Solstice strength

        Returns: 0-60 Shashtiamsas (simplified calculation)
        """
        if planet not in self.planets or planet in ["RAHU", "KETU"]:
            return 30.0

        kaala_bala = 30.0  # Base value

        # Day/Night strength (Diurnal planets stronger by day, nocturnal by night)
        is_daytime = 6 <= self.birth_hour < 18

        diurnal_planets = ["SUN", "JUPITER", "SATURN"]
        nocturnal_planets = ["MOON", "MARS", "VENUS"]

        if planet in diurnal_planets:
            kaala_bala += 15 if is_daytime else -5
        elif planet in nocturnal_planets:
            kaala_bala += 15 if not is_daytime else -5
        else:  # Mercury - neutral
            kaala_bala += 5

        # Paksha Bala for Moon (waxing = stronger)
        if planet == "MOON":
            moon_long = self.planets.get("MOON", {}).get("longitude", 0)
            sun_long = self.planets.get("SUN", {}).get("longitude", 0)
            tithi_angle = (moon_long - sun_long) % 360

            # Waxing (0-180°) = stronger, Waning (180-360°) = weaker
            if tithi_angle <= 180:
                kaala_bala += 15  # Shukla Paksha bonus
            else:
                kaala_bala -= 10  # Krishna Paksha penalty

        return max(0.0, min(60.0, kaala_bala))

    def calculate_chesta_bala(self, planet: str) -> float:
        """
        Calculate Chesta Bala (Motional Strength).

        Based on planetary speed:
        - Retrograde = reduced strength
        - Stationary = very reduced strength
        - Direct motion with good speed = full strength

        Returns: 0-60 Shashtiamsas
        """
        if planet not in self.planets:
            return 30.0

        # Sun and Moon don't have Chesta Bala (never retrograde)
        if planet in ["SUN", "MOON", "RAHU", "KETU"]:
            return 30.0  # Neutral value

        planet_data = self.planets[planet]
        is_retrograde = planet_data.get('is_retrograde', False)
        speed = planet_data.get('speed', 1.0)

        if is_retrograde:
            # Retrograde planets get reduced Chesta Bala
            chesta_bala = 15.0  # 25% of max
        elif abs(speed) < 0.1:
            # Stationary (very slow) planets
            chesta_bala = 10.0
        else:
            # Direct motion - strength based on speed
            # Normalize speed (average daily motion varies by planet)
            avg_speeds = {
                "MARS": 0.5, "MERCURY": 1.0, "JUPITER": 0.08,
                "VENUS": 1.0, "SATURN": 0.03
            }
            avg = avg_speeds.get(planet, 0.5)
            speed_ratio = min(abs(speed) / avg, 2.0)  # Cap at 2x average
            chesta_bala = 30 + (30 * speed_ratio / 2)  # 30-60 range

        return max(0.0, min(60.0, chesta_bala))

    def calculate_naisargika_bala(self, planet: str) -> float:
        """
        Calculate Naisargika Bala (Natural Strength).

        This is fixed for each planet based on luminosity:
        Sun=60, Moon=51.43, Venus=42.85, Jupiter=34.28,
        Mercury=25.71, Mars=17.14, Saturn=8.57

        Returns: 0-60 Shashtiamsas
        """
        return NAISARGIKA_BALA.get(planet, 30.0)

    def calculate_drik_bala(self, planet: str) -> float:
        """
        Calculate Drik Bala (Aspectual Strength).

        Based on aspects received from benefics and malefics:
        - Benefic aspects (Jupiter, Venus, Mercury, waxing Moon) add strength
        - Malefic aspects (Saturn, Mars, Rahu, Ketu) reduce strength

        Returns: 0-60 Shashtiamsas (simplified)
        """
        if planet not in self.planets:
            return 30.0

        drik_bala = 30.0  # Base neutral value
        planet_long = self.planets[planet].get('longitude', 0)

        benefics = ["JUPITER", "VENUS"]
        malefics = ["SATURN", "MARS"]

        for other_planet, other_data in self.planets.items():
            if other_planet == planet or other_planet in ["RAHU", "KETU"]:
                continue

            other_long = other_data.get('longitude', 0)
            aspect_angle = abs(planet_long - other_long)
            if aspect_angle > 180:
                aspect_angle = 360 - aspect_angle

            # Check for major aspects (conjunction, opposition, trine, square)
            is_aspecting = False
            aspect_strength = 0

            if aspect_angle < 10:  # Conjunction (0°)
                is_aspecting = True
                aspect_strength = 1.0
            elif 170 < aspect_angle < 190:  # Opposition (180°)
                is_aspecting = True
                aspect_strength = 1.0
            elif 115 < aspect_angle < 125:  # Trine (120°)
                is_aspecting = True
                aspect_strength = 0.75
            elif 85 < aspect_angle < 95:  # Square (90°)
                is_aspecting = True
                aspect_strength = 0.5

            if is_aspecting:
                if other_planet in benefics:
                    drik_bala += 10 * aspect_strength
                elif other_planet in malefics:
                    drik_bala -= 10 * aspect_strength

        return max(0.0, min(60.0, drik_bala))

    def _get_house_from_lagna(self, rashi: str) -> int:
        """Get house number (1-12) for a rashi from lagna."""
        try:
            lagna_index = RASHI_LIST.index(self.lagna_rashi)
            rashi_index = RASHI_LIST.index(rashi)
            house = ((rashi_index - lagna_index) % 12) + 1
            return house
        except (ValueError, IndexError):
            return 1

    def get_strength_level(self, total: float, planet: str) -> str:
        """Classify strength level based on total Shadbala."""
        min_required = self.MINIMUM_REQUIRED.get(planet, 300)

        ratio = total / min_required

        if ratio >= 1.5:
            return "very_strong"
        elif ratio >= 1.0:
            return "strong"
        elif ratio >= 0.7:
            return "average"
        else:
            return "weak"

    def calculate_shadbala(self, planet: str) -> ShadbalaResult:
        """Calculate complete Shadbala for a single planet."""
        sthana = self.calculate_sthana_bala(planet)
        dig = self.calculate_dig_bala(planet)
        kaala = self.calculate_kaala_bala(planet)
        chesta = self.calculate_chesta_bala(planet)
        naisargika = self.calculate_naisargika_bala(planet)
        drik = self.calculate_drik_bala(planet)

        total = sthana + dig + kaala + chesta + naisargika + drik
        strength_percent = (total / 360) * 100
        strength_level = self.get_strength_level(total, planet)

        return ShadbalaResult(
            planet=planet,
            sthana_bala=round(sthana, 2),
            dig_bala=round(dig, 2),
            kaala_bala=round(kaala, 2),
            chesta_bala=round(chesta, 2),
            naisargika_bala=round(naisargika, 2),
            drik_bala=round(drik, 2),
            total=round(total, 2),
            strength_percent=round(strength_percent, 1),
            strength_level=strength_level
        )

    def get_all_shadbala(self) -> Dict[str, ShadbalaResult]:
        """Calculate Shadbala for all planets."""
        results = {}
        for planet in ["SUN", "MOON", "MARS", "MERCURY", "JUPITER", "VENUS", "SATURN"]:
            if planet in self.planets:
                results[planet] = self.calculate_shadbala(planet)
        return results

    def get_shadbala_modifier(self, planet: str) -> float:
        """
        Get a modifier (-0.3 to +0.3) based on Shadbala strength.
        Used to modify transit intensity in Rashifal.

        Returns:
            Modifier to add to transit intensity
        """
        if planet in ["RAHU", "KETU"]:
            return 0.0

        result = self.calculate_shadbala(planet)

        # Map strength level to modifier
        modifiers = {
            "very_strong": 0.25,
            "strong": 0.10,
            "average": 0.0,
            "weak": -0.15,
        }

        return modifiers.get(result.strength_level, 0.0)


# =============================================================================
# HELPER FUNCTIONS FOR RASHIFAL INTEGRATION
# =============================================================================

def get_shadbala_for_transit(kundali, transit_positions: Dict) -> Dict[str, float]:
    """
    Get Shadbala modifiers for transit planets.

    Args:
        kundali: Birth chart Kundali object
        transit_positions: Current planetary positions

    Returns:
        Dict of planet -> modifier (-0.3 to +0.3)
    """
    if kundali is None:
        return {}

    try:
        calc = ShadbalaCalculator(kundali)
        modifiers = {}

        for planet in transit_positions:
            if planet not in ["RAHU", "KETU"]:
                modifiers[planet] = calc.get_shadbala_modifier(planet)

        return modifiers
    except Exception:
        return {}
