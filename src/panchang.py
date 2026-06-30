"""
Panchang Calculator - Five Limbs of Vedic Time (Complete Implementation)
Calculates Tithi, Nakshatra, Yoga, Karana, and Vara for any datetime

Based on authentic classical texts:
- Surya Siddhanta
- Muhurta Chintamani by Rama Daivagnya
- Brihat Samhita by Varahamihira
- Dharmasindhu

Includes:
- Five Limbs (Panch Ang): Tithi, Nakshatra, Yoga, Karana, Vara
- Choghadiya (Day and Night)
- Rahu Kaal, Yamaghantaka, Gulika Kaal
- Sunrise, Sunset, Moonrise, Moonset
- Auspicious/Inauspicious indicators
"""

import swisseph as swe
from datetime import datetime, timedelta, time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import pytz

from .planets import PlanetaryCalculator
from .config import (
    Planet, NAKSHATRAS, TITHIS, YOGAS_27, KARANAS, VARAS,
    RIKTA_TITHIS, INAUSPICIOUS_YOGAS, NAKSHATRA_SPAN,
    RAHU_KALA_SEQUENCE, YAMAGHANTAKA_SEQUENCE, GULIKA_SEQUENCE
)


# =============================================================================
# CHOGHADIYA CONSTANTS (from Muhurta Chintamani)
# =============================================================================

# Choghadiya types with their qualities
CHOGHADIYA_TYPES = {
    "Udveg": {"hindi": "उद्वेग", "quality": "Inauspicious", "lord": "Sun", "nature": "Anxiety"},
    "Char": {"hindi": "चर", "quality": "Good for travel", "lord": "Venus", "nature": "Movement"},
    "Labh": {"hindi": "लाभ", "quality": "Auspicious", "lord": "Mercury", "nature": "Gain"},
    "Amrit": {"hindi": "अमृत", "quality": "Most Auspicious", "lord": "Moon", "nature": "Nectar"},
    "Kaal": {"hindi": "काल", "quality": "Inauspicious", "lord": "Saturn", "nature": "Death"},
    "Shubh": {"hindi": "शुभ", "quality": "Auspicious", "lord": "Jupiter", "nature": "Good"},
    "Rog": {"hindi": "रोग", "quality": "Inauspicious", "lord": "Mars", "nature": "Disease"},
}

# Day Choghadiya sequence by weekday (0=Sunday)
# Each day starts with a different Choghadiya after sunrise
DAY_CHOGHADIYA_SEQUENCE = {
    0: ["Udveg", "Char", "Labh", "Amrit", "Kaal", "Shubh", "Rog", "Udveg"],  # Sunday
    1: ["Amrit", "Kaal", "Shubh", "Rog", "Udveg", "Char", "Labh", "Amrit"],  # Monday
    2: ["Rog", "Udveg", "Char", "Labh", "Amrit", "Kaal", "Shubh", "Rog"],    # Tuesday
    3: ["Labh", "Amrit", "Kaal", "Shubh", "Rog", "Udveg", "Char", "Labh"],   # Wednesday
    4: ["Shubh", "Rog", "Udveg", "Char", "Labh", "Amrit", "Kaal", "Shubh"],  # Thursday
    5: ["Char", "Labh", "Amrit", "Kaal", "Shubh", "Rog", "Udveg", "Char"],   # Friday
    6: ["Kaal", "Shubh", "Rog", "Udveg", "Char", "Labh", "Amrit", "Kaal"],   # Saturday
}

# Night Choghadiya sequence by weekday
NIGHT_CHOGHADIYA_SEQUENCE = {
    0: ["Shubh", "Amrit", "Char", "Rog", "Kaal", "Labh", "Udveg", "Shubh"],  # Sunday night
    1: ["Char", "Rog", "Kaal", "Labh", "Udveg", "Shubh", "Amrit", "Char"],   # Monday night
    2: ["Kaal", "Labh", "Udveg", "Shubh", "Amrit", "Char", "Rog", "Kaal"],   # Tuesday night
    3: ["Udveg", "Shubh", "Amrit", "Char", "Rog", "Kaal", "Labh", "Udveg"],  # Wednesday night
    4: ["Amrit", "Char", "Rog", "Kaal", "Labh", "Udveg", "Shubh", "Amrit"],  # Thursday night
    5: ["Rog", "Kaal", "Labh", "Udveg", "Shubh", "Amrit", "Char", "Rog"],    # Friday night
    6: ["Labh", "Udveg", "Shubh", "Amrit", "Char", "Rog", "Kaal", "Labh"],   # Saturday night
}


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class TithiData:
    """Lunar day (1-30)."""
    number: int
    name: str
    hindi: str
    paksha: str
    paksha_hindi: str
    lord: str
    is_rikta: bool
    is_purnima: bool
    is_amavasya: bool
    percentage_elapsed: float
    end_time: Optional[datetime] = None


@dataclass
class NakshatraData:
    """Moon's Nakshatra details."""
    number: int
    name: str
    hindi: str
    lord: str
    deity: str
    pada: int
    start_degree: float
    end_degree: float
    percentage_elapsed: float
    end_time: Optional[datetime] = None


@dataclass
class YogaData:
    """Sun-Moon combination yoga (1-27)."""
    number: int
    name: str
    hindi: str
    is_inauspicious: bool
    description: str
    end_time: Optional[datetime] = None


@dataclass
class KaranaData:
    """Half-tithi division (1-11 cyclical)."""
    number: int
    name: str
    hindi: str
    type: str
    is_auspicious: bool
    is_vishti: bool  # Bhadra Karana
    end_time: Optional[datetime] = None


