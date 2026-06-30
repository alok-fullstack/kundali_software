"""
Kundali Matching Predictions and Remedies

This module provides:
- Detailed interpretation of each Koota
- Remedies for various doshas
- Marriage timing suggestions
- Compatibility analysis narratives

Based on classical texts:
- Brihat Parashara Hora Shastra
- Muhurta Chintamani
- Jataka Parijata
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from .kundali_matching import (
    MatchingResult, KootaResult, Gana, Nadi, Varna, VashyaType,
    NAKSHATRA_GANA, NAKSHATRA_NADI, RASHI_VARNA,
    NAKSHATRA_NAMES, RASHI_LORDS
)
from .config import RASHIS


# =============================================================================
# KOOTA INTERPRETATIONS
# =============================================================================

VARNA_INTERPRETATIONS = {
    "full": {
        "title": "Excellent Spiritual Compatibility",
        "title_hindi": "उत्तम आध्यात्मिक मेल",
        "description": "The boy's varna (spiritual level) is equal to or higher than the girl's. This indicates a harmonious spiritual and intellectual relationship where traditional roles are naturally balanced.",
        "description_hindi": "लड़के का वर्ण लड़की के बराबर या ऊंचा है। इससे दोनों में आपसी सम्मान रहेगा और परिवार में शांति बनी रहेगी। दोनों एक-दूसरे की सोच को समझेंगे।",
        "effects": [
            "Mutual respect in spiritual matters",
            "Balanced ego dynamics",
            "Good understanding of each other's values",
            "Harmonious family life"
        ],
        "effects_hindi": [
            "धार्मिक मामलों में आपसी सम्मान रहेगा",
            "अहंकार की टक्कर नहीं होगी",
            "एक-दूसरे की values समझेंगे",
            "घर में शांति और खुशहाली रहेगी"
        ]
    },
    "none": {
        "title": "Varna Mismatch",
        "title_hindi": "वर्ण में अंतर",
        "description": "The girl's varna is higher than the boy's. In traditional interpretation, this may cause ego conflicts, though modern couples often overcome this through mutual understanding.",
        "description_hindi": "लड़की का वर्ण लड़के से ऊंचा है। परंपरा के अनुसार इससे कभी-कभी ego की समस्या हो सकती है, लेकिन समझदारी से इसे handle किया जा सकता है।",
        "effects": [
            "Possible ego clashes",
            "Girl may feel intellectually superior",
            "May require extra effort in mutual respect",
            "Communication about values important"
        ],
        "effects_hindi": [
            "कभी-कभी ego की टक्कर हो सकती है",
            "लड़की को खुद को ज्यादा समझदार लग सकता है",
            "एक-दूसरे की इज्जत करने में मेहनत लगेगी",
            "खुलकर बात करना जरूरी है"
        ]
    }
}

VASHYA_INTERPRETATIONS = {
    "excellent": {
        "title": "Strong Mutual Attraction",
        "title_hindi": "बहुत अच्छा आकर्षण",
        "description": "Both partners naturally feel drawn to each other. There is a magnetic quality to the relationship with good mutual understanding and cooperation.",
        "description_hindi": "दोनों में natural खिंचाव है। एक-दूसरे को समझना आसान होगा और रिश्ते में chemistry बहुत अच्छी रहेगी।",
        "effects": [
            "Natural attraction and affection",
            "Partners tend to agree easily",
            "Good cooperation in daily life",
            "Harmonious domestic environment"
        ],
        "effects_hindi": [
            "एक-दूसरे के प्रति natural प्यार और आकर्षण",
            "ज्यादातर बातों पर आसानी से सहमत होंगे",
            "रोज़मर्रा के कामों में अच्छा तालमेल",
            "घर का माहौल खुशनुमा रहेगा"
        ]
    },
    "good": {
        "title": "Moderate Attraction",
        "title_hindi": "ठीक-ठाक आकर्षण",
        "description": "There is partial mutual attraction. One partner may be more dominant, but with understanding, balance can be achieved.",
        "description_hindi": "दोनों में आकर्षण है पर थोड़ा कम। एक partner ज्यादा dominant हो सकता है, लेकिन समझदारी से balance बनाया जा सकता है।",
        "effects": [
            "One partner may lead more often",
            "Compromise needed in decisions",
            "Workable relationship dynamics",
            "Respect develops over time"
        ],
        "effects_hindi": [
            "एक partner ज्यादा lead करेगा",
            "फैसलों में compromise करना होगा",
            "रिश्ता चल सकता है थोड़ी मेहनत से",
            "समय के साथ respect बढ़ेगी"
        ]
    },
    "poor": {
        "title": "Weak Mutual Attraction",
        "title_hindi": "कम आकर्षण",
        "description": "Natural chemistry may be lacking. The relationship may require more conscious effort to maintain harmony and understanding.",
        "description_hindi": "दोनों में natural chemistry थोड़ी कम है। रिश्ते को अच्छा बनाने के लिए दोनों को मेहनत करनी होगी।",
        "effects": [
            "May feel like strangers initially",
            "Extra effort needed for bonding",
            "Different wavelengths possible",
            "Patience required in early years"
        ],
        "effects_hindi": [
            "शुरू में थोड़ा अजनबी जैसा feel हो सकता है",
            "एक-दूसरे से जुड़ने में मेहनत लगेगी",
            "सोच में फर्क हो सकता है",
            "शुरुआती सालों में धैर्य रखना होगा"
        ]
    }
}

TARA_INTERPRETATIONS = {
    "auspicious": {
        "title": "Favorable Star Alignment",
        "title_hindi": "शुभ तारा मेल",
        "description": "The birth stars (nakshatras) are in a favorable relationship. This indicates health compatibility and overall well-being for both partners.",
        "description_hindi": "दोनों के जन्म नक्षत्र अच्छे position में हैं। इससे दोनों की सेहत अच्छी रहेगी और जीवन में सुख-समृद्धि आएगी।",
        "effects": [
            "Good health in married life",
            "Prosperity and happiness",
            "Supportive life path alignment",
            "Children will be healthy"
        ],
        "effects_hindi": [
            "शादी के बाद सेहत अच्छी रहेगी",
            "घर में खुशहाली और समृद्धि आएगी",
            "जीवन में एक-दूसरे का साथ मिलेगा",
            "बच्चे स्वस्थ होंगे"
        ]
    },
    "neutral": {
        "title": "Mixed Star Alignment",
        "title_hindi": "मिला-जुला तारा मेल",
        "description": "One of the Taras is inauspicious. This partial compatibility suggests some areas of life may face challenges.",
        "description_hindi": "एक तारा थोड़ा कमजोर है। कुछ क्षेत्रों में थोड़ी दिक्कत हो सकती है, पर manage हो जाएगी।",
        "effects": [
            "Some health concerns possible",
            "Need attention to specific life areas",
            "Generally manageable with awareness",
            "Remedies can help balance"
        ],
        "effects_hindi": [
            "कभी-कभी सेहत का ध्यान रखना होगा",
            "कुछ मामलों में सावधानी जरूरी",
            "समझदारी से सब संभल जाएगा",
            "उपाय करने से और अच्छा होगा"
        ]
    },
    "inauspicious": {
        "title": "Challenging Star Alignment",
        "title_hindi": "तारा में कमजोरी",
        "description": "Both Taras fall in inauspicious categories (Vipat, Pratyak, or Naidhana). This indicates potential challenges in health and overall fortune.",
        "description_hindi": "दोनों के तारा मेल में कमी है। सेहत और किस्मत में कुछ रुकावटें आ सकती हैं। उपाय जरूर करें।",
        "effects": [
            "Health issues may arise",
            "Obstacles in joint ventures",
            "Financial challenges possible",
            "Remedies strongly recommended"
        ],
        "effects_hindi": [
            "सेहत की परेशानी हो सकती है",
            "साथ मिलकर काम करने में दिक्कत",
            "पैसों की तंगी हो सकती है",
            "उपाय करना बहुत जरूरी है"
        ]
    }
}

YONI_INTERPRETATIONS = {
    "excellent": {
        "title": "Perfect Physical Compatibility",
        "title_hindi": "शारीरिक मेल बहुत अच्छा",
        "description": "Same yoni (animal symbol) with complementary genders indicates excellent physical and intimate compatibility. The couple will have a satisfying physical relationship.",
        "description_hindi": "दोनों की योनि (शारीरिक स्वभाव) एक जैसी है। इससे शादी के बाद शारीरिक संबंध और intimacy में कोई दिक्कत नहीं होगी। दोनों एक-दूसरे को अच्छे से समझेंगे।",
        "effects": [
            "Excellent physical compatibility",
            "Strong attraction maintained",
            "Satisfying intimate life",
            "Physical harmony in marriage"
        ],
        "effects_hindi": [
            "शारीरिक तालमेल बहुत अच्छा रहेगा",
            "एक-दूसरे के प्रति आकर्षण बना रहेगा",
            "वैवाहिक जीवन में संतुष्टि रहेगी",
            "शारीरिक संबंधों में harmony रहेगी"
        ]
    },
    "good": {
        "title": "Good Physical Compatibility",
        "title_hindi": "शारीरिक मेल अच्छा",
        "description": "Same yoni with same gender, or friendly yonis. Good physical compatibility with some adjustments needed.",
        "description_hindi": "योनि मेल ठीक-ठाक है। शारीरिक संबंधों में थोड़ा adjustment करना पड़ सकता है, पर overall अच्छा रहेगा।",
        "effects": [
            "Good physical understanding",
            "Attraction present",
            "Minor adjustments may help",
            "Overall satisfying relationship"
        ],
        "effects_hindi": [
            "एक-दूसरे को अच्छे से समझेंगे",
            "आकर्षण है दोनों में",
            "थोड़े adjustment से और अच्छा होगा",
            "Overall संतुष्टि रहेगी"
        ]
    },
    "moderate": {
        "title": "Moderate Physical Compatibility",
        "title_hindi": "शारीरिक मेल ठीक-ठाक",
        "description": "Different but non-enemy yonis. Physical compatibility exists but may require more conscious effort.",
        "description_hindi": "योनि अलग है पर दुश्मन नहीं। शारीरिक संबंधों में थोड़ी मेहनत करनी होगी, पर सब ठीक रहेगा।",
        "effects": [
            "Workable physical relationship",
            "Communication important",
            "Understanding each other's needs",
            "Patience in intimate matters"
        ],
        "effects_hindi": [
            "शारीरिक संबंध चल जाएंगे",
            "खुलकर बात करना जरूरी है",
            "एक-दूसरे की जरूरतें समझनी होंगी",
            "धैर्य रखना होगा"
        ]
    },
    "poor": {
        "title": "Physical Incompatibility",
        "title_hindi": "शारीरिक मेल में कमी",
        "description": "Enemy yonis indicate potential challenges in physical compatibility. This requires understanding and patience from both partners.",
        "description_hindi": "योनि मेल में कमी है। शारीरिक संबंधों में थोड़ी दिक्कत हो सकती है। दोनों को मिलकर समझदारी से काम लेना होगा।",
        "effects": [
            "Physical differences exist",
            "May need counseling",
            "Extra effort in intimacy",
            "Focus on emotional bonding"
        ],
        "effects_hindi": [
            "शारीरिक तालमेल में फर्क है",
            "जरूरत पड़े तो counseling लें",
            "intimacy में extra effort लगेगी",
            "भावनात्मक जुड़ाव पर ध्यान दें"
        ]
    }
}

GRAHA_MAITRI_INTERPRETATIONS = {
    "excellent": {
        "title": "Excellent Mental Harmony",
        "title_hindi": "मानसिक मेल उत्तम",
        "description": "The lords of both Moon signs are friends or the same planet. This indicates excellent mental compatibility, understanding, and emotional resonance.",
        "description_hindi": "दोनों की राशियों के स्वामी ग्रह दोस्त हैं। इससे दोनों की सोच मिलती-जुलती होगी और एक-दूसरे को समझना बहुत आसान होगा।",
        "effects": [
            "Deep mental understanding",
            "Similar thought processes",
            "Easy communication",
            "Emotional synchronization"
        ],
        "effects_hindi": [
            "एक-दूसरे की सोच गहराई से समझेंगे",
            "सोचने का तरीका मिलता-जुलता होगा",
            "बातचीत आसान होगी",
            "भावनात्मक रूप से जुड़े रहेंगे"
        ]
    },
    "good": {
        "title": "Good Mental Compatibility",
        "title_hindi": "मानसिक मेल अच्छा",
        "description": "One lord is friendly while the other is neutral. Good mental compatibility with minor differences in thinking.",
        "description_hindi": "राशि स्वामियों में एक दोस्त है, एक neutral। मानसिक तालमेल अच्छा रहेगा, बस कभी-कभी सोच में थोड़ा फर्क हो सकता है।",
        "effects": [
            "Generally good understanding",
            "Some differences in approach",
            "Communication resolves issues",
            "Complementary perspectives"
        ],
        "effects_hindi": [
            "आमतौर पर समझ अच्छी रहेगी",
            "कभी-कभी approach में फर्क होगा",
            "बातचीत से सब सुलझ जाएगा",
            "एक-दूसरे की सोच पूरक होगी"
        ]
    },
    "average": {
        "title": "Average Mental Compatibility",
        "title_hindi": "मानसिक मेल ठीक-ठाक",
        "description": "Both lords are neutral to each other. Average mental compatibility requiring effort to understand each other.",
        "description_hindi": "दोनों के राशि स्वामी neutral हैं। एक-दूसरे को समझने में थोड़ी मेहनत लगेगी, पर समय के साथ बेहतर होगा।",
        "effects": [
            "Neutral mental connection",
            "Need to develop understanding",
            "Different mental approaches",
            "Growth possible over time"
        ],
        "effects_hindi": [
            "मानसिक जुड़ाव neutral है",
            "समझ विकसित करनी होगी",
            "सोचने का तरीका अलग है",
            "समय के साथ सुधार होगा"
        ]
    },
    "poor": {
        "title": "Mental Friction Likely",
        "title_hindi": "मानसिक मेल में कमी",
        "description": "The lords are enemies or have mixed relationships. This indicates potential misunderstandings and different mental wavelengths.",
        "description_hindi": "राशि स्वामी दुश्मन हैं। सोच में काफी फर्क हो सकता है और गलतफहमी की संभावना है। धैर्य और समझदारी से काम लें।",
        "effects": [
            "Different ways of thinking",
            "Misunderstandings possible",
            "Extra communication needed",
            "Patience and tolerance required"
        ],
        "effects_hindi": [
            "सोचने का तरीका अलग होगा",
            "गलतफहमी हो सकती है",
            "ज्यादा बातचीत करनी होगी",
            "धैर्य और सहनशीलता जरूरी है"
        ]
    }
}

GANA_INTERPRETATIONS = {
    "same_deva": {
        "title": "Divine Temperament Match",
        "title_hindi": "दोनों देव गण - बहुत शुभ",
        "description": "Both partners have Deva (divine) temperament. They share gentle, spiritual, and harmonious natures.",
        "description_hindi": "दोनों का गण देव है। दोनों शांत स्वभाव के हैं, धार्मिक और सौम्य। घर में शांति और सुख रहेगा।",
        "effects": [
            "Peaceful household",
            "Spiritual inclinations shared",
            "Gentle communication",
            "Harmonious family life"
        ],
        "effects_hindi": [
            "घर में शांति रहेगी",
            "दोनों धार्मिक और आध्यात्मिक होंगे",
            "बातचीत नरमी से होगी",
            "परिवार में खुशहाली रहेगी"
        ]
    },
    "same_manushya": {
        "title": "Human Temperament Match",
        "title_hindi": "दोनों मनुष्य गण - अच्छा",
        "description": "Both partners have Manushya (human) temperament. They share practical, balanced, and worldly approaches.",
        "description_hindi": "दोनों मनुष्य गण के हैं। दोनों practical और balanced हैं। जीवन को समझदारी से जीएंगे।",
        "effects": [
            "Practical approach to life",
            "Balanced decision-making",
            "Realistic expectations",
            "Stable family dynamics"
        ],
        "effects_hindi": [
            "जीवन के प्रति practical नजरिया",
            "फैसले संतुलित होंगे",
            "उम्मीदें हकीकत पर आधारित होंगी",
            "परिवार स्थिर रहेगा"
        ]
    },
    "same_rakshasa": {
        "title": "Rakshasa Temperament Match",
        "title_hindi": "दोनों राक्षस गण - चलेगा",
        "description": "Both partners have Rakshasa (intense) temperament. They share passionate, assertive, and strong personalities.",
        "description_hindi": "दोनों राक्षस गण के हैं। दोनों तेज स्वभाव के हैं और मजबूत personality वाले। एक-दूसरे को समझेंगे क्योंकि nature एक जैसा है।",
        "effects": [
            "Passionate relationship",
            "Strong personalities together",
            "Need for mutual respect",
            "Intense but understanding"
        ],
        "effects_hindi": [
            "रिश्ते में जोश और passion रहेगा",
            "दोनों की personality मजबूत है",
            "एक-दूसरे की इज्जत करना जरूरी है",
            "तेज स्वभाव पर समझ रहेगी"
        ]
    },
    "deva_manushya": {
        "title": "Compatible Temperaments",
        "title_hindi": "देव-मनुष्य गण - शुभ",
        "description": "Deva and Manushya temperaments combine well. The divine nature balances with practical human nature.",
        "description_hindi": "एक देव गण और एक मनुष्य गण - यह अच्छा मेल है। शांत और practical स्वभाव मिलकर अच्छा balance बनाते हैं।",
        "effects": [
            "Good balance of idealism and practicality",
            "Complementary natures",
            "Spiritual meets worldly",
            "Harmonious adjustment"
        ],
        "effects_hindi": [
            "आदर्श और व्यावहारिकता का अच्छा मेल",
            "एक-दूसरे को पूरा करने वाले स्वभाव",
            "आध्यात्मिक और दुनियादारी का संतुलन",
            "आपसी तालमेल अच्छा रहेगा"
        ]
    },
    "gana_dosha": {
        "title": "Temperament Clash - Gana Dosha",
        "title_hindi": "गण दोष - स्वभाव में टकराव",
        "description": "Incompatible temperaments (Deva-Rakshasa or Manushya-Rakshasa). This can lead to fundamental differences in approach to life.",
        "description_hindi": "गण मेल नहीं है। एक शांत और एक तेज स्वभाव का मेल मुश्किल हो सकता है। जीवन जीने के तरीके में फर्क होगा। उपाय करना जरूरी है।",
        "effects": [
            "Different life philosophies",
            "Potential for conflicts",
            "Need for tolerance",
            "Remedies recommended"
        ],
        "effects_hindi": [
            "जीवन जीने का नजरिया अलग होगा",
            "झगड़े और मतभेद हो सकते हैं",
            "सहनशीलता रखनी होगी",
            "उपाय करना बहुत जरूरी है"
        ]
    }
}

BHAKOOT_INTERPRETATIONS = {
    "excellent": {
        "title": "Favorable Rashi Relationship",
        "title_hindi": "भकूट शुभ - राशि मेल अच्छा",
        "description": "The Moon signs are in a favorable position. No Bhakoot dosha present, indicating good emotional and material compatibility.",
        "description_hindi": "दोनों की राशियों का मेल बहुत अच्छा है। भकूट दोष नहीं है। पैसों और भावनाओं दोनों में तालमेल अच्छा रहेगा।",
        "effects": [
            "Emotional harmony",
            "Financial prosperity",
            "Good family relations",
            "Mutual support"
        ],
        "effects_hindi": [
            "भावनात्मक तालमेल अच्छा रहेगा",
            "आर्थिक समृद्धि होगी",
            "परिवार में अच्छे संबंध रहेंगे",
            "एक-दूसरे का साथ मिलेगा"
        ]
    },
    "shadashtak": {
        "title": "Shadashtak Dosha (6/8 Position)",
        "title_hindi": "षडाष्टक दोष (6/8 स्थिति) - गंभीर",
        "description": "The most challenging Bhakoot combination. The 6/8 relationship can indicate conflicts, health issues, and separation tendencies.",
        "description_hindi": "यह सबसे कठिन भकूट दोष है। 6/8 की स्थिति में झगड़े, सेहत की समस्या और अलगाव का खतरा रहता है। उपाय जरूरी हैं।",
        "effects": [
            "Potential for conflicts",
            "Health concerns possible",
            "Financial disputes",
            "Extra caution needed"
        ],
        "effects_hindi": [
            "झगड़े की संभावना है",
            "सेहत की समस्या हो सकती है",
            "पैसों को लेकर विवाद हो सकता है",
            "बहुत सावधानी जरूरी है"
        ],
        "remedies": [
            "Worship Lord Shiva together",
            "Perform Rudrabhishek",
            "Donate to health causes",
            "Consult astrologer for specific remedies"
        ]
    },
    "dwi_dwadash": {
        "title": "Dwi-Dwadash Dosha (2/12 Position)",
        "title_hindi": "द्वि-द्वादश दोष (2/12 स्थिति)",
        "description": "This combination can affect finances and family harmony. The 2/12 position indicates potential financial struggles.",
        "description_hindi": "2/12 की स्थिति में पैसों और परिवार में तालमेल की समस्या हो सकती है। आर्थिक planning जरूरी है।",
        "effects": [
            "Financial challenges",
            "Different spending habits",
            "Family disputes possible",
            "Need for financial planning"
        ],
        "effects_hindi": [
            "पैसों की तंगी हो सकती है",
            "खर्च करने का तरीका अलग होगा",
            "परिवार में विवाद हो सकते हैं",
            "Financial planning जरूरी है"
        ],
        "remedies": [
            "Worship Goddess Lakshmi",
            "Donate food on Fridays",
            "Perform Lakshmi Puja together",
            "Maintain joint financial accounts"
        ]
    },
    "cancelled": {
        "title": "Bhakoot Dosha Cancelled",
        "title_hindi": "भकूट दोष समाप्त - शुभ",
        "description": "Though the positions indicate dosha, it is cancelled because the lords are friends or the same. The negative effects are neutralized.",
        "description_hindi": "भकूट दोष था पर cancel हो गया क्योंकि दोनों राशियों के स्वामी दोस्त हैं। अब कोई चिंता की बात नहीं है।",
        "effects": [
            "Dosha effects minimized",
            "Lords' friendship helps",
            "No major concerns",
            "Proceed with confidence"
        ],
        "effects_hindi": [
            "दोष का असर खत्म हो गया",
            "ग्रहों की मित्रता से लाभ",
            "कोई बड़ी चिंता नहीं",
            "विश्वास के साथ आगे बढ़ें"
        ]
    }
}

NADI_INTERPRETATIONS = {
    "different": {
        "title": "Healthy Genetic Compatibility",
        "title_hindi": "नाड़ी मेल उत्तम - स्वस्थ संतान",
        "description": "Different Nadis indicate good genetic compatibility. Children will be healthy and the couple will have vitality.",
        "description_hindi": "दोनों की नाड़ी अलग है जो बहुत शुभ है। बच्चे स्वस्थ होंगे और दोनों की सेहत भी अच्छी रहेगी। यह 8 अंक का पूरा लाभ देता है।",
        "effects": [
            "Healthy children likely",
            "Good physical vitality",
            "No genetic concerns",
            "Long and healthy life together"
        ],
        "effects_hindi": [
            "बच्चे स्वस्थ और तंदुरुस्त होंगे",
            "दोनों में ऊर्जा और जोश रहेगा",
            "genetic समस्या की कोई चिंता नहीं",
            "लंबी और स्वस्थ ज़िंदगी साथ में"
        ]
    },
    "same_aadi": {
        "title": "NADI DOSHA - Same Aadi (Vata) Nadi",
        "title_hindi": "नाड़ी दोष - दोनों आदि (वात) नाड़ी - गंभीर",
        "description": "Both partners have Aadi (Vata) Nadi. This is considered most serious for progeny and health.",
        "description_hindi": "दोनों की नाड़ी एक जैसी (आदि/वात) है। यह गंभीर नाड़ी दोष है। संतान और सेहत दोनों पर असर पड़ सकता है। उपाय करना बहुत जरूरी है।",
        "effects": [
            "Concerns for children's health",
            "Vata-related health issues",
            "Genetic incompatibility",
            "Remedies essential"
        ],
        "effects_hindi": [
            "बच्चों की सेहत पर असर पड़ सकता है",
            "वात संबंधी बीमारियां हो सकती हैं",
            "genetic मेल में कमी है",
            "उपाय करना अनिवार्य है"
        ],
        "remedies": [
            "Perform Nadi Dosha Nivaran Puja",
            "Donate gold to temple",
            "Worship Lord Vishnu",
            "Offer prayers at Nadi-related temples",
            "Consult qualified astrologer for specific rituals"
        ]
    },
    "same_madhya": {
        "title": "NADI DOSHA - Same Madhya (Pitta) Nadi",
        "title_hindi": "नाड़ी दोष - दोनों मध्य (पित्त) नाड़ी - गंभीर",
        "description": "Both partners have Madhya (Pitta) Nadi. This can affect progeny and may cause heat-related health issues.",
        "description_hindi": "दोनों की नाड़ी एक जैसी (मध्य/पित्त) है। संतान में दिक्कत हो सकती है और गर्मी से जुड़ी बीमारियां हो सकती हैं। उपाय करें।",
        "effects": [
            "Pitta-related health concerns",
            "Possible difficulties with children",
            "Inflammatory conditions possible",
            "Remedies needed"
        ],
        "effects_hindi": [
            "पित्त संबंधी स्वास्थ्य समस्याएं",
            "संतान में दिक्कत हो सकती है",
            "सूजन और गर्मी की बीमारियां संभव",
            "उपाय करना जरूरी है"
        ],
        "remedies": [
            "Worship Lord Shiva",
            "Perform Mahamrityunjaya Japa",
            "Donate silver to temple",
            "Offer milk to Shivalinga"
        ]
    },
    "same_antya": {
        "title": "NADI DOSHA - Same Antya (Kapha) Nadi",
        "title_hindi": "नाड़ी दोष - दोनों अंत्य (कफ) नाड़ी - गंभीर",
        "description": "Both partners have Antya (Kapha) Nadi. This can affect children and may cause Kapha-related health issues.",
        "description_hindi": "दोनों की नाड़ी एक जैसी (अंत्य/कफ) है। संतान और सेहत पर असर पड़ सकता है। कफ से जुड़ी बीमारियां हो सकती हैं।",
        "effects": [
            "Kapha-related health issues",
            "Possible fertility concerns",
            "Respiratory/weight issues",
            "Remedies important"
        ],
        "effects_hindi": [
            "कफ संबंधी बीमारियां हो सकती हैं",
            "संतान में दिक्कत हो सकती है",
            "सांस और वजन की समस्या संभव",
            "उपाय करना बहुत जरूरी है"
        ],
        "remedies": [
            "Worship Goddess Durga",
            "Perform Durga Saptashati Path",
            "Donate grains to poor",
            "Visit Navagraha temple"
        ]
    }
}


# =============================================================================
# DOSHA REMEDIES
# =============================================================================

MANGLIK_REMEDIES = {
    "general": [
        "कुंभ विवाह करें (असली शादी से पहले घड़े या पेड़ से विवाह) / Kumbh Vivah before marriage",
        "हनुमान जी की नियमित पूजा करें / Worship Lord Hanuman regularly",
        "रोज़ हनुमान चालीसा पढ़ें / Recite Hanuman Chalisa daily",
        "मंगलवार को व्रत रखें / Fast on Tuesdays",
        "मंगलवार को लाल चीज़ें दान करें (कपड़े, मसूर दाल) / Donate red items on Tuesdays",
        "ज्योतिषी से सलाह लेकर मूंगा (Coral) पहनें / Wear coral gemstone after consultation",
        "मंगल शांति पूजा करवाएं / Perform Mangal Shanti Puja"
    ],
    "both_manglik": [
        "दोनों मांगलिक हैं - दोष एक-दूसरे से कट जाता है / Both Manglik - doshas cancel each other",
        "शादी की सामान्य तैयारी जारी रखें / Continue normal marriage preparations",
        "वैकल्पिक: मंगल ग्रह को मजबूत करने के लिए साथ में पूजा करें / Optional: Joint Mars worship",
        "शादी के लिए शुभ मंगल का समय देखें / Consider auspicious Mars timing"
    ],
    "cancelled": [
        "मांगलिक दोष naturally निरस्त है / Manglik dosha naturally cancelled",
        "मंगल अच्छी स्थिति/राशि में है / Mars is in favorable position",
        "कोई उपाय जरूरी नहीं / No remedies needed",
        "विश्वास से शादी करें / Proceed with marriage confidently"
    ]
}

NADI_REMEDIES = {
    "standard": [
        "नाड़ी दोष निवारण पूजा करवाएं - योग्य पंडित से / Nadi Dosha Nivaran Puja by qualified priest",
        "महामृत्युंजय मंत्र जप (1.25 लाख बार) / Mahamrityunjaya Mantra Japa (1.25 lakh times)",
        "दुल्हन के वजन के बराबर सोना दान करें (symbolic amount चलेगा) / Donate gold (symbolic amount acceptable)",
        "राहु-केतु मंदिर में पूजा करें / Worship at Rahu-Ketu temple",
        "सर्प दोष पूजा करवाएं / Perform Sarpa Dosha Puja",
        "शुभ दिनों पर ब्राह्मणों को भोजन कराएं / Feed Brahmins on auspicious days",
        "त्र्यंबकेश्वर मंदिर जाएं नाड़ी शांति के लिए / Visit Trimbakeshwar temple for Nadi Shanti"
    ],
    "exceptions": [
        "अगर दोनों एक नक्षत्र में हैं पर अलग पद में - दोष कम है / Same nakshatra, different pada - dosha reduced",
        "अगर नक्षत्र स्वामी मित्र हैं - दोष कम है / If nakshatra lords are friends - dosha reduced",
        "पद-विशेष विश्लेषण के लिए ज्योतिषी से मिलें / Consult astrologer for pada-specific analysis"
    ]
}

BHAKOOT_REMEDIES = {
    "shadashtak": [
        "भगवान शिव का रुद्राभिषेक करवाएं / Rudrabhishek to Lord Shiva",
        "दोनों की चंद्र राशि के स्वामी की पूजा करें / Worship both Moon sign lords",
        "नवग्रह शांति पूजा करवाएं / Perform Navagraha Shanti",
        "साथ मिलकर दान करें / Donate to charity together",
        "ज्योतिर्लिंग मंदिरों के दर्शन करें / Visit Jyotirlinga temples"
    ],
    "dwi_dwadash": [
        "शुक्रवार को लक्ष्मी पूजा करें / Lakshmi Puja on Fridays",
        "भोजन और कपड़े दान करें / Donate food and clothes",
        "माता लक्ष्मी की पूजा करें / Worship Goddess Lakshmi",
        "श्री सूक्त पाठ करें / Perform Shri Sukta Path",
        "पैसों के मामले में पारदर्शिता रखें / Maintain financial transparency"
    ]
}

GANA_REMEDIES = {
    "standard": [
        "गण दोष शांति पूजा करवाएं / Perform Gana Dosha Shanti Puja",
        "कुल देवता की पूजा करें / Worship family deity (Kul Devta)",
        "साथ में गायत्री मंत्र का जाप करें / Recite Gayatri Mantra together",
        "साथ तीर्थ यात्रा पर जाएं / Visit pilgrimage sites together",
        "सहनशीलता और समझदारी रखें / Practice tolerance and understanding"
    ]
}


# =============================================================================
# MARRIAGE TIMING SUGGESTIONS
# =============================================================================

def get_marriage_timing_suggestions(
    boy_moon_rashi: int,
    girl_moon_rashi: int,
    total_score: float
) -> Dict[str, Any]:
    """
    Provide marriage timing suggestions based on compatibility score and Rashis.

    Returns:
        Dictionary with timing suggestions
    """
    suggestions = {
        "favorable_days": [],
        "favorable_months": [],
        "avoid": [],
        "general_advice": []
    }

    # Based on score
    if total_score >= 25:
        suggestions["general_advice"].append(
            "मिलान अच्छा है। जब भी शुभ मुहूर्त मिले, शादी कर सकते हैं। / Good compatibility - marry when muhurta is favorable."
        )
    elif total_score >= 18:
        suggestions["general_advice"].append(
            "गुरु (Jupiter) का चंद्र राशि पर शुभ गोचर का इंतज़ार करें। / Wait for Jupiter's favorable transit over Moon signs."
        )
        suggestions["general_advice"].append(
            "दशा के आधार पर समय के लिए योग्य ज्योतिषी से मिलें। / Consult astrologer for Dasha-based timing."
        )
    else:
        suggestions["general_advice"].append(
            "शादी से पहले उपाय करना जरूरी है। / Extensive remedies recommended before marriage."
        )
        suggestions["general_advice"].append(
            "शुक्र और गुरु के मजबूत गोचर का इंतज़ार करें। / Wait for Venus and Jupiter to be strong in transit."
        )

    # Favorable days based on Moon signs
    boy_lord = RASHI_LORDS[boy_moon_rashi]
    girl_lord = RASHI_LORDS[girl_moon_rashi]

    day_mapping = {
        "SUN": "रविवार / Sunday",
        "MOON": "सोमवार / Monday",
        "MARS": "मंगलवार / Tuesday",
        "MERCURY": "बुधवार / Wednesday",
        "JUPITER": "गुरुवार / Thursday",
        "VENUS": "शुक्रवार / Friday",
        "SATURN": "शनिवार / Saturday"
    }

    if boy_lord in day_mapping:
        suggestions["favorable_days"].append(day_mapping[boy_lord])
    if girl_lord in day_mapping and girl_lord != boy_lord:
        suggestions["favorable_days"].append(day_mapping[girl_lord])

    # Always add Thursday and Friday for marriage
    thursday_hindi = "गुरुवार (बृहस्पति का दिन) / Thursday (Jupiter's day)"
    friday_hindi = "शुक्रवार (शुक्र का दिन) / Friday (Venus's day)"

    has_thursday = any("Thursday" in d or "गुरुवार" in d for d in suggestions["favorable_days"])
    has_friday = any("Friday" in d or "शुक्रवार" in d for d in suggestions["favorable_days"])

    if not has_thursday:
        suggestions["favorable_days"].append(thursday_hindi)
    if not has_friday:
        suggestions["favorable_days"].append(friday_hindi)

    # Favorable months (Hindu calendar)
    suggestions["favorable_months"] = [
        "माघ (जनवरी-फरवरी) / Magha (Jan-Feb)",
        "फाल्गुन (फरवरी-मार्च) / Phalguna (Feb-Mar)",
        "वैशाख (अप्रैल-मई) / Vaishakha (Apr-May)",
        "ज्येष्ठ (मई-जून) / Jyeshtha (May-Jun)",
        "मार्गशीर्ष (नवंबर-दिसंबर) / Margashirsha (Nov-Dec)"
    ]

    suggestions["avoid"] = [
        "आषाढ़ मास (जून-जुलाई) - सिर्फ emergency में / Ashada month - except emergency",
        "भाद्रपद मास (अगस्त-सितंबर) - टालें / Bhadrapada month - avoid",
        "पितृ पक्ष का समय / Pitru Paksha period",
        "ग्रहण और आस-पास के दिन / Eclipses and surrounding days",
        "अमावस्या (नई चंद्रमा) / Amavasya (New Moon)",
        "रिक्ता तिथियां (4, 9, 14) / Rikta Tithis (4th, 9th, 14th)"
    ]

    return suggestions


# =============================================================================
# COMPREHENSIVE PREDICTION GENERATOR
# =============================================================================

@dataclass
class MatchingPrediction:
    """Complete matching prediction with interpretations."""
    overall_summary: str
    compatibility_level: str  # Excellent, Good, Average, Below Average, Poor
    koota_interpretations: List[Dict[str, Any]]
    dosha_analysis: List[Dict[str, Any]]
    remedies: List[str]
    marriage_timing: Dict[str, Any]
    areas_of_strength: List[str]
    areas_of_concern: List[str]
    final_recommendation: str


def generate_matching_predictions(
    matching_result: MatchingResult
) -> MatchingPrediction:
    """
    Generate comprehensive predictions from matching result.

    Args:
        matching_result: MatchingResult from KundaliMatcher

    Returns:
        MatchingPrediction with detailed interpretations
    """
    percentage = matching_result.percentage
    total = matching_result.total_points

    # Determine compatibility level
    if percentage >= 80:
        compatibility_level = "Excellent"
    elif percentage >= 60:
        compatibility_level = "Good"
    elif percentage >= 50:
        compatibility_level = "Average"
    elif percentage >= 36:
        compatibility_level = "Below Average"
    else:
        compatibility_level = "Poor"

    # Generate overall summary
    overall_summary = _generate_overall_summary(matching_result, compatibility_level)

    # Generate koota interpretations
    koota_interpretations = []
    for koota in matching_result.koota_results:
        interpretation = _get_koota_interpretation(koota)
        koota_interpretations.append(interpretation)

    # Analyze doshas
    dosha_analysis = []
    all_remedies = []

    for dosha in matching_result.doshas:
        analysis = _analyze_dosha(dosha)
        dosha_analysis.append(analysis)
        all_remedies.extend(analysis.get("remedies", []))

    # Get marriage timing
    detailed = matching_result.detailed_analysis
    boy_rashi = list(RASHIS.keys())[
        list(r["name"] for r in RASHIS.values()).index(detailed.get("boy_moon_sign", "Mesha"))
    ] if "boy_moon_sign" in detailed else 0
    girl_rashi = list(RASHIS.keys())[
        list(r["name"] for r in RASHIS.values()).index(detailed.get("girl_moon_sign", "Mesha"))
    ] if "girl_moon_sign" in detailed else 0

    marriage_timing = get_marriage_timing_suggestions(boy_rashi, girl_rashi, total)

    # Koota Hindi descriptions for strengths/concerns
    koota_hindi_desc = {
        "Varna": "वर्ण - आध्यात्मिक स्तर और सामाजिक मेल",
        "Vashya": "वश्य - आपसी आकर्षण और नियंत्रण",
        "Tara": "तारा - भाग्य और स्वास्थ्य",
        "Yoni": "योनि - शारीरिक और यौन अनुकूलता",
        "Graha Maitri": "ग्रह मैत्री - मानसिक और भावनात्मक मेल",
        "Gana": "गण - स्वभाव और व्यवहार",
        "Bhakoot": "भकूट - प्रेम, स्वास्थ्य और आर्थिक स्थिति",
        "Nadi": "नाड़ी - स्वास्थ्य और संतान"
    }

    # Identify strengths and concerns
    areas_of_strength = []
    areas_of_concern = []

    for koota in matching_result.koota_results:
        percentage_of_max = (koota.obtained_points / koota.max_points) * 100
        hindi_desc = koota_hindi_desc.get(koota.name, koota.name_hindi)
        if percentage_of_max >= 75:
            areas_of_strength.append(f"✓ {hindi_desc} - अच्छा / {koota.name}: Good - {koota.description}")
        elif percentage_of_max < 50:
            areas_of_concern.append(f"⚠ {hindi_desc} - ध्यान दें / {koota.name}: Needs attention - {koota.description}")

    # Final recommendation
    final_recommendation = _generate_final_recommendation(
        matching_result, compatibility_level, dosha_analysis
    )

    return MatchingPrediction(
        overall_summary=overall_summary,
        compatibility_level=compatibility_level,
        koota_interpretations=koota_interpretations,
        dosha_analysis=dosha_analysis,
        remedies=list(set(all_remedies)),  # Remove duplicates
        marriage_timing=marriage_timing,
        areas_of_strength=areas_of_strength,
        areas_of_concern=areas_of_concern,
        final_recommendation=final_recommendation
    )


def _generate_overall_summary(
    result: MatchingResult, level: str
) -> str:
    """Generate overall summary text in Hindi/Hinglish."""
    summaries = {
        "Excellent": f"""
{result.boy_name} और {result.girl_name} की कुंडली मिलान उत्तम है!
कुल {result.total_points}/36 गुण ({result.percentage}%) मिले हैं।

