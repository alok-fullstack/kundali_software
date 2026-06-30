"""
Main Kundali (Birth Chart) Generator
Combines all calculations into a complete horoscope
"""

from datetime import datetime
from typing import Dict, Optional, List
from dataclasses import dataclass, field
import pytz
from geopy.geocoders import Nominatim

from .planets import PlanetaryCalculator, format_degree, format_rashi_position
from .dasha import VimshottariDasha
from .config import Planet, RASHIS, BHAVA_NAMES, DEFAULT_LOCATION


@dataclass
class BirthData:
    """Birth details for kundali calculation."""
    name: str
    date: datetime
    latitude: float
    longitude: float
    timezone: str = "Asia/Kolkata"
    city: str = ""

    def __post_init__(self):
        if self.date.tzinfo is None:
            tz = pytz.timezone(self.timezone)
            self.date = tz.localize(self.date)


class Kundali:
    """
    Complete Kundali (Birth Chart) Generator.

    Provides:
    - Lagna (Ascendant) calculation
    - All 9 planet positions (Navagraha)
    - 12 house positions (Bhava)
    - Vimshottari Dasha
    - Nakshatra details

    Accuracy: Based on Swiss Ephemeris (NASA JPL DE431)
    - Planetary positions: < 0.001 arc-second (sub-milli-arc-second precision)
    - Lahiri Ayanamsha (Indian Government standard)
    """

    def __init__(self, birth_data: BirthData):
        self.birth_data = birth_data
        self.calculator = PlanetaryCalculator()
        self.dasha_calculator = VimshottariDasha()

        # Calculate Julian Day once
        self.jd = self.calculator.datetime_to_jd(
            birth_data.date,
            birth_data.timezone
        )

        # Core calculations
        self._lagna = None
        self._planets = None
        self._houses = None
        self._dasha = None

    @property
    def lagna(self) -> Dict:
        """Get Lagna (Ascendant) details."""
        if self._lagna is None:
            self._lagna = self.calculator.get_lagna(
                self.jd,
                self.birth_data.latitude,
                self.birth_data.longitude
            )
        return self._lagna

    @property
    def planets(self) -> Dict[str, Dict]:
        """Get all planet positions."""
        if self._planets is None:
            self._planets = self.calculator.get_all_planets(self.jd)
        return self._planets

    @property
    def houses(self) -> List[Dict]:
        """Get all 12 house details."""
        if self._houses is None:
            cusps = self.calculator.get_house_cusps(
                self.jd,
                self.birth_data.latitude,
                self.birth_data.longitude
            )
            self._houses = []
            for i, cusp in enumerate(cusps, 1):
                rashi_num = int(cusp / 30)
                self._houses.append({
                    "house": i,
                    "name": BHAVA_NAMES[i]["name"],
                    "significance": BHAVA_NAMES[i]["significance"],
                    "cusp_longitude": cusp,
                    "rashi": RASHIS[rashi_num]["name"],
                    "rashi_english": RASHIS[rashi_num]["english"],
                })
        return self._houses

    def get_planets_in_houses(self) -> Dict[int, List[str]]:
        """Get which planets are in which houses."""
        planets_in_houses = {i: [] for i in range(1, 13)}

        lagna_rashi = self.lagna["rashi_num"]

        for planet_name, planet_data in self.planets.items():
            planet_rashi = planet_data["rashi_num"]
            # House number relative to Lagna
            house_num = ((planet_rashi - lagna_rashi) % 12) + 1
            planets_in_houses[house_num].append(planet_name)

        return planets_in_houses

    def get_mahadashas(self, years: int = 120) -> List:
        """Get Vimshottari Mahadasha periods."""
        moon_data = self.planets["MOON"]
        return self.dasha_calculator.calculate_mahadashas(
            moon_data["longitude"],
            self.birth_data.date,
            years
        )

    def get_current_dasha(self, target_date: datetime = None) -> Dict:
        """Get running dasha for a specific date."""
        moon_data = self.planets["MOON"]
        return self.dasha_calculator.get_current_dasha(
            moon_data["longitude"],
            self.birth_data.date,
            target_date
        )

    def get_chart_summary(self) -> Dict:
        """Get a complete summary of the kundali."""
        return {
            "birth_details": {
                "name": self.birth_data.name,
                "date": self.birth_data.date.strftime("%Y-%m-%d %H:%M:%S %Z"),
                "city": self.birth_data.city,
                "coordinates": f"{abs(self.birth_data.latitude):.4f}°{'N' if self.birth_data.latitude >= 0 else 'S'}, {abs(self.birth_data.longitude):.4f}°{'E' if self.birth_data.longitude >= 0 else 'W'}",
            },
            "lagna": {
                "rashi": self.lagna["rashi"],
                "rashi_english": self.lagna["rashi_english"],
                "degree": format_degree(self.lagna["rashi_degree"]),
                "nakshatra": self.lagna["nakshatra"],
                "pada": self.lagna["pada"],
            },
            "moon_sign": {
                "rashi": self.planets["MOON"]["rashi"],
                "nakshatra": self.planets["MOON"]["nakshatra"],
                "pada": self.planets["MOON"]["pada"],
            },
            "sun_sign": {
                "rashi": self.planets["SUN"]["rashi"],
            },
            "planets": {
                name: {
                    "rashi": data["rashi"],
                    "degree": format_degree(data["rashi_degree"]),
                    "nakshatra": data["nakshatra"],
                    "retrograde": data["is_retrograde"],
                }
                for name, data in self.planets.items()
            },
            "current_dasha": self.get_current_dasha(),
        }

    def print_kundali(self):
        """Print a formatted kundali report."""
        summary = self.get_chart_summary()

        print("\n" + "=" * 60)
        print(f"          JANAM KUNDALI - {summary['birth_details']['name']}")
        print("=" * 60)

        print(f"\nJanma Tithi: {summary['birth_details']['date']}")
        print(f"Janma Sthan: {summary['birth_details']['city']}")
        print(f"Coordinates: {summary['birth_details']['coordinates']}")

        print("\n" + "-" * 40)
        print("LAGNA (Ascendant)")
        print("-" * 40)
        print(f"  Rashi: {summary['lagna']['rashi']} ({summary['lagna']['rashi_english']})")
        print(f"  Degree: {summary['lagna']['degree']}")
        print(f"  Nakshatra: {summary['lagna']['nakshatra']} Pada {summary['lagna']['pada']}")

        print("\n" + "-" * 40)
        print("CHANDRA (Moon Sign)")
        print("-" * 40)
        print(f"  Rashi: {summary['moon_sign']['rashi']}")
        print(f"  Nakshatra: {summary['moon_sign']['nakshatra']} Pada {summary['moon_sign']['pada']}")

        print("\n" + "-" * 40)
        print("GRAHA STHITI (Planet Positions)")
        print("-" * 40)
        for name, data in summary['planets'].items():
            retro = " (R)" if data['retrograde'] else ""
            print(f"  {name:10} : {data['rashi']:12} {data['degree']:10} - {data['nakshatra']}{retro}")

        print("\n" + "-" * 40)
        print("VARTAMAN DASHA (Current Period)")
        print("-" * 40)
        dasha = summary['current_dasha']
        print(f"  Mahadasha    : {dasha['mahadasha']['planet']}")
        print(f"  Antardasha   : {dasha['antardasha']['planet']}")
        print(f"  Pratyantardasha: {dasha['pratyantardasha']['planet']}")
        print(f"  Full Dasha   : {dasha['full_dasha']}")

        print("\n" + "=" * 60)


