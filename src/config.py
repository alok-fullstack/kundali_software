"""
Configuration and constants for Vedic Astrology calculations
"""

from enum import Enum
from typing import Dict, List, Tuple

# Ayanamsa - Lahiri is most widely used in India (Government of India standard)
AYANAMSA_LAHIRI = 1  # Swiss Ephemeris constant for Lahiri

# 12 Rashis (Zodiac Signs) with their lords
RASHIS: Dict[int, Dict] = {
    0: {"name": "Mesha", "english": "Aries", "lord": "Mars", "element": "Fire", "symbol": "♈"},
    1: {"name": "Vrishabha", "english": "Taurus", "lord": "Venus", "element": "Earth", "symbol": "♉"},
    2: {"name": "Mithuna", "english": "Gemini", "lord": "Mercury", "element": "Air", "symbol": "♊"},
    3: {"name": "Karka", "english": "Cancer", "lord": "Moon", "element": "Water", "symbol": "♋"},
    4: {"name": "Simha", "english": "Leo", "lord": "Sun", "element": "Fire", "symbol": "♌"},
    5: {"name": "Kanya", "english": "Virgo", "lord": "Mercury", "element": "Earth", "symbol": "♍"},
    6: {"name": "Tula", "english": "Libra", "lord": "Venus", "element": "Air", "symbol": "♎"},
    7: {"name": "Vrishchika", "english": "Scorpio", "lord": "Mars", "element": "Water", "symbol": "♏"},
    8: {"name": "Dhanu", "english": "Sagittarius", "lord": "Jupiter", "element": "Fire", "symbol": "♐"},
    9: {"name": "Makara", "english": "Capricorn", "lord": "Saturn", "element": "Earth", "symbol": "♑"},
    10: {"name": "Kumbha", "english": "Aquarius", "lord": "Saturn", "element": "Air", "symbol": "♒"},
    11: {"name": "Meena", "english": "Pisces", "lord": "Jupiter", "element": "Water", "symbol": "♓"},
}

# 27 Nakshatras with their lords and degrees
NAKSHATRAS: List[Dict] = [
    {"name": "Ashwini", "lord": "Ketu", "start": 0.0, "deity": "Ashwini Kumaras"},
    {"name": "Bharani", "lord": "Venus", "start": 13.333333, "deity": "Yama"},
    {"name": "Krittika", "lord": "Sun", "start": 26.666667, "deity": "Agni"},
    {"name": "Rohini", "lord": "Moon", "start": 40.0, "deity": "Brahma"},
    {"name": "Mrigashira", "lord": "Mars", "start": 53.333333, "deity": "Soma"},
    {"name": "Ardra", "lord": "Rahu", "start": 66.666667, "deity": "Rudra"},
    {"name": "Punarvasu", "lord": "Jupiter", "start": 80.0, "deity": "Aditi"},
    {"name": "Pushya", "lord": "Saturn", "start": 93.333333, "deity": "Brihaspati"},
    {"name": "Ashlesha", "lord": "Mercury", "start": 106.666667, "deity": "Sarpa"},
    {"name": "Magha", "lord": "Ketu", "start": 120.0, "deity": "Pitris"},
    {"name": "Purva Phalguni", "lord": "Venus", "start": 133.333333, "deity": "Bhaga"},
    {"name": "Uttara Phalguni", "lord": "Sun", "start": 146.666667, "deity": "Aryaman"},
    {"name": "Hasta", "lord": "Moon", "start": 160.0, "deity": "Savitar"},
    {"name": "Chitra", "lord": "Mars", "start": 173.333333, "deity": "Vishwakarma"},
    {"name": "Swati", "lord": "Rahu", "start": 186.666667, "deity": "Vayu"},
    {"name": "Vishakha", "lord": "Jupiter", "start": 200.0, "deity": "Indra-Agni"},
    {"name": "Anuradha", "lord": "Saturn", "start": 213.333333, "deity": "Mitra"},
    {"name": "Jyeshtha", "lord": "Mercury", "start": 226.666667, "deity": "Indra"},
    {"name": "Mula", "lord": "Ketu", "start": 240.0, "deity": "Nirriti"},
    {"name": "Purva Ashadha", "lord": "Venus", "start": 253.333333, "deity": "Apas"},
    {"name": "Uttara Ashadha", "lord": "Sun", "start": 266.666667, "deity": "Vishvadevas"},
    {"name": "Shravana", "lord": "Moon", "start": 280.0, "deity": "Vishnu"},
    {"name": "Dhanishta", "lord": "Mars", "start": 293.333333, "deity": "Vasus"},
    {"name": "Shatabhisha", "lord": "Rahu", "start": 306.666667, "deity": "Varuna"},
    {"name": "Purva Bhadrapada", "lord": "Jupiter", "start": 320.0, "deity": "Aja Ekapada"},
    {"name": "Uttara Bhadrapada", "lord": "Saturn", "start": 333.333333, "deity": "Ahir Budhnya"},
    {"name": "Revati", "lord": "Mercury", "start": 346.666667, "deity": "Pushan"},
]

# Nakshatra span in degrees (exact calculation)
NAKSHATRA_SPAN = 360.0 / 27  # Exact: 13.333333... degrees

# Pada span in degrees (each nakshatra has 4 padas)
PADA_SPAN = 360.0 / 108  # Exact: 3.333333... degrees (27 nakshatras * 4 padas)

# Planets (Grahas) - Swiss Ephemeris constants
class Planet(Enum):
    SUN = 0
    MOON = 1
    MARS = 4
    MERCURY = 2
    JUPITER = 5
    VENUS = 3
    SATURN = 6
    RAHU = 11  # Mean Node (True Node = 10)
    KETU = -1  # Calculated as 180° from Rahu

PLANET_NAMES: Dict[Planet, Dict] = {
    Planet.SUN: {"sanskrit": "Surya", "hindi": "सूर्य", "symbol": "☉"},
    Planet.MOON: {"sanskrit": "Chandra", "hindi": "चंद्र", "symbol": "☽"},
    Planet.MARS: {"sanskrit": "Mangal", "hindi": "मंगल", "symbol": "♂"},
    Planet.MERCURY: {"sanskrit": "Budha", "hindi": "बुध", "symbol": "☿"},
    Planet.JUPITER: {"sanskrit": "Guru", "hindi": "गुरु", "symbol": "♃"},
    Planet.VENUS: {"sanskrit": "Shukra", "hindi": "शुक्र", "symbol": "♀"},
    Planet.SATURN: {"sanskrit": "Shani", "hindi": "शनि", "symbol": "♄"},
    Planet.RAHU: {"sanskrit": "Rahu", "hindi": "राहु", "symbol": "☊"},
    Planet.KETU: {"sanskrit": "Ketu", "hindi": "केतु", "symbol": "☋"},
}

# Vimshottari Dasha periods (in years)
VIMSHOTTARI_YEARS: Dict[str, int] = {
    "Ketu": 7,
    "Venus": 20,
    "Sun": 6,
    "Moon": 10,
    "Mars": 7,
    "Rahu": 18,
    "Jupiter": 16,
    "Saturn": 19,
    "Mercury": 17,
}

# Dasha sequence
DASHA_SEQUENCE: List[str] = [
    "Ketu", "Venus", "Sun", "Moon", "Mars",
    "Rahu", "Jupiter", "Saturn", "Mercury"
]

