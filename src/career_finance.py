"""
Career and Finance Analysis Module

Based on authentic Vedic texts:
- Brihat Parashara Hora Shastra (BPHS) - Dhana Yoga chapter
- Phaladeepika - Raja Yoga and Dhana Yoga
- Jataka Parijata
- Saravali

Implements:
1. Career Analysis (10th house)
2. Dhana Yogas (Wealth combinations)
3. Professional guidance
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum


# =============================================================================
# CONSTANTS
# =============================================================================

# Sign lords
SIGN_LORDS = {
    0: "MARS", 1: "VENUS", 2: "MERCURY", 3: "MOON",
    4: "SUN", 5: "MERCURY", 6: "VENUS", 7: "MARS",
    8: "JUPITER", 9: "SATURN", 10: "SATURN", 11: "JUPITER"
}

# Career indications by 10th house sign
CAREER_BY_10TH_SIGN = {
    "Mesha": {
        "careers": ["सेना/पुलिस / Army/Police", "खेल / Sports", "सर्जन / Surgeon", "इंजीनियर / Engineer", "उद्यमी / Entrepreneur"],
        "traits": "नेतृत्व, साहस, स्वतंत्रता / Leadership, courage, independence",
        "element": "अग्नि / Fire"
    },
    "Vrishabha": {
        "careers": ["बैंकिंग / Banking", "रियल एस्टेट / Real Estate", "कृषि / Agriculture", "होटल / Hospitality", "ज्वेलरी / Jewelry"],
        "traits": "स्थिरता, धन प्रबंधन / Stability, wealth management",
        "element": "पृथ्वी / Earth"
    },
    "Mithuna": {
        "careers": ["पत्रकारिता / Journalism", "लेखन / Writing", "शिक्षा / Teaching", "व्यापार / Trading", "IT/सॉफ्टवेयर / IT/Software"],
        "traits": "संवाद, बुद्धि, बहुमुखी / Communication, intellect, versatile",
        "element": "वायु / Air"
    },
    "Karka": {
        "careers": ["नर्सिंग / Nursing", "होटल / Hospitality", "रियल एस्टेट / Real Estate", "खाद्य उद्योग / Food Industry", "मनोविज्ञान / Psychology"],
        "traits": "देखभाल, पोषण, भावनात्मक बुद्धि / Caring, nurturing, emotional intelligence",
        "element": "जल / Water"
    },
    "Simha": {
        "careers": ["सरकारी नौकरी / Government Job", "राजनीति / Politics", "मनोरंजन / Entertainment", "प्रबंधन / Management", "शिक्षा प्रशासन / Education Admin"],
        "traits": "अधिकार, प्रतिष्ठा, नेतृत्व / Authority, prestige, leadership",
        "element": "अग्नि / Fire"
    },
    "Kanya": {
        "careers": ["चिकित्सा / Medicine", "लेखा / Accounting", "विश्लेषण / Analysis", "संपादन / Editing", "गुणवत्ता नियंत्रण / Quality Control"],
        "traits": "विस्तार पर ध्यान, सेवा, विश्लेषण / Detail-oriented, service, analytical",
        "element": "पृथ्वी / Earth"
    },
    "Tula": {
        "careers": ["कानून / Law", "कूटनीति / Diplomacy", "फैशन / Fashion", "कला / Art", "परामर्श / Counseling"],
        "traits": "न्याय, सौंदर्य, संतुलन / Justice, beauty, balance",
        "element": "वायु / Air"
    },
    "Vrishchika": {
        "careers": ["अनुसंधान / Research", "जांच / Investigation", "सर्जरी / Surgery", "मनोविज्ञान / Psychology", "बीमा / Insurance"],
        "traits": "गहराई, रहस्य, परिवर्तन / Depth, mystery, transformation",
        "element": "जल / Water"
    },
    "Dhanu": {
        "careers": ["शिक्षा / Education", "कानून / Law", "धर्म / Religion", "प्रकाशन / Publishing", "यात्रा उद्योग / Travel Industry"],
        "traits": "ज्ञान, दर्शन, विस्तार / Knowledge, philosophy, expansion",
        "element": "अग्नि / Fire"
    },
    "Makara": {
        "careers": ["सरकारी नौकरी / Government", "प्रशासन / Administration", "निर्माण / Construction", "खनन / Mining", "कॉर्पोरेट / Corporate"],
        "traits": "महत्वाकांक्षा, अनुशासन, संरचना / Ambition, discipline, structure",
        "element": "पृथ्वी / Earth"
    },
    "Kumbha": {
        "careers": ["टेक्नोलॉजी / Technology", "विज्ञान / Science", "सामाजिक कार्य / Social Work", "नवाचार / Innovation", "नेटवर्किंग / Networking"],
        "traits": "नवाचार, मानवता, स्वतंत्रता / Innovation, humanity, independence",
        "element": "वायु / Air"
    },
    "Meena": {
        "careers": ["कला / Art", "संगीत / Music", "आध्यात्मिक / Spiritual", "चिकित्सा / Healing", "फोटोग्राफी / Photography"],
        "traits": "रचनात्मकता, अंतर्ज्ञान, करुणा / Creativity, intuition, compassion",
        "element": "जल / Water"
    }
}

# Planet career indications
PLANET_CAREERS = {
    "SUN": ["सरकारी नौकरी / Government", "राजनीति / Politics", "प्रशासन / Administration", "चिकित्सा / Medicine"],
    "MOON": ["नर्सिंग / Nursing", "होटल / Hospitality", "जनसंपर्क / Public Relations", "खाद्य / Food"],
    "MARS": ["सेना / Military", "पुलिस / Police", "इंजीनियरिंग / Engineering", "खेल / Sports", "सर्जरी / Surgery"],
    "MERCURY": ["व्यापार / Business", "लेखा / Accounting", "IT / Technology", "लेखन / Writing", "शिक्षा / Teaching"],
    "JUPITER": ["शिक्षा / Education", "कानून / Law", "बैंकिंग / Banking", "परामर्श / Consulting", "धर्म / Religion"],
    "VENUS": ["कला / Art", "मनोरंजन / Entertainment", "फैशन / Fashion", "ज्वेलरी / Jewelry", "सौंदर्य / Beauty"],
    "SATURN": ["खनन / Mining", "निर्माण / Construction", "कृषि / Agriculture", "तेल/गैस / Oil-Gas", "श्रम / Labor"],
    "RAHU": ["विदेश / Foreign", "IT / Technology", "जासूसी / Spying", "शोध / Research", "नवाचार / Innovation"],
    "KETU": ["आध्यात्मिक / Spiritual", "गणित / Mathematics", "कंप्यूटर / Computers", "चिकित्सा / Healing"]
}


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class YogaResult:
    """Result for a detected yoga"""
    name: str
    name_hindi: str
    is_present: bool
    strength: str  # "Strong", "Moderate", "Weak"
    description: str
    description_hindi: str
    effects: List[str]
    effects_hindi: List[str]
    planets_involved: List[str] = field(default_factory=list)


@dataclass
class CareerAnalysis:
    """Complete career analysis"""
    tenth_house_sign: str
    tenth_house_lord: str
    tenth_lord_house: int
    planets_in_tenth: List[str]
    recommended_careers: List[str]
    career_traits: str
    career_timing: str
    career_timing_hindi: str
    government_job_yoga: bool
    business_yoga: bool
    foreign_career_yoga: bool


@dataclass
class DhanaYogaAnalysis:
    """Wealth yoga analysis"""
    yogas_present: List[YogaResult]
    wealth_potential: str  # "High", "Moderate", "Low"
    wealth_potential_hindi: str
    best_wealth_periods: List[str]
    wealth_sources: List[str]
    wealth_sources_hindi: List[str]
    poverty_yogas: List[YogaResult]


@dataclass
class CareerFinanceReport:
    """Complete career and finance report"""
    career_analysis: CareerAnalysis
    dhana_yoga_analysis: DhanaYogaAnalysis
    overall_career_score: int  # 0-100
    overall_wealth_score: int  # 0-100
    summary: str
    summary_hindi: str
    recommendations: List[str]
    recommendations_hindi: List[str]


# =============================================================================
# CAREER FINANCE ANALYZER
# =============================================================================

class CareerFinanceAnalyzer:
    """
    Analyzer for Career and Finance based on Vedic Astrology.

    Uses BPHS, Phaladeepika, and Saravali principles.
    """

    RASHI_NAMES = ["Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
                   "Tula", "Vrishchika", "Dhanu", "Makara", "Kumbha", "Meena"]

    def __init__(self, kundali_data: Dict[str, Any]):
        """Initialize with Kundali data"""
        self.kundali = kundali_data
        self.planets = kundali_data.get("planets", {})
        self.lagna_num = self._get_lagna_num()

    def _get_lagna_num(self) -> int:
        """Get lagna rashi number (0-11)"""
        lagna = self.kundali.get("lagna", {})
        return lagna.get("rashi_num", 0)

    def _get_planet_house(self, planet: str) -> int:
        """Get house number (1-12) for a planet"""
        planet_data = self.planets.get(planet, {})
        return planet_data.get("house", 1)

    def _get_planet_rashi_num(self, planet: str) -> int:
        """Get rashi number (0-11) for a planet"""
        planet_data = self.planets.get(planet, {})
        return planet_data.get("rashi_num", 0)

    def _get_house_sign(self, house_num: int) -> str:
        """Get sign name for a house"""
        sign_num = (self.lagna_num + house_num - 1) % 12
        return self.RASHI_NAMES[sign_num]

    def _get_house_lord(self, house_num: int) -> str:
        """Get lord planet for a house"""
        sign_num = (self.lagna_num + house_num - 1) % 12
        return SIGN_LORDS[sign_num]

    def _are_planets_conjunct(self, p1: str, p2: str) -> bool:
        """Check if two planets are in same sign"""
        return self._get_planet_rashi_num(p1) == self._get_planet_rashi_num(p2)

    def _is_planet_in_kendra(self, planet: str) -> bool:
        """Check if planet is in Kendra (1, 4, 7, 10)"""
        return self._get_planet_house(planet) in [1, 4, 7, 10]

    def _is_planet_in_trikona(self, planet: str) -> bool:
        """Check if planet is in Trikona (1, 5, 9)"""
        return self._get_planet_house(planet) in [1, 5, 9]

    # =========================================================================
    # CAREER ANALYSIS
    # =========================================================================

    def analyze_career(self) -> CareerAnalysis:
        """Analyze career prospects based on 10th house"""

        # 10th house analysis
        tenth_sign = self._get_house_sign(10)
        tenth_lord = self._get_house_lord(10)
        tenth_lord_house = self._get_planet_house(tenth_lord)

        # Planets in 10th house
        planets_in_10th = []
        for planet in ["SUN", "MOON", "MARS", "MERCURY", "JUPITER", "VENUS", "SATURN", "RAHU", "KETU"]:
            if self._get_planet_house(planet) == 10:
                planets_in_10th.append(planet)

        # Get career recommendations
        sign_info = CAREER_BY_10TH_SIGN.get(tenth_sign, {})
        recommended = sign_info.get("careers", [])

        # Add careers from planets in 10th
        for planet in planets_in_10th:
            recommended.extend(PLANET_CAREERS.get(planet, [])[:2])

        # Add careers from 10th lord placement
        recommended.extend(PLANET_CAREERS.get(tenth_lord, [])[:2])

        # Remove duplicates
        recommended = list(dict.fromkeys(recommended))[:8]

        # Check special yogas
        sun_house = self._get_planet_house("SUN")
        jupiter_house = self._get_planet_house("JUPITER")
        rahu_house = self._get_planet_house("RAHU")

        # Government job yoga: Sun strong + 10th house connection
        govt_yoga = (sun_house in [1, 4, 7, 10] or
                    "SUN" in planets_in_10th or
                    self._are_planets_conjunct("SUN", tenth_lord))

        # Business yoga: Mercury + Venus + 10th connection
        business_yoga = (self._get_planet_house("MERCURY") in [1, 7, 10] and
                        self._get_planet_house("VENUS") in [1, 2, 7, 10, 11])

        # Foreign career: Rahu in 10th or 9th, or 10th lord in 12th
        foreign_yoga = (rahu_house in [9, 10, 12] or
                       tenth_lord_house == 12 or
                       self._get_planet_house("KETU") in [9, 10])

        # Career timing based on Dasha
        timing = "Current Dasha period important for career decisions."
        timing_hindi = "वर्तमान दशा करियर निर्णयों के लिए महत्वपूर्ण है।"

        if tenth_lord_house in [1, 4, 7, 10]:
            timing = f"{tenth_lord} Dasha will be excellent for career."
            timing_hindi = f"{tenth_lord} की दशा करियर के लिए उत्तम होगी।"

        return CareerAnalysis(
            tenth_house_sign=tenth_sign,
            tenth_house_lord=tenth_lord,
            tenth_lord_house=tenth_lord_house,
            planets_in_tenth=planets_in_10th,
            recommended_careers=recommended,
            career_traits=sign_info.get("traits", ""),
            career_timing=timing,
            career_timing_hindi=timing_hindi,
            government_job_yoga=govt_yoga,
            business_yoga=business_yoga,
            foreign_career_yoga=foreign_yoga
        )

    # =========================================================================
    # DHANA YOGA ANALYSIS
    # =========================================================================

    def analyze_dhana_yogas(self) -> DhanaYogaAnalysis:
        """Analyze wealth yogas based on BPHS"""

        yogas_found = []
        poverty_yogas = []

        # 1. DHANA YOGA - 2nd and 11th lord connection
        lord_2 = self._get_house_lord(2)
        lord_11 = self._get_house_lord(11)

        if (self._are_planets_conjunct(lord_2, lord_11) or
            self._get_planet_house(lord_2) == 11 or
            self._get_planet_house(lord_11) == 2):
            yogas_found.append(YogaResult(
                name="Dhana Yoga",
                name_hindi="धन योग",
                is_present=True,
                strength="Strong" if self._is_planet_in_kendra(lord_2) else "Moderate",
                description="Connection between 2nd and 11th lords brings wealth",
                description_hindi="दूसरे और ग्यारहवें भाव के स्वामी का संबंध धन लाता है",
                effects=["Good accumulation of wealth", "Multiple income sources"],
                effects_hindi=["धन का अच्छा संचय", "आय के कई स्रोत"],
                planets_involved=[lord_2, lord_11]
            ))

        # 2. LAKSHMI YOGA - 9th lord in Kendra/Trikona, Venus strong
        lord_9 = self._get_house_lord(9)
        if self._is_planet_in_kendra(lord_9) or self._is_planet_in_trikona(lord_9):
            venus_strong = self._is_planet_in_kendra("VENUS") or self._get_planet_rashi_num("VENUS") in [1, 11]
            yogas_found.append(YogaResult(
                name="Lakshmi Yoga",
                name_hindi="लक्ष्मी योग",
                is_present=True,
                strength="Strong" if venus_strong else "Moderate",
                description="9th lord well placed - Fortune and wealth combination",
                description_hindi="नवम भाव का स्वामी शुभ स्थान में - भाग्य और धन का योग",
                effects=["Blessed by goddess Lakshmi", "Fortune favors wealth accumulation"],
                effects_hindi=["माता लक्ष्मी की कृपा", "भाग्य धन संचय में सहायक"],
                planets_involved=[lord_9, "VENUS"]
            ))

        # 3. GAJAKESARI YOGA - Moon-Jupiter in Kendra from each other
        moon_house = self._get_planet_house("MOON")
        jupiter_house = self._get_planet_house("JUPITER")
        moon_jupiter_diff = abs(moon_house - jupiter_house)

        if moon_jupiter_diff in [0, 3, 6, 9] or (12 - moon_jupiter_diff) in [3, 6, 9]:
            yogas_found.append(YogaResult(
                name="Gajakesari Yoga",
                name_hindi="गजकेसरी योग",
                is_present=True,
                strength="Strong" if self._is_planet_in_kendra("JUPITER") else "Moderate",
                description="Moon and Jupiter in Kendra from each other",
                description_hindi="चंद्रमा और गुरु एक-दूसरे से केंद्र में",
                effects=["Fame and recognition", "Wisdom leads to wealth", "Respected in society"],
                effects_hindi=["यश और प्रसिद्धि", "बुद्धि से धन", "समाज में सम्मान"],
                planets_involved=["MOON", "JUPITER"]
            ))

        # 4. BUDHA-ADITYA YOGA - Sun-Mercury conjunction
        if self._are_planets_conjunct("SUN", "MERCURY"):
            yogas_found.append(YogaResult(
                name="Budha-Aditya Yoga",
                name_hindi="बुधादित्य योग",
                is_present=True,
                strength="Strong" if self._is_planet_in_kendra("SUN") else "Moderate",
                description="Sun and Mercury conjunction",
                description_hindi="सूर्य और बुध की युति",
                effects=["Intelligence in business", "Good communication for earning", "Success in trading"],
                effects_hindi=["व्यापार में बुद्धि", "कमाई के लिए अच्छा संवाद", "व्यापार में सफलता"],
                planets_involved=["SUN", "MERCURY"]
            ))

        # 5. CHANDRA-MANGAL YOGA - Moon-Mars conjunction
        if self._are_planets_conjunct("MOON", "MARS"):
            yogas_found.append(YogaResult(
                name="Chandra-Mangal Yoga",
                name_hindi="चंद्र-मंगल योग",
                is_present=True,
                strength="Moderate",
                description="Moon and Mars conjunction - wealth through courage",
                description_hindi="चंद्रमा और मंगल की युति - साहस से धन",
                effects=["Wealth through bold actions", "Real estate gains", "Success in competitive fields"],
                effects_hindi=["साहसिक कार्यों से धन", "रियल एस्टेट से लाभ", "प्रतिस्पर्धी क्षेत्रों में सफलता"],
                planets_involved=["MOON", "MARS"]
            ))

        # 6. PANCHA MAHAPURUSHA YOGAS
        # Hamsa Yoga - Jupiter in Kendra in own/exalted sign
        jupiter_rashi = self._get_planet_rashi_num("JUPITER")
        if self._is_planet_in_kendra("JUPITER") and jupiter_rashi in [3, 8, 11]:  # Cancer, Sagittarius, Pisces
            yogas_found.append(YogaResult(
                name="Hamsa Yoga",
                name_hindi="हंस योग",
                is_present=True,
                strength="Strong",
                description="Jupiter in Kendra in own/exalted sign",
                description_hindi="गुरु केंद्र में स्वराशि/उच्च में",
                effects=["Great wisdom and wealth", "Spiritual and material success", "Respected advisor"],
                effects_hindi=["महान बुद्धि और धन", "आध्यात्मिक और भौतिक सफलता", "सम्मानित सलाहकार"],
                planets_involved=["JUPITER"]
            ))

        # Malavya Yoga - Venus in Kendra in own/exalted sign
        venus_rashi = self._get_planet_rashi_num("VENUS")
        if self._is_planet_in_kendra("VENUS") and venus_rashi in [1, 6, 11]:  # Taurus, Libra, Pisces
            yogas_found.append(YogaResult(
                name="Malavya Yoga",
                name_hindi="मालव्य योग",
                is_present=True,
                strength="Strong",
                description="Venus in Kendra in own/exalted sign",
                description_hindi="शुक्र केंद्र में स्वराशि/उच्च में",
                effects=["Luxury and comfort", "Beautiful possessions", "Artistic wealth"],
                effects_hindi=["विलासिता और आराम", "सुंदर संपत्ति", "कलात्मक धन"],
                planets_involved=["VENUS"]
            ))

        # Check POVERTY YOGAS

        # Kemadruma Yoga - Moon alone (no planets in 2nd or 12th from Moon)
        moon_house = self._get_planet_house("MOON")
        planets_around_moon = 0
        for planet in ["SUN", "MARS", "MERCURY", "JUPITER", "VENUS", "SATURN"]:
            p_house = self._get_planet_house(planet)
            if p_house == (moon_house % 12) + 1 or p_house == ((moon_house - 2) % 12) + 1:
                planets_around_moon += 1

        if planets_around_moon == 0:
            # Check for cancellation
            if not (self._is_planet_in_kendra("MOON") or self._is_planet_in_kendra("JUPITER")):
                poverty_yogas.append(YogaResult(
                    name="Kemadruma Yoga",
                    name_hindi="केमद्रुम योग",
                    is_present=True,
                    strength="Moderate",
                    description="Moon alone without planetary support",
                    description_hindi="चंद्रमा अकेला, ग्रहों का साथ नहीं",
                    effects=["Financial struggles possible", "Emotional challenges with money"],
                    effects_hindi=["आर्थिक कठिनाई संभव", "धन के साथ भावनात्मक चुनौतियां"],
                    planets_involved=["MOON"]
                ))

        # Determine wealth potential
        yoga_count = len(yogas_found)
        strong_yogas = sum(1 for y in yogas_found if y.strength == "Strong")

        if strong_yogas >= 2 or yoga_count >= 4:
            wealth_potential = "High"
            wealth_potential_hindi = "उच्च / High"
        elif yoga_count >= 2 or strong_yogas >= 1:
            wealth_potential = "Moderate"
            wealth_potential_hindi = "मध्यम / Moderate"
        else:
            wealth_potential = "Low"
            wealth_potential_hindi = "कम / Low"

        if poverty_yogas and yoga_count < 2:
            wealth_potential = "Low"
            wealth_potential_hindi = "कम / Low"

        # Wealth sources based on strong houses
        wealth_sources = []
        wealth_sources_hindi = []

        if self._get_planet_house(lord_2) in [1, 4, 7, 10, 11]:
            wealth_sources.append("Savings and accumulated wealth")
            wealth_sources_hindi.append("बचत और संचित धन")

        if self._get_planet_house(lord_11) in [1, 2, 4, 7, 10]:
            wealth_sources.append("Regular income and gains")
            wealth_sources_hindi.append("नियमित आय और लाभ")

        if "JUPITER" in [p for y in yogas_found for p in y.planets_involved]:
            wealth_sources.append("Education, consulting, advisory")
            wealth_sources_hindi.append("शिक्षा, परामर्श, सलाह")

        if "VENUS" in [p for y in yogas_found for p in y.planets_involved]:
            wealth_sources.append("Art, entertainment, luxury goods")
            wealth_sources_hindi.append("कला, मनोरंजन, विलासिता")

        if "MARS" in [p for y in yogas_found for p in y.planets_involved]:
            wealth_sources.append("Real estate, engineering, sports")
            wealth_sources_hindi.append("रियल एस्टेट, इंजीनियरिंग, खेल")

        return DhanaYogaAnalysis(
            yogas_present=yogas_found,
            wealth_potential=wealth_potential,
            wealth_potential_hindi=wealth_potential_hindi,
            best_wealth_periods=[f"{lord_2} Dasha", f"{lord_11} Dasha", "Jupiter Dasha"],
            wealth_sources=wealth_sources if wealth_sources else ["General employment"],
            wealth_sources_hindi=wealth_sources_hindi if wealth_sources_hindi else ["सामान्य रोजगार"],
            poverty_yogas=poverty_yogas
        )

    # =========================================================================
    # COMPLETE ANALYSIS
    # =========================================================================

    def get_complete_analysis(self) -> CareerFinanceReport:
        """Get complete career and finance analysis"""

        career = self.analyze_career()
        dhana = self.analyze_dhana_yogas()

        # Calculate scores
        career_score = 50  # Base score
        if career.government_job_yoga:
            career_score += 15
        if career.business_yoga:
            career_score += 15
        if career.tenth_lord_house in [1, 4, 7, 10]:
            career_score += 10
        if career.planets_in_tenth:
            career_score += len(career.planets_in_tenth) * 5
        career_score = min(100, career_score)

        wealth_score = 50  # Base score
        for yoga in dhana.yogas_present:
            if yoga.strength == "Strong":
                wealth_score += 15
            else:
                wealth_score += 10
        for _ in dhana.poverty_yogas:
            wealth_score -= 15
        wealth_score = max(0, min(100, wealth_score))

        # Generate summary
        summary_parts = []
        summary_hindi_parts = []

        if career_score >= 70:
            summary_parts.append("Excellent career potential with strong professional yogas.")
            summary_hindi_parts.append("उत्कृष्ट करियर क्षमता है।")
        elif career_score >= 50:
            summary_parts.append("Good career prospects with steady growth expected.")
            summary_hindi_parts.append("अच्छी करियर संभावनाएं हैं।")
        else:
            summary_parts.append("Career growth needs focused effort.")
            summary_hindi_parts.append("करियर विकास के लिए मेहनत जरूरी है।")

        if wealth_score >= 70:
            summary_parts.append("Strong wealth yogas indicate good financial fortune.")
            summary_hindi_parts.append("मजबूत धन योग अच्छे आर्थिक भाग्य का संकेत।")
        elif wealth_score >= 50:
            summary_parts.append("Moderate wealth potential with steady accumulation.")
            summary_hindi_parts.append("मध्यम धन क्षमता, धीरे-धीरे संचय होगा।")
        else:
            summary_parts.append("Financial planning and remedies recommended.")
            summary_hindi_parts.append("आर्थिक योजना और उपाय सुझाए जाते हैं।")

        # Recommendations
        recommendations = []
        recommendations_hindi = []

        if career.government_job_yoga:
            recommendations.append("Consider government sector jobs - you have strong Sun influence.")
            recommendations_hindi.append("सरकारी नौकरी पर विचार करें - सूर्य का प्रभाव मजबूत है।")

        if career.business_yoga:
            recommendations.append("Business ventures can be successful - Mercury-Venus combination favorable.")
            recommendations_hindi.append("व्यापार सफल हो सकता है - बुध-शुक्र का संयोग अनुकूल है।")

        if career.foreign_career_yoga:
            recommendations.append("Opportunities in foreign lands or MNCs indicated.")
            recommendations_hindi.append("विदेश या MNC में अवसर दिखते हैं।")

        if dhana.wealth_potential == "Low":
            recommendations.append("Strengthen 2nd and 11th house lords through remedies.")
            recommendations_hindi.append("उपायों से 2nd और 11th भाव के स्वामी को मजबूत करें।")

        return CareerFinanceReport(
            career_analysis=career,
            dhana_yoga_analysis=dhana,
            overall_career_score=career_score,
            overall_wealth_score=wealth_score,
            summary=" ".join(summary_parts),
            summary_hindi=" ".join(summary_hindi_parts),
            recommendations=recommendations,
            recommendations_hindi=recommendations_hindi
        )


# =============================================================================
# CONVENIENCE FUNCTION
# =============================================================================

def analyze_career_finance(kundali_data: Dict[str, Any]) -> CareerFinanceReport:
    """
    Convenience function to analyze career and finance.

    Args:
        kundali_data: Kundali dictionary with planet positions

    Returns:
        CareerFinanceReport object
    """
    analyzer = CareerFinanceAnalyzer(kundali_data)
    return analyzer.get_complete_analysis()