यह एक बहुत अच्छा मिलान है। ज्यादातर factors में अच्छी compatibility है।
इस शादी में खुशहाली, समृद्धि और शांति के योग हैं। 🙏

Excellent compatibility with strong alignment across most factors.
Marriage is blessed with potential for happiness and harmony.
""",
        "Good": f"""
{result.boy_name} और {result.girl_name} की कुंडली मिलान अच्छी है।
कुल {result.total_points}/36 गुण ({result.percentage}%) मिले हैं।

यह एक अच्छा मिलान है जिसमें मजबूत नींव है। कुछ जगह थोड़ा adjustment लग सकता है,
पर overall शादी की सफलता के अच्छे chances हैं।

Good compatibility with solid foundations. Marriage has good potential for success.
""",
        "Average": f"""
{result.boy_name} और {result.girl_name} की कुंडली मिलान औसत है।
कुल {result.total_points}/36 गुण ({result.percentage}%) मिले हैं।

इस मिलान में कुछ अच्छी बातें हैं और कुछ जगह ध्यान देने की जरूरत है।
आपसी समझ, धैर्य और कुछ उपायों से शादी अच्छी चल सकती है।

Average match with both strengths and areas needing attention.
With understanding and patience, marriage can work well.
""",
        "Below Average": f"""
{result.boy_name} और {result.girl_name} की कुंडली मिलान औसत से कम है।
कुल {result.total_points}/36 गुण ({result.percentage}%) मिले हैं।

