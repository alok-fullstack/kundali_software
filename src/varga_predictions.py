"""
Varga Chart Predictions and Interpretations
Based on Brihat Parashara Hora Shastra (BPHS) and classical texts

This module provides predictions based on divisional charts.
Key focus areas:
- D-9 Navamsa: Marriage, spouse characteristics, dharma
- D-10 Dasamsa: Career, profession, social status
- D-7 Saptamsa: Children and progeny
- D-12 Dwadasamsa: Parents
- D-60 Shashtiamsa: Past life karma

Author: Kundali Software
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from .divisional_charts import (
    DivisionalChartCalculator, DivisionalChart, DivisionalPosition,
    VargaChart, get_varga_chart_for_kundali, get_planet_vimshopaka_bala
)
from .config import RASHIS, Planet


@dataclass
class VargaPrediction:
    """A single prediction from varga analysis."""
    category: str           # e.g., "Marriage", "Career", "Children"
    aspect: str             # Specific aspect being analyzed
    prediction: str         # The prediction text
    strength: str           # Strong, Moderate, Weak
    is_favorable: bool      # Overall favorable or not
    supporting_factors: List[str]  # Reasons for prediction
    remedies: List[str]     # Suggested remedies if unfavorable


class NavamsaPredictor:
    """
    D-9 Navamsa Predictions (Marriage and Spiritual Life)

    Based on BPHS principles:
    - 7th house of Navamsa shows spouse characteristics
    - Venus (for men) and Jupiter (for women) indicate spouse
    - Navamsa lagna shows inner self and dharmic nature
    - Strong planets in Navamsa support marriage
    """

    # Spouse characteristics by Navamsa Rashi
    SPOUSE_CHARACTERISTICS = {
        0: {  # Aries
            "appearance": "Athletic build, sharp features, reddish complexion",
            "nature": "Independent, energetic, leader-type, passionate",
            "traits": "Courageous but can be impulsive, direct in approach",
        },
        1: {  # Taurus
            "appearance": "Well-built, beautiful features, pleasant face",
            "nature": "Stable, sensual, loves luxury and comfort",
            "traits": "Loyal, patient but can be stubborn, good with finances",
        },
        2: {  # Gemini
            "appearance": "Youthful, expressive features, average height",
            "nature": "Intelligent, communicative, versatile",
            "traits": "Good conversationalist, curious but can be restless",
        },
        3: {  # Cancer
            "appearance": "Round face, nurturing look, fair complexion",
            "nature": "Emotional, caring, family-oriented",
            "traits": "Protective, intuitive, may be moody at times",
        },
        4: {  # Leo
            "appearance": "Dignified bearing, strong presence, royal appearance",
            "nature": "Proud, generous, loves admiration",
            "traits": "Creative, loyal, can be dominating",
        },
        5: {  # Virgo
            "appearance": "Refined features, clean appearance, modest",
            "nature": "Analytical, practical, service-oriented",
            "traits": "Detail-oriented, health conscious, can be critical",
        },
        6: {  # Libra
            "appearance": "Attractive, symmetrical features, charming",
            "nature": "Balanced, artistic, loves harmony",
            "traits": "Diplomatic, romantic, may be indecisive",
        },
        7: {  # Scorpio
            "appearance": "Intense gaze, magnetic presence, mysterious",
            "nature": "Deep, passionate, transformative",
            "traits": "Loyal, resourceful, can be possessive",
        },
        8: {  # Sagittarius
            "appearance": "Tall, athletic, friendly appearance",
            "nature": "Philosophical, optimistic, freedom-loving",
            "traits": "Honest, adventurous, can be blunt",
        },
        9: {  # Capricorn
            "appearance": "Serious demeanor, thin build, mature look",
            "nature": "Ambitious, disciplined, practical",
            "traits": "Responsible, hardworking, can be cold",
        },
        10: {  # Aquarius
            "appearance": "Unique features, unconventional style",
            "nature": "Intellectual, humanitarian, independent",
            "traits": "Original thinker, friendly but detached",
        },
        11: {  # Pisces
            "appearance": "Soft features, dreamy eyes, gentle presence",
            "nature": "Compassionate, spiritual, imaginative",
            "traits": "Artistic, intuitive, can be escapist",
        },
    }

    # Planet effects in 7th house of Navamsa
    SEVENTH_HOUSE_PLANET_EFFECTS = {
        "SUN": {
            "effect": "Spouse may be proud, authoritative, government-connected",
            "timing": "Marriage may happen with some delays",
            "quality": "Partnership needs mutual respect for ego",
        },
        "MOON": {
            "effect": "Spouse is emotional, nurturing, may be involved in public dealings",
            "timing": "Marriage timing connected to emotional readiness",
            "quality": "Emotional compatibility crucial",
        },
        "MARS": {
            "effect": "Spouse is energetic, possibly argumentative, technical skills",
            "timing": "Mangal Dosha considerations apply",
            "quality": "Physical compatibility strong but need patience",
        },
        "MERCURY": {
            "effect": "Spouse is intelligent, communicative, youthful",
            "timing": "Marriage through communication or education",
            "quality": "Intellectual compatibility important",
        },
        "JUPITER": {
            "effect": "Spouse is wise, spiritual, from good family",
            "timing": "Generally favorable for marriage",
            "quality": "Dharmic partnership, spiritual growth together",
        },
        "VENUS": {
            "effect": "Spouse is beautiful, artistic, loving",
            "timing": "Marriage brings luxury and comfort",
            "quality": "Strong romantic and physical compatibility",
        },
        "SATURN": {
            "effect": "Spouse may be older or mature, disciplined",
            "timing": "Delayed marriage but stable",
            "quality": "Long-lasting partnership through patience",
        },
        "RAHU": {
            "effect": "Unconventional spouse, possibly from different background",
            "timing": "Sudden or unusual circumstances in marriage",
            "quality": "Need to balance desires and dharma",
        },
        "KETU": {
            "effect": "Spiritually inclined spouse, detached nature",
            "timing": "Karmic connection from past life",
            "quality": "Deep spiritual bond but material detachment",
        },
    }

    def __init__(self):
        self.calculator = DivisionalChartCalculator()

    def analyze_navamsa(self, navamsa_chart: DivisionalChart) -> Dict:
        """
        Complete Navamsa analysis for marriage predictions.

        Args:
            navamsa_chart: Pre-calculated D-9 chart

        Returns:
            Dictionary with comprehensive marriage analysis
        """
        analysis = {
            "navamsa_lagna": self._analyze_navamsa_lagna(navamsa_chart),
            "spouse_characteristics": self._predict_spouse(navamsa_chart),
            "marriage_timing_factors": self._analyze_marriage_timing(navamsa_chart),
            "marriage_quality": self._analyze_marriage_quality(navamsa_chart),
            "spiritual_aspects": self._analyze_spiritual_nature(navamsa_chart),
            "predictions": [],
        }

        # Generate summary predictions
        analysis["predictions"] = self._generate_navamsa_predictions(analysis)

        return analysis

    def _analyze_navamsa_lagna(self, chart: DivisionalChart) -> Dict:
        """Analyze the Navamsa Lagna for inner nature."""
        lagna = chart.lagna
        return {
            "rashi": lagna.varga_rashi,
            "rashi_english": lagna.varga_rashi_english,
            "interpretation": f"Your inner dharmic nature is {lagna.varga_rashi_english}. "
                            f"This reveals your true spiritual path and approach to commitments.",
            "element": self._get_element(lagna.varga_rashi_num),
        }

    def _predict_spouse(self, chart: DivisionalChart) -> Dict:
        """Predict spouse characteristics from 7th house."""
        lagna_num = chart.lagna.varga_rashi_num
        seventh_house_rashi = (lagna_num + 6) % 12

        # Get planets in 7th house
        planets_in_7th = chart.planets_in_houses.get(7, [])

        # Get 7th lord position
        seventh_lord = RASHIS[seventh_house_rashi]["lord"]

        characteristics = self.SPOUSE_CHARACTERISTICS[seventh_house_rashi]

        result = {
            "seventh_house_rashi": RASHIS[seventh_house_rashi]["name"],
            "seventh_house_rashi_english": RASHIS[seventh_house_rashi]["english"],
            "appearance": characteristics["appearance"],
            "nature": characteristics["nature"],
            "key_traits": characteristics["traits"],
            "seventh_lord": seventh_lord,
            "planets_in_seventh": planets_in_7th,
            "planet_influences": [],
        }

        # Add planet influences
        for planet in planets_in_7th:
            if planet in self.SEVENTH_HOUSE_PLANET_EFFECTS:
                result["planet_influences"].append({
                    "planet": planet,
                    **self.SEVENTH_HOUSE_PLANET_EFFECTS[planet]
                })

        return result

    def _analyze_marriage_timing(self, chart: DivisionalChart) -> Dict:
        """Analyze factors affecting marriage timing."""
        factors = []
        overall_timing = "Normal"

        # Check Venus condition (for male charts)
        venus_pos = chart.planets.get("VENUS")
        if venus_pos:
            if venus_pos.is_exalted:
                factors.append("Venus exalted in Navamsa - favorable for early, happy marriage")
            elif venus_pos.is_debilitated:
                factors.append("Venus debilitated - may face delays or challenges in marriage")
                overall_timing = "Delayed"
            elif venus_pos.is_own_sign:
                factors.append("Venus in own sign - strong marriage yoga")

        # Check Jupiter condition (for female charts)
        jupiter_pos = chart.planets.get("JUPITER")
        if jupiter_pos:
            if jupiter_pos.is_exalted:
                factors.append("Jupiter exalted - blessed with good spouse")
            elif jupiter_pos.is_debilitated:
                factors.append("Jupiter debilitated - need careful spouse selection")

        # Check Saturn aspects (delays)
        saturn_pos = chart.planets.get("SATURN")
        if saturn_pos:
            saturn_house = ((saturn_pos.varga_rashi_num - chart.lagna.varga_rashi_num) % 12) + 1
            if saturn_house == 7:
                factors.append("Saturn in 7th - delayed but stable marriage")
                overall_timing = "Delayed"

        return {
            "overall_indication": overall_timing,
            "factors": factors,
        }

    def _analyze_marriage_quality(self, chart: DivisionalChart) -> Dict:
        """Analyze quality of married life."""
        quality_score = 70  # Base score
        positive_factors = []
        negative_factors = []

        # Check 7th house
        planets_in_7th = chart.planets_in_houses.get(7, [])

        benefics = ["JUPITER", "VENUS", "MERCURY", "MOON"]
        malefics = ["SATURN", "MARS", "RAHU", "KETU", "SUN"]

        for planet in planets_in_7th:
            if planet in benefics:
                quality_score += 10
                positive_factors.append(f"{planet} in 7th brings harmony")
            elif planet in malefics and planet != "SUN":
                quality_score -= 10
                negative_factors.append(f"{planet} in 7th may create challenges")

        # Check 7th lord dignity
        lagna_num = chart.lagna.varga_rashi_num
        seventh_house_rashi = (lagna_num + 6) % 12
        seventh_lord_name = RASHIS[seventh_house_rashi]["lord"].upper()

        # Find seventh lord in planets
        for planet_name, planet_pos in chart.planets.items():
            if seventh_lord_name in planet_name:
                if planet_pos.is_exalted:
                    quality_score += 15
                    positive_factors.append("7th lord exalted - excellent marriage prospects")
                elif planet_pos.is_debilitated:
                    quality_score -= 15
                    negative_factors.append("7th lord debilitated - challenges in partnership")

        quality_level = "Excellent" if quality_score >= 85 else \
                       "Good" if quality_score >= 70 else \
                       "Moderate" if quality_score >= 50 else "Challenging"

        return {
            "quality_score": min(100, max(0, quality_score)),
            "quality_level": quality_level,
            "positive_factors": positive_factors,
            "negative_factors": negative_factors,
        }

    def _analyze_spiritual_nature(self, chart: DivisionalChart) -> Dict:
        """Analyze spiritual/dharmic nature from Navamsa."""
        spiritual_factors = []

        # Check 9th house (dharma)
        planets_in_9th = chart.planets_in_houses.get(9, [])

        for planet in planets_in_9th:
            if planet == "JUPITER":
                spiritual_factors.append("Jupiter in 9th - strong dharmic inclination")
            elif planet == "KETU":
                spiritual_factors.append("Ketu in 9th - past life spiritual merit")

        # Check Jupiter's position
        jupiter_pos = chart.planets.get("JUPITER")
        if jupiter_pos and jupiter_pos.is_own_sign:
            spiritual_factors.append("Jupiter in own sign - natural spiritual wisdom")

        return {
            "dharmic_strengths": spiritual_factors,
            "spiritual_path": self._get_spiritual_path(chart.lagna.varga_rashi_num),
        }

    def _get_spiritual_path(self, lagna_num: int) -> str:
        """Get spiritual path based on Navamsa lagna."""
        paths = {
            0: "Karma Yoga - Path of Action",
            1: "Bhakti Yoga - Path of Devotion (through senses)",
            2: "Jnana Yoga - Path of Knowledge",
            3: "Bhakti Yoga - Path of Emotional Devotion",
            4: "Raja Yoga - Royal Path of Self-mastery",
            5: "Karma Yoga - Path of Service",
            6: "Bhakti Yoga - Path of Harmony",
            7: "Tantra - Path of Transformation",
            8: "Jnana Yoga - Path of Higher Learning",
            9: "Karma Yoga - Path of Discipline",
            10: "Jnana Yoga - Path of Innovation",
            11: "Bhakti Yoga - Path of Surrender",
        }
        return paths.get(lagna_num, "Mixed spiritual path")

    def _get_element(self, rashi_num: int) -> str:
        """Get element of a rashi."""
        elements = {0: "Fire", 1: "Earth", 2: "Air", 3: "Water",
                   4: "Fire", 5: "Earth", 6: "Air", 7: "Water",
                   8: "Fire", 9: "Earth", 10: "Air", 11: "Water"}
        return elements.get(rashi_num, "Unknown")

    def _generate_navamsa_predictions(self, analysis: Dict) -> List[VargaPrediction]:
        """Generate final predictions from analysis."""
        predictions = []

        # Spouse prediction
        spouse = analysis["spouse_characteristics"]
        predictions.append(VargaPrediction(
            category="Marriage",
            aspect="Spouse Characteristics",
            prediction=f"Your spouse is likely to have {spouse['appearance'].lower()}. "
                       f"By nature, they will be {spouse['nature'].lower()}.",
            strength="Strong" if analysis["marriage_quality"]["quality_score"] >= 70 else "Moderate",
            is_favorable=analysis["marriage_quality"]["quality_score"] >= 60,
            supporting_factors=[spouse["key_traits"]],
            remedies=[] if analysis["marriage_quality"]["quality_score"] >= 60 else
                    ["Worship Venus on Fridays", "Recite Sukta for marital harmony"],
        ))

        # Marriage timing
        timing = analysis["marriage_timing_factors"]
        predictions.append(VargaPrediction(
            category="Marriage",
            aspect="Timing",
            prediction=f"Marriage timing indication: {timing['overall_indication']}. "
                       + " ".join(timing["factors"][:2]),
            strength="Strong" if timing["overall_indication"] == "Normal" else "Moderate",
            is_favorable=timing["overall_indication"] != "Delayed",
            supporting_factors=timing["factors"],
            remedies=["Fast on Thursdays for Jupiter's blessings"] if timing["overall_indication"] == "Delayed" else [],
        ))

        return predictions


class DasamsaPredictor:
    """
    D-10 Dasamsa Predictions (Career and Profession)

    Based on BPHS principles:
    - 10th house shows main career
    - Lagna shows approach to profession
    - Sun's position shows authority and recognition
    - Saturn shows hard work and discipline
    """

    # Career indications by Dasamsa Lagna
    CAREER_BY_LAGNA = {
        0: ["Military", "Sports", "Engineering", "Surgery", "Police"],
        1: ["Banking", "Finance", "Agriculture", "Luxury goods", "Art dealing"],
        2: ["Communication", "Writing", "Trading", "Teaching", "Sales"],
        3: ["Hospitality", "Real estate", "Nursing", "Psychology", "Food industry"],
        4: ["Government", "Politics", "Entertainment", "Leadership roles", "Management"],
        5: ["Healthcare", "Accounting", "Analysis", "Quality control", "Research"],
        6: ["Law", "Diplomacy", "Fashion", "Partnership business", "Counseling"],
        7: ["Research", "Investigation", "Psychology", "Insurance", "Mining"],
        8: ["Education", "Travel industry", "Religion", "Publishing", "Law"],
        9: ["Administration", "Manufacturing", "Mining", "Construction", "Politics"],
        10: ["Technology", "Social work", "Innovation", "Science", "Networking"],
        11: ["Healing", "Arts", "Spirituality", "Photography", "Foreign trade"],
    }

    # Planet career significations
    PLANET_CAREERS = {
        "SUN": ["Government", "Politics", "Medicine", "Authority positions"],
        "MOON": ["Public dealing", "Tourism", "Nursing", "Hotels", "Liquids"],
        "MARS": ["Military", "Engineering", "Surgery", "Sports", "Real estate"],
        "MERCURY": ["Communication", "Writing", "Trading", "Accounting", "IT"],
        "JUPITER": ["Education", "Law", "Finance", "Consulting", "Religion"],
        "VENUS": ["Entertainment", "Arts", "Fashion", "Luxury", "Beauty"],
        "SATURN": ["Labor", "Mining", "Agriculture", "Manufacturing", "Service"],
        "RAHU": ["Foreign affairs", "Technology", "Research", "Unconventional"],
        "KETU": ["Spiritual", "Occult", "Investigation", "Alternative healing"],
    }

    def __init__(self):
        self.calculator = DivisionalChartCalculator()

    def analyze_dasamsa(self, dasamsa_chart: DivisionalChart) -> Dict:
        """
        Complete Dasamsa analysis for career predictions.

        Args:
            dasamsa_chart: Pre-calculated D-10 chart

        Returns:
            Dictionary with comprehensive career analysis
        """
        analysis = {
            "career_lagna": self._analyze_career_lagna(dasamsa_chart),
            "10th_house_analysis": self._analyze_10th_house(dasamsa_chart),
            "career_indicators": self._get_career_indicators(dasamsa_chart),
            "professional_strengths": self._analyze_professional_strengths(dasamsa_chart),
            "career_timing": self._analyze_career_growth(dasamsa_chart),
            "predictions": [],
        }

        analysis["predictions"] = self._generate_dasamsa_predictions(analysis)

        return analysis

    def _analyze_career_lagna(self, chart: DivisionalChart) -> Dict:
        """Analyze Dasamsa Lagna for professional approach."""
        lagna = chart.lagna
        careers = self.CAREER_BY_LAGNA.get(lagna.varga_rashi_num, [])

        return {
            "rashi": lagna.varga_rashi,
            "rashi_english": lagna.varga_rashi_english,
            "professional_approach": self._get_professional_approach(lagna.varga_rashi_num),
            "suitable_careers": careers,
        }

    def _get_professional_approach(self, rashi_num: int) -> str:
        """Get professional approach based on Dasamsa lagna."""
        approaches = {
            0: "Dynamic, pioneering, likes to lead and take initiative",
            1: "Steady, persistent, builds wealth through patience",
            2: "Versatile, good communicator, adapts to multiple roles",
            3: "Nurturing approach, cares for others, emotional intelligence",
            4: "Authoritative, creative, seeks recognition and power",
            5: "Analytical, detail-oriented, service-minded",
            6: "Balanced, diplomatic, works well in partnerships",
            7: "Intense, research-oriented, transformative approach",
            8: "Expansive, philosophical, seeks higher meaning in work",
            9: "Ambitious, disciplined, achieves through hard work",
            10: "Innovative, humanitarian, unconventional methods",
            11: "Intuitive, creative, spiritually inclined in profession",
        }
        return approaches.get(rashi_num, "Mixed professional approach")

    def _analyze_10th_house(self, chart: DivisionalChart) -> Dict:
        """Analyze 10th house of Dasamsa."""
        lagna_num = chart.lagna.varga_rashi_num
        tenth_house_rashi = (lagna_num + 9) % 12

        planets_in_10th = chart.planets_in_houses.get(10, [])
        tenth_lord = RASHIS[tenth_house_rashi]["lord"]

        career_domains = []
        for planet in planets_in_10th:
            if planet in self.PLANET_CAREERS:
                career_domains.extend(self.PLANET_CAREERS[planet])

        return {
            "rashi": RASHIS[tenth_house_rashi]["name"],
            "rashi_english": RASHIS[tenth_house_rashi]["english"],
            "tenth_lord": tenth_lord,
            "planets_in_10th": planets_in_10th,
            "indicated_domains": list(set(career_domains)),
        }

    def _get_career_indicators(self, chart: DivisionalChart) -> List[Dict]:
        """Get specific career indicators from planetary positions."""
        indicators = []

        # Check Sun's position (authority)
        sun_pos = chart.planets.get("SUN")
        if sun_pos:
            sun_house = ((sun_pos.varga_rashi_num - chart.lagna.varga_rashi_num) % 12) + 1
            if sun_house in [1, 10, 11]:
                indicators.append({
                    "planet": "Sun",
                    "indication": "Strong leadership and authority potential",
                    "favorable": True,
                })
            if sun_pos.is_exalted:
                indicators.append({
                    "planet": "Sun",
                    "indication": "Exceptional career success and recognition",
                    "favorable": True,
                })

        # Check Saturn's position (hard work)
        saturn_pos = chart.planets.get("SATURN")
        if saturn_pos:
            if saturn_pos.is_own_sign or saturn_pos.is_exalted:
                indicators.append({
                    "planet": "Saturn",
                    "indication": "Success through disciplined, long-term efforts",
                    "favorable": True,
                })

        # Check Mercury (business/communication)
        mercury_pos = chart.planets.get("MERCURY")
        if mercury_pos:
            mercury_house = ((mercury_pos.varga_rashi_num - chart.lagna.varga_rashi_num) % 12) + 1
            if mercury_house in [1, 2, 10, 11]:
                indicators.append({
                    "planet": "Mercury",
                    "indication": "Success in business, communication, or intellectual fields",
                    "favorable": True,
                })

        return indicators

    def _analyze_professional_strengths(self, chart: DivisionalChart) -> Dict:
        """Analyze professional strengths and weaknesses."""
        strengths = []
        weaknesses = []

        # Check planets in kendras (1, 4, 7, 10)
        for house in [1, 4, 7, 10]:
            for planet in chart.planets_in_houses.get(house, []):
                if planet in ["JUPITER", "VENUS", "MERCURY"]:
                    strengths.append(f"{planet} in kendra - professional stability")

        # Check planets in dusthanas (6, 8, 12)
        for house in [6, 8, 12]:
            for planet in chart.planets_in_houses.get(house, []):
                if planet in ["SUN", "MOON", "JUPITER"]:
                    weaknesses.append(f"{planet} in house {house} - some career obstacles")

        return {
            "strengths": strengths,
            "weaknesses": weaknesses,
        }

    def _analyze_career_growth(self, chart: DivisionalChart) -> Dict:
        """Analyze career growth and timing factors."""
        growth_factors = []

        # Jupiter indicates expansion
        jupiter_pos = chart.planets.get("JUPITER")
        if jupiter_pos:
            jupiter_house = ((jupiter_pos.varga_rashi_num - chart.lagna.varga_rashi_num) % 12) + 1
            if jupiter_house in [1, 5, 9, 10, 11]:
                growth_factors.append("Jupiter well-placed - steady career growth expected")

        # Saturn indicates discipline
        saturn_pos = chart.planets.get("SATURN")
        if saturn_pos:
            saturn_house = ((saturn_pos.varga_rashi_num - chart.lagna.varga_rashi_num) % 12) + 1
            if saturn_house == 10:
                growth_factors.append("Saturn in 10th - success through patience and persistence")

        return {
            "growth_pattern": "Steady" if len(growth_factors) > 0 else "Variable",
            "factors": growth_factors,
        }

    def _generate_dasamsa_predictions(self, analysis: Dict) -> List[VargaPrediction]:
        """Generate career predictions."""
        predictions = []

        # Career direction
        lagna_analysis = analysis["career_lagna"]
        predictions.append(VargaPrediction(
            category="Career",
            aspect="Career Direction",
            prediction=f"Professional approach: {lagna_analysis['professional_approach']}. "
                       f"Suitable fields include: {', '.join(lagna_analysis['suitable_careers'][:3])}.",
            strength="Strong",
            is_favorable=True,
            supporting_factors=[f"Dasamsa Lagna in {lagna_analysis['rashi_english']}"],
            remedies=[],
        ))

        # 10th house analysis
        tenth = analysis["10th_house_analysis"]
        if tenth["indicated_domains"]:
            predictions.append(VargaPrediction(
                category="Career",
                aspect="Career Domain",
                prediction=f"Career domains indicated: {', '.join(tenth['indicated_domains'][:4])}.",
                strength="Strong" if len(tenth["planets_in_10th"]) > 0 else "Moderate",
                is_favorable=True,
                supporting_factors=[f"10th house in {tenth['rashi_english']}"],
                remedies=[],
            ))

        return predictions


class SaptamsaPredictor:
    """
    D-7 Saptamsa Predictions (Children and Progeny)

    Based on BPHS principles:
    - 5th house indicates children
    - Jupiter (significator of children) position is crucial
    - Planets in 5th house of D-7 indicate nature of children
    """

    def __init__(self):
        self.calculator = DivisionalChartCalculator()

    def analyze_saptamsa(self, saptamsa_chart: DivisionalChart) -> Dict:
        """Analyze D-7 for children predictions."""
        analysis = {
            "5th_house_analysis": self._analyze_5th_house(saptamsa_chart),
            "jupiter_analysis": self._analyze_jupiter(saptamsa_chart),
            "children_indicators": self._get_children_indicators(saptamsa_chart),
            "predictions": [],
        }

        analysis["predictions"] = self._generate_saptamsa_predictions(analysis)
        return analysis

    def _analyze_5th_house(self, chart: DivisionalChart) -> Dict:
        """Analyze 5th house of Saptamsa."""
        lagna_num = chart.lagna.varga_rashi_num
        fifth_house_rashi = (lagna_num + 4) % 12

        planets_in_5th = chart.planets_in_houses.get(5, [])
        fifth_lord = RASHIS[fifth_house_rashi]["lord"]

        return {
            "rashi": RASHIS[fifth_house_rashi]["name"],
            "fifth_lord": fifth_lord,
            "planets_in_5th": planets_in_5th,
        }

    def _analyze_jupiter(self, chart: DivisionalChart) -> Dict:
        """Analyze Jupiter as significator of children."""
        jupiter_pos = chart.planets.get("JUPITER")
        if not jupiter_pos:
            return {"status": "Unknown"}

        jupiter_house = ((jupiter_pos.varga_rashi_num - chart.lagna.varga_rashi_num) % 12) + 1

        status = "Strong" if jupiter_pos.is_exalted or jupiter_pos.is_own_sign else \
                "Weak" if jupiter_pos.is_debilitated else "Normal"

        return {
            "house": jupiter_house,
            "rashi": jupiter_pos.varga_rashi,
            "status": status,
            "is_exalted": jupiter_pos.is_exalted,
            "is_debilitated": jupiter_pos.is_debilitated,
        }

    def _get_children_indicators(self, chart: DivisionalChart) -> List[Dict]:
        """Get indicators about children."""
        indicators = []

        # Jupiter in 5th or 9th is excellent
        jupiter_pos = chart.planets.get("JUPITER")
        if jupiter_pos:
            jupiter_house = ((jupiter_pos.varga_rashi_num - chart.lagna.varga_rashi_num) % 12) + 1
            if jupiter_house in [5, 9]:
                indicators.append({
                    "factor": "Jupiter in trikona",
                    "effect": "Blessed with children, good relationship",
                    "favorable": True,
                })

        # Check 5th lord
        lagna_num = chart.lagna.varga_rashi_num
        fifth_house_rashi = (lagna_num + 4) % 12
        fifth_lord_name = RASHIS[fifth_house_rashi]["lord"].upper()

        for planet_name, planet_pos in chart.planets.items():
            if fifth_lord_name in planet_name:
                if planet_pos.is_exalted:
                    indicators.append({
                        "factor": "5th lord exalted",
                        "effect": "Children bring happiness and pride",
                        "favorable": True,
                    })

        return indicators

    def _generate_saptamsa_predictions(self, analysis: Dict) -> List[VargaPrediction]:
        """Generate children predictions."""
        predictions = []

        jupiter_analysis = analysis["jupiter_analysis"]
        if jupiter_analysis.get("status"):
            prediction_text = f"Jupiter is {jupiter_analysis['status'].lower()} in Saptamsa. "

            if jupiter_analysis["status"] == "Strong":
                prediction_text += "This indicates blessings regarding children."
            elif jupiter_analysis["status"] == "Weak":
                prediction_text += "Remedies may help improve progeny prospects."

            predictions.append(VargaPrediction(
                category="Children",
                aspect="General Indication",
                prediction=prediction_text,
                strength=jupiter_analysis["status"],
                is_favorable=jupiter_analysis["status"] != "Weak",
                supporting_factors=[f"Jupiter in {jupiter_analysis.get('rashi', 'N/A')}"],
                remedies=["Worship Jupiter on Thursdays", "Donate to children's causes"]
                        if jupiter_analysis["status"] == "Weak" else [],
            ))

        return predictions


class VargaPredictionEngine:
    """
    Master prediction engine combining all varga analyzers.

    Provides comprehensive predictions from all divisional charts.
    """

    def __init__(self):
        self.navamsa_predictor = NavamsaPredictor()
        self.dasamsa_predictor = DasamsaPredictor()
        self.saptamsa_predictor = SaptamsaPredictor()
        self.calculator = DivisionalChartCalculator()

    def get_complete_varga_analysis(self, kundali) -> Dict:
        """
        Get complete analysis from all major divisional charts.

        Args:
            kundali: Kundali object with lagna and planets

        Returns:
            Comprehensive varga analysis
        """
        lagna_longitude = kundali.lagna["longitude"]
        planets = kundali.planets

        # Calculate key divisional charts
        d9_chart = self.calculator.calculate_complete_varga_chart(
            VargaChart.D9_NAVAMSA, lagna_longitude, planets)
        d10_chart = self.calculator.calculate_complete_varga_chart(
            VargaChart.D10_DASAMSA, lagna_longitude, planets)
        d7_chart = self.calculator.calculate_complete_varga_chart(
            VargaChart.D7_SAPTAMSA, lagna_longitude, planets)

        # Get Vimshopaka strength
        vimshopaka = get_planet_vimshopaka_bala(kundali)

        return {
            "navamsa_analysis": self.navamsa_predictor.analyze_navamsa(d9_chart),
            "dasamsa_analysis": self.dasamsa_predictor.analyze_dasamsa(d10_chart),
            "saptamsa_analysis": self.saptamsa_predictor.analyze_saptamsa(d7_chart),
            "vimshopaka_bala": vimshopaka,
            "summary": self._generate_summary(d9_chart, d10_chart, d7_chart),
        }

    def _generate_summary(
        self,
        d9: DivisionalChart,
        d10: DivisionalChart,
        d7: DivisionalChart
    ) -> Dict:
        """Generate summary of key findings."""
        return {
            "marriage_outlook": self._summarize_marriage(d9),
            "career_outlook": self._summarize_career(d10),
            "children_outlook": self._summarize_children(d7),
        }

    def _summarize_marriage(self, d9: DivisionalChart) -> str:
        """Summarize marriage outlook from Navamsa."""
        planets_in_7th = d9.planets_in_houses.get(7, [])

        if "JUPITER" in planets_in_7th or "VENUS" in planets_in_7th:
            return "Favorable marriage prospects indicated"
        elif "SATURN" in planets_in_7th or "RAHU" in planets_in_7th:
            return "Marriage may be delayed but stable"
        else:
            return "Normal marriage indications"

    def _summarize_career(self, d10: DivisionalChart) -> str:
        """Summarize career outlook from Dasamsa."""
        planets_in_10th = d10.planets_in_houses.get(10, [])

        if "SUN" in planets_in_10th or "JUPITER" in planets_in_10th:
            return "Strong career success indicated"
        elif "SATURN" in planets_in_10th:
            return "Career growth through persistent effort"
        else:
            return "Steady professional development"

    def _summarize_children(self, d7: DivisionalChart) -> str:
        """Summarize children outlook from Saptamsa."""
        planets_in_5th = d7.planets_in_houses.get(5, [])

        if "JUPITER" in planets_in_5th:
            return "Blessed with children"
        elif any(p in planets_in_5th for p in ["SATURN", "RAHU", "KETU"]):
            return "Children may come after some delay"
        else:
            return "Normal indications for progeny"