@dataclass
class VaraData:
    """Weekday with planetary ruler."""
    number: int
    name: str
    hindi: str
    english: str
    lord: str
    is_auspicious: bool


@dataclass
class ChoghadiyaData:
    """Single Choghadiya period."""
    name: str
    hindi: str
    start_time: datetime
    end_time: datetime
    quality: str
    lord: str
    nature: str
    is_auspicious: bool


@dataclass
class InauspiciousPeriod:
    """Inauspicious time period."""
    name: str
    hindi: str
    start_time: datetime
    end_time: datetime
    severity: str
    description: str


@dataclass
class SunMoonTimings:
    """Sun and Moon rise/set timings."""
    sunrise: datetime
    sunset: datetime
    moonrise: Optional[datetime]
    moonset: Optional[datetime]
    day_duration: timedelta
    night_duration: timedelta


@dataclass
class AuspiciousnessInfo:
    """Overall auspiciousness assessment."""
    is_shubh_din: bool
    score: int  # 0-100
    positive_factors: List[str]
    negative_factors: List[str]
    recommendations: List[str]


@dataclass
class PanchangData:
    """Complete Panchang (five limbs) data for a moment."""
    date: datetime
    location: str
    latitude: float
    longitude: float
    timezone: str

    # Five Limbs
    tithi: TithiData
    nakshatra: NakshatraData
    yoga: YogaData
    karana: KaranaData
    vara: VaraData

    # Sun/Moon Timings
    timings: SunMoonTimings

    # Choghadiya
    day_choghadiya: List[ChoghadiyaData]
    night_choghadiya: List[ChoghadiyaData]
    current_choghadiya: Optional[ChoghadiyaData]

    # Inauspicious Periods
    rahu_kaal: InauspiciousPeriod
    yamaghantaka: InauspiciousPeriod
    gulika_kaal: InauspiciousPeriod
    abhijit_muhurta: Optional[Tuple[datetime, datetime]]

    # Astronomical Data
    moon_longitude: float
    sun_longitude: float
    moon_rashi: str
    moon_rashi_num: int
    moon_rashi_hindi: str
    sun_rashi: str
    ayanamsa: float

    # Overall Assessment
    auspiciousness: AuspiciousnessInfo


# =============================================================================
# HINDI DATA CONSTANTS
# =============================================================================

NAKSHATRA_HINDI = [
    "अश्विनी", "भरणी", "कृत्तिका", "रोहिणी", "मृगशिरा", "आर्द्रा",
    "पुनर्वसु", "पुष्य", "आश्लेषा", "मघा", "पूर्वा फाल्गुनी", "उत्तरा फाल्गुनी",
    "हस्त", "चित्रा", "स्वाति", "विशाखा", "अनुराधा", "ज्येष्ठा",
    "मूल", "पूर्वाषाढ़ा", "उत्तराषाढ़ा", "श्रवण", "धनिष्ठा", "शतभिषा",
    "पूर्वाभाद्रपद", "उत्तराभाद्रपद", "रेवती"
]

RASHI_HINDI = {
    "Mesha": "मेष", "Vrishabha": "वृषभ", "Mithuna": "मिथुन",
    "Karka": "कर्क", "Simha": "सिंह", "Kanya": "कन्या",
    "Tula": "तुला", "Vrishchika": "वृश्चिक", "Dhanu": "धनु",
    "Makara": "मकर", "Kumbha": "कुंभ", "Meena": "मीन"
}


# =============================================================================
# MAIN PANCHANG CALCULATOR CLASS
# =============================================================================

