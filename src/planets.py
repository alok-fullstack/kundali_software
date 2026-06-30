"""
Planetary calculations using Swiss Ephemeris
Accuracy: < 0.001 arc-second (based on NASA JPL DE431)
"""

import swisseph as swe
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import pytz
import os
import atexit

from .config import (
    Planet, PLANET_NAMES, RASHIS, NAKSHATRAS,
    NAKSHATRA_SPAN, PADA_SPAN, AYANAMSA_LAHIRI
)

# Set ephemeris path if .se1 files exist
_EPHE_PATH = os.path.join(os.path.dirname(__file__), 'ephe')
if os.path.exists(_EPHE_PATH):
    swe.set_ephe_path(_EPHE_PATH)

# Register cleanup on exit to prevent memory leaks
def _cleanup_swisseph():
    """Close Swiss Ephemeris file handles on exit."""
    try:
        swe.close()
    except Exception:
        pass

atexit.register(_cleanup_swisseph)


class PlanetaryCalculator:
    """
    High-accuracy planetary position calculator using Swiss Ephemeris.
    Uses Lahiri Ayanamsa (Indian Government standard) for sidereal calculations.
    """

    def __init__(self, ayanamsa: int = AYANAMSA_LAHIRI):
        """Initialize with specified ayanamsa."""
        self.ayanamsa = ayanamsa
        swe.set_sid_mode(ayanamsa)

    def datetime_to_jd(self, dt: datetime, timezone: str = "Asia/Kolkata") -> float:
        """
        Convert datetime to Julian Day number.
        Julian Day is the standard for astronomical calculations.
        """
        if dt.tzinfo is None:
            tz = pytz.timezone(timezone)
            dt = tz.localize(dt)

        # Convert to UTC
        dt_utc = dt.astimezone(pytz.UTC)

        # Calculate Julian Day
        jd = swe.julday(
            dt_utc.year,
            dt_utc.month,
            dt_utc.day,
            dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0
        )
        return jd

    def get_ayanamsa_value(self, jd: float) -> float:
        """Get the ayanamsa value for a given Julian Day."""
        return swe.get_ayanamsa(jd)

    def get_planet_position(
        self,
        planet: Planet,
        jd: float,
        flags: int = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
    ) -> Dict:
        """
        Calculate sidereal position of a planet.

        Returns:
            Dict with longitude, latitude, distance, speed, rashi, nakshatra, pada
        """
        if planet == Planet.KETU:
            # Ketu is always 180° from Rahu
            rahu_pos = self.get_planet_position(Planet.RAHU, jd, flags)
            longitude = (rahu_pos["longitude"] + 180) % 360
        else:
            result, ret_flag = swe.calc_ut(jd, planet.value, flags)
            longitude = result[0]

        # Calculate Rashi (sign) - ensure within 0-11 range
        rashi_num = int(longitude / 30) % 12
        rashi_degree = longitude % 30

        # Calculate Nakshatra and Pada - with boundary protection
        nakshatra_num = int(longitude / NAKSHATRA_SPAN) % 27
        nakshatra_degree = longitude % NAKSHATRA_SPAN
        pada = min(int(nakshatra_degree / PADA_SPAN) + 1, 4)  # Ensure pada is 1-4

        # Get retrograde status
        if planet == Planet.KETU:
            # Ketu is always retrograde in Vedic astrology
            is_retrograde = True
            speed = 0
        elif planet == Planet.RAHU:
            # Rahu is always retrograde in Vedic astrology (mean node)
            speed = result[3]
            is_retrograde = True
        else:
            speed = result[3]
            is_retrograde = speed < 0

        return {
            "planet": planet.name,
            "planet_hindi": PLANET_NAMES[planet]["hindi"],
            "longitude": round(longitude, 6),
            "rashi_num": rashi_num,
            "rashi": RASHIS[rashi_num]["name"],
            "rashi_english": RASHIS[rashi_num]["english"],
            "rashi_degree": round(rashi_degree, 4),
            "nakshatra_num": nakshatra_num,
            "nakshatra": NAKSHATRAS[nakshatra_num]["name"],
            "nakshatra_lord": NAKSHATRAS[nakshatra_num]["lord"],
            "pada": pada,
            "is_retrograde": is_retrograde,
            "speed": round(speed, 6) if planet != Planet.KETU else None,
            "symbol": PLANET_NAMES[planet]["symbol"],
        }

    def get_all_planets(self, jd: float) -> Dict[str, Dict]:
        """Get positions of all 9 planets (Navagraha)."""
        planets = {}
        for planet in Planet:
            planets[planet.name] = self.get_planet_position(planet, jd)
        return planets

    def get_lagna(
        self,
        jd: float,
        latitude: float,
        longitude: float
    ) -> Dict:
        """
        Calculate Lagna (Ascendant) for a given time and location.
        This is the most critical calculation in a horoscope.
        """
        # Get houses using Placidus system (can be changed)
        cusps, ascmc = swe.houses(jd, latitude, longitude, b'P')

        # Get sidereal ayanamsa
        ayanamsa = swe.get_ayanamsa(jd)

        # Convert to sidereal
        lagna_tropical = ascmc[0]
        lagna_sidereal = (lagna_tropical - ayanamsa) % 360

        # Calculate Rashi
        rashi_num = int(lagna_sidereal / 30)
        rashi_degree = lagna_sidereal % 30

        # Calculate Nakshatra and Pada
        nakshatra_num = int(lagna_sidereal / NAKSHATRA_SPAN)
        nakshatra_degree = lagna_sidereal % NAKSHATRA_SPAN
        pada = int(nakshatra_degree / PADA_SPAN) + 1

        return {
            "longitude": round(lagna_sidereal, 6),
            "rashi_num": rashi_num,
            "rashi": RASHIS[rashi_num]["name"],
            "rashi_english": RASHIS[rashi_num]["english"],
            "rashi_degree": round(rashi_degree, 4),
            "nakshatra_num": nakshatra_num,
            "nakshatra": NAKSHATRAS[nakshatra_num]["name"],
            "nakshatra_lord": NAKSHATRAS[nakshatra_num]["lord"],
            "pada": pada,
        }

    def get_house_cusps(
        self,
        jd: float,
        latitude: float,
        longitude: float,
        house_system: str = 'W'  # W=Whole Sign (Vedic default), P=Placidus, E=Equal
    ) -> List[float]:
        """
        Calculate house cusps (Bhava cusps).
        Returns 12 house cusp positions in sidereal longitude.
        """
        cusps, ascmc = swe.houses(jd, latitude, longitude, house_system.encode())
        ayanamsa = swe.get_ayanamsa(jd)

        # Convert to sidereal
        sidereal_cusps = [(cusp - ayanamsa) % 360 for cusp in cusps[1:13]]
        return [round(c, 6) for c in sidereal_cusps]

    def get_moon_nakshatra(self, jd: float) -> Dict:
        """
        Get Moon's Nakshatra - crucial for Dasha calculations.
        """
        moon_pos = self.get_planet_position(Planet.MOON, jd)
        return {
            "nakshatra": moon_pos["nakshatra"],
            "nakshatra_num": moon_pos["nakshatra_num"],
            "nakshatra_lord": moon_pos["nakshatra_lord"],
            "pada": moon_pos["pada"],
            "longitude": moon_pos["longitude"],
            "degree_in_nakshatra": moon_pos["longitude"] % NAKSHATRA_SPAN,
        }


def format_degree(degrees: float) -> str:
    """
    Format degrees to degree-minute-second notation.
    Example: 23.5 -> 23°30'00"
    """
    d = int(degrees)
    m_float = (degrees - d) * 60
    m = int(m_float)
    s = int((m_float - m) * 60)
    return f"{d}°{m:02d}'{s:02d}\""


def format_rashi_position(rashi: str, degree: float) -> str:
    """
    Format position as Rashi + degree.
    Example: "Mesha 15°30'00"
    """
    return f"{rashi} {format_degree(degree)}"
