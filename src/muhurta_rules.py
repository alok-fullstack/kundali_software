"""
Muhurta Rules - Classical inauspicious period calculations and event-specific rules

Based on authentic Vedic texts:
- Muhurta Chintamani by Rama Daivagnya
- Brihat Samhita by Varahamihira
- Kalaprakashika
- Phaladeepika by Mantreshwara
"""

from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from enum import Enum

from .config import (
    RAHU_KALA_SEQUENCE,
    YAMAGHANTAKA_SEQUENCE,
    GULIKA_SEQUENCE,
    MARRIAGE_MUHURTA_RULES,
    CAREER_MUHURTA_RULES,
    PROPERTY_MUHURTA_RULES,
    GRIHA_PRAVESH_MUHURTA_RULES,
    TRAVEL_MUHURTA_RULES,
    NAKSHATRA_CLASSIFICATION,
    TARABALA_NAMES,
    CHANDRABALA_FAVORABLE_HOUSES,
)


class EventType(Enum):
    """Supported event types for Muhurta selection."""
    MARRIAGE = "marriage"
    CAREER = "career"
    PROPERTY = "property"
    GRIHA_PRAVESH = "griha_pravesh"
    TRAVEL = "travel"
    EDUCATION = "education"
    MEDICAL = "medical"
    NAMING = "naming"
    GENERAL = "general"


@dataclass
class InauspiciousPeriod:
    """Represents an inauspicious time period."""
    name: str
    hindi: str
    start_time: datetime
    end_time: datetime
    severity: str
    description: str


def calculate_rahu_kala(
    sunrise: datetime,
    sunset: datetime,
    weekday: int
) -> Tuple[datetime, datetime]:
    """
    Calculate Rahu Kala for a given day.

    Rahu Kala is an inauspicious period that occurs daily,
    varying by weekday. The day is divided into 8 equal parts.

    Memory aid: "Mother Saw Father Wearing The Turban on Saturday"
    - Monday: 2nd part
    - Saturday: 3rd part
    - Friday: 4th part
    - Wednesday: 5th part
    - Thursday: 6th part
    - Tuesday: 7th part
    - Sunday: 8th part

    Args:
        sunrise: Sunrise time
        sunset: Sunset time
        weekday: Python weekday (0=Monday, 6=Sunday)

    Returns:
        Tuple of (start_time, end_time) for Rahu Kala
    """
    adjusted_weekday = (weekday + 1) % 7

    day_duration = (sunset - sunrise).total_seconds()
    part_duration = day_duration / 8

    rahu_part = RAHU_KALA_SEQUENCE[adjusted_weekday]

    start = sunrise + timedelta(seconds=(rahu_part - 1) * part_duration)
    end = start + timedelta(seconds=part_duration)

    return start, end


def calculate_yamaghantaka(
    sunrise: datetime,
    sunset: datetime,
    weekday: int
) -> Tuple[datetime, datetime]:
    """
    Calculate Yamaghantaka (Yama Ghantaka) period.

    Yamaghantaka is an inauspicious period ruled by Yama,
    the god of death. Important activities should be avoided.

    Args:
        sunrise: Sunrise time
        sunset: Sunset time
        weekday: Python weekday (0=Monday, 6=Sunday)

    Returns:
        Tuple of (start_time, end_time) for Yamaghantaka
    """
    adjusted_weekday = (weekday + 1) % 7

    day_duration = (sunset - sunrise).total_seconds()
    part_duration = day_duration / 8

    yama_part = YAMAGHANTAKA_SEQUENCE[adjusted_weekday]

    start = sunrise + timedelta(seconds=(yama_part - 1) * part_duration)
    end = start + timedelta(seconds=part_duration)

    return start, end