# Total Vimshottari cycle = 120 years
VIMSHOTTARI_TOTAL_YEARS = 120

# 12 Bhavas (Houses)
BHAVA_NAMES: Dict[int, Dict] = {
    1: {"name": "Lagna", "significance": "Self, personality, physical body"},
    2: {"name": "Dhana", "significance": "Wealth, family, speech"},
    3: {"name": "Sahaja", "significance": "Siblings, courage, communication"},
    4: {"name": "Sukha", "significance": "Mother, home, happiness, vehicles"},
    5: {"name": "Putra", "significance": "Children, intelligence, creativity"},
    6: {"name": "Ari", "significance": "Enemies, diseases, debts"},
    7: {"name": "Yuvati", "significance": "Marriage, partnerships, spouse"},
    8: {"name": "Randhra", "significance": "Longevity, obstacles, transformation"},
    9: {"name": "Dharma", "significance": "Fortune, father, religion"},
    10: {"name": "Karma", "significance": "Career, profession, status"},
    11: {"name": "Labha", "significance": "Gains, income, elder siblings"},
    12: {"name": "Vyaya", "significance": "Losses, expenses, liberation"},
}

# Default location (Delhi, India)
DEFAULT_LOCATION = {
    "city": "Delhi",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "timezone": "Asia/Kolkata"
}

# =============================================================================
# PLANET DIGNITIES (Exaltation, Debilitation, Own Signs, Mooltrikona)
# =============================================================================
PLANET_DIGNITIES = {
    "SUN": {"own": ["Simha"], "exalted": "Mesha", "debilitated": "Tula", "mooltrikona": "Simha"},
    "MOON": {"own": ["Karka"], "exalted": "Vrishabha", "debilitated": "Vrishchika", "mooltrikona": "Vrishabha"},
    "MARS": {"own": ["Mesha", "Vrishchika"], "exalted": "Makara", "debilitated": "Karka", "mooltrikona": "Mesha"},
    "MERCURY": {"own": ["Mithuna", "Kanya"], "exalted": "Kanya", "debilitated": "Meena", "mooltrikona": "Kanya"},
    "JUPITER": {"own": ["Dhanu", "Meena"], "exalted": "Karka", "debilitated": "Makara", "mooltrikona": "Dhanu"},
    "VENUS": {"own": ["Vrishabha", "Tula"], "exalted": "Meena", "debilitated": "Kanya", "mooltrikona": "Tula"},
    "SATURN": {"own": ["Makara", "Kumbha"], "exalted": "Tula", "debilitated": "Mesha", "mooltrikona": "Kumbha"},
    "RAHU": {"own": ["Kumbha"], "exalted": "Vrishabha", "debilitated": "Vrishchika", "mooltrikona": "Kanya"},
    "KETU": {"own": ["Vrishchika"], "exalted": "Vrishchika", "debilitated": "Vrishabha", "mooltrikona": "Dhanu"},
}

# =============================================================================
# ACCURACY ENHANCEMENT CONSTANTS (Per BPHS)
# =============================================================================

# COMBUSTION (Asta) - Orbs in degrees when planet is too close to Sun
# Per BPHS Chapter 25: Combust planets lose their strength
COMBUSTION_ORBS = {
    "MOON": 12,       # Within 12° of Sun
    "MARS": 17,       # Within 17° of Sun
    "MERCURY": 14,    # Within 14° (12° when retrograde)
    "JUPITER": 11,    # Within 11° of Sun
    "VENUS": 10,      # Within 10° (8° when retrograde)
    "SATURN": 15,     # Within 15° of Sun
}

# NAISARGIKA BALA (Natural Strength) - Fixed values per BPHS Chapter 27
# Scale: 0-60 Shashtiamsas (sixtieths of a Rupa)
NAISARGIKA_BALA = {
    "SUN": 60.0,
    "MOON": 51.43,
    "VENUS": 42.85,
    "JUPITER": 34.28,
    "MERCURY": 25.71,
    "MARS": 17.14,
    "SATURN": 8.57,
}

# DIG BALA (Directional Strength) - Optimal houses per BPHS
# Planet gets full 60 points when in this house, 0 in opposite house
DIG_BALA_HOUSES = {
    "SUN": 10,      # Strong in 10th (Karma bhava)
    "MARS": 10,     # Strong in 10th
    "MOON": 4,      # Strong in 4th (Sukha bhava)
    "VENUS": 4,     # Strong in 4th
    "MERCURY": 1,   # Strong in 1st (Lagna)
    "JUPITER": 1,   # Strong in 1st
    "SATURN": 7,    # Strong in 7th (Kama bhava)
}

# TARA BALA (Nakshatra Strength) - 9-fold cycle from birth nakshatra
# Per Muhurta Chintamani and BPHS
TARABALA_EFFECTS = {
    1: {"name": "Janma", "name_hi": "जन्म", "modifier": -0.30, "favorable": False},      # Birth star - challenging
    2: {"name": "Sampat", "name_hi": "संपत्", "modifier": +0.20, "favorable": True},     # Wealth - good
    3: {"name": "Vipat", "name_hi": "विपत्", "modifier": -0.20, "favorable": False},     # Danger - avoid
    4: {"name": "Kshema", "name_hi": "क्षेम", "modifier": +0.15, "favorable": True},     # Welfare - good
    5: {"name": "Pratyak", "name_hi": "प्रत्यक्", "modifier": -0.15, "favorable": False}, # Obstacles
    6: {"name": "Sadhana", "name_hi": "साधन", "modifier": +0.10, "favorable": True},     # Achievement
    7: {"name": "Naidhana", "name_hi": "निधन", "modifier": -0.25, "favorable": False},   # Death star - worst
    8: {"name": "Mitra", "name_hi": "मित्र", "modifier": +0.15, "favorable": True},      # Friend - good
    9: {"name": "Parama Mitra", "name_hi": "परम मित्र", "modifier": +0.25, "favorable": True},  # Best friend - best
}

# EXALTATION DEGREES (Exact degrees where planet is at peak strength)
# Used for calculating Uchcha Bala in Shadbala
EXALTATION_DEGREES = {
    "SUN": 10,       # 10° Aries
    "MOON": 33,      # 3° Taurus (33° from 0° Aries)
    "MARS": 298,     # 28° Capricorn
    "MERCURY": 165,  # 15° Virgo
    "JUPITER": 95,   # 5° Cancer
    "VENUS": 357,    # 27° Pisces
    "SATURN": 200,   # 20° Libra
}

