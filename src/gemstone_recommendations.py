"""
Gemstone (Ratna) Recommendations based on Vedic Astrology
Based on authentic sources:
- Brihat Parashara Hora Shastra (BPHS) - Chapter on Ratna
- Garuda Purana (Ratna Pariksha chapter)
- Brihat Samhita by Varahamihira
- Jataka Parijata
- Mani Mala (classical gemology text)
- Phaladeepika by Mantreshwara

BPHS Priority for Gemstone Recommendations:
1. Current Mahadasha Lord (PRIMARY) - Most important per BPHS
2. Lagna Lord - For overall wellbeing
3. Yogakaraka Planet - For Raja Yoga results
4. Moon Sign Lord - For mental peace
5. 9th Lord (Bhagya) - For fortune

NEVER recommend gemstones of:
- Functional malefics (6th, 8th, 12th lords)
- 3rd and 11th lords
- Dusthana lords (especially 8th - Maraka)
- Shadow planets (Rahu/Ketu) unless during their Mahadasha

Functional Benefics/Malefics are determined per Lagna as per BPHS:
- Trikona lords (5th, 9th) are always benefic
- Kendra lords (1st, 4th, 7th, 10th) become neutral
- Lagna lord is always benefic regardless of other lordships
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

from .config import (
    Planet, RASHIS, PLANET_NAMES, PLANET_DIGNITIES,
    FUNCTIONAL_BENEFICS, FUNCTIONAL_MALEFICS, YOGAKARAKA,
    HOUSE_LORDSHIPS, NATURAL_RELATIONSHIPS,
    KENDRA_HOUSES, TRIKONA_HOUSES, DUSTHANA_HOUSES
)


# =============================================================================
# GEMSTONE DATA (from Garuda Purana, Brihat Samhita, Mani Mala)
# =============================================================================

@dataclass
class GemstoneInfo:
    """Complete information about a gemstone."""
    name_hindi: str
    name_english: str
    name_sanskrit: str
    planet: str
    color: str
    finger: str  # Which finger to wear
    finger_hindi: str
    metal: str  # Gold/Silver
    metal_hindi: str
    minimum_weight_ratti: float
    minimum_weight_carat: float
    day: str  # Day to wear
    day_hindi: str
    time: str  # Best time to wear
    time_hindi: str
    nakshatra: List[str]  # Favorable nakshatras for wearing
    mantra: str
    mantra_count: int
    alternative_stones: List[str]  # Upratna (substitute stones)
    benefits: List[str]
    precautions: List[str]


# Planet to Gemstone Mapping (as per Garuda Purana and Brihat Samhita)
PLANET_GEMSTONE_MAP: Dict[str, GemstoneInfo] = {
    "SUN": GemstoneInfo(
        name_hindi="माणिक्य (Manikya)",
        name_english="Ruby",
        name_sanskrit="माणिक्य / पद्मराग",
        planet="SUN",
        color="गहरा लाल / Deep Red",
        finger="अनामिका (Ring Finger)",
        finger_hindi="अनामिका उंगली",
        metal="Gold (सोना)",
        metal_hindi="सोना",
        minimum_weight_ratti=3.0,
        minimum_weight_carat=2.625,
        day="Ravivaar (Sunday)",
        day_hindi="रविवार",
        time="Sunrise (सूर्योदय के समय)",
        time_hindi="प्रातः सूर्योदय के 1 घंटे के भीतर",
        nakshatra=["Krittika", "Uttara Phalguni", "Uttara Ashadha"],
        mantra="ॐ ह्रां ह्रीं ह्रौं सः सूर्याय नमः",
        mantra_count=7000,
        alternative_stones=["Garnet (तामड़ा)", "Red Spinel (लाल स्पिनेल)", "Star Ruby"],
        benefits=[
            "आत्मविश्वास और नेतृत्व क्षमता बढ़ती है",
            "सरकारी कार्यों में सफलता मिलती है",
            "पिता से संबंध सुधरते हैं",
            "हृदय और आंखों की समस्याओं में लाभ",
            "प्रतिष्ठा और सम्मान में वृद्धि"
        ],
        precautions=[
            "शनि या राहु की दशा में सावधानी से पहनें",
            "तुला और कुंभ लग्न वालों को नहीं पहनना चाहिए",
            "उच्च रक्तचाप वालों को सावधानी बरतनी चाहिए",
            "पित्त प्रकृति वालों के लिए उपयुक्त नहीं"
        ]
    ),
    "MOON": GemstoneInfo(
        name_hindi="मोती (Moti)",
        name_english="Pearl",
        name_sanskrit="मुक्ता / मौक्तिक",
        planet="MOON",
        color="सफेद / चमकदार / White-Lustrous",
        finger="कनिष्ठा (Little Finger)",
        finger_hindi="छोटी उंगली",
        metal="Silver (चांदी)",
        metal_hindi="चांदी",
        minimum_weight_ratti=4.0,
        minimum_weight_carat=3.5,
        day="Somvaar (Monday)",
        day_hindi="सोमवार",
        time="Evening (शुक्ल पक्ष में सायंकाल)",
        time_hindi="शुक्ल पक्ष के सोमवार, सायंकाल",
        nakshatra=["Rohini", "Hasta", "Shravana"],
        mantra="ॐ श्रां श्रीं श्रौं सः चंद्रमसे नमः",
        mantra_count=11000,
        alternative_stones=["Moonstone (चंद्रमणि)", "White Coral", "White Sapphire"],
        benefits=[
            "मन की शांति और स्थिरता मिलती है",
            "माता से संबंध सुधरते हैं",
            "भावनात्मक संतुलन बढ़ता है",
            "नींद और मानसिक स्वास्थ्य में सुधार",
            "जल संबंधी व्यवसाय में लाभ"
        ],
        precautions=[
            "कफ प्रकृति वालों को सावधानी से पहनें",
            "अत्यधिक भावुक व्यक्तियों के लिए उपयुक्त नहीं",
            "वृश्चिक और मकर लग्न वालों को परहेज करें",
            "कृष्ण पक्ष में धारण न करें"
        ]
    ),
    "MARS": GemstoneInfo(
        name_hindi="मूंगा (Moonga)",
        name_english="Red Coral",
        name_sanskrit="प्रवाल / विद्रुम",
        planet="MARS",
        color="लाल / संतरी-लाल / Red-Orange",
        finger="अनामिका (Ring Finger)",
        finger_hindi="अनामिका उंगली",
        metal="Gold or Copper (सोना या तांबा)",
        metal_hindi="सोना या तांबा",
        minimum_weight_ratti=6.0,
        minimum_weight_carat=5.25,
        day="Mangalvaar (Tuesday)",
        day_hindi="मंगलवार",
        time="Morning (प्रातःकाल सूर्योदय के बाद)",
        time_hindi="प्रातः 6-8 बजे के बीच",
        nakshatra=["Mrigashira", "Chitra", "Dhanishta"],
        mantra="ॐ क्रां क्रीं क्रौं सः भौमाय नमः",
        mantra_count=10000,
        alternative_stones=["Carnelian (अकीक)", "Red Jasper", "Red Agate"],
        benefits=[
            "साहस और आत्मविश्वास बढ़ता है",
            "भूमि और संपत्ति संबंधी लाभ",
            "रक्त संबंधी समस्याओं में लाभ",
            "भाई-बहनों से संबंध सुधरते हैं",
            "ऊर्जा और शारीरिक शक्ति में वृद्धि"
        ],
        precautions=[
            "पित्त और रक्त विकार वालों को सावधानी से",
            "मिथुन और कन्या लग्न वालों के लिए अशुभ",
            "क्रोधी स्वभाव वालों को नहीं पहनना चाहिए",
            "गर्मियों में सावधानी बरतें"
        ]
    ),
    "MERCURY": GemstoneInfo(
        name_hindi="पन्ना (Panna)",
        name_english="Emerald",
        name_sanskrit="मरकत / गारुत्मत",
        planet="MERCURY",
        color="हरा / Green",
        finger="कनिष्ठा (Little Finger)",
        finger_hindi="छोटी उंगली",
        metal="Gold (सोना)",
        metal_hindi="सोना",
        minimum_weight_ratti=3.5,
        minimum_weight_carat=3.0,
        day="Budhvaar (Wednesday)",
        day_hindi="बुधवार",
        time="Morning (प्रातःकाल 2 घंटे के भीतर)",
        time_hindi="सूर्योदय के 2 घंटे के भीतर",
        nakshatra=["Ashlesha", "Jyeshtha", "Revati"],
        mantra="ॐ ब्रां ब्रीं ब्रौं सः बुधाय नमः",
        mantra_count=9000,
        alternative_stones=["Green Tourmaline", "Peridot (जबरजद)", "Green Onyx"],
        benefits=[
            "बुद्धि और वाक् शक्ति में वृद्धि",
            "व्यापार और व्यवसाय में सफलता",
            "संचार और लेखन कौशल में सुधार",
            "त्वचा रोगों में लाभ",
            "शिक्षा और परीक्षा में सफलता"
        ],
        precautions=[
            "मेष और वृश्चिक लग्न वालों को सावधानी से",
            "गुरु की महादशा में विचार करके पहनें",
            "अत्यधिक सोचने वालों के लिए उपयुक्त नहीं",
            "नकली पन्ने से हानि हो सकती है"
        ]
    ),
    "JUPITER": GemstoneInfo(
        name_hindi="पुखराज (Pukhraj)",
        name_english="Yellow Sapphire",
        name_sanskrit="पुष्पराग / गुरुरत्न",
        planet="JUPITER",
        color="पीला / Yellow",
        finger="तर्जनी (Index Finger)",
        finger_hindi="तर्जनी उंगली",
        metal="Gold (सोना)",
        metal_hindi="सोना",
        minimum_weight_ratti=3.25,
        minimum_weight_carat=2.85,
        day="Guruvaar (Thursday)",
        day_hindi="गुरुवार",
        time="Morning (प्रातःकाल पूजा के बाद)",
        time_hindi="प्रातः 6-8 बजे के बीच",
        nakshatra=["Punarvasu", "Vishakha", "Purva Bhadrapada"],
        mantra="ॐ ग्रां ग्रीं ग्रौं सः गुरवे नमः",
        mantra_count=19000,
        alternative_stones=["Yellow Topaz (सुनहला)", "Citrine", "Yellow Tourmaline"],
        benefits=[
            "धन और समृद्धि में वृद्धि",
            "विवाह और संतान सुख में लाभ",
            "ज्ञान और विद्या में प्रगति",
            "गुरुजनों और पितृजनों का आशीर्वाद",
            "न्याय और धर्म में विश्वास बढ़ता है"
        ],
        precautions=[
            "तुला और मकर लग्न वालों के लिए अशुभ",
            "शुक्र की महादशा में सावधानी से",
            "अत्यधिक वजन का पुखराज हानिकारक",
            "दोषयुक्त रत्न कभी न पहनें"
        ]
    ),
    "VENUS": GemstoneInfo(
        name_hindi="हीरा (Heera)",
        name_english="Diamond",
        name_sanskrit="वज्र / हीरक",
        planet="VENUS",
        color="पारदर्शी / सफेद / Colorless",
        finger="मध्यमा (Middle Finger)",
        finger_hindi="मध्यमा उंगली",
        metal="Platinum or White Gold",
        metal_hindi="प्लैटिनम या सफेद सोना",
        minimum_weight_ratti=0.5,
        minimum_weight_carat=0.43,
        day="Shukravaar (Friday)",
        day_hindi="शुक्रवार",
        time="Morning (शुक्ल पक्ष में प्रातःकाल)",
        time_hindi="शुक्ल पक्ष के शुक्रवार, प्रातःकाल",
        nakshatra=["Bharani", "Purva Phalguni", "Purva Ashadha"],
        mantra="ॐ द्रां द्रीं द्रौं सः शुक्राय नमः",
        mantra_count=16000,
        alternative_stones=["White Sapphire (सफेद पुखराज)", "Zircon", "White Topaz", "Opal"],
        benefits=[
            "विवाह सुख और वैवाहिक जीवन में सुधार",
            "कला और सौंदर्य में रुचि बढ़ती है",
            "भौतिक सुख-सुविधाएं प्राप्त होती हैं",
            "प्रजनन क्षमता में वृद्धि",
            "आकर्षण और करिश्मा बढ़ता है"
        ],
        precautions=[
            "कर्क और सिंह लग्न वालों को नहीं पहनना चाहिए",
            "सूर्य या चंद्र की महादशा में सावधानी से",
            "दोषयुक्त हीरा अत्यंत हानिकारक",
            "नीलम के साथ कभी न पहनें"
        ]
    ),
    "SATURN": GemstoneInfo(
        name_hindi="नीलम (Neelam)",
        name_english="Blue Sapphire",
        name_sanskrit="नीलमणि / इंद्रनील",
        planet="SATURN",
        color="गहरा नीला / Deep Blue",
        finger="मध्यमा (Middle Finger)",
        finger_hindi="मध्यमा उंगली",
        metal="Silver or Iron (चांदी या लोहा)",
        metal_hindi="पंचधातु या लोहा",
        minimum_weight_ratti=4.25,
        minimum_weight_carat=3.72,
        day="Shanivaar (Saturday)",
        day_hindi="शनिवार",
        time="Evening (सायंकाल सूर्यास्त से पहले)",
        time_hindi="शाम 5-7 बजे के बीच",
        nakshatra=["Pushya", "Anuradha", "Uttara Bhadrapada"],
        mantra="ॐ प्रां प्रीं प्रौं सः शनैश्चराय नमः",
        mantra_count=23000,
        alternative_stones=["Amethyst (जमुनिया)", "Blue Spinel", "Iolite (नीली)"],
        benefits=[
            "व्यवसाय और कैरियर में उन्नति",
            "दीर्घायु और स्वास्थ्य लाभ",
            "कानूनी मामलों में विजय",
            "अनुशासन और कठोर परिश्रम में सफलता",
            "शनि दोष और साढ़ेसाती में राहत"
        ],
        precautions=[
            "परीक्षण के बाद ही पहनें - पहले 3 दिन धागे में बांधकर रखें",
            "सिंह और कर्क लग्न वालों को कभी नहीं पहनना चाहिए",
            "माणिक्य के साथ एक साथ न पहनें",
            "दोषयुक्त नीलम अत्यंत हानिकारक है",
            "गर्भवती महिलाओं को नहीं पहनना चाहिए"
        ]
    ),
    "RAHU": GemstoneInfo(
        name_hindi="गोमेद (Gomed)",
        name_english="Hessonite Garnet",
        name_sanskrit="गोमेदक",
        planet="RAHU",
        color="शहद जैसा भूरा / Honey-Brown",
        finger="मध्यमा (Middle Finger)",
        finger_hindi="मध्यमा उंगली",
        metal="Silver or Ashtadhatu (चांदी या अष्टधातु)",
        metal_hindi="चांदी या अष्टधातु",
        minimum_weight_ratti=5.25,
        minimum_weight_carat=4.6,
        day="Shanivaar (Saturday)",
        day_hindi="शनिवार",
        time="Evening (रात्रि में राहुकाल के बाद)",
        time_hindi="सायंकाल या रात्रि में",
        nakshatra=["Ardra", "Swati", "Shatabhisha"],
        mantra="ॐ भ्रां भ्रीं भ्रौं सः राहवे नमः",
        mantra_count=18000,
        alternative_stones=["Orange Zircon", "Spessartite Garnet"],
        benefits=[
            "राहु दोष और कालसर्प योग में लाभ",
            "मानसिक भ्रम और चिंता में कमी",
            "विदेश यात्रा और विदेश में सफलता",
            "छुपे हुए शत्रुओं से रक्षा",
            "राजनीति और प्रशासन में सफलता"
        ],
        precautions=[
            "केतु की महादशा में न पहनें",
            "लहसुनिया के साथ न पहनें",
            "मानसिक अस्थिरता वालों को सावधानी से",
            "शुद्ध और दोषरहित गोमेद ही पहनें"
        ]
    ),
    "KETU": GemstoneInfo(
        name_hindi="लहसुनिया (Lehsunia)",
        name_english="Cat's Eye",
        name_sanskrit="वैदूर्य / केतुरत्न",
        planet="KETU",
        color="भूरा-हरा / Greenish-Brown",
        finger="मध्यमा (Middle Finger)",
        finger_hindi="मध्यमा उंगली",
        metal="Silver or Gold (चांदी या सोना)",
        metal_hindi="चांदी या सोना",
        minimum_weight_ratti=3.0,
        minimum_weight_carat=2.625,
        day="Mangalvaar (Tuesday) or Guruvaar (Thursday)",
        day_hindi="मंगलवार या गुरुवार",
        time="Evening (सायंकाल)",
        time_hindi="सायंकाल 4-6 बजे के बीच",
        nakshatra=["Ashwini", "Magha", "Mula"],
        mantra="ॐ स्रां स्रीं स्रौं सः केतवे नमः",
        mantra_count=17000,
        alternative_stones=["Tiger's Eye", "Cat's Eye Quartz", "Chrysoberyl"],
        benefits=[
            "केतु दोष और ग्रहण योग में लाभ",
            "आध्यात्मिक उन्नति और मोक्ष मार्ग",
            "अज्ञात शत्रुओं और भूत-प्रेत बाधा से रक्षा",
            "दुर्घटनाओं से बचाव",
            "अंतर्ज्ञान और छठी इंद्रिय का विकास"
        ],
        precautions=[
            "राहु की महादशा में न पहनें",
            "गोमेद के साथ न पहनें",
            "स्पष्ट Cat's Eye effect वाला ही पहनें",
            "दोषयुक्त रत्न हानिकारक है"
        ]
    )
}


# =============================================================================
# CONFLICTING GEMSTONE COMBINATIONS (from Brihat Samhita)
# =============================================================================

CONFLICTING_STONES = {
    "SUN": ["SATURN", "VENUS"],  # Ruby should not be worn with Blue Sapphire or Diamond
    "MOON": ["RAHU", "KETU"],    # Pearl should not be worn with Hessonite or Cat's Eye
    "MARS": ["MERCURY", "SATURN"],  # Coral should not be worn with Emerald or Blue Sapphire
    "MERCURY": ["MOON", "MARS"],  # Emerald should not be worn with Pearl or Coral
    "JUPITER": ["VENUS", "MERCURY"],  # Yellow Sapphire should not be worn with Diamond or Emerald
    "VENUS": ["SUN", "MOON", "JUPITER"],  # Diamond conflicts with Ruby, Pearl, Yellow Sapphire
    "SATURN": ["SUN", "MOON", "MARS"],  # Blue Sapphire conflicts with Ruby, Pearl, Coral
    "RAHU": ["MOON", "KETU"],  # Hessonite should not be worn with Pearl or Cat's Eye
    "KETU": ["MOON", "RAHU"]   # Cat's Eye should not be worn with Pearl or Hessonite
}


# =============================================================================
# GEMSTONE ADVISOR CLASS
# =============================================================================

@dataclass
class GemstoneRecommendation:
    """A single gemstone recommendation with all details."""
    planet: str
    planet_hindi: str
    gemstone: GemstoneInfo
    reason: str
    reason_hindi: str
    priority: int  # 1 = Primary, 2 = Secondary, 3 = Optional
    priority_label: str
    priority_label_hindi: str
    current_dasha_relevant: bool
    contraindications: List[str]
    special_instructions: List[str]


class GemstoneAdvisor:
    """
    Provides gemstone recommendations based on Kundali analysis.

    Recommendation Logic (as per classical texts):
    1. Lagna Lord - Primary recommendation if weak/afflicted
    2. Moon Sign Lord - For emotional wellbeing
    3. Yogakaraka Planet - If exists for the Lagna
    4. 9th and 10th Lord - For fortune and career
    5. Current Dasha Lord - If beneficial

    NEVER recommends gems for:
    - Natural malefics (unless specific yoga)
    - Dusthana lords (6th, 8th, 12th)
    - Afflicted planets without remedy yoga
    """

    def __init__(self, kundali):
        """Initialize with a Kundali object."""
        self.kundali = kundali
        self.lagna_rashi = kundali.lagna["rashi"]
        self.moon_rashi = kundali.planets["MOON"]["rashi"]
        self.planets = kundali.planets
        self.planets_in_houses = kundali.get_planets_in_houses()
        self.current_dasha = kundali.get_current_dasha()

    def _get_planet_strength(self, planet_name: str) -> Dict:
        """Analyze strength of a planet."""
        planet_data = self.planets.get(planet_name, {})
        rashi = planet_data.get("rashi", "")
        dignities = PLANET_DIGNITIES.get(planet_name, {})

        strength = {
            "is_exalted": rashi == dignities.get("exalted", ""),
            "is_debilitated": rashi == dignities.get("debilitated", ""),
            "is_own_sign": rashi in dignities.get("own", []),
            "is_mooltrikona": rashi == dignities.get("mooltrikona", ""),
            "is_retrograde": planet_data.get("is_retrograde", False),
            "is_weak": False,
            "is_strong": False
        }

        # Determine overall strength
        if strength["is_exalted"] or strength["is_mooltrikona"] or strength["is_own_sign"]:
            strength["is_strong"] = True
        elif strength["is_debilitated"]:
            strength["is_weak"] = True

        return strength

    def _is_functional_benefic(self, planet_name: str) -> bool:
        """Check if planet is a functional benefic for this lagna."""
        benefics = FUNCTIONAL_BENEFICS.get(self.lagna_rashi, [])
        return planet_name in benefics

    def _is_functional_malefic(self, planet_name: str) -> bool:
        """Check if planet is a functional malefic for this lagna."""
        malefics = FUNCTIONAL_MALEFICS.get(self.lagna_rashi, [])
        return planet_name in malefics

    def _get_yogakaraka(self) -> Optional[str]:
        """Get Yogakaraka planet for this lagna."""
        return YOGAKARAKA.get(self.lagna_rashi)

    def _get_lagna_lord(self) -> str:
        """Get the lord of the Lagna."""
        lagna_lord_map = {
            "Mesha": "MARS", "Vrishabha": "VENUS", "Mithuna": "MERCURY",
            "Karka": "MOON", "Simha": "SUN", "Kanya": "MERCURY",
            "Tula": "VENUS", "Vrishchika": "MARS", "Dhanu": "JUPITER",
            "Makara": "SATURN", "Kumbha": "SATURN", "Meena": "JUPITER"
        }
        return lagna_lord_map.get(self.lagna_rashi, "JUPITER")

    def _get_moon_sign_lord(self) -> str:
        """Get the lord of Moon sign."""
        lord_map = {
            "Mesha": "MARS", "Vrishabha": "VENUS", "Mithuna": "MERCURY",
            "Karka": "MOON", "Simha": "SUN", "Kanya": "MERCURY",
            "Tula": "VENUS", "Vrishchika": "MARS", "Dhanu": "JUPITER",
            "Makara": "SATURN", "Kumbha": "SATURN", "Meena": "JUPITER"
        }
        return lord_map.get(self.moon_rashi, "MOON")

    def _get_current_dasha_lord(self) -> str:
        """Get the current Mahadasha lord."""
        dasha_lord_map = {
            "Ketu": "KETU", "Venus": "VENUS", "Sun": "SUN",
            "Moon": "MOON", "Mars": "MARS", "Rahu": "RAHU",
            "Jupiter": "JUPITER", "Saturn": "SATURN", "Mercury": "MERCURY"
        }
        md_planet = self.current_dasha.get("mahadasha", {}).get("planet", "")
        return dasha_lord_map.get(md_planet, "JUPITER")

    def _should_recommend_gem(self, planet_name: str) -> Tuple[bool, str, str]:
        """
        Determine if gem should be recommended for this planet.
        Returns: (should_recommend, reason_english, reason_hindi)
        """
        # Never recommend for Rahu/Ketu unless specific conditions
        if planet_name in ["RAHU", "KETU"]:
            dasha_lord = self._get_current_dasha_lord()
            if dasha_lord == planet_name:
                return (True,
                        f"{planet_name} Mahadasha running - gem may help balance energies",
                        f"{planet_name} की महादशा चल रही है - रत्न ऊर्जा संतुलित कर सकता है")
            return (False,
                    f"{planet_name} is a shadow planet - gem not generally recommended",
                    f"{planet_name} छाया ग्रह है - रत्न सामान्यतः अनुशंसित नहीं")

        # Check if functional malefic
        if self._is_functional_malefic(planet_name):
            return (False,
                    f"{planet_name} is a functional malefic for {self.lagna_rashi} Lagna",
                    f"{planet_name} {self.lagna_rashi} लग्न के लिए कारक अशुभ ग्रह है")

        # Check if functional benefic
        if self._is_functional_benefic(planet_name):
            strength = self._get_planet_strength(planet_name)
            if strength["is_weak"]:
                return (True,
                        f"{planet_name} is benefic but weak - gem will strengthen",
                        f"{planet_name} शुभ लेकिन कमजोर है - रत्न मजबूत करेगा")
            return (True,
                    f"{planet_name} is a functional benefic for {self.lagna_rashi} Lagna",
                    f"{planet_name} {self.lagna_rashi} लग्न के लिए कारक शुभ ग्रह है")

        return (False,
                f"{planet_name} is neutral - gem not strongly recommended",
                f"{planet_name} तटस्थ है - रत्न विशेष अनुशंसित नहीं")

    def _get_contraindications(self, planet_name: str) -> List[str]:
        """Get list of contraindications for wearing this planet's gem."""
        contraindications = []
        gemstone = PLANET_GEMSTONE_MAP.get(planet_name)

        if gemstone:
            contraindications.extend(gemstone.precautions)

        # Add conflicting planets
        conflicts = CONFLICTING_STONES.get(planet_name, [])
        for conflict in conflicts:
            conflict_gem = PLANET_GEMSTONE_MAP.get(conflict)
            if conflict_gem:
                contraindications.append(
                    f"{gemstone.name_english} के साथ {conflict_gem.name_english} न पहनें / "
                    f"Do not wear {conflict_gem.name_english} with {gemstone.name_english}"
                )

        return contraindications

    def get_primary_recommendations(self) -> List[GemstoneRecommendation]:
        """
        Get primary (most important) gemstone recommendations.

        BPHS Priority Order:
        1. Current Mahadasha Lord (if functional benefic) - MOST IMPORTANT per BPHS
        2. Lagna Lord - Always beneficial for overall wellbeing
        3. Yogakaraka Planet - Gives Raja Yoga results

        Reference: Brihat Parashara Hora Shastra - Chapter on Ratna (Gemstones)
        """
        recommendations = []
        added_planets = set()

        # 1. Current Mahadasha Lord - PRIMARY per BPHS
        # "The gemstone of the ruling Mahadasha Lord, if benefic, should be worn first"
        dasha_lord = self._get_current_dasha_lord()
        if dasha_lord not in ["RAHU", "KETU"]:  # Avoid shadow planets
            should_rec, reason, reason_hindi = self._should_recommend_gem(dasha_lord)
            if should_rec:
                gemstone = PLANET_GEMSTONE_MAP.get(dasha_lord)
                if gemstone:
                    md_info = self.current_dasha.get("mahadasha", {})
                    recommendations.append(GemstoneRecommendation(
                        planet=dasha_lord,
                        planet_hindi=PLANET_NAMES[Planet[dasha_lord]]["hindi"],
                        gemstone=gemstone,
                        reason=f"Current Mahadasha Lord ({md_info.get('planet', dasha_lord)}) - {reason}",
                        reason_hindi=f"वर्तमान महादशा स्वामी ({md_info.get('planet', dasha_lord)}) - {reason_hindi}",
                        priority=1,
                        priority_label="Primary / MOST RECOMMENDED (Per BPHS)",
                        priority_label_hindi="प्राथमिक / सर्वाधिक अनुशंसित (BPHS के अनुसार)",
                        current_dasha_relevant=True,
                        contraindications=self._get_contraindications(dasha_lord),
                        special_instructions=[
                            "महादशा स्वामी का रत्न सबसे प्रभावशाली / Mahadasha Lord's gem is most effective",
                            "दशा काल में विशेष लाभकारी / Especially beneficial during Dasha period",
                            "BPHS: वर्तमान दशा के अनुसार रत्न धारण करें / Wear gem as per current Dasha"
                        ]
                    ))
                    added_planets.add(dasha_lord)

        # 2. Lagna Lord
        lagna_lord = self._get_lagna_lord()
        if lagna_lord not in added_planets:
            should_rec, reason, reason_hindi = self._should_recommend_gem(lagna_lord)
            if should_rec:
                gemstone = PLANET_GEMSTONE_MAP.get(lagna_lord)
                if gemstone:
                    recommendations.append(GemstoneRecommendation(
                        planet=lagna_lord,
                        planet_hindi=PLANET_NAMES[Planet[lagna_lord]]["hindi"],
                        gemstone=gemstone,
                        reason=f"Lagna Lord ({self.lagna_rashi}) - {reason}",
                        reason_hindi=f"लग्नेश ({self.lagna_rashi}) - {reason_hindi}",
                        priority=1,
                        priority_label="Primary / Highly Recommended",
                        priority_label_hindi="प्राथमिक / अत्यधिक अनुशंसित",
                        current_dasha_relevant=(lagna_lord == dasha_lord),
                        contraindications=self._get_contraindications(lagna_lord),
                        special_instructions=[
                            "लग्नेश का रत्न समग्र कल्याण के लिए / Lagna Lord's gem for overall wellbeing",
                            "जन्मदिन या लग्नेश के दिन धारण करें / Wear on birthday or Lagna Lord's day"
                        ]
                    ))
                    added_planets.add(lagna_lord)

        # 3. Yogakaraka (if exists)
        yogakaraka = self._get_yogakaraka()
        if yogakaraka and yogakaraka not in added_planets:
            should_rec, reason, reason_hindi = self._should_recommend_gem(yogakaraka)
            if should_rec:
                gemstone = PLANET_GEMSTONE_MAP.get(yogakaraka)
                if gemstone:
                    recommendations.append(GemstoneRecommendation(
                        planet=yogakaraka,
                        planet_hindi=PLANET_NAMES[Planet[yogakaraka]]["hindi"],
                        gemstone=gemstone,
                        reason=f"Yogakaraka Planet - {reason}",
                        reason_hindi=f"योगकारक ग्रह - {reason_hindi}",
                        priority=1,
                        priority_label="Primary / Raja Yoga Giver",
                        priority_label_hindi="प्राथमिक / राजयोग कारक",
                        current_dasha_relevant=(yogakaraka == dasha_lord),
                        contraindications=self._get_contraindications(yogakaraka),
                        special_instructions=[
                            "योगकारक रत्न राजयोग फल देता है / Yogakaraka gem gives Raja Yoga results",
                            "लग्नेश रत्न के साथ पहन सकते हैं / Can wear with Lagna Lord's gem"
                        ]
                    ))
                    added_planets.add(yogakaraka)

        return recommendations

    def get_secondary_recommendations(self) -> List[GemstoneRecommendation]:
        """Get secondary (supportive) gemstone recommendations."""
        recommendations = []
        primary_planets = [r.planet for r in self.get_primary_recommendations()]

        # 1. Moon Sign Lord (for emotional balance)
        moon_lord = self._get_moon_sign_lord()
        if moon_lord not in primary_planets:
            should_rec, reason, reason_hindi = self._should_recommend_gem(moon_lord)
            if should_rec:
                gemstone = PLANET_GEMSTONE_MAP.get(moon_lord)
                if gemstone:
                    recommendations.append(GemstoneRecommendation(
                        planet=moon_lord,
                        planet_hindi=PLANET_NAMES[Planet[moon_lord]]["hindi"],
                        gemstone=gemstone,
                        reason=f"Moon Sign Lord ({self.moon_rashi}) - {reason}",
                        reason_hindi=f"चंद्र राशि स्वामी ({self.moon_rashi}) - {reason_hindi}",
                        priority=2,
                        priority_label="Secondary / Recommended",
                        priority_label_hindi="द्वितीयक / अनुशंसित",
                        current_dasha_relevant=(moon_lord == self._get_current_dasha_lord()),
                        contraindications=self._get_contraindications(moon_lord),
                        special_instructions=[
                            "मानसिक शांति के लिए उपयोगी / Useful for mental peace",
                            "शुक्ल पक्ष में धारण करें / Wear during Shukla Paksha"
                        ]
                    ))

        # Note: Dasha Lord is now in PRIMARY recommendations per BPHS

        # 2. 9th Lord (Bhagya - Fortune) if different from primary planets
        ninth_lord = self._get_house_lord(9)
        if ninth_lord and ninth_lord not in primary_planets and ninth_lord != moon_lord:
            should_rec, reason, reason_hindi = self._should_recommend_gem(ninth_lord)
            if should_rec:
                gemstone = PLANET_GEMSTONE_MAP.get(ninth_lord)
                if gemstone:
                    recommendations.append(GemstoneRecommendation(
                        planet=ninth_lord,
                        planet_hindi=PLANET_NAMES[Planet[ninth_lord]]["hindi"],
                        gemstone=gemstone,
                        reason=f"9th House Lord (Bhagya/Fortune) - {reason}",
                        reason_hindi=f"भाग्य भाव (9वां) स्वामी - {reason_hindi}",
                        priority=2,
                        priority_label="Secondary / For Fortune & Luck",
                        priority_label_hindi="द्वितीयक / भाग्य वृद्धि हेतु",
                        current_dasha_relevant=(ninth_lord == self._get_current_dasha_lord()),
                        contraindications=self._get_contraindications(ninth_lord),
                        special_instructions=[
                            "भाग्योदय और धार्मिक कार्यों में लाभ / Benefits in fortune and religious pursuits",
                            "गुरुवार को धारण करना शुभ / Auspicious to wear on Thursday"
                        ]
                    ))

        return recommendations

    def _get_house_lord(self, house_num: int) -> Optional[str]:
        """Get the lord of a specific house based on Lagna."""
        house_to_sign_offset = house_num - 1
        lagna_index = {
            "Mesha": 0, "Vrishabha": 1, "Mithuna": 2, "Karka": 3,
            "Simha": 4, "Kanya": 5, "Tula": 6, "Vrishchika": 7,
            "Dhanu": 8, "Makara": 9, "Kumbha": 10, "Meena": 11
        }.get(self.lagna_rashi, 0)

        house_sign_index = (lagna_index + house_to_sign_offset) % 12
        sign_lords = {
            0: "MARS", 1: "VENUS", 2: "MERCURY", 3: "MOON",
            4: "SUN", 5: "MERCURY", 6: "VENUS", 7: "MARS",
            8: "JUPITER", 9: "SATURN", 10: "SATURN", 11: "JUPITER"
        }
        return sign_lords.get(house_sign_index)

    def get_stones_to_avoid(self) -> List[Dict]:
        """
        Get list of gemstones that should be avoided.

        Per BPHS, NEVER wear gemstones of:
        1. Functional malefics (6th, 8th, 12th lords; 3rd, 11th lords)
        2. Planets that are enemies of Lagna Lord
        3. Dusthana lords (especially 8th lord - death-inflicting)
        """
        avoid_list = []

        for planet in ["SUN", "MOON", "MARS", "MERCURY", "JUPITER", "VENUS", "SATURN"]:
            if self._is_functional_malefic(planet):
                gemstone = PLANET_GEMSTONE_MAP.get(planet)
                if gemstone:
                    # Get houses ruled by this planet
                    houses = HOUSE_LORDSHIPS.get(self.lagna_rashi, {}).get(planet, [])
                    house_str = ", ".join(map(str, houses)) if houses else "unknown"

                    # Determine severity
                    severity = "High"
                    severity_hindi = "गंभीर"
                    if 8 in houses:
                        severity = "Very High (8th Lord - Maraka)"
                        severity_hindi = "अत्यंत गंभीर (अष्टमेश - मारक)"
                    elif 6 in houses or 12 in houses:
                        severity = "High (Dusthana Lord)"
                        severity_hindi = "गंभीर (दुःस्थान स्वामी)"

                    avoid_list.append({
                        "planet": planet,
                        "planet_hindi": PLANET_NAMES[Planet[planet]]["hindi"],
                        "gemstone_english": gemstone.name_english,
                        "gemstone_hindi": gemstone.name_hindi,
                        "houses_ruled": houses,
                        "reason": f"{planet} rules houses {house_str} - functional malefic for {self.lagna_rashi} Lagna",
                        "reason_hindi": f"{planet} भाव {house_str} का स्वामी है - {self.lagna_rashi} लग्न के लिए अशुभ",
                        "severity": severity,
                        "severity_hindi": severity_hindi,
                        "warning": f"⚠️ AVOID: {gemstone.name_english} ({gemstone.name_hindi})",
                        "warning_hindi": f"⚠️ न पहनें: {gemstone.name_hindi} ({gemstone.name_english})"
                    })

        # Also add Rahu/Ketu warnings (always controversial)
        for shadow_planet in ["RAHU", "KETU"]:
            gemstone = PLANET_GEMSTONE_MAP.get(shadow_planet)
            if gemstone:
                avoid_list.append({
                    "planet": shadow_planet,
                    "planet_hindi": PLANET_NAMES[Planet[shadow_planet]]["hindi"],
                    "gemstone_english": gemstone.name_english,
                    "gemstone_hindi": gemstone.name_hindi,
                    "houses_ruled": [],
                    "reason": f"{shadow_planet} is a shadow planet - wear only during its Mahadasha after expert consultation",
                    "reason_hindi": f"{shadow_planet} छाया ग्रह है - केवल इसकी महादशा में विशेषज्ञ परामर्श के बाद पहनें",
                    "severity": "Caution Required",
                    "severity_hindi": "सावधानी आवश्यक",
                    "warning": f"⚠️ CAUTION: {gemstone.name_english} - Only during {shadow_planet} Mahadasha",
                    "warning_hindi": f"⚠️ सावधानी: {gemstone.name_hindi} - केवल {shadow_planet} महादशा में"
                })

        return avoid_list

    def get_complete_recommendations(self) -> Dict:
        """Get complete gemstone recommendations with all details."""
        primary = self.get_primary_recommendations()
        secondary = self.get_secondary_recommendations()
        avoid = self.get_stones_to_avoid()

        # Format current dasha info
        dasha_info = {
            "mahadasha": self.current_dasha.get("mahadasha", {}).get("planet", ""),
            "antardasha": self.current_dasha.get("antardasha", {}).get("planet", ""),
            "full_dasha": self.current_dasha.get("full_dasha", "")
        }

        return {
            "success": True,
            "lagna": {
                "rashi": self.lagna_rashi,
                "rashi_english": self.kundali.lagna["rashi_english"],
                "lord": self._get_lagna_lord()
            },
            "moon_sign": {
                "rashi": self.moon_rashi,
                "lord": self._get_moon_sign_lord()
            },
            "yogakaraka": self._get_yogakaraka(),
            "current_dasha": dasha_info,
            "primary_recommendations": [self._format_recommendation(r) for r in primary],
            "secondary_recommendations": [self._format_recommendation(r) for r in secondary],
            "stones_to_avoid": avoid,
            "general_guidelines": self._get_general_guidelines(),
            "disclaimer": self._get_disclaimer()
        }

    def _format_recommendation(self, rec: GemstoneRecommendation) -> Dict:
        """Format a recommendation for API response."""
        return {
            "planet": rec.planet,
            "planet_hindi": rec.planet_hindi,
            "gemstone": {
                "name_hindi": rec.gemstone.name_hindi,
                "name_english": rec.gemstone.name_english,
                "name_sanskrit": rec.gemstone.name_sanskrit,
                "color": rec.gemstone.color,
                "finger": rec.gemstone.finger,
                "finger_hindi": rec.gemstone.finger_hindi,
                "metal": rec.gemstone.metal,
                "metal_hindi": rec.gemstone.metal_hindi,
                "minimum_weight_ratti": rec.gemstone.minimum_weight_ratti,
                "minimum_weight_carat": rec.gemstone.minimum_weight_carat,
                "day": rec.gemstone.day,
                "day_hindi": rec.gemstone.day_hindi,
                "time": rec.gemstone.time,
                "time_hindi": rec.gemstone.time_hindi,
                "nakshatra": rec.gemstone.nakshatra,
                "mantra": rec.gemstone.mantra,
                "mantra_count": rec.gemstone.mantra_count,
                "alternative_stones": rec.gemstone.alternative_stones,
                "benefits": rec.gemstone.benefits,
                "precautions": rec.gemstone.precautions
            },
            "reason": rec.reason,
            "reason_hindi": rec.reason_hindi,
            "priority": rec.priority,
            "priority_label": rec.priority_label,
            "priority_label_hindi": rec.priority_label_hindi,
            "current_dasha_relevant": rec.current_dasha_relevant,
            "contraindications": rec.contraindications,
            "special_instructions": rec.special_instructions
        }

    def _get_general_guidelines(self) -> List[Dict]:
        """Get general guidelines for wearing gemstones."""
        return [
            {
                "title": "रत्न धारण करने से पहले / Before Wearing",
                "guidelines": [
                    "रत्न को रात भर कच्चे दूध या गंगाजल में रखें",
                    "सुबह स्नान के बाद शुद्ध वस्त्र पहनें",
                    "पूर्व या उत्तर दिशा की ओर मुख करके बैठें",
                    "दीपक और धूप जलाएं"
                ]
            },
            {
                "title": "धारण विधि / Wearing Procedure",
                "guidelines": [
                    "निर्धारित मंत्र का उचित संख्या में जाप करें",
                    "रत्न को अंगूठी या लॉकेट में पहनें",
                    "पहली बार शुभ मुहूर्त में ही धारण करें",
                    "रत्न धारण के बाद मीठा प्रसाद वितरित करें"
                ]
            },
            {
                "title": "सावधानियां / Precautions",
                "guidelines": [
                    "दोषयुक्त रत्न कभी न पहनें",
                    "विरोधी रत्न एक साथ न पहनें",
                    "रत्न को नियमित रूप से साफ करें",
                    "रत्न टूट जाए या रंग फीका पड़े तो तुरंत उतार दें",
                    "किसी अन्य का पहना हुआ रत्न न पहनें"
                ]
            },
            {
                "title": "विशेष ध्यान / Special Notes",
                "guidelines": [
                    "प्रमाणित रत्न विक्रेता से ही खरीदें",
                    "प्राकृतिक रत्न ही पहनें, सिंथेटिक नहीं",
                    "रत्न का वजन शरीर के वजन के अनुसार हो",
                    "किसी योग्य ज्योतिषी से परामर्श अवश्य लें"
                ]
            }
        ]

    def _get_disclaimer(self) -> Dict:
        """Get disclaimer text."""
        return {
            "hindi": "यह रत्न सुझाव केवल ज्योतिषीय मार्गदर्शन के लिए है। "
                     "कोई भी रत्न धारण करने से पहले किसी योग्य ज्योतिषी से परामर्श अवश्य लें। "
                     "रत्नों का प्रभाव व्यक्तिगत कुंडली और परिस्थितियों पर निर्भर करता है।",
            "english": "This gemstone suggestion is for astrological guidance only. "
                       "Please consult a qualified astrologer before wearing any gemstone. "
                       "The effect of gemstones depends on individual horoscope and circumstances."
        }


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_gemstone_for_planet(planet_name: str) -> Optional[Dict]:
    """Get gemstone information for a specific planet."""
    gemstone = PLANET_GEMSTONE_MAP.get(planet_name.upper())
    if gemstone:
        return {
            "name_hindi": gemstone.name_hindi,
            "name_english": gemstone.name_english,
            "name_sanskrit": gemstone.name_sanskrit,
            "planet": gemstone.planet,
            "color": gemstone.color,
            "finger": gemstone.finger,
            "finger_hindi": gemstone.finger_hindi,
            "metal": gemstone.metal,
            "metal_hindi": gemstone.metal_hindi,
            "minimum_weight_ratti": gemstone.minimum_weight_ratti,
            "minimum_weight_carat": gemstone.minimum_weight_carat,
            "day": gemstone.day,
            "day_hindi": gemstone.day_hindi,
            "time": gemstone.time,
            "time_hindi": gemstone.time_hindi,
            "nakshatra": gemstone.nakshatra,
            "mantra": gemstone.mantra,
            "mantra_count": gemstone.mantra_count,
            "alternative_stones": gemstone.alternative_stones,
            "benefits": gemstone.benefits,
            "precautions": gemstone.precautions
        }
    return None


