"""
Dosha Analysis Module - Comprehensive Dosha Detection

Based on authentic Vedic texts:
- Brihat Parashara Hora Shastra (BPHS)
- Phaladeepika by Mantreshwara
- Jataka Parijata
- Laghu Parashari

Implements:
1. Kaal Sarp Dosha (12 types)
2. Pitra Dosha
3. Shani Sade Sati (detailed phases)
4. Guru Chandal Dosha
5. Grahan Dosha
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum


# =============================================================================
# ENUMS AND CONSTANTS
# =============================================================================

class DoshaSeverity(Enum):
    NONE = "none"
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"


class KaalSarpType(Enum):
    """12 Types of Kaal Sarp Dosha based on Rahu's house position"""
    ANANT = ("Anant", 1, "अनंत काल सर्प", "Rahu in 1st, Ketu in 7th")
    KULIK = ("Kulik", 2, "कुलिक काल सर्प", "Rahu in 2nd, Ketu in 8th")
    VASUKI = ("Vasuki", 3, "वासुकी काल सर्प", "Rahu in 3rd, Ketu in 9th")
    SHANKHAPAL = ("Shankhapal", 4, "शंखपाल काल सर्प", "Rahu in 4th, Ketu in 10th")
    PADMA = ("Padma", 5, "पद्म काल सर्प", "Rahu in 5th, Ketu in 11th")
    MAHAPADMA = ("Mahapadma", 6, "महापद्म काल सर्प", "Rahu in 6th, Ketu in 12th")
    TAKSHAK = ("Takshak", 7, "तक्षक काल सर्प", "Rahu in 7th, Ketu in 1st")
    KARKOTAK = ("Karkotak", 8, "कर्कोटक काल सर्प", "Rahu in 8th, Ketu in 2nd")
    SHANKHACHUR = ("Shankhachur", 9, "शंखचूड़ काल सर्प", "Rahu in 9th, Ketu in 3rd")
    GHATAK = ("Ghatak", 10, "घातक काल सर्प", "Rahu in 10th, Ketu in 4th")
    VISHDHAR = ("Vishdhar", 11, "विषधर काल सर्प", "Rahu in 11th, Ketu in 5th")
    SHESHNAG = ("Sheshnag", 12, "शेषनाग काल सर्प", "Rahu in 12th, Ketu in 6th")


# Sade Sati effects for each Moon sign
SADE_SATI_EFFECTS = {
    "Mesha": {
        "phase1": "करियर में रुकावट, मानसिक तनाव / Career obstacles, mental stress",
        "phase2": "स्वास्थ्य समस्या, आर्थिक दबाव / Health issues, financial pressure",
        "phase3": "धीरे-धीरे सुधार, नई शुरुआत / Gradual improvement, new beginnings"
    },
    "Vrishabha": {
        "phase1": "खर्च बढ़ेंगे, यात्रा संभव / Expenses increase, travel possible",
        "phase2": "स्वास्थ्य ध्यान दें, परिवार में तनाव / Watch health, family tension",
        "phase3": "आय में सुधार, स्थिरता / Income improves, stability"
    },
    "Mithuna": {
        "phase1": "संबंधों में तनाव, खर्च / Relationship stress, expenses",
        "phase2": "निर्णय में कठिनाई, भ्रम / Difficulty in decisions, confusion",
        "phase3": "बातचीत से समाधान / Resolution through communication"
    },
    "Karka": {
        "phase1": "मानसिक अशांति, घर में समस्या / Mental unrest, home issues",
        "phase2": "माता की चिंता, भावनात्मक तनाव / Mother's concern, emotional stress",
        "phase3": "शांति धीरे आएगी / Peace will come gradually"
    },
    "Simha": {
        "phase1": "आत्मविश्वास में कमी, रुकावट / Confidence low, obstacles",
        "phase2": "नेतृत्व में चुनौती, अहंकार टूटेगा / Leadership challenges, ego breaks",
        "phase3": "सीख मिलेगी, विकास / Lessons learned, growth"
    },
    "Kanya": {
        "phase1": "स्वास्थ्य, काम में दिक्कत / Health, work issues",
        "phase2": "विश्लेषण पक्षाघात, चिंता / Analysis paralysis, anxiety",
        "phase3": "व्यावहारिक समाधान मिलेंगे / Practical solutions emerge"
    },
    "Tula": {
        "phase1": "साझेदारी में समस्या / Partnership issues",
        "phase2": "न्याय की तलाश, संतुलन बिगड़े / Seeking justice, balance disturbed",
        "phase3": "नए रिश्ते, समझौता / New relationships, compromise"
    },
    "Vrishchika": {
        "phase1": "गहरा परिवर्तन शुरू / Deep transformation begins",
        "phase2": "पुराना छूटेगा, कठिन समय / Old leaves, difficult time",
        "phase3": "नवजन्म, शक्ति / Rebirth, power"
    },
    "Dhanu": {
        "phase1": "धर्म-कर्म में संदेह / Doubt in beliefs",
        "phase2": "गुरु/पिता से दूरी, यात्रा / Distance from guru/father, travel",
        "phase3": "नई दिशा, ज्ञान / New direction, knowledge"
    },
    "Makara": {
        "phase1": "करियर में बदलाव / Career changes",
        "phase2": "कड़ी मेहनत जरूरी, धैर्य / Hard work needed, patience",
        "phase3": "सफलता की नींव / Foundation for success"
    },
    "Kumbha": {
        "phase1": "मित्रता में बदलाव / Friendship changes",
        "phase2": "अकेलापन, आय में उतार-चढ़ाव / Loneliness, income fluctuation",
        "phase3": "नया नेटवर्क, लाभ / New network, gains"
    },
    "Meena": {
        "phase1": "आध्यात्मिक जागृति / Spiritual awakening",
        "phase2": "भ्रम, खर्च, स्वास्थ्य / Confusion, expenses, health",
        "phase3": "मोक्ष की ओर, शांति / Towards liberation, peace"
    }
}


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class DoshaResult:
    """Result for a single dosha analysis"""
    name: str
    name_hindi: str
    is_present: bool
    severity: DoshaSeverity
    description: str
    description_hindi: str
    effects: List[str]
    effects_hindi: List[str]
    remedies: List[str]
    remedies_hindi: List[str]
    cancellation_factors: List[str] = field(default_factory=list)
    additional_info: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KaalSarpResult(DoshaResult):
    """Specific result for Kaal Sarp Dosha"""
    kaal_sarp_type: Optional[KaalSarpType] = None
    is_partial: bool = False
    ascending: bool = True  # True if planets go Rahu->Ketu, False if Ketu->Rahu