# =============================================================================
# HOUSE LORDSHIPS (Which houses each planet rules for each lagna)
# =============================================================================
HOUSE_LORDSHIPS = {
    "Mesha": {"SUN": [5], "MOON": [4], "MARS": [1,8], "MERCURY": [3,6], "JUPITER": [9,12], "VENUS": [2,7], "SATURN": [10,11]},
    "Vrishabha": {"SUN": [4], "MOON": [3], "MARS": [7,12], "MERCURY": [2,5], "JUPITER": [8,11], "VENUS": [1,6], "SATURN": [9,10]},
    "Mithuna": {"SUN": [3], "MOON": [2], "MARS": [6,11], "MERCURY": [1,4], "JUPITER": [7,10], "VENUS": [5,12], "SATURN": [8,9]},
    "Karka": {"SUN": [2], "MOON": [1], "MARS": [5,10], "MERCURY": [3,12], "JUPITER": [6,9], "VENUS": [4,11], "SATURN": [7,8]},
    "Simha": {"SUN": [1], "MOON": [12], "MARS": [4,9], "MERCURY": [2,11], "JUPITER": [5,8], "VENUS": [3,10], "SATURN": [6,7]},
    "Kanya": {"SUN": [12], "MOON": [11], "MARS": [3,8], "MERCURY": [1,10], "JUPITER": [4,7], "VENUS": [2,9], "SATURN": [5,6]},
    "Tula": {"SUN": [11], "MOON": [10], "MARS": [2,7], "MERCURY": [9,12], "JUPITER": [3,6], "VENUS": [1,8], "SATURN": [4,5]},
    "Vrishchika": {"SUN": [10], "MOON": [9], "MARS": [1,6], "MERCURY": [8,11], "JUPITER": [2,5], "VENUS": [7,12], "SATURN": [3,4]},
    "Dhanu": {"SUN": [9], "MOON": [8], "MARS": [5,12], "MERCURY": [7,10], "JUPITER": [1,4], "VENUS": [6,11], "SATURN": [2,3]},
    "Makara": {"SUN": [8], "MOON": [7], "MARS": [4,11], "MERCURY": [6,9], "JUPITER": [3,12], "VENUS": [5,10], "SATURN": [1,2]},
    "Kumbha": {"SUN": [7], "MOON": [6], "MARS": [3,10], "MERCURY": [5,8], "JUPITER": [2,11], "VENUS": [4,9], "SATURN": [1,12]},
    "Meena": {"SUN": [6], "MOON": [5], "MARS": [2,9], "MERCURY": [4,7], "JUPITER": [1,10], "VENUS": [3,8], "SATURN": [11,12]},
}

# =============================================================================
# FUNCTIONAL BENEFICS AND MALEFICS (per Lagna)
# =============================================================================
FUNCTIONAL_BENEFICS = {
    # Based on BPHS: Trikona lords (5,9) always benefic, Lagna lord benefic
    # Kendra lords neutral, Dusthana lords (6,8,12) malefic
    "Mesha": ["SUN", "MOON", "JUPITER", "MARS"],  # Sun=5th, Moon=4th(Kendra), Jupiter=9th, Mars=1st
    "Vrishabha": ["SUN", "MERCURY", "SATURN"],  # Sun=4th(neutral-benefic), Mercury=5th, Saturn=9th+10th(Yogakaraka)
    "Mithuna": ["VENUS", "SATURN", "MERCURY"],  # Venus=5th, Saturn=9th, Mercury=1st+4th (FIXED: added Mercury as Lagna lord)
    "Karka": ["MOON", "MARS", "JUPITER"],  # Moon=1st, Mars=5th+10th(Yogakaraka), Jupiter=9th
    "Simha": ["SUN", "MARS", "JUPITER"],  # Sun=1st, Mars=4th+9th(Yogakaraka), Jupiter=5th
    "Kanya": ["MERCURY", "VENUS"],  # Mercury=1st+10th, Venus=9th
    "Tula": ["VENUS", "SATURN"],  # Venus=1st, Saturn=4th+5th(Yogakaraka) (FIXED: removed Mercury - 12th is Mooltrikona)
    "Vrishchika": ["MOON", "SUN", "JUPITER", "MARS"],  # Moon=9th, Sun=10th(neutral), Jupiter=5th, Mars=1st (FIXED: added Mars as Lagna lord)
    "Dhanu": ["SUN", "MARS", "JUPITER"],  # Sun=9th, Mars=5th, Jupiter=1st+4th
    "Makara": ["VENUS", "MERCURY", "SATURN"],  # Venus=5th+10th(Yogakaraka), Mercury=9th, Saturn=1st
    "Kumbha": ["VENUS", "SUN", "SATURN"],  # Venus=4th+9th(Yogakaraka), Sun=7th(neutral), Saturn=1st
    "Meena": ["MOON", "MARS", "JUPITER"],  # Moon=5th, Mars=9th, Jupiter=1st+10th
}

FUNCTIONAL_MALEFICS = {
    # Based on BPHS: Dusthana lords (6,8,12) malefic, 3rd/11th lords malefic
    # Maraka lords (2,7) can be malefic, especially if also ruling dusthana
    "Mesha": ["MERCURY", "VENUS", "SATURN"],  # Mercury=3rd+6th, Venus=2nd+7th, Saturn=10th+11th
    "Vrishabha": ["MARS", "JUPITER", "VENUS", "MOON"],  # Mars=7th+12th, Jupiter=8th+11th, Venus=6th, Moon=3rd (FIXED: added Moon)
    "Mithuna": ["MARS", "SUN"],  # Mars=6th+11th, Sun=3rd
    "Karka": ["MERCURY", "VENUS", "SATURN"],  # Mercury=3rd+12th, Venus=4th+11th, Saturn=7th+8th
    "Simha": ["MOON", "MERCURY", "VENUS", "SATURN"],  # Moon=12th, Mercury=2nd+11th, Venus=3rd+10th, Saturn=6th+7th
    "Kanya": ["MARS", "MOON", "JUPITER", "SUN"],  # Mars=3rd+8th, Moon=11th, Jupiter=4th+7th(neutral), Sun=12th (FIXED: added Sun)
    "Tula": ["SUN", "MARS", "JUPITER"],  # Sun=11th, Mars=2nd+7th(double Maraka), Jupiter=3rd+6th
    "Vrishchika": ["MERCURY", "VENUS", "SATURN"],  # Mercury=8th+11th, Venus=7th+12th, Saturn=3rd+4th (FIXED: added Saturn)
    "Dhanu": ["VENUS", "SATURN", "MERCURY", "MOON"],  # Venus=6th+11th, Saturn=2nd+3rd, Mercury=7th+10th(neutral), Moon=8th (FIXED: added Moon)
    "Makara": ["MARS", "MOON", "JUPITER", "SUN"],  # Mars=4th+11th, Moon=7th, Jupiter=3rd+12th, Sun=8th (FIXED: added Sun)
    "Kumbha": ["MOON", "MARS", "JUPITER"],  # Moon=6th, Mars=3rd+10th, Jupiter=2nd+11th
    "Meena": ["SUN", "VENUS", "SATURN"],  # Sun=6th, Venus=3rd+8th, Saturn=11th+12th (FIXED: removed Mercury - Kendradhipatya only)
}

YOGAKARAKA = {
    "Mesha": None,
    "Vrishabha": "SATURN",
    "Mithuna": None,
    "Karka": "MARS",  # 5th + 10th lord
    "Simha": "MARS",  # 4th + 9th lord
    "Kanya": None,
    "Tula": "SATURN",  # 4th + 5th lord
    "Vrishchika": None,
    "Dhanu": None,
    "Makara": "VENUS",  # 5th + 10th lord
    "Kumbha": "VENUS",  # 4th + 9th lord
    "Meena": None,
}

