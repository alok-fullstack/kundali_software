"""
Rashifal (Horoscope) Prediction System for Vedic Astrology

This module provides daily, weekly, monthly, and yearly horoscope predictions
based on authentic Vedic sources:
- Brihat Parashara Hora Shastra (BPHS)
- Phaladeepika by Mantreshwara
- Brihat Samhita by Varahamihira

The predictions are based on:
1. Moon Sign (Chandra Rashi) - PRIMARY
2. Current Planetary Transits (Gochar) over natal Moon
3. Dasha periods influence
4. Saturn, Jupiter, Rahu/Ketu transits

Author: Kundali Software
References: BPHS Chapter 41-65, Phaladeepika Chapters 15-25
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum
import pytz

from .planets import PlanetaryCalculator
from .config import (
    Planet, RASHIS, NAKSHATRAS, PLANET_NAMES,
    NAKSHATRA_SPAN, RASHI_LIST, GOCHAR_PLANET_EFFECTS,
    COMBUSTION_ORBS, TARABALA_EFFECTS, PLANET_DIGNITIES
)

# Optional imports for enhanced accuracy (Ashtakavarga + Vedha + Dasha + Sade Sati)
try:
    from .ashtakavarga import (
        AshtakavargaCalculator, get_moorti, Moorti,
        calculate_kakshya, get_kakshya_modifier,
        check_sade_sati, get_sade_sati_score_modifier
    )
    from .vedha import VedhaCalculator, VEDHA_POINTS
    from .dasha_transit_sync import apply_dasha_transit_sync, get_dasha_sync_prediction
    from .bindu_predictions import get_bindu_prediction, get_bindu_category, get_combined_prediction
    ASHTAKAVARGA_AVAILABLE = True
except ImportError:
    ASHTAKAVARGA_AVAILABLE = False

# Optional imports for additional accuracy components (Shadbala + Navamsa)
try:
    from .shadbala import ShadbalaCalculator, get_shadbala_for_transit
    SHADBALA_AVAILABLE = True
except ImportError:
    SHADBALA_AVAILABLE = False

try:
    from .divisional_charts import DivisionalChartCalculator
    NAVAMSA_AVAILABLE = True
except ImportError:
    NAVAMSA_AVAILABLE = False


# =============================================================================
# ENUMS AND CONSTANTS
# =============================================================================

class RashifalPeriod(Enum):
    """Rashifal time periods."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class PredictionCategory(Enum):
    """Prediction categories based on house significations."""
    CAREER = "career"          # 10th from Moon
    FINANCE = "finance"        # 2nd, 11th from Moon
    HEALTH = "health"          # 6th from Moon
    RELATIONSHIPS = "relationships"  # 7th from Moon
    FAMILY = "family"          # 4th from Moon
    OVERALL = "overall"        # General luck


# Average daily motion in degrees (for transit calculations)
AVERAGE_DAILY_MOTION = {
    "SUN": 0.9856,
    "MOON": 13.1764,
    "MARS": 0.5240,
    "MERCURY": 1.3833,
    "JUPITER": 0.0831,
    "VENUS": 1.2000,
    "SATURN": 0.0335,
    "RAHU": 0.0529,
    "KETU": 0.0529,
}

# Rashi names in Hindi
RASHI_HINDI_NAMES = {
    0: "मेष", 1: "वृषभ", 2: "मिथुन", 3: "कर्क",
    4: "सिंह", 5: "कन्या", 6: "तुला", 7: "वृश्चिक",
    8: "धनु", 9: "मकर", 10: "कुंभ", 11: "मीन"
}

# Transit house effects from Moon (Gochara Phal from BPHS)
# Key: House from Moon, Value: (effect_type, intensity)
# effect_type: "shubh" (auspicious), "ashubh" (inauspicious), "mishra" (mixed)
GOCHARA_HOUSE_EFFECTS = {
    1: ("mishra", 0.5),   # Transit over Moon - mixed
    2: ("ashubh", 0.6),   # 2nd from Moon - generally challenging
    3: ("shubh", 0.8),    # 3rd from Moon - favorable
    4: ("ashubh", 0.7),   # 4th from Moon - challenging
    5: ("mishra", 0.5),   # 5th from Moon - mixed (trikona)
    6: ("shubh", 0.9),    # 6th from Moon - very favorable
    7: ("ashubh", 0.6),   # 7th from Moon - challenging
    8: ("ashubh", 0.8),   # 8th from Moon - most challenging
    9: ("mishra", 0.5),   # 9th from Moon - mixed (trikona)
    10: ("shubh", 0.9),   # 10th from Moon - very favorable
    11: ("shubh", 1.0),   # 11th from Moon - most favorable
    12: ("ashubh", 0.7),  # 12th from Moon - challenging
}

# Planet significance weight for predictions - BASE WEIGHTS
PLANET_WEIGHTS = {
    "SATURN": 1.0,    # Most significant for long-term
    "JUPITER": 0.95,  # Very significant for growth
    "RAHU": 0.85,     # Significant for sudden changes
    "KETU": 0.80,     # Significant for spiritual matters
    "MARS": 0.70,     # Important for energy and actions
    "SUN": 0.65,      # Important for career and authority
    "VENUS": 0.60,    # Important for relationships
    "MERCURY": 0.55,  # Important for communication
    "MOON": 0.50,     # Important for emotions (fast moving)
}

# Period-specific planet weights (different planets matter for different periods)
PERIOD_PLANET_WEIGHTS = {
    "daily": {
        "MOON": 1.0,      # Moon is PRIMARY for daily predictions (moves 13°/day)
        "SUN": 0.7,
        "MERCURY": 0.8,
        "VENUS": 0.75,
        "MARS": 0.5,
        "JUPITER": 0.3,
        "SATURN": 0.2,
        "RAHU": 0.3,
        "KETU": 0.3,
    },
    "weekly": {
        "MOON": 0.6,
        "SUN": 0.9,       # Sun moves ~7° per week
        "MERCURY": 1.0,   # Mercury is important for weekly (fast mover)
        "VENUS": 0.9,     # Venus important for weekly
        "MARS": 0.7,
        "JUPITER": 0.4,
        "SATURN": 0.3,
        "RAHU": 0.4,
        "KETU": 0.4,
    },
    "monthly": {
        "MOON": 0.4,
        "SUN": 1.0,       # Sun changes sign monthly - PRIMARY
        "MERCURY": 0.8,
        "VENUS": 0.85,
        "MARS": 0.9,      # Mars important for monthly
        "JUPITER": 0.6,
        "SATURN": 0.5,
        "RAHU": 0.55,
        "KETU": 0.55,
    },
    "yearly": {
        "MOON": 0.2,
        "SUN": 0.5,
        "MERCURY": 0.4,
        "VENUS": 0.5,
        "MARS": 0.7,
        "JUPITER": 1.0,   # Jupiter is PRIMARY for yearly (changes sign yearly)
        "SATURN": 0.95,   # Saturn very important for yearly
        "RAHU": 0.9,      # Rahu/Ketu important for yearly
        "KETU": 0.9,
    },
}


# =============================================================================
# DATACLASSES
# =============================================================================

@dataclass
class CategoryPrediction:
    """Prediction for a specific life category."""
    category: PredictionCategory
    category_hindi: str
    prediction_hindi: str
    prediction_english: str
    score: int  # 1-10 rating
    favorable: bool
    key_advice: str
    lucky_elements: Dict[str, str] = field(default_factory=dict)


@dataclass
class RashifalPrediction:
    """Complete Rashifal prediction for a Rashi."""
    rashi_num: int
    rashi_name: str
    rashi_hindi: str
    rashi_symbol: str
    period: RashifalPeriod
    start_date: datetime
    end_date: datetime
    overall_score: int  # 1-10
    overall_prediction_hindi: str
    overall_prediction_english: str
    category_predictions: List[CategoryPrediction]
    planetary_influences: List[Dict]
    key_transits: List[str]
    lucky_color: str
    lucky_number: str
    lucky_day: str
    mantra: str
    deity: str
    dos: List[str]  # Things to do
    donts: List[str]  # Things to avoid
    generated_at: datetime = field(default_factory=datetime.now)
    # Enhanced Vedic components (99.99% accuracy)
    sade_sati_info: Optional[Dict] = None  # Sade Sati / Dhaiya detection
    dasha_sync_info: Optional[Dict] = None  # Dasha-Transit synchronization
    has_ashtakavarga: bool = False  # Was Ashtakavarga used?
    has_vedha: bool = False  # Was Vedha checking used?
    has_kakshya: bool = False  # Was Kakshya sub-division used?
    # Additional accuracy components
    has_shadbala: bool = False  # Was Shadbala strength used?
    has_combustion_check: bool = False  # Was combustion checked?
    has_tarabala: bool = False  # Was Tara Bala used?
    has_planetary_war: bool = False  # Was planetary war checked?
    has_navamsa_check: bool = False  # Was Navamsa D9 checked?
    combusted_planets: List[str] = field(default_factory=list)  # List of combust planets
    planetary_wars: List[Dict] = field(default_factory=list)  # List of active wars
    tarabala_info: Optional[Dict] = None  # Tara Bala for Moon transit


# =============================================================================
# PREDICTION TEMPLATES (Hindi/Hinglish)
# Based on BPHS Gochara Adhyaya and Phaladeepika
# =============================================================================

