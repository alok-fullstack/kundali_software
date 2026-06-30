"""
Divisional Charts (Varga Charts) Calculator
Based on Brihat Parashara Hora Shastra (BPHS)

This module implements all 16 primary divisional charts used in Vedic astrology.
Each chart divides the zodiac differently to reveal specific life areas.

References:
- Brihat Parashara Hora Shastra, Chapters 6-7 (Varga Division)
- Brihat Parashara Hora Shastra, Chapter 44 (Vimshopaka Bala)

Author: Kundali Software
Accuracy: Based on exact BPHS formulas
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

from .config import RASHIS, Planet


class VargaChart(Enum):
    """Enumeration of all 16 divisional charts."""
    D1_RASHI = 1         # Main birth chart
    D2_HORA = 2          # Wealth
    D3_DREKKANA = 3      # Siblings, courage
    D4_CHATURTHAMSA = 4  # Fortune, property
    D7_SAPTAMSA = 7      # Children, progeny
    D9_NAVAMSA = 9       # Marriage, spouse, dharma - MOST IMPORTANT
    D10_DASAMSA = 10     # Career, profession
    D12_DWADASAMSA = 12  # Parents
    D16_SHODASAMSA = 16  # Vehicles, comforts
    D20_VIMSAMSA = 20    # Spiritual progress
    D24_CHATURVIMSAMSA = 24  # Education, learning
    D27_BHAMSA = 27      # Strength, weakness (Nakshatra-based)
    D30_TRIMSAMSA = 30   # Evils, misfortune
    D40_KHAVEDAMSA = 40  # Auspicious/inauspicious effects
    D45_AKSHAVEDAMSA = 45  # General indications
    D60_SHASHTIAMSA = 60   # Past life karma


# Sign element classification (for Navamsa calculation)
FIRE_SIGNS = [0, 4, 8]      # Aries (0), Leo (4), Sagittarius (8)
EARTH_SIGNS = [1, 5, 9]     # Taurus (1), Virgo (5), Capricorn (9)
AIR_SIGNS = [2, 6, 10]      # Gemini (2), Libra (6), Aquarius (10)
WATER_SIGNS = [3, 7, 11]    # Cancer (3), Scorpio (7), Pisces (11)

# Navamsa starting signs based on element (BPHS Chapter 6, Verse 9-10)
NAVAMSA_START = {
    'Fire': 0,    # Aries
    'Earth': 9,   # Capricorn
    'Air': 6,     # Libra
    'Water': 3,   # Cancer
}


@dataclass
class DivisionalPosition:
    """Position of a planet in a divisional chart."""
    planet: str
    original_longitude: float
    original_rashi_num: int
    original_rashi: str
    original_degree: float

    varga_rashi_num: int
    varga_rashi: str
    varga_rashi_english: str
    varga_degree: float  # Degree within the varga division
    division_number: int  # Which division (1-N) within the sign

    # Dignity status in divisional chart
    is_own_sign: bool = False
    is_exalted: bool = False
    is_debilitated: bool = False
    is_mooltrikona: bool = False


@dataclass
class DivisionalChart:
    """Complete divisional chart data."""
    varga_type: VargaChart
    varga_name: str
    varga_description: str
    division_count: int

    # Lagna and planets in this varga
    lagna: DivisionalPosition
    planets: Dict[str, DivisionalPosition]

    # Planets in houses (relative to varga lagna)
    planets_in_houses: Dict[int, List[str]] = field(default_factory=dict)


# D-60 Shashtiamsa names and deities (BPHS Chapter 6, Verses 34-37)
# Each degree of a sign has 2 shashtiamsas (60 per sign = 2 per degree)
SHASHTIAMSA_NAMES = [
    {"name": "Ghora", "deity": "Yama", "nature": "malefic"},
    {"name": "Rakshasa", "deity": "Rakshasa", "nature": "malefic"},
    {"name": "Deva", "deity": "Deva", "nature": "benefic"},
    {"name": "Kubera", "deity": "Kubera", "nature": "benefic"},
    {"name": "Yaksha", "deity": "Yaksha", "nature": "neutral"},
    {"name": "Kinnara", "deity": "Kinnara", "nature": "benefic"},
    {"name": "Bhrashta", "deity": "Agni", "nature": "malefic"},
    {"name": "Kulaghna", "deity": "Surya", "nature": "malefic"},
    {"name": "Garala", "deity": "Chandra", "nature": "malefic"},
    {"name": "Vahni", "deity": "Agni", "nature": "malefic"},
    {"name": "Maya", "deity": "Maya", "nature": "neutral"},
    {"name": "Purishaka", "deity": "Purusha", "nature": "neutral"},
    {"name": "Apampathi", "deity": "Varuna", "nature": "benefic"},
    {"name": "Marut", "deity": "Vayu", "nature": "benefic"},
    {"name": "Kaala", "deity": "Kaala", "nature": "malefic"},
    {"name": "Sarpa", "deity": "Sarpa", "nature": "malefic"},
    {"name": "Amrita", "deity": "Chandra", "nature": "benefic"},
    {"name": "Indu", "deity": "Chandra", "nature": "benefic"},
    {"name": "Mridu", "deity": "Chandra", "nature": "benefic"},
    {"name": "Komala", "deity": "Shukra", "nature": "benefic"},
    {"name": "Heramba", "deity": "Ganesha", "nature": "benefic"},
    {"name": "Brahma", "deity": "Brahma", "nature": "benefic"},
    {"name": "Vishnu", "deity": "Vishnu", "nature": "benefic"},
    {"name": "Maheswara", "deity": "Shiva", "nature": "benefic"},
    {"name": "Deva", "deity": "Indra", "nature": "benefic"},
    {"name": "Ardra", "deity": "Rudra", "nature": "malefic"},
    {"name": "Kalinasa", "deity": "Surya", "nature": "benefic"},
    {"name": "Kshitisa", "deity": "Bhumi", "nature": "benefic"},
    {"name": "Kamalakara", "deity": "Lakshmi", "nature": "benefic"},
    {"name": "Gulika", "deity": "Gulika", "nature": "malefic"},
    {"name": "Mrithyu", "deity": "Yama", "nature": "malefic"},
    {"name": "Kaala", "deity": "Kaala", "nature": "malefic"},
    {"name": "Davagni", "deity": "Agni", "nature": "malefic"},
    {"name": "Ghora", "deity": "Yama", "nature": "malefic"},
    {"name": "Yama", "deity": "Yama", "nature": "malefic"},
    {"name": "Kantaka", "deity": "Shani", "nature": "malefic"},
    {"name": "Sudha", "deity": "Amrita", "nature": "benefic"},
    {"name": "Amrita", "deity": "Chandra", "nature": "benefic"},
    {"name": "Purnachandra", "deity": "Chandra", "nature": "benefic"},
    {"name": "Vishadagdha", "deity": "Agni", "nature": "malefic"},
    {"name": "Kulanasa", "deity": "Agni", "nature": "malefic"},
    {"name": "Vamshakshaya", "deity": "Ketu", "nature": "malefic"},
    {"name": "Utpata", "deity": "Rahu", "nature": "malefic"},
    {"name": "Kaala", "deity": "Kaala", "nature": "malefic"},
    {"name": "Saumya", "deity": "Chandra", "nature": "benefic"},
    {"name": "Komala", "deity": "Shukra", "nature": "benefic"},
    {"name": "Shitala", "deity": "Chandra", "nature": "benefic"},
    {"name": "Karala Damshtra", "deity": "Rudra", "nature": "malefic"},
    {"name": "Chandra Mukhi", "deity": "Chandra", "nature": "benefic"},
    {"name": "Praveena", "deity": "Brihaspati", "nature": "benefic"},
    {"name": "Kaala Pavaka", "deity": "Agni", "nature": "malefic"},
    {"name": "Dandayudha", "deity": "Yama", "nature": "malefic"},
    {"name": "Nirmala", "deity": "Vishnu", "nature": "benefic"},
    {"name": "Saumya", "deity": "Lakshmi", "nature": "benefic"},
    {"name": "Kroora", "deity": "Rudra", "nature": "malefic"},
    {"name": "Atishitala", "deity": "Chandra", "nature": "benefic"},
    {"name": "Amrita", "deity": "Amrita", "nature": "benefic"},
    {"name": "Payodhi", "deity": "Varuna", "nature": "benefic"},
    {"name": "Brahmana", "deity": "Brahma", "nature": "benefic"},
    {"name": "Chandra Rekha", "deity": "Chandra", "nature": "benefic"},
]


class DivisionalChartCalculator:
    """
    Calculator for all 16 primary divisional charts (Varga).

    Based on Brihat Parashara Hora Shastra (BPHS), Chapters 6-7.
    """

    def __init__(self):
        """Initialize the calculator with BPHS rules."""
        # Planet dignity data for varga charts
        self.planet_own_signs = {
            "SUN": [4],           # Leo
            "MOON": [3],          # Cancer
            "MARS": [0, 7],       # Aries, Scorpio
            "MERCURY": [2, 5],    # Gemini, Virgo
            "JUPITER": [8, 11],   # Sagittarius, Pisces
            "VENUS": [1, 6],      # Taurus, Libra
            "SATURN": [9, 10],    # Capricorn, Aquarius
            "RAHU": [10],         # Aquarius (Mool Trikona)
            "KETU": [7],          # Scorpio
        }

        self.planet_exaltation = {
            "SUN": 0,      # Aries
            "MOON": 1,     # Taurus
            "MARS": 9,     # Capricorn
            "MERCURY": 5,  # Virgo
            "JUPITER": 3,  # Cancer
            "VENUS": 11,   # Pisces
            "SATURN": 6,   # Libra
            "RAHU": 1,     # Taurus
            "KETU": 7,     # Scorpio
        }

        self.planet_debilitation = {
            "SUN": 6,      # Libra
            "MOON": 7,     # Scorpio
            "MARS": 3,     # Cancer
            "MERCURY": 11, # Pisces
            "JUPITER": 9,  # Capricorn
            "VENUS": 5,    # Virgo
            "SATURN": 0,   # Aries
            "RAHU": 7,     # Scorpio
            "KETU": 1,     # Taurus
        }

    def _get_sign_element(self, rashi_num: int) -> str:
        """Get the element of a zodiac sign."""
        if rashi_num in FIRE_SIGNS:
            return 'Fire'
        elif rashi_num in EARTH_SIGNS:
            return 'Earth'
        elif rashi_num in AIR_SIGNS:
            return 'Air'
        else:
            return 'Water'

    def _is_odd_sign(self, rashi_num: int) -> bool:
        """Check if sign is odd (1, 3, 5... Aries, Gemini, Leo...)."""
        return rashi_num % 2 == 0  # 0-indexed: 0=Aries(odd), 1=Taurus(even)

    def _get_dignity_status(self, planet: str, rashi_num: int) -> Tuple[bool, bool, bool, bool]:
        """
        Get dignity status of planet in a sign.
        Returns: (is_own, is_exalted, is_debilitated, is_mooltrikona)
        """
        is_own = rashi_num in self.planet_own_signs.get(planet, [])
        is_exalted = self.planet_exaltation.get(planet) == rashi_num
        is_debilitated = self.planet_debilitation.get(planet) == rashi_num
        is_mooltrikona = False  # Mooltrikona calculation more complex, simplified here

        return is_own, is_exalted, is_debilitated, is_mooltrikona

    def calculate_d1_rashi(self, longitude: float, planet: str = "") -> DivisionalPosition:
        """
        D-1 Rashi Chart (Birth Chart) - BPHS Chapter 6, Verse 5

        This is the main birth chart where each sign is 30 degrees.
        """
        rashi_num = int(longitude / 30) % 12
        degree_in_sign = longitude % 30

        is_own, is_exalted, is_debilitated, is_mooltrikona = self._get_dignity_status(planet, rashi_num)

        return DivisionalPosition(
            planet=planet,
            original_longitude=longitude,
            original_rashi_num=rashi_num,
            original_rashi=RASHIS[rashi_num]["name"],
            original_degree=degree_in_sign,
            varga_rashi_num=rashi_num,
            varga_rashi=RASHIS[rashi_num]["name"],
            varga_rashi_english=RASHIS[rashi_num]["english"],
            varga_degree=degree_in_sign,
            division_number=1,
            is_own_sign=is_own,
            is_exalted=is_exalted,
            is_debilitated=is_debilitated,
            is_mooltrikona=is_mooltrikona,
        )

    def calculate_d2_hora(self, longitude: float, planet: str = "") -> DivisionalPosition:
        """
        D-2 Hora Chart (Wealth) - BPHS Chapter 6, Verse 6

        Each sign is divided into 2 parts of 15 degrees each.

        Rules:
        - First 15 degrees of ODD signs = Sun (Leo)
        - Last 15 degrees of ODD signs = Moon (Cancer)
        - First 15 degrees of EVEN signs = Moon (Cancer)
        - Last 15 degrees of EVEN signs = Sun (Leo)
        """
        rashi_num = int(longitude / 30) % 12
        degree_in_sign = longitude % 30
        is_odd = self._is_odd_sign(rashi_num)

        is_first_half = degree_in_sign < 15
        division = 1 if is_first_half else 2

        # Determine Hora lord
        if is_odd:
            # Odd signs: first half = Sun (Leo), second half = Moon (Cancer)
            hora_rashi = 4 if is_first_half else 3  # Leo or Cancer
        else:
            # Even signs: first half = Moon (Cancer), second half = Sun (Leo)
            hora_rashi = 3 if is_first_half else 4  # Cancer or Leo

        hora_degree = degree_in_sign % 15

        is_own, is_exalted, is_debilitated, is_mooltrikona = self._get_dignity_status(planet, hora_rashi)

        return DivisionalPosition(
            planet=planet,
            original_longitude=longitude,
            original_rashi_num=rashi_num,
            original_rashi=RASHIS[rashi_num]["name"],
            original_degree=degree_in_sign,
            varga_rashi_num=hora_rashi,
            varga_rashi=RASHIS[hora_rashi]["name"],
            varga_rashi_english=RASHIS[hora_rashi]["english"],
            varga_degree=hora_degree,
            division_number=division,
            is_own_sign=is_own,
            is_exalted=is_exalted,
            is_debilitated=is_debilitated,
            is_mooltrikona=is_mooltrikona,
        )

    def calculate_d3_drekkana(self, longitude: float, planet: str = "") -> DivisionalPosition:
        """
        D-3 Drekkana Chart (Siblings, Courage) - BPHS Chapter 6, Verse 7

        Each sign is divided into 3 parts of 10 degrees each.

        Rules:
        - 1st drekkana (0-10): Same sign
        - 2nd drekkana (10-20): 5th sign from it
        - 3rd drekkana (20-30): 9th sign from it
        """
        rashi_num = int(longitude / 30) % 12
        degree_in_sign = longitude % 30

        # Determine which drekkana (1, 2, or 3)
        division = int(degree_in_sign / 10) + 1
        division = min(division, 3)  # Ensure max is 3

        # Calculate drekkana sign
        if division == 1:
            drekkana_rashi = rashi_num
        elif division == 2:
            drekkana_rashi = (rashi_num + 4) % 12  # 5th from sign
        else:
            drekkana_rashi = (rashi_num + 8) % 12  # 9th from sign

        drekkana_degree = degree_in_sign % 10

        is_own, is_exalted, is_debilitated, is_mooltrikona = self._get_dignity_status(planet, drekkana_rashi)

        return DivisionalPosition(
            planet=planet,
            original_longitude=longitude,
            original_rashi_num=rashi_num,
            original_rashi=RASHIS[rashi_num]["name"],
            original_degree=degree_in_sign,
            varga_rashi_num=drekkana_rashi,
            varga_rashi=RASHIS[drekkana_rashi]["name"],
            varga_rashi_english=RASHIS[drekkana_rashi]["english"],
            varga_degree=drekkana_degree,
            division_number=division,
            is_own_sign=is_own,
            is_exalted=is_exalted,
            is_debilitated=is_debilitated,
            is_mooltrikona=is_mooltrikona,
        )

    def calculate_d4_chaturthamsa(self, longitude: float, planet: str = "") -> DivisionalPosition:
        """
        D-4 Chaturthamsa Chart (Property, Fortune) - BPHS Chapter 6, Verse 8

        Each sign is divided into 4 parts of 7.5 degrees each.

        Rules:
        - Odd signs: Start from same sign, then 4th, 7th, 10th
        - Even signs: Start from 4th sign, then 7th, 10th, 1st
        """
        rashi_num = int(longitude / 30) % 12
        degree_in_sign = longitude % 30
        is_odd = self._is_odd_sign(rashi_num)

        # Determine which division (1-4)
        division = int(degree_in_sign / 7.5) + 1
        division = min(division, 4)

        # Calculate chaturthamsa sign
        if is_odd:
            # Odd signs: start from same sign
            chaturthamsa_rashi = (rashi_num + (division - 1) * 3) % 12
        else:
            # Even signs: start from 4th sign
            chaturthamsa_rashi = (rashi_num + 3 + (division - 1) * 3) % 12

        chaturthamsa_degree = degree_in_sign % 7.5

        is_own, is_exalted, is_debilitated, is_mooltrikona = self._get_dignity_status(planet, chaturthamsa_rashi)

        return DivisionalPosition(
            planet=planet,
            original_longitude=longitude,
            original_rashi_num=rashi_num,
            original_rashi=RASHIS[rashi_num]["name"],
            original_degree=degree_in_sign,
            varga_rashi_num=chaturthamsa_rashi,
            varga_rashi=RASHIS[chaturthamsa_rashi]["name"],
            varga_rashi_english=RASHIS[chaturthamsa_rashi]["english"],
            varga_degree=chaturthamsa_degree,
            division_number=division,
            is_own_sign=is_own,
            is_exalted=is_exalted,
            is_debilitated=is_debilitated,
            is_mooltrikona=is_mooltrikona,
        )

    def calculate_d7_saptamsa(self, longitude: float, planet: str = "") -> DivisionalPosition:
        """
        D-7 Saptamsa Chart (Children, Progeny) - BPHS Chapter 6, Verse 9

        Each sign is divided into 7 parts of 4.285714... degrees each (30/7).

        Rules:
        - Odd signs: Start from same sign, count forward
        - Even signs: Start from 7th sign from it, count forward
        """
        rashi_num = int(longitude / 30) % 12
        degree_in_sign = longitude % 30
        is_odd = self._is_odd_sign(rashi_num)

        # Each division is 30/7 = 4.285714... degrees
        division_span = 30.0 / 7.0
        division = int(degree_in_sign / division_span) + 1
        division = min(division, 7)

        # Calculate saptamsa sign
        if is_odd:
            # Odd signs: start from same sign
            saptamsa_rashi = (rashi_num + division - 1) % 12
        else:
            # Even signs: start from 7th sign
            saptamsa_rashi = (rashi_num + 6 + division - 1) % 12

        saptamsa_degree = degree_in_sign % division_span

        is_own, is_exalted, is_debilitated, is_mooltrikona = self._get_dignity_status(planet, saptamsa_rashi)

        return DivisionalPosition(
            planet=planet,
            original_longitude=longitude,
            original_rashi_num=rashi_num,
            original_rashi=RASHIS[rashi_num]["name"],
            original_degree=degree_in_sign,
            varga_rashi_num=saptamsa_rashi,
            varga_rashi=RASHIS[saptamsa_rashi]["name"],
            varga_rashi_english=RASHIS[saptamsa_rashi]["english"],
            varga_degree=saptamsa_degree,
            division_number=division,
            is_own_sign=is_own,
            is_exalted=is_exalted,
            is_debilitated=is_debilitated,
            is_mooltrikona=is_mooltrikona,
        )

    def calculate_d9_navamsa(self, longitude: float, planet: str = "") -> DivisionalPosition:
        """
        D-9 Navamsa Chart (Marriage, Spouse, Dharma) - BPHS Chapter 6, Verses 9-10

        THE MOST IMPORTANT divisional chart after the Rashi chart.
        Each sign is divided into 9 parts of 3.333... degrees each (30/9).

        Rules based on the ELEMENT of the sign:
        - Fire signs (Aries, Leo, Sag): Navamsas start from Aries (0)
        - Earth signs (Taurus, Virgo, Cap): Navamsas start from Capricorn (9)
        - Air signs (Gemini, Libra, Aqua): Navamsas start from Libra (6)
        - Water signs (Cancer, Scorpio, Pisces): Navamsas start from Cancer (3)

        Formula: navamsa_sign = (start_sign + floor(degree / 3.333...)) % 12
        """
        rashi_num = int(longitude / 30) % 12
        degree_in_sign = longitude % 30

        # Each navamsa is 3.333... degrees (30/9)
        navamsa_span = 30.0 / 9.0
        division = int(degree_in_sign / navamsa_span) + 1
        division = min(division, 9)

        # Determine starting sign based on element
        element = self._get_sign_element(rashi_num)
        start_sign = NAVAMSA_START[element]

        # Calculate navamsa sign
        navamsa_rashi = (start_sign + division - 1) % 12
        navamsa_degree = degree_in_sign % navamsa_span

        is_own, is_exalted, is_debilitated, is_mooltrikona = self._get_dignity_status(planet, navamsa_rashi)

        return DivisionalPosition(
            planet=planet,
            original_longitude=longitude,
            original_rashi_num=rashi_num,
            original_rashi=RASHIS[rashi_num]["name"],
            original_degree=degree_in_sign,
            varga_rashi_num=navamsa_rashi,
            varga_rashi=RASHIS[navamsa_rashi]["name"],
            varga_rashi_english=RASHIS[navamsa_rashi]["english"],
            varga_degree=navamsa_degree,
            division_number=division,
            is_own_sign=is_own,
            is_exalted=is_exalted,
            is_debilitated=is_debilitated,
            is_mooltrikona=is_mooltrikona,
        )

    def calculate_d10_dasamsa(self, longitude: float, planet: str = "") -> DivisionalPosition:
        """
        D-10 Dasamsa Chart (Career, Profession) - BPHS Chapter 6, Verse 11

        Each sign is divided into 10 parts of 3 degrees each.

        Rules:
        - Odd signs: Start from same sign, count forward
        - Even signs: Start from 9th sign from it, count forward

        Formula: dasamsa_sign = (sign + floor(degree/3) + (0 if odd else 8)) % 12
        """
        rashi_num = int(longitude / 30) % 12
        degree_in_sign = longitude % 30
        is_odd = self._is_odd_sign(rashi_num)

        # Each division is 3 degrees
        division = int(degree_in_sign / 3.0) + 1
        division = min(division, 10)

        # Calculate dasamsa sign
        if is_odd:
            dasamsa_rashi = (rashi_num + division - 1) % 12
        else:
            # Even signs: start from 9th sign (add 8 to 0-indexed)
            dasamsa_rashi = (rashi_num + 8 + division - 1) % 12

        dasamsa_degree = degree_in_sign % 3.0

        is_own, is_exalted, is_debilitated, is_mooltrikona = self._get_dignity_status(planet, dasamsa_rashi)

        return DivisionalPosition(
            planet=planet,
            original_longitude=longitude,
            original_rashi_num=rashi_num,
            original_rashi=RASHIS[rashi_num]["name"],
            original_degree=degree_in_sign,
            varga_rashi_num=dasamsa_rashi,
            varga_rashi=RASHIS[dasamsa_rashi]["name"],
            varga_rashi_english=RASHIS[dasamsa_rashi]["english"],
            varga_degree=dasamsa_degree,
            division_number=division,
            is_own_sign=is_own,
            is_exalted=is_exalted,
            is_debilitated=is_debilitated,
            is_mooltrikona=is_mooltrikona,
        )

    def calculate_d12_dwadasamsa(self, longitude: float, planet: str = "") -> DivisionalPosition:
        """
        D-12 Dwadasamsa Chart (Parents) - BPHS Chapter 6, Verse 12

        Each sign is divided into 12 parts of 2.5 degrees each.

        Rules:
        - Always starts from the same sign
        - Counts forward through all 12 signs

        Formula: dwadasamsa_sign = (sign + floor(degree/2.5)) % 12
        """
        rashi_num = int(longitude / 30) % 12
        degree_in_sign = longitude % 30

        # Each division is 2.5 degrees
        division = int(degree_in_sign / 2.5) + 1
        division = min(division, 12)

        # Calculate dwadasamsa sign - always starts from same sign
        dwadasamsa_rashi = (rashi_num + division - 1) % 12
        dwadasamsa_degree = degree_in_sign % 2.5

        is_own, is_exalted, is_debilitated, is_mooltrikona = self._get_dignity_status(planet, dwadasamsa_rashi)

        return DivisionalPosition(
            planet=planet,
            original_longitude=longitude,
            original_rashi_num=rashi_num,
            original_rashi=RASHIS[rashi_num]["name"],
            original_degree=degree_in_sign,
            varga_rashi_num=dwadasamsa_rashi,
            varga_rashi=RASHIS[dwadasamsa_rashi]["name"],
            varga_rashi_english=RASHIS[dwadasamsa_rashi]["english"],
            varga_degree=dwadasamsa_degree,
            division_number=division,
            is_own_sign=is_own,
            is_exalted=is_exalted,
            is_debilitated=is_debilitated,
            is_mooltrikona=is_mooltrikona,
        )

    def calculate_d16_shodasamsa(self, longitude: float, planet: str = "") -> DivisionalPosition:
        """
        D-16 Shodasamsa Chart (Vehicles, Comforts) - BPHS Chapter 6, Verse 13

        Each sign is divided into 16 parts of 1.875 degrees each.

        Rules:
        - Moveable signs (Aries, Cancer, Libra, Cap): Start from Aries
        - Fixed signs (Taurus, Leo, Scorpio, Aqua): Start from Leo
        - Dual signs (Gemini, Virgo, Sag, Pisces): Start from Sagittarius
        """
        rashi_num = int(longitude / 30) % 12
        degree_in_sign = longitude % 30

        # Determine sign quality
        moveable_signs = [0, 3, 6, 9]    # Aries, Cancer, Libra, Capricorn
        fixed_signs = [1, 4, 7, 10]       # Taurus, Leo, Scorpio, Aquarius
        dual_signs = [2, 5, 8, 11]        # Gemini, Virgo, Sagittarius, Pisces

        # Each division is 30/16 = 1.875 degrees
        division_span = 30.0 / 16.0
        division = int(degree_in_sign / division_span) + 1
        division = min(division, 16)

        # Determine starting sign
        if rashi_num in moveable_signs:
            start_sign = 0   # Aries
        elif rashi_num in fixed_signs:
            start_sign = 4   # Leo
        else:
            start_sign = 8   # Sagittarius

        shodasamsa_rashi = (start_sign + division - 1) % 12
        shodasamsa_degree = degree_in_sign % division_span

        is_own, is_exalted, is_debilitated, is_mooltrikona = self._get_dignity_status(planet, shodasamsa_rashi)

        return DivisionalPosition(
            planet=planet,
            original_longitude=longitude,
            original_rashi_num=rashi_num,
            original_rashi=RASHIS[rashi_num]["name"],
            original_degree=degree_in_sign,
            varga_rashi_num=shodasamsa_rashi,
            varga_rashi=RASHIS[shodasamsa_rashi]["name"],
            varga_rashi_english=RASHIS[shodasamsa_rashi]["english"],
            varga_degree=shodasamsa_degree,
            division_number=division,
            is_own_sign=is_own,
            is_exalted=is_exalted,
            is_debilitated=is_debilitated,
            is_mooltrikona=is_mooltrikona,
        )

    def calculate_d20_vimsamsa(self, longitude: float, planet: str = "") -> DivisionalPosition:
        """
        D-20 Vimsamsa Chart (Spiritual Progress) - BPHS Chapter 6, Verse 14

        Each sign is divided into 20 parts of 1.5 degrees each.

        Rules:
        - Moveable signs: Start from Aries
        - Fixed signs: Start from Sagittarius
        - Dual signs: Start from Leo
        """
        rashi_num = int(longitude / 30) % 12
        degree_in_sign = longitude % 30

        moveable_signs = [0, 3, 6, 9]
        fixed_signs = [1, 4, 7, 10]

        # Each division is 1.5 degrees
        division_span = 30.0 / 20.0
        division = int(degree_in_sign / division_span) + 1
        division = min(division, 20)

        # Determine starting sign
        if rashi_num in moveable_signs:
            start_sign = 0   # Aries
        elif rashi_num in fixed_signs:
            start_sign = 8   # Sagittarius
        else:
            start_sign = 4   # Leo

        vimsamsa_rashi = (start_sign + division - 1) % 12
        vimsamsa_degree = degree_in_sign % division_span

        is_own, is_exalted, is_debilitated, is_mooltrikona = self._get_dignity_status(planet, vimsamsa_rashi)

        return DivisionalPosition(
            planet=planet,
            original_longitude=longitude,
            original_rashi_num=rashi_num,
            original_rashi=RASHIS[rashi_num]["name"],
            original_degree=degree_in_sign,
            varga_rashi_num=vimsamsa_rashi,
            varga_rashi=RASHIS[vimsamsa_rashi]["name"],
            varga_rashi_english=RASHIS[vimsamsa_rashi]["english"],
            varga_degree=vimsamsa_degree,
            division_number=division,
            is_own_sign=is_own,
            is_exalted=is_exalted,
            is_debilitated=is_debilitated,
            is_mooltrikona=is_mooltrikona,
        )

    def calculate_d24_chaturvimsamsa(self, longitude: float, planet: str = "") -> DivisionalPosition:
        """
        D-24 Chaturvimsamsa/Siddhamsa Chart (Education, Learning) - BPHS Chapter 6, Verse 15

        Each sign is divided into 24 parts of 1.25 degrees each.

        Rules:
        - Odd signs: Start from Leo
        - Even signs: Start from Cancer
        """
        rashi_num = int(longitude / 30) % 12
        degree_in_sign = longitude % 30
        is_odd = self._is_odd_sign(rashi_num)

        # Each division is 1.25 degrees
        division_span = 30.0 / 24.0
        division = int(degree_in_sign / division_span) + 1
        division = min(division, 24)

        # Determine starting sign
        if is_odd:
            start_sign = 4   # Leo
        else:
            start_sign = 3   # Cancer

        siddhamsa_rashi = (start_sign + division - 1) % 12
        siddhamsa_degree = degree_in_sign % division_span

        is_own, is_exalted, is_debilitated, is_mooltrikona = self._get_dignity_status(planet, siddhamsa_rashi)

        return DivisionalPosition(
            planet=planet,
            original_longitude=longitude,
            original_rashi_num=rashi_num,
            original_rashi=RASHIS[rashi_num]["name"],
            original_degree=degree_in_sign,
            varga_rashi_num=siddhamsa_rashi,
            varga_rashi=RASHIS[siddhamsa_rashi]["name"],
            varga_rashi_english=RASHIS[siddhamsa_rashi]["english"],
            varga_degree=siddhamsa_degree,
            division_number=division,
            is_own_sign=is_own,
            is_exalted=is_exalted,
            is_debilitated=is_debilitated,
            is_mooltrikona=is_mooltrikona,
        )

    def calculate_d27_bhamsa(self, longitude: float, planet: str = "") -> DivisionalPosition:
        """
        D-27 Bhamsa/Nakshatramsa Chart (Strength, Weakness) - BPHS Chapter 6, Verse 16

        Each sign is divided into 27 parts of 1.111... degrees each.
        Based on the nakshatra system.

        Rules:
        - Fire signs: Start from Aries
        - Earth signs: Start from Cancer
        - Air signs: Start from Libra
        - Water signs: Start from Capricorn
        """
        rashi_num = int(longitude / 30) % 12
        degree_in_sign = longitude % 30
        element = self._get_sign_element(rashi_num)

        # Each division is 30/27 = 1.111... degrees
        division_span = 30.0 / 27.0
        division = int(degree_in_sign / division_span) + 1
        division = min(division, 27)

        # Determine starting sign based on element
        if element == 'Fire':
            start_sign = 0   # Aries
        elif element == 'Earth':
            start_sign = 3   # Cancer
        elif element == 'Air':
            start_sign = 6   # Libra
        else:
            start_sign = 9   # Capricorn

        bhamsa_rashi = (start_sign + division - 1) % 12
        bhamsa_degree = degree_in_sign % division_span

        is_own, is_exalted, is_debilitated, is_mooltrikona = self._get_dignity_status(planet, bhamsa_rashi)

        return DivisionalPosition(
            planet=planet,
            original_longitude=longitude,
            original_rashi_num=rashi_num,
            original_rashi=RASHIS[rashi_num]["name"],
            original_degree=degree_in_sign,
            varga_rashi_num=bhamsa_rashi,
            varga_rashi=RASHIS[bhamsa_rashi]["name"],
            varga_rashi_english=RASHIS[bhamsa_rashi]["english"],
            varga_degree=bhamsa_degree,
            division_number=division,
            is_own_sign=is_own,
            is_exalted=is_exalted,
            is_debilitated=is_debilitated,
            is_mooltrikona=is_mooltrikona,
        )

    def calculate_d30_trimsamsa(self, longitude: float, planet: str = "") -> DivisionalPosition:
        """
        D-30 Trimsamsa Chart (Evils, Misfortunes) - BPHS Chapter 6, Verses 17-18

        SPECIAL: This chart has only 5 unequal divisions (not 30 equal ones).
        The name refers to the 30-degree sign being divided differently.

        For ODD signs (Aries, Gemini, Leo, Libra, Sag, Aqua):
        - 0-5 degrees: Mars (Aries)
        - 5-10 degrees: Saturn (Aquarius)
        - 10-18 degrees: Jupiter (Sagittarius)
        - 18-25 degrees: Mercury (Gemini)
        - 25-30 degrees: Venus (Taurus)

        For EVEN signs (Taurus, Cancer, Virgo, Scorpio, Cap, Pisces):
        - Reverse the order:
        - 0-5 degrees: Venus (Taurus)
        - 5-12 degrees: Mercury (Gemini)
        - 12-20 degrees: Jupiter (Sagittarius)
        - 20-25 degrees: Saturn (Aquarius)
        - 25-30 degrees: Mars (Aries)
        """
        rashi_num = int(longitude / 30) % 12
        degree_in_sign = longitude % 30
        is_odd = self._is_odd_sign(rashi_num)

        # Trimsamsa rulers and their signs
        if is_odd:
            if degree_in_sign < 5:
                trimsamsa_rashi = 0    # Aries (Mars)
                division = 1
            elif degree_in_sign < 10:
                trimsamsa_rashi = 10   # Aquarius (Saturn)
                division = 2
            elif degree_in_sign < 18:
                trimsamsa_rashi = 8    # Sagittarius (Jupiter)
                division = 3
            elif degree_in_sign < 25:
                trimsamsa_rashi = 2    # Gemini (Mercury)
                division = 4
            else:
                trimsamsa_rashi = 1    # Taurus (Venus)
                division = 5
        else:  # Even signs - reverse order
            if degree_in_sign < 5:
                trimsamsa_rashi = 1    # Taurus (Venus)
                division = 1
            elif degree_in_sign < 12:
                trimsamsa_rashi = 2    # Gemini (Mercury)
                division = 2
            elif degree_in_sign < 20:
                trimsamsa_rashi = 8    # Sagittarius (Jupiter)
                division = 3
            elif degree_in_sign < 25:
                trimsamsa_rashi = 10   # Aquarius (Saturn)
                division = 4
            else:
                trimsamsa_rashi = 0    # Aries (Mars)
                division = 5

        is_own, is_exalted, is_debilitated, is_mooltrikona = self._get_dignity_status(planet, trimsamsa_rashi)

        return DivisionalPosition(
            planet=planet,
            original_longitude=longitude,
            original_rashi_num=rashi_num,
            original_rashi=RASHIS[rashi_num]["name"],
            original_degree=degree_in_sign,
            varga_rashi_num=trimsamsa_rashi,
            varga_rashi=RASHIS[trimsamsa_rashi]["name"],
            varga_rashi_english=RASHIS[trimsamsa_rashi]["english"],
            varga_degree=degree_in_sign,  # Keep original as divisions are unequal
            division_number=division,
            is_own_sign=is_own,
            is_exalted=is_exalted,
            is_debilitated=is_debilitated,
            is_mooltrikona=is_mooltrikona,
        )

    def calculate_d40_khavedamsa(self, longitude: float, planet: str = "") -> DivisionalPosition:
        """
        D-40 Khavedamsa Chart (Auspicious/Inauspicious Effects) - BPHS Chapter 6, Verse 19

        Each sign is divided into 40 parts of 0.75 degrees each.

        Rules:
        - Odd signs: Start from Aries
        - Even signs: Start from Libra
        """
        rashi_num = int(longitude / 30) % 12
        degree_in_sign = longitude % 30
        is_odd = self._is_odd_sign(rashi_num)

        # Each division is 0.75 degrees
        division_span = 30.0 / 40.0
        division = int(degree_in_sign / division_span) + 1
        division = min(division, 40)

        # Determine starting sign
        start_sign = 0 if is_odd else 6  # Aries or Libra

        khavedamsa_rashi = (start_sign + division - 1) % 12
        khavedamsa_degree = degree_in_sign % division_span

        is_own, is_exalted, is_debilitated, is_mooltrikona = self._get_dignity_status(planet, khavedamsa_rashi)

        return DivisionalPosition(
            planet=planet,
            original_longitude=longitude,
            original_rashi_num=rashi_num,
            original_rashi=RASHIS[rashi_num]["name"],
            original_degree=degree_in_sign,
            varga_rashi_num=khavedamsa_rashi,
            varga_rashi=RASHIS[khavedamsa_rashi]["name"],
            varga_rashi_english=RASHIS[khavedamsa_rashi]["english"],
            varga_degree=khavedamsa_degree,
            division_number=division,
            is_own_sign=is_own,
            is_exalted=is_exalted,
            is_debilitated=is_debilitated,
            is_mooltrikona=is_mooltrikona,
        )

    def calculate_d45_akshavedamsa(self, longitude: float, planet: str = "") -> DivisionalPosition:
        """
        D-45 Akshavedamsa Chart (General Indications) - BPHS Chapter 6, Verse 20

        Each sign is divided into 45 parts of 0.666... degrees each.

        Rules:
        - Moveable signs: Start from Aries
        - Fixed signs: Start from Leo
        - Dual signs: Start from Sagittarius
        """
        rashi_num = int(longitude / 30) % 12
        degree_in_sign = longitude % 30

        moveable_signs = [0, 3, 6, 9]
        fixed_signs = [1, 4, 7, 10]

        # Each division is 30/45 = 0.666... degrees
        division_span = 30.0 / 45.0
        division = int(degree_in_sign / division_span) + 1
        division = min(division, 45)

        # Determine starting sign
        if rashi_num in moveable_signs:
            start_sign = 0   # Aries
        elif rashi_num in fixed_signs:
            start_sign = 4   # Leo
        else:
            start_sign = 8   # Sagittarius

        akshavedamsa_rashi = (start_sign + division - 1) % 12
        akshavedamsa_degree = degree_in_sign % division_span

        is_own, is_exalted, is_debilitated, is_mooltrikona = self._get_dignity_status(planet, akshavedamsa_rashi)

        return DivisionalPosition(
            planet=planet,
            original_longitude=longitude,
            original_rashi_num=rashi_num,
            original_rashi=RASHIS[rashi_num]["name"],
            original_degree=degree_in_sign,
            varga_rashi_num=akshavedamsa_rashi,
            varga_rashi=RASHIS[akshavedamsa_rashi]["name"],
            varga_rashi_english=RASHIS[akshavedamsa_rashi]["english"],
            varga_degree=akshavedamsa_degree,
            division_number=division,
            is_own_sign=is_own,
            is_exalted=is_exalted,
            is_debilitated=is_debilitated,
            is_mooltrikona=is_mooltrikona,
        )

    def calculate_d60_shashtiamsa(self, longitude: float, planet: str = "") -> DivisionalPosition:
        """
        D-60 Shashtiamsa Chart (Past Life Karma) - BPHS Chapter 6, Verses 21-37

        VERY IMPORTANT chart for determining past-life karmic influences.
        Each sign is divided into 60 parts of 0.5 degrees each.

        Rules:
        - Odd signs: Count divisions from same sign
        - Even signs: Count divisions from the sign opposite (180 degrees away)

        Each division has a specific name and deity associated with it.
        """
        rashi_num = int(longitude / 30) % 12
        degree_in_sign = longitude % 30
        is_odd = self._is_odd_sign(rashi_num)

        # Each division is 0.5 degrees
        division_span = 30.0 / 60.0
        division = int(degree_in_sign / division_span) + 1
        division = min(division, 60)

        # Calculate shashtiamsa sign
        if is_odd:
            # Odd signs: count from same sign
            shashtiamsa_rashi = (rashi_num + ((division - 1) // 5)) % 12
        else:
            # Even signs: count from opposite sign
            opposite_sign = (rashi_num + 6) % 12
            shashtiamsa_rashi = (opposite_sign + ((division - 1) // 5)) % 12

        shashtiamsa_degree = degree_in_sign % division_span

        is_own, is_exalted, is_debilitated, is_mooltrikona = self._get_dignity_status(planet, shashtiamsa_rashi)

        # Get shashtiamsa name and details
        shashtiamsa_index = (division - 1) % 60
        shashtiamsa_info = SHASHTIAMSA_NAMES[shashtiamsa_index]

        position = DivisionalPosition(
            planet=planet,
            original_longitude=longitude,
            original_rashi_num=rashi_num,
            original_rashi=RASHIS[rashi_num]["name"],
            original_degree=degree_in_sign,
            varga_rashi_num=shashtiamsa_rashi,
            varga_rashi=RASHIS[shashtiamsa_rashi]["name"],
            varga_rashi_english=RASHIS[shashtiamsa_rashi]["english"],
            varga_degree=shashtiamsa_degree,
            division_number=division,
            is_own_sign=is_own,
            is_exalted=is_exalted,
            is_debilitated=is_debilitated,
            is_mooltrikona=is_mooltrikona,
        )

        # Add shashtiamsa-specific details as additional attributes
        position.shashtiamsa_name = shashtiamsa_info["name"]
        position.shashtiamsa_deity = shashtiamsa_info["deity"]
        position.shashtiamsa_nature = shashtiamsa_info["nature"]

        return position

    def calculate_varga(self, varga: VargaChart, longitude: float, planet: str = "") -> DivisionalPosition:
        """Calculate position for any varga chart."""
        calculator_map = {
            VargaChart.D1_RASHI: self.calculate_d1_rashi,
            VargaChart.D2_HORA: self.calculate_d2_hora,
            VargaChart.D3_DREKKANA: self.calculate_d3_drekkana,
            VargaChart.D4_CHATURTHAMSA: self.calculate_d4_chaturthamsa,
            VargaChart.D7_SAPTAMSA: self.calculate_d7_saptamsa,
            VargaChart.D9_NAVAMSA: self.calculate_d9_navamsa,
            VargaChart.D10_DASAMSA: self.calculate_d10_dasamsa,
            VargaChart.D12_DWADASAMSA: self.calculate_d12_dwadasamsa,
            VargaChart.D16_SHODASAMSA: self.calculate_d16_shodasamsa,
            VargaChart.D20_VIMSAMSA: self.calculate_d20_vimsamsa,
            VargaChart.D24_CHATURVIMSAMSA: self.calculate_d24_chaturvimsamsa,
            VargaChart.D27_BHAMSA: self.calculate_d27_bhamsa,
            VargaChart.D30_TRIMSAMSA: self.calculate_d30_trimsamsa,
            VargaChart.D40_KHAVEDAMSA: self.calculate_d40_khavedamsa,
            VargaChart.D45_AKSHAVEDAMSA: self.calculate_d45_akshavedamsa,
            VargaChart.D60_SHASHTIAMSA: self.calculate_d60_shashtiamsa,
        }
        return calculator_map[varga](longitude, planet)

    def calculate_all_vargas(self, longitude: float, planet: str = "") -> Dict[str, DivisionalPosition]:
        """Calculate all 16 varga positions for a single planet."""
        return {
            varga.name: self.calculate_varga(varga, longitude, planet)
            for varga in VargaChart
        }

    def calculate_complete_varga_chart(
        self,
        varga: VargaChart,
        lagna_longitude: float,
        planets: Dict[str, Dict],
    ) -> DivisionalChart:
        """
        Calculate a complete divisional chart with lagna and all planets.

        Args:
            varga: The divisional chart to calculate
            lagna_longitude: Sidereal longitude of the Ascendant
            planets: Dictionary of planet data from main chart

        Returns:
            DivisionalChart with all positions
        """
        varga_descriptions = {
            VargaChart.D1_RASHI: ("Rashi", "Main birth chart - overall life patterns"),
            VargaChart.D2_HORA: ("Hora", "Wealth and financial prosperity"),
            VargaChart.D3_DREKKANA: ("Drekkana", "Siblings, courage, and short journeys"),
            VargaChart.D4_CHATURTHAMSA: ("Chaturthamsa", "Property, home, and fortune"),
            VargaChart.D7_SAPTAMSA: ("Saptamsa", "Children and progeny"),
            VargaChart.D9_NAVAMSA: ("Navamsa", "Marriage, spouse, and dharma"),
            VargaChart.D10_DASAMSA: ("Dasamsa", "Career and profession"),
            VargaChart.D12_DWADASAMSA: ("Dwadasamsa", "Parents and ancestry"),
            VargaChart.D16_SHODASAMSA: ("Shodasamsa", "Vehicles and comforts"),
            VargaChart.D20_VIMSAMSA: ("Vimsamsa", "Spiritual progress and worship"),
            VargaChart.D24_CHATURVIMSAMSA: ("Siddhamsa", "Education and learning"),
            VargaChart.D27_BHAMSA: ("Bhamsa", "Physical strength and weakness"),
            VargaChart.D30_TRIMSAMSA: ("Trimsamsa", "Evils and misfortunes"),
            VargaChart.D40_KHAVEDAMSA: ("Khavedamsa", "Auspicious/inauspicious effects"),
            VargaChart.D45_AKSHAVEDAMSA: ("Akshavedamsa", "General life indications"),
            VargaChart.D60_SHASHTIAMSA: ("Shashtiamsa", "Past life karma"),
        }

        varga_name, varga_desc = varga_descriptions[varga]

        # Calculate lagna position
        lagna_pos = self.calculate_varga(varga, lagna_longitude, "LAGNA")

        # Calculate all planet positions
        planet_positions = {}
        for planet_name, planet_data in planets.items():
            longitude = planet_data["longitude"]
            planet_positions[planet_name] = self.calculate_varga(varga, longitude, planet_name)

        # Calculate planets in houses (relative to varga lagna)
        planets_in_houses = {i: [] for i in range(1, 13)}
        varga_lagna_num = lagna_pos.varga_rashi_num

        for planet_name, pos in planet_positions.items():
            house = ((pos.varga_rashi_num - varga_lagna_num) % 12) + 1
            planets_in_houses[house].append(planet_name)

        return DivisionalChart(
            varga_type=varga,
            varga_name=varga_name,
            varga_description=varga_desc,
            division_count=varga.value,
            lagna=lagna_pos,
            planets=planet_positions,
            planets_in_houses=planets_in_houses,
        )


class VimshopakaBala:
    """
    Vimshopaka Bala (20-Point Strength) Calculator
    Based on BPHS Chapter 44

    This measures planetary strength across multiple divisional charts.
    """

    # Shadvarga scheme (6 vargas) weights
    SHADVARGA_WEIGHTS = {
        VargaChart.D1_RASHI: 6,
        VargaChart.D2_HORA: 2,
        VargaChart.D3_DREKKANA: 4,
        VargaChart.D9_NAVAMSA: 5,
        VargaChart.D12_DWADASAMSA: 2,
        VargaChart.D30_TRIMSAMSA: 1,
    }

    # Saptavarga scheme (7 vargas) weights
    SAPTAVARGA_WEIGHTS = {
        VargaChart.D1_RASHI: 5,
        VargaChart.D2_HORA: 2,
        VargaChart.D3_DREKKANA: 3,
        VargaChart.D7_SAPTAMSA: 2.5,
        VargaChart.D9_NAVAMSA: 4.5,
        VargaChart.D12_DWADASAMSA: 2,
        VargaChart.D30_TRIMSAMSA: 1,
    }

    # Dashavarga scheme (10 vargas) weights
    DASHAVARGA_WEIGHTS = {
        VargaChart.D1_RASHI: 3,
        VargaChart.D2_HORA: 1.5,
        VargaChart.D3_DREKKANA: 1.5,
        VargaChart.D7_SAPTAMSA: 1.5,
        VargaChart.D9_NAVAMSA: 3,
        VargaChart.D10_DASAMSA: 3,
        VargaChart.D12_DWADASAMSA: 1.5,
        VargaChart.D16_SHODASAMSA: 2,
        VargaChart.D30_TRIMSAMSA: 1.5,
        VargaChart.D60_SHASHTIAMSA: 1.5,
    }

    # Shodashavarga scheme (16 vargas) weights - most comprehensive
    SHODASHAVARGA_WEIGHTS = {
        VargaChart.D1_RASHI: 3.5,
        VargaChart.D2_HORA: 1,
        VargaChart.D3_DREKKANA: 1,
        VargaChart.D4_CHATURTHAMSA: 0.5,
        VargaChart.D7_SAPTAMSA: 0.5,
        VargaChart.D9_NAVAMSA: 3,
        VargaChart.D10_DASAMSA: 2.5,
        VargaChart.D12_DWADASAMSA: 0.5,
        VargaChart.D16_SHODASAMSA: 2,
        VargaChart.D20_VIMSAMSA: 0.5,
        VargaChart.D24_CHATURVIMSAMSA: 0.5,
        VargaChart.D27_BHAMSA: 0.5,
        VargaChart.D30_TRIMSAMSA: 1,
        VargaChart.D40_KHAVEDAMSA: 0.5,
        VargaChart.D45_AKSHAVEDAMSA: 0.5,
        VargaChart.D60_SHASHTIAMSA: 2,
    }

    def __init__(self):
        self.calculator = DivisionalChartCalculator()

    def _get_dignity_points(self, position: DivisionalPosition) -> float:
        """
        Calculate dignity points for a planet in a varga.

        Points as per BPHS:
        - Own sign: Full weight
        - Exalted: Full weight
        - Mooltrikona: Full weight
        - Friendly sign: 3/4 weight
        - Neutral sign: 1/2 weight
        - Enemy sign: 1/4 weight
        - Debilitated: 0 points
        """
        if position.is_debilitated:
            return 0.0
        elif position.is_exalted or position.is_own_sign or position.is_mooltrikona:
            return 1.0
        else:
            # Simplified: assume neutral for other cases
            # Full implementation would check friendly/enemy status
            return 0.5

    def calculate_shadvarga_bala(
        self,
        longitude: float,
        planet: str
    ) -> Dict:
        """Calculate Shadvarga (6-chart) strength."""
        total_points = 0.0
        details = {}

        for varga, weight in self.SHADVARGA_WEIGHTS.items():
            position = self.calculator.calculate_varga(varga, longitude, planet)
            dignity_points = self._get_dignity_points(position)
            weighted_points = dignity_points * weight

            details[varga.name] = {
                "rashi": position.varga_rashi,
                "dignity_points": dignity_points,
                "weight": weight,
                "weighted_points": weighted_points,
            }
            total_points += weighted_points

        return {
            "total_points": round(total_points, 2),
            "max_points": 20.0,
            "percentage": round((total_points / 20.0) * 100, 1),
            "details": details,
        }

    def calculate_shodashavarga_bala(
        self,
        longitude: float,
        planet: str
    ) -> Dict:
        """Calculate Shodashavarga (16-chart) strength."""
        total_points = 0.0
        details = {}

        for varga, weight in self.SHODASHAVARGA_WEIGHTS.items():
            position = self.calculator.calculate_varga(varga, longitude, planet)
            dignity_points = self._get_dignity_points(position)
            weighted_points = dignity_points * weight

            details[varga.name] = {
                "rashi": position.varga_rashi,
                "dignity_points": dignity_points,
                "weight": weight,
                "weighted_points": weighted_points,
            }
            total_points += weighted_points

        return {
            "total_points": round(total_points, 2),
            "max_points": 20.0,
            "percentage": round((total_points / 20.0) * 100, 1),
            "details": details,
        }


def get_varga_chart_for_kundali(
    kundali,
    varga: VargaChart = VargaChart.D9_NAVAMSA
) -> DivisionalChart:
    """
    Helper function to get a divisional chart from a Kundali object.

    Args:
        kundali: Kundali object with lagna and planets
        varga: Which divisional chart to calculate

    Returns:
        DivisionalChart with all positions
    """
    calculator = DivisionalChartCalculator()
    return calculator.calculate_complete_varga_chart(
        varga=varga,
        lagna_longitude=kundali.lagna["longitude"],
        planets=kundali.planets,
    )


def get_all_varga_charts_for_kundali(kundali) -> Dict[str, DivisionalChart]:
    """
    Get all 16 divisional charts for a Kundali.

    Args:
        kundali: Kundali object

    Returns:
        Dictionary mapping varga name to DivisionalChart
    """
    calculator = DivisionalChartCalculator()
    charts = {}

    for varga in VargaChart:
        charts[varga.name] = calculator.calculate_complete_varga_chart(
            varga=varga,
            lagna_longitude=kundali.lagna["longitude"],
            planets=kundali.planets,
        )

    return charts


def get_planet_vimshopaka_bala(kundali) -> Dict[str, Dict]:
    """
    Calculate Vimshopaka Bala for all planets in a Kundali.

    Args:
        kundali: Kundali object

    Returns:
        Dictionary of planet strengths
    """
    bala_calculator = VimshopakaBala()
    results = {}

    for planet_name, planet_data in kundali.planets.items():
        longitude = planet_data["longitude"]
        results[planet_name] = {
            "shadvarga": bala_calculator.calculate_shadvarga_bala(longitude, planet_name),
            "shodashavarga": bala_calculator.calculate_shodashavarga_bala(longitude, planet_name),
        }

    return results