# =============================================================================
# NATURAL RELATIONSHIPS (Planet Friendships)
# =============================================================================
NATURAL_RELATIONSHIPS = {
    "SUN": {"friends": ["MOON", "MARS", "JUPITER"], "enemies": ["VENUS", "SATURN"], "neutral": ["MERCURY"]},
    "MOON": {"friends": ["SUN", "MERCURY"], "enemies": [], "neutral": ["MARS", "JUPITER", "VENUS", "SATURN"]},
    "MARS": {"friends": ["SUN", "MOON", "JUPITER"], "enemies": ["MERCURY"], "neutral": ["VENUS", "SATURN"]},
    "MERCURY": {"friends": ["SUN", "VENUS"], "enemies": ["MOON"], "neutral": ["MARS", "JUPITER", "SATURN"]},
    "JUPITER": {"friends": ["SUN", "MOON", "MARS"], "enemies": ["MERCURY", "VENUS"], "neutral": ["SATURN"]},
    "VENUS": {"friends": ["MERCURY", "SATURN"], "enemies": ["SUN", "MOON"], "neutral": ["MARS", "JUPITER"]},
    "SATURN": {"friends": ["MERCURY", "VENUS"], "enemies": ["SUN", "MOON", "MARS"], "neutral": ["JUPITER"]},
    "RAHU": {"friends": ["VENUS", "SATURN"], "enemies": ["SUN", "MOON", "MARS"], "neutral": ["MERCURY", "JUPITER"]},
    "KETU": {"friends": ["MARS", "JUPITER"], "enemies": ["VENUS", "SATURN"], "neutral": ["SUN", "MOON", "MERCURY"]},
}

# =============================================================================
# HOUSE CLASSIFICATION CONSTANTS
# =============================================================================
KENDRA_HOUSES = [1, 4, 7, 10]  # Angular houses
TRIKONA_HOUSES = [1, 5, 9]     # Trine houses
DUSTHANA_HOUSES = [6, 8, 12]   # Malefic houses
UPACHAYA_HOUSES = [3, 6, 10, 11]  # Growth houses
MARAKA_HOUSES = [2, 7]         # Death-inflicting houses

# =============================================================================
# MUHURTA CONSTANTS (from Muhurta Chintamani, Brihat Samhita)
# =============================================================================

# 15 Tithis (lunar days) with lords - repeats for Shukla and Krishna Paksha
TITHIS = [
    {"num": 1, "name": "Pratipada", "hindi": "प्रतिपदा", "lord": "Sun"},
    {"num": 2, "name": "Dwitiya", "hindi": "द्वितीया", "lord": "Moon"},
    {"num": 3, "name": "Tritiya", "hindi": "तृतीया", "lord": "Mars"},
    {"num": 4, "name": "Chaturthi", "hindi": "चतुर्थी", "lord": "Mercury"},  # Rikta
    {"num": 5, "name": "Panchami", "hindi": "पंचमी", "lord": "Jupiter"},
    {"num": 6, "name": "Shashthi", "hindi": "षष्ठी", "lord": "Venus"},
    {"num": 7, "name": "Saptami", "hindi": "सप्तमी", "lord": "Saturn"},
    {"num": 8, "name": "Ashtami", "hindi": "अष्टमी", "lord": "Rahu"},
    {"num": 9, "name": "Navami", "hindi": "नवमी", "lord": "Sun"},  # Rikta
    {"num": 10, "name": "Dashami", "hindi": "दशमी", "lord": "Moon"},
    {"num": 11, "name": "Ekadashi", "hindi": "एकादशी", "lord": "Mars"},
    {"num": 12, "name": "Dwadashi", "hindi": "द्वादशी", "lord": "Mercury"},
    {"num": 13, "name": "Trayodashi", "hindi": "त्रयोदशी", "lord": "Jupiter"},
    {"num": 14, "name": "Chaturdashi", "hindi": "चतुर्दशी", "lord": "Venus"},  # Rikta
    {"num": 15, "name": "Purnima", "hindi": "पूर्णिमा", "lord": "Saturn"},  # Full Moon
    {"num": 30, "name": "Amavasya", "hindi": "अमावस्या", "lord": "Saturn"},  # New Moon
]

# Rikta (inauspicious) Tithis - 4th, 9th, 14th of each paksha
RIKTA_TITHIS = [4, 9, 14]

# 27 Yogas (Sun-Moon combinations) from Brihat Samhita
YOGAS_27 = [
    {"num": 1, "name": "Vishkumbha", "hindi": "विष्कुम्भ", "inauspicious": True},
    {"num": 2, "name": "Priti", "hindi": "प्रीति", "inauspicious": False},
    {"num": 3, "name": "Ayushman", "hindi": "आयुष्मान", "inauspicious": False},
    {"num": 4, "name": "Saubhagya", "hindi": "सौभाग्य", "inauspicious": False},
    {"num": 5, "name": "Shobhana", "hindi": "शोभन", "inauspicious": False},
    {"num": 6, "name": "Atiganda", "hindi": "अतिगण्ड", "inauspicious": True},
    {"num": 7, "name": "Sukarma", "hindi": "सुकर्मा", "inauspicious": False},
    {"num": 8, "name": "Dhriti", "hindi": "धृति", "inauspicious": False},
    {"num": 9, "name": "Shoola", "hindi": "शूल", "inauspicious": True},
    {"num": 10, "name": "Ganda", "hindi": "गण्ड", "inauspicious": True},
    {"num": 11, "name": "Vriddhi", "hindi": "वृद्धि", "inauspicious": False},
    {"num": 12, "name": "Dhruva", "hindi": "ध्रुव", "inauspicious": False},
    {"num": 13, "name": "Vyaghata", "hindi": "व्याघात", "inauspicious": True},
    {"num": 14, "name": "Harshana", "hindi": "हर्षण", "inauspicious": False},
    {"num": 15, "name": "Vajra", "hindi": "वज्र", "inauspicious": True},
    {"num": 16, "name": "Siddhi", "hindi": "सिद्धि", "inauspicious": False},
    {"num": 17, "name": "Vyatipata", "hindi": "व्यतीपात", "inauspicious": True},
    {"num": 18, "name": "Variyan", "hindi": "वरीयान", "inauspicious": False},
    {"num": 19, "name": "Parigha", "hindi": "परिघ", "inauspicious": True},
    {"num": 20, "name": "Shiva", "hindi": "शिव", "inauspicious": False},
    {"num": 21, "name": "Siddha", "hindi": "सिद्ध", "inauspicious": False},
    {"num": 22, "name": "Sadhya", "hindi": "साध्य", "inauspicious": False},
    {"num": 23, "name": "Shubha", "hindi": "शुभ", "inauspicious": False},
    {"num": 24, "name": "Shukla", "hindi": "शुक्ल", "inauspicious": False},
    {"num": 25, "name": "Brahma", "hindi": "ब्रह्म", "inauspicious": False},
    {"num": 26, "name": "Indra", "hindi": "इन्द्र", "inauspicious": False},
    {"num": 27, "name": "Vaidhriti", "hindi": "वैधृति", "inauspicious": True},
]

# Inauspicious Yoga indices (0-based)
INAUSPICIOUS_YOGAS = [0, 5, 8, 9, 12, 14, 16, 18, 26]

# 11 Karanas (half-tithis)
KARANAS = [
    {"num": 1, "name": "Bava", "hindi": "बव", "type": "Chara", "auspicious": True},
    {"num": 2, "name": "Balava", "hindi": "बालव", "type": "Chara", "auspicious": True},
    {"num": 3, "name": "Kaulava", "hindi": "कौलव", "type": "Chara", "auspicious": True},
    {"num": 4, "name": "Taitila", "hindi": "तैतिल", "type": "Chara", "auspicious": True},
    {"num": 5, "name": "Gara", "hindi": "गर", "type": "Chara", "auspicious": True},
    {"num": 6, "name": "Vanija", "hindi": "वणिज", "type": "Chara", "auspicious": True},
    {"num": 7, "name": "Vishti", "hindi": "विष्टि", "type": "Chara", "auspicious": False},  # Bhadra
    {"num": 8, "name": "Shakuni", "hindi": "शकुनि", "type": "Sthira", "auspicious": False},
    {"num": 9, "name": "Chatushpada", "hindi": "चतुष्पद", "type": "Sthira", "auspicious": False},
    {"num": 10, "name": "Naga", "hindi": "नाग", "type": "Sthira", "auspicious": False},
    {"num": 11, "name": "Kimstughna", "hindi": "किंस्तुघ्न", "type": "Sthira", "auspicious": True},
]