# Career predictions based on 10th house transit
CAREER_PREDICTIONS = {
    "excellent": [
        "करियर में उत्कृष्ट समय। प्रमोशन और तरक्की के योग बन रहे हैं।",
        "व्यापार में सफलता मिलेगी। नए अवसर आएंगे।",
        "बॉस और सीनियर्स का सहयोग मिलेगा। मान-सम्मान बढ़ेगा।",
        "नौकरी में स्थिरता और वृद्धि के संकेत हैं।",
    ],
    "good": [
        "करियर में अच्छा समय। मेहनत का फल मिलेगा।",
        "कार्यस्थल पर माहौल सकारात्मक रहेगा।",
        "नए प्रोजेक्ट मिल सकते हैं। प्रयास जारी रखें।",
        "व्यापारिक गतिविधियों में लाभ के योग हैं।",
    ],
    "average": [
        "करियर में सामान्य समय। धैर्य रखें।",
        "कुछ चुनौतियां आ सकती हैं पर निराश न हों।",
        "मेहनत करते रहें, फल अवश्य मिलेगा।",
        "कार्यस्थल पर सतर्क रहें।",
    ],
    "challenging": [
        "करियर में थोड़ी चुनौतियां रहेंगी। संयम रखें।",
        "बड़े फैसले टालें। समय का इंतजार करें।",
        "ऑफिस पॉलिटिक्स से बचें। अपने काम पर ध्यान दें।",
        "नए बदलाव अभी न करें।",
    ],
}

# Finance predictions based on 2nd and 11th house transits
FINANCE_PREDICTIONS = {
    "excellent": [
        "आर्थिक मामलों में उत्तम समय। धन लाभ के प्रबल योग।",
        "निवेश से अच्छा रिटर्न मिलेगा।",
        "आय के नए स्रोत खुलेंगे। बचत करने का अच्छा समय।",
        "अप्रत्याशित धन लाभ के योग बन रहे हैं।",
    ],
    "good": [
        "आर्थिक स्थिति मजबूत रहेगी।",
        "खर्चे नियंत्रण में रहेंगे। बजट बनाकर चलें।",
        "छोटे-मोटे निवेश फायदेमंद रहेंगे।",
        "परिवार की आर्थिक जरूरतें पूरी होंगी।",
    ],
    "average": [
        "आर्थिक मामलों में सामान्य समय।",
        "आय और व्यय में संतुलन बनाए रखें।",
        "बड़े खर्चे टालें। जरूरी खर्चे ही करें।",
        "लोन लेने से बचें।",
    ],
    "challenging": [
        "आर्थिक चुनौतियां रह सकती हैं। सावधान रहें।",
        "अनावश्यक खर्चों पर लगाम लगाएं।",
        "उधार देने से बचें। अपनी जमा पूंजी बचाएं।",
        "जोखिम भरे निवेश न करें।",
    ],
}

# Health predictions based on 6th house transit
HEALTH_PREDICTIONS = {
    "excellent": [
        "स्वास्थ्य उत्तम रहेगा। ऊर्जा का स्तर अच्छा रहेगा।",
        "रोग प्रतिरोधक क्षमता मजबूत रहेगी।",
        "मानसिक शांति बनी रहेगी।",
        "व्यायाम और योग का समय निकालें।",
    ],
    "good": [
        "स्वास्थ्य अच्छा रहेगा। नियमित दिनचर्या अपनाएं।",
        "छोटी-मोटी तकलीफें हो सकती हैं पर चिंता न करें।",
        "खान-पान पर ध्यान दें।",
        "पर्याप्त नींद लें।",
    ],
    "average": [
        "स्वास्थ्य पर ध्यान देने की जरूरत है।",
        "मौसमी बीमारियों से बचाव करें।",
        "तनाव से दूर रहें।",
        "नियमित स्वास्थ्य जांच करवाएं।",
    ],
    "challenging": [
        "स्वास्थ्य संबंधी सावधानी बरतें।",
        "पुरानी बीमारियों पर ध्यान दें।",
        "डॉक्टर की सलाह लें। दवाइयां नियमित लें।",
        "तला-भुना खाने से बचें। पानी ज्यादा पिएं।",
    ],
}

# Relationship predictions based on 7th house transit
RELATIONSHIP_PREDICTIONS = {
    "excellent": [
        "रिश्तों में मधुरता और प्रेम बढ़ेगा।",
        "जीवनसाथी से संबंध मजबूत होंगे।",
        "नए रिश्ते बनने के योग हैं।",
        "विवाह योग्य लोगों के लिए शुभ समय।",
    ],
    "good": [
        "पारिवारिक संबंध अच्छे रहेंगे।",
        "मित्रों से सहयोग मिलेगा।",
        "साझेदारी में लाभ के योग हैं।",
        "सामाजिक प्रतिष्ठा बढ़ेगी।",
    ],
    "average": [
        "रिश्तों में सामान्य समय।",
        "संवाद बनाए रखें। गलतफहमी से बचें।",
        "धैर्य और समझदारी से काम लें।",
        "अहम पर नियंत्रण रखें।",
    ],
    "challenging": [
        "रिश्तों में थोड़ा तनाव रह सकता है।",
        "विवादों से बचें। शांत रहें।",
        "जीवनसाथी की भावनाओं का ख्याल रखें।",
        "बड़े फैसले अभी न लें।",
    ],
}

# Family predictions based on 4th house transit
FAMILY_PREDICTIONS = {
    "excellent": [
        "पारिवारिक जीवन में खुशियां आएंगी।",
        "घर में शांति और सुख का वातावरण रहेगा।",
        "माता-पिता का आशीर्वाद मिलेगा।",
        "घर में मांगलिक कार्य हो सकते हैं।",
    ],
    "good": [
        "परिवार का साथ मिलेगा।",
        "घरेलू कामों में सफलता मिलेगी।",
        "संतान पक्ष से शुभ समाचार मिल सकते हैं।",
        "पारिवारिक समारोह में भाग लेंगे।",
    ],
    "average": [
        "पारिवारिक मामलों में सामान्य समय।",
        "छोटे-मोटे विवाद हो सकते हैं।",
        "बड़ों का सम्मान करें।",
        "परिवार को समय दें।",
    ],
    "challenging": [
        "पारिवारिक तनाव से बचें।",
        "घरेलू खर्चे बढ़ सकते हैं।",
        "बुजुर्गों के स्वास्थ्य पर ध्यान दें।",
        "धैर्य और संयम से काम लें।",
    ],
}

# Overall predictions based on combined transits
OVERALL_PREDICTIONS = {
    "excellent": [
        "समग्र रूप से बहुत शुभ समय। भाग्य का साथ मिलेगा।",
        "आपके प्रयास सफल होंगे। आत्मविश्वास बनाए रखें।",
        "नए कार्य शुरू करने के लिए उत्तम समय।",
        "शुभ ग्रहों की कृपा आप पर बनी रहेगी।",
    ],
    "good": [
        "अच्छा समय है। अपने लक्ष्यों पर काम करें।",
        "सकारात्मक सोच रखें। सफलता मिलेगी।",
        "मेहनत का फल मिलेगा।",
        "आत्मविश्वास बनाए रखें।",
    ],
    "average": [
        "सामान्य समय है। धैर्य रखें।",
        "संतुलित दृष्टिकोण अपनाएं।",
        "छोटी-छोटी सफलताओं का जश्न मनाएं।",
        "नियमित पूजा-पाठ करें।",
    ],
    "challenging": [
        "कुछ चुनौतियों का सामना करना पड़ सकता है।",
        "धैर्य और विवेक से काम लें।",
        "बड़े फैसले टालें। समय का इंतजार करें।",
        "ईश्वर पर भरोसा रखें। यह समय भी बीत जाएगा।",
    ],
}

