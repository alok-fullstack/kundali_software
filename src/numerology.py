"""
Vedic Numerology (Ank Jyotish) Calculator

Based on authentic sources:
- Vedic Numerology (Ank Shastra)
- Cheiro's Numerology (for reference)
- Indian Ank Jyotish traditions

Provides:
- Moolank (Root Number) from birth date
- Bhagyank (Destiny Number) from full DOB
- Namank (Name Number) using Chaldean & Pythagorean systems
- Planet-Number correlations per Vedic tradition
- Personality traits, lucky elements, compatibility analysis
- Name correction suggestions
"""

from datetime import datetime, date
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum


class NumerologySystem(Enum):
    """Numerology calculation systems."""
    CHALDEAN = "Chaldean"
    PYTHAGOREAN = "Pythagorean"


@dataclass
class NumerologyResult:
    """Complete numerology analysis result."""
    name: str
    birth_date: date
    moolank: int
    bhagyank: int
    namank_chaldean: int
    namank_pythagorean: int
    moolank_planet: str
    bhagyank_planet: str
    namank_planet_chaldean: str
    namank_planet_pythagorean: str
    personality_traits: List[str]
    life_path_description: str
    lucky_numbers: List[int]
    lucky_colors: List[str]
    lucky_days: List[str]
    lucky_gemstone: str
    friendly_numbers: List[int]
    unfriendly_numbers: List[int]
    name_analysis: Dict
    compatibility_numbers: List[int]


@dataclass
class NameCorrectionSuggestion:
    """Suggestion for name correction."""
    original_name: str
    suggested_name: str
    original_number: int
    new_number: int
    change_description: str
    benefit: str


@dataclass
class CompatibilityResult:
    """Compatibility result between two people."""
    person1_name: str
    person2_name: str
    person1_moolank: int
    person2_moolank: int
    person1_bhagyank: int
    person2_bhagyank: int
    compatibility_score: int
    compatibility_level: str
    strengths: List[str]
    challenges: List[str]
    remedies: List[str]