# 7 Varas (weekdays) with planetary rulers
VARAS = [
    {"num": 0, "name": "Ravivara", "hindi": "रविवार", "english": "Sunday", "lord": "Sun"},
    {"num": 1, "name": "Somavara", "hindi": "सोमवार", "english": "Monday", "lord": "Moon"},
    {"num": 2, "name": "Mangalavara", "hindi": "मंगलवार", "english": "Tuesday", "lord": "Mars"},
    {"num": 3, "name": "Budhavara", "hindi": "बुधवार", "english": "Wednesday", "lord": "Mercury"},
    {"num": 4, "name": "Guruvara", "hindi": "गुरुवार", "english": "Thursday", "lord": "Jupiter"},
    {"num": 5, "name": "Shukravara", "hindi": "शुक्रवार", "english": "Friday", "lord": "Venus"},
    {"num": 6, "name": "Shanivara", "hindi": "शनिवार", "english": "Saturday", "lord": "Saturn"},
]

# Rahu Kala sequence (which 1/8th part of day is Rahu Kala for each weekday)
# From Kalaprakashika - memorized as "Mother Saw Father Wearing The Turban on Saturday"
RAHU_KALA_SEQUENCE = {
    0: 8,  # Sunday - 8th part (4:30-6:00 PM equivalent)
    1: 2,  # Monday - 2nd part (7:30-9:00 AM)
    2: 7,  # Tuesday - 7th part (3:00-4:30 PM)
    3: 5,  # Wednesday - 5th part (12:00-1:30 PM)
    4: 6,  # Thursday - 6th part (1:30-3:00 PM)
    5: 4,  # Friday - 4th part (10:30-12:00 PM)
    6: 3,  # Saturday - 3rd part (9:00-10:30 AM)
}

# Yamaghantaka sequence (inauspicious period ruled by Yama)
YAMAGHANTAKA_SEQUENCE = {
    0: 5,  # Sunday
    1: 4,  # Monday
    2: 3,  # Tuesday
    3: 2,  # Wednesday
    4: 1,  # Thursday
    5: 7,  # Friday
    6: 6,  # Saturday
}

# Gulika Kala sequence (period of Gulika/Mandi - son of Saturn)
GULIKA_SEQUENCE = {
    0: 7,  # Sunday
    1: 6,  # Monday
    2: 5,  # Tuesday
    3: 4,  # Wednesday
    4: 3,  # Thursday
    5: 2,  # Friday
    6: 1,  # Saturday
}

# Nakshatra Classification for Muhurta (from Muhurta Chintamani)
NAKSHATRA_CLASSIFICATION = {
    # Fixed (Dhruva/Sthira) - good for permanent works, construction, property
    "Fixed": [3, 10, 11, 20, 24],  # Rohini, Uttara Phalguni, Hasta, Uttara Ashadha, Uttara Bhadrapada

    # Moveable (Chara) - good for travel, starting journeys
    "Moveable": [6, 7, 12, 16, 21, 26],  # Punarvasu, Pushya, Hasta, Anuradha, Shravana, Revati

    # Soft/Tender (Mridu) - good for arts, romance, music, pleasure
    "Soft": [4, 13, 14],  # Mrigashira, Chitra, Swati

    # Sharp/Fierce (Tikshna/Ugra) - good for surgery, competition, warfare
    "Sharp": [5, 8, 17, 18],  # Ardra, Ashlesha, Jyeshtha, Mula

    # Mixed (Mishra/Sadharana) - moderately good for various activities
    "Mixed": [2, 6, 15, 21],  # Krittika, Punarvasu, Vishakha, Shravana

    # Light/Swift (Kshipra/Laghu) - good for quick tasks, learning, travel
    "Light": [0, 6, 7, 12, 26],  # Ashwini, Punarvasu, Pushya, Hasta, Revati
}

# Tarabala (9-fold star strength cycle)
TARABALA_NAMES = {
    1: {"name": "Janma", "hindi": "जन्म", "effect": "Birth star - avoid", "score": 0},
    2: {"name": "Sampat", "hindi": "सम्पत्", "effect": "Wealth - favorable", "score": 10},
    3: {"name": "Vipat", "hindi": "विपत्", "effect": "Danger - avoid", "score": 0},
    4: {"name": "Kshema", "hindi": "क्षेम", "effect": "Prosperity - good", "score": 8},
    5: {"name": "Pratyak", "hindi": "प्रत्यक्", "effect": "Obstacles - avoid", "score": 0},
    6: {"name": "Sadhaka", "hindi": "साधक", "effect": "Achievement - very good", "score": 10},
    7: {"name": "Naidhana", "hindi": "नैधन", "effect": "Death/harm - avoid", "score": 0},
    8: {"name": "Mitra", "hindi": "मित्र", "effect": "Friend - good", "score": 8},
    9: {"name": "Paramamitra", "hindi": "परममित्र", "effect": "Best friend - excellent", "score": 10},
}

# Chandrabala (Moon transit houses) - favorable houses from natal Moon
CHANDRABALA_FAVORABLE_HOUSES = [1, 3, 6, 7, 10, 11]
CHANDRABALA_UNFAVORABLE_HOUSES = [4, 8, 12]

# =============================================================================
# EVENT-SPECIFIC MUHURTA RULES (from Muhurta Chintamani)
# =============================================================================

MARRIAGE_MUHURTA_RULES = {
    # Favorable nakshatras for marriage (0-indexed)
    "favorable_nakshatras": [3, 4, 9, 11, 12, 14, 16, 20, 24, 26],
    # Rohini(3), Mrigashira(4), Magha(9), Uttara Phalguni(11), Hasta(12),
    # Swati(14), Anuradha(16), Uttara Ashadha(20), Uttara Bhadrapada(24), Revati(26)

    # Unfavorable nakshatras (avoid completely or specific padas)
    "unfavorable_nakshatras": [1, 2, 5, 8, 17, 18],
    # Bharani(1), Krittika(2), Ardra(5), Ashlesha(8), Jyeshtha(17), Mula(18-1st pada)

    # Favorable tithis (1-based within paksha)
    "favorable_tithis": [2, 3, 5, 7, 10, 11, 12, 13],

    # Unfavorable tithis
    "unfavorable_tithis": [4, 9, 14, 30],  # Rikta tithis + Amavasya

    # Unfavorable yogas (0-indexed)
    "unfavorable_yogas": [0, 5, 8, 9, 12, 14, 16, 18, 26],
    # Vishkumbha, Atiganda, Shoola, Ganda, Vyaghata, Vajra, Vyatipata, Parigha, Vaidhriti

    # Favorable weekdays
    "favorable_weekdays": [1, 3, 4, 5],  # Monday, Wednesday, Thursday, Friday

    # Unfavorable weekdays
    "unfavorable_weekdays": [0, 2, 6],  # Sunday, Tuesday, Saturday

    # Shukla Paksha preferred
    "prefer_shukla_paksha": True,

    # Lunar months to avoid
    "avoid_months": ["Ashada", "Bhadrapada", "Pausha"],
}