def calculate_gulika_kala(
    sunrise: datetime,
    sunset: datetime,
    weekday: int
) -> Tuple[datetime, datetime]:
    """
    Calculate Gulika Kala (also called Mandi Kala).

    Gulika/Mandi is considered the son of Saturn.
    This period is inauspicious for auspicious activities.

    Args:
        sunrise: Sunrise time
        sunset: Sunset time
        weekday: Python weekday (0=Monday, 6=Sunday)

    Returns:
        Tuple of (start_time, end_time) for Gulika Kala
    """
    adjusted_weekday = (weekday + 1) % 7

    day_duration = (sunset - sunrise).total_seconds()
    part_duration = day_duration / 8

    gulika_part = GULIKA_SEQUENCE[adjusted_weekday]

    start = sunrise + timedelta(seconds=(gulika_part - 1) * part_duration)
    end = start + timedelta(seconds=part_duration)

    return start, end


def calculate_durmuhurta(
    sunrise: datetime,
    sunset: datetime
) -> List[Tuple[datetime, datetime]]:
    """
    Calculate Durmuhurta periods.

    Durmuhurta means "bad muhurta". There are two durmuhurtas each day:
    - Day Durmuhurta: 8th muhurta from sunrise
    - Night Durmuhurta: varies (15th muhurta from sunrise typically)

    A muhurta is approximately 48 minutes (day divided into 30 muhurtas).

    Args:
        sunrise: Sunrise time
        sunset: Sunset time

    Returns:
        List of (start_time, end_time) tuples for Durmuhurta periods
    """
    day_duration = (sunset - sunrise).total_seconds()
    muhurta_duration = day_duration / 15

    durmuhurtas = []

    day_dm_start = sunrise + timedelta(seconds=7 * muhurta_duration)
    day_dm_end = day_dm_start + timedelta(seconds=muhurta_duration)
    durmuhurtas.append((day_dm_start, day_dm_end))

    late_dm_start = sunrise + timedelta(seconds=10 * muhurta_duration)
    late_dm_end = late_dm_start + timedelta(seconds=muhurta_duration)
    durmuhurtas.append((late_dm_start, late_dm_end))

    return durmuhurtas


def calculate_abhijit_muhurta(
    sunrise: datetime,
    sunset: datetime
) -> Tuple[datetime, datetime]:
    """
    Calculate Abhijit Muhurta - the most auspicious muhurta of the day.

    Abhijit means "victorious". This muhurta occurs around midday
    (local noon) and is considered excellent for all auspicious works.

    It's the 8th muhurta from sunrise, spanning approximately
    24 minutes before and after local noon.

    Args:
        sunrise: Sunrise time
        sunset: Sunset time

    Returns:
        Tuple of (start_time, end_time) for Abhijit Muhurta
    """
    day_duration = (sunset - sunrise).total_seconds()
    muhurta_duration = day_duration / 15

    mid_day = sunrise + timedelta(seconds=day_duration / 2)
    start = mid_day - timedelta(seconds=muhurta_duration / 2)
    end = mid_day + timedelta(seconds=muhurta_duration / 2)

    return start, end


def get_all_inauspicious_periods(
    sunrise: datetime,
    sunset: datetime,
    weekday: int
) -> List[InauspiciousPeriod]:
    """
    Get all inauspicious periods for a day.

    Args:
        sunrise: Sunrise time
        sunset: Sunset time
        weekday: Python weekday (0=Monday, 6=Sunday)

    Returns:
        List of InauspiciousPeriod objects
    """
    periods = []

    rahu_start, rahu_end = calculate_rahu_kala(sunrise, sunset, weekday)
    periods.append(InauspiciousPeriod(
        name="Rahu Kala",
        hindi="राहु काल",
        start_time=rahu_start,
        end_time=rahu_end,
        severity="high",
        description="Period ruled by Rahu. Avoid starting important works."
    ))

    yama_start, yama_end = calculate_yamaghantaka(sunrise, sunset, weekday)
    periods.append(InauspiciousPeriod(
        name="Yamaghantaka",
        hindi="यमघण्टक",
        start_time=yama_start,
        end_time=yama_end,
        severity="medium",
        description="Period ruled by Yama. Avoid auspicious ceremonies."
    ))

    gulika_start, gulika_end = calculate_gulika_kala(sunrise, sunset, weekday)
    periods.append(InauspiciousPeriod(
        name="Gulika Kala",
        hindi="गुलिक काल",
        start_time=gulika_start,
        end_time=gulika_end,
        severity="medium",
        description="Period of Gulika/Mandi. Avoid starting new ventures."
    ))

    durmuhurtas = calculate_durmuhurta(sunrise, sunset)
    for i, (dm_start, dm_end) in enumerate(durmuhurtas):
        periods.append(InauspiciousPeriod(
            name=f"Durmuhurta {i+1}",
            hindi="दुर्मुहूर्त",
            start_time=dm_start,
            end_time=dm_end,
            severity="low",
            description="Inauspicious muhurta. Avoid if possible."
        ))

    return periods