class PanchangCalculator:
    """
    Complete Panchang Calculator for Vedic almanac data.

    Uses Swiss Ephemeris for high-accuracy planetary calculations.
    Based on authentic Vedic texts: Surya Siddhanta, Muhurta Chintamani,
    Brihat Samhita, and Dharmasindhu.
    """

    def __init__(self):
        self.calculator = PlanetaryCalculator()

    def get_panchang(
        self,
        dt: datetime,
        latitude: float = 28.6139,
        longitude: float = 77.2090,
        timezone: str = "Asia/Kolkata",
        location: str = "Delhi"
    ) -> PanchangData:
        """
        Get complete Panchang data for a given datetime and location.

        Args:
            dt: Datetime for calculation
            latitude: Location latitude (default: Delhi)
            longitude: Location longitude (default: Delhi)
            timezone: Timezone string (default: Asia/Kolkata)
            location: Location name for display

        Returns:
            PanchangData with all five limbs and additional information
        """
        tz = pytz.timezone(timezone)
        if dt.tzinfo is None:
            dt = tz.localize(dt)

        jd = self.calculator.datetime_to_jd(dt, timezone)

        # Get planetary positions
        sun_pos = self.calculator.get_planet_position(Planet.SUN, jd)
        moon_pos = self.calculator.get_planet_position(Planet.MOON, jd)

        sun_long = sun_pos["longitude"]
        moon_long = moon_pos["longitude"]

        # Calculate sun/moon timings
        timings = self._calculate_sun_moon_timings(dt, latitude, longitude, tz)

        # Calculate Five Limbs
        tithi = self._calculate_tithi(sun_long, moon_long, dt, timezone)
        nakshatra = self._calculate_nakshatra(moon_pos, dt, timezone)
        yoga = self._calculate_yoga(sun_long, moon_long)
        karana = self._calculate_karana(sun_long, moon_long)
        vara = self._calculate_vara(dt)

        # Calculate Choghadiya
        day_choghadiya = self._calculate_day_choghadiya(
            timings.sunrise, timings.sunset, dt.weekday()
        )
        night_choghadiya = self._calculate_night_choghadiya(
            timings.sunset, timings.sunrise + timedelta(days=1), dt.weekday()
        )
        current_chog = self._get_current_choghadiya(dt, day_choghadiya, night_choghadiya)

        # Calculate Inauspicious Periods
        rahu_kaal = self._calculate_rahu_kaal(timings.sunrise, timings.sunset, dt.weekday())
        yamaghantaka = self._calculate_yamaghantaka(timings.sunrise, timings.sunset, dt.weekday())
        gulika_kaal = self._calculate_gulika_kaal(timings.sunrise, timings.sunset, dt.weekday())
        abhijit = self._calculate_abhijit_muhurta(timings.sunrise, timings.sunset)

        # Get Ayanamsa
        ayanamsa = self.calculator.get_ayanamsa_value(jd)

        # Calculate overall auspiciousness
        auspiciousness = self._calculate_auspiciousness(
            tithi, nakshatra, yoga, karana, vara
        )

        return PanchangData(
            date=dt,
            location=location,
            latitude=latitude,
            longitude=longitude,
            timezone=timezone,
            tithi=tithi,
            nakshatra=nakshatra,
            yoga=yoga,
            karana=karana,
            vara=vara,
            timings=timings,
            day_choghadiya=day_choghadiya,
            night_choghadiya=night_choghadiya,
            current_choghadiya=current_chog,
            rahu_kaal=rahu_kaal,
            yamaghantaka=yamaghantaka,
            gulika_kaal=gulika_kaal,
            abhijit_muhurta=abhijit,
            moon_longitude=moon_long,
            sun_longitude=sun_long,
            moon_rashi=moon_pos["rashi"],
            moon_rashi_num=moon_pos["rashi_num"],
            moon_rashi_hindi=RASHI_HINDI.get(moon_pos["rashi"], moon_pos["rashi"]),
            sun_rashi=sun_pos["rashi"],
            ayanamsa=ayanamsa,
            auspiciousness=auspiciousness
        )

    def _calculate_tithi(
        self,
        sun_long: float,
        moon_long: float,
        dt: datetime,
        timezone: str
    ) -> TithiData:
        """
        Calculate Tithi (lunar day) based on Surya Siddhanta.

        Tithi is the angular distance between Moon and Sun divided by 12 degrees.
        Each tithi spans 12 degrees of elongation.
        """
        angle_diff = (moon_long - sun_long) % 360
        tithi_num_raw = int(angle_diff / 12)
        tithi_num = tithi_num_raw + 1

        percentage_elapsed = ((angle_diff % 12) / 12) * 100

        if tithi_num <= 15:
            paksha = "Shukla"
            paksha_hindi = "शुक्ल पक्ष"
            tithi_index = tithi_num - 1
        else:
            paksha = "Krishna"
            paksha_hindi = "कृष्ण पक्ष"
            tithi_index = (tithi_num - 16) if tithi_num < 30 else 14

        is_purnima = (tithi_num == 15)
        is_amavasya = (tithi_num == 30)

        if is_purnima:
            tithi_info = TITHIS[14]
            name = "Purnima"
            hindi = "पूर्णिमा"
        elif is_amavasya:
            tithi_info = TITHIS[15]
            name = "Amavasya"
            hindi = "अमावस्या"
        else:
            tithi_info = TITHIS[tithi_index % 15]
            name = tithi_info["name"]
            hindi = tithi_info["hindi"]

        tithi_in_paksha = tithi_num if tithi_num <= 15 else tithi_num - 15
        is_rikta = tithi_in_paksha in RIKTA_TITHIS

        return TithiData(
            number=tithi_num,
            name=name,
            hindi=hindi,
            paksha=paksha,
            paksha_hindi=paksha_hindi,
            lord=tithi_info["lord"],
            is_rikta=is_rikta,
            is_purnima=is_purnima,
            is_amavasya=is_amavasya,
            percentage_elapsed=round(percentage_elapsed, 2)
        )

    def _calculate_nakshatra(
        self,
        moon_pos: Dict,
        dt: datetime,
        timezone: str
    ) -> NakshatraData:
        """
        Calculate Moon's Nakshatra based on Swiss Ephemeris position.

        27 Nakshatras, each spanning 13°20' (13.333... degrees).
        """
        nakshatra_num = moon_pos["nakshatra_num"]
        nakshatra_info = NAKSHATRAS[nakshatra_num]

        moon_long = moon_pos["longitude"]
        start_deg = nakshatra_info["start"]
        end_deg = (start_deg + NAKSHATRA_SPAN) % 360

        # Calculate percentage elapsed within nakshatra
        if end_deg > start_deg:
            position_in_nakshatra = moon_long - start_deg
        else:
            if moon_long >= start_deg:
                position_in_nakshatra = moon_long - start_deg
            else:
                position_in_nakshatra = (360 - start_deg) + moon_long

        percentage_elapsed = (position_in_nakshatra / NAKSHATRA_SPAN) * 100

        hindi_name = NAKSHATRA_HINDI[nakshatra_num] if nakshatra_num < len(NAKSHATRA_HINDI) else nakshatra_info["name"]

        return NakshatraData(
            number=nakshatra_num + 1,
            name=nakshatra_info["name"],
            hindi=hindi_name,
            lord=nakshatra_info["lord"],
            deity=nakshatra_info["deity"],
            pada=moon_pos["pada"],
            start_degree=start_deg,
            end_degree=end_deg,
            percentage_elapsed=round(percentage_elapsed, 2)
        )

    def _calculate_yoga(self, sun_long: float, moon_long: float) -> YogaData:
        """
        Calculate Yoga based on Brihat Samhita.

        Yoga is the sum of Sun and Moon longitudes divided by 13°20'.
        27 Yogas from Vishkumbha to Vaidhriti.
        """
        angle_sum = (sun_long + moon_long) % 360
        yoga_span = 360 / 27
        yoga_index = int(angle_sum / yoga_span) % 27

        yoga_info = YOGAS_27[yoga_index]

        # Descriptions for yogas
        yoga_descriptions = {
            "Vishkumbha": "Obstacles and delays (Vighna karak)",
            "Priti": "Love and affection (Prem karak)",
            "Ayushman": "Long life and health (Ayu karak)",
            "Saubhagya": "Good fortune (Bhagya karak)",
            "Shobhana": "Beauty and charm (Shobha karak)",
            "Atiganda": "Obstacles in work (Kasht karak)",
            "Sukarma": "Good deeds rewarded (Punya karak)",
            "Dhriti": "Stability and patience (Dhairya karak)",
            "Shoola": "Pain and suffering (Dukh karak)",
            "Ganda": "Difficulties (Sankat karak)",
            "Vriddhi": "Growth and progress (Unnati karak)",
            "Dhruva": "Permanence (Sthirata karak)",
            "Vyaghata": "Destruction (Vinash karak)",
            "Harshana": "Joy and happiness (Harsha karak)",
            "Vajra": "Strength but obstacles (Shakti karak)",
            "Siddhi": "Success in endeavors (Siddhi karak)",
            "Vyatipata": "Calamity (Aapat karak)",
            "Variyan": "Comfort and ease (Sukh karak)",
            "Parigha": "Obstruction (Baadha karak)",
            "Shiva": "Auspicious (Shubh karak)",
            "Siddha": "Accomplishment (Safalta karak)",
            "Sadhya": "Achievable goals (Prapti karak)",
            "Shubha": "Auspicious (Mangal karak)",
            "Shukla": "Purity (Pavitrata karak)",
            "Brahma": "Knowledge (Gyan karak)",
            "Indra": "Prosperity (Samriddhi karak)",
            "Vaidhriti": "Problems (Samasya karak)",
        }

        return YogaData(
            number=yoga_index + 1,
            name=yoga_info["name"],
            hindi=yoga_info["hindi"],
            is_inauspicious=yoga_info["inauspicious"],
            description=yoga_descriptions.get(yoga_info["name"], "")
        )

    def _calculate_karana(self, sun_long: float, moon_long: float) -> KaranaData:
        """
        Calculate Karana (half-tithi) based on Dharmasindhu.

        11 Karanas: 4 fixed (occur once) + 7 moveable (cycle 8 times).
        Vishti (Bhadra) is considered inauspicious.
        """
        angle_diff = (moon_long - sun_long) % 360
        karana_num_raw = int(angle_diff / 6)

        # Map raw karana number to karana index
        if karana_num_raw == 0:
            karana_index = 10  # Kimstughna
        elif karana_num_raw == 57:
            karana_index = 7   # Shakuni
        elif karana_num_raw == 58:
            karana_index = 8   # Chatushpada
        elif karana_num_raw == 59:
            karana_index = 9   # Naga
        else:
            karana_index = ((karana_num_raw - 1) % 7)

        karana_info = KARANAS[karana_index]
        is_vishti = (karana_info["name"] == "Vishti")

        return KaranaData(
            number=karana_index + 1,
            name=karana_info["name"],
            hindi=karana_info["hindi"],
            type=karana_info["type"],
            is_auspicious=karana_info["auspicious"],
            is_vishti=is_vishti
        )

    def _calculate_vara(self, dt: datetime) -> VaraData:
        """Calculate Vara (weekday) with planetary lord."""
        weekday = dt.weekday()
        vara_index = (weekday + 1) % 7

        vara_info = VARAS[vara_index]

        # Generally auspicious weekdays for starting work
        auspicious_varas = [1, 3, 4, 5]  # Monday, Wednesday, Thursday, Friday
        is_auspicious = vara_index in auspicious_varas

        return VaraData(
            number=vara_index,
            name=vara_info["name"],
            hindi=vara_info["hindi"],
            english=vara_info["english"],
            lord=vara_info["lord"],
            is_auspicious=is_auspicious
        )

    def _calculate_sun_moon_timings(
        self,
        dt: datetime,
        latitude: float,
        longitude: float,
        tz: pytz.timezone
    ) -> SunMoonTimings:
        """Calculate sunrise, sunset, moonrise, moonset times."""
        if dt.tzinfo is None:
            dt = tz.localize(dt)

        dt_midnight = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        dt_utc = dt_midnight.astimezone(pytz.UTC)

        jd_midnight = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, 0.0)

        # Sunrise
        try:
            rise_result = swe.rise_trans(
                jd_midnight, swe.SUN, longitude, latitude, 0.0, 0.0, 0.0,
                swe.CALC_RISE | swe.BIT_DISC_CENTER
            )
            sunrise_jd = rise_result[1][0] if isinstance(rise_result[1], (list, tuple)) else rise_result[1]
            sunrise = self._jd_to_datetime(sunrise_jd, tz)
        except Exception:
            sunrise = dt.replace(hour=6, minute=0, second=0, microsecond=0)

        # Sunset
        try:
            set_result = swe.rise_trans(
                jd_midnight, swe.SUN, longitude, latitude, 0.0, 0.0, 0.0,
                swe.CALC_SET | swe.BIT_DISC_CENTER
            )
            sunset_jd = set_result[1][0] if isinstance(set_result[1], (list, tuple)) else set_result[1]
            sunset = self._jd_to_datetime(sunset_jd, tz)
        except Exception:
            sunset = dt.replace(hour=18, minute=0, second=0, microsecond=0)

        # Moonrise
        moonrise = None
        try:
            moon_rise_result = swe.rise_trans(
                jd_midnight, swe.MOON, longitude, latitude, 0.0, 0.0, 0.0,
                swe.CALC_RISE | swe.BIT_DISC_CENTER
            )
            if moon_rise_result[0] >= 0:
                moonrise_jd = moon_rise_result[1][0] if isinstance(moon_rise_result[1], (list, tuple)) else moon_rise_result[1]
                moonrise = self._jd_to_datetime(moonrise_jd, tz)
        except Exception:
            pass

        # Moonset
        moonset = None
        try:
            moon_set_result = swe.rise_trans(
                jd_midnight, swe.MOON, longitude, latitude, 0.0, 0.0, 0.0,
                swe.CALC_SET | swe.BIT_DISC_CENTER
            )
            if moon_set_result[0] >= 0:
                moonset_jd = moon_set_result[1][0] if isinstance(moon_set_result[1], (list, tuple)) else moon_set_result[1]
                moonset = self._jd_to_datetime(moonset_jd, tz)
        except Exception:
            pass

        day_duration = sunset - sunrise
        # Night duration (sunset to next sunrise, approximated)
        night_duration = timedelta(hours=24) - day_duration

        return SunMoonTimings(
            sunrise=sunrise,
            sunset=sunset,
            moonrise=moonrise,
            moonset=moonset,
            day_duration=day_duration,
            night_duration=night_duration
        )

    def _calculate_day_choghadiya(
        self,
        sunrise: datetime,
        sunset: datetime,
        weekday: int
    ) -> List[ChoghadiyaData]:
        """
        Calculate Day Choghadiya (8 parts from sunrise to sunset).

        Based on Muhurta Chintamani - each day starts with a different
        Choghadiya based on the weekday.
        """
        # Adjust weekday (Python: 0=Mon, we need 0=Sun)
        adjusted_weekday = (weekday + 1) % 7

        day_duration = (sunset - sunrise).total_seconds()
        part_duration = day_duration / 8

        sequence = DAY_CHOGHADIYA_SEQUENCE[adjusted_weekday]
        choghadiyas = []

        for i, name in enumerate(sequence):
            start = sunrise + timedelta(seconds=i * part_duration)
            end = sunrise + timedelta(seconds=(i + 1) * part_duration)

            info = CHOGHADIYA_TYPES[name]
            is_auspicious = info["quality"] in ["Most Auspicious", "Auspicious", "Good for travel"]

            choghadiyas.append(ChoghadiyaData(
                name=name,
                hindi=info["hindi"],
                start_time=start,
                end_time=end,
                quality=info["quality"],
                lord=info["lord"],
                nature=info["nature"],
                is_auspicious=is_auspicious
            ))

        return choghadiyas

    def _calculate_night_choghadiya(
        self,
        sunset: datetime,
        next_sunrise: datetime,
        weekday: int
    ) -> List[ChoghadiyaData]:
        """
        Calculate Night Choghadiya (8 parts from sunset to next sunrise).
        """
        adjusted_weekday = (weekday + 1) % 7

        night_duration = (next_sunrise - sunset).total_seconds()
        part_duration = night_duration / 8

        sequence = NIGHT_CHOGHADIYA_SEQUENCE[adjusted_weekday]
        choghadiyas = []

        for i, name in enumerate(sequence):
            start = sunset + timedelta(seconds=i * part_duration)
            end = sunset + timedelta(seconds=(i + 1) * part_duration)

            info = CHOGHADIYA_TYPES[name]
            is_auspicious = info["quality"] in ["Most Auspicious", "Auspicious", "Good for travel"]

            choghadiyas.append(ChoghadiyaData(
                name=name,
                hindi=info["hindi"],
                start_time=start,
                end_time=end,
                quality=info["quality"],
                lord=info["lord"],
                nature=info["nature"],
                is_auspicious=is_auspicious
            ))

        return choghadiyas

    def _get_current_choghadiya(
        self,
        dt: datetime,
        day_choghadiyas: List[ChoghadiyaData],
        night_choghadiyas: List[ChoghadiyaData]
    ) -> Optional[ChoghadiyaData]:
        """Find the current Choghadiya for a given time."""
        for chog in day_choghadiyas:
            if chog.start_time <= dt < chog.end_time:
                return chog

        for chog in night_choghadiyas:
            if chog.start_time <= dt < chog.end_time:
                return chog

        return None

    def _calculate_rahu_kaal(
        self,
        sunrise: datetime,
        sunset: datetime,
        weekday: int
    ) -> InauspiciousPeriod:
        """
        Calculate Rahu Kaal - inauspicious period ruled by Rahu.

        Memory aid: "Mother Saw Father Wearing The Turban on Saturday"
        Mon=2, Sat=3, Fri=4, Wed=5, Thu=6, Tue=7, Sun=8
        """
        adjusted_weekday = (weekday + 1) % 7
        day_duration = (sunset - sunrise).total_seconds()
        part_duration = day_duration / 8

        rahu_part = RAHU_KALA_SEQUENCE[adjusted_weekday]
        start = sunrise + timedelta(seconds=(rahu_part - 1) * part_duration)
        end = start + timedelta(seconds=part_duration)

        return InauspiciousPeriod(
            name="Rahu Kaal",
            hindi="राहु काल",
            start_time=start,
            end_time=end,
            severity="high",
            description="Avoid starting important works during this period"
        )

    def _calculate_yamaghantaka(
        self,
        sunrise: datetime,
        sunset: datetime,
        weekday: int
    ) -> InauspiciousPeriod:
        """Calculate Yamaghantaka - period ruled by Yama (god of death)."""
        adjusted_weekday = (weekday + 1) % 7
        day_duration = (sunset - sunrise).total_seconds()
        part_duration = day_duration / 8

        yama_part = YAMAGHANTAKA_SEQUENCE[adjusted_weekday]
        start = sunrise + timedelta(seconds=(yama_part - 1) * part_duration)
        end = start + timedelta(seconds=part_duration)

        return InauspiciousPeriod(
            name="Yamaghantaka",
            hindi="यमघण्टक",
            start_time=start,
            end_time=end,
            severity="medium",
            description="Avoid auspicious ceremonies during this period"
        )

    def _calculate_gulika_kaal(
        self,
        sunrise: datetime,
        sunset: datetime,
        weekday: int
    ) -> InauspiciousPeriod:
        """Calculate Gulika Kaal - period of Gulika/Mandi (son of Saturn)."""
        adjusted_weekday = (weekday + 1) % 7
        day_duration = (sunset - sunrise).total_seconds()
        part_duration = day_duration / 8

        gulika_part = GULIKA_SEQUENCE[adjusted_weekday]
        start = sunrise + timedelta(seconds=(gulika_part - 1) * part_duration)
        end = start + timedelta(seconds=part_duration)

        return InauspiciousPeriod(
            name="Gulika Kaal",
            hindi="गुलिक काल",
            start_time=start,
            end_time=end,
            severity="medium",
            description="Avoid starting new ventures during this period"
        )

    def _calculate_abhijit_muhurta(
        self,
        sunrise: datetime,
        sunset: datetime
    ) -> Optional[Tuple[datetime, datetime]]:
        """
        Calculate Abhijit Muhurta - the most auspicious time of the day.

        Occurs around local noon, approximately 24 minutes before and after.
        """
        day_duration = (sunset - sunrise).total_seconds()
        muhurta_duration = day_duration / 15  # Day divided into 15 muhurtas

        mid_day = sunrise + timedelta(seconds=day_duration / 2)
        start = mid_day - timedelta(seconds=muhurta_duration / 2)
        end = mid_day + timedelta(seconds=muhurta_duration / 2)

        return (start, end)

    def _calculate_auspiciousness(
        self,
        tithi: TithiData,
        nakshatra: NakshatraData,
        yoga: YogaData,
        karana: KaranaData,
        vara: VaraData
    ) -> AuspiciousnessInfo:
        """Calculate overall auspiciousness of the day."""
        score = 50  # Start with neutral score
        positive_factors = []
        negative_factors = []
        recommendations = []

        # Tithi analysis
        if tithi.is_rikta:
            score -= 15
            negative_factors.append(f"Rikta Tithi ({tithi.name}) - avoid important works / रिक्ता तिथि - महत्वपूर्ण कार्य टालें")
        elif tithi.is_amavasya:
            score -= 20
            negative_factors.append("Amavasya - generally inauspicious / अमावस्या - सामान्यतः अशुभ")
        elif tithi.is_purnima:
            score += 10
            positive_factors.append("Purnima - auspicious for spiritual activities / पूर्णिमा - आध्यात्मिक कार्यों के लिए शुभ")
        else:
            if tithi.number in [2, 3, 5, 7, 10, 11, 12, 13]:
                score += 5
                positive_factors.append(f"{tithi.name} Tithi - favorable / {tithi.hindi} - शुभ")

        # Nakshatra analysis
        fixed_nakshatras = [4, 11, 12, 21, 25]  # Rohini, Uttara Phalguni, Hasta, etc.
        if nakshatra.number in fixed_nakshatras:
            score += 10
            positive_factors.append(f"{nakshatra.name} - Fixed/Stable nakshatra / {nakshatra.hindi} - स्थिर नक्षत्र")

        inauspicious_nakshatras = [6, 9, 18, 19]  # Ardra, Ashlesha, Jyeshtha, Mula
        if nakshatra.number in inauspicious_nakshatras:
            score -= 10
            negative_factors.append(f"{nakshatra.name} - Sharp nakshatra, caution advised / {nakshatra.hindi} - तीक्ष्ण नक्षत्र, सावधानी बरतें")

        # Yoga analysis
        if yoga.is_inauspicious:
            score -= 12
            negative_factors.append(f"{yoga.name} Yoga - inauspicious / {yoga.hindi} योग - अशुभ")
        else:
            score += 5
            positive_factors.append(f"{yoga.name} Yoga - favorable / {yoga.hindi} योग - शुभ")

        # Karana analysis
        if karana.is_vishti:
            score -= 15
            negative_factors.append("Vishti (Bhadra) Karana - avoid important works / विष्टि (भद्रा) करण - महत्वपूर्ण कार्य टालें")
            recommendations.append("Wait for Vishti karana to pass / विष्टि करण समाप्त होने की प्रतीक्षा करें")
        elif karana.is_auspicious:
            score += 5
            positive_factors.append(f"{karana.name} Karana - favorable / {karana.hindi} करण - शुभ")

        # Vara analysis
        if vara.is_auspicious:
            score += 8
            positive_factors.append(f"{vara.english} - favorable weekday / {vara.hindi} - शुभ वार")
        else:
            if vara.number in [2, 6]:  # Tuesday, Saturday
                negative_factors.append(f"{vara.english} - exercise caution / {vara.hindi} - सावधानी बरतें")

        # Recommendations based on score
        if score >= 70:
            recommendations.append("Excellent day for important activities / महत्वपूर्ण कार्यों के लिए उत्तम दिन")
        elif score >= 50:
            recommendations.append("Good day, proceed with normal activities / सामान्य कार्यों के लिए अच्छा दिन")
        elif score >= 35:
            recommendations.append("Moderate day, avoid major decisions / साधारण दिन, बड़े निर्णय टालें")
        else:
            recommendations.append("Challenging day, postpone important works if possible / कठिन दिन, संभव हो तो महत्वपूर्ण कार्य टालें")

        # Clamp score
        score = max(0, min(100, score))

        return AuspiciousnessInfo(
            is_shubh_din=(score >= 50),
            score=score,
            positive_factors=positive_factors,
            negative_factors=negative_factors,
            recommendations=recommendations
        )

    def _jd_to_datetime(self, jd: float, tz: pytz.timezone) -> datetime:
        """Convert Julian Day to datetime in specified timezone."""
        result = swe.revjul(jd)
        year, month, day, hour_decimal = result

        hours = int(hour_decimal)
        minutes_decimal = (hour_decimal - hours) * 60
        minutes = int(minutes_decimal)
        seconds = int((minutes_decimal - minutes) * 60)

        dt_utc = datetime(
            int(year), int(month), int(day),
            hours, minutes, seconds,
            tzinfo=pytz.UTC
        )

        return dt_utc.astimezone(tz)

    def get_panchang_summary(
        self,
        dt: datetime,
        latitude: float = 28.6139,
        longitude: float = 77.2090,
        timezone: str = "Asia/Kolkata",
        location: str = "Delhi"
    ) -> Dict:
        """Get a comprehensive summary dictionary of Panchang data."""
        panchang = self.get_panchang(dt, latitude, longitude, timezone, location)

        # Format Choghadiya for display
        def format_choghadiya(chog_list):
            return [
                {
                    "name": c.name,
                    "hindi": c.hindi,
                    "start": c.start_time.strftime("%H:%M"),
                    "end": c.end_time.strftime("%H:%M"),
                    "quality": c.quality,
                    "is_auspicious": c.is_auspicious
                }
                for c in chog_list
            ]

        return {
            "date": panchang.date.strftime("%Y-%m-%d"),
            "date_hindi": self._format_date_hindi(panchang.date),
            "location": panchang.location,

            # Five Limbs
            "vara": {
                "name": panchang.vara.english,
                "hindi": panchang.vara.hindi,
                "lord": panchang.vara.lord,
                "is_auspicious": panchang.vara.is_auspicious
            },
            "tithi": {
                "name": panchang.tithi.name,
                "hindi": panchang.tithi.hindi,
                "number": panchang.tithi.number,
                "paksha": panchang.tithi.paksha,
                "paksha_hindi": panchang.tithi.paksha_hindi,
                "lord": panchang.tithi.lord,
                "is_rikta": panchang.tithi.is_rikta,
                "percentage_elapsed": panchang.tithi.percentage_elapsed
            },
            "nakshatra": {
                "name": panchang.nakshatra.name,
                "hindi": panchang.nakshatra.hindi,
                "lord": panchang.nakshatra.lord,
                "deity": panchang.nakshatra.deity,
                "pada": panchang.nakshatra.pada,
                "percentage_elapsed": panchang.nakshatra.percentage_elapsed
            },
            "yoga": {
                "name": panchang.yoga.name,
                "hindi": panchang.yoga.hindi,
                "is_inauspicious": panchang.yoga.is_inauspicious,
                "description": panchang.yoga.description
            },
            "karana": {
                "name": panchang.karana.name,
                "hindi": panchang.karana.hindi,
                "type": panchang.karana.type,
                "is_auspicious": panchang.karana.is_auspicious,
                "is_vishti": panchang.karana.is_vishti
            },

            # Sun/Moon Timings
            "timings": {
                "sunrise": panchang.timings.sunrise.strftime("%H:%M"),
                "sunset": panchang.timings.sunset.strftime("%H:%M"),
                "moonrise": panchang.timings.moonrise.strftime("%H:%M") if panchang.timings.moonrise else None,
                "moonset": panchang.timings.moonset.strftime("%H:%M") if panchang.timings.moonset else None,
                "day_duration": str(panchang.timings.day_duration).split('.')[0]
            },

            # Moon Sign
            "moon_rashi": {
                "name": panchang.moon_rashi,
                "hindi": panchang.moon_rashi_hindi
            },

            # Choghadiya
            "day_choghadiya": format_choghadiya(panchang.day_choghadiya),
            "night_choghadiya": format_choghadiya(panchang.night_choghadiya),
            "current_choghadiya": {
                "name": panchang.current_choghadiya.name,
                "hindi": panchang.current_choghadiya.hindi,
                "quality": panchang.current_choghadiya.quality,
                "is_auspicious": panchang.current_choghadiya.is_auspicious
            } if panchang.current_choghadiya else None,

            # Inauspicious Periods
            "rahu_kaal": {
                "start": panchang.rahu_kaal.start_time.strftime("%H:%M"),
                "end": panchang.rahu_kaal.end_time.strftime("%H:%M"),
                "hindi": panchang.rahu_kaal.hindi
            },
            "yamaghantaka": {
                "start": panchang.yamaghantaka.start_time.strftime("%H:%M"),
                "end": panchang.yamaghantaka.end_time.strftime("%H:%M"),
                "hindi": panchang.yamaghantaka.hindi
            },
            "gulika_kaal": {
                "start": panchang.gulika_kaal.start_time.strftime("%H:%M"),
                "end": panchang.gulika_kaal.end_time.strftime("%H:%M"),
                "hindi": panchang.gulika_kaal.hindi
            },
            "abhijit_muhurta": {
                "start": panchang.abhijit_muhurta[0].strftime("%H:%M"),
                "end": panchang.abhijit_muhurta[1].strftime("%H:%M")
            } if panchang.abhijit_muhurta else None,

            # Auspiciousness
            "auspiciousness": {
                "is_shubh_din": panchang.auspiciousness.is_shubh_din,
                "score": panchang.auspiciousness.score,
                "positive_factors": panchang.auspiciousness.positive_factors,
                "negative_factors": panchang.auspiciousness.negative_factors,
                "recommendations": panchang.auspiciousness.recommendations
            },

            # Astronomical
            "ayanamsa": round(panchang.ayanamsa, 4),
            "moon_longitude": round(panchang.moon_longitude, 4),
            "sun_longitude": round(panchang.sun_longitude, 4)
        }

    def _format_date_hindi(self, dt: datetime) -> str:
        """Format date in Hindi style."""
        months_hindi = [
            "जनवरी", "फरवरी", "मार्च", "अप्रैल", "मई", "जून",
            "जुलाई", "अगस्त", "सितंबर", "अक्टूबर", "नवंबर", "दिसंबर"
        ]
        return f"{dt.day} {months_hindi[dt.month - 1]} {dt.year}"

    def get_tithi_for_date(
        self,
        dt: datetime,
        timezone: str = "Asia/Kolkata"
    ) -> TithiData:
        """Get just the Tithi for a date."""
        jd = self.calculator.datetime_to_jd(dt, timezone)
        sun_pos = self.calculator.get_planet_position(Planet.SUN, jd)
        moon_pos = self.calculator.get_planet_position(Planet.MOON, jd)
        return self._calculate_tithi(sun_pos["longitude"], moon_pos["longitude"], dt, timezone)

    def get_nakshatra_for_date(
        self,
        dt: datetime,
        timezone: str = "Asia/Kolkata"
    ) -> Dict:
        """Get Moon's nakshatra for a date."""
        jd = self.calculator.datetime_to_jd(dt, timezone)
        moon_pos = self.calculator.get_planet_position(Planet.MOON, jd)
        return {
            "nakshatra": moon_pos["nakshatra"],
            "nakshatra_num": moon_pos["nakshatra_num"],
            "nakshatra_lord": moon_pos["nakshatra_lord"],
            "pada": moon_pos["pada"]
        }

    def find_tithi_start_time(
        self,
        target_tithi: int,
        start_date: datetime,
        end_date: datetime,
        timezone: str = "Asia/Kolkata"
    ) -> Optional[datetime]:
        """
        Find when a specific tithi starts within a date range.
        Uses binary search for efficiency.
        """
        tz = pytz.timezone(timezone)

        if start_date.tzinfo is None:
            start_date = tz.localize(start_date)
        if end_date.tzinfo is None:
            end_date = tz.localize(end_date)

        current = start_date
        step = timedelta(hours=1)

        while current < end_date:
            tithi = self.get_tithi_for_date(current, timezone)
            if tithi.number == target_tithi:
                # Binary search to find exact start
                low = current - step
                high = current

                while (high - low).total_seconds() > 60:
                    mid = low + (high - low) / 2
                    mid_tithi = self.get_tithi_for_date(mid, timezone)
                    if mid_tithi.number == target_tithi:
                        high = mid
                    else:
                        low = mid

                return high

            current += step

        return None

    def is_time_in_rahu_kaal(
        self,
        dt: datetime,
        latitude: float = 28.6139,
        longitude: float = 77.2090,
        timezone: str = "Asia/Kolkata"
    ) -> bool:
        """Check if a given time falls within Rahu Kaal."""
        panchang = self.get_panchang(dt, latitude, longitude, timezone)
        return panchang.rahu_kaal.start_time <= dt <= panchang.rahu_kaal.end_time

    def get_auspicious_times(
        self,
        dt: datetime,
        latitude: float = 28.6139,
        longitude: float = 77.2090,
        timezone: str = "Asia/Kolkata"
    ) -> List[Dict]:
        """Get list of auspicious time windows for the day."""
        panchang = self.get_panchang(dt, latitude, longitude, timezone)

        auspicious_windows = []

        # Add Abhijit Muhurta
        if panchang.abhijit_muhurta:
            auspicious_windows.append({
                "name": "Abhijit Muhurta",
                "hindi": "अभिजित मुहूर्त",
                "start": panchang.abhijit_muhurta[0].strftime("%H:%M"),
                "end": panchang.abhijit_muhurta[1].strftime("%H:%M"),
                "quality": "Most Auspicious",
                "description": "Best time for all auspicious works / सभी शुभ कार्यों के लिए सर्वोत्तम समय"
            })

        # Add auspicious Choghadiyas
        for chog in panchang.day_choghadiya:
            if chog.is_auspicious:
                # Check if it overlaps with Rahu Kaal
                overlaps_rahu = (
                    chog.start_time < panchang.rahu_kaal.end_time and
                    chog.end_time > panchang.rahu_kaal.start_time
                )
                if not overlaps_rahu:
                    auspicious_windows.append({
                        "name": f"{chog.name} Choghadiya",
                        "hindi": f"{chog.hindi} चौघड़िया",
                        "start": chog.start_time.strftime("%H:%M"),
                        "end": chog.end_time.strftime("%H:%M"),
                        "quality": chog.quality,
                        "description": f"Day Choghadiya - {chog.nature}"
                    })

        return auspicious_windows