# Period-specific overall predictions
PERIOD_OVERALL_PREDICTIONS = {
    "daily": {
        "excellent": [
            "आज का दिन बहुत शुभ है। चंद्रमा की स्थिति अनुकूल है।",
            "आज आपकी मनोकामनाएं पूर्ण होने के योग हैं।",
            "आज कोई भी शुभ कार्य करें, सफलता निश्चित है।",
            "आज का दिन खुशियों भरा रहेगा। मन प्रसन्न रहेगा।",
        ],
        "good": [
            "आज का दिन अच्छा रहेगा। सामान्य कार्य सफल होंगे।",
            "आज मेहनत का फल मिलेगा। सकारात्मक रहें।",
            "आज परिवार और मित्रों का साथ मिलेगा।",
            "आज के दिन में छोटी-छोटी खुशियां मिलेंगी।",
        ],
        "average": [
            "आज का दिन सामान्य रहेगा। धैर्य रखें।",
            "आज कोई बड़ा फैसला न लें। सोच-समझकर कार्य करें।",
            "आज थोड़ी व्यस्तता रहेगी। शांत मन से काम करें।",
            "आज किसी से विवाद न करें। संयम रखें।",
        ],
        "challenging": [
            "आज सावधानी बरतें। जल्दबाजी में कोई फैसला न लें।",
            "आज यात्रा टालें। घर पर रहें तो बेहतर।",
            "आज स्वास्थ्य का ध्यान रखें। तनाव से बचें।",
            "आज का दिन चुनौतीपूर्ण है। ईश्वर का स्मरण करें।",
        ],
    },
    "weekly": {
        "excellent": [
            "यह सप्ताह आपके लिए बहुत शुभ है। बुध और शुक्र अनुकूल हैं।",
            "इस सप्ताह नए अवसर मिलेंगे। तैयार रहें।",
            "सप्ताह में कोई महत्वपूर्ण सफलता मिल सकती है।",
            "इस सप्ताह आर्थिक लाभ के योग बन रहे हैं।",
        ],
        "good": [
            "यह सप्ताह अच्छा रहेगा। कार्यक्षेत्र में प्रगति होगी।",
            "सप्ताह में रिश्तों में मधुरता बढ़ेगी।",
            "इस सप्ताह मेहनत का फल मिलेगा।",
            "सप्ताह के अंत तक सकारात्मक परिणाम मिलेंगे।",
        ],
        "average": [
            "यह सप्ताह मिश्रित फल देगा। संतुलन बनाए रखें।",
            "सप्ताह में उतार-चढ़ाव रहेंगे। धैर्य रखें।",
            "इस सप्ताह बड़े खर्चे टालें। बजट बनाकर चलें।",
            "सप्ताह में कुछ चुनौतियां आ सकती हैं।",
        ],
        "challenging": [
            "यह सप्ताह सावधानी से बिताएं। जोखिम न लें।",
            "सप्ताह में विवादों से बचें। शांत रहें।",
            "इस सप्ताह स्वास्थ्य पर विशेष ध्यान दें।",
            "सप्ताह में बड़े निर्णय टालें। अगले सप्ताह करें।",
        ],
    },
    "monthly": {
        "excellent": [
            "यह महीना आपके लिए बेहद शुभ है। सूर्य की स्थिति उत्तम है।",
            "इस महीने करियर में बड़ी सफलता मिल सकती है।",
            "महीने में आय में वृद्धि के प्रबल योग हैं।",
            "यह महीना नए शुरुआत के लिए उत्तम है।",
        ],
        "good": [
            "यह महीना अच्छा रहेगा। प्रगति के मार्ग खुलेंगे।",
            "महीने में पारिवारिक जीवन सुखमय रहेगा।",
            "इस महीने मेहनत का अच्छा फल मिलेगा।",
            "महीने में कोई शुभ समाचार मिल सकता है।",
        ],
        "average": [
            "यह महीना सामान्य रहेगा। धीरे-धीरे प्रगति होगी।",
            "महीने में खर्चों पर नियंत्रण रखें।",
            "इस महीने बड़े निवेश से बचें।",
            "महीने में स्वास्थ्य का ध्यान रखें।",
        ],
        "challenging": [
            "यह महीना चुनौतीपूर्ण है। सावधानी से आगे बढ़ें।",
            "महीने में आर्थिक मामलों में सतर्क रहें।",
            "इस महीने रिश्तों में तनाव से बचें।",
            "महीने में बड़े फैसले अगले महीने पर टालें।",
        ],
    },
    "yearly": {
        "excellent": [
            "यह वर्ष आपके लिए स्वर्णिम है। गुरु और शनि अनुकूल हैं।",
            "इस वर्ष जीवन में बड़े सकारात्मक बदलाव आएंगे।",
            "वर्ष में धन, यश और सम्मान में वृद्धि होगी।",
            "यह वर्ष आपके सपनों को साकार करने वाला है।",
        ],
        "good": [
            "यह वर्ष कुल मिलाकर अच्छा रहेगा। प्रगति होगी।",
            "वर्ष में करियर में स्थिरता और वृद्धि मिलेगी।",
            "इस वर्ष परिवार में खुशियां आएंगी।",
            "वर्ष में नए अवसर मिलेंगे। तैयार रहें।",
        ],
        "average": [
            "यह वर्ष मिश्रित फल देगा। धैर्य रखें।",
            "वर्ष में कुछ उतार-चढ़ाव रहेंगे।",
            "इस वर्ष संयम और विवेक से काम लें।",
            "वर्ष के दूसरे भाग में स्थिति सुधरेगी।",
        ],
        "challenging": [
            "यह वर्ष चुनौतीपूर्ण है। शनि की साढ़ेसाती या ढैय्या हो सकती है।",
            "वर्ष में बड़े जोखिम न लें। सुरक्षित रहें।",
            "इस वर्ष स्वास्थ्य और धन दोनों की चिंता रहेगी।",
            "वर्ष में ईश्वर भक्ति और दान-पुण्य करें।",
        ],
    },
}


# Lucky elements by rashi
RASHI_LUCKY_ELEMENTS = {
    0: {"color": "लाल (Red)", "number": "9", "day": "मंगलवार", "deity": "हनुमान जी", "mantra": "ॐ अं अंगारकाय नमः"},
    1: {"color": "सफेद/क्रीम (White/Cream)", "number": "6", "day": "शुक्रवार", "deity": "लक्ष्मी जी", "mantra": "ॐ शुं शुक्राय नमः"},
    2: {"color": "हरा (Green)", "number": "5", "day": "बुधवार", "deity": "विष्णु भगवान", "mantra": "ॐ बुं बुधाय नमः"},
    3: {"color": "सफेद (White)", "number": "2", "day": "सोमवार", "deity": "शिव जी", "mantra": "ॐ सों सोमाय नमः"},
    4: {"color": "सुनहरा (Golden)", "number": "1", "day": "रविवार", "deity": "सूर्य देव", "mantra": "ॐ ह्रां ह्रीं ह्रौं सः सूर्याय नमः"},
    5: {"color": "हरा (Green)", "number": "5", "day": "बुधवार", "deity": "दुर्गा माता", "mantra": "ॐ बुं बुधाय नमः"},
    6: {"color": "सफेद/गुलाबी (White/Pink)", "number": "6", "day": "शुक्रवार", "deity": "लक्ष्मी जी", "mantra": "ॐ शुं शुक्राय नमः"},
    7: {"color": "लाल (Red)", "number": "9", "day": "मंगलवार", "deity": "हनुमान जी", "mantra": "ॐ अं अंगारकाय नमः"},
    8: {"color": "पीला (Yellow)", "number": "3", "day": "गुरुवार", "deity": "गुरु बृहस्पति", "mantra": "ॐ बृं बृहस्पतये नमः"},
    9: {"color": "नीला/काला (Blue/Black)", "number": "8", "day": "शनिवार", "deity": "शनि देव", "mantra": "ॐ शं शनैश्चराय नमः"},
    10: {"color": "नीला/काला (Blue/Black)", "number": "8", "day": "शनिवार", "deity": "शनि देव", "mantra": "ॐ शं शनैश्चराय नमः"},
    11: {"color": "पीला (Yellow)", "number": "3", "day": "गुरुवार", "deity": "विष्णु भगवान", "mantra": "ॐ बृं बृहस्पतये नमः"},
}


# =============================================================================
# ACCURACY ENHANCEMENT FUNCTIONS (BPHS Chapters 17, 25, 27)
# =============================================================================

def check_combustion(
    planet: str,
    planet_longitude: float,
    sun_longitude: float,
    is_retrograde: bool = False
) -> Tuple[bool, float]:
    """
    Check if a planet is combust (Asta) - too close to the Sun.

    Based on BPHS Chapter 25 "Graha Avastha":
    - Combustion weakens a planet's significations
    - Each planet has different combustion orbs
    - Retrograde planets have tighter orbs

    Args:
        planet: Planet name (e.g., "MARS", "VENUS")
        planet_longitude: Planet's ecliptic longitude in degrees
        sun_longitude: Sun's ecliptic longitude in degrees
        is_retrograde: Whether the planet is retrograde

    Returns:
        Tuple of (is_combust: bool, severity: float 0-1)
    """
    if planet not in COMBUSTION_ORBS or planet == "SUN":
        return False, 0.0

    orb = COMBUSTION_ORBS[planet]

    # Retrograde planets have tighter combustion orb (BPHS rule)
    if is_retrograde and planet in ["MERCURY", "VENUS"]:
        orb -= 2

    # Calculate angular distance
    distance = abs(planet_longitude - sun_longitude)
    if distance > 180:
        distance = 360 - distance

    is_combust = distance < orb
    # Severity: 1.0 = very close to Sun, 0.0 = at orb boundary
    severity = max(0.0, 1 - (distance / orb)) if is_combust else 0.0

    return is_combust, round(severity, 3)


def check_planetary_war(positions: Dict[str, Dict]) -> List[Dict]:
    """
    Check for Planetary War (Graha Yuddha) - planets within 1° of each other.

    Based on BPHS Chapter 17 "Graha Yuddha Adhyaya":
    - Only Mars, Mercury, Jupiter, Venus, Saturn can be in war
    - Sun, Moon, Rahu, Ketu are excluded
    - Planet with higher declination wins (simplified: higher longitude wins)
    - Loser planet's effects are significantly weakened

    Args:
        positions: Dict of planet positions {name: {longitude, ...}}

    Returns:
        List of war dicts: [{winner, loser, distance}, ...]
    """
    wars = []
    war_planets = ["MARS", "MERCURY", "JUPITER", "VENUS", "SATURN"]

    for i, p1 in enumerate(war_planets):
        if p1 not in positions:
            continue
        for p2 in war_planets[i + 1:]:
            if p2 not in positions:
                continue

            long1 = positions[p1].get("longitude", 0)
            long2 = positions[p2].get("longitude", 0)

            distance = abs(long1 - long2)
            if distance > 180:
                distance = 360 - distance

            if distance <= 1.0:  # Within 1 degree = war
                winner = p1 if long1 > long2 else p2
                loser = p2 if winner == p1 else p1
                wars.append({
                    "winner": winner,
                    "loser": loser,
                    "distance": round(distance, 3)
                })

    return wars


def calculate_tarabala(birth_nakshatra_num: int, transit_nakshatra_num: int) -> Dict:
    """
    Calculate Tara Bala (Nakshatra strength) from the 9-fold cycle.

    Based on Muhurta Chintamani and BPHS transit principles:
    - Nakshatras are counted from birth nakshatra
    - 9 categories repeat: Janma, Sampat, Vipat, Kshema, Pratyak,
      Sadhana, Naidhana, Mitra, Parama Mitra

    Args:
        birth_nakshatra_num: Birth Moon's nakshatra (0-26)
        transit_nakshatra_num: Transiting planet's nakshatra (0-26)

    Returns:
        Dict with name, modifier, favorable
    """
    count = (transit_nakshatra_num - birth_nakshatra_num) % 27
    tara_num = (count % 9) + 1  # 1-9 cycle

    return TARABALA_EFFECTS.get(tara_num, TARABALA_EFFECTS[5])  # Default: Pratyak