def is_time_in_inauspicious_period(
    check_time: datetime,
    inauspicious_periods: List[InauspiciousPeriod],
    min_severity: str = "low"
) -> Tuple[bool, Optional[InauspiciousPeriod]]:
    """
    Check if a given time falls within an inauspicious period.

    Args:
        check_time: Time to check
        inauspicious_periods: List of inauspicious periods
        min_severity: Minimum severity to consider ("low", "medium", "high")

    Returns:
        Tuple of (is_inauspicious, period_if_found)
    """
    severity_order = {"low": 1, "medium": 2, "high": 3}
    min_sev_num = severity_order.get(min_severity, 1)

    for period in inauspicious_periods:
        period_sev = severity_order.get(period.severity, 1)
        if period_sev >= min_sev_num:
            if period.start_time <= check_time <= period.end_time:
                return True, period

    return False, None


def get_event_rules(event_type: EventType) -> Dict:
    """
    Get Muhurta rules for a specific event type.

    Args:
        event_type: Type of event

    Returns:
        Dictionary of rules for that event type
    """
    rules_map = {
        EventType.MARRIAGE: MARRIAGE_MUHURTA_RULES,
        EventType.CAREER: CAREER_MUHURTA_RULES,
        EventType.PROPERTY: PROPERTY_MUHURTA_RULES,
        EventType.GRIHA_PRAVESH: GRIHA_PRAVESH_MUHURTA_RULES,
        EventType.TRAVEL: TRAVEL_MUHURTA_RULES,
    }

    if event_type in rules_map:
        return rules_map[event_type]

    return {
        "favorable_nakshatras": [0, 3, 6, 7, 11, 12, 14, 20, 21, 24, 26],
        "unfavorable_nakshatras": [5, 8, 17, 18],
        "favorable_tithis": [2, 3, 5, 7, 10, 11, 12, 13],
        "unfavorable_tithis": [4, 9, 14, 30],
        "unfavorable_yogas": [0, 5, 8, 9, 12, 14, 16, 18, 26],
        "favorable_weekdays": [1, 3, 4, 5],
        "unfavorable_weekdays": [2, 6],
        "prefer_shukla_paksha": True,
    }


def calculate_tarabala(
    birth_nakshatra_num: int,
    current_nakshatra_num: int
) -> Tuple[int, str, str, int]:
    """
    Calculate Tarabala (Star Strength).

    Tarabala measures the compatibility between birth nakshatra
    and current nakshatra using a 9-fold cycle (Tara chakra).

    The 27 nakshatras are divided into 3 cycles of 9 each.
    Each position in the cycle has different significance.

    Args:
        birth_nakshatra_num: Birth Moon nakshatra (0-26)
        current_nakshatra_num: Current Moon nakshatra (0-26)

    Returns:
        Tuple of (tara_number, tara_name, effect, score)
    """
    distance = (current_nakshatra_num - birth_nakshatra_num) % 27

    tara_num = (distance % 9) + 1

    tara_info = TARABALA_NAMES[tara_num]

    return (
        tara_num,
        tara_info["name"],
        tara_info["effect"],
        tara_info["score"]
    )