कई क्षेत्रों में सावधानी बरतने की जरूरत है। शादी हो सकती है पर उपाय करना जरूरी है।
किसी अनुभवी ज्योतिषी से सलाह लेना उचित होगा।

Below average compatibility. Marriage possible but remedies recommended.
Consider consulting an experienced astrologer.
""",
        "Poor": f"""
{result.boy_name} और {result.girl_name} की कुंडली मिलान में चुनौतियां हैं।
कुल {result.total_points}/36 गुण ({result.percentage}%) मिले हैं।

कई महत्वपूर्ण अंतर हैं जो वैवाहिक जीवन में कठिनाई पैदा कर सकते हैं।
अगर शादी करनी है तो बहुत सारे उपाय और दोनों की लगातार मेहनत जरूरी है।
योग्य ज्योतिषी से परामर्श अवश्य लें।

Challenging compatibility. Extensive remedies needed if proceeding.
Professional astrological consultation strongly advised.
"""
    }

    return summaries.get(level, summaries["Average"]).strip()


def _get_koota_interpretation(koota: KootaResult) -> Dict[str, Any]:
    """Get detailed interpretation for a koota."""
    interpretation = {
        "name": koota.name,
        "name_hindi": koota.name_hindi,
        "score": f"{koota.obtained_points}/{koota.max_points}",
        "percentage": round((koota.obtained_points / koota.max_points) * 100, 1),
        "boy_value": koota.boy_value,
        "girl_value": koota.girl_value,
        "is_favorable": koota.is_auspicious,
        "description": koota.description,
        "detailed_interpretation": "",
        "effects": [],
        "dosha": koota.dosha
    }

    # Get specific interpretation based on koota type and score
    if koota.name == "Varna":
        key = "full" if koota.is_auspicious else "none"
        interp = VARNA_INTERPRETATIONS[key]
    elif koota.name == "Vashya":
        if koota.obtained_points >= 1.5:
            key = "excellent"
        elif koota.obtained_points >= 0.5:
            key = "good"
        else:
            key = "poor"
        interp = VASHYA_INTERPRETATIONS[key]
    elif koota.name == "Tara":
        if koota.obtained_points >= 3:
            key = "auspicious"
        elif koota.obtained_points >= 1.5:
            key = "neutral"
        else:
            key = "inauspicious"
        interp = TARA_INTERPRETATIONS[key]
    elif koota.name == "Yoni":
        if koota.obtained_points >= 4:
            key = "excellent"
        elif koota.obtained_points >= 3:
            key = "good"
        elif koota.obtained_points >= 2:
            key = "moderate"
        else:
            key = "poor"
        interp = YONI_INTERPRETATIONS[key]
    elif koota.name == "Graha Maitri":
        if koota.obtained_points >= 5:
            key = "excellent"
        elif koota.obtained_points >= 4:
            key = "good"
        elif koota.obtained_points >= 3:
            key = "average"
        else:
            key = "poor"
        interp = GRAHA_MAITRI_INTERPRETATIONS[key]
    elif koota.name == "Gana":
        if koota.dosha:
            key = "gana_dosha"
        elif koota.boy_value == koota.girl_value:
            if koota.boy_value == "Deva":
                key = "same_deva"
            elif koota.boy_value == "Manushya":
                key = "same_manushya"
            else:
                key = "same_rakshasa"
        else:
            key = "deva_manushya"
        interp = GANA_INTERPRETATIONS[key]
    elif koota.name == "Bhakoot":
        if koota.dosha == "Shadashtak":
            key = "shadashtak"
        elif koota.dosha == "Dwi-Dwadash":
            key = "dwi_dwadash"
        elif "cancelled" in koota.description.lower():
            key = "cancelled"
        else:
            key = "excellent"
        interp = BHAKOOT_INTERPRETATIONS[key]
    elif koota.name == "Nadi":
        if koota.dosha:
            # Determine which Nadi
            if "Aadi" in koota.boy_value:
                key = "same_aadi"
            elif "Madhya" in koota.boy_value:
                key = "same_madhya"
            else:
                key = "same_antya"
        else:
            key = "different"
        interp = NADI_INTERPRETATIONS[key]
    else:
        interp = {"title": "", "description": "", "effects": []}

    interpretation["detailed_interpretation"] = interp.get("description", "")
    interpretation["effects"] = interp.get("effects", [])
    interpretation["title"] = interp.get("title", "")

    # Add Hindi translations
    interpretation["title_hindi"] = interp.get("title_hindi", "")
    interpretation["detailed_interpretation_hindi"] = interp.get("description_hindi", "")
    interpretation["effects_hindi"] = interp.get("effects_hindi", [])

    if "remedies" in interp:
        interpretation["remedies"] = interp["remedies"]

    return interpretation


def _analyze_dosha(dosha: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze a dosha and provide remedies."""
    analysis = {
        "name": dosha["name"],
        "type": dosha["type"],
        "severity": dosha["severity"],
        "description": dosha["description"],
        "remedies": [],
        "is_cancelled": dosha["severity"] in ["Cancelled", "Cancelled/Reduced"]
    }

    if "Nadi" in dosha["type"]:
        analysis["remedies"] = NADI_REMEDIES["standard"]
        analysis["exceptions"] = NADI_REMEDIES["exceptions"]
    elif "Bhakoot" in dosha["type"]:
        if "Shadashtak" in dosha["name"] or "6/8" in dosha.get("description", ""):
            analysis["remedies"] = BHAKOOT_REMEDIES["shadashtak"]
        else:
            analysis["remedies"] = BHAKOOT_REMEDIES["dwi_dwadash"]
    elif "Manglik" in dosha["type"]:
        if dosha["severity"] == "Cancelled":
            analysis["remedies"] = MANGLIK_REMEDIES["both_manglik"]
        elif dosha.get("cancellation"):
            analysis["remedies"] = MANGLIK_REMEDIES["cancelled"]
        else:
            analysis["remedies"] = MANGLIK_REMEDIES["general"]
    elif "Gana" in dosha["type"]:
        analysis["remedies"] = GANA_REMEDIES["standard"]

    return analysis