@dataclass
class SadeSatiResult(DoshaResult):
    """Specific result for Sade Sati"""
    current_phase: Optional[str] = None  # "rising", "peak", "setting", or None
    phase_start_date: Optional[str] = None
    phase_end_date: Optional[str] = None
    is_dhaiya: bool = False  # Small Panoti


@dataclass
class CompleteDoshaAnalysis:
    """Complete dosha analysis for a Kundali"""
    kaal_sarp: KaalSarpResult
    pitra_dosha: DoshaResult
    sade_sati: SadeSatiResult
    guru_chandal: DoshaResult
    grahan_dosha: DoshaResult
    manglik_dosha: DoshaResult
    summary: str
    summary_hindi: str
    total_doshas_found: int
    overall_severity: DoshaSeverity


# =============================================================================
# DOSHA ANALYZER CLASS
# =============================================================================

class DoshaAnalyzer:
    """
    Comprehensive Dosha Analyzer based on Vedic Astrology principles.

    All calculations follow BPHS and classical texts.
    """

    def __init__(self, kundali_data: Dict[str, Any]):
        """
        Initialize with Kundali data.

        Args:
            kundali_data: Dictionary containing planet positions, houses, etc.
        """
        self.kundali = kundali_data
        self.planets = kundali_data.get("planets", {})
        self.houses = kundali_data.get("houses", {})
        self.lagna = kundali_data.get("lagna", {})
        self.moon_sign = self._get_moon_sign()

    def _get_moon_sign(self) -> str:
        """Get Moon's rashi name"""
        moon = self.planets.get("MOON", {})
        return moon.get("rashi", "Mesha")

    def _get_planet_house(self, planet: str) -> int:
        """Get house number (1-12) for a planet"""
        planet_data = self.planets.get(planet, {})
        return planet_data.get("house", 1)

    def _get_planet_rashi_num(self, planet: str) -> int:
        """Get rashi number (0-11) for a planet"""
        planet_data = self.planets.get(planet, {})
        return planet_data.get("rashi_num", 0)

    def _are_planets_conjunct(self, planet1: str, planet2: str, orb: float = 10.0) -> bool:
        """Check if two planets are conjunct (same sign or within orb)"""
        p1_rashi = self._get_planet_rashi_num(planet1)
        p2_rashi = self._get_planet_rashi_num(planet2)

        if p1_rashi == p2_rashi:
            return True

        # Check longitude proximity
        p1_long = self.planets.get(planet1, {}).get("longitude", 0)
        p2_long = self.planets.get(planet2, {}).get("longitude", 0)

        diff = abs(p1_long - p2_long)
        if diff > 180:
            diff = 360 - diff

        return diff <= orb

    # =========================================================================
    # KAAL SARP DOSHA
    # =========================================================================

    def analyze_kaal_sarp(self) -> KaalSarpResult:
        """
        Analyze Kaal Sarp Dosha.

        Kaal Sarp Dosha occurs when all 7 planets (Sun to Saturn) are
        hemmed between Rahu and Ketu axis.

        Based on: Brihat Parashara Hora Shastra
        """
        rahu_house = self._get_planet_house("RAHU")
        ketu_house = self._get_planet_house("KETU")

        # Get all planet houses
        main_planets = ["SUN", "MOON", "MARS", "MERCURY", "JUPITER", "VENUS", "SATURN"]
        planet_houses = [self._get_planet_house(p) for p in main_planets]

        # Check if all planets are between Rahu and Ketu
        # Ascending: Rahu -> planets -> Ketu (clockwise)
        # Descending: Ketu -> planets -> Rahu (anti-clockwise)

        def is_between_ascending(house, start, end):
            """Check if house is between start and end going clockwise"""
            if start < end:
                return start < house < end
            else:
                return house > start or house < end

        def is_between_descending(house, start, end):
            """Check if house is between start and end going anti-clockwise"""
            return is_between_ascending(house, end, start)

        # Check ascending Kaal Sarp (Rahu -> Ketu)
        ascending_count = sum(1 for h in planet_houses if is_between_ascending(h, rahu_house, ketu_house))

        # Check descending Kaal Sarp (Ketu -> Rahu)
        descending_count = sum(1 for h in planet_houses if is_between_descending(h, rahu_house, ketu_house))

        is_ascending = ascending_count == 7
        is_descending = descending_count == 7
        is_partial = ascending_count >= 5 or descending_count >= 5
        is_present = is_ascending or is_descending

        # Determine type based on Rahu's house
        kaal_sarp_type = None
        for kst in KaalSarpType:
            if kst.value[1] == rahu_house:
                kaal_sarp_type = kst
                break

        # Cancellation factors (per BPHS)
        cancellation = []

        # 1. If any planet is conjunct Rahu or Ketu
        for planet in main_planets:
            if self._are_planets_conjunct(planet, "RAHU") or self._are_planets_conjunct(planet, "KETU"):
                cancellation.append(f"{planet} conjunct Rahu/Ketu - दोष कम / Dosha reduced")

        # 2. If Rahu/Ketu in benefic signs
        rahu_rashi = self._get_planet_rashi_num("RAHU")
        if rahu_rashi in [1, 2, 4, 5, 8, 11]:  # Benefic positions for Rahu
            cancellation.append("Rahu in favorable sign - राहु शुभ राशि में / Rahu in good sign")

        # 3. Jupiter aspects Rahu/Ketu
        jupiter_house = self._get_planet_house("JUPITER")
        jupiter_aspects = [(jupiter_house + 4) % 12 + 1, (jupiter_house + 6) % 12 + 1, (jupiter_house + 8) % 12 + 1]
        if rahu_house in jupiter_aspects or ketu_house in jupiter_aspects:
            cancellation.append("Jupiter aspects Rahu/Ketu - गुरु की दृष्टि / Jupiter's aspect")

        # Determine severity
        if not is_present and not is_partial:
            severity = DoshaSeverity.NONE
        elif is_partial and not is_present:
            severity = DoshaSeverity.MILD
        elif is_present and cancellation:
            severity = DoshaSeverity.MODERATE
        else:
            severity = DoshaSeverity.SEVERE

        # Effects based on type
        effects = []
        effects_hindi = []

        if is_present and kaal_sarp_type:
            type_effects = {
                KaalSarpType.ANANT: ("Self-image issues, health concerns", "आत्म-छवि में समस्या, स्वास्थ्य चिंता"),
                KaalSarpType.KULIK: ("Financial struggles, family disputes", "आर्थिक समस्या, पारिवारिक विवाद"),
                KaalSarpType.VASUKI: ("Sibling issues, courage problems", "भाई-बहन से समस्या, साहस की कमी"),
                KaalSarpType.SHANKHAPAL: ("Property issues, mother's health", "संपत्ति समस्या, माता का स्वास्थ्य"),
                KaalSarpType.PADMA: ("Children delays, education issues", "संतान में देरी, शिक्षा में रुकावट"),
                KaalSarpType.MAHAPADMA: ("Debts, enemies, health issues", "कर्ज, शत्रु, स्वास्थ्य समस्या"),
                KaalSarpType.TAKSHAK: ("Marriage delays, partnership issues", "विवाह में देरी, साझेदारी समस्या"),
                KaalSarpType.KARKOTAK: ("Sudden events, inheritance issues", "अचानक घटनाएं, विरासत समस्या"),
                KaalSarpType.SHANKHACHUR: ("Fortune delays, father issues", "भाग्य में देरी, पिता से समस्या"),
                KaalSarpType.GHATAK: ("Career obstacles, reputation issues", "करियर में रुकावट, प्रतिष्ठा समस्या"),
                KaalSarpType.VISHDHAR: ("Income fluctuation, unfulfilled desires", "आय में उतार-चढ़ाव, इच्छा अपूर्ण"),
                KaalSarpType.SHESHNAG: ("Expenses, sleep issues, foreign settlement", "खर्च, नींद समस्या, विदेश"),
            }
            eng, hindi = type_effects.get(kaal_sarp_type, ("General life obstacles", "जीवन में रुकावट"))
            effects.append(eng)
            effects_hindi.append(hindi)

        # Remedies
        remedies = [
            "Kaal Sarp Dosha Nivaran Puja at Trimbakeshwar or Rameswaram",
            "Recite Rahu Beej Mantra: 'Om Bhram Bhreem Bhroum Sah Rahave Namah' 18000 times",
            "Donate black sesame seeds on Saturday",
            "Wear Gomed (Hessonite) after consultation",
            "Visit Nageshwar Jyotirlinga"
        ]

        remedies_hindi = [
            "त्र्यंबकेश्वर या रामेश्वरम में काल सर्प दोष निवारण पूजा करवाएं",
            "राहु बीज मंत्र 'ॐ भ्रां भ्रीं भ्रौं सः राहवे नमः' 18000 बार जपें",
            "शनिवार को काले तिल दान करें",
            "ज्योतिषी से सलाह लेकर गोमेद धारण करें",
            "नागेश्वर ज्योतिर्लिंग के दर्शन करें"
        ]

        return KaalSarpResult(
            name="Kaal Sarp Dosha",
            name_hindi="काल सर्प दोष",
            is_present=is_present or is_partial,
            severity=severity,
            description=f"{'Full' if is_present else 'Partial'} Kaal Sarp Dosha - {kaal_sarp_type.value[0] if kaal_sarp_type else 'None'}" if is_present or is_partial else "No Kaal Sarp Dosha",
            description_hindi=f"{'पूर्ण' if is_present else 'आंशिक'} काल सर्प दोष - {kaal_sarp_type.value[2] if kaal_sarp_type else ''}" if is_present or is_partial else "काल सर्प दोष नहीं है",
            effects=effects if effects else ["No significant effects"],
            effects_hindi=effects_hindi if effects_hindi else ["कोई विशेष प्रभाव नहीं"],
            remedies=remedies if is_present or is_partial else [],
            remedies_hindi=remedies_hindi if is_present or is_partial else [],
            cancellation_factors=cancellation,
            kaal_sarp_type=kaal_sarp_type,
            is_partial=is_partial and not is_present,
            ascending=is_ascending
        )

    # =========================================================================
    # PITRA DOSHA
    # =========================================================================

    def analyze_pitra_dosha(self) -> DoshaResult:
        """
        Analyze Pitra Dosha (Ancestral Curse).

        Pitra Dosha occurs when:
        1. Sun is afflicted by Rahu/Ketu/Saturn
        2. 9th house or its lord is afflicted
        3. Sun in 9th with malefics

        Based on: Brihat Parashara Hora Shastra, Pitra Dosha chapter
        """
        sun_house = self._get_planet_house("SUN")
        sun_rashi = self._get_planet_rashi_num("SUN")
        ninth_house_sign = (self._get_planet_rashi_num("LAGNA") + 8) % 12  # 9th from Lagna

        # Check various conditions
        conditions_met = []

        # 1. Sun conjunct Rahu
        if self._are_planets_conjunct("SUN", "RAHU"):
            conditions_met.append("Sun-Rahu conjunction (Surya Grahan Yoga) - सूर्य-राहु युति")

        # 2. Sun conjunct Ketu
        if self._are_planets_conjunct("SUN", "KETU"):
            conditions_met.append("Sun-Ketu conjunction - सूर्य-केतु युति")

        # 3. Sun conjunct Saturn
        if self._are_planets_conjunct("SUN", "SATURN"):
            conditions_met.append("Sun-Saturn conjunction - सूर्य-शनि युति")

        # 4. Sun in 9th house with malefics
        if sun_house == 9:
            malefics_in_9th = []
            for malefic in ["MARS", "SATURN", "RAHU", "KETU"]:
                if self._get_planet_house(malefic) == 9:
                    malefics_in_9th.append(malefic)
            if malefics_in_9th:
                conditions_met.append(f"Sun in 9th with malefics - सूर्य 9वें भाव में पाप ग्रहों के साथ")

        # 5. Rahu in 9th house
        if self._get_planet_house("RAHU") == 9:
            conditions_met.append("Rahu in 9th house - राहु 9वें भाव में")

        # 6. 9th lord afflicted
        ninth_lord = self._get_house_lord(9)
        if ninth_lord:
            if self._are_planets_conjunct(ninth_lord, "RAHU") or self._are_planets_conjunct(ninth_lord, "KETU"):
                conditions_met.append(f"9th lord {ninth_lord} afflicted - 9वें भाव का स्वामी पीड़ित")

        is_present = len(conditions_met) > 0

        # Determine severity
        if len(conditions_met) == 0:
            severity = DoshaSeverity.NONE
        elif len(conditions_met) == 1:
            severity = DoshaSeverity.MILD
        elif len(conditions_met) == 2:
            severity = DoshaSeverity.MODERATE
        else:
            severity = DoshaSeverity.SEVERE

        effects = [
            "Obstacles in progress despite hard work",
            "Delays in marriage or childbirth",
            "Frequent health issues in family",
            "Sudden financial losses",
            "Lack of peace and harmony"
        ] if is_present else []

        effects_hindi = [
            "मेहनत के बावजूद तरक्की में रुकावट",
            "विवाह या संतान में देरी",
            "परिवार में बार-बार स्वास्थ्य समस्या",
            "अचानक आर्थिक नुकसान",
            "शांति और सामंजस्य की कमी"
        ] if is_present else []

        remedies = [
            "Perform Pitra Dosha Nivaran Puja on Amavasya",
            "Do Tarpan (water offering) for ancestors during Pitru Paksha",
            "Feed Brahmins and donate to charity in ancestors' name",
            "Recite Pitra Gayatri Mantra daily",
            "Visit Gaya for Pind Daan"
        ]

        remedies_hindi = [
            "अमावस्या पर पितृ दोष निवारण पूजा करें",
            "पितृ पक्ष में पूर्वजों को तर्पण करें",
            "पूर्वजों के नाम पर ब्राह्मण भोजन और दान करें",
            "रोज़ पितृ गायत्री मंत्र का जाप करें",
            "गया में पिंड दान करें"
        ]

        return DoshaResult(
            name="Pitra Dosha",
            name_hindi="पितृ दोष",
            is_present=is_present,
            severity=severity,
            description=f"Pitra Dosha present due to: {', '.join(conditions_met)}" if is_present else "No Pitra Dosha",
            description_hindi=f"पितृ दोष है: {', '.join(conditions_met)}" if is_present else "पितृ दोष नहीं है",
            effects=effects,
            effects_hindi=effects_hindi,
            remedies=remedies if is_present else [],
            remedies_hindi=remedies_hindi if is_present else [],
            additional_info={"conditions": conditions_met}
        )

    def _get_house_lord(self, house_num: int) -> Optional[str]:
        """Get the lord planet of a house"""
        # This would need the actual lagna to calculate
        # For now, return a placeholder
        lagna_num = self._get_planet_rashi_num("LAGNA") if "LAGNA" in self.planets else 0
        house_sign = (lagna_num + house_num - 1) % 12

        sign_lords = {
            0: "MARS", 1: "VENUS", 2: "MERCURY", 3: "MOON",
            4: "SUN", 5: "MERCURY", 6: "VENUS", 7: "MARS",
            8: "JUPITER", 9: "SATURN", 10: "SATURN", 11: "JUPITER"
        }
        return sign_lords.get(house_sign)

    # =========================================================================
    # SADE SATI
    # =========================================================================

    def analyze_sade_sati(self, current_saturn_rashi: int = None) -> SadeSatiResult:
        """
        Analyze Shani Sade Sati (7.5 years of Saturn).

        Sade Sati occurs when Saturn transits:
        - 12th from Moon (Rising phase - 2.5 years)
        - Over Moon sign (Peak phase - 2.5 years)
        - 2nd from Moon (Setting phase - 2.5 years)

        Small Panoti (Dhaiya) occurs when Saturn is in 4th or 8th from Moon.

        Based on: Classical transit principles
        """
        moon_rashi = self._get_planet_rashi_num("MOON")
        moon_sign_name = self._get_moon_sign()

        # If current Saturn position not provided, use natal Saturn
        if current_saturn_rashi is None:
            current_saturn_rashi = self._get_planet_rashi_num("SATURN")

        # Calculate relative position
        saturn_from_moon = (current_saturn_rashi - moon_rashi) % 12 + 1

        # Determine phase
        current_phase = None
        is_dhaiya = False

        if saturn_from_moon == 12:
            current_phase = "rising"
            phase_desc = "Rising Phase (1st 2.5 years)"
            phase_desc_hindi = "उदय चरण (पहले 2.5 साल)"
        elif saturn_from_moon == 1:
            current_phase = "peak"
            phase_desc = "Peak Phase (Middle 2.5 years) - Most intense"
            phase_desc_hindi = "शिखर चरण (बीच के 2.5 साल) - सबसे कठिन"
        elif saturn_from_moon == 2:
            current_phase = "setting"
            phase_desc = "Setting Phase (Last 2.5 years)"
            phase_desc_hindi = "अस्त चरण (आखिरी 2.5 साल)"
        elif saturn_from_moon == 4:
            is_dhaiya = True
            phase_desc = "Small Panoti (Dhaiya) - Saturn in 4th from Moon"
            phase_desc_hindi = "छोटी पनौती (ढैया) - शनि चंद्र से 4वें में"
        elif saturn_from_moon == 8:
            is_dhaiya = True
            phase_desc = "Small Panoti (Dhaiya) - Saturn in 8th from Moon"
            phase_desc_hindi = "छोटी पनौती (ढैया) - शनि चंद्र से 8वें में"
        else:
            phase_desc = "No Sade Sati or Dhaiya currently"
            phase_desc_hindi = "अभी साढ़े साती या ढैया नहीं है"

        is_present = current_phase is not None or is_dhaiya

        # Determine severity
        if not is_present:
            severity = DoshaSeverity.NONE
        elif is_dhaiya:
            severity = DoshaSeverity.MILD
        elif current_phase == "peak":
            severity = DoshaSeverity.SEVERE
        else:
            severity = DoshaSeverity.MODERATE

        # Get sign-specific effects
        sign_effects = SADE_SATI_EFFECTS.get(moon_sign_name, {})

        effects = []
        effects_hindi = []

        if current_phase:
            phase_effect = sign_effects.get(f"phase{1 if current_phase == 'rising' else 2 if current_phase == 'peak' else 3}", "")
            if phase_effect:
                parts = phase_effect.split(" / ")
                effects_hindi.append(parts[0])
                effects.append(parts[1] if len(parts) > 1 else parts[0])

        if is_dhaiya:
            effects.append("Minor obstacles, need for patience")
            effects_hindi.append("छोटी रुकावटें, धैर्य की जरूरत")

        # General Sade Sati effects
        if current_phase:
            effects.extend([
                "Mental stress and anxiety",
                "Career challenges or changes",
                "Health issues, especially chronic",
                "Financial pressures",
                "Relationship strains"
            ])
            effects_hindi.extend([
                "मानसिक तनाव और चिंता",
                "करियर में चुनौती या बदलाव",
                "स्वास्थ्य समस्या, खासकर पुरानी",
                "आर्थिक दबाव",
                "रिश्तों में तनाव"
            ])

        remedies = [
            "Recite Shani Chalisa and Shani Stotra on Saturdays",
            "Donate black items (sesame, cloth, iron) on Saturdays",
            "Feed crows and black dogs",
            "Light mustard oil lamp under Peepal tree on Saturday evenings",
            "Wear Blue Sapphire (Neelam) only after proper consultation",
            "Visit Shani temple on Saturdays",
            "Chant 'Om Sham Shanaishcharaya Namah' 108 times daily"
        ]

        remedies_hindi = [
            "शनिवार को शनि चालीसा और शनि स्तोत्र पढ़ें",
            "शनिवार को काली चीजें (तिल, कपड़ा, लोहा) दान करें",
            "कौओं और काले कुत्तों को खाना खिलाएं",
            "शनिवार शाम को पीपल के पेड़ के नीचे सरसों के तेल का दीपक जलाएं",
            "नीलम सिर्फ अच्छी सलाह के बाद ही पहनें",
            "शनिवार को शनि मंदिर जाएं",
            "'ॐ शं शनैश्चराय नमः' रोज़ 108 बार जपें"
        ]

        return SadeSatiResult(
            name="Shani Sade Sati",
            name_hindi="शनि साढ़े साती",
            is_present=is_present,
            severity=severity,
            description=phase_desc,
            description_hindi=phase_desc_hindi,
            effects=effects,
            effects_hindi=effects_hindi,
            remedies=remedies if is_present else [],
            remedies_hindi=remedies_hindi if is_present else [],
            current_phase=current_phase,
            is_dhaiya=is_dhaiya,
            additional_info={
                "moon_sign": moon_sign_name,
                "saturn_position": saturn_from_moon
            }
        )

    # =========================================================================
    # GURU CHANDAL DOSHA
    # =========================================================================

    def analyze_guru_chandal(self) -> DoshaResult:
        """
        Analyze Guru Chandal Dosha.

        Occurs when Jupiter is conjunct with Rahu or Ketu.
        This afflicts Jupiter's beneficial nature.

        Based on: Brihat Parashara Hora Shastra
        """
        jupiter_conjunct_rahu = self._are_planets_conjunct("JUPITER", "RAHU")
        jupiter_conjunct_ketu = self._are_planets_conjunct("JUPITER", "KETU")

        is_present = jupiter_conjunct_rahu or jupiter_conjunct_ketu

        # Check for cancellation
        cancellation = []

        # Jupiter in own sign or exalted
        jupiter_rashi = self._get_planet_rashi_num("JUPITER")
        if jupiter_rashi in [8, 11]:  # Sagittarius, Pisces (own signs)
            cancellation.append("Jupiter in own sign - गुरु स्वराशि में")
        if jupiter_rashi == 3:  # Cancer (exalted)
            cancellation.append("Jupiter exalted - गुरु उच्च का")

        # Determine severity
        if not is_present:
            severity = DoshaSeverity.NONE
        elif cancellation:
            severity = DoshaSeverity.MILD
        else:
            severity = DoshaSeverity.MODERATE

        effects = [
            "Lack of respect for teachers and elders",
            "Problems in education",
            "Issues with children",
            "Spiritual confusion",
            "Wrong decisions in important matters"
        ] if is_present else []

        effects_hindi = [
            "गुरुजनों और बड़ों के प्रति सम्मान में कमी",
            "शिक्षा में समस्या",
            "संतान से जुड़ी समस्या",
            "आध्यात्मिक भ्रम",
            "महत्वपूर्ण मामलों में गलत निर्णय"
        ] if is_present else []

        remedies = [
            "Respect teachers and elders",
            "Recite Guru Beej Mantra: 'Om Gram Greem Groum Sah Gurave Namah'",
            "Wear Yellow Sapphire (Pukhraj) after consultation",
            "Donate yellow items on Thursdays",
            "Visit Guru temple on Thursdays"
        ]

        remedies_hindi = [
            "गुरुजनों और बड़ों का सम्मान करें",
            "गुरु बीज मंत्र जपें: 'ॐ ग्रां ग्रीं ग्रौं सः गुरवे नमः'",
            "सलाह के बाद पुखराज धारण करें",
            "गुरुवार को पीली चीजें दान करें",
            "गुरुवार को गुरु मंदिर जाएं"
        ]

        conjunction_type = "Rahu" if jupiter_conjunct_rahu else "Ketu" if jupiter_conjunct_ketu else None

        return DoshaResult(
            name="Guru Chandal Dosha",
            name_hindi="गुरु चांडाल दोष",
            is_present=is_present,
            severity=severity,
            description=f"Jupiter conjunct {conjunction_type} - Guru Chandal Yoga" if is_present else "No Guru Chandal Dosha",
            description_hindi=f"गुरु {conjunction_type} के साथ - गुरु चांडाल योग" if is_present else "गुरु चांडाल दोष नहीं है",
            effects=effects,
            effects_hindi=effects_hindi,
            remedies=remedies if is_present else [],
            remedies_hindi=remedies_hindi if is_present else [],
            cancellation_factors=cancellation,
            additional_info={"conjunction_with": conjunction_type}
        )

    # =========================================================================
    # GRAHAN DOSHA
    # =========================================================================

    def analyze_grahan_dosha(self) -> DoshaResult:
        """
        Analyze Grahan Dosha (Eclipse Affliction).

        Occurs when:
        - Sun is conjunct Rahu (Surya Grahan - Solar Eclipse)
        - Sun is conjunct Ketu
        - Moon is conjunct Rahu
        - Moon is conjunct Ketu (Chandra Grahan - Lunar Eclipse)

        Based on: Brihat Parashara Hora Shastra
        """
        sun_rahu = self._are_planets_conjunct("SUN", "RAHU")
        sun_ketu = self._are_planets_conjunct("SUN", "KETU")
        moon_rahu = self._are_planets_conjunct("MOON", "RAHU")
        moon_ketu = self._are_planets_conjunct("MOON", "KETU")

        grahan_types = []
        if sun_rahu or sun_ketu:
            grahan_types.append("Surya Grahan Dosha / सूर्य ग्रहण दोष")
        if moon_rahu or moon_ketu:
            grahan_types.append("Chandra Grahan Dosha / चंद्र ग्रहण दोष")

        is_present = len(grahan_types) > 0

        # Determine severity
        if not is_present:
            severity = DoshaSeverity.NONE
        elif len(grahan_types) == 1:
            severity = DoshaSeverity.MODERATE
        else:
            severity = DoshaSeverity.SEVERE

        effects = []
        effects_hindi = []

        if sun_rahu or sun_ketu:
            effects.extend([
                "Father's health or relationship issues",
                "Ego and self-confidence problems",
                "Government-related obstacles",
                "Eye or heart issues possible"
            ])
            effects_hindi.extend([
                "पिता के स्वास्थ्य या रिश्ते में समस्या",
                "अहंकार और आत्मविश्वास में समस्या",
                "सरकारी कामों में रुकावट",
                "आंख या हृदय की समस्या संभव"
            ])

        if moon_rahu or moon_ketu:
            effects.extend([
                "Mother's health or relationship issues",
                "Mental peace disturbed",
                "Emotional instability",
                "Sleep disorders possible"
            ])
            effects_hindi.extend([
                "माता के स्वास्थ्य या रिश्ते में समस्या",
                "मानसिक शांति में कमी",
                "भावनात्मक अस्थिरता",
                "नींद में समस्या संभव"
            ])

        remedies = [
            "Perform Grahan Dosha Shanti Puja",
            "Chant Surya/Chandra Beej Mantra as applicable",
            "Donate wheat (for Sun) or rice (for Moon) on respective days",
            "Observe fasting on Eclipse days",
            "Perform Rudrabhishek for severe cases"
        ]

        remedies_hindi = [
            "ग्रहण दोष शांति पूजा करवाएं",
            "सूर्य/चंद्र बीज मंत्र का जाप करें",
            "रविवार को गेहूं (सूर्य के लिए) या सोमवार को चावल (चंद्र के लिए) दान करें",
            "ग्रहण के दिन व्रत रखें",
            "गंभीर स्थिति में रुद्राभिषेक करवाएं"
        ]

        return DoshaResult(
            name="Grahan Dosha",
            name_hindi="ग्रहण दोष",
            is_present=is_present,
            severity=severity,
            description=f"Grahan Dosha: {', '.join(grahan_types)}" if is_present else "No Grahan Dosha",
            description_hindi=f"ग्रहण दोष: {', '.join(grahan_types)}" if is_present else "ग्रहण दोष नहीं है",
            effects=effects,
            effects_hindi=effects_hindi,
            remedies=remedies if is_present else [],
            remedies_hindi=remedies_hindi if is_present else [],
            additional_info={
                "sun_afflicted": sun_rahu or sun_ketu,
                "moon_afflicted": moon_rahu or moon_ketu,
                "grahan_types": grahan_types
            }
        )

    # =========================================================================
    # MANGLIK DOSHA (from existing implementation)
    # =========================================================================

    def _get_house_from_reference(self, planet: str, reference: str) -> int:
        """
        Calculate house position of a planet from a reference point.

        Args:
            planet: Planet name (e.g., "MARS")
            reference: Reference point - "LAGNA", "MOON", or "VENUS"

        Returns:
            House number (1-12) from the reference point
        """
        planet_rashi = self._get_planet_rashi_num(planet)

        if reference == "LAGNA":
            ref_rashi = self.lagna.get("rashi_num", 0)
        else:
            ref_rashi = self._get_planet_rashi_num(reference)

        # Calculate house (1-12)
        house = ((planet_rashi - ref_rashi) % 12) + 1
        return house

    def analyze_manglik_dosha(self) -> DoshaResult:
        """
        Analyze Manglik (Kuja/Chevvai) Dosha.

        Mars in houses 1, 2, 4, 7, 8, or 12 from Lagna, Moon, OR Venus
        causes Manglik Dosha.

        Based on: Brihat Parashara Hora Shastra, Jataka Parijata

        Note: Even if Mars is in these houses from ANY of the three
        reference points (Lagna, Moon, Venus), Manglik Dosha exists.
        """
        manglik_houses = {1, 2, 4, 7, 8, 12}

        # Check Mars house from all three reference points
        mars_from_lagna = self._get_house_from_reference("MARS", "LAGNA")
        mars_from_moon = self._get_house_from_reference("MARS", "MOON")
        mars_from_venus = self._get_house_from_reference("MARS", "VENUS")

        # Manglik if Mars is in 1, 2, 4, 7, 8, 12 from ANY reference
        is_manglik_from_lagna = mars_from_lagna in manglik_houses
        is_manglik_from_moon = mars_from_moon in manglik_houses
        is_manglik_from_venus = mars_from_venus in manglik_houses

        is_present = is_manglik_from_lagna or is_manglik_from_moon or is_manglik_from_venus

        # Build description of where manglik exists
        manglik_sources = []
        if is_manglik_from_lagna:
            manglik_sources.append(f"Lagna से {mars_from_lagna}वें भाव में")
        if is_manglik_from_moon:
            manglik_sources.append(f"Moon से {mars_from_moon}वें भाव में")
        if is_manglik_from_venus:
            manglik_sources.append(f"Venus से {mars_from_venus}वें भाव में")

        # Check cancellation factors
        cancellation = []
        mars_rashi = self._get_planet_rashi_num("MARS")

        # 1. Mars in own sign (Aries=0, Scorpio=7)
        if mars_rashi in [0, 7]:
            cancellation.append("Mars in own sign (Aries/Scorpio) - मंगल स्वराशि में (मेष/वृश्चिक)")

        # 2. Mars exalted (Capricorn=9)
        if mars_rashi == 9:
            cancellation.append("Mars exalted in Capricorn - मंगल मकर में उच्च का")

        # 3. Mars debilitated (Cancer=3) - some texts say this reduces effect
        if mars_rashi == 3:
            cancellation.append("Mars debilitated in Cancer - मंगल कर्क में नीच का (प्रभाव कम)")

        # 4. Jupiter aspects Mars (5th, 7th, 9th aspect)
        jupiter_house = self._get_house_from_reference("JUPITER", "LAGNA")
        mars_house_from_lagna = mars_from_lagna
        jupiter_aspects = [(jupiter_house + 4) % 12 or 12, (jupiter_house + 6) % 12 or 12, (jupiter_house + 8) % 12 or 12]
        if mars_house_from_lagna in jupiter_aspects or jupiter_house == mars_house_from_lagna:
            cancellation.append("Jupiter aspects/conjuncts Mars - गुरु की दृष्टि/युति मंगल पर")

        # 5. Venus aspects Mars
        venus_house = self._get_house_from_reference("VENUS", "LAGNA")
        if venus_house == mars_house_from_lagna:
            cancellation.append("Venus conjunct Mars - शुक्र-मंगल युति (दोष कम)")

        # 6. Mars in 2nd house in Gemini/Virgo (Mercury signs)
        if mars_from_lagna == 2 and mars_rashi in [2, 5]:
            cancellation.append("Mars in 2nd in Mercury sign - मंगल 2 में बुध राशि में (दोष कम)")

        # 7. Mars in 12th house in Taurus/Libra (Venus signs)
        if mars_from_lagna == 12 and mars_rashi in [1, 6]:
            cancellation.append("Mars in 12th in Venus sign - मंगल 12 में शुक्र राशि में (दोष कम)")

        # 8. If partner is also Manglik
        # (This is checked during matching, not here)

        # Determine severity
        if not is_present:
            severity = DoshaSeverity.NONE
        elif len(cancellation) >= 2:
            severity = DoshaSeverity.MILD
        elif cancellation:
            severity = DoshaSeverity.MODERATE
        elif mars_from_lagna in {7, 8} or mars_from_moon in {7, 8}:
            severity = DoshaSeverity.SEVERE
        else:
            severity = DoshaSeverity.MODERATE

        effects = [
            "Delays or obstacles in marriage / विवाह में देरी या रुकावट",
            "Marital discord and arguments possible / वैवाहिक कलह संभव",
            "Aggressive or dominating temperament / तीक्ष्ण या दबंग स्वभाव",
            "Partner's health may need attention / जीवनसाथी के स्वास्थ्य पर ध्यान दें",
            "High energy that needs positive channeling / ऊर्जा को सकारात्मक दिशा दें"
        ] if is_present else []

        effects_hindi = [
            "विवाह में देरी या बाधा आ सकती है",
            "वैवाहिक जीवन में तनाव या कलह संभव",
            "स्वभाव में तीक्ष्णता या क्रोध",
            "जीवनसाथी के स्वास्थ्य की चिंता",
            "उच्च ऊर्जा को सही दिशा देना आवश्यक"
        ] if is_present else []

        remedies = [
            "Kumbh Vivah (symbolic marriage with pot/tree) before actual marriage",
            "Recite Hanuman Chalisa daily, especially on Tuesdays",
            "Fast on Tuesdays (Mangalvar Vrat)",
            "Donate red lentils, red cloth, copper on Tuesdays",
            "Marry a Manglik partner (doshas cancel each other)",
            "Worship Lord Hanuman and Kartikeya",
            "Chant 'Om Kraam Kreem Kraum Sah Bhaumaya Namah' 108 times daily"
        ]

        remedies_hindi = [
            "विवाह से पहले कुंभ विवाह (घड़े/पेड़ से) करें",
            "प्रतिदिन हनुमान चालीसा पढ़ें, विशेषकर मंगलवार को",
            "मंगलवार को व्रत रखें",
            "मंगलवार को मसूर दाल, लाल कपड़ा, तांबा दान करें",
            "मांगलिक व्यक्ति से विवाह करें (दोष समाप्त)",
            "हनुमान जी और कार्तिकेय की पूजा करें",
            "मंगल मंत्र 'ॐ क्रां क्रीं क्रौं सः भौमाय नमः' 108 बार जपें"
        ]

        # Build description
        if is_present:
            sources_str = ", ".join(manglik_sources)
            description = f"Manglik Dosha present - Mars in houses {sources_str}"
            description_hindi = f"मांगलिक दोष है - मंगल {sources_str}"
        else:
            description = "No Manglik Dosha - Mars not in 1, 2, 4, 7, 8, 12 from Lagna/Moon/Venus"
            description_hindi = "मांगलिक दोष नहीं है - मंगल लग्न/चंद्र/शुक्र से 1,2,4,7,8,12 भाव में नहीं"

        return DoshaResult(
            name="Manglik Dosha",
            name_hindi="मांगलिक दोष",
            is_present=is_present,
            severity=severity,
            description=description,
            description_hindi=description_hindi,
            effects=effects,
            effects_hindi=effects_hindi,
            remedies=remedies if is_present else [],
            remedies_hindi=remedies_hindi if is_present else [],
            cancellation_factors=cancellation,
            additional_info={
                "mars_from_lagna": mars_from_lagna,
                "mars_from_moon": mars_from_moon,
                "mars_from_venus": mars_from_venus,
                "is_manglik_from_lagna": is_manglik_from_lagna,
                "is_manglik_from_moon": is_manglik_from_moon,
                "is_manglik_from_venus": is_manglik_from_venus
            }
        )

    # =========================================================================
    # COMPLETE ANALYSIS
    # =========================================================================

    def get_complete_analysis(self, current_saturn_rashi: int = None) -> CompleteDoshaAnalysis:
        """
        Get complete dosha analysis for the Kundali.

        Args:
            current_saturn_rashi: Current transit position of Saturn (0-11)

        Returns:
            CompleteDoshaAnalysis with all doshas analyzed
        """
        kaal_sarp = self.analyze_kaal_sarp()
        pitra = self.analyze_pitra_dosha()
        sade_sati = self.analyze_sade_sati(current_saturn_rashi)
        guru_chandal = self.analyze_guru_chandal()
        grahan = self.analyze_grahan_dosha()
        manglik = self.analyze_manglik_dosha()

        # Count doshas
        doshas_present = [
            kaal_sarp, pitra, sade_sati, guru_chandal, grahan, manglik
        ]
        total_found = sum(1 for d in doshas_present if d.is_present)

        # Determine overall severity
        severities = [d.severity for d in doshas_present if d.is_present]
        if DoshaSeverity.SEVERE in severities:
            overall = DoshaSeverity.SEVERE
        elif DoshaSeverity.MODERATE in severities:
            overall = DoshaSeverity.MODERATE
        elif DoshaSeverity.MILD in severities:
            overall = DoshaSeverity.MILD
        else:
            overall = DoshaSeverity.NONE

        # Generate summary
        if total_found == 0:
            summary = "No significant doshas found in this Kundali. The chart is relatively clean."
            summary_hindi = "इस कुंडली में कोई महत्वपूर्ण दोष नहीं है। कुंडली साफ है।"
        elif total_found <= 2:
            summary = f"{total_found} dosha(s) found. Remedies are recommended for better results."
            summary_hindi = f"{total_found} दोष पाए गए। बेहतर परिणाम के लिए उपाय करें।"
        else:
            summary = f"{total_found} doshas found. Multiple remedies strongly recommended. Consult an astrologer."
            summary_hindi = f"{total_found} दोष पाए गए। उपाय अवश्य करें। ज्योतिषी से मिलें।"

        return CompleteDoshaAnalysis(
            kaal_sarp=kaal_sarp,
            pitra_dosha=pitra,
            sade_sati=sade_sati,
            guru_chandal=guru_chandal,
            grahan_dosha=grahan,
            manglik_dosha=manglik,
            summary=summary,
            summary_hindi=summary_hindi,
            total_doshas_found=total_found,
            overall_severity=overall
        )


# =============================================================================
# CONVENIENCE FUNCTION
# =============================================================================

def analyze_doshas(kundali_data: Dict[str, Any], current_saturn_rashi: int = None) -> CompleteDoshaAnalysis:
    """
    Convenience function to analyze all doshas.

    Args:
        kundali_data: Kundali dictionary with planet positions
        current_saturn_rashi: Current Saturn transit position (0-11)

    Returns:
        CompleteDoshaAnalysis object
    """
    analyzer = DoshaAnalyzer(kundali_data)
    return analyzer.get_complete_analysis(current_saturn_rashi)