def calculate_chandrabala(
    natal_moon_rashi_num: int,
    transit_moon_rashi_num: int
) -> Tuple[int, int, str]:
    """
    Calculate Chandrabala (Moon Strength).

    Chandrabala measures the transit Moon's position from natal Moon.
    Certain houses from the Moon are favorable for activities.

    Favorable houses: 1, 3, 6, 7, 10, 11 (from Moon)
    Unfavorable houses: 4, 8, 12 (from Moon)

    Args:
        natal_moon_rashi_num: Birth Moon rashi (0-11)
        transit_moon_rashi_num: Current Moon rashi (0-11)

    Returns:
        Tuple of (house_from_moon, score, effect_description)
    """
    house = ((transit_moon_rashi_num - natal_moon_rashi_num) % 12) + 1

    score_map = {
        1: (8, "Self house - favorable for personal matters"),
        2: (3, "Wealth house - neutral"),
        3: (10, "Courage house - excellent for initiatives"),
        4: (0, "Happiness house - avoid important activities"),
        5: (5, "Intelligence house - moderate"),
        6: (10, "Victory house - excellent for competitive matters"),
        7: (10, "Partnership house - excellent for relationships"),
        8: (0, "Obstacles house - avoid starting new works"),
        9: (5, "Fortune house - moderate"),
        10: (10, "Karma house - excellent for career matters"),
        11: (10, "Gains house - excellent for financial matters"),
        12: (0, "Loss house - avoid important decisions"),
    }

    score, effect = score_map[house]
    return house, score, effect


def is_nakshatra_favorable(
    nakshatra_num: int,
    event_type: EventType
) -> Tuple[bool, str]:
    """
    Check if a nakshatra is favorable for an event type.

    Args:
        nakshatra_num: Nakshatra number (0-26)
        event_type: Type of event

    Returns:
        Tuple of (is_favorable, reason)
    """
    rules = get_event_rules(event_type)

    if nakshatra_num in rules.get("favorable_nakshatras", []):
        return True, "Favorable nakshatra for this event"

    if nakshatra_num in rules.get("unfavorable_nakshatras", []):
        return False, "Unfavorable nakshatra for this event"

    return True, "Neutral nakshatra"


def get_nakshatra_classification(nakshatra_num: int) -> List[str]:
    """
    Get the classification(s) of a nakshatra.

    Args:
        nakshatra_num: Nakshatra number (0-26)

    Returns:
        List of classifications (e.g., ["Fixed", "Soft"])
    """
    classifications = []
    for classification, nakshatras in NAKSHATRA_CLASSIFICATION.items():
        if nakshatra_num in nakshatras:
            classifications.append(classification)
    return classifications if classifications else ["General"]


def calculate_panchaka(
    nakshatra_num: int,
    weekday: int
) -> Tuple[bool, Optional[str]]:
    """
    Check for Panchaka dosha (5-fold defect).

    Panchaka occurs when certain combinations of nakshatra and
    weekday align, creating inauspicious conditions.

    There are 5 types of Panchaka:
    1. Mrityu Panchaka (death)
    2. Agni Panchaka (fire)
    3. Raja Panchaka (king's trouble)
    4. Chora Panchaka (theft)
    5. Roga Panchaka (disease)

    Args:
        nakshatra_num: Current nakshatra (0-26)
        weekday: Python weekday (0=Monday)

    Returns:
        Tuple of (has_panchaka, panchaka_type)
    """
    nakshatra_value = nakshatra_num + 1
    weekday_value = weekday + 1

    panchaka_sum = (nakshatra_value + weekday_value) % 9

    panchaka_map = {
        1: "Mrityu Panchaka",
        2: "Agni Panchaka",
        4: "Raja Panchaka",
        6: "Chora Panchaka",
        8: "Roga Panchaka",
    }

    if panchaka_sum in panchaka_map:
        return True, panchaka_map[panchaka_sum]

    return False, None