def _generate_final_recommendation(
    result: MatchingResult,
    level: str,
    dosha_analysis: List[Dict]
) -> str:
    """Generate final recommendation text."""
    # Check for serious doshas
    has_serious_dosha = any(
        d["severity"] in ["Critical", "High"] and not d["is_cancelled"]
        for d in dosha_analysis
    )

    recommendations = {
        "Excellent": """
सिफारिश: शादी के लिए बहुत शुभ / HIGHLY FAVORABLE FOR MARRIAGE

यह एक उत्तम मिलान है! सभी प्रमुख factors में अच्छी compatibility है।
स्वभाव, शारीरिक अनुकूलता, मानसिक तालमेल और स्वास्थ्य सभी में अच्छा मेल है।
विश्वास के साथ शादी कर सकते हैं। 🙏

सुझाव / Suggested Actions:
• शादी के लिए शुभ मुहूर्त चुनें
• परंपरा के अनुसार शादी से पहले की रस्में करें
• बड़ों का आशीर्वाद लेकर वैवाहिक जीवन शुरू करें
""",
        "Good": """
सिफारिश: शादी के लिए अनुकूल / FAVORABLE FOR MARRIAGE

यह एक अच्छा मिलान है जिसमें मजबूत नींव है। कुछ छोटी बातों पर ध्यान देना पड़ सकता है,
पर कोई बड़ी बाधा नहीं है। शादी की सलाह दी जाती है।

सुझाव / Suggested Actions:
• जहां 50% से कम score है वहां उपाय करें
• शुभ मुहूर्त चुनें
• जहां फर्क है वहां बातचीत पर ध्यान दें
• शादी की तैयारी करें
""",
        "Average": """
सिफारिश: समझदारी से शादी हो सकती है / MARRIAGE POSSIBLE WITH AWARENESS

इस मिलान में कुछ अच्छी बातें हैं और कुछ जगह ध्यान देने की जरूरत है।
आपसी समझ, धैर्य और सही उपायों से शादी सफल हो सकती है।

सुझाव / Suggested Actions:
• शादी से पहले सुझाए गए उपाय करें
• ज्योतिषी से विशेष मार्गदर्शन लें
• कमजोर क्षेत्रों में बातचीत से सुधार लाएं
• विशेष रूप से शुभ मुहूर्त चुनें
""",
        "Below Average": """
सिफारिश: सावधानी से आगे बढ़ें / PROCEED WITH CAUTION

इस मिलान में कई क्षेत्रों में चिंता है। शादी हो सकती है पर ध्यान से सोचें और उपाय करें।

सुझाव / Suggested Actions:
• सभी सुझाए गए उपाय करें
• अनुभवी ज्योतिषी से मिलें
• रिश्ते की अन्य ताकतों पर विचार करें (प्यार, समझ, परिवार का साथ)
• दोनों partners को संभावित चुनौतियों का पता हो
• सबसे अच्छा मुहूर्त चुनें
""",
        "Poor": """
सिफारिश: बहुत सारे उपाय जरूरी / EXTENSIVE REMEDIES REQUIRED

इस मिलान में काफी compatibility चुनौतियां हैं। अगर शादी करनी है तो बहुत सारे उपाय
और दोनों की लगातार मेहनत जरूरी है।

सुझाव / Suggested Actions:
• कई अनुभवी ज्योतिषियों से सलाह लें
• सभी उपाय पूरी तरह से करें
• ज्योतिष के अलावा compatibility पर भी विचार करें
• दोनों की मजबूत प्रतिबद्धता जरूरी है
• कुल देवता और आध्यात्मिक गुरुओं का आशीर्वाद लें
"""
    }

    base_recommendation = recommendations.get(level, recommendations["Average"])

    # Add dosha-specific warnings
    if has_serious_dosha:
        base_recommendation += """

⚠️ महत्वपूर्ण: गंभीर दोष पाया गया है। शादी से पहले सभी विशेष उपाय अवश्य करें।
योग्य वैदिक ज्योतिषी से व्यक्तिगत मार्गदर्शन लें।

IMPORTANT: Serious dosha detected. Ensure all remedies are performed.
Consult a qualified Vedic astrologer for personalized guidance.
"""

    return base_recommendation.strip()