def get_all_gemstones() -> List[Dict]:
    """Get list of all gemstones with basic info."""
    gemstones = []
    for planet, gemstone in PLANET_GEMSTONE_MAP.items():
        gemstones.append({
            "planet": planet,
            "planet_hindi": PLANET_NAMES[Planet[planet]]["hindi"],
            "gemstone_hindi": gemstone.name_hindi,
            "gemstone_english": gemstone.name_english,
            "color": gemstone.color,
            "finger": gemstone.finger
        })
    return gemstones


def check_stone_compatibility(stone1_planet: str, stone2_planet: str) -> Dict:
    """Check if two stones can be worn together."""
    stone1 = stone1_planet.upper()
    stone2 = stone2_planet.upper()

    conflicts1 = CONFLICTING_STONES.get(stone1, [])
    conflicts2 = CONFLICTING_STONES.get(stone2, [])

    is_compatible = stone2 not in conflicts1 and stone1 not in conflicts2

    gem1 = PLANET_GEMSTONE_MAP.get(stone1)
    gem2 = PLANET_GEMSTONE_MAP.get(stone2)

    return {
        "stone1": gem1.name_english if gem1 else stone1,
        "stone2": gem2.name_english if gem2 else stone2,
        "compatible": is_compatible,
        "message_hindi": (
            f"{gem1.name_hindi} और {gem2.name_hindi} साथ में पहन सकते हैं"
            if is_compatible else
            f"{gem1.name_hindi} और {gem2.name_hindi} एक साथ नहीं पहनने चाहिए - विरोधी ग्रह हैं"
        ) if gem1 and gem2 else "",
        "message_english": (
            f"{gem1.name_english} and {gem2.name_english} can be worn together"
            if is_compatible else
            f"{gem1.name_english} and {gem2.name_english} should not be worn together - conflicting planets"
        ) if gem1 and gem2 else ""
    }