def find_best_time_window(
    sunrise: datetime,
    sunset: datetime,
    weekday: int,
    avoid_high_severity: bool = True
) -> Tuple[datetime, datetime]:
    """
    Find the best time window avoiding inauspicious periods.

    Args:
        sunrise: Sunrise time
        sunset: Sunset time
        weekday: Python weekday
        avoid_high_severity: If True, only avoid high severity periods

    Returns:
        Tuple of (best_start, best_end) time
    """
    periods = get_all_inauspicious_periods(sunrise, sunset, weekday)

    if avoid_high_severity:
        periods = [p for p in periods if p.severity == "high"]

    periods.sort(key=lambda p: p.start_time)

    windows = []

    morning_end = sunrise + timedelta(hours=1)
    if all(not (p.start_time <= morning_end <= p.end_time) for p in periods):
        windows.append((sunrise + timedelta(hours=1), periods[0].start_time if periods else sunset))

    for i in range(len(periods) - 1):
        gap_start = periods[i].end_time
        gap_end = periods[i + 1].start_time
        if (gap_end - gap_start).total_seconds() > 3600:
            windows.append((gap_start, gap_end))

    if periods:
        last_end = periods[-1].end_time
        if last_end < sunset - timedelta(hours=1):
            windows.append((last_end, sunset - timedelta(hours=1)))

    if not windows:
        return sunrise + timedelta(hours=1), sunset - timedelta(hours=1)

    windows.sort(key=lambda w: (w[1] - w[0]).total_seconds(), reverse=True)
    return windows[0]


def get_hora_lord(dt: datetime, sunrise: datetime) -> str:
    """
    Calculate the planetary Hora lord for a given time.

    Each hour (Hora) of the day is ruled by a planet.
    The sequence follows: Sun, Venus, Mercury, Moon, Saturn, Jupiter, Mars
    The first hora after sunrise is ruled by the day's lord.

    Args:
        dt: Time to check
        sunrise: Sunrise time for that day

    Returns:
        Name of the Hora lord planet
    """
    hora_sequence = ["Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars"]

    weekday = dt.weekday()
    weekday_lords = ["Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Sun"]
    day_lord = weekday_lords[weekday]

    start_index = hora_sequence.index(day_lord)

    time_since_sunrise = (dt - sunrise).total_seconds()
    hora_number = int(time_since_sunrise / 3600) % 24

    hora_index = (start_index + hora_number) % 7

    return hora_sequence[hora_index]


def is_hora_favorable(
    hora_lord: str,
    event_type: EventType
) -> Tuple[bool, str]:
    """
    Check if the current Hora is favorable for an event type.

    Args:
        hora_lord: Current Hora lord planet
        event_type: Type of event

    Returns:
        Tuple of (is_favorable, reason)
    """
    hora_event_map = {
        EventType.MARRIAGE: {
            "favorable": ["Venus", "Jupiter", "Moon"],
            "unfavorable": ["Saturn", "Mars"]
        },
        EventType.CAREER: {
            "favorable": ["Sun", "Jupiter", "Mercury"],
            "unfavorable": ["Saturn"]
        },
        EventType.PROPERTY: {
            "favorable": ["Jupiter", "Venus", "Moon"],
            "unfavorable": ["Mars"]
        },
        EventType.TRAVEL: {
            "favorable": ["Mercury", "Moon", "Venus"],
            "unfavorable": ["Saturn", "Mars"]
        },
    }

    rules = hora_event_map.get(event_type, {"favorable": ["Jupiter", "Venus"], "unfavorable": ["Saturn"]})

    if hora_lord in rules["favorable"]:
        return True, f"{hora_lord} Hora is favorable for {event_type.value}"

    if hora_lord in rules["unfavorable"]:
        return False, f"{hora_lord} Hora is unfavorable for {event_type.value}"

    return True, f"{hora_lord} Hora is neutral"