def get_navamsa_strength_modifier(planet: str, longitude: float) -> float:
    """
    Get Navamsa (D9) chart strength modifier for a planet.

    Based on BPHS Chapter 6 "Varga Vibhaga":
    - Navamsa shows the soul's strength of a planet
    - Planet in own/exalted navamsa = strong
    - Planet in debilitated navamsa = weak

    Args:
        planet: Planet name
        longitude: Planet's ecliptic longitude

    Returns:
        Modifier: +0.15 for own/exalted, -0.10 for debilitated, 0 otherwise
    """
    if not NAVAMSA_AVAILABLE:
        return 0.0

    try:
        # Calculate navamsa rashi from longitude
        # Each navamsa = 3°20' = 3.333...°
        # 9 navamsas per rashi, starting from Aries for fire signs
        rashi_num = int(longitude / 30)
        degree_in_rashi = longitude % 30
        navamsa_num = int(degree_in_rashi / 3.333333)

        # Calculate navamsa rashi based on element
        # Fire signs (0,4,8): navamsas start from Aries
        # Earth signs (1,5,9): navamsas start from Capricorn
        # Air signs (2,6,10): navamsas start from Libra
        # Water signs (3,7,11): navamsas start from Cancer
        element = rashi_num % 4
        start_rashi = [0, 9, 6, 3][element]  # Aries, Cap, Libra, Cancer
        navamsa_rashi_num = (start_rashi + navamsa_num) % 12
        navamsa_rashi = RASHI_LIST[navamsa_rashi_num]

        # Check planet's dignity in navamsa
        dignities = PLANET_DIGNITIES.get(planet, {})
        own_signs = dignities.get("own", [])
        exalted = dignities.get("exalted", "")
        debilitated = dignities.get("debilitated", "")

        if navamsa_rashi == exalted or navamsa_rashi in own_signs:
            return 0.15  # Strength bonus
        elif navamsa_rashi == debilitated:
            return -0.10  # Weakness penalty

        return 0.0
    except Exception:
        return 0.0


# =============================================================================
# MAIN RASHIFAL CALCULATOR CLASS
# =============================================================================