CAREER_MUHURTA_RULES = {
    # Moveable and light nakshatras good for new ventures
    "favorable_nakshatras": [0, 6, 7, 12, 14, 21, 26],
    # Ashwini, Punarvasu, Pushya, Hasta, Swati, Shravana, Revati

    "unfavorable_nakshatras": [5, 8, 17, 18],  # Sharp nakshatras

    "favorable_tithis": [2, 3, 5, 6, 7, 10, 11, 12, 13],

    "unfavorable_tithis": [4, 9, 14, 30],

    "unfavorable_yogas": [0, 5, 8, 9, 12, 14, 16, 18, 26],

    "favorable_weekdays": [1, 3, 4, 5],  # Moon, Mercury, Jupiter, Venus days

    "unfavorable_weekdays": [2, 6],  # Tuesday, Saturday

    "prefer_shukla_paksha": True,
}

PROPERTY_MUHURTA_RULES = {
    # Fixed nakshatras good for property and permanent works
    "favorable_nakshatras": [3, 10, 11, 20, 24],
    # Rohini, Uttara Phalguni, Hasta, Uttara Ashadha, Uttara Bhadrapada

    # Avoid moveable nakshatras
    "unfavorable_nakshatras": [6, 7, 16, 17, 26],

    "favorable_tithis": [2, 3, 5, 7, 10, 11, 12, 13],

    "unfavorable_tithis": [4, 9, 14, 30],

    "unfavorable_yogas": [0, 5, 8, 9, 12, 14, 16, 18, 26],

    "favorable_weekdays": [1, 4, 5],  # Monday, Thursday, Friday

    "unfavorable_weekdays": [2, 6],  # Tuesday, Saturday

    "prefer_shukla_paksha": True,
}

GRIHA_PRAVESH_MUHURTA_RULES = {
    # House warming ceremony rules (similar to property but more specific)
    "favorable_nakshatras": [3, 6, 7, 11, 12, 20, 21, 24, 26],
    # Rohini, Punarvasu, Pushya, Uttara Phalguni, Hasta, Uttara Ashadha, Shravana,
    # Uttara Bhadrapada, Revati

    "unfavorable_nakshatras": [1, 2, 5, 8, 17, 18],

    "favorable_tithis": [2, 3, 5, 7, 10, 11, 12, 13],

    "unfavorable_tithis": [4, 6, 8, 9, 12, 14, 30],  # Also avoid 6, 8, 12

    "unfavorable_yogas": [0, 5, 8, 9, 12, 14, 16, 18, 26],

    "favorable_weekdays": [1, 3, 4, 5],

    "unfavorable_weekdays": [0, 2, 6],

    "prefer_shukla_paksha": True,

    # Sun should not be in 6th, 8th, 12th from lagna during griha pravesh
    "sun_avoid_houses": [6, 8, 12],
}

TRAVEL_MUHURTA_RULES = {
    # Moveable and light nakshatras good for travel
    "favorable_nakshatras": [0, 4, 6, 7, 12, 14, 21, 26],
    # Ashwini, Mrigashira, Punarvasu, Pushya, Hasta, Swati, Shravana, Revati

    "unfavorable_nakshatras": [1, 5, 8, 17, 18],

    "favorable_tithis": [2, 3, 5, 7, 10, 11, 13],

    "unfavorable_tithis": [4, 9, 14, 30],

    "unfavorable_yogas": [0, 5, 8, 9, 12, 14, 16, 18, 26],

    "favorable_weekdays": [1, 3, 4, 5],

    "unfavorable_weekdays": [2, 6],  # Avoid Tuesday, Saturday for travel

    "prefer_shukla_paksha": False,  # Both pakshas acceptable for travel
}

# =============================================================================
# RASHI LIST (for easy indexing in Ashtakavarga calculations)
# =============================================================================
RASHI_LIST = [
    "Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
    "Tula", "Vrishchika", "Dhanu", "Makara", "Kumbha", "Meena"
]

# Rashi Lords mapping
RASHI_LORDS = {
    "Mesha": "MARS", "Vrishabha": "VENUS", "Mithuna": "MERCURY",
    "Karka": "MOON", "Simha": "SUN", "Kanya": "MERCURY",
    "Tula": "VENUS", "Vrishchika": "MARS", "Dhanu": "JUPITER",
    "Makara": "SATURN", "Kumbha": "SATURN", "Meena": "JUPITER"
}

# =============================================================================
# GOCHAR (TRANSIT) EFFECTS - Per BPHS, Phaladeepika, Brihat Samhita
# =============================================================================

