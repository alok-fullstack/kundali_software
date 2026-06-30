"""
Prashna Kundali (Horary Astrology) Module

Based on authentic Vedic texts:
- Prashna Marga by Harihara
- Prashna Tantra
- Tajika Neelakanthi
- Daivagya Vallabha

Implements:
1. Prashna chart generation
2. Question-specific analysis
3. Timing predictions
4. Arudha calculations
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from enum import Enum
import math


# =============================================================================
# ENUMS AND CONSTANTS
# =============================================================================

class QuestionCategory(Enum):
    """Categories of questions"""
    GENERAL = "general"
    MARRIAGE = "marriage"
    CAREER = "career"
    HEALTH = "health"
    TRAVEL = "travel"
    LOST_ITEM = "lost_item"
    LITIGATION = "litigation"
    EDUCATION = "education"
    FINANCE = "finance"
    PREGNANCY = "pregnancy"


# House significations for different questions
QUESTION_HOUSES = {
    QuestionCategory.GENERAL: [1, 10],
    QuestionCategory.MARRIAGE: [7, 2, 11],
    QuestionCategory.CAREER: [10, 6, 2, 11],
    QuestionCategory.HEALTH: [1, 6, 8],
    QuestionCategory.TRAVEL: [3, 9, 12],
    QuestionCategory.LOST_ITEM: [2, 4, 7],
    QuestionCategory.LITIGATION: [6, 7, 8],
    QuestionCategory.EDUCATION: [4, 5, 9],
    QuestionCategory.FINANCE: [2, 5, 11],
    QuestionCategory.PREGNANCY: [5, 1, 7]
}

# Mook Prashna indicators (when querent is silent)
MOOK_INDICATORS = {
    "FIRST_WORD": "First word spoken indicates house",
    "DIRECTION": "Direction faced indicates result",
    "BODY_TOUCH": "Body part touched indicates matter"
}

# Sign lords
SIGN_LORDS = {
    0: "MARS", 1: "VENUS", 2: "MERCURY", 3: "MOON",
    4: "SUN", 5: "MERCURY", 6: "VENUS", 7: "MARS",
    8: "JUPITER", 9: "SATURN", 10: "SATURN", 11: "JUPITER"
}

# Nakshatra data for Prashna
NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta",
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class PrashnaChart:
    """Prashna (Horary) chart data"""
    question_time: datetime
    location: str
    latitude: float
    longitude: float
    timezone: str
    lagna_sign: str
    lagna_degree: float
    moon_sign: str
    moon_nakshatra: str
    moon_nakshatra_pada: int
    planet_positions: Dict[str, Any]
    houses: Dict[int, Dict[str, Any]]


@dataclass
class ArudhaResult:
    """Arudha (significator) calculation"""
    arudha_house: int
    arudha_sign: str
    arudha_lord: str
    arudha_lord_house: int
    strength: str  # Strong, Moderate, Weak


@dataclass
class TimingResult:
    """Timing prediction for answer"""
    will_happen: bool
    timeframe: str
    timeframe_hindi: str
    timing_basis: str
    confidence: str  # High, Moderate, Low


@dataclass
class PrashnaAnalysis:
    """Complete Prashna analysis result"""
    question_category: QuestionCategory
    primary_house: int
    significators: List[str]
    lagna_analysis: Dict[str, Any]
    moon_analysis: Dict[str, Any]
    arudha: ArudhaResult
    timing: TimingResult
    answer: str
    answer_hindi: str
    confidence_level: int  # 0-100
    favorable_factors: List[str]
    unfavorable_factors: List[str]
    detailed_interpretation: str
    detailed_interpretation_hindi: str


# =============================================================================
# PRASHNA CALCULATOR
# =============================================================================

class PrashnaCalculator:
    """
    Prashna (Horary Astrology) Calculator.

    Based on Prashna Marga principles.
    """

    RASHI_NAMES = ["Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
                   "Tula", "Vrishchika", "Dhanu", "Makara", "Kumbha", "Meena"]

    RASHI_HINDI = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या",
                   "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"]

    # Element mapping
    ELEMENTS = {
        "FIRE": [0, 4, 8],    # Aries, Leo, Sagittarius
        "EARTH": [1, 5, 9],   # Taurus, Virgo, Capricorn
        "AIR": [2, 6, 10],    # Gemini, Libra, Aquarius
        "WATER": [3, 7, 11]   # Cancer, Scorpio, Pisces
    }

    # Quality mapping
    QUALITIES = {
        "CARDINAL": [0, 3, 6, 9],    # Moveable
        "FIXED": [1, 4, 7, 10],      # Fixed
        "MUTABLE": [2, 5, 8, 11]     # Dual
    }

    def __init__(self, prashna_data: Dict[str, Any]):
        """
        Initialize with Prashna chart data.

        Args:
            prashna_data: Dictionary containing chart details
        """
        self.chart = prashna_data
        self.planets = prashna_data.get("planets", {})
        self.lagna = prashna_data.get("lagna", {})

    def _get_lagna_num(self) -> int:
        """Get lagna rashi number (0-11)"""
        return self.lagna.get("rashi_num", 0)

    def _get_house_sign_num(self, house: int) -> int:
        """Get sign number for a house"""
        return (self._get_lagna_num() + house - 1) % 12

    def _get_house_lord(self, house: int) -> str:
        """Get lord of a house"""
        sign_num = self._get_house_sign_num(house)
        return SIGN_LORDS[sign_num]

    def _get_planet_house(self, planet: str) -> int:
        """Get house number (1-12) where planet is placed"""
        planet_data = self.planets.get(planet, {})
        planet_sign = planet_data.get("rashi_num", 0)
        return ((planet_sign - self._get_lagna_num()) % 12) + 1

    def _is_benefic(self, planet: str) -> bool:
        """Check if planet is natural benefic"""
        return planet in ["JUPITER", "VENUS", "MOON", "MERCURY"]

    def _is_malefic(self, planet: str) -> bool:
        """Check if planet is natural malefic"""
        return planet in ["SATURN", "MARS", "RAHU", "KETU", "SUN"]

    def _analyze_lagna(self) -> Dict[str, Any]:
        """Analyze Lagna for Prashna"""
        lagna_num = self._get_lagna_num()
        lagna_lord = SIGN_LORDS[lagna_num]
        lagna_lord_house = self._get_planet_house(lagna_lord)

        # Check planets in lagna
        planets_in_lagna = []
        for planet in ["SUN", "MOON", "MARS", "MERCURY", "JUPITER", "VENUS", "SATURN", "RAHU", "KETU"]:
            if self._get_planet_house(planet) == 1:
                planets_in_lagna.append(planet)

        # Assess lagna strength
        strength = "Moderate"
        if lagna_lord_house in [1, 4, 5, 7, 9, 10]:
            strength = "Strong"
        elif lagna_lord_house in [6, 8, 12]:
            strength = "Weak"

        # Benefics in lagna is good
        benefic_count = sum(1 for p in planets_in_lagna if self._is_benefic(p))
        if benefic_count >= 2:
            strength = "Strong"

        return {
            "sign": self.RASHI_NAMES[lagna_num],
            "sign_hindi": self.RASHI_HINDI[lagna_num],
            "lord": lagna_lord,
            "lord_house": lagna_lord_house,
            "planets_in_lagna": planets_in_lagna,
            "strength": strength,
            "interpretation": self._get_lagna_interpretation(lagna_num, strength)
        }

    def _get_lagna_interpretation(self, lagna_num: int, strength: str) -> str:
        """Get interpretation based on lagna"""
        element = None
        for elem, signs in self.ELEMENTS.items():
            if lagna_num in signs:
                element = elem
                break

        quality = None
        for qual, signs in self.QUALITIES.items():
            if lagna_num in signs:
                quality = qual
                break

        interp = f"Lagna in {self.RASHI_NAMES[lagna_num]} ({element}, {quality}). "

        if strength == "Strong":
            interp += "Strong lagna indicates favorable outcome."
        elif strength == "Weak":
            interp += "Weak lagna suggests obstacles or delays."
        else:
            interp += "Moderate lagna - mixed results expected."

        return interp

    def _analyze_moon(self) -> Dict[str, Any]:
        """Analyze Moon position for Prashna"""
        moon_data = self.planets.get("MOON", {})
        moon_house = self._get_planet_house("MOON")
        moon_sign = moon_data.get("rashi_num", 0)
        moon_nakshatra = moon_data.get("nakshatra", "")
        moon_degree = moon_data.get("degree", 0)

        # Calculate pada
        nak_start = (moon_sign * 30) + ((moon_degree % 30) // (30/9))
        pada = int((moon_degree % (360/27)) // (360/108)) + 1
        if pada > 4:
            pada = 4

        # Moon in good houses
        is_favorable = moon_house in [1, 2, 3, 4, 5, 7, 9, 10, 11]

        # Paksha (waxing/waning)
        sun_data = self.planets.get("SUN", {})
        sun_degree = sun_data.get("longitude", 0)
        moon_degree_abs = moon_data.get("longitude", 0)
        diff = (moon_degree_abs - sun_degree) % 360

        paksha = "Shukla" if diff < 180 else "Krishna"
        is_waxing = paksha == "Shukla"

        return {
            "house": moon_house,
            "sign": self.RASHI_NAMES[moon_sign],
            "sign_hindi": self.RASHI_HINDI[moon_sign],
            "nakshatra": moon_nakshatra,
            "pada": pada,
            "paksha": paksha,
            "is_waxing": is_waxing,
            "is_favorable": is_favorable,
            "interpretation": self._get_moon_interpretation(moon_house, is_waxing)
        }

    def _get_moon_interpretation(self, house: int, is_waxing: bool) -> str:
        """Get interpretation based on Moon"""
        interp = f"Moon in {house}th house. "

        if house in [1, 4, 7, 10]:  # Kendra
            interp += "Moon in Kendra - query is significant. "
        elif house in [5, 9]:  # Trikona
            interp += "Moon in Trikona - auspicious for the question. "
        elif house in [6, 8, 12]:  # Dusthana
            interp += "Moon in Dusthana - obstacles indicated. "

        if is_waxing:
            interp += "Waxing Moon (Shukla Paksha) - favorable for new beginnings."
        else:
            interp += "Waning Moon (Krishna Paksha) - better for endings or conclusions."

        return interp

    def _calculate_arudha(self, karaka_house: int) -> ArudhaResult:
        """
        Calculate Arudha Lagna for the question.

        Arudha = count from house lord to house, then same from lord.
        """
        house_lord = self._get_house_lord(karaka_house)
        lord_house = self._get_planet_house(house_lord)

        # Distance from karaka house to lord
        distance = lord_house - karaka_house
        if distance < 0:
            distance += 12

        # Arudha = same distance from lord
        arudha_house = ((lord_house + distance - 1) % 12) + 1

        # Adjust if arudha falls in 1st or 7th from karaka
        if arudha_house == karaka_house:
            arudha_house = ((arudha_house + 9) % 12) + 1
        elif arudha_house == ((karaka_house + 6) % 12) + 1:
            arudha_house = ((arudha_house + 9) % 12) + 1

        arudha_sign_num = self._get_house_sign_num(arudha_house)
        arudha_lord = SIGN_LORDS[arudha_sign_num]
        arudha_lord_house = self._get_planet_house(arudha_lord)

        # Assess strength
        strength = "Moderate"
        if arudha_lord_house in [1, 4, 5, 7, 9, 10, 11]:
            strength = "Strong"
        elif arudha_lord_house in [6, 8, 12]:
            strength = "Weak"

        return ArudhaResult(
            arudha_house=arudha_house,
            arudha_sign=self.RASHI_NAMES[arudha_sign_num],
            arudha_lord=arudha_lord,
            arudha_lord_house=arudha_lord_house,
            strength=strength
        )

    def _calculate_timing(self, category: QuestionCategory, favorable: bool) -> TimingResult:
        """Calculate timing for the answer"""

        lagna_num = self._get_lagna_num()
        moon_house = self._get_planet_house("MOON")

        # Base timing on sign quality
        if lagna_num in self.QUALITIES["CARDINAL"]:
            base_unit = "days"
            multiplier = moon_house
        elif lagna_num in self.QUALITIES["FIXED"]:
            base_unit = "months"
            multiplier = moon_house
        else:  # Mutable
            base_unit = "weeks"
            multiplier = moon_house

        # Adjust based on element
        if lagna_num in self.ELEMENTS["FIRE"]:
            timeframe = f"{multiplier} {base_unit}"
            timeframe_hindi = f"{multiplier} {'दिन' if base_unit == 'days' else 'सप्ताह' if base_unit == 'weeks' else 'महीने'}"
        elif lagna_num in self.ELEMENTS["EARTH"]:
            adjusted = multiplier * 2
            timeframe = f"{adjusted} {base_unit}"
            timeframe_hindi = f"{adjusted} {'दिन' if base_unit == 'days' else 'सप्ताह' if base_unit == 'weeks' else 'महीने'}"
        elif lagna_num in self.ELEMENTS["AIR"]:
            timeframe = f"{multiplier} {base_unit}"
            timeframe_hindi = f"{multiplier} {'दिन' if base_unit == 'days' else 'सप्ताह' if base_unit == 'weeks' else 'महीने'}"
        else:  # Water
            adjusted = int(multiplier * 1.5)
            timeframe = f"{adjusted} {base_unit}"
            timeframe_hindi = f"{adjusted} {'दिन' if base_unit == 'days' else 'सप्ताह' if base_unit == 'weeks' else 'महीने'}"

        timing_basis = f"Based on {self.RASHI_NAMES[lagna_num]} lagna (sign quality and Moon position)"

        # Confidence
        if favorable:
            confidence = "High" if moon_house in [1, 4, 5, 9, 10, 11] else "Moderate"
        else:
            confidence = "Low"

        return TimingResult(
            will_happen=favorable,
            timeframe=timeframe if favorable else "Uncertain / अनिश्चित",
            timeframe_hindi=timeframe_hindi if favorable else "अनिश्चित",
            timing_basis=timing_basis,
            confidence=confidence
        )

    def analyze_question(self, category: QuestionCategory = QuestionCategory.GENERAL) -> PrashnaAnalysis:
        """
        Analyze the Prashna chart for a specific question category.

        Args:
            category: Type of question being asked

        Returns:
            PrashnaAnalysis with complete interpretation
        """

        # Get primary houses for this category
        question_houses = QUESTION_HOUSES.get(category, [1])
        primary_house = question_houses[0]

        # Get significators (karaka planets)
        significators = [self._get_house_lord(h) for h in question_houses]
        significators = list(dict.fromkeys(significators))  # Remove duplicates

        # Analyze lagna and moon
        lagna_analysis = self._analyze_lagna()
        moon_analysis = self._analyze_moon()

        # Calculate Arudha
        arudha = self._calculate_arudha(primary_house)

        # Collect favorable and unfavorable factors
        favorable = []
        unfavorable = []

        # Lagna factors
        if lagna_analysis["strength"] == "Strong":
            favorable.append(f"Strong Lagna in {lagna_analysis['sign']} / मजबूत लग्न")
        elif lagna_analysis["strength"] == "Weak":
            unfavorable.append(f"Weak Lagna lord in {lagna_analysis['lord_house']}th house")

        # Moon factors
        if moon_analysis["is_favorable"]:
            favorable.append(f"Moon well placed in {moon_analysis['house']}th house / चंद्रमा शुभ स्थान में")
        else:
            unfavorable.append(f"Moon in {moon_analysis['house']}th house - challenging / चंद्रमा कठिन स्थान में")

        if moon_analysis["is_waxing"]:
            favorable.append("Waxing Moon (Shukla Paksha) / शुक्ल पक्ष")
        else:
            unfavorable.append("Waning Moon (Krishna Paksha) / कृष्ण पक्ष")

        # Significator strength
        for sig in significators[:2]:
            sig_house = self._get_planet_house(sig)
            if sig_house in [1, 4, 5, 7, 9, 10, 11]:
                favorable.append(f"{sig} strong in {sig_house}th house")
            elif sig_house in [6, 8, 12]:
                unfavorable.append(f"{sig} weak in {sig_house}th house")

        # Arudha strength
        if arudha.strength == "Strong":
            favorable.append(f"Strong Arudha in {arudha.arudha_sign}")
        elif arudha.strength == "Weak":
            unfavorable.append(f"Weak Arudha lord in {arudha.arudha_lord_house}th house")

        # Calculate confidence
        confidence = 50 + (len(favorable) * 10) - (len(unfavorable) * 10)
        confidence = max(10, min(90, confidence))

        # Determine answer
        is_favorable = len(favorable) > len(unfavorable)

        # Calculate timing
        timing = self._calculate_timing(category, is_favorable)

        # Generate answer and interpretation
        answer, answer_hindi = self._generate_answer(category, is_favorable, confidence)
        interpretation, interpretation_hindi = self._generate_interpretation(
            category, lagna_analysis, moon_analysis, arudha, favorable, unfavorable
        )

        return PrashnaAnalysis(
            question_category=category,
            primary_house=primary_house,
            significators=significators,
            lagna_analysis=lagna_analysis,
            moon_analysis=moon_analysis,
            arudha=arudha,
            timing=timing,
            answer=answer,
            answer_hindi=answer_hindi,
            confidence_level=confidence,
            favorable_factors=favorable,
            unfavorable_factors=unfavorable,
            detailed_interpretation=interpretation,
            detailed_interpretation_hindi=interpretation_hindi
        )

    def _generate_answer(self, category: QuestionCategory, favorable: bool, confidence: int) -> Tuple[str, str]:
        """Generate the answer based on analysis"""

        if category == QuestionCategory.MARRIAGE:
            if favorable and confidence > 60:
                return ("Marriage prospects are favorable. Union likely within the indicated time.",
                        "विवाह की संभावना अनुकूल है। संकेतित समय में मिलन संभव।")
            elif favorable:
                return ("Marriage possible but may face some delays or minor obstacles.",
                        "विवाह संभव है लेकिन कुछ विलंब या छोटी बाधाएं हो सकती हैं।")
            else:
                return ("Marriage may face obstacles. Patience and remedies recommended.",
                        "विवाह में बाधाएं आ सकती हैं। धैर्य और उपाय सुझाए जाते हैं।")

        elif category == QuestionCategory.CAREER:
            if favorable and confidence > 60:
                return ("Career matter will resolve favorably. Success indicated.",
                        "करियर का मामला अनुकूल रूप से हल होगा। सफलता के संकेत।")
            elif favorable:
                return ("Career progress likely but may require effort and patience.",
                        "करियर में प्रगति संभव है लेकिन प्रयास और धैर्य जरूरी।")
            else:
                return ("Career matter challenging at present. Consider alternatives.",
                        "वर्तमान में करियर मामला चुनौतीपूर्ण। विकल्पों पर विचार करें।")

        elif category == QuestionCategory.HEALTH:
            if favorable and confidence > 60:
                return ("Health will improve. Recovery indicated.",
                        "स्वास्थ्य में सुधार होगा। स्वस्थ होने के संकेत।")
            elif favorable:
                return ("Health matters will stabilize. Follow medical advice.",
                        "स्वास्थ्य स्थिर होगा। चिकित्सा सलाह का पालन करें।")
            else:
                return ("Health needs attention. Seek proper medical care.",
                        "स्वास्थ्य पर ध्यान देना जरूरी। उचित चिकित्सा लें।")

        elif category == QuestionCategory.LOST_ITEM:
            if favorable and confidence > 60:
                return ("Lost item will be recovered. Look in indicated direction.",
                        "खोई वस्तु मिल जाएगी। संकेतित दिशा में देखें।")
            elif favorable:
                return ("Recovery possible but may take time.",
                        "प्राप्ति संभव लेकिन समय लग सकता है।")
            else:
                return ("Recovery unlikely. Item may have changed hands.",
                        "प्राप्ति की संभावना कम। वस्तु किसी और के पास हो सकती है।")

        elif category == QuestionCategory.TRAVEL:
            if favorable and confidence > 60:
                return ("Travel will be successful and beneficial.",
                        "यात्रा सफल और लाभकारी होगी।")
            elif favorable:
                return ("Travel possible with some precautions.",
                        "कुछ सावधानियों के साथ यात्रा संभव।")
            else:
                return ("Postpone travel if possible. Conditions not favorable.",
                        "संभव हो तो यात्रा स्थगित करें। स्थितियां अनुकूल नहीं।")

        elif category == QuestionCategory.LITIGATION:
            if favorable and confidence > 60:
                return ("Legal matter will resolve in your favor.",
                        "कानूनी मामला आपके पक्ष में होगा।")
            elif favorable:
                return ("Legal outcome positive but process may be long.",
                        "कानूनी परिणाम सकारात्मक लेकिन प्रक्रिया लंबी।")
            else:
                return ("Legal matter challenging. Consider settlement.",
                        "कानूनी मामला कठिन। समझौते पर विचार करें।")

        else:  # General
            if favorable and confidence > 60:
                return ("The matter will resolve favorably. Success indicated.",
                        "मामला अनुकूल रूप से हल होगा। सफलता के संकेत।")
            elif favorable:
                return ("Outcome likely positive with some effort required.",
                        "परिणाम सकारात्मक होने की संभावना, कुछ प्रयास जरूरी।")
            else:
                return ("Matter faces obstacles. Patience and effort needed.",
                        "मामले में बाधाएं हैं। धैर्य और प्रयास जरूरी।")

    def _generate_interpretation(
        self,
        category: QuestionCategory,
        lagna: Dict,
        moon: Dict,
        arudha: ArudhaResult,
        favorable: List[str],
        unfavorable: List[str]
    ) -> Tuple[str, str]:
        """Generate detailed interpretation"""

        interp_parts = []
        interp_hindi_parts = []

        # Lagna interpretation
        interp_parts.append(f"The Prashna lagna is {lagna['sign']} ({lagna['sign_hindi']}) "
                          f"with its lord {lagna['lord']} in the {lagna['lord_house']}th house.")
        interp_hindi_parts.append(f"प्रश्न लग्न {lagna['sign_hindi']} है, "
                                  f"जिसका स्वामी {lagna['lord']} {lagna['lord_house']}वें भाव में है।")

        # Moon interpretation
        interp_parts.append(f"Moon is in the {moon['house']}th house in {moon['sign']} "
                          f"({moon['nakshatra']} nakshatra). "
                          f"The query comes in {moon['paksha']} Paksha.")
        interp_hindi_parts.append(f"चंद्रमा {moon['house']}वें भाव में {moon['sign_hindi']} राशि में है "
                                  f"({moon['nakshatra']} नक्षत्र)। "
                                  f"प्रश्न {moon['paksha']} पक्ष में पूछा गया है।")

        # Arudha interpretation
        interp_parts.append(f"The Arudha for this question falls in the {arudha.arudha_house}th house "
                          f"({arudha.arudha_sign}), with its lord {arudha.arudha_lord} "
                          f"in the {arudha.arudha_lord_house}th house.")
        interp_hindi_parts.append(f"इस प्रश्न का आरूढ़ {arudha.arudha_house}वें भाव ({arudha.arudha_sign}) में है, "
                                  f"जिसका स्वामी {arudha.arudha_lord} {arudha.arudha_lord_house}वें भाव में है।")

        # Summary
        if len(favorable) > len(unfavorable):
            interp_parts.append("Overall, the chart shows more favorable indications than unfavorable ones.")
            interp_hindi_parts.append("कुल मिलाकर, कुंडली अनुकूल संकेत अधिक दिखाती है।")
        else:
            interp_parts.append("The chart shows some challenging factors that need attention.")
            interp_hindi_parts.append("कुंडली कुछ चुनौतीपूर्ण कारक दिखाती है जिन पर ध्यान देना जरूरी है।")

        return " ".join(interp_parts), " ".join(interp_hindi_parts)


# =============================================================================
# CONVENIENCE FUNCTION
# =============================================================================

def analyze_prashna(
    chart_data: Dict[str, Any],
    question_type: str = "general"
) -> PrashnaAnalysis:
    """
    Convenience function to analyze a Prashna chart.

    Args:
        chart_data: Prashna chart dictionary
        question_type: Type of question (marriage, career, health, etc.)

    Returns:
        PrashnaAnalysis object
    """
    # Map string to enum
    category_map = {
        "general": QuestionCategory.GENERAL,
        "marriage": QuestionCategory.MARRIAGE,
        "career": QuestionCategory.CAREER,
        "health": QuestionCategory.HEALTH,
        "travel": QuestionCategory.TRAVEL,
        "lost_item": QuestionCategory.LOST_ITEM,
        "litigation": QuestionCategory.LITIGATION,
        "education": QuestionCategory.EDUCATION,
        "finance": QuestionCategory.FINANCE,
        "pregnancy": QuestionCategory.PREGNANCY
    }

    category = category_map.get(question_type.lower(), QuestionCategory.GENERAL)

    calculator = PrashnaCalculator(chart_data)
    return calculator.analyze_question(category)