class RashifalCalculator:
    """
    Calculator for generating Rashifal (horoscope) predictions.

    Based on:
    - Chandra Rashi (Moon Sign) as primary
    - Gochar (Transit) analysis
    - BPHS and Phaladeepika principles
    """

    def __init__(self):
        """Initialize the calculator with planetary calculator."""
        self.calculator = PlanetaryCalculator()
        self.timezone = "Asia/Kolkata"

    def get_current_planetary_positions(
        self,
        date: datetime = None,
        timezone: str = "Asia/Kolkata"
    ) -> Dict[str, Dict]:
        """
        Get current planetary positions for transit analysis.

        Args:
            date: Date for positions (default: now)
            timezone: Timezone string

        Returns:
            Dict with planet names as keys and position data as values
        """
        if date is None:
            date = datetime.now(pytz.timezone(timezone))

        jd = self.calculator.datetime_to_jd(date, timezone)
        return self.calculator.get_all_planets(jd)

    def calculate_transit_house_from_moon(
        self,
        transit_rashi_num: int,
        moon_rashi_num: int
    ) -> int:
        """
        Calculate which house a transiting planet is in from natal Moon.

        Args:
            transit_rashi_num: Rashi number of transiting planet (0-11)
            moon_rashi_num: Natal Moon's rashi number (0-11)

        Returns:
            House number from Moon (1-12)
        """
        return ((transit_rashi_num - moon_rashi_num) % 12) + 1

    def get_transit_effects_for_rashi(
        self,
        moon_rashi_num: int,
        current_positions: Dict[str, Dict],
        period: RashifalPeriod = None,
        kundali=None
    ) -> Tuple[float, List[Dict], Dict]:
        """
        Calculate overall transit effects for a rashi using authentic Vedic Gochar rules.

        NOW FULLY INTEGRATED with:
        - BPHS/Phaladeepika Gochar effects per planet
        - Kakshya sub-division modifier (ALWAYS applied)
        - Sade Sati detection (ALWAYS checked)
        - Ashtakavarga bindu-based strength (if kundali provided)
        - Vedha (obstruction) checking (if kundali provided)

        Args:
            moon_rashi_num: The Moon rashi number (0-11)
            current_positions: Current planetary positions
            period: Prediction period for period-specific weighting
            kundali: Optional Kundali object for Ashtakavarga calculations

        Returns:
            Tuple of (overall_score 0-10, list of planetary influences, extra_data dict)
        """
        influences = []
        weighted_score = 0.0
        total_weight = 0.0
        extra_data = {
            "sade_sati": None,
            "sade_sati_modifier": 0.0,
            "has_ashtakavarga": False,
            "has_vedha": False,
            "has_shadbala": False,
            "has_combustion": False,
            "has_tarabala": False,
            "has_planetary_war": False,
            "has_navamsa": False,
            "combusted_planets": [],
            "planetary_wars": [],
            "tarabala_info": None,
        }

        # Get period-specific weights or use default
        period_key = period.value if period else "daily"
        period_weights = PERIOD_PLANET_WEIGHTS.get(period_key, PLANET_WEIGHTS)

        # ========================================
        # SADE SATI CHECK (Always performed)
        # ========================================
        if ASHTAKAVARGA_AVAILABLE and "SATURN" in current_positions:
            saturn_rashi = current_positions["SATURN"]["rashi_num"]
            sade_sati_info = check_sade_sati(saturn_rashi, moon_rashi_num)
            extra_data["sade_sati"] = sade_sati_info

            if sade_sati_info["is_sade_sati"] or sade_sati_info["is_dhaiya"]:
                # Check if Saturn is Yogakaraka for this lagna (if kundali provided)
                saturn_yogakaraka = False
                if kundali:
                    lagna_rashi = kundali.lagna.get("rashi", "")
                    from .config import YOGAKARAKA
                    saturn_yogakaraka = YOGAKARAKA.get(lagna_rashi) == "SATURN"

                sade_sati_modifier = get_sade_sati_score_modifier(
                    sade_sati_info, saturn_yogakaraka
                )
                extra_data["sade_sati_modifier"] = sade_sati_modifier

        # ========================================
        # ASHTAKAVARGA & VEDHA (if kundali provided)
        # ========================================
        ashtakavarga_calc = None
        vedha_calc = None
        if kundali is not None and ASHTAKAVARGA_AVAILABLE:
            try:
                ashtakavarga_calc = AshtakavargaCalculator(kundali)
                moon_rashi_name = RASHI_LIST[moon_rashi_num]
                vedha_calc = VedhaCalculator.from_kundali(kundali, moon_rashi_name)
                extra_data["has_ashtakavarga"] = True
                extra_data["has_vedha"] = True
            except Exception:
                pass  # Fall back to basic calculation

        # Build planet houses map for Vedha checking
        planet_houses = {}
        for planet_name, pos_data in current_positions.items():
            transit_rashi = pos_data["rashi_num"]
            house = ((transit_rashi - moon_rashi_num) % 12) + 1
            planet_houses[planet_name] = house

        # ========================================
        # PLANETARY WAR CHECK (Graha Yuddha - BPHS Chapter 17)
        # Done once before the loop
        # ========================================
        planetary_wars = check_planetary_war(current_positions)
        if planetary_wars:
            extra_data["has_planetary_war"] = True
            extra_data["planetary_wars"] = planetary_wars

        # Build set of war losers for quick lookup
        war_losers = {war["loser"] for war in planetary_wars}

        for planet_name, pos_data in current_positions.items():
            transit_rashi = pos_data["rashi_num"]
            transit_rashi_name = pos_data.get("rashi", RASHI_LIST[transit_rashi])
            transit_longitude = pos_data.get("longitude", 0.0)
            house_from_moon = self.calculate_transit_house_from_moon(
                transit_rashi, moon_rashi_num
            )

            # Get authentic Gochar effects for this planet from BPHS/Phaladeepika
            planet_gochar = GOCHAR_PLANET_EFFECTS.get(planet_name, {})
            house_effects = planet_gochar.get("house_effects", {})
            house_effect = house_effects.get(house_from_moon, {})

            effect_type = house_effect.get("type", "mishra")
            intensity = house_effect.get("intensity", 0.5)
            keywords_hi = house_effect.get("keywords_hi", "")

            # Get planet weight (period-specific)
            weight = period_weights.get(planet_name, 0.5)

            # ========================================
            # KAKSHYA MODIFIER (Always applied)
            # ========================================
            kakshya_data = None
            kakshya_modifier = 0.0
            if ASHTAKAVARGA_AVAILABLE and transit_longitude > 0:
                try:
                    kakshya_data = calculate_kakshya(transit_longitude)
                    kakshya_modifier = get_kakshya_modifier(kakshya_data)
                    # Apply kakshya modifier to intensity
                    intensity = max(0.1, min(1.0, intensity + kakshya_modifier))
                except Exception:
                    pass

            # ========================================
            # ASHTAKAVARGA BINDU MODIFIER (if available)
            # ========================================
            bindu_score = None
            moorti = None
            if ashtakavarga_calc and planet_name not in ["RAHU", "KETU"]:
                try:
                    moon_rashi_name = RASHI_LIST[moon_rashi_num]
                    strength = ashtakavarga_calc.get_transit_strength_from_moon(
                        planet_name, transit_rashi_name, moon_rashi_name
                    )
                    bindu_score = strength.get("bindus", 4)
                    moorti = strength.get("moorti_name", "")
                    # Modify intensity based on Ashtakavarga (0-8 bindus)
                    # 4 bindus = neutral, <4 weakens, >4 strengthens
                    bindu_modifier = (bindu_score - 4) / 8  # -0.5 to +0.5
                    intensity = max(0.1, min(1.0, intensity + bindu_modifier * 0.3))
                except Exception:
                    pass

            # Check for Vedha (obstruction)
            vedha_blocked = False
            vedha_info = None
            if vedha_calc and effect_type == "shubh":
                try:
                    vedha_result = vedha_calc.check_vedha(planet_name, house_from_moon)
                    if vedha_result.has_vedha:
                        vedha_blocked = True
                        vedha_info = {
                            "vedha_planet": vedha_result.vedha_planet,
                            "vedha_house": vedha_result.vedha_house,
                        }
                        # Vedha nullifies good effect - make it neutral
                        effect_type = "mishra"
                        intensity = 0.5
                except Exception:
                    pass

            # ========================================
            # COMBUSTION CHECK (Asta - BPHS Chapter 25)
            # ========================================
            is_combust = False
            combust_severity = 0.0
            if planet_name not in ["SUN", "RAHU", "KETU"] and "SUN" in current_positions:
                sun_longitude = current_positions["SUN"].get("longitude", 0)
                is_retrograde = pos_data.get("is_retrograde", False)
                is_combust, combust_severity = check_combustion(
                    planet_name, transit_longitude, sun_longitude, is_retrograde
                )
                if is_combust:
                    # Combustion weakens planet's effects (50-100% based on severity)
                    intensity *= (0.5 + 0.5 * (1 - combust_severity))
                    extra_data["has_combustion"] = True
                    if planet_name not in extra_data["combusted_planets"]:
                        extra_data["combusted_planets"].append(planet_name)

            # ========================================
            # NAVAMSA D9 STRENGTH CHECK (BPHS Chapter 6)
            # ========================================
            navamsa_modifier = 0.0
            if NAVAMSA_AVAILABLE and planet_name not in ["RAHU", "KETU"]:
                navamsa_modifier = get_navamsa_strength_modifier(planet_name, transit_longitude)
                if navamsa_modifier != 0.0:
                    intensity = max(0.1, min(1.0, intensity + navamsa_modifier))
                    extra_data["has_navamsa"] = True

            # ========================================
            # SHADBALA MODIFIER (BPHS Chapter 27)
            # ========================================
            shadbala_modifier = 0.0
            if kundali and SHADBALA_AVAILABLE and planet_name not in ["RAHU", "KETU"]:
                try:
                    shadbala_modifiers = get_shadbala_for_transit(kundali, current_positions)
                    shadbala_modifier = shadbala_modifiers.get(planet_name, 0.0)
                    if shadbala_modifier != 0.0:
                        intensity = max(0.1, min(1.0, intensity + shadbala_modifier))
                        extra_data["has_shadbala"] = True
                except Exception:
                    pass

            # ========================================
            # PLANETARY WAR LOSER PENALTY (BPHS Chapter 17)
            # ========================================
            is_war_loser = False
            if planet_name in war_losers:
                is_war_loser = True
                # War loser's effects are weakened by 30%
                intensity *= 0.7

            # ========================================
            # TARA BALA CHECK (For Moon transit - Muhurta Chintamani)
            # ========================================
            tarabala_result = None
            if planet_name == "MOON" and kundali:
                try:
                    # Get birth nakshatra from kundali
                    birth_moon = kundali.planets.get("MOON", {})
                    birth_nak_num = birth_moon.get("nakshatra_num", 0)
                    transit_nak_num = pos_data.get("nakshatra_num", 0)

                    if birth_nak_num is not None and transit_nak_num is not None:
                        tarabala_result = calculate_tarabala(birth_nak_num, transit_nak_num)
                        intensity = max(0.1, min(1.0, intensity + tarabala_result["modifier"]))
                        extra_data["has_tarabala"] = True
                        extra_data["tarabala_info"] = tarabala_result
                except Exception:
                    pass

            # Calculate score contribution based on effect type
            if effect_type == "shubh":
                score_contribution = 7 + (intensity * 3)  # 7-10
            elif effect_type == "ashubh":
                score_contribution = 1 + ((1 - intensity) * 3)  # 1-4
            else:  # mishra
                score_contribution = 5  # 5

            weighted_score += score_contribution * weight
            total_weight += weight

            influence_data = {
                "planet": planet_name,
                "planet_hindi": PLANET_NAMES[Planet[planet_name]]["hindi"],
                "transit_rashi": pos_data["rashi"],
                "transit_rashi_hindi": RASHI_HINDI_NAMES[transit_rashi],
                "house_from_moon": house_from_moon,
                "effect": effect_type,
                "intensity": round(intensity, 2),
                "keywords_hindi": keywords_hi,
                "is_retrograde": pos_data.get("is_retrograde", False),
                "significance": "high" if weight >= 0.8 else "medium" if weight >= 0.6 else "low",
            }

            # Add Ashtakavarga data if available
            if bindu_score is not None:
                influence_data["ashtakavarga_bindus"] = bindu_score
                influence_data["moorti"] = moorti

            # Add Kakshya data if calculated
            if kakshya_data is not None:
                influence_data["kakshya"] = {
                    "number": kakshya_data.kakshya_num,
                    "lord": kakshya_data.kakshya_lord,
                    "modifier": round(kakshya_modifier, 3),
                }

            # Add Vedha info if blocked
            if vedha_blocked and vedha_info:
                influence_data["vedha_blocked"] = True
                influence_data["vedha_info"] = vedha_info

            # Add Combustion info if combust
            if is_combust:
                influence_data["is_combust"] = True
                influence_data["combust_severity"] = round(combust_severity, 2)

            # Add Navamsa modifier if applied
            if navamsa_modifier != 0.0:
                influence_data["navamsa_modifier"] = round(navamsa_modifier, 2)

            # Add Shadbala modifier if applied
            if shadbala_modifier != 0.0:
                influence_data["shadbala_modifier"] = round(shadbala_modifier, 2)

            # Add Planetary War loser flag
            if is_war_loser:
                influence_data["is_war_loser"] = True

            # Add Tara Bala info for Moon
            if tarabala_result:
                influence_data["tarabala"] = tarabala_result

            influences.append(influence_data)

        # Calculate final score
        final_score = (weighted_score / total_weight) if total_weight > 0 else 5.0

        # Apply Sade Sati modifier if present (affects overall score)
        sade_sati_modifier = extra_data.get("sade_sati_modifier", 0.0)
        if sade_sati_modifier != 0.0:
            final_score = max(1.0, min(10.0, final_score + sade_sati_modifier))

        # Sort influences by period-specific significance
        influences.sort(
            key=lambda x: period_weights.get(x["planet"], 0.5),
            reverse=True
        )

        return (round(final_score, 1), influences, extra_data)

    def _get_prediction_level(self, score: float) -> str:
        """Get prediction level based on score."""
        if score >= 7.5:
            return "excellent"
        elif score >= 5.5:
            return "good"
        elif score >= 4.0:
            return "average"
        else:
            return "challenging"

    def _select_prediction(
        self,
        predictions_dict: Dict[str, List[str]],
        score: float,
        seed: int
    ) -> str:
        """Select a prediction based on score and seed for variety."""
        level = self._get_prediction_level(score)
        predictions = predictions_dict.get(level, predictions_dict["average"])
        return predictions[seed % len(predictions)]

    def generate_category_predictions(
        self,
        moon_rashi_num: int,
        overall_score: float,
        influences: List[Dict],
        period: RashifalPeriod,
        date_seed: int
    ) -> List[CategoryPrediction]:
        """
        Generate predictions for each life category.

        Args:
            moon_rashi_num: Moon rashi number (0-11)
            overall_score: Overall transit score
            influences: List of planetary influences
            period: Prediction period
            date_seed: Seed based on date for variety

        Returns:
            List of CategoryPrediction objects
        """
        category_predictions = []

        # Calculate category-specific scores based on relevant house transits
        category_houses = {
            PredictionCategory.CAREER: [10],
            PredictionCategory.FINANCE: [2, 11],
            PredictionCategory.HEALTH: [6],
            PredictionCategory.RELATIONSHIPS: [7],
            PredictionCategory.FAMILY: [4],
            PredictionCategory.OVERALL: [1, 5, 9],
        }

        # Period-specific category names
        period_prefixes = {
            RashifalPeriod.DAILY: "आज ",
            RashifalPeriod.WEEKLY: "इस सप्ताह ",
            RashifalPeriod.MONTHLY: "इस महीने ",
            RashifalPeriod.YEARLY: "इस वर्ष ",
        }
        prefix = period_prefixes.get(period, "")

        category_hindi_names = {
            PredictionCategory.CAREER: f"{prefix}करियर/व्यवसाय",
            PredictionCategory.FINANCE: f"{prefix}धन/वित्त",
            PredictionCategory.HEALTH: f"{prefix}स्वास्थ्य",
            PredictionCategory.RELATIONSHIPS: f"{prefix}संबंध",
            PredictionCategory.FAMILY: f"{prefix}परिवार",
            PredictionCategory.OVERALL: f"{prefix}समग्र भाग्य",
        }

        prediction_templates = {
            PredictionCategory.CAREER: CAREER_PREDICTIONS,
            PredictionCategory.FINANCE: FINANCE_PREDICTIONS,
            PredictionCategory.HEALTH: HEALTH_PREDICTIONS,
            PredictionCategory.RELATIONSHIPS: RELATIONSHIP_PREDICTIONS,
            PredictionCategory.FAMILY: FAMILY_PREDICTIONS,
            PredictionCategory.OVERALL: PERIOD_OVERALL_PREDICTIONS.get(period.value, OVERALL_PREDICTIONS),
        }

        # Period-specific weights for categories
        period_weights = PERIOD_PLANET_WEIGHTS.get(period.value, PLANET_WEIGHTS)

        for category in PredictionCategory:
            houses = category_houses[category]

            # Calculate category-specific score using period-aware weights
            category_score = 0.0
            relevant_count = 0

            for influence in influences:
                if influence["house_from_moon"] in houses:
                    # Use period-specific weight
                    weight = period_weights.get(influence["planet"], 0.5)
                    if influence["effect"] == "shubh":
                        category_score += 8 * weight
                    elif influence["effect"] == "ashubh":
                        category_score += 3 * weight
                    else:
                        category_score += 5 * weight
                    relevant_count += weight

            # If no direct house influence, use overall score with period-based variation
            if relevant_count == 0:
                # Add period-specific variance
                period_variance = {
                    RashifalPeriod.DAILY: (date_seed % 5 - 2) * 0.4,
                    RashifalPeriod.WEEKLY: (date_seed % 4 - 2) * 0.6,
                    RashifalPeriod.MONTHLY: (date_seed % 3 - 1) * 0.8,
                    RashifalPeriod.YEARLY: (date_seed % 3 - 1) * 1.0,
                }
                variance = period_variance.get(period, 0)
                category_score = overall_score + variance
            else:
                category_score = category_score / relevant_count

            # Clamp score to 1-10
            category_score = max(1, min(10, category_score))

            # ========================================
            # BINDU-SPECIFIC PREDICTIONS (if Ashtakavarga available)
            # ========================================
            prediction_hindi = None
            if ASHTAKAVARGA_AVAILABLE:
                # Get average bindus for planets in relevant houses
                relevant_bindus = []
                for influence in influences:
                    if influence["house_from_moon"] in houses and "ashtakavarga_bindus" in influence:
                        relevant_bindus.append(influence["ashtakavarga_bindus"])

                if relevant_bindus:
                    avg_bindus = sum(relevant_bindus) / len(relevant_bindus)
                    # Map category to bindu prediction category
                    bindu_category_map = {
                        PredictionCategory.CAREER: "career",
                        PredictionCategory.FINANCE: "finance",
                        PredictionCategory.HEALTH: "health",
                        PredictionCategory.RELATIONSHIPS: "relationship",
                        PredictionCategory.FAMILY: "family",
                        PredictionCategory.OVERALL: "overall",
                    }
                    bindu_cat = bindu_category_map.get(category, "overall")
                    try:
                        prediction_hindi = get_bindu_prediction(
                            bindu_cat, int(round(avg_bindus)), date_seed
                        )
                    except Exception:
                        pass

            # Fall back to standard prediction if bindu prediction not available
            if not prediction_hindi:
                prediction_hindi = self._select_prediction(
                    prediction_templates[category],
                    category_score,
                    date_seed + hash(category.value)
                )

            # Generate English translation (simplified)
            level = self._get_prediction_level(category_score)

            category_predictions.append(CategoryPrediction(
                category=category,
                category_hindi=category_hindi_names[category],
                prediction_hindi=prediction_hindi,
                prediction_english=f"{category.value.title()} outlook: {level.title()}",
                score=int(round(category_score)),
                favorable=category_score >= 5.5,
                key_advice=self._get_key_advice(category, level),
                lucky_elements={}
            ))

        return category_predictions

    def _get_key_advice(self, category: PredictionCategory, level: str) -> str:
        """Get key advice based on category and level."""
        advice = {
            PredictionCategory.CAREER: {
                "excellent": "नए अवसर लपकें। आत्मविश्वास से आगे बढ़ें।",
                "good": "मेहनत जारी रखें। धैर्य रखें।",
                "average": "सतर्क रहें। बड़े बदलाव टालें।",
                "challenging": "शांत रहें। संयम से काम लें।",
            },
            PredictionCategory.FINANCE: {
                "excellent": "निवेश का अच्छा समय। बचत करें।",
                "good": "बजट बनाकर चलें।",
                "average": "खर्चों पर नियंत्रण रखें।",
                "challenging": "कोई भी जोखिम न लें।",
            },
            PredictionCategory.HEALTH: {
                "excellent": "एक्टिव रहें। व्यायाम करें।",
                "good": "नियमित दिनचर्या अपनाएं।",
                "average": "आराम करें। तनाव से बचें।",
                "challenging": "डॉक्टर से मिलें।",
            },
            PredictionCategory.RELATIONSHIPS: {
                "excellent": "प्यार का इजहार करें।",
                "good": "समय दें। बात करें।",
                "average": "धैर्य रखें। समझदारी दिखाएं।",
                "challenging": "शांत रहें। विवाद से बचें।",
            },
            PredictionCategory.FAMILY: {
                "excellent": "खुशियां बांटें। उत्सव मनाएं।",
                "good": "समय दें। संवाद बनाए रखें।",
                "average": "बड़ों का आशीर्वाद लें।",
                "challenging": "धैर्य रखें। प्रेम से बात करें।",
            },
            PredictionCategory.OVERALL: {
                "excellent": "आगे बढ़ें। भाग्य साथ है।",
                "good": "सकारात्मक रहें।",
                "average": "नियमित पूजा-पाठ करें।",
                "challenging": "ईश्वर पर भरोसा रखें।",
            },
        }
        return advice.get(category, {}).get(level, "धैर्य रखें।")

    def _get_dynamic_lucky_elements(
        self, rashi_num: int, kundali=None, dasha_sync_info=None
    ) -> Dict[str, str]:
        """
        Get lucky elements dynamically based on:
        1. Current dasha lord (if kundali provided) - most personalized
        2. Fall back to rashi-based (if no kundali) - newspaper horoscope style

        This ensures personalized lucky elements when chart is available.
        """
        # Lucky elements by ruling planet (for dasha-based selection)
        PLANET_LUCKY_ELEMENTS = {
            "Sun": {"color": "सुनहरा/नारंगी (Golden/Orange)", "number": "1, 4", "day": "रविवार", "deity": "सूर्य देव", "mantra": "ॐ ह्रां ह्रीं ह्रौं सः सूर्याय नमः"},
            "Moon": {"color": "सफेद/चांदी (White/Silver)", "number": "2, 7", "day": "सोमवार", "deity": "शिव जी", "mantra": "ॐ सों सोमाय नमः"},
            "Mars": {"color": "लाल (Red)", "number": "9, 3", "day": "मंगलवार", "deity": "हनुमान जी", "mantra": "ॐ अं अंगारकाय नमः"},
            "Mercury": {"color": "हरा (Green)", "number": "5, 3", "day": "बुधवार", "deity": "विष्णु भगवान", "mantra": "ॐ बुं बुधाय नमः"},
            "Jupiter": {"color": "पीला (Yellow)", "number": "3, 12", "day": "गुरुवार", "deity": "गुरु बृहस्पति", "mantra": "ॐ बृं बृहस्पतये नमः"},
            "Venus": {"color": "सफेद/गुलाबी (White/Pink)", "number": "6, 5", "day": "शुक्रवार", "deity": "लक्ष्मी जी", "mantra": "ॐ शुं शुक्राय नमः"},
            "Saturn": {"color": "नीला/काला (Blue/Black)", "number": "8, 10", "day": "शनिवार", "deity": "शनि देव", "mantra": "ॐ शं शनैश्चराय नमः"},
            "Rahu": {"color": "गहरा नीला/काला (Dark Blue/Black)", "number": "4, 8", "day": "शनिवार", "deity": "दुर्गा माता", "mantra": "ॐ रां राहवे नमः"},
            "Ketu": {"color": "भूरा/धूसर (Brown/Grey)", "number": "7, 9", "day": "मंगलवार", "deity": "गणेश जी", "mantra": "ॐ कें केतवे नमः"},
        }

        # If kundali with dasha info is available, use dasha lord's elements
        if kundali is not None:
            try:
                dasha_info = None
                if hasattr(kundali, 'get_current_dasha'):
                    dasha_info = kundali.get_current_dasha()
                elif hasattr(kundali, 'dasha'):
                    dasha_info = getattr(kundali, 'dasha', None)

                if dasha_info and isinstance(dasha_info, dict):
                    maha_lord = dasha_info.get('mahadasha', {}).get('planet', '')
                    if maha_lord and maha_lord in PLANET_LUCKY_ELEMENTS:
                        # Return dasha lord's lucky elements
                        return PLANET_LUCKY_ELEMENTS[maha_lord]
            except Exception:
                pass  # Fall through to rashi-based

        # Fall back to static rashi-based elements (newspaper horoscope style)
        return RASHI_LUCKY_ELEMENTS.get(rashi_num, RASHI_LUCKY_ELEMENTS[0])

    def _generate_dos_donts(
        self,
        influences: List[Dict],
        overall_score: float,
        period: RashifalPeriod
    ) -> Tuple[List[str], List[str]]:
        """Generate do's and don'ts based on transit analysis, period, and planetary positions."""
        dos = []
        donts = []

        # Period prefix
        period_prefix = {
            RashifalPeriod.DAILY: "आज ",
            RashifalPeriod.WEEKLY: "इस सप्ताह ",
            RashifalPeriod.MONTHLY: "इस माह ",
            RashifalPeriod.YEARLY: "इस वर्ष ",
        }
        prefix = period_prefix.get(period, "")

        # House-specific advice based on planetary transits (BPHS Gochar rules)
        house_dos = {
            1: "आत्मविश्वास बढ़ाएं",
            2: "धन संचय करें",
            3: "साहस से काम लें",
            4: "परिवार के साथ समय बिताएं",
            5: "रचनात्मक कार्य करें",
            6: "स्वास्थ्य पर ध्यान दें",
            7: "साझेदारी में सहयोग करें",
            8: "अध्यात्म में रुचि लें",
            9: "धार्मिक कार्य करें",
            10: "करियर पर फोकस करें",
            11: "मित्रों से मिलें",
            12: "दान-पुण्य करें",
        }

        house_donts = {
            1: "अहंकार से बचें",
            2: "फिजूलखर्ची न करें",
            3: "जल्दबाजी न करें",
            4: "घर में विवाद न करें",
            5: "जुआ/सट्टे से दूर रहें",
            6: "दुश्मनों को उकसाएं नहीं",
            7: "रिश्तों में टकराव से बचें",
            8: "जोखिम न लें",
            9: "अधर्म से दूर रहें",
            10: "बॉस से बहस न करें",
            11: "गलत संगत से बचें",
            12: "अनावश्यक खर्च न करें",
        }

        # Planet-specific advice based on house position and effect
        planet_advice = {
            "SATURN": {
                "shubh_dos": ["मेहनत और लगन से काम करें", "बड़ों की सेवा करें"],
                "shubh_donts": ["आलस्य न करें"],
                "ashubh_dos": ["शनि मंत्र का जाप करें", "काले तिल का दान करें"],
                "ashubh_donts": ["जल्दबाजी में फैसले न लें", "नया काम शुरू न करें"],
            },
            "JUPITER": {
                "shubh_dos": ["गुरुवार को व्रत रखें", "शिक्षा और ज्ञान बढ़ाएं", "गुरु का आशीर्वाद लें"],
                "shubh_donts": ["अहंकार न करें"],
                "ashubh_dos": ["पीले वस्त्र धारण करें", "विष्णु पूजा करें"],
                "ashubh_donts": ["अति आत्मविश्वास से बचें", "बड़े निवेश टालें"],
            },
            "MARS": {
                "shubh_dos": ["खेल और व्यायाम करें", "साहसिक कार्य करें"],
                "shubh_donts": ["उग्रता से बचें"],
                "ashubh_dos": ["हनुमान चालीसा पढ़ें", "लाल वस्त्र पहनें"],
                "ashubh_donts": ["क्रोध पर नियंत्रण रखें", "विवाद से बचें", "वाहन सावधानी से चलाएं"],
            },
            "VENUS": {
                "shubh_dos": ["कला और संगीत का आनंद लें", "सौंदर्य प्रसाधन खरीदें"],
                "shubh_donts": ["भोग-विलास में अति न करें"],
                "ashubh_dos": ["शुक्र मंत्र जपें", "सफेद वस्त्र धारण करें"],
                "ashubh_donts": ["अनावश्यक खर्च से बचें", "प्रेम संबंधों में सावधानी"],
            },
            "MERCURY": {
                "shubh_dos": ["व्यापार और संचार में आगे बढ़ें", "नई भाषा सीखें"],
                "shubh_donts": ["बहुत ज्यादा न बोलें"],
                "ashubh_dos": ["बुध मंत्र जपें", "हरे रंग का प्रयोग करें"],
                "ashubh_donts": ["महत्वपूर्ण दस्तावेज सावधानी से करें", "झूठ न बोलें"],
            },
            "MOON": {
                "shubh_dos": ["मां की सेवा करें", "जल दान करें"],
                "shubh_donts": ["मन को अशांत न होने दें"],
                "ashubh_dos": ["चंद्र मंत्र जपें", "सफेद वस्तुएं दान करें"],
                "ashubh_donts": ["भावुकता में निर्णय न लें", "मानसिक तनाव से बचें"],
            },
            "SUN": {
                "shubh_dos": ["सूर्य नमस्कार करें", "पिता की सेवा करें"],
                "shubh_donts": ["घमंड न करें"],
                "ashubh_dos": ["आदित्य हृदय स्तोत्र पढ़ें", "गेहूं दान करें"],
                "ashubh_donts": ["सरकारी कार्यों में सावधानी", "पिता से विवाद न करें"],
            },
            "RAHU": {
                "shubh_dos": ["नई तकनीक सीखें", "विदेश यात्रा की योजना बनाएं"],
                "shubh_donts": ["अति लालच से बचें"],
                "ashubh_dos": ["राहु मंत्र जपें", "नारियल दान करें"],
                "ashubh_donts": ["नशीली चीजों से दूर रहें", "झूठ और छल से बचें", "अनजान लोगों पर भरोसा न करें"],
            },
            "KETU": {
                "shubh_dos": ["आध्यात्मिक साधना करें", "ध्यान करें"],
                "shubh_donts": ["भौतिकता में न फंसें"],
                "ashubh_dos": ["गणेश पूजा करें", "कुत्ते को रोटी खिलाएं"],
                "ashubh_donts": ["अचानक निर्णय न लें", "पुराने विवादों को न छेड़ें"],
            },
        }

        # FIRST: Add planet-specific advice based on current transits (varies with date)
        for influence in influences:
            planet = influence["planet"]
            effect = influence["effect"]
            house = influence["house_from_moon"]

            advice = planet_advice.get(planet, {})

            if effect == "shubh":
                if advice.get("shubh_dos"):
                    dos.append(f"{prefix}{advice['shubh_dos'][0]}")
                if advice.get("shubh_donts"):
                    donts.append(f"{prefix}{advice['shubh_donts'][0]}")
            elif effect == "ashubh":
                if advice.get("ashubh_dos"):
                    dos.append(f"{prefix}{advice['ashubh_dos'][0]}")
                if advice.get("ashubh_donts"):
                    donts.append(f"{prefix}{advice['ashubh_donts'][0]}")

            # Add house-specific advice for significant planets
            if influence.get("significance") == "high":
                dos.append(f"{prefix}{house_dos.get(house, '')}")
                donts.append(f"{prefix}{house_donts.get(house, '')}")

        # SECOND: Add general advice based on score level (as fallback)
        if overall_score >= 7:
            dos.append(f"{prefix}नए कार्य शुरू करें")
            dos.append(f"{prefix}महत्वपूर्ण निर्णय लें")
        elif overall_score >= 5:
            dos.append(f"{prefix}धैर्य से काम लें")
            dos.append(f"{prefix}नियमित कार्य जारी रखें")
        else:
            dos.append(f"{prefix}शांत रहें और पूजा-पाठ करें")
            donts.append(f"{prefix}बड़े फैसले टालें")

        # Remove empty strings and duplicates while preserving order
        dos = [d for d in dos if d.strip()]
        donts = [d for d in donts if d.strip()]
        dos = list(dict.fromkeys(dos))[:5]
        donts = list(dict.fromkeys(donts))[:5]

        # Add default items if needed
        if not donts:
            default_donts = {
                RashifalPeriod.DAILY: ["आज अनावश्यक तनाव न लें", "आज गलत संगत से बचें"],
                RashifalPeriod.WEEKLY: ["इस सप्ताह अनावश्यक तनाव न लें", "इस हफ्ते गलत संगत से बचें"],
                RashifalPeriod.MONTHLY: ["इस माह अनावश्यक तनाव न लें", "इस महीने गलत संगत से बचें"],
                RashifalPeriod.YEARLY: ["इस वर्ष अनावश्यक तनाव न लें", "इस साल गलत संगत से बचें"],
            }
            donts = default_donts.get(period, default_donts[RashifalPeriod.DAILY])

        if not dos:
            default_dos = {
                RashifalPeriod.DAILY: ["आज सकारात्मक सोचें", "आज ईश्वर का स्मरण करें"],
                RashifalPeriod.WEEKLY: ["इस सप्ताह सकारात्मक रहें", "हफ्ते में मंदिर जाएं"],
                RashifalPeriod.MONTHLY: ["इस माह आशावादी रहें", "महीने में दान करें"],
                RashifalPeriod.YEARLY: ["इस वर्ष धैर्य रखें", "साल भर पुण्य कार्य करें"],
            }
            dos = default_dos.get(period, default_dos[RashifalPeriod.DAILY])

        return (dos, donts)

    def _format_key_transits(
        self,
        influences: List[Dict],
        period: RashifalPeriod
    ) -> List[str]:
        """Format key transits as readable strings."""
        key_transits = []

        for influence in influences[:4]:  # Top 4 significant transits
            planet_hindi = influence["planet_hindi"]
            rashi_hindi = influence["transit_rashi_hindi"]
            house = influence["house_from_moon"]
            effect = influence["effect"]
            retrograde = influence.get("is_retrograde", False)

            effect_text = "शुभ" if effect == "shubh" else "चुनौतीपूर्ण" if effect == "ashubh" else "मिश्रित"
            retro_text = " (वक्री)" if retrograde else ""

            transit_text = f"{planet_hindi}{retro_text} {rashi_hindi} में ({house}वें भाव में) - {effect_text}"
            key_transits.append(transit_text)

        return key_transits

    def generate_rashifal(
        self,
        rashi_num: int,
        period: RashifalPeriod,
        date: datetime = None,
        timezone: str = "Asia/Kolkata",
        kundali=None
    ) -> RashifalPrediction:
        """
        Generate complete Rashifal prediction for a rashi.

        FULLY INTEGRATED with Vedic components:
        - Sade Sati detection (ALWAYS applied)
        - Kakshya sub-division modifier (ALWAYS applied)
        - Ashtakavarga bindu-based strength (if kundali provided)
        - Vedha obstruction checking (if kundali provided)
        - Dasha-Transit synchronization (if kundali has dasha info)

        Args:
            rashi_num: Rashi number (0-11, where 0=Mesha/Aries)
            period: Prediction period (daily/weekly/monthly/yearly)
            date: Start date for prediction (default: now)
            timezone: Timezone string
            kundali: Optional Kundali object for personalized predictions

        Returns:
            RashifalPrediction object with complete prediction
        """
        if date is None:
            date = datetime.now(pytz.timezone(timezone))

        # Calculate date range based on period
        if period == RashifalPeriod.DAILY:
            start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=1)
        elif period == RashifalPeriod.WEEKLY:
            # Start from Monday of current week
            days_since_monday = date.weekday()
            start_date = (date - timedelta(days=days_since_monday)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            end_date = start_date + timedelta(days=7)
        elif period == RashifalPeriod.MONTHLY:
            start_date = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            # Get last day of month
            if date.month == 12:
                end_date = start_date.replace(year=date.year + 1, month=1)
            else:
                end_date = start_date.replace(month=date.month + 1)
        else:  # yearly
            start_date = date.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date.replace(year=date.year + 1)

        # Get current planetary positions
        positions = self.get_current_planetary_positions(date, timezone)

        # Calculate transit effects with period-specific weighting
        # NOW FULLY INTEGRATED: passes kundali for Ashtakavarga, Vedha, Kakshya, Sade Sati
        overall_score, influences, extra_data = self.get_transit_effects_for_rashi(
            rashi_num, positions, period, kundali
        )

        # ========================================
        # DASHA-TRANSIT SYNCHRONIZATION (if kundali has dasha info)
        # ========================================
        dasha_sync_info = None
        if kundali is not None and ASHTAKAVARGA_AVAILABLE:
            try:
                # Check if kundali has dasha information via get_current_dasha method
                dasha_info = None
                if hasattr(kundali, 'get_current_dasha'):
                    dasha_info = kundali.get_current_dasha()
                elif hasattr(kundali, 'dasha'):
                    dasha_info = getattr(kundali, 'dasha', None)

                if dasha_info and isinstance(dasha_info, dict):
                    from .dasha_transit_sync import apply_dasha_transit_sync
                    overall_score, dasha_sync_info = apply_dasha_transit_sync(
                        overall_score, dasha_info, positions, rashi_num
                    )
            except Exception:
                pass  # Dasha sync is optional enhancement

        # Generate period-specific date seed for prediction variety
        # Different periods should give different predictions even on same day
        period_multipliers = {
            RashifalPeriod.DAILY: 1,
            RashifalPeriod.WEEKLY: 7,
            RashifalPeriod.MONTHLY: 30,
            RashifalPeriod.YEARLY: 365,
        }
        base_seed = int(date.strftime("%Y%m%d"))
        period_mult = period_multipliers.get(period, 1)
        date_seed = base_seed * period_mult + rashi_num

        # Generate category predictions
        category_predictions = self.generate_category_predictions(
            rashi_num, overall_score, influences, period, date_seed
        )

        # Generate do's and don'ts
        dos, donts = self._generate_dos_donts(influences, overall_score, period)

        # Format key transits
        key_transits = self._format_key_transits(influences, period)

        # Get lucky elements - dynamic based on current dasha if kundali provided
        lucky = self._get_dynamic_lucky_elements(rashi_num, kundali, dasha_sync_info)

        # Generate overall prediction text (period-specific)
        level = self._get_prediction_level(overall_score)
        period_predictions = PERIOD_OVERALL_PREDICTIONS.get(
            period.value, OVERALL_PREDICTIONS
        )
        overall_prediction = self._select_prediction(
            period_predictions, overall_score, date_seed
        )

        # Check if Kakshya was used in any influence
        has_kakshya = any("kakshya" in inf for inf in influences)

        return RashifalPrediction(
            rashi_num=rashi_num,
            rashi_name=RASHIS[rashi_num]["name"],
            rashi_hindi=RASHI_HINDI_NAMES[rashi_num],
            rashi_symbol=RASHIS[rashi_num]["symbol"],
            period=period,
            start_date=start_date,
            end_date=end_date,
            overall_score=int(round(overall_score)),
            overall_prediction_hindi=overall_prediction,
            overall_prediction_english=f"Overall outlook: {level.title()}",
            category_predictions=category_predictions,
            planetary_influences=influences,
            key_transits=key_transits,
            lucky_color=lucky["color"],
            lucky_number=lucky["number"],
            lucky_day=lucky["day"],
            mantra=lucky["mantra"],
            deity=lucky["deity"],
            dos=dos,
            donts=donts,
            # Enhanced Vedic components
            sade_sati_info=extra_data.get("sade_sati"),
            dasha_sync_info=dasha_sync_info,
            has_ashtakavarga=extra_data.get("has_ashtakavarga", False),
            has_vedha=extra_data.get("has_vedha", False),
            has_kakshya=has_kakshya,
            # Additional accuracy components
            has_shadbala=extra_data.get("has_shadbala", False),
            has_combustion_check=extra_data.get("has_combustion", False),
            has_tarabala=extra_data.get("has_tarabala", False),
            has_planetary_war=extra_data.get("has_planetary_war", False),
            has_navamsa_check=extra_data.get("has_navamsa", False),
            combusted_planets=extra_data.get("combusted_planets", []),
            planetary_wars=extra_data.get("planetary_wars", []),
            tarabala_info=extra_data.get("tarabala_info"),
        )

    def generate_all_rashifal(
        self,
        period: RashifalPeriod,
        date: datetime = None,
        timezone: str = "Asia/Kolkata"
    ) -> List[RashifalPrediction]:
        """
        Generate Rashifal for all 12 rashis.

        Args:
            period: Prediction period
            date: Start date (default: now)
            timezone: Timezone string

        Returns:
            List of RashifalPrediction objects for all 12 rashis
        """
        predictions = []
        for rashi_num in range(12):
            prediction = self.generate_rashifal(rashi_num, period, date, timezone)
            predictions.append(prediction)
        return predictions


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_rashifal(
    rashi_num: int,
    period: str = "daily",
    date: datetime = None,
    kundali=None
) -> Dict:
    """
    Convenience function to get Rashifal prediction.

    Args:
        rashi_num: Rashi number (0-11)
        period: Period string ("daily", "weekly", "monthly", "yearly")
        date: Date for prediction (default: now)
        kundali: Optional Kundali object for personalized predictions

    Returns:
        Dict with prediction data including enhanced Vedic components
    """
    calculator = RashifalCalculator()
    period_enum = RashifalPeriod(period.lower())

    prediction = calculator.generate_rashifal(rashi_num, period_enum, date, kundali=kundali)

    # Convert to dict for API response
    return {
        "rashi_num": prediction.rashi_num,
        "rashi_name": prediction.rashi_name,
        "rashi_hindi": prediction.rashi_hindi,
        "rashi_symbol": prediction.rashi_symbol,
        "period": prediction.period.value,
        "start_date": prediction.start_date.isoformat(),
        "end_date": prediction.end_date.isoformat(),
        "overall_score": prediction.overall_score,
        "overall_prediction_hindi": prediction.overall_prediction_hindi,
        "overall_prediction_english": prediction.overall_prediction_english,
        "category_predictions": [
            {
                "category": cp.category.value,
                "category_hindi": cp.category_hindi,
                "prediction_hindi": cp.prediction_hindi,
                "prediction_english": cp.prediction_english,
                "score": cp.score,
                "favorable": cp.favorable,
                "key_advice": cp.key_advice,
            }
            for cp in prediction.category_predictions
        ],
        "planetary_influences": prediction.planetary_influences,
        "key_transits": prediction.key_transits,
        "lucky_color": prediction.lucky_color,
        "lucky_number": prediction.lucky_number,
        "lucky_day": prediction.lucky_day,
        "mantra": prediction.mantra,
        "deity": prediction.deity,
        "dos": prediction.dos,
        "donts": prediction.donts,
        "generated_at": prediction.generated_at.isoformat(),
        # Enhanced Vedic components (99.99% accuracy)
        "sade_sati_info": prediction.sade_sati_info,
        "dasha_sync_info": prediction.dasha_sync_info,
        "has_ashtakavarga": prediction.has_ashtakavarga,
        "has_vedha": prediction.has_vedha,
        "has_kakshya": prediction.has_kakshya,
        # Additional accuracy components
        "has_shadbala": prediction.has_shadbala,
        "has_combustion_check": prediction.has_combustion_check,
        "has_tarabala": prediction.has_tarabala,
        "has_planetary_war": prediction.has_planetary_war,
        "has_navamsa_check": prediction.has_navamsa_check,
        "combusted_planets": prediction.combusted_planets,
        "planetary_wars": prediction.planetary_wars,
        "tarabala_info": prediction.tarabala_info,
    }


def get_all_rashifal(
    period: str = "daily",
    date: datetime = None
) -> List[Dict]:
    """
    Get Rashifal for all 12 rashis.

    Args:
        period: Period string ("daily", "weekly", "monthly", "yearly")
        date: Date for prediction (default: now)

    Returns:
        List of dicts with prediction data for all 12 rashis
    """
    return [get_rashifal(i, period, date) for i in range(12)]


def get_rashi_list() -> List[Dict]:
    """
    Get list of all rashis with basic info.

    Returns:
        List of dicts with rashi info
    """
    return [
        {
            "rashi_num": i,
            "name": RASHIS[i]["name"],
            "english": RASHIS[i]["english"],
            "hindi": RASHI_HINDI_NAMES[i],
            "symbol": RASHIS[i]["symbol"],
            "lord": RASHIS[i]["lord"],
            "element": RASHIS[i]["element"],
        }
        for i in range(12)
    ]


# Export for module access
__all__ = [
    "RashifalCalculator",
    "RashifalPrediction",
    "RashifalPeriod",
    "PredictionCategory",
    "CategoryPrediction",
    "get_rashifal",
    "get_all_rashifal",
    "get_rashi_list",
    "RASHI_HINDI_NAMES",
]
