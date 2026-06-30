"""
Transit (Gochara) Calculator for Vedic Astrology

This module calculates planetary transits and their effects relative to
the natal chart. Gochara analysis is crucial for timing predictions.

Key concepts:
- Gochara: Transit of planets over natal positions
- Ashtakavarga: Transit strength calculation (future enhancement)
- Vedha: Obstruction points that nullify transit effects (future enhancement)
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
import pytz

from .planets import PlanetaryCalculator
from .config import Planet, RASHIS, PLANET_NAMES
from .kundali import Kundali


# Planetary aspects in Vedic astrology (from the planet's position)
# Each planet has specific houses it aspects (counted from its position)
VEDIC_ASPECTS: Dict[str, List[int]] = {
    "SUN": [7],           # 7th aspect (opposition)
    "MOON": [7],          # 7th aspect
    "MARS": [4, 7, 8],    # 4th, 7th, and 8th aspects
    "MERCURY": [7],       # 7th aspect
    "JUPITER": [5, 7, 9], # 5th, 7th, and 9th aspects (trikona aspects)
    "VENUS": [7],         # 7th aspect
    "SATURN": [3, 7, 10], # 3rd, 7th, and 10th aspects
    "RAHU": [5, 7, 9],    # Same as Jupiter (some traditions)
    "KETU": [5, 7, 9],    # Same as Jupiter (some traditions)
}

# Slow-moving planets (significant for transit analysis)
SLOW_PLANETS = ["SATURN", "JUPITER", "RAHU", "KETU"]

# Medium-speed planets
MEDIUM_PLANETS = ["MARS", "SUN"]

# Fast-moving planets (transits less significant individually)
FAST_PLANETS = ["MOON", "MERCURY", "VENUS"]

# Average daily motion in degrees (approximate)
AVERAGE_DAILY_MOTION: Dict[str, float] = {
    "SUN": 0.9856,      # ~1 degree per day
    "MOON": 13.1764,    # ~13 degrees per day
    "MARS": 0.5240,     # Variable, avg ~0.5 degree
    "MERCURY": 1.3833,  # Variable, avg ~1.4 degrees
    "JUPITER": 0.0831,  # ~30 days per degree
    "VENUS": 1.2000,    # Variable, avg ~1.2 degrees
    "SATURN": 0.0335,   # ~30 years per cycle
    "RAHU": 0.0529,     # Always retrograde, ~18 months per sign
    "KETU": 0.0529,     # Always retrograde
}


@dataclass
class TransitEvent:
    """Represents a transit event (planet entering a new sign)."""
    planet: str
    rashi: str
    rashi_english: str
    rashi_num: int
    start_date: datetime
    end_date: Optional[datetime]
    is_retrograde: bool = False


@dataclass
class TransitAspect:
    """Represents a transit aspect to a natal planet."""
    transiting_planet: str
    natal_planet: str
    aspect_type: int  # House number of aspect (7=opposition, etc.)
    orb: float       # Degrees from exact
    is_applying: bool  # True if aspect is applying, False if separating
    transit_rashi: str
    natal_rashi: str


class TransitCalculator:
    """
    Calculator for planetary transits (Gochara) in Vedic Astrology.

    This class provides methods to:
    - Calculate planetary positions for any date
    - Track transit of planets through signs over date ranges
    - Determine house position of transiting planets from natal Moon (Gochara)
    - Calculate aspects between transiting and natal planets

    Usage:
        natal_kundali = create_kundali("Name", 1990, 1, 1, 12, 0, "Delhi")
        transit_calc = TransitCalculator(natal_kundali)

        # Get current transit positions
        positions = transit_calc.get_transit_positions(datetime.now())

        # Get Saturn transit timeline for next year
        saturn_transits = transit_calc.get_planet_transit_timeline(
            "SATURN", datetime.now(), datetime.now() + timedelta(days=365)
        )
    """

    def __init__(self, natal_kundali: Kundali):
        """
        Initialize with a natal chart for comparison.

        Args:
            natal_kundali: The natal Kundali object to compare transits against
        """
        self.natal_kundali = natal_kundali
        self.calculator = PlanetaryCalculator()

        # Cache natal positions for efficiency
        self._natal_planets = natal_kundali.planets
        self._natal_moon_rashi = natal_kundali.planets["MOON"]["rashi_num"]
        self._natal_lagna_rashi = natal_kundali.lagna["rashi_num"]

    @property
    def natal_moon_rashi(self) -> int:
        """Get the natal Moon's rashi number (0-11)."""
        return self._natal_moon_rashi

    @property
    def natal_lagna_rashi(self) -> int:
        """Get the natal Lagna's rashi number (0-11)."""
        return self._natal_lagna_rashi

    def get_transit_positions(
        self,
        date: datetime,
        timezone: str = "Asia/Kolkata"
    ) -> Dict[str, Dict]:
        """
        Get all planet positions for a given date.

        Args:
            date: The datetime for which to calculate positions
            timezone: Timezone string (default: Asia/Kolkata)

        Returns:
            Dict with planet names as keys and position data as values,
            including longitude, rashi, nakshatra, retrograde status, etc.
        """
        jd = self.calculator.datetime_to_jd(date, timezone)
        return self.calculator.get_all_planets(jd)

    def get_single_planet_position(
        self,
        planet: str,
        date: datetime,
        timezone: str = "Asia/Kolkata"
    ) -> Dict:
        """
        Get position of a single planet for a given date.

        Args:
            planet: Planet name (e.g., "SATURN", "JUPITER")
            date: The datetime for which to calculate position
            timezone: Timezone string

        Returns:
            Dict with planet position data
        """
        planet_enum = Planet[planet]
        jd = self.calculator.datetime_to_jd(date, timezone)
        return self.calculator.get_planet_position(planet_enum, jd)

    def get_planet_transit_timeline(
        self,
        planet: str,
        start_date: datetime,
        end_date: datetime,
        timezone: str = "Asia/Kolkata"
    ) -> List[TransitEvent]:
        """
        Get timeline of a planet's transit through signs over a date range.

        This is particularly useful for slow-moving planets like Saturn,
        Jupiter, Rahu, and Ketu to track their ingress into new signs.

        Args:
            planet: Planet name (e.g., "SATURN", "JUPITER")
            start_date: Start of the date range
            end_date: End of the date range
            timezone: Timezone string

        Returns:
            List of TransitEvent objects showing sign changes
        """
        transit_events: List[TransitEvent] = []

        # Determine step size based on planet speed
        if planet in SLOW_PLANETS:
            step_days = 1  # Daily check for slow planets
        elif planet in MEDIUM_PLANETS:
            step_days = 1
        else:
            step_days = 1  # Even for fast planets, daily precision

        current_date = start_date
        prev_rashi = None
        current_event = None

        while current_date <= end_date:
            pos = self.get_single_planet_position(planet, current_date, timezone)
            current_rashi = pos["rashi_num"]
            is_retrograde = pos["is_retrograde"]

            if prev_rashi is None:
                # First entry - start tracking
                current_event = TransitEvent(
                    planet=planet,
                    rashi=pos["rashi"],
                    rashi_english=pos["rashi_english"],
                    rashi_num=current_rashi,
                    start_date=current_date,
                    end_date=None,
                    is_retrograde=is_retrograde
                )
            elif current_rashi != prev_rashi:
                # Sign change detected
                # Close the previous event
                if current_event:
                    current_event.end_date = current_date - timedelta(days=1)
                    transit_events.append(current_event)

                # Start new event
                current_event = TransitEvent(
                    planet=planet,
                    rashi=pos["rashi"],
                    rashi_english=pos["rashi_english"],
                    rashi_num=current_rashi,
                    start_date=current_date,
                    end_date=None,
                    is_retrograde=is_retrograde
                )

            prev_rashi = current_rashi
            current_date += timedelta(days=step_days)

        # Close the last event
        if current_event:
            current_event.end_date = min(end_date, current_date)
            transit_events.append(current_event)

        return transit_events

    def get_transit_house_from_moon(
        self,
        planet: str,
        date: datetime,
        timezone: str = "Asia/Kolkata"
    ) -> Dict:
        """
        Determine which house a transiting planet occupies relative to natal Moon.

        This is the primary Gochara calculation in Vedic astrology. The house
        position from Moon determines the general effect of the transit.

        Traditional Gochara effects (general guidelines):
        - 1st, 2nd, 4th, 5th, 7th, 8th, 9th, 12th from Moon: Generally challenging
        - 3rd, 6th, 10th, 11th from Moon: Generally favorable
        (Note: Actual effects depend on many factors including Ashtakavarga)

        Args:
            planet: Planet name
            date: Transit date
            timezone: Timezone string

        Returns:
            Dict with house number, transit position, and interpretation hints
        """
        transit_pos = self.get_single_planet_position(planet, date, timezone)
        transit_rashi = transit_pos["rashi_num"]

        # Calculate house from Moon (1-indexed)
        house_from_moon = ((transit_rashi - self._natal_moon_rashi) % 12) + 1

        # Traditional Gochara interpretation
        favorable_houses = [3, 6, 10, 11]
        neutral_houses = [1, 5, 9]  # Trikona - can be mixed
        challenging_houses = [2, 4, 7, 8, 12]

        if house_from_moon in favorable_houses:
            general_effect = "favorable"
        elif house_from_moon in challenging_houses:
            general_effect = "challenging"
        else:
            general_effect = "mixed"

        return {
            "planet": planet,
            "transit_rashi": transit_pos["rashi"],
            "transit_rashi_english": transit_pos["rashi_english"],
            "transit_longitude": transit_pos["longitude"],
            "house_from_moon": house_from_moon,
            "natal_moon_rashi": RASHIS[self._natal_moon_rashi]["name"],
            "general_effect": general_effect,
            "is_retrograde": transit_pos["is_retrograde"],
        }

    def get_transit_house_from_lagna(
        self,
        planet: str,
        date: datetime,
        timezone: str = "Asia/Kolkata"
    ) -> Dict:
        """
        Determine which house a transiting planet occupies relative to natal Lagna.

        Args:
            planet: Planet name
            date: Transit date
            timezone: Timezone string

        Returns:
            Dict with house number and transit position
        """
        transit_pos = self.get_single_planet_position(planet, date, timezone)
        transit_rashi = transit_pos["rashi_num"]

        # Calculate house from Lagna (1-indexed)
        house_from_lagna = ((transit_rashi - self._natal_lagna_rashi) % 12) + 1

        return {
            "planet": planet,
            "transit_rashi": transit_pos["rashi"],
            "transit_rashi_english": transit_pos["rashi_english"],
            "house_from_lagna": house_from_lagna,
            "natal_lagna_rashi": RASHIS[self._natal_lagna_rashi]["name"],
            "is_retrograde": transit_pos["is_retrograde"],
        }

    def get_all_transits_from_moon(
        self,
        date: datetime,
        timezone: str = "Asia/Kolkata"
    ) -> List[Dict]:
        """
        Get house positions of all transiting planets from natal Moon.

        Args:
            date: Transit date
            timezone: Timezone string

        Returns:
            List of dicts with each planet's Gochara position
        """
        transits = []
        for planet in Planet:
            transit_info = self.get_transit_house_from_moon(
                planet.name, date, timezone
            )
            transits.append(transit_info)
        return transits

    def get_transit_aspects(
        self,
        date: datetime,
        orb: float = 10.0,
        timezone: str = "Asia/Kolkata"
    ) -> List[TransitAspect]:
        """
        Calculate significant transit aspects to natal planets.

        This method checks all transiting planets for aspects to natal planets
        based on Vedic aspect rules (each planet has specific aspects).

        Args:
            date: Transit date
            orb: Maximum orb in degrees for aspect consideration (default 10)
            timezone: Timezone string

        Returns:
            List of TransitAspect objects representing significant aspects
        """
        transit_positions = self.get_transit_positions(date, timezone)
        aspects: List[TransitAspect] = []

        for trans_planet_name, trans_data in transit_positions.items():
            trans_longitude = trans_data["longitude"]
            trans_rashi_num = trans_data["rashi_num"]

            # Get the aspect houses for this planet
            aspect_houses = VEDIC_ASPECTS.get(trans_planet_name, [7])

            for natal_planet_name, natal_data in self._natal_planets.items():
                natal_longitude = natal_data["longitude"]
                natal_rashi_num = natal_data["rashi_num"]

                # Check each aspect type
                for aspect_house in aspect_houses:
                    # Calculate the rashi that this aspect falls in
                    aspected_rashi = (trans_rashi_num + aspect_house - 1) % 12

                    # Check if natal planet is in the aspected rashi
                    if natal_rashi_num == aspected_rashi:
                        # Calculate the orb (degree difference)
                        # Aspect is from transiting planet to natal planet
                        expected_longitude = (trans_longitude + (aspect_house - 1) * 30) % 360
                        degree_diff = abs(expected_longitude - natal_longitude)
                        if degree_diff > 180:
                            degree_diff = 360 - degree_diff

                        # Check if within orb and in the same sign
                        if degree_diff <= orb:
                            # Determine if aspect is applying or separating
                            # For direct motion planets, applying if trans < natal
                            # For retrograde planets, applying if trans > natal
                            is_retrograde = trans_data["is_retrograde"]
                            trans_degree_in_sign = trans_data["rashi_degree"]
                            natal_degree_in_sign = natal_data["rashi_degree"]

                            if aspect_house == 7:  # Opposition
                                # Direct aspect calculation
                                if is_retrograde:
                                    is_applying = trans_degree_in_sign > natal_degree_in_sign
                                else:
                                    is_applying = trans_degree_in_sign < natal_degree_in_sign
                            else:
                                is_applying = degree_diff < orb / 2  # Simplified

                            aspects.append(TransitAspect(
                                transiting_planet=trans_planet_name,
                                natal_planet=natal_planet_name,
                                aspect_type=aspect_house,
                                orb=round(degree_diff, 2),
                                is_applying=is_applying,
                                transit_rashi=trans_data["rashi"],
                                natal_rashi=natal_data["rashi"]
                            ))

                # Also check for conjunction (same sign)
                if trans_rashi_num == natal_rashi_num:
                    degree_diff = abs(trans_data["rashi_degree"] - natal_data["rashi_degree"])

                    if degree_diff <= orb:
                        is_retrograde = trans_data["is_retrograde"]
                        if is_retrograde:
                            is_applying = trans_data["rashi_degree"] > natal_data["rashi_degree"]
                        else:
                            is_applying = trans_data["rashi_degree"] < natal_data["rashi_degree"]

                        aspects.append(TransitAspect(
                            transiting_planet=trans_planet_name,
                            natal_planet=natal_planet_name,
                            aspect_type=1,  # Conjunction
                            orb=round(degree_diff, 2),
                            is_applying=is_applying,
                            transit_rashi=trans_data["rashi"],
                            natal_rashi=natal_data["rashi"]
                        ))

        # Sort by orb (closest aspects first)
        aspects.sort(key=lambda x: x.orb)

        return aspects

    def get_slow_planet_transits(
        self,
        start_date: datetime,
        end_date: datetime,
        timezone: str = "Asia/Kolkata"
    ) -> Dict[str, List[TransitEvent]]:
        """
        Get transit timelines for all slow-moving planets (Saturn, Jupiter, Rahu, Ketu).

        These are the most significant transits for long-term predictions.

        Args:
            start_date: Start of the date range
            end_date: End of the date range
            timezone: Timezone string

        Returns:
            Dict with planet names as keys and list of TransitEvents as values
        """
        slow_transits = {}
        for planet in SLOW_PLANETS:
            slow_transits[planet] = self.get_planet_transit_timeline(
                planet, start_date, end_date, timezone
            )
        return slow_transits

    def get_sade_sati_status(
        self,
        date: datetime,
        timezone: str = "Asia/Kolkata"
    ) -> Dict:
        """
        Check if the native is under Sade Sati (7.5 years of Saturn).

        Sade Sati occurs when Saturn transits the 12th, 1st, and 2nd houses
        from natal Moon. This is one of the most significant transits.

        Args:
            date: Date to check
            timezone: Timezone string

        Returns:
            Dict with Sade Sati status and phase information
        """
        saturn_pos = self.get_single_planet_position("SATURN", date, timezone)
        saturn_rashi = saturn_pos["rashi_num"]
        moon_rashi = self._natal_moon_rashi

        # Calculate Saturn's position from Moon
        house_from_moon = ((saturn_rashi - moon_rashi) % 12) + 1

        # Sade Sati phases
        is_sade_sati = house_from_moon in [12, 1, 2]

        if house_from_moon == 12:
            phase = "Rising (1st phase)"
            description = "Saturn transiting 12th from Moon - Beginning of Sade Sati"
        elif house_from_moon == 1:
            phase = "Peak (2nd phase)"
            description = "Saturn transiting over natal Moon - Peak of Sade Sati"
        elif house_from_moon == 2:
            phase = "Setting (3rd phase)"
            description = "Saturn transiting 2nd from Moon - Final phase of Sade Sati"
        else:
            phase = None
            description = "Not under Sade Sati"

        # Check for Dhaiya (Small Panoti) - Saturn in 4th or 8th from Moon
        is_dhaiya = house_from_moon in [4, 8]
        dhaiya_type = None
        if house_from_moon == 4:
            dhaiya_type = "Kantak Shani (Saturn in 4th from Moon)"
        elif house_from_moon == 8:
            dhaiya_type = "Ashtama Shani (Saturn in 8th from Moon)"

        return {
            "is_sade_sati": is_sade_sati,
            "sade_sati_phase": phase,
            "description": description,
            "saturn_rashi": saturn_pos["rashi"],
            "saturn_house_from_moon": house_from_moon,
            "is_dhaiya": is_dhaiya,
            "dhaiya_type": dhaiya_type,
            "is_retrograde": saturn_pos["is_retrograde"],
        }

    def get_jupiter_transit_effects(
        self,
        date: datetime,
        timezone: str = "Asia/Kolkata"
    ) -> Dict:
        """
        Analyze Jupiter's transit effects (Guru Gochara).

        Jupiter's transit is significant for growth, wisdom, and fortune.

        Args:
            date: Date to check
            timezone: Timezone string

        Returns:
            Dict with Jupiter transit analysis
        """
        jupiter_pos = self.get_single_planet_position("JUPITER", date, timezone)
        jupiter_rashi = jupiter_pos["rashi_num"]

        house_from_moon = ((jupiter_rashi - self._natal_moon_rashi) % 12) + 1
        house_from_lagna = ((jupiter_rashi - self._natal_lagna_rashi) % 12) + 1

        # Jupiter is favorable in 2, 5, 7, 9, 11 from Moon
        favorable_from_moon = [2, 5, 7, 9, 11]
        is_favorable = house_from_moon in favorable_from_moon

        return {
            "jupiter_rashi": jupiter_pos["rashi"],
            "jupiter_rashi_english": jupiter_pos["rashi_english"],
            "house_from_moon": house_from_moon,
            "house_from_lagna": house_from_lagna,
            "is_favorable": is_favorable,
            "is_retrograde": jupiter_pos["is_retrograde"],
            "general_effect": "favorable" if is_favorable else "challenging",
        }

    def get_transit_summary(
        self,
        date: datetime,
        timezone: str = "Asia/Kolkata"
    ) -> Dict:
        """
        Get a comprehensive summary of all current transits.

        Args:
            date: Date for the summary
            timezone: Timezone string

        Returns:
            Dict with complete transit analysis
        """
        # Get all transit positions
        all_positions = self.get_transit_positions(date, timezone)

        # Get house positions from Moon
        gochara_from_moon = self.get_all_transits_from_moon(date, timezone)

        # Get key transit events
        sade_sati = self.get_sade_sati_status(date, timezone)
        jupiter_effects = self.get_jupiter_transit_effects(date, timezone)

        # Get significant aspects
        aspects = self.get_transit_aspects(date, orb=5.0, timezone=timezone)

        # Filter for significant aspects (slow planets to natal planets)
        significant_aspects = [
            asp for asp in aspects
            if asp.transiting_planet in SLOW_PLANETS
        ]

        return {
            "date": date.strftime("%Y-%m-%d %H:%M:%S"),
            "natal_moon_rashi": RASHIS[self._natal_moon_rashi]["name"],
            "natal_lagna_rashi": RASHIS[self._natal_lagna_rashi]["name"],
            "transit_positions": {
                name: {
                    "rashi": data["rashi"],
                    "degree": round(data["rashi_degree"], 2),
                    "nakshatra": data["nakshatra"],
                    "retrograde": data["is_retrograde"],
                }
                for name, data in all_positions.items()
            },
            "gochara_from_moon": {
                item["planet"]: {
                    "house": item["house_from_moon"],
                    "rashi": item["transit_rashi"],
                    "effect": item["general_effect"],
                }
                for item in gochara_from_moon
            },
            "sade_sati": sade_sati,
            "jupiter_transit": jupiter_effects,
            "significant_aspects": [
                {
                    "transiting": asp.transiting_planet,
                    "natal": asp.natal_planet,
                    "aspect": asp.aspect_type,
                    "orb": asp.orb,
                }
                for asp in significant_aspects[:10]  # Top 10 closest aspects
            ],
        }


def get_transit_calculator(natal_kundali: Kundali) -> TransitCalculator:
    """
    Convenience function to create a TransitCalculator.

    Args:
        natal_kundali: The natal Kundali object

    Returns:
        TransitCalculator instance
    """
    return TransitCalculator(natal_kundali)