class NumerologyCalculator:
    """
    Vedic Numerology Calculator (Ank Jyotish).

    Planet-Number Mapping (Vedic):
    1 = Sun (Surya) - Aatma, leadership
    2 = Moon (Chandra) - Mann, emotions
    3 = Jupiter (Guru) - Gyan, wisdom
    4 = Rahu - Unexpected changes
    5 = Mercury (Budh) - Buddhi, intellect
    6 = Venus (Shukra) - Prem, beauty
    7 = Ketu - Spiritual detachment
    8 = Saturn (Shani) - Karma, discipline
    9 = Mars (Mangal) - Courage, energy
    """

    # Vedic Planet-Number Mapping
    NUMBER_PLANET_MAP = {
        1: {"planet": "Sun", "sanskrit": "Surya", "hindi": "सूर्य", "symbol": "1"},
        2: {"planet": "Moon", "sanskrit": "Chandra", "hindi": "चंद्र", "symbol": "2"},
        3: {"planet": "Jupiter", "sanskrit": "Guru", "hindi": "गुरु", "symbol": "3"},
        4: {"planet": "Rahu", "sanskrit": "Rahu", "hindi": "राहु", "symbol": "4"},
        5: {"planet": "Mercury", "sanskrit": "Budh", "hindi": "बुध", "symbol": "5"},
        6: {"planet": "Venus", "sanskrit": "Shukra", "hindi": "शुक्र", "symbol": "6"},
        7: {"planet": "Ketu", "sanskrit": "Ketu", "hindi": "केतु", "symbol": "7"},
        8: {"planet": "Saturn", "sanskrit": "Shani", "hindi": "शनि", "symbol": "8"},
        9: {"planet": "Mars", "sanskrit": "Mangal", "hindi": "मंगल", "symbol": "9"},
    }

    # Chaldean Number System (Ancient Babylonian - more mystical)
    CHALDEAN_MAP = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 8, 'G': 3, 'H': 5,
        'I': 1, 'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 7, 'P': 8,
        'Q': 1, 'R': 2, 'S': 3, 'T': 4, 'U': 6, 'V': 6, 'W': 6, 'X': 5,
        'Y': 1, 'Z': 7,
    }

    # Pythagorean Number System (Western - more common)
    PYTHAGOREAN_MAP = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8,
        'I': 9, 'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7,
        'Q': 8, 'R': 9, 'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6,
        'Y': 7, 'Z': 8,
    }

    # Hindi letter to number mapping (for Hindi names)
    HINDI_LETTER_MAP = {
        # Vowels (Swar)
        'अ': 1, 'आ': 1, 'इ': 1, 'ई': 1, 'उ': 6, 'ऊ': 6,
        'ए': 5, 'ऐ': 5, 'ओ': 7, 'औ': 7,
        # Consonants (Vyanjan)
        'क': 2, 'ख': 2, 'ग': 3, 'घ': 3, 'ङ': 5,
        'च': 3, 'छ': 3, 'ज': 1, 'झ': 1, 'ञ': 5,
        'ट': 4, 'ठ': 4, 'ड': 4, 'ढ': 4, 'ण': 5,
        'त': 4, 'थ': 4, 'द': 4, 'ध': 4, 'न': 5,
        'प': 8, 'फ': 8, 'ब': 2, 'भ': 2, 'म': 4,
        'य': 1, 'र': 2, 'ल': 3, 'व': 6, 'श': 3,
        'ष': 3, 'स': 3, 'ह': 5,
    }

    # Personality traits for each number (Hindi/English)
    PERSONALITY_TRAITS = {
        1: {
            "traits": [
                "नेतृत्व क्षमता / Leadership ability",
                "आत्मविश्वास / Self-confidence",
                "स्वतंत्रता प्रिय / Independence loving",
                "महत्वाकांक्षी / Ambitious",
                "सृजनात्मक / Creative",
                "अहंकार की प्रवृत्ति / Tendency towards ego",
            ],
            "description": "सूर्य की भांति तेजस्वी व्यक्तित्व। नेता बनने के गुण। स्वाभिमानी और आत्मनिर्भर। / Sun-like radiant personality. Leadership qualities. Self-respecting and self-reliant.",
        },
        2: {
            "traits": [
                "भावुक / Emotional",
                "कल्पनाशील / Imaginative",
                "सहयोगी / Cooperative",
                "कूटनीतिज्ञ / Diplomatic",
                "संवेदनशील / Sensitive",
                "अनिर्णय की प्रवृत्ति / Tendency to be indecisive",
            ],
            "description": "चंद्रमा जैसा शांत और भावुक स्वभाव। रिश्तों में निपुण। कला और संगीत प्रेमी। / Moon-like calm and emotional nature. Skilled in relationships. Lover of art and music.",
        },
        3: {
            "traits": [
                "आशावादी / Optimistic",
                "ज्ञान प्रेमी / Knowledge seeker",
                "धार्मिक / Religious",
                "उदार / Generous",
                "अनुशासित / Disciplined",
                "अति विस्तारवादी / Tendency to overexpand",
            ],
            "description": "गुरु की कृपा से ज्ञान और भाग्य का साथ। शिक्षा और आध्यात्मिकता में रुचि। / Blessed with knowledge and fortune by Jupiter. Interest in education and spirituality.",
        },
        4: {
            "traits": [
                "परिश्रमी / Hardworking",
                "व्यावहारिक / Practical",
                "अचानक परिवर्तन / Sudden changes",
                "विद्रोही / Rebellious",
                "तकनीकी दक्षता / Technical skills",
                "अस्थिरता / Instability",
            ],
            "description": "राहु के प्रभाव से जीवन में उतार-चढ़ाव। नई तकनीक और विचारों में रुचि। अप्रत्याशित सफलता। / Life fluctuations due to Rahu's influence. Interest in new technology and ideas. Unexpected success.",
        },
        5: {
            "traits": [
                "बुद्धिमान / Intelligent",
                "संचार कुशल / Good communicator",
                "बहुमुखी / Versatile",
                "व्यापारिक कौशल / Business acumen",
                "जिज्ञासु / Curious",
                "अस्थिर / Restless",
            ],
            "description": "बुध के प्रभाव से तेज बुद्धि और वाक्पटुता। व्यापार और संवाद में सफल। बहुमुखी प्रतिभा। / Sharp intellect and eloquence due to Mercury's influence. Successful in business and communication.",
        },
        6: {
            "traits": [
                "प्रेम प्रधान / Love-oriented",
                "सौंदर्य प्रेमी / Beauty loving",
                "कलात्मक / Artistic",
                "आकर्षक / Charming",
                "विलासी / Luxurious",
                "आलसी प्रवृत्ति / Lazy tendency",
            ],
            "description": "शुक्र के प्रभाव से प्रेम, सौंदर्य और कला का आकर्षण। रोमांटिक स्वभाव। भौतिक सुख प्रेमी। / Attraction to love, beauty and art due to Venus. Romantic nature. Lover of material comforts.",
        },
        7: {
            "traits": [
                "आध्यात्मिक / Spiritual",
                "रहस्यमय / Mysterious",
                "विश्लेषणात्मक / Analytical",
                "अंतर्मुखी / Introverted",
                "ज्ञान साधक / Knowledge seeker",
                "एकांत प्रिय / Solitude loving",
            ],
            "description": "केतु के प्रभाव से आध्यात्मिक झुकाव। रहस्य और गूढ़ विषयों में रुचि। मोक्ष की खोज। / Spiritual inclination due to Ketu. Interest in mysteries and occult. Quest for liberation.",
        },
        8: {
            "traits": [
                "कर्मयोगी / Action-oriented",
                "अनुशासित / Disciplined",
                "धैर्यवान / Patient",
                "न्यायप्रिय / Justice loving",
                "परिश्रमी / Hardworking",
                "कठोर / Harsh",
            ],
            "description": "शनि के प्रभाव से कर्म प्रधान जीवन। धीमी लेकिन स्थायी सफलता। संघर्ष से उन्नति। / Karma-oriented life due to Saturn. Slow but lasting success. Progress through struggle.",
        },
        9: {
            "traits": [
                "साहसी / Courageous",
                "ऊर्जावान / Energetic",
                "नेता / Leader",
                "जोशीला / Enthusiastic",
                "रक्षक / Protector",
                "आक्रामक / Aggressive",
            ],
            "description": "मंगल के प्रभाव से योद्धा स्वभाव। साहस और शक्ति। रक्षा और खेल में सफल। देशभक्त। / Warrior nature due to Mars. Courage and strength. Successful in defense and sports. Patriotic.",
        },
    }

    # Lucky colors for each number
    LUCKY_COLORS = {
        1: ["सुनहरा/Golden", "नारंगी/Orange", "पीला/Yellow"],
        2: ["सफेद/White", "क्रीम/Cream", "हल्का हरा/Light Green"],
        3: ["पीला/Yellow", "नारंगी/Orange", "गुलाबी/Pink"],
        4: ["नीला/Blue", "धूम्र/Grey", "खाकी/Khaki"],
        5: ["हरा/Green", "हल्का नीला/Light Blue", "सफेद/White"],
        6: ["हल्का नीला/Light Blue", "गुलाबी/Pink", "सफेद/White"],
        7: ["हल्का हरा/Light Green", "पीला/Yellow", "सफेद/White"],
        8: ["काला/Black", "गहरा नीला/Dark Blue", "बैंगनी/Purple"],
        9: ["लाल/Red", "गुलाबी/Pink", "मैरून/Maroon"],
    }

    # Lucky days for each number
    LUCKY_DAYS = {
        1: ["रविवार/Sunday"],
        2: ["सोमवार/Monday"],
        3: ["गुरुवार/Thursday"],
        4: ["रविवार/Sunday", "सोमवार/Monday", "शनिवार/Saturday"],
        5: ["बुधवार/Wednesday", "शुक्रवार/Friday"],
        6: ["शुक्रवार/Friday"],
        7: ["सोमवार/Monday", "रविवार/Sunday"],
        8: ["शनिवार/Saturday"],
        9: ["मंगलवार/Tuesday", "गुरुवार/Thursday"],
    }

    # Lucky gemstones for each number (cross-reference with Vedic gemstone recommendations)
    LUCKY_GEMSTONES = {
        1: {"name": "माणिक/Ruby", "sanskrit": "Manikya", "planet": "Sun"},
        2: {"name": "मोती/Pearl", "sanskrit": "Moti", "planet": "Moon"},
        3: {"name": "पुखराज/Yellow Sapphire", "sanskrit": "Pukhraj", "planet": "Jupiter"},
        4: {"name": "गोमेद/Hessonite", "sanskrit": "Gomed", "planet": "Rahu"},
        5: {"name": "पन्ना/Emerald", "sanskrit": "Panna", "planet": "Mercury"},
        6: {"name": "हीरा/Diamond", "sanskrit": "Heera", "planet": "Venus"},
        7: {"name": "लहसुनिया/Cat's Eye", "sanskrit": "Lehsuniya", "planet": "Ketu"},
        8: {"name": "नीलम/Blue Sapphire", "sanskrit": "Neelam", "planet": "Saturn"},
        9: {"name": "मूंगा/Red Coral", "sanskrit": "Moonga", "planet": "Mars"},
    }

    # Number friendships and enmities (based on planetary relationships)
    NUMBER_RELATIONSHIPS = {
        1: {"friends": [1, 2, 3, 9], "enemies": [4, 6, 8], "neutral": [5, 7]},
        2: {"friends": [1, 2, 3], "enemies": [4, 5, 8], "neutral": [6, 7, 9]},
        3: {"friends": [1, 2, 3, 9], "enemies": [5, 6], "neutral": [4, 7, 8]},
        4: {"friends": [5, 6, 8], "enemies": [1, 2, 9], "neutral": [3, 4, 7]},
        5: {"friends": [1, 4, 6], "enemies": [2], "neutral": [3, 5, 7, 8, 9]},
        6: {"friends": [4, 5, 8], "enemies": [1, 2], "neutral": [3, 6, 7, 9]},
        7: {"friends": [1, 2, 4], "enemies": [8, 9], "neutral": [3, 5, 6, 7]},
        8: {"friends": [4, 5, 6], "enemies": [1, 2, 9], "neutral": [3, 7, 8]},
        9: {"friends": [1, 2, 3, 9], "enemies": [4, 8], "neutral": [5, 6, 7]},
    }

    # Life path descriptions for Bhagyank
    LIFE_PATH_DESCRIPTIONS = {
        1: "आपका जीवन पथ नेतृत्व और स्वतंत्रता का है। आप नई शुरुआत करने में सक्षम हैं और दूसरों को प्रेरित करते हैं। सफलता आपके लिए निश्चित है यदि आप अपने लक्ष्य पर केंद्रित रहें। / Your life path is of leadership and independence. You are capable of new beginnings and inspire others. Success is certain if you stay focused on your goals.",

        2: "आपका जीवन पथ सहयोग और संतुलन का है। आप रिश्तों में माहिर हैं और दूसरों की मदद करने में आनंद पाते हैं। धैर्य और कूटनीति से आप सफल होंगे। / Your life path is of cooperation and balance. You excel in relationships and find joy in helping others. With patience and diplomacy, you will succeed.",

        3: "आपका जीवन पथ रचनात्मकता और आनंद का है। ज्ञान और आध्यात्मिकता आपको आकर्षित करती है। शिक्षा, लेखन, या कला में सफलता मिलेगी। / Your life path is of creativity and joy. Knowledge and spirituality attract you. Success will come in education, writing, or arts.",

        4: "आपका जीवन पथ कठिन परिश्रम और स्थिरता का है। अचानक परिवर्तन आपके जीवन का हिस्सा हैं। धैर्य से आप मजबूत नींव बना सकते हैं। / Your life path is of hard work and stability. Sudden changes are part of your life. With patience, you can build a strong foundation.",

        5: "आपका जीवन पथ स्वतंत्रता और परिवर्तन का है। यात्रा और नए अनुभव आपको आकर्षित करते हैं। व्यापार और संचार में सफलता मिलेगी। / Your life path is of freedom and change. Travel and new experiences attract you. Success will come in business and communication.",

        6: "आपका जीवन पथ प्रेम और जिम्मेदारी का है। परिवार और घर आपके लिए महत्वपूर्ण हैं। कला, सौंदर्य, और सेवा में सफलता मिलेगी। / Your life path is of love and responsibility. Family and home are important to you. Success will come in arts, beauty, and service.",

        7: "आपका जीवन पथ आध्यात्मिक खोज और आत्मज्ञान का है। आप रहस्यों और गहराई में रुचि रखते हैं। अनुसंधान और आध्यात्मिकता में सफलता मिलेगी। / Your life path is of spiritual quest and self-knowledge. You are interested in mysteries and depth. Success will come in research and spirituality.",

        8: "आपका जीवन पथ शक्ति और उपलब्धि का है। भौतिक सफलता और अधिकार आपको आकर्षित करते हैं। व्यवसाय और प्रबंधन में सफलता मिलेगी। / Your life path is of power and achievement. Material success and authority attract you. Success will come in business and management.",

        9: "आपका जीवन पथ मानवता की सेवा और आध्यात्मिक पूर्णता का है। आप दूसरों के लिए जीना जानते हैं। नेतृत्व और सामाजिक कार्यों में सफलता मिलेगी। / Your life path is of humanitarian service and spiritual fulfillment. You know how to live for others. Success will come in leadership and social work.",
    }

    def __init__(self):
        """Initialize the Numerology Calculator."""
        pass

    @staticmethod
    def reduce_to_single_digit(number: int) -> int:
        """
        Reduce any number to a single digit (1-9).
        Keep reducing until single digit is obtained.

        Special cases: 11, 22, 33 are master numbers in Western numerology,
        but in Vedic numerology we reduce all to single digit.
        """
        while number > 9:
            number = sum(int(d) for d in str(number))
        return number

    def calculate_moolank(self, birth_date: Union[date, datetime]) -> int:
        """
        Calculate Moolank (Root Number / Driver Number).

        Moolank is calculated from the birth date only (not month/year).
        It represents the core personality and inner self.

        Example: Born on 28th -> 2 + 8 = 10 -> 1 + 0 = 1
        """
        if isinstance(birth_date, datetime):
            birth_date = birth_date.date()

        day = birth_date.day
        return self.reduce_to_single_digit(day)

    def calculate_bhagyank(self, birth_date: Union[date, datetime]) -> int:
        """
        Calculate Bhagyank (Destiny Number / Conductor Number).

        Bhagyank is calculated from the full date of birth (DD+MM+YYYY).
        It represents the life path and destiny.

        Example: 28-05-1990 -> 2+8+0+5+1+9+9+0 = 34 -> 3+4 = 7
        """
        if isinstance(birth_date, datetime):
            birth_date = birth_date.date()

        date_str = birth_date.strftime("%d%m%Y")
        total = sum(int(d) for d in date_str)
        return self.reduce_to_single_digit(total)

    def calculate_namank(
        self,
        name: str,
        system: NumerologySystem = NumerologySystem.CHALDEAN
    ) -> int:
        """
        Calculate Namank (Name Number).

        The name number represents how you present yourself to the world
        and the vibration of your name.

        Args:
            name: Full name (English or Hindi)
            system: Chaldean or Pythagorean system

        Returns:
            Single digit name number (1-9)
        """
        name = name.upper().strip()
        total = 0

        letter_map = (
            self.CHALDEAN_MAP if system == NumerologySystem.CHALDEAN
            else self.PYTHAGOREAN_MAP
        )

        for char in name:
            if char.isalpha():
                if char in letter_map:
                    total += letter_map[char]
                elif char in self.HINDI_LETTER_MAP:
                    total += self.HINDI_LETTER_MAP[char]

        return self.reduce_to_single_digit(total)

    def get_planet_for_number(self, number: int) -> Dict:
        """Get the ruling planet for a number."""
        number = self.reduce_to_single_digit(number)
        return self.NUMBER_PLANET_MAP.get(number, self.NUMBER_PLANET_MAP[1])

    def get_personality_traits(self, moolank: int) -> Dict:
        """Get personality traits based on Moolank."""
        return self.PERSONALITY_TRAITS.get(moolank, self.PERSONALITY_TRAITS[1])

    def get_life_path_description(self, bhagyank: int) -> str:
        """Get life path description based on Bhagyank."""
        return self.LIFE_PATH_DESCRIPTIONS.get(bhagyank, self.LIFE_PATH_DESCRIPTIONS[1])

    def get_lucky_numbers(self, moolank: int, bhagyank: int) -> List[int]:
        """
        Get lucky numbers based on Moolank and Bhagyank.

        Lucky numbers include:
        - The Moolank itself
        - The Bhagyank itself
        - Friendly numbers of Moolank
        - Compound numbers that reduce to Moolank/Bhagyank
        """
        lucky = set()
        lucky.add(moolank)
        lucky.add(bhagyank)

        # Add friendly numbers
        friends = self.NUMBER_RELATIONSHIPS.get(moolank, {}).get("friends", [])
        lucky.update(friends)

        # Add some compound lucky numbers
        for base in [moolank, bhagyank]:
            lucky.add(base + 9)  # 9 is universal
            lucky.add(base + 18)

        return sorted(list(lucky))[:7]  # Return top 7 lucky numbers

    def get_lucky_colors(self, moolank: int) -> List[str]:
        """Get lucky colors based on Moolank."""
        return self.LUCKY_COLORS.get(moolank, self.LUCKY_COLORS[1])

    def get_lucky_days(self, moolank: int) -> List[str]:
        """Get lucky days based on Moolank."""
        return self.LUCKY_DAYS.get(moolank, self.LUCKY_DAYS[1])

    def get_lucky_gemstone(self, moolank: int) -> Dict:
        """Get lucky gemstone based on Moolank."""
        return self.LUCKY_GEMSTONES.get(moolank, self.LUCKY_GEMSTONES[1])

    def get_friendly_numbers(self, moolank: int) -> List[int]:
        """Get friendly numbers for Moolank."""
        return self.NUMBER_RELATIONSHIPS.get(moolank, {}).get("friends", [1, 2, 3])

    def get_unfriendly_numbers(self, moolank: int) -> List[int]:
        """Get unfriendly/enemy numbers for Moolank."""
        return self.NUMBER_RELATIONSHIPS.get(moolank, {}).get("enemies", [])

    def analyze_name(self, name: str) -> Dict:
        """
        Analyze a name and provide detailed breakdown.

        Returns:
            Dictionary with name analysis including letter breakdown,
            vowel/consonant numbers, and recommendations.
        """
        name_upper = name.upper().strip()

        vowels = "AEIOU"
        vowel_total = 0
        consonant_total = 0
        letter_breakdown = []

        for char in name_upper:
            if char.isalpha():
                chaldean_val = self.CHALDEAN_MAP.get(char, 0)
                pythagorean_val = self.PYTHAGOREAN_MAP.get(char, 0)
                is_vowel = char in vowels

                letter_breakdown.append({
                    "letter": char,
                    "chaldean": chaldean_val,
                    "pythagorean": pythagorean_val,
                    "is_vowel": is_vowel,
                })

                if is_vowel:
                    vowel_total += chaldean_val
                else:
                    consonant_total += chaldean_val

        chaldean_total = sum(lb["chaldean"] for lb in letter_breakdown)
        pythagorean_total = sum(lb["pythagorean"] for lb in letter_breakdown)

        return {
            "name": name,
            "letter_breakdown": letter_breakdown,
            "chaldean_total": chaldean_total,
            "chaldean_reduced": self.reduce_to_single_digit(chaldean_total),
            "pythagorean_total": pythagorean_total,
            "pythagorean_reduced": self.reduce_to_single_digit(pythagorean_total),
            "soul_number": self.reduce_to_single_digit(vowel_total),  # From vowels
            "personality_number": self.reduce_to_single_digit(consonant_total),  # From consonants
            "soul_number_desc": "आत्मा अंक / Soul Number - आपकी अंतरात्मा की इच्छाएं / Inner desires",
            "personality_number_desc": "व्यक्तित्व अंक / Personality Number - बाहरी व्यक्तित्व / Outer personality",
        }

    def suggest_name_corrections(
        self,
        name: str,
        target_number: Optional[int] = None,
        birth_date: Optional[Union[date, datetime]] = None
    ) -> List[NameCorrectionSuggestion]:
        """
        Suggest name corrections for better numerological vibration.

        If target_number is not specified, it will suggest corrections
        to make the name number compatible with Moolank/Bhagyank.

        Args:
            name: Current name
            target_number: Desired name number (1-9)
            birth_date: Birth date for calculating compatible number

        Returns:
            List of name correction suggestions
        """
        suggestions = []
        current_namank = self.calculate_namank(name, NumerologySystem.CHALDEAN)

        # Determine target number if not specified
        if target_number is None and birth_date:
            moolank = self.calculate_moolank(birth_date)
            bhagyank = self.calculate_bhagyank(birth_date)
            # Target should be friendly to both Moolank and Bhagyank
            friends = set(self.get_friendly_numbers(moolank))
            friends.update(self.get_friendly_numbers(bhagyank))
            friends.add(moolank)
            friends.add(bhagyank)
            target_options = list(friends)
        elif target_number:
            target_options = [target_number]
        else:
            target_options = [1, 5, 6]  # Generally auspicious numbers

        name_upper = name.upper()

        for target in target_options:
            if target == current_namank:
                continue

            # Strategy 1: Add a letter at the end
            for letter, value in self.CHALDEAN_MAP.items():
                new_name = name + letter.lower()
                new_namank = self.calculate_namank(new_name, NumerologySystem.CHALDEAN)
                if new_namank == target:
                    planet = self.get_planet_for_number(target)
                    suggestions.append(NameCorrectionSuggestion(
                        original_name=name,
                        suggested_name=new_name.title(),
                        original_number=current_namank,
                        new_number=target,
                        change_description=f"नाम के अंत में '{letter}' जोड़ें / Add '{letter}' at the end",
                        benefit=f"यह {planet['hindi']} ({planet['planet']}) की शुभ ऊर्जा लाएगा। / This will bring auspicious energy of {planet['hindi']} ({planet['planet']}).",
                    ))

            # Strategy 2: Add letter at beginning
            for letter, value in self.CHALDEAN_MAP.items():
                new_name = letter.lower() + name
                new_namank = self.calculate_namank(new_name, NumerologySystem.CHALDEAN)
                if new_namank == target and letter.lower() != name[0].lower():
                    planet = self.get_planet_for_number(target)
                    suggestions.append(NameCorrectionSuggestion(
                        original_name=name,
                        suggested_name=new_name.title(),
                        original_number=current_namank,
                        new_number=target,
                        change_description=f"नाम की शुरुआत में '{letter}' जोड़ें / Add '{letter}' at the beginning",
                        benefit=f"यह {planet['hindi']} ({planet['planet']}) की शुभ ऊर्जा लाएगा। / This will bring auspicious energy of {planet['hindi']} ({planet['planet']}).",
                    ))

            # Strategy 3: Double a letter
            for i, char in enumerate(name):
                if char.isalpha():
                    new_name = name[:i] + char + name[i:]
                    new_namank = self.calculate_namank(new_name, NumerologySystem.CHALDEAN)
                    if new_namank == target:
                        planet = self.get_planet_for_number(target)
                        suggestions.append(NameCorrectionSuggestion(
                            original_name=name,
                            suggested_name=new_name.title(),
                            original_number=current_namank,
                            new_number=target,
                            change_description=f"'{char}' अक्षर को दोगुना करें / Double the letter '{char}'",
                            benefit=f"यह {planet['hindi']} ({planet['planet']}) की शुभ ऊर्जा लाएगा। / This will bring auspicious energy of {planet['hindi']} ({planet['planet']}).",
                        ))

        # Return top 5 unique suggestions
        seen = set()
        unique_suggestions = []
        for s in suggestions:
            if s.suggested_name not in seen:
                seen.add(s.suggested_name)
                unique_suggestions.append(s)

        return unique_suggestions[:5]

    def calculate_compatibility(
        self,
        person1_name: str,
        person1_dob: Union[date, datetime],
        person2_name: str,
        person2_dob: Union[date, datetime]
    ) -> CompatibilityResult:
        """
        Calculate numerological compatibility between two people.

        Based on:
        - Moolank compatibility
        - Bhagyank compatibility
        - Name number compatibility
        """
        p1_moolank = self.calculate_moolank(person1_dob)
        p1_bhagyank = self.calculate_bhagyank(person1_dob)
        p2_moolank = self.calculate_moolank(person2_dob)
        p2_bhagyank = self.calculate_bhagyank(person2_dob)

        score = 0
        strengths = []
        challenges = []

        # Check Moolank compatibility (35 points)
        p1_friends = set(self.NUMBER_RELATIONSHIPS.get(p1_moolank, {}).get("friends", []))
        p1_enemies = set(self.NUMBER_RELATIONSHIPS.get(p1_moolank, {}).get("enemies", []))

        if p2_moolank in p1_friends or p1_moolank == p2_moolank:
            score += 35
            strengths.append(f"मूलांक अनुकूलता उत्तम ({p1_moolank} और {p2_moolank}) / Excellent Moolank compatibility ({p1_moolank} and {p2_moolank})")
        elif p2_moolank in p1_enemies:
            score += 10
            challenges.append(f"मूलांक में कुछ तनाव ({p1_moolank} और {p2_moolank}) / Some tension in Moolank ({p1_moolank} and {p2_moolank})")
        else:
            score += 20
            strengths.append(f"मूलांक में सामान्य अनुकूलता / Average Moolank compatibility")

        # Check Bhagyank compatibility (35 points)
        p1_bhag_friends = set(self.NUMBER_RELATIONSHIPS.get(p1_bhagyank, {}).get("friends", []))
        p1_bhag_enemies = set(self.NUMBER_RELATIONSHIPS.get(p1_bhagyank, {}).get("enemies", []))

        if p2_bhagyank in p1_bhag_friends or p1_bhagyank == p2_bhagyank:
            score += 35
            strengths.append(f"भाग्यांक अनुकूलता उत्तम ({p1_bhagyank} और {p2_bhagyank}) / Excellent Bhagyank compatibility ({p1_bhagyank} and {p2_bhagyank})")
        elif p2_bhagyank in p1_bhag_enemies:
            score += 10
            challenges.append(f"भाग्यांक में कुछ बाधाएं ({p1_bhagyank} और {p2_bhagyank}) / Some obstacles in Bhagyank ({p1_bhagyank} and {p2_bhagyank})")
        else:
            score += 20
            strengths.append(f"भाग्यांक में सामान्य अनुकूलता / Average Bhagyank compatibility")

        # Check Name Number compatibility (30 points)
        p1_namank = self.calculate_namank(person1_name, NumerologySystem.CHALDEAN)
        p2_namank = self.calculate_namank(person2_name, NumerologySystem.CHALDEAN)

        p1_name_friends = set(self.NUMBER_RELATIONSHIPS.get(p1_namank, {}).get("friends", []))

        if p2_namank in p1_name_friends or p1_namank == p2_namank:
            score += 30
            strengths.append(f"नाम अंक अनुकूलता उत्तम ({p1_namank} और {p2_namank}) / Excellent Name Number compatibility ({p1_namank} and {p2_namank})")
        else:
            score += 15

        # Determine compatibility level
        if score >= 80:
            level = "उत्तम / Excellent"
        elif score >= 60:
            level = "अच्छा / Good"
        elif score >= 40:
            level = "औसत / Average"
        else:
            level = "कम / Low"

        # Generate remedies if needed
        remedies = []
        if score < 70:
            if p2_moolank in p1_enemies:
                planet = self.get_planet_for_number(p1_moolank)
                remedies.append(f"{planet['hindi']} के दिन {planet['planet']} का उपाय करें / Perform remedy for {planet['planet']} on {self.LUCKY_DAYS[p1_moolank][0]}")

            remedies.append("दोनों व्यक्तियों को अपने-अपने शुभ रंग पहनने चाहिए / Both should wear their lucky colors")
            remedies.append("मिलकर मंत्र जाप करें - 'ॐ गं गणपतये नमः' / Chant together - 'Om Gam Ganapataye Namah'")

        return CompatibilityResult(
            person1_name=person1_name,
            person2_name=person2_name,
            person1_moolank=p1_moolank,
            person2_moolank=p2_moolank,
            person1_bhagyank=p1_bhagyank,
            person2_bhagyank=p2_bhagyank,
            compatibility_score=score,
            compatibility_level=level,
            strengths=strengths,
            challenges=challenges,
            remedies=remedies,
        )

    def analyze_business_name(self, business_name: str, owner_dob: Union[date, datetime]) -> Dict:
        """
        Analyze a business name for numerological compatibility with the owner.

        Args:
            business_name: Name of the business
            owner_dob: Owner's date of birth

        Returns:
            Dictionary with business name analysis and recommendations
        """
        owner_moolank = self.calculate_moolank(owner_dob)
        owner_bhagyank = self.calculate_bhagyank(owner_dob)

        business_namank_chaldean = self.calculate_namank(business_name, NumerologySystem.CHALDEAN)
        business_namank_pythagorean = self.calculate_namank(business_name, NumerologySystem.PYTHAGOREAN)

        # Check compatibility
        owner_friends = set(self.NUMBER_RELATIONSHIPS.get(owner_moolank, {}).get("friends", []))
        owner_friends.update(self.NUMBER_RELATIONSHIPS.get(owner_bhagyank, {}).get("friends", []))
        owner_friends.add(owner_moolank)
        owner_friends.add(owner_bhagyank)

        is_compatible = business_namank_chaldean in owner_friends

        # Business success numbers
        business_success_numbers = [1, 3, 5, 6, 9]
        is_auspicious = business_namank_chaldean in business_success_numbers

        business_planet = self.get_planet_for_number(business_namank_chaldean)

        recommendations = []
        if not is_compatible:
            recommendations.append("व्यापार नाम का अंक मालिक के अंकों से मेल नहीं खाता। नाम में बदलाव विचारणीय है।")
            recommendations.append("Business name number doesn't match with owner's numbers. Consider name modification.")

            # Suggest better numbers
            better_numbers = list(owner_friends.intersection(set(business_success_numbers)))
            if better_numbers:
                recommendations.append(f"शुभ अंक: {', '.join(map(str, better_numbers))} / Auspicious numbers: {', '.join(map(str, better_numbers))}")

        if not is_auspicious:
            recommendations.append(f"व्यापार के लिए अंक {business_namank_chaldean} सामान्य माना जाता है।")
            recommendations.append(f"Number {business_namank_chaldean} is considered average for business.")

        return {
            "business_name": business_name,
            "namank_chaldean": business_namank_chaldean,
            "namank_pythagorean": business_namank_pythagorean,
            "ruling_planet": business_planet,
            "owner_moolank": owner_moolank,
            "owner_bhagyank": owner_bhagyank,
            "is_compatible": is_compatible,
            "is_auspicious": is_auspicious,
            "compatibility_level": "उत्तम / Excellent" if is_compatible and is_auspicious else "अच्छा / Good" if is_compatible or is_auspicious else "सामान्य / Average",
            "recommendations": recommendations,
            "lucky_days_for_business": self.LUCKY_DAYS.get(business_namank_chaldean, []),
            "lucky_colors_for_business": self.LUCKY_COLORS.get(business_namank_chaldean, []),
        }

    def get_complete_analysis(
        self,
        name: str,
        birth_date: Union[date, datetime, str]
    ) -> NumerologyResult:
        """
        Get complete numerology analysis for a person.

        Args:
            name: Person's full name
            birth_date: Date of birth (date object or 'YYYY-MM-DD' string)

        Returns:
            Complete NumerologyResult with all analysis
        """
        # Parse birth date if string
        if isinstance(birth_date, str):
            birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
        elif isinstance(birth_date, datetime):
            birth_date = birth_date.date()

        # Calculate core numbers
        moolank = self.calculate_moolank(birth_date)
        bhagyank = self.calculate_bhagyank(birth_date)
        namank_chaldean = self.calculate_namank(name, NumerologySystem.CHALDEAN)
        namank_pythagorean = self.calculate_namank(name, NumerologySystem.PYTHAGOREAN)

        # Get planet information
        moolank_planet = self.get_planet_for_number(moolank)
        bhagyank_planet = self.get_planet_for_number(bhagyank)
        namank_planet_chaldean = self.get_planet_for_number(namank_chaldean)
        namank_planet_pythagorean = self.get_planet_for_number(namank_pythagorean)

        # Get personality and life path
        personality = self.get_personality_traits(moolank)
        life_path = self.get_life_path_description(bhagyank)

        # Get lucky elements
        lucky_numbers = self.get_lucky_numbers(moolank, bhagyank)
        lucky_colors = self.get_lucky_colors(moolank)
        lucky_days = self.get_lucky_days(moolank)
        lucky_gemstone = self.get_lucky_gemstone(moolank)

        # Get number relationships
        friendly_numbers = self.get_friendly_numbers(moolank)
        unfriendly_numbers = self.get_unfriendly_numbers(moolank)

        # Analyze name
        name_analysis = self.analyze_name(name)

        # Compatibility numbers (numbers that work well for partnerships)
        compatibility_numbers = list(set(friendly_numbers + self.get_friendly_numbers(bhagyank)))

        return NumerologyResult(
            name=name,
            birth_date=birth_date,
            moolank=moolank,
            bhagyank=bhagyank,
            namank_chaldean=namank_chaldean,
            namank_pythagorean=namank_pythagorean,
            moolank_planet=f"{moolank_planet['hindi']} ({moolank_planet['planet']})",
            bhagyank_planet=f"{bhagyank_planet['hindi']} ({bhagyank_planet['planet']})",
            namank_planet_chaldean=f"{namank_planet_chaldean['hindi']} ({namank_planet_chaldean['planet']})",
            namank_planet_pythagorean=f"{namank_planet_pythagorean['hindi']} ({namank_planet_pythagorean['planet']})",
            personality_traits=personality["traits"],
            life_path_description=life_path,
            lucky_numbers=lucky_numbers,
            lucky_colors=lucky_colors,
            lucky_days=lucky_days,
            lucky_gemstone=f"{lucky_gemstone['name']} - {lucky_gemstone['planet']}",
            friendly_numbers=friendly_numbers,
            unfriendly_numbers=unfriendly_numbers,
            name_analysis=name_analysis,
            compatibility_numbers=compatibility_numbers,
        )

    def get_analysis_as_dict(
        self,
        name: str,
        birth_date: Union[date, datetime, str]
    ) -> Dict:
        """
        Get complete numerology analysis as a dictionary (for API responses).
        """
        result = self.get_complete_analysis(name, birth_date)

        # Get additional details
        moolank_personality = self.get_personality_traits(result.moolank)
        gemstone_details = self.get_lucky_gemstone(result.moolank)

        return {
            "name": result.name,
            "birth_date": result.birth_date.isoformat(),
            "core_numbers": {
                "moolank": {
                    "value": result.moolank,
                    "planet": result.moolank_planet,
                    "description": "मूलांक / Root Number - जन्म तिथि से / From birth date",
                },
                "bhagyank": {
                    "value": result.bhagyank,
                    "planet": result.bhagyank_planet,
                    "description": "भाग्यांक / Destiny Number - पूर्ण जन्मतिथि से / From full DOB",
                },
                "namank_chaldean": {
                    "value": result.namank_chaldean,
                    "planet": result.namank_planet_chaldean,
                    "description": "नामांक (कैल्डियन) / Name Number (Chaldean)",
                },
                "namank_pythagorean": {
                    "value": result.namank_pythagorean,
                    "planet": result.namank_planet_pythagorean,
                    "description": "नामांक (पाइथागोरियन) / Name Number (Pythagorean)",
                },
            },
            "personality": {
                "traits": result.personality_traits,
                "description": moolank_personality["description"],
            },
            "life_path": {
                "description": result.life_path_description,
            },
            "lucky_elements": {
                "numbers": result.lucky_numbers,
                "colors": result.lucky_colors,
                "days": result.lucky_days,
                "gemstone": {
                    "name": gemstone_details["name"],
                    "sanskrit": gemstone_details["sanskrit"],
                    "planet": gemstone_details["planet"],
                },
            },
            "number_relationships": {
                "friendly_numbers": result.friendly_numbers,
                "unfriendly_numbers": result.unfriendly_numbers,
                "compatibility_numbers": result.compatibility_numbers,
            },
            "name_analysis": result.name_analysis,
        }