def get_coordinates(city: str) -> Dict:
    """
    Get latitude and longitude for a city using geocoding.
    """
    try:
        geolocator = Nominatim(user_agent="kundali_software")
        location = geolocator.geocode(city)
        if location:
            return {
                "city": city,
                "latitude": location.latitude,
                "longitude": location.longitude,
            }
    except Exception as e:
        print(f"Geocoding error: {e}")

    # Return default (Delhi) if geocoding fails
    return DEFAULT_LOCATION


def create_kundali(
    name: str,
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    city: str = "Delhi",
    latitude: float = None,
    longitude: float = None,
    timezone: str = "Asia/Kolkata"
) -> Kundali:
    """
    Convenience function to create a Kundali.

    Args:
        name: Person's name
        year, month, day: Birth date
        hour, minute: Birth time (24-hour format)
        city: Birth city (for geocoding if lat/lon not provided)
        latitude, longitude: Birth place coordinates (optional)
        timezone: Timezone string (default: Asia/Kolkata)

    Returns:
        Kundali object
    """
    # Get coordinates if not provided
    if latitude is None or longitude is None:
        coords = get_coordinates(city)
        latitude = coords["latitude"]
        longitude = coords["longitude"]

    birth_dt = datetime(year, month, day, hour, minute)

    birth_data = BirthData(
        name=name,
        date=birth_dt,
        latitude=latitude,
        longitude=longitude,
        timezone=timezone,
        city=city
    )

    return Kundali(birth_data)
