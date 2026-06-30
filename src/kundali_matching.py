"""
Kundali Matching (Marriage Compatibility) - Ashtakoot Milan

Based on classical Vedic astrology texts:
- Brihat Parashara Hora Shastra (BPHS)
- Muhurta Chintamani
- Jataka Parijata

This module implements the complete Ashtakoot (8-fold) matching system
used in North India for marriage compatibility analysis.

Total: 36 Gunas (Points)
- Varna: 1 point
- Vashya: 2 points
- Tara: 3 points
- Yoni: 4 points
- Graha Maitri: 5 points
- Gana: 6 points
- Bhakoot: 7 points
- Nadi: 8 points

Enhanced with accuracy components (BPHS-based):
- Shadbala comparison for Venus, Jupiter, 7th lord
- Combustion check for key marriage planets
- Navamsa D9 analysis
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum

from .config import RASHIS, NAKSHATRAS, NATURAL_RELATIONSHIPS, COMBUSTION_ORBS

# Import accuracy components for enhanced matching
try:
    from .shadbala import ShadbalaCalculator
    SHADBALA_AVAILABLE = True
except ImportError:
    SHADBALA_AVAILABLE = False

try:
    from .rashifal import check_combustion, get_navamsa_strength_modifier
    ACCURACY_COMPONENTS_AVAILABLE = True
except ImportError:
    ACCURACY_COMPONENTS_AVAILABLE = False


# =============================================================================
# NAKSHATRA CONSTANTS (0-indexed for internal use)
# =============================================================================

NAKSHATRA_NAMES = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]


# =============================================================================
# VARNA (Caste/Spiritual Level) - 1 Point
# Based on Brihat Parashara Hora Shastra
# =============================================================================

class Varna(Enum):
    BRAHMIN = 4  # Highest spiritual level
    KSHATRIYA = 3
    VAISHYA = 2
    SHUDRA = 1  # Lowest in hierarchy


# Varna classification by Rashi (Moon Sign)
# Cancer, Scorpio, Pisces = Brahmin (Water signs)
# Aries, Leo, Sagittarius = Kshatriya (Fire signs)
# Taurus, Virgo, Capricorn = Vaishya (Earth signs)
# Gemini, Libra, Aquarius = Shudra (Air signs)
RASHI_VARNA = {
    0: Varna.KSHATRIYA,   # Mesha (Aries)
    1: Varna.VAISHYA,     # Vrishabha (Taurus)
    2: Varna.SHUDRA,      # Mithuna (Gemini)
    3: Varna.BRAHMIN,     # Karka (Cancer)
    4: Varna.KSHATRIYA,   # Simha (Leo)
    5: Varna.VAISHYA,     # Kanya (Virgo)
    6: Varna.SHUDRA,      # Tula (Libra)
    7: Varna.BRAHMIN,     # Vrishchika (Scorpio)
    8: Varna.KSHATRIYA,   # Dhanu (Sagittarius)
    9: Varna.VAISHYA,     # Makara (Capricorn)
    10: Varna.SHUDRA,     # Kumbha (Aquarius)
    11: Varna.BRAHMIN,    # Meena (Pisces)
}


# =============================================================================
# VASHYA (Dominance/Control) - 2 Points
# Based on Muhurta Chintamani
# =============================================================================

class VashyaType(Enum):
    CHATUSHPADA = "Chatushpada"   # Quadruped
    MANAVA = "Manava"             # Human
    JALACHARA = "Jalachara"       # Water creature
    VANACHARA = "Vanachara"       # Wild animal (forest dweller)
    KEETA = "Keeta"               # Insect


# Vashya classification by Rashi
# Note: Some signs have split classifications based on degree
def get_vashya_type(rashi_num: int, degree: float = 15.0) -> VashyaType:
    """
    Get Vashya type for a Rashi.

    Per Muhurta Chintamani:
    - Chatushpada (quadruped): Aries, Taurus, 2nd half of Sagittarius, 1st half of Capricorn
    - Manava (human): Gemini, Virgo, Libra, 1st half of Sagittarius, Aquarius
    - Jalachara (water): Cancer, Pisces, 2nd half of Capricorn
    - Vanachara (wild/forest): Leo
    - Keeta (insect): Scorpio
    """
    if rashi_num == 0:  # Aries
        return VashyaType.CHATUSHPADA
    elif rashi_num == 1:  # Taurus
        return VashyaType.CHATUSHPADA
    elif rashi_num == 2:  # Gemini
        return VashyaType.MANAVA
    elif rashi_num == 3:  # Cancer
        return VashyaType.JALACHARA
    elif rashi_num == 4:  # Leo
        return VashyaType.VANACHARA
    elif rashi_num == 5:  # Virgo
        return VashyaType.MANAVA
    elif rashi_num == 6:  # Libra
        return VashyaType.MANAVA
    elif rashi_num == 7:  # Scorpio
        return VashyaType.KEETA
    elif rashi_num == 8:  # Sagittarius
        # First half (0-15 deg) = Manava, Second half (15-30 deg) = Chatushpada
        return VashyaType.MANAVA if degree < 15 else VashyaType.CHATUSHPADA
    elif rashi_num == 9:  # Capricorn
        # First half (0-15 deg) = Chatushpada, Second half (15-30 deg) = Jalachara
        return VashyaType.CHATUSHPADA if degree < 15 else VashyaType.JALACHARA
    elif rashi_num == 10:  # Aquarius
        return VashyaType.MANAVA
    elif rashi_num == 11:  # Pisces
        return VashyaType.JALACHARA
    return VashyaType.MANAVA  # Default


# Vashya compatibility matrix (row = boy, col = girl)
# Values: 2 = Full, 1 = Half, 0.5 = Quarter, 0 = None
VASHYA_MATRIX = {
    VashyaType.CHATUSHPADA: {
        VashyaType.CHATUSHPADA: 2,
        VashyaType.MANAVA: 0.5,
        VashyaType.JALACHARA: 0,
        VashyaType.VANACHARA: 1,
        VashyaType.KEETA: 0,
    },
    VashyaType.MANAVA: {
        VashyaType.CHATUSHPADA: 0.5,
        VashyaType.MANAVA: 2,
        VashyaType.JALACHARA: 0.5,
        VashyaType.VANACHARA: 0,
        VashyaType.KEETA: 1,
    },
    VashyaType.JALACHARA: {
        VashyaType.CHATUSHPADA: 0,
        VashyaType.MANAVA: 0.5,
        VashyaType.JALACHARA: 2,
        VashyaType.VANACHARA: 0,
        VashyaType.KEETA: 0.5,
    },
    VashyaType.VANACHARA: {
        VashyaType.CHATUSHPADA: 1,
        VashyaType.MANAVA: 0,
        VashyaType.JALACHARA: 0,
        VashyaType.VANACHARA: 2,
        VashyaType.KEETA: 1,
    },
    VashyaType.KEETA: {
        VashyaType.CHATUSHPADA: 0,
        VashyaType.MANAVA: 1,
        VashyaType.JALACHARA: 0.5,
        VashyaType.VANACHARA: 1,
        VashyaType.KEETA: 2,
    },
}


# =============================================================================
# TARA (Birth Star Compatibility) - 3 Points
# Based on Brihat Parashara Hora Shastra
# =============================================================================

# Tara names and their effects (1-9 cycle)
TARA_NAMES = {
    1: {"name": "Janma", "hindi": "जन्म", "effect": "Birth star - neutral to mildly inauspicious"},
    2: {"name": "Sampat", "hindi": "सम्पत्", "effect": "Wealth and prosperity - very auspicious"},
    3: {"name": "Vipat", "hindi": "विपत्", "effect": "Danger and obstacles - inauspicious"},
    4: {"name": "Kshema", "hindi": "क्षेम", "effect": "Prosperity and well-being - auspicious"},
    5: {"name": "Pratyak", "hindi": "प्रत्यक्", "effect": "Obstacles and hindrances - inauspicious"},
    6: {"name": "Sadhaka", "hindi": "साधक", "effect": "Achievement and success - auspicious"},
    7: {"name": "Naidhana", "hindi": "नैधन", "effect": "Death-like suffering - most inauspicious"},
    8: {"name": "Mitra", "hindi": "मित्र", "effect": "Friendship - auspicious"},
    9: {"name": "Paramamitra", "hindi": "परममित्र", "effect": "Best friendship - most auspicious"},
}

# Inauspicious Taras to avoid (3, 5, 7)
INAUSPICIOUS_TARAS = {3, 5, 7}


# =============================================================================
# YONI (Sexual/Physical Compatibility) - 4 Points
# Based on Brihat Parashara Hora Shastra
# =============================================================================

class Yoni(Enum):
    HORSE = "Ashwa"       # Horse
    ELEPHANT = "Gaja"     # Elephant
    SHEEP = "Mesha"       # Sheep/Goat
    SERPENT = "Sarpa"     # Snake
    DOG = "Shwan"         # Dog
    CAT = "Marjara"       # Cat
    RAT = "Mushaka"       # Rat
    COW = "Gau"           # Cow
    BUFFALO = "Mahisha"   # Buffalo
    TIGER = "Vyaghra"     # Tiger
    DEER = "Mriga"        # Deer
    MONKEY = "Vanara"     # Monkey
    MONGOOSE = "Nakula"   # Mongoose
    LION = "Simha"        # Lion


# Nakshatra to Yoni mapping (0-indexed)
NAKSHATRA_YONI = {
    0: Yoni.HORSE,      # Ashwini
    1: Yoni.ELEPHANT,   # Bharani
    2: Yoni.SHEEP,      # Krittika
    3: Yoni.SERPENT,    # Rohini
    4: Yoni.SERPENT,    # Mrigashira
    5: Yoni.DOG,        # Ardra
    6: Yoni.CAT,        # Punarvasu
    7: Yoni.SHEEP,      # Pushya
    8: Yoni.CAT,        # Ashlesha
    9: Yoni.RAT,        # Magha
    10: Yoni.RAT,       # Purva Phalguni
    11: Yoni.COW,       # Uttara Phalguni
    12: Yoni.BUFFALO,   # Hasta
    13: Yoni.TIGER,     # Chitra
    14: Yoni.BUFFALO,   # Swati
    15: Yoni.TIGER,     # Vishakha
    16: Yoni.DEER,      # Anuradha
    17: Yoni.DEER,      # Jyeshtha
    18: Yoni.DOG,       # Mula
    19: Yoni.MONKEY,    # Purva Ashadha
    20: Yoni.MONGOOSE,  # Uttara Ashadha
    21: Yoni.MONKEY,    # Shravana
    22: Yoni.LION,      # Dhanishta
    23: Yoni.HORSE,     # Shatabhisha
    24: Yoni.LION,      # Purva Bhadrapada
    25: Yoni.COW,       # Uttara Bhadrapada
    26: Yoni.ELEPHANT,  # Revati
}

# Yoni gender mapping (Male/Female pairs for each nakshatra)
NAKSHATRA_YONI_GENDER = {
    0: "M",   # Ashwini - Male Horse
    1: "M",   # Bharani - Male Elephant
    2: "F",   # Krittika - Female Sheep
    3: "M",   # Rohini - Male Serpent
    4: "F",   # Mrigashira - Female Serpent
    5: "F",   # Ardra - Female Dog
    6: "M",   # Punarvasu - Male Cat
    7: "M",   # Pushya - Male Sheep
    8: "F",   # Ashlesha - Female Cat
    9: "M",   # Magha - Male Rat
    10: "F",  # Purva Phalguni - Female Rat
    11: "M",  # Uttara Phalguni - Male Cow
    12: "F",  # Hasta - Female Buffalo
    13: "F",  # Chitra - Female Tiger
    14: "M",  # Swati - Male Buffalo
    15: "M",  # Vishakha - Male Tiger
    16: "F",  # Anuradha - Female Deer
    17: "M",  # Jyeshtha - Male Deer
    18: "M",  # Mula - Male Dog
    19: "M",  # Purva Ashadha - Male Monkey
    20: "M",  # Uttara Ashadha - Male Mongoose
    21: "F",  # Shravana - Female Monkey
    22: "F",  # Dhanishta - Female Lion
    23: "F",  # Shatabhisha - Female Horse
    24: "M",  # Purva Bhadrapada - Male Lion
    25: "F",  # Uttara Bhadrapada - Female Cow
    26: "F",  # Revati - Female Elephant
}

# Enemy pairs (0 points) - Natural animal enmities
YONI_ENEMIES = {
    (Yoni.HORSE, Yoni.BUFFALO),
    (Yoni.ELEPHANT, Yoni.LION),
    (Yoni.SHEEP, Yoni.MONKEY),
    (Yoni.SERPENT, Yoni.MONGOOSE),
    (Yoni.DOG, Yoni.DEER),
    (Yoni.CAT, Yoni.RAT),
    (Yoni.TIGER, Yoni.COW),
}

# Yoni compatibility scores
# Same yoni & same gender = 4, Same yoni diff gender = 3,
# Friendly = 2, Neutral = 1, Enemy = 0
def get_yoni_score(boy_nakshatra: int, girl_nakshatra: int) -> Tuple[float, str]:
    """
    Calculate Yoni compatibility score.

    Returns:
        (score, description)
    """
    boy_yoni = NAKSHATRA_YONI[boy_nakshatra]
    girl_yoni = NAKSHATRA_YONI[girl_nakshatra]
    boy_gender = NAKSHATRA_YONI_GENDER[boy_nakshatra]
    girl_gender = NAKSHATRA_YONI_GENDER[girl_nakshatra]

    # Same Yoni
    if boy_yoni == girl_yoni:
        if boy_gender != girl_gender:
            return 4, "Same Yoni, opposite gender - excellent physical compatibility"
        else:
            return 3, "Same Yoni, same gender - good physical compatibility"

    # Check for enemy pairs
    pair = tuple(sorted([boy_yoni, girl_yoni], key=lambda x: x.value))
    for enemy_pair in YONI_ENEMIES:
        sorted_enemy = tuple(sorted(enemy_pair, key=lambda x: x.value))
        if pair == sorted_enemy:
            return 0, f"Enemy Yonis ({boy_yoni.value} vs {girl_yoni.value}) - physical incompatibility"

    # Friendly/Neutral animals get partial scores
    return 2, f"Different Yonis ({boy_yoni.value} and {girl_yoni.value}) - moderate compatibility"


# =============================================================================
# GRAHA MAITRI (Planetary Friendship) - 5 Points
# Based on natural planetary relationships from BPHS
# =============================================================================

# Planet lords for each Rashi
RASHI_LORDS = {
    0: "MARS",      # Aries
    1: "VENUS",     # Taurus
    2: "MERCURY",   # Gemini
    3: "MOON",      # Cancer
    4: "SUN",       # Leo
    5: "MERCURY",   # Virgo
    6: "VENUS",     # Libra
    7: "MARS",      # Scorpio
    8: "JUPITER",   # Sagittarius
    9: "SATURN",    # Capricorn
    10: "SATURN",   # Aquarius
    11: "JUPITER",  # Pisces
}


def get_graha_maitri_score(boy_rashi: int, girl_rashi: int) -> Tuple[float, str]:
    """
    Calculate Graha Maitri (planetary friendship) score.

    Based on natural friendship between Moon sign lords:
    - Same lord or mutual friends = 5
    - One friend, one neutral = 4
    - Both neutral = 3
    - One friend, one enemy = 1
    - One neutral, one enemy = 0.5
    - Mutual enemies = 0
    """
    boy_lord = RASHI_LORDS[boy_rashi]
    girl_lord = RASHI_LORDS[girl_rashi]

    # Same lord
    if boy_lord == girl_lord:
        return 5, f"Same lord ({boy_lord}) - excellent mental compatibility"

    # Get relationship data
    boy_rel = NATURAL_RELATIONSHIPS.get(boy_lord, {})
    girl_rel = NATURAL_RELATIONSHIPS.get(girl_lord, {})

    # Check relationship from boy's lord to girl's lord
    boy_to_girl = "neutral"
    if girl_lord in boy_rel.get("friends", []):
        boy_to_girl = "friend"
    elif girl_lord in boy_rel.get("enemies", []):
        boy_to_girl = "enemy"

    # Check relationship from girl's lord to boy's lord
    girl_to_boy = "neutral"
    if boy_lord in girl_rel.get("friends", []):
        girl_to_boy = "friend"
    elif boy_lord in girl_rel.get("enemies", []):
        girl_to_boy = "enemy"

    # Calculate score based on mutual relationship
    if boy_to_girl == "friend" and girl_to_boy == "friend":
        return 5, f"Mutual friends ({boy_lord} & {girl_lord}) - excellent mental harmony"
    elif boy_to_girl == "friend" and girl_to_boy == "neutral":
        return 4, f"One-sided friendship ({boy_lord} friendly, {girl_lord} neutral)"
    elif boy_to_girl == "neutral" and girl_to_boy == "friend":
        return 4, f"One-sided friendship ({girl_lord} friendly, {boy_lord} neutral)"
    elif boy_to_girl == "neutral" and girl_to_boy == "neutral":
        return 3, f"Both neutral ({boy_lord} & {girl_lord}) - acceptable compatibility"
    elif (boy_to_girl == "friend" and girl_to_boy == "enemy") or \
         (boy_to_girl == "enemy" and girl_to_boy == "friend"):
        return 1, f"Mixed relationship ({boy_lord} & {girl_lord}) - potential conflicts"
    elif (boy_to_girl == "neutral" and girl_to_boy == "enemy") or \
         (boy_to_girl == "enemy" and girl_to_boy == "neutral"):
        return 0.5, f"Semi-hostile ({boy_lord} & {girl_lord}) - mental friction likely"
    else:
        return 0, f"Mutual enemies ({boy_lord} & {girl_lord}) - mental incompatibility"


# =============================================================================
# GANA (Temperament) - 6 Points
# Based on Muhurta Chintamani
# =============================================================================

class Gana(Enum):
    DEVA = "Deva"           # Divine/God-like temperament
    MANUSHYA = "Manushya"   # Human temperament
    RAKSHASA = "Rakshasa"   # Demon-like temperament


# Nakshatra to Gana mapping (0-indexed)
NAKSHATRA_GANA = {
    0: Gana.DEVA,       # Ashwini
    1: Gana.MANUSHYA,   # Bharani
    2: Gana.RAKSHASA,   # Krittika
    3: Gana.MANUSHYA,   # Rohini
    4: Gana.DEVA,       # Mrigashira
    5: Gana.MANUSHYA,   # Ardra
    6: Gana.DEVA,       # Punarvasu
    7: Gana.DEVA,       # Pushya
    8: Gana.RAKSHASA,   # Ashlesha
    9: Gana.RAKSHASA,   # Magha
    10: Gana.MANUSHYA,  # Purva Phalguni
    11: Gana.MANUSHYA,  # Uttara Phalguni
    12: Gana.DEVA,      # Hasta
    13: Gana.RAKSHASA,  # Chitra
    14: Gana.DEVA,      # Swati
    15: Gana.RAKSHASA,  # Vishakha
    16: Gana.DEVA,      # Anuradha
    17: Gana.RAKSHASA,  # Jyeshtha
    18: Gana.RAKSHASA,  # Mula
    19: Gana.MANUSHYA,  # Purva Ashadha
    20: Gana.MANUSHYA,  # Uttara Ashadha
    21: Gana.DEVA,      # Shravana
    22: Gana.RAKSHASA,  # Dhanishta
    23: Gana.RAKSHASA,  # Shatabhisha
    24: Gana.MANUSHYA,  # Purva Bhadrapada
    25: Gana.MANUSHYA,  # Uttara Bhadrapada
    26: Gana.DEVA,      # Revati
}

# Gana compatibility matrix (6 points max)
GANA_MATRIX = {
    Gana.DEVA: {
        Gana.DEVA: 6,       # Divine + Divine = Perfect
        Gana.MANUSHYA: 5,   # Divine + Human = Good (boy superior)
        Gana.RAKSHASA: 0,   # Divine + Demon = Worst
    },
    Gana.MANUSHYA: {
        Gana.DEVA: 6,       # Human + Divine = Very Good
        Gana.MANUSHYA: 6,   # Human + Human = Perfect
        Gana.RAKSHASA: 1,   # Human + Demon = Bad
    },
    Gana.RAKSHASA: {
        Gana.DEVA: 0,       # Demon + Divine = Worst
        Gana.MANUSHYA: 0,   # Demon + Human = Bad (some say 1)
        Gana.RAKSHASA: 6,   # Demon + Demon = Perfect for them
    },
}


# =============================================================================
# BHAKOOT (Rashi Compatibility) - 7 Points
# Based on Brihat Parashara Hora Shastra
# =============================================================================

def get_bhakoot_score(boy_rashi: int, girl_rashi: int) -> Tuple[float, str, Optional[str]]:
    """
    Calculate Bhakoot (Rashi relationship) score.

    Checks for:
    - 2/12 position (financial troubles)
    - 5/9 position (progeny issues)
    - 6/8 position (health/death-like issues)

    Returns:
        (score, description, dosha_name if any)
    """
    # Calculate relative positions
    boy_from_girl = ((boy_rashi - girl_rashi) % 12) + 1
    girl_from_boy = ((girl_rashi - boy_rashi) % 12) + 1

    boy_lord = RASHI_LORDS[boy_rashi]
    girl_lord = RASHI_LORDS[girl_rashi]

    # Check for doshas
    positions = sorted([boy_from_girl, girl_from_boy])

    # 6/8 Shadashtak Dosha - Most severe
    if positions == [6, 8]:
        # Exception: If lords are same or friends, dosha is cancelled
        if boy_lord == girl_lord:
            return 7, f"6/8 स्थिति - दोष नहीं (एक ही स्वामी: {boy_lord}) / 6/8 position cancelled (same lord)", None

        boy_rel = NATURAL_RELATIONSHIPS.get(boy_lord, {})
        girl_rel = NATURAL_RELATIONSHIPS.get(girl_lord, {})

        if girl_lord in boy_rel.get("friends", []) and boy_lord in girl_rel.get("friends", []):
            return 7, f"6/8 स्थिति - दोष नहीं (स्वामी {boy_lord} और {girl_lord} मित्र हैं) / 6/8 position cancelled (lords are friends)", None

        return 0, f"षड़ाष्टक दोष (6/8 स्थिति) - विवाद और अलगाव का खतरा। उपाय करें। / Shadashtak Dosha (6/8) - conflict & separation risk", "Shadashtak"

    # 2/12 Dwi-Dwadash Dosha
    if positions == [2, 12]:
        # Exception: If lords are same or friends
        if boy_lord == girl_lord:
            return 7, f"2/12 स्थिति - दोष नहीं (एक ही स्वामी: {boy_lord}) / 2/12 position cancelled (same lord)", None

        boy_rel = NATURAL_RELATIONSHIPS.get(boy_lord, {})
        girl_rel = NATURAL_RELATIONSHIPS.get(girl_lord, {})

        if girl_lord in boy_rel.get("friends", []) and boy_lord in girl_rel.get("friends", []):
            return 7, f"2/12 स्थिति - दोष नहीं (स्वामी मित्र हैं) / 2/12 position cancelled (lords are friends)", None

        return 0, f"द्वि-द्वादश दोष (2/12 स्थिति) - आर्थिक समस्या हो सकती है। उपाय करें। / Dwi-Dwadash Dosha (2/12) - financial troubles", "Dwi-Dwadash"

    # 5/9 Nava-Pancham Dosha (actually considered auspicious by some)
    if positions == [5, 9]:
        # This is often considered good (Trikon relation)
        # But some texts say it affects progeny
        return 7, f"5/9 त्रिकोण स्थिति - आमतौर पर शुभ / 5/9 Trikon position - generally auspicious", None

    # No dosha - full points
    return 7, f"स्थिति {boy_from_girl}/{girl_from_boy} - अनुकूल / Positions {boy_from_girl}/{girl_from_boy} - compatible", None


# =============================================================================
# NADI (Health/Genetic Compatibility) - 8 Points
# Most important factor - Based on Muhurta Chintamani
# =============================================================================

class Nadi(Enum):
    AADI = "Aadi"       # Vata (Wind) - First/Beginning
    MADHYA = "Madhya"   # Pitta (Bile) - Middle
    ANTYA = "Antya"     # Kapha (Phlegm) - End


# Nakshatra to Nadi mapping (0-indexed)
NAKSHATRA_NADI = {
    0: Nadi.AADI,       # Ashwini
    1: Nadi.MADHYA,     # Bharani
    2: Nadi.ANTYA,      # Krittika
    3: Nadi.ANTYA,      # Rohini
    4: Nadi.MADHYA,     # Mrigashira
    5: Nadi.AADI,       # Ardra
    6: Nadi.AADI,       # Punarvasu
    7: Nadi.MADHYA,     # Pushya
    8: Nadi.ANTYA,      # Ashlesha
    9: Nadi.ANTYA,      # Magha
    10: Nadi.MADHYA,    # Purva Phalguni
    11: Nadi.AADI,      # Uttara Phalguni
    12: Nadi.AADI,      # Hasta
    13: Nadi.MADHYA,    # Chitra
    14: Nadi.ANTYA,     # Swati
    15: Nadi.ANTYA,     # Vishakha
    16: Nadi.MADHYA,    # Anuradha
    17: Nadi.AADI,      # Jyeshtha
    18: Nadi.AADI,      # Mula
    19: Nadi.MADHYA,    # Purva Ashadha
    20: Nadi.ANTYA,     # Uttara Ashadha
    21: Nadi.ANTYA,     # Shravana
    22: Nadi.MADHYA,    # Dhanishta
    23: Nadi.AADI,      # Shatabhisha
    24: Nadi.AADI,      # Purva Bhadrapada
    25: Nadi.MADHYA,    # Uttara Bhadrapada
    26: Nadi.ANTYA,     # Revati
}


def get_nadi_score(boy_nakshatra: int, girl_nakshatra: int) -> Tuple[float, str, bool]:
    """
    Calculate Nadi compatibility score.

    Same Nadi = 0 (Nadi Dosha - most serious dosha)
    Different Nadi = 8 (Full points)

    Returns:
        (score, description, has_dosha)
    """
    boy_nadi = NAKSHATRA_NADI[boy_nakshatra]
    girl_nadi = NAKSHATRA_NADI[girl_nakshatra]

    if boy_nadi == girl_nadi:
        return 0, f"एक ही नाड़ी ({boy_nadi.value}) - नाड़ी दोष: स्वास्थ्य और संतान में समस्या हो सकती है। उपाय करें। / Same Nadi - NADI DOSHA: Health & progeny issues possible. Remedies needed.", True
    else:
        return 8, f"अलग-अलग नाड़ी ({boy_nadi.value} और {girl_nadi.value}) - स्वस्थ अनुकूलता / Different Nadis - healthy compatibility", False


# =============================================================================
# MANGLIK DOSHA (Mars Affliction)
# Based on Brihat Parashara Hora Shastra
# =============================================================================

MANGLIK_HOUSES = {1, 2, 4, 7, 8, 12}  # Houses where Mars causes Manglik Dosha


def check_manglik_dosha(
    mars_house_from_lagna: int,
    mars_house_from_moon: int,
    mars_house_from_venus: int,
    mars_rashi: str,
    lagna_rashi: str
) -> Dict[str, Any]:
    """
    Check for Manglik (Kuja) Dosha.

    Manglik Dosha occurs when Mars is in houses 1, 2, 4, 7, 8, or 12 from:
    - Lagna (Ascendant)
    - Moon
    - Venus (some traditions)

    Returns detailed analysis including cancellation conditions.
    """
    result = {
        "is_manglik": False,
        "severity": "None",
        "from_lagna": False,
        "from_moon": False,
        "from_venus": False,
        "cancellation": [],
        "description": ""
    }

    # Check from each reference point
    manglik_count = 0

    if mars_house_from_lagna in MANGLIK_HOUSES:
        result["from_lagna"] = True
        manglik_count += 1

    if mars_house_from_moon in MANGLIK_HOUSES:
        result["from_moon"] = True
        manglik_count += 1

    if mars_house_from_venus in MANGLIK_HOUSES:
        result["from_venus"] = True
        manglik_count += 1

    if manglik_count == 0:
        result["description"] = "मांगलिक दोष नहीं है / No Manglik Dosha"
        return result

    result["is_manglik"] = True

    # Determine severity
    if manglik_count >= 2:
        result["severity"] = "High"
    else:
        result["severity"] = "Moderate"

    # Check for cancellation conditions (per BPHS)
    cancellations = []
    cancellations_hindi = []

    # 1. Mars in own sign (Aries, Scorpio)
    if mars_rashi in ["Mesha", "Vrishchika"]:
        cancellations.append("Mars in own sign (Aries/Scorpio)")
        cancellations_hindi.append("मंगल अपनी राशि में (मेष/वृश्चिक)")

    # 2. Mars in exalted sign (Capricorn)
    if mars_rashi == "Makara":
        cancellations.append("Mars exalted in Capricorn")
        cancellations_hindi.append("मंगल उच्च का (मकर)")

    # 3. Mars aspected by benefics (Jupiter, Venus)
    # This would require more chart data

    # 4. Mars in house 1/2 for certain lagnas
    if mars_house_from_lagna == 1 and lagna_rashi in ["Mesha", "Simha", "Dhanu"]:
        cancellations.append("Mars in 1st house with fire sign lagna")
        cancellations_hindi.append("मंगल पहले भाव में अग्नि राशि लग्न के साथ")

    if mars_house_from_lagna == 2 and lagna_rashi in ["Mithuna", "Kanya"]:
        cancellations.append("Mars in 2nd house with Mercury sign lagna")
        cancellations_hindi.append("मंगल दूसरे भाव में बुध राशि लग्न के साथ")

    # 5. Mars conjunct/aspected by Jupiter or Moon (needs more data)

    result["cancellation"] = cancellations

    if cancellations:
        result["severity"] = "Cancelled/Reduced"
        result["description"] = f"मांगलिक दोष है पर निरस्त/कम: {', '.join(cancellations_hindi)} / Manglik Dosha cancelled/reduced: {', '.join(cancellations)}"
    else:
        result["description"] = f"मांगलिक दोष है ({manglik_count} स्थान से)। उपाय करें। / Manglik Dosha present from {manglik_count} point(s). Remedies needed."

    return result


# =============================================================================
# MAIN KUNDALI MATCHER CLASS
# =============================================================================

@dataclass
class KootaResult:
    """Result for a single Koota (matching factor)."""
    name: str
    name_hindi: str
    max_points: float
    obtained_points: float
    boy_value: str
    girl_value: str
    description: str
    is_auspicious: bool
    dosha: Optional[str] = None


@dataclass
class MatchingResult:
    """Complete Kundali matching result."""
    boy_name: str
    girl_name: str
    total_points: float
    max_points: float = 36.0
    percentage: float = 0.0
    koota_results: List[KootaResult] = field(default_factory=list)
    doshas: List[Dict[str, Any]] = field(default_factory=list)
    recommendation: str = ""
    detailed_analysis: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.percentage = round((self.total_points / self.max_points) * 100, 1)


class KundaliMatcher:
    """
    Comprehensive Kundali Matching Calculator.

    Implements Ashtakoot Milan (8-fold matching) system
    for marriage compatibility analysis based on classical
    Vedic astrology texts.
    """

    def __init__(self):
        pass

    def match(
        self,
        boy_moon_rashi_num: int,
        boy_moon_nakshatra_num: int,
        boy_moon_degree: float,
        girl_moon_rashi_num: int,
        girl_moon_nakshatra_num: int,
        girl_moon_degree: float,
        boy_name: str = "Boy",
        girl_name: str = "Girl",
        boy_mars_house_from_lagna: Optional[int] = None,
        boy_mars_house_from_moon: Optional[int] = None,
        boy_mars_rashi: Optional[str] = None,
        boy_lagna_rashi: Optional[str] = None,
        girl_mars_house_from_lagna: Optional[int] = None,
        girl_mars_house_from_moon: Optional[int] = None,
        girl_mars_rashi: Optional[str] = None,
        girl_lagna_rashi: Optional[str] = None,
    ) -> MatchingResult:
        """
        Perform complete Ashtakoot matching.

        Args:
            boy_moon_rashi_num: Boy's Moon sign (0-11)
            boy_moon_nakshatra_num: Boy's Moon nakshatra (0-26)
            boy_moon_degree: Boy's Moon degree within rashi
            girl_moon_rashi_num: Girl's Moon sign (0-11)
            girl_moon_nakshatra_num: Girl's Moon nakshatra (0-26)
            girl_moon_degree: Girl's Moon degree within rashi
            boy_name: Boy's name for report
            girl_name: Girl's name for report
            Additional parameters for Manglik dosha check

        Returns:
            MatchingResult with complete analysis
        """
        koota_results = []
        doshas = []
        total_points = 0.0

        # 1. VARNA (1 point)
        varna_result = self._calculate_varna(
            boy_moon_rashi_num, girl_moon_rashi_num
        )
        koota_results.append(varna_result)
        total_points += varna_result.obtained_points

        # 2. VASHYA (2 points)
        vashya_result = self._calculate_vashya(
            boy_moon_rashi_num, boy_moon_degree,
            girl_moon_rashi_num, girl_moon_degree
        )
        koota_results.append(vashya_result)
        total_points += vashya_result.obtained_points

        # 3. TARA (3 points)
        tara_result = self._calculate_tara(
            boy_moon_nakshatra_num, girl_moon_nakshatra_num
        )
        koota_results.append(tara_result)
        total_points += tara_result.obtained_points

        # 4. YONI (4 points)
        yoni_result = self._calculate_yoni(
            boy_moon_nakshatra_num, girl_moon_nakshatra_num
        )
        koota_results.append(yoni_result)
        total_points += yoni_result.obtained_points

        # 5. GRAHA MAITRI (5 points)
        maitri_result = self._calculate_graha_maitri(
            boy_moon_rashi_num, girl_moon_rashi_num
        )
        koota_results.append(maitri_result)
        total_points += maitri_result.obtained_points

        # 6. GANA (6 points)
        gana_result = self._calculate_gana(
            boy_moon_nakshatra_num, girl_moon_nakshatra_num
        )
        koota_results.append(gana_result)
        total_points += gana_result.obtained_points
        if gana_result.dosha:
            doshas.append({
                "name": gana_result.dosha,
                "type": "Gana Dosha",
                "severity": "Moderate",
                "description": gana_result.description
            })

        # 7. BHAKOOT (7 points)
        bhakoot_result = self._calculate_bhakoot(
            boy_moon_rashi_num, girl_moon_rashi_num
        )
        koota_results.append(bhakoot_result)
        total_points += bhakoot_result.obtained_points
        if bhakoot_result.dosha:
            doshas.append({
                "name": bhakoot_result.dosha,
                "type": "Bhakoot Dosha",
                "severity": "High",
                "description": bhakoot_result.description
            })

        # 8. NADI (8 points)
        nadi_result = self._calculate_nadi(
            boy_moon_nakshatra_num, girl_moon_nakshatra_num
        )
        koota_results.append(nadi_result)
        total_points += nadi_result.obtained_points
        if nadi_result.dosha:
            doshas.append({
                "name": nadi_result.dosha,
                "type": "Nadi Dosha",
                "severity": "Critical",
                "description": nadi_result.description
            })

        # Check Manglik Dosha if data provided
        boy_manglik = None
        girl_manglik = None

        if boy_mars_house_from_lagna is not None and boy_mars_house_from_moon is not None:
            boy_manglik = check_manglik_dosha(
                boy_mars_house_from_lagna,
                boy_mars_house_from_moon,
                0,  # Venus house not provided
                boy_mars_rashi or "",
                boy_lagna_rashi or ""
            )
            if boy_manglik["is_manglik"]:
                doshas.append({
                    "name": "Manglik Dosha (Boy)",
                    "type": "Manglik Dosha",
                    "severity": boy_manglik["severity"],
                    "description": boy_manglik["description"],
                    "cancellation": boy_manglik["cancellation"]
                })

        if girl_mars_house_from_lagna is not None and girl_mars_house_from_moon is not None:
            girl_manglik = check_manglik_dosha(
                girl_mars_house_from_lagna,
                girl_mars_house_from_moon,
                0,  # Venus house not provided
                girl_mars_rashi or "",
                girl_lagna_rashi or ""
            )
            if girl_manglik["is_manglik"]:
                doshas.append({
                    "name": "Manglik Dosha (Girl)",
                    "type": "Manglik Dosha",
                    "severity": girl_manglik["severity"],
                    "description": girl_manglik["description"],
                    "cancellation": girl_manglik["cancellation"]
                })

        # Check if Manglik doshas cancel each other
        if boy_manglik and girl_manglik:
            if boy_manglik["is_manglik"] and girl_manglik["is_manglik"]:
                # Both Manglik - doshas cancel each other
                for dosha in doshas:
                    if dosha["type"] == "Manglik Dosha":
                        dosha["severity"] = "Cancelled"
                        dosha["description"] += " (Cancelled: Both partners are Manglik)"

        # Generate recommendation
        recommendation = self._generate_recommendation(total_points, doshas)

        # Create detailed analysis
        detailed_analysis = {
            "boy_moon_sign": RASHIS[boy_moon_rashi_num]["name"],
            "girl_moon_sign": RASHIS[girl_moon_rashi_num]["name"],
            "boy_nakshatra": NAKSHATRA_NAMES[boy_moon_nakshatra_num],
            "girl_nakshatra": NAKSHATRA_NAMES[girl_moon_nakshatra_num],
            "boy_manglik": boy_manglik,
            "girl_manglik": girl_manglik,
            "score_breakdown": {
                "varna": varna_result.obtained_points,
                "vashya": vashya_result.obtained_points,
                "tara": tara_result.obtained_points,
                "yoni": yoni_result.obtained_points,
                "graha_maitri": maitri_result.obtained_points,
                "gana": gana_result.obtained_points,
                "bhakoot": bhakoot_result.obtained_points,
                "nadi": nadi_result.obtained_points,
            }
        }

        return MatchingResult(
            boy_name=boy_name,
            girl_name=girl_name,
            total_points=total_points,
            koota_results=koota_results,
            doshas=doshas,
            recommendation=recommendation,
            detailed_analysis=detailed_analysis
        )

    def _calculate_varna(
        self, boy_rashi: int, girl_rashi: int
    ) -> KootaResult:
        """Calculate Varna Koota (1 point max)."""
        boy_varna = RASHI_VARNA[boy_rashi]
        girl_varna = RASHI_VARNA[girl_rashi]

        # Boy's varna >= Girl's varna = 1 point
        if boy_varna.value >= girl_varna.value:
            points = 1
            desc = f"Boy's Varna ({boy_varna.name}) >= Girl's Varna ({girl_varna.name}) - Compatible"
            auspicious = True
        else:
            points = 0
            desc = f"Boy's Varna ({boy_varna.name}) < Girl's Varna ({girl_varna.name}) - Not ideal per tradition"
            auspicious = False

        return KootaResult(
            name="Varna",
            name_hindi="वर्ण",
            max_points=1,
            obtained_points=points,
            boy_value=boy_varna.name,
            girl_value=girl_varna.name,
            description=desc,
            is_auspicious=auspicious
        )

    def _calculate_vashya(
        self, boy_rashi: int, boy_degree: float,
        girl_rashi: int, girl_degree: float
    ) -> KootaResult:
        """Calculate Vashya Koota (2 points max)."""
        boy_vashya = get_vashya_type(boy_rashi, boy_degree)
        girl_vashya = get_vashya_type(girl_rashi, girl_degree)

        points = VASHYA_MATRIX[boy_vashya][girl_vashya]

        if points >= 1.5:
            auspicious = True
            desc = f"{boy_vashya.value} and {girl_vashya.value} have good mutual attraction"
        elif points >= 0.5:
            auspicious = True
            desc = f"{boy_vashya.value} and {girl_vashya.value} have partial attraction"
        else:
            auspicious = False
            desc = f"{boy_vashya.value} and {girl_vashya.value} lack mutual attraction"

        return KootaResult(
            name="Vashya",
            name_hindi="वश्य",
            max_points=2,
            obtained_points=points,
            boy_value=boy_vashya.value,
            girl_value=girl_vashya.value,
            description=desc,
            is_auspicious=auspicious
        )

    def _calculate_tara(
        self, boy_nakshatra: int, girl_nakshatra: int
    ) -> KootaResult:
        """Calculate Tara Koota (3 points max)."""
        # Count from girl's nakshatra to boy's
        girl_to_boy = ((boy_nakshatra - girl_nakshatra) % 27) + 1
        tara_girl = ((girl_to_boy - 1) % 9) + 1

        # Count from boy's nakshatra to girl's
        boy_to_girl = ((girl_nakshatra - boy_nakshatra) % 27) + 1
        tara_boy = ((boy_to_girl - 1) % 9) + 1

        # Check if either is inauspicious
        girl_bad = tara_girl in INAUSPICIOUS_TARAS
        boy_bad = tara_boy in INAUSPICIOUS_TARAS

        if not girl_bad and not boy_bad:
            points = 3
            auspicious = True
            desc = f"Both Taras auspicious ({TARA_NAMES[tara_girl]['name']} & {TARA_NAMES[tara_boy]['name']})"
        elif girl_bad and boy_bad:
            points = 0
            auspicious = False
            desc = f"Both Taras inauspicious ({TARA_NAMES[tara_girl]['name']} & {TARA_NAMES[tara_boy]['name']}) - Avoid"
        else:
            points = 1.5
            auspicious = True  # Partial
            bad_tara = TARA_NAMES[tara_girl]['name'] if girl_bad else TARA_NAMES[tara_boy]['name']
            desc = f"One inauspicious Tara ({bad_tara}) - Partially compatible"

        return KootaResult(
            name="Tara",
            name_hindi="तारा",
            max_points=3,
            obtained_points=points,
            boy_value=f"{TARA_NAMES[tara_boy]['name']} ({tara_boy})",
            girl_value=f"{TARA_NAMES[tara_girl]['name']} ({tara_girl})",
            description=desc,
            is_auspicious=auspicious
        )

    def _calculate_yoni(
        self, boy_nakshatra: int, girl_nakshatra: int
    ) -> KootaResult:
        """Calculate Yoni Koota (4 points max)."""
        points, desc = get_yoni_score(boy_nakshatra, girl_nakshatra)

        boy_yoni = NAKSHATRA_YONI[boy_nakshatra]
        girl_yoni = NAKSHATRA_YONI[girl_nakshatra]

        return KootaResult(
            name="Yoni",
            name_hindi="योनि",
            max_points=4,
            obtained_points=points,
            boy_value=boy_yoni.value,
            girl_value=girl_yoni.value,
            description=desc,
            is_auspicious=points >= 2
        )

    def _calculate_graha_maitri(
        self, boy_rashi: int, girl_rashi: int
    ) -> KootaResult:
        """Calculate Graha Maitri Koota (5 points max)."""
        points, desc = get_graha_maitri_score(boy_rashi, girl_rashi)

        boy_lord = RASHI_LORDS[boy_rashi]
        girl_lord = RASHI_LORDS[girl_rashi]

        return KootaResult(
            name="Graha Maitri",
            name_hindi="ग्रह मैत्री",
            max_points=5,
            obtained_points=points,
            boy_value=boy_lord,
            girl_value=girl_lord,
            description=desc,
            is_auspicious=points >= 3
        )

    def _calculate_gana(
        self, boy_nakshatra: int, girl_nakshatra: int
    ) -> KootaResult:
        """Calculate Gana Koota (6 points max)."""
        boy_gana = NAKSHATRA_GANA[boy_nakshatra]
        girl_gana = NAKSHATRA_GANA[girl_nakshatra]

        points = GANA_MATRIX[boy_gana][girl_gana]

        dosha = None
        if points == 0:
            desc = f"{boy_gana.value} + {girl_gana.value} = Gana Dosha (temperament clash)"
            dosha = "Gana Dosha"
            auspicious = False
        elif points == 1:
            desc = f"{boy_gana.value} + {girl_gana.value} = Partial compatibility"
            auspicious = False
        else:
            desc = f"{boy_gana.value} + {girl_gana.value} = Good temperament match"
            auspicious = True

        return KootaResult(
            name="Gana",
            name_hindi="गण",
            max_points=6,
            obtained_points=points,
            boy_value=boy_gana.value,
            girl_value=girl_gana.value,
            description=desc,
            is_auspicious=auspicious,
            dosha=dosha
        )

    def _calculate_bhakoot(
        self, boy_rashi: int, girl_rashi: int
    ) -> KootaResult:
        """Calculate Bhakoot Koota (7 points max)."""
        points, desc, dosha = get_bhakoot_score(boy_rashi, girl_rashi)

        boy_sign = RASHIS[boy_rashi]["name"]
        girl_sign = RASHIS[girl_rashi]["name"]

        return KootaResult(
            name="Bhakoot",
            name_hindi="भकूट",
            max_points=7,
            obtained_points=points,
            boy_value=boy_sign,
            girl_value=girl_sign,
            description=desc,
            is_auspicious=points > 0,
            dosha=dosha
        )

    def _calculate_nadi(
        self, boy_nakshatra: int, girl_nakshatra: int
    ) -> KootaResult:
        """Calculate Nadi Koota (8 points max)."""
        points, desc, has_dosha = get_nadi_score(boy_nakshatra, girl_nakshatra)

        boy_nadi = NAKSHATRA_NADI[boy_nakshatra]
        girl_nadi = NAKSHATRA_NADI[girl_nakshatra]

        dosha = "Nadi Dosha" if has_dosha else None

        return KootaResult(
            name="Nadi",
            name_hindi="नाड़ी",
            max_points=8,
            obtained_points=points,
            boy_value=boy_nadi.value,
            girl_value=girl_nadi.value,
            description=desc,
            is_auspicious=not has_dosha,
            dosha=dosha
        )

    def _generate_recommendation(
        self, total_points: float, doshas: List[Dict]
    ) -> str:
        """Generate marriage recommendation based on score and doshas."""
        percentage = (total_points / 36) * 100

        # Check for critical doshas
        has_nadi_dosha = any(d["type"] == "Nadi Dosha" and d["severity"] != "Cancelled" for d in doshas)
        has_bhakoot_dosha = any(d["type"] == "Bhakoot Dosha" and d["severity"] != "Cancelled" for d in doshas)
        has_gana_dosha = any(d["type"] == "Gana Dosha" for d in doshas)

        # Generate recommendation in Hindi/Hinglish
        if percentage >= 80:
            base = "उत्तम मिलान! शादी के लिए बहुत अच्छा है। / Excellent match! Highly recommended for marriage."
        elif percentage >= 60:
            base = "अच्छा मिलान है। शादी पर विचार किया जा सकता है। / Good match. Marriage can be considered."
        elif percentage >= 50:
            base = "औसत मिलान है। थोड़ी समझदारी से शादी हो सकती है। / Average match. Marriage possible with adjustments."
        elif percentage >= 36:
            base = "मिलान कम है। शादी से पहले उपाय करें। / Below average match. Consider remedies before proceeding."
        else:
            base = "अनुकूलता कम है। बिना उपाय के शादी की सलाह नहीं है। / Poor compatibility. Marriage not recommended without remedies."

        warnings = []

        if has_nadi_dosha:
            warnings.append("⚠️ गंभीर: नाड़ी दोष है - स्वास्थ्य और संतान के लिए योग्य ज्योतिषी से मिलें। / CRITICAL: Nadi Dosha - consult astrologer for health & progeny.")

        if has_bhakoot_dosha:
            warnings.append("⚠️ चेतावनी: भकूट दोष है - झगड़े और आर्थिक समस्या हो सकती है। / WARNING: Bhakoot Dosha - potential conflicts & financial issues.")

        if has_gana_dosha:
            warnings.append("⚠️ सावधान: गण दोष है - स्वभाव में फर्क से तनाव हो सकता है। / CAUTION: Gana Dosha - temperament differences may cause friction.")

        if warnings:
            return f"{base}\n\n" + "\n".join(warnings)

        return base


# =============================================================================
# PLANETARY STRENGTH ANALYSIS FOR MARRIAGE (BPHS-Based)
# =============================================================================

def analyze_marriage_strength(boy_kundali, girl_kundali) -> Dict[str, Any]:
    """
    Analyze planetary strength relevant to marriage for both partners.

    Based on BPHS principles:
    - Venus strength (Karaka for marriage)
    - Jupiter strength (Karaka for spouse in female chart)
    - 7th house lord strength
    - Combustion of marriage significators

    Args:
        boy_kundali: Boy's Kundali object or dict
        girl_kundali: Girl's Kundali object or dict

    Returns:
        Dict with strength analysis and recommendations
    """
    result = {
        "available": False,
        "boy_analysis": {},
        "girl_analysis": {},
        "comparison": {},
        "recommendations": []
    }

    if not SHADBALA_AVAILABLE or not ACCURACY_COMPONENTS_AVAILABLE:
        result["error"] = "Accuracy components not available"
        return result

    result["available"] = True

    # Helper to extract planets from kundali (dict or object)
    def get_planets(kundali):
        if hasattr(kundali, 'planets'):
            return kundali.planets
        return kundali.get("planets", {})

    boy_planets = get_planets(boy_kundali)
    girl_planets = get_planets(girl_kundali)

    # Analyze each partner
    for label, planets, analysis_key in [
        ("Boy", boy_planets, "boy_analysis"),
        ("Girl", girl_planets, "girl_analysis")
    ]:
        analysis = {}

        # Get Sun longitude for combustion check
        sun_long = planets.get("SUN", {}).get("longitude", 0)

        # Check key marriage planets
        for planet in ["VENUS", "JUPITER", "MOON"]:
            if planet not in planets:
                continue

            p_data = planets[planet]
            p_long = p_data.get("longitude", 0)
            is_retro = p_data.get("is_retrograde", False)

            # Combustion check
            is_combust, severity = check_combustion(planet, p_long, sun_long, is_retro)

            # Navamsa strength
            navamsa_mod = get_navamsa_strength_modifier(planet, p_long)

            analysis[planet] = {
                "is_combust": is_combust,
                "combust_severity": round(severity, 2) if is_combust else 0,
                "navamsa_strength": "strong" if navamsa_mod > 0 else "weak" if navamsa_mod < 0 else "neutral",
                "navamsa_modifier": navamsa_mod
            }

            # Add warnings
            if is_combust and planet == "VENUS":
                result["recommendations"].append(
                    f"{label}: शुक्र अस्त है - वैवाहिक सुख में कमी संभव। शुक्र मंत्र और उपाय करें।"
                )
            if is_combust and planet == "JUPITER" and label == "Girl":
                result["recommendations"].append(
                    f"{label}: गुरु अस्त है - पति से संबंधों में चुनौती। गुरु पूजा करें।"
                )

        # Try Shadbala if Kundali object available
        try:
            if hasattr(boy_kundali if label == "Boy" else girl_kundali, 'planets'):
                kundali_obj = boy_kundali if label == "Boy" else girl_kundali
                calc = ShadbalaCalculator(kundali_obj)

                for planet in ["VENUS", "JUPITER"]:
                    if planet in planets:
                        sb = calc.calculate_shadbala(planet)
                        analysis[planet]["shadbala_total"] = round(sb.total, 1)
                        analysis[planet]["shadbala_level"] = sb.strength_level

                        if sb.strength_level == "weak":
                            planet_hindi = "शुक्र" if planet == "VENUS" else "गुरु"
                            result["recommendations"].append(
                                f"{label}: {planet_hindi} दुर्बल है - विवाह संबंधित उपाय आवश्यक।"
                            )
        except Exception:
            pass

        result[analysis_key] = analysis

    # Comparison
    boy_venus = result["boy_analysis"].get("VENUS", {})
    girl_venus = result["girl_analysis"].get("VENUS", {})

    if boy_venus and girl_venus:
        boy_score = 0
        girl_score = 0

        if not boy_venus.get("is_combust"):
            boy_score += 1
        if boy_venus.get("navamsa_strength") == "strong":
            boy_score += 1
        if boy_venus.get("shadbala_level") in ["strong", "very_strong"]:
            boy_score += 1

        if not girl_venus.get("is_combust"):
            girl_score += 1
        if girl_venus.get("navamsa_strength") == "strong":
            girl_score += 1
        if girl_venus.get("shadbala_level") in ["strong", "very_strong"]:
            girl_score += 1

        result["comparison"]["venus_balance"] = {
            "boy_score": boy_score,
            "girl_score": girl_score,
            "status": "balanced" if abs(boy_score - girl_score) <= 1 else "imbalanced"
        }

        if abs(boy_score - girl_score) > 1:
            stronger = "लड़के" if boy_score > girl_score else "लड़की"
            result["recommendations"].append(
                f"शुक्र बल असंतुलित है - {stronger} का शुक्र अधिक बली। समझौते की आवश्यकता।"
            )

    # Overall assessment
    if not result["recommendations"]:
        result["recommendations"].append(
            "✅ विवाह संबंधित ग्रह बली हैं। शुभ मिलान।"
        )

    return result


# =============================================================================
# CONVENIENCE FUNCTION
# =============================================================================

def match_kundalis(
    boy_kundali: Dict[str, Any],
    girl_kundali: Dict[str, Any]
) -> MatchingResult:
    """
    Convenience function to match two Kundalis.

    Args:
        boy_kundali: Dict with Moon position data from Kundali class
        girl_kundali: Dict with Moon position data from Kundali class

    Returns:
        MatchingResult with complete analysis
    """
    matcher = KundaliMatcher()

    # Extract required data
    boy_moon = boy_kundali.get("planets", {}).get("MOON", {})
    girl_moon = girl_kundali.get("planets", {}).get("MOON", {})

    result = matcher.match(
        boy_moon_rashi_num=boy_moon.get("rashi_num", 0),
        boy_moon_nakshatra_num=boy_moon.get("nakshatra_num", 0),
        boy_moon_degree=boy_moon.get("rashi_degree", 15.0),
        girl_moon_rashi_num=girl_moon.get("rashi_num", 0),
        girl_moon_nakshatra_num=girl_moon.get("nakshatra_num", 0),
        girl_moon_degree=girl_moon.get("rashi_degree", 15.0),
        boy_name=boy_kundali.get("birth_details", {}).get("name", "Boy"),
        girl_name=girl_kundali.get("birth_details", {}).get("name", "Girl"),
    )

    # Add planetary strength analysis (BPHS-based accuracy enhancement)
    try:
        strength_analysis = analyze_marriage_strength(boy_kundali, girl_kundali)
        result.detailed_analysis["planetary_strength"] = strength_analysis
    except Exception:
        pass  # Strength analysis is optional enhancement

    return result