# =============================================================================
# HTML REPORT GENERATOR
# =============================================================================

def generate_matching_html(
    result: MatchingResult,
    predictions: MatchingPrediction
) -> str:
    """
    Generate HTML report for matching results.

    Args:
        result: MatchingResult from KundaliMatcher
        predictions: MatchingPrediction with interpretations

    Returns:
        HTML string for display
    """
    # Determine color based on compatibility
    if result.percentage >= 70:
        score_color = "#22c55e"  # Green
        bg_gradient = "from-green-500 to-emerald-500"
    elif result.percentage >= 50:
        score_color = "#f59e0b"  # Amber
        bg_gradient = "from-amber-500 to-orange-500"
    else:
        score_color = "#ef4444"  # Red
        bg_gradient = "from-red-500 to-rose-500"

    html = f"""
    <div class="matching-report bg-white rounded-xl shadow-lg overflow-hidden">
        <!-- Header -->
        <div class="bg-gradient-to-r {bg_gradient} text-white p-6 text-center">
            <h1 class="text-2xl font-bold mb-2">Kundali Milan Report</h1>
            <p class="text-white/90">Marriage Compatibility Analysis</p>
        </div>

        <!-- Names Section -->
        <div class="p-6 bg-orange-50 border-b">
            <div class="flex justify-around items-center">
                <div class="text-center">
                    <div class="text-3xl mb-2">👤</div>
                    <div class="font-bold text-lg">{result.boy_name}</div>
                    <div class="text-sm text-gray-600">{result.detailed_analysis.get('boy_moon_sign', 'N/A')}</div>
                    <div class="text-xs text-gray-500">{result.detailed_analysis.get('boy_nakshatra', 'N/A')}</div>
                </div>
                <div class="text-4xl text-red-500">❤️</div>
                <div class="text-center">
                    <div class="text-3xl mb-2">👤</div>
                    <div class="font-bold text-lg">{result.girl_name}</div>
                    <div class="text-sm text-gray-600">{result.detailed_analysis.get('girl_moon_sign', 'N/A')}</div>
                    <div class="text-xs text-gray-500">{result.detailed_analysis.get('girl_nakshatra', 'N/A')}</div>
                </div>
            </div>
        </div>

        <!-- Score Section -->
        <div class="p-6 text-center border-b">
            <div class="relative inline-block">
                <svg class="w-32 h-32" viewBox="0 0 36 36">
                    <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                          fill="none" stroke="#e5e7eb" stroke-width="3"/>
                    <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                          fill="none" stroke="{score_color}" stroke-width="3"
                          stroke-dasharray="{result.percentage}, 100"/>
                </svg>
                <div class="absolute inset-0 flex items-center justify-center">
                    <div>
                        <div class="text-2xl font-bold" style="color: {score_color}">{result.total_points}/36</div>
                        <div class="text-sm text-gray-500">{result.percentage}%</div>
                    </div>
                </div>
            </div>
            <div class="mt-4">
                <span class="px-4 py-2 rounded-full text-white font-medium" style="background-color: {score_color}">
                    {predictions.compatibility_level} Match
                </span>
            </div>
        </div>

        <!-- Koota Results Table -->
        <div class="p-6 border-b">
            <h2 class="text-xl font-bold mb-4 text-gray-800">Ashtakoot Milan (8 Factors)</h2>
            <div class="overflow-x-auto">
                <table class="w-full text-sm">
                    <thead class="bg-gray-100">
                        <tr>
                            <th class="px-4 py-3 text-left">Koota</th>
                            <th class="px-4 py-3 text-center">Points</th>
                            <th class="px-4 py-3 text-left">Boy</th>
                            <th class="px-4 py-3 text-left">Girl</th>
                            <th class="px-4 py-3 text-left">Result</th>
                        </tr>
                    </thead>
                    <tbody>
    """

    for koota in result.koota_results:
        row_color = "#dcfce7" if koota.is_auspicious else "#fef2f2"
        status_icon = "✓" if koota.is_auspicious else "✗"
        status_color = "#22c55e" if koota.is_auspicious else "#ef4444"

        html += f"""
                        <tr style="background-color: {row_color}">
                            <td class="px-4 py-3">
                                <div class="font-medium">{koota.name}</div>
                                <div class="text-xs text-gray-500">{koota.name_hindi}</div>
                            </td>
                            <td class="px-4 py-3 text-center font-bold">{koota.obtained_points}/{koota.max_points}</td>
                            <td class="px-4 py-3">{koota.boy_value}</td>
                            <td class="px-4 py-3">{koota.girl_value}</td>
                            <td class="px-4 py-3">
                                <span style="color: {status_color}" class="font-bold">{status_icon}</span>
                                <span class="text-xs ml-1">{koota.description[:50]}...</span>
                            </td>
                        </tr>
        """

    html += """
                    </tbody>
                </table>
            </div>
        </div>
    """

    # Doshas Section
    if result.doshas:
        html += """
        <div class="p-6 border-b bg-red-50">
            <h2 class="text-xl font-bold mb-4 text-red-800">Doshas Detected</h2>
        """
        for dosha in result.doshas:
            severity_colors = {
                "Critical": "#dc2626",
                "High": "#ea580c",
                "Moderate": "#d97706",
                "Cancelled": "#22c55e",
                "Cancelled/Reduced": "#22c55e"
            }
            color = severity_colors.get(dosha["severity"], "#d97706")

            html += f"""
            <div class="mb-4 p-4 bg-white rounded-lg shadow">
                <div class="flex items-center justify-between mb-2">
                    <span class="font-bold text-gray-800">{dosha["name"]}</span>
                    <span class="px-2 py-1 rounded text-white text-sm" style="background-color: {color}">
                        {dosha["severity"]}
                    </span>
                </div>
                <p class="text-sm text-gray-600">{dosha["description"]}</p>
            </div>
            """
        html += "</div>"

    # Remedies Section
    if predictions.remedies:
        html += """
        <div class="p-6 border-b">
            <h2 class="text-xl font-bold mb-4 text-gray-800">Recommended Remedies</h2>
            <ul class="space-y-2">
        """
        for remedy in predictions.remedies[:10]:  # Limit to 10 remedies
            html += f"""
                <li class="flex items-start gap-2">
                    <span class="text-orange-500 mt-1">🙏</span>
                    <span class="text-gray-700">{remedy}</span>
                </li>
            """
        html += """
            </ul>
        </div>
        """

    # Recommendation Section
    html += f"""
        <div class="p-6 bg-gradient-to-r from-orange-100 to-yellow-100">
            <h2 class="text-xl font-bold mb-4 text-gray-800">Final Recommendation</h2>
            <div class="whitespace-pre-line text-gray-700">{predictions.final_recommendation}</div>
        </div>

        <!-- Footer -->
        <div class="p-4 bg-gray-100 text-center text-xs text-gray-500">
            <p>Based on Brihat Parashara Hora Shastra • Muhurta Chintamani • Jataka Parijata</p>
            <p class="mt-1">This report is for guidance only. Please consult a qualified astrologer for important decisions.</p>
        </div>
    </div>
    """

    return html