# Gochar Planet Effects for Rashifal (authentic Vedic transit effects)
# Format: planet -> {house_from_moon: {effect_type, intensity, keywords}}
GOCHAR_PLANET_EFFECTS = {
    "SATURN": {
        "favorable_houses": [3, 6, 11],
        "unfavorable_houses": [1, 2, 4, 7, 8, 10, 12],
        "mixed_houses": [5, 9],
        "transit_duration_days": 912,  # ~2.5 years
        "significance_weight": 1.0,  # Highest for yearly predictions
        "house_effects": {
            1: {"type": "ashubh", "intensity": 0.9, "keywords_hi": "स्वास्थ्य समस्या, विलंब, मानसिक तनाव"},
            2: {"type": "ashubh", "intensity": 0.7, "keywords_hi": "आर्थिक हानि, पारिवारिक कलह"},
            3: {"type": "shubh", "intensity": 0.85, "keywords_hi": "विजय, साहस, भाई-बहनों से लाभ"},
            4: {"type": "ashubh", "intensity": 0.75, "keywords_hi": "गृह कष्ट, माता की चिंता"},
            5: {"type": "mishra", "intensity": 0.5, "keywords_hi": "संतान चिंता, शिक्षा में बाधा"},
            6: {"type": "shubh", "intensity": 0.9, "keywords_hi": "शत्रु पराजय, स्वास्थ्य सुधार"},
            7: {"type": "ashubh", "intensity": 0.7, "keywords_hi": "वैवाहिक कलह, साझेदारी में समस्या"},
            8: {"type": "ashubh", "intensity": 0.95, "keywords_hi": "दीर्घ रोग, दुर्घटना, हानि"},
            9: {"type": "mishra", "intensity": 0.55, "keywords_hi": "पिता की चिंता, भाग्य में कमी"},
            10: {"type": "ashubh", "intensity": 0.8, "keywords_hi": "करियर में बाधा, पद हानि"},
            11: {"type": "shubh", "intensity": 1.0, "keywords_hi": "अधिकतम लाभ, इच्छा पूर्ति"},
            12: {"type": "ashubh", "intensity": 0.75, "keywords_hi": "व्यय, अस्पताल"},
        },
    },
    "JUPITER": {
        "favorable_houses": [2, 5, 7, 9, 11],
        "unfavorable_houses": [1, 3, 4, 6, 8, 10, 12],
        "mixed_houses": [],
        "transit_duration_days": 365,  # ~1 year
        "significance_weight": 0.95,
        "house_effects": {
            1: {"type": "mishra", "intensity": 0.5, "keywords_hi": "व्यय, यात्रा, निवास परिवर्तन"},
            2: {"type": "shubh", "intensity": 0.85, "keywords_hi": "धन लाभ, परिवार सुख"},
            3: {"type": "ashubh", "intensity": 0.6, "keywords_hi": "बाधाएं, भाई से हानि"},
            4: {"type": "ashubh", "intensity": 0.65, "keywords_hi": "सुख हानि, गृह कलह"},
            5: {"type": "shubh", "intensity": 0.95, "keywords_hi": "संतान सुख, शिक्षा सफलता"},
            6: {"type": "ashubh", "intensity": 0.7, "keywords_hi": "शत्रु वृद्धि, स्वास्थ्य समस्या"},
            7: {"type": "shubh", "intensity": 0.8, "keywords_hi": "विवाह, साझेदारी लाभ"},
            8: {"type": "ashubh", "intensity": 0.75, "keywords_hi": "कारावास, मानसिक कष्ट"},
            9: {"type": "shubh", "intensity": 1.0, "keywords_hi": "अधिकतम भाग्योदय, आध्यात्मिक उन्नति"},
            10: {"type": "ashubh", "intensity": 0.7, "keywords_hi": "पद हानि, करियर समस्या"},
            11: {"type": "shubh", "intensity": 1.0, "keywords_hi": "सर्वांगीण समृद्धि, लाभ"},
            12: {"type": "ashubh", "intensity": 0.65, "keywords_hi": "व्यय, मानसिक चिंता"},
        },
    },
    "MARS": {
        "favorable_houses": [3, 6, 11],
        "unfavorable_houses": [1, 2, 4, 5, 7, 8, 12],
        "mixed_houses": [9, 10],
        "transit_duration_days": 45,
        "significance_weight": 0.7,
        "house_effects": {
            1: {"type": "ashubh", "intensity": 0.8, "keywords_hi": "दुर्घटना, बुखार, कलह"},
            2: {"type": "ashubh", "intensity": 0.7, "keywords_hi": "आर्थिक हानि, कटु वाणी"},
            3: {"type": "shubh", "intensity": 0.9, "keywords_hi": "विजय, साहस, सफलता"},
            4: {"type": "ashubh", "intensity": 0.75, "keywords_hi": "गृह समस्या, संपत्ति विवाद"},
            5: {"type": "ashubh", "intensity": 0.65, "keywords_hi": "संतान समस्या, पेट रोग"},
            6: {"type": "shubh", "intensity": 0.95, "keywords_hi": "शत्रु पराजय, प्रतियोगिता सफलता"},
            7: {"type": "ashubh", "intensity": 0.7, "keywords_hi": "वैवाहिक कलह, जीवनसाथी स्वास्थ्य"},
            8: {"type": "ashubh", "intensity": 0.9, "keywords_hi": "दुर्घटना, शल्य चिकित्सा, हानि"},
            9: {"type": "mishra", "intensity": 0.5, "keywords_hi": "पिता समस्या, यात्रा"},
            10: {"type": "mishra", "intensity": 0.55, "keywords_hi": "करियर मिश्रित, संघर्ष से पदोन्नति"},
            11: {"type": "shubh", "intensity": 1.0, "keywords_hi": "अधिकतम लाभ, संपत्ति अर्जन"},
            12: {"type": "ashubh", "intensity": 0.75, "keywords_hi": "व्यय, अस्पताल"},
        },
    },
    "SUN": {
        "favorable_houses": [3, 6, 10, 11],
        "unfavorable_houses": [1, 2, 4, 7, 8, 12],
        "mixed_houses": [5, 9],
        "transit_duration_days": 30,
        "significance_weight": 0.65,
        "house_effects": {
            1: {"type": "ashubh", "intensity": 0.7, "keywords_hi": "स्वास्थ्य, अहंकार संघर्ष"},
            2: {"type": "ashubh", "intensity": 0.65, "keywords_hi": "आर्थिक हानि, नेत्र समस्या"},
            3: {"type": "shubh", "intensity": 0.8, "keywords_hi": "सफलता, साहस"},
            4: {"type": "ashubh", "intensity": 0.7, "keywords_hi": "मानसिक कष्ट, हृदय समस्या"},
            5: {"type": "mishra", "intensity": 0.5, "keywords_hi": "संतान चिंता"},
            6: {"type": "shubh", "intensity": 0.9, "keywords_hi": "शत्रु विजय, स्वास्थ्य सुधार"},
            7: {"type": "ashubh", "intensity": 0.6, "keywords_hi": "यात्रा कष्ट, थकान"},
            8: {"type": "ashubh", "intensity": 0.75, "keywords_hi": "स्वास्थ्य समस्या, दुर्घटना"},
            9: {"type": "mishra", "intensity": 0.5, "keywords_hi": "पिता चिंता"},
            10: {"type": "shubh", "intensity": 0.85, "keywords_hi": "करियर सफलता, मान्यता"},
            11: {"type": "shubh", "intensity": 1.0, "keywords_hi": "लाभ, लक्ष्य प्राप्ति"},
            12: {"type": "ashubh", "intensity": 0.7, "keywords_hi": "व्यय, पद हानि"},
        },
    },
    "MOON": {
        "favorable_houses": [1, 3, 6, 7, 10, 11],
        "unfavorable_houses": [2, 4, 5, 8, 9, 12],
        "mixed_houses": [],
        "transit_duration_days": 2.25,
        "significance_weight": 0.5,  # Highest for daily predictions
        "house_effects": {
            1: {"type": "shubh", "intensity": 0.8, "keywords_hi": "मानसिक शांति, सुख"},
            2: {"type": "ashubh", "intensity": 0.6, "keywords_hi": "आर्थिक चिंता"},
            3: {"type": "shubh", "intensity": 0.8, "keywords_hi": "सफलता, शुभ समाचार"},
            4: {"type": "ashubh", "intensity": 0.65, "keywords_hi": "मानसिक चिंता"},
            5: {"type": "ashubh", "intensity": 0.55, "keywords_hi": "संतान चिंता"},
            6: {"type": "shubh", "intensity": 0.85, "keywords_hi": "शत्रु विजय"},
            7: {"type": "shubh", "intensity": 0.75, "keywords_hi": "आनंद, जीवनसाथी सुख"},
            8: {"type": "ashubh", "intensity": 0.7, "keywords_hi": "मानसिक कष्ट"},
            9: {"type": "ashubh", "intensity": 0.6, "keywords_hi": "बाधाएं"},
            10: {"type": "shubh", "intensity": 0.85, "keywords_hi": "कार्य सफलता"},
            11: {"type": "shubh", "intensity": 1.0, "keywords_hi": "लाभ, प्रसन्नता"},
            12: {"type": "ashubh", "intensity": 0.65, "keywords_hi": "व्यय, निद्रा समस्या"},
        },
    },
    "MERCURY": {
        "favorable_houses": [2, 4, 6, 8, 10, 11],
        "unfavorable_houses": [1, 3, 5, 7, 9, 12],
        "mixed_houses": [],
        "transit_duration_days": 25,
        "significance_weight": 0.55,
        "house_effects": {
            1: {"type": "ashubh", "intensity": 0.6, "keywords_hi": "संवाद समस्या"},
            2: {"type": "shubh", "intensity": 0.8, "keywords_hi": "आर्थिक लाभ, वाकपटुता"},
            3: {"type": "ashubh", "intensity": 0.55, "keywords_hi": "भाई-बहन समस्या"},
            4: {"type": "shubh", "intensity": 0.75, "keywords_hi": "गृह सुख"},
            5: {"type": "ashubh", "intensity": 0.6, "keywords_hi": "शिक्षा बाधा"},
            6: {"type": "shubh", "intensity": 0.85, "keywords_hi": "वाद-विवाद में विजय"},
            7: {"type": "ashubh", "intensity": 0.6, "keywords_hi": "साझेदारी विवाद"},
            8: {"type": "shubh", "intensity": 0.7, "keywords_hi": "गूढ़ ज्ञान"},
            9: {"type": "ashubh", "intensity": 0.55, "keywords_hi": "उच्च शिक्षा बाधा"},
            10: {"type": "shubh", "intensity": 0.85, "keywords_hi": "करियर सफलता"},
            11: {"type": "shubh", "intensity": 1.0, "keywords_hi": "अधिकतम लाभ"},
            12: {"type": "ashubh", "intensity": 0.6, "keywords_hi": "व्यय, चिंता"},
        },
    },
    "VENUS": {
        "favorable_houses": [1, 2, 3, 4, 5, 8, 9, 11, 12],
        "unfavorable_houses": [6, 7, 10],
        "mixed_houses": [],
        "transit_duration_days": 28,
        "significance_weight": 0.6,
        "house_effects": {
            1: {"type": "shubh", "intensity": 0.8, "keywords_hi": "सुख, विलासिता"},
            2: {"type": "shubh", "intensity": 0.85, "keywords_hi": "धन लाभ"},
            3: {"type": "shubh", "intensity": 0.75, "keywords_hi": "कला में सफलता"},
            4: {"type": "shubh", "intensity": 0.85, "keywords_hi": "वाहन लाभ, सुख"},
            5: {"type": "shubh", "intensity": 0.9, "keywords_hi": "प्रेम, सृजनात्मकता"},
            6: {"type": "ashubh", "intensity": 0.6, "keywords_hi": "स्वास्थ्य समस्या"},
            7: {"type": "ashubh", "intensity": 0.65, "keywords_hi": "वैवाहिक समस्या"},
            8: {"type": "shubh", "intensity": 0.7, "keywords_hi": "आकस्मिक लाभ"},
            9: {"type": "shubh", "intensity": 0.8, "keywords_hi": "भाग्य, धार्मिक कार्य"},
            10: {"type": "ashubh", "intensity": 0.6, "keywords_hi": "करियर बाधा"},
            11: {"type": "shubh", "intensity": 1.0, "keywords_hi": "अधिकतम लाभ, सुख"},
            12: {"type": "shubh", "intensity": 0.75, "keywords_hi": "शयन सुख, विदेश लाभ"},
        },
    },
    "RAHU": {
        "favorable_houses": [3, 6, 10, 11],
        "unfavorable_houses": [1, 2, 4, 5, 7, 8, 9, 12],
        "mixed_houses": [],
        "transit_duration_days": 548,  # ~18 months
        "significance_weight": 0.85,
        "house_effects": {
            1: {"type": "ashubh", "intensity": 0.8, "keywords_hi": "स्वास्थ्य, भ्रम, चिंता"},
            2: {"type": "ashubh", "intensity": 0.7, "keywords_hi": "आर्थिक हानि, पारिवारिक कलह"},
            3: {"type": "shubh", "intensity": 0.85, "keywords_hi": "साहस, अपारंपरिक सफलता"},
            4: {"type": "ashubh", "intensity": 0.75, "keywords_hi": "गृह अशांति, माता समस्या"},
            5: {"type": "ashubh", "intensity": 0.7, "keywords_hi": "संतान समस्या, सट्टा हानि"},
            6: {"type": "shubh", "intensity": 0.95, "keywords_hi": "शत्रु विजय, प्रतियोगिता सफलता"},
            7: {"type": "ashubh", "intensity": 0.7, "keywords_hi": "वैवाहिक समस्या, छल"},
            8: {"type": "ashubh", "intensity": 0.85, "keywords_hi": "आकस्मिक हानि, दुर्घटना"},
            9: {"type": "ashubh", "intensity": 0.65, "keywords_hi": "पिता समस्या, धार्मिक भ्रम"},
            10: {"type": "shubh", "intensity": 0.8, "keywords_hi": "आकस्मिक उन्नति, अपारंपरिक करियर"},
            11: {"type": "shubh", "intensity": 1.0, "keywords_hi": "अधिकतम लाभ, विदेशी स्रोत"},
            12: {"type": "ashubh", "intensity": 0.75, "keywords_hi": "व्यय, विदेश समस्या"},
        },
    },
    "KETU": {
        "favorable_houses": [3, 6, 11],
        "unfavorable_houses": [1, 2, 4, 5, 7, 9, 10],
        "mixed_houses": [8, 12],
        "transit_duration_days": 548,  # ~18 months
        "significance_weight": 0.8,
        "house_effects": {
            1: {"type": "ashubh", "intensity": 0.75, "keywords_hi": "स्वास्थ्य, भ्रम"},
            2: {"type": "ashubh", "intensity": 0.7, "keywords_hi": "आर्थिक हानि, वाणी समस्या"},
            3: {"type": "shubh", "intensity": 0.85, "keywords_hi": "साहस, वैराग्य से सफलता"},
            4: {"type": "ashubh", "intensity": 0.7, "keywords_hi": "गृह समस्या, माता से दूरी"},
            5: {"type": "ashubh", "intensity": 0.65, "keywords_hi": "संतान समस्या"},
            6: {"type": "shubh", "intensity": 0.9, "keywords_hi": "शत्रु विजय, आध्यात्मिक स्वास्थ्य"},
            7: {"type": "ashubh", "intensity": 0.7, "keywords_hi": "वैवाहिक समस्या, विच्छेद"},
            8: {"type": "mishra", "intensity": 0.5, "keywords_hi": "आध्यात्मिक परिवर्तन, गूढ़ विद्या"},
            9: {"type": "ashubh", "intensity": 0.6, "keywords_hi": "पिता समस्या, धार्मिक संशय"},
            10: {"type": "ashubh", "intensity": 0.7, "keywords_hi": "करियर अस्थिरता"},
            11: {"type": "shubh", "intensity": 0.85, "keywords_hi": "आध्यात्मिक लाभ, वैराग्य सफलता"},
            12: {"type": "mishra", "intensity": 0.5, "keywords_hi": "आध्यात्मिक प्रगति, मोक्ष"},
        },
    },
}

# Period-specific primary planets for Rashifal
PRIMARY_PLANETS_BY_PERIOD = {
    "daily": ["MOON"],  # Moon changes every 2.25 days
    "weekly": ["MOON", "SUN", "MERCURY"],
    "monthly": ["SUN", "MARS", "MERCURY", "VENUS"],
    "yearly": ["JUPITER", "SATURN", "RAHU", "KETU"],  # Slow-moving planets
}

# Planet special aspects (for double transit calculations)
PLANET_ASPECTS = {
    "SATURN": [3, 7, 10],  # 3rd, 7th, 10th aspect
    "JUPITER": [5, 7, 9],  # 5th, 7th, 9th aspect
    "MARS": [4, 7, 8],     # 4th, 7th, 8th aspect
    "RAHU": [5, 7, 9],     # Same as Jupiter
    "KETU": [5, 7, 9],     # Same as Jupiter
    "SUN": [7],
    "MOON": [7],
    "MERCURY": [7],
    "VENUS": [7],
}