# Convenience functions for direct use
def calculate_numerology(name: str, birth_date: Union[date, datetime, str]) -> Dict:
    """
    Calculate complete numerology analysis.

    Args:
        name: Person's full name
        birth_date: Date of birth

    Returns:
        Dictionary with complete analysis
    """
    calculator = NumerologyCalculator()
    return calculator.get_analysis_as_dict(name, birth_date)


def get_compatibility(
    person1_name: str,
    person1_dob: Union[date, datetime, str],
    person2_name: str,
    person2_dob: Union[date, datetime, str]
) -> Dict:
    """
    Calculate compatibility between two people.

    Returns:
        Dictionary with compatibility analysis
    """
    calculator = NumerologyCalculator()

    # Parse dates if strings
    if isinstance(person1_dob, str):
        person1_dob = datetime.strptime(person1_dob, "%Y-%m-%d").date()
    if isinstance(person2_dob, str):
        person2_dob = datetime.strptime(person2_dob, "%Y-%m-%d").date()

    result = calculator.calculate_compatibility(
        person1_name, person1_dob,
        person2_name, person2_dob
    )

    return {
        "person1": {
            "name": result.person1_name,
            "moolank": result.person1_moolank,
            "bhagyank": result.person1_bhagyank,
        },
        "person2": {
            "name": result.person2_name,
            "moolank": result.person2_moolank,
            "bhagyank": result.person2_bhagyank,
        },
        "compatibility_score": result.compatibility_score,
        "compatibility_level": result.compatibility_level,
        "strengths": result.strengths,
        "challenges": result.challenges,
        "remedies": result.remedies,
    }


def suggest_name_correction(
    name: str,
    birth_date: Union[date, datetime, str],
    target_number: Optional[int] = None
) -> List[Dict]:
    """
    Suggest name corrections for better numerology.

    Returns:
        List of suggestions
    """
    calculator = NumerologyCalculator()

    if isinstance(birth_date, str):
        birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()

    suggestions = calculator.suggest_name_corrections(name, target_number, birth_date)

    return [
        {
            "original_name": s.original_name,
            "suggested_name": s.suggested_name,
            "original_number": s.original_number,
            "new_number": s.new_number,
            "change_description": s.change_description,
            "benefit": s.benefit,
        }
        for s in suggestions
    ]


def analyze_business_name(
    business_name: str,
    owner_dob: Union[date, datetime, str]
) -> Dict:
    """
    Analyze business name compatibility with owner.

    Returns:
        Dictionary with business name analysis
    """
    calculator = NumerologyCalculator()

    if isinstance(owner_dob, str):
        owner_dob = datetime.strptime(owner_dob, "%Y-%m-%d").date()

    return calculator.analyze_business_name(business_name, owner_dob)
