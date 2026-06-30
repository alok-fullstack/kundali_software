"""
Bindu-Specific Prediction Templates for Ashtakavarga-Based Rashifal

Predictions vary based on Ashtakavarga bindu count:
- Loha (Iron): 0-2 bindus - Very challenging
- Tamra (Copper): 3 bindus - Mixed/Moderate
- Rajata (Silver): 4 bindus - Good
- Swarna (Gold): 5-8 bindus - Excellent

Per BPHS: Bindu count determines the strength of transit effects.

Author: Claude Code Assistant
Date: 2026-06-28
"""

from typing import Dict, List


# =============================================================================
# OVERALL PREDICTIONS BY BINDU RANGE
# =============================================================================

OVERALL_BINDU_PREDICTIONS = {
    "loha": [  # 0-2 bindus - Very Challenging
        "यह समय चुनौतीपूर्ण है। धैर्य और संयम से काम लें।",
        "ग्रहों की स्थिति कमजोर है। बड़े फैसले टालें।",
        "इस अवधि में सावधानी आवश्यक है। उपाय करें।",
        "कठिन समय है। आध्यात्मिक उपायों से लाभ होगा।",
    ],
    "tamra": [  # 3 bindus - Mixed
        "मिश्रित परिणामों का समय है। संतुलन बनाए रखें।",
        "कुछ चुनौतियां रहेंगी पर निराश न हों।",
        "धैर्य रखें, स्थिति धीरे-धीरे सुधरेगी।",
        "मध्यम अनुकूल समय। प्रयास जारी रखें।",
    ],
    "rajata": [  # 4 bindus - Good
        "अच्छा समय है। आपके प्रयास सफल होंगे।",
        "ग्रहों की स्थिति अनुकूल है। अवसरों का लाभ उठाएं।",
        "शुभ समय। नए कार्य आरंभ कर सकते हैं।",
        "सकारात्मक परिणामों की संभावना है।",
    ],
    "swarna": [  # 5+ bindus - Excellent
        "उत्कृष्ट समय! ग्रहों का पूर्ण आशीर्वाद है।",
        "अत्यंत शुभ अवधि। सभी कार्यों में सफलता मिलेगी।",
        "भाग्योदय का समय। बड़े लक्ष्य प्राप्त होंगे।",
        "स्वर्णिम अवसर। इस समय का पूर्ण लाभ उठाएं।",
    ],
}


# =============================================================================
# CATEGORY-WISE PREDICTIONS BY BINDU LEVEL
# =============================================================================

CAREER_BINDU_PREDICTIONS = {
    "loha": [
        "करियर में कठिन समय। बड़े फैसले टालें।",
        "व्यापार में सावधानी रखें। नए निवेश से बचें।",
        "कार्यस्थल पर चुनौतियां रहेंगी। धैर्य रखें।",
        "पदोन्नति में विलंब संभव। समय का इंतजार करें।",
    ],
    "tamra": [
        "करियर में मिश्रित परिणाम। धैर्य रखें।",
        "कुछ बाधाएं आ सकती हैं पर प्रयास जारी रखें।",
        "व्यापार में सामान्य प्रगति होगी।",
        "कार्यस्थल पर स्थिरता रहेगी।",
    ],
    "rajata": [
        "करियर में अच्छी प्रगति। अवसर मिलेंगे।",
        "व्यापार में लाभ के योग हैं।",
        "नौकरी में मान-सम्मान बढ़ेगा।",
        "नए प्रोजेक्ट सफल होंगे।",
    ],
    "swarna": [
        "करियर में उत्कृष्ट समय। सफलता निश्चित।",
        "पदोन्नति और वेतन वृद्धि के प्रबल योग।",
        "व्यापार में अप्रत्याशित लाभ होगा।",
        "नेतृत्व के अवसर मिलेंगे।",
    ],
}

FINANCE_BINDU_PREDICTIONS = {
    "loha": [
        "आर्थिक मामलों में सतर्क रहें। अनावश्यक खर्च टालें।",
        "निवेश में हानि की संभावना। नया निवेश न करें।",
        "कर्ज लेने से बचें। बचत पर ध्यान दें।",
        "आकस्मिक व्यय हो सकते हैं। तैयार रहें।",
    ],
    "tamra": [
        "आर्थिक स्थिति सामान्य रहेगी।",
        "आय-व्यय में संतुलन बनाए रखें।",
        "छोटे निवेश ठीक रहेंगे। बड़े निवेश टालें।",
        "बजट बनाकर चलें।",
    ],
    "rajata": [
        "आर्थिक स्थिति मजबूत रहेगी।",
        "निवेश से अच्छा रिटर्न मिलेगा।",
        "आय में वृद्धि के योग हैं।",
        "पुराने बकाया वसूल हो सकते हैं।",
    ],
    "swarna": [
        "धन लाभ के उत्तम योग। समृद्धि बढ़ेगी।",
        "अप्रत्याशित आय की संभावना।",
        "निवेश में उत्कृष्ट रिटर्न मिलेगा।",
        "संपत्ति खरीदने का शुभ समय।",
    ],
}

HEALTH_BINDU_PREDICTIONS = {
    "loha": [
        "स्वास्थ्य पर विशेष ध्यान दें। नियमित जांच कराएं।",
        "पुरानी बीमारी उभर सकती है। सावधान रहें।",
        "तनाव से बचें। पर्याप्त आराम लें।",
        "खान-पान में संयम रखें।",
    ],
    "tamra": [
        "स्वास्थ्य सामान्य रहेगा। सतर्कता जरूरी।",
        "छोटी-मोटी समस्याएं हो सकती हैं।",
        "नियमित व्यायाम करें।",
        "मौसमी बीमारियों से बचें।",
    ],
    "rajata": [
        "स्वास्थ्य अच्छा रहेगा। ऊर्जा बनी रहेगी।",
        "पुरानी समस्याओं में सुधार होगा।",
        "मानसिक शांति रहेगी।",
        "फिटनेस में सुधार होगा।",
    ],
    "swarna": [
        "उत्तम स्वास्थ्य। ऊर्जा और जोश रहेगा।",
        "रोगों से मुक्ति मिलेगी।",
        "मानसिक और शारीरिक संतुलन बेहतर होगा।",
        "नई स्वास्थ्य आदतें सफल होंगी।",
    ],
}

RELATIONSHIP_BINDU_PREDICTIONS = {
    "loha": [
        "संबंधों में तनाव संभव। संयम रखें।",
        "गलतफहमियां हो सकती हैं। संवाद बनाए रखें।",
        "जीवनसाथी के स्वास्थ्य पर ध्यान दें।",
        "विवाद से बचें। शांति बनाए रखें।",
    ],
    "tamra": [
        "संबंधों में सामान्य समय।",
        "धैर्य और समझ से काम लें।",
        "पुराने मतभेद सुलझ सकते हैं।",
        "प्रेम संबंधों में स्थिरता रहेगी।",
    ],
    "rajata": [
        "संबंधों में प्रेम और सामंजस्य बढ़ेगा।",
        "जीवनसाथी का सहयोग मिलेगा।",
        "नए प्रेम संबंध बन सकते हैं।",
        "पारिवारिक सुख में वृद्धि होगी।",
    ],
    "swarna": [
        "संबंधों में अद्भुत समय। प्रेम गहरा होगा।",
        "विवाह के उत्तम योग हैं।",
        "जीवनसाथी से पूर्ण सहयोग मिलेगा।",
        "रोमांटिक पल यादगार होंगे।",
    ],
}

FAMILY_BINDU_PREDICTIONS = {
    "loha": [
        "परिवार में कुछ तनाव रह सकता है।",
        "बुजुर्गों के स्वास्थ्य पर ध्यान दें।",
        "पारिवारिक विवादों से बचें।",
        "गृह शांति के उपाय करें।",
    ],
    "tamra": [
        "पारिवारिक वातावरण सामान्य रहेगा।",
        "छोटे-मोटे मतभेद हो सकते हैं।",
        "परिवार के साथ समय बिताएं।",
        "घर में शांति बनाए रखें।",
    ],
    "rajata": [
        "परिवार में सुख-शांति रहेगी।",
        "पारिवारिक आयोजन सफल होंगे।",
        "बच्चों से खुशखबरी मिल सकती है।",
        "घर में सकारात्मक वातावरण रहेगा।",
    ],
    "swarna": [
        "परिवार में उत्सव का माहौल रहेगा।",
        "शुभ समाचार और मांगलिक कार्य होंगे।",
        "परिवार का पूर्ण सहयोग मिलेगा।",
        "गृह सुख में वृद्धि होगी।",
    ],
}


# =============================================================================
# VEDHA-AFFECTED PREDICTIONS
# =============================================================================

VEDHA_PREDICTIONS = {
    "blocked": [
        "शुभ ग्रह की स्थिति वेध से प्रभावित है। फल में कमी होगी।",
        "ग्रह शुभ भाव में है पर वेध से बाधित। पूर्ण लाभ नहीं मिलेगा।",
        "वेध के कारण शुभ प्रभाव कम हो गया है।",
    ],
    "not_blocked": [
        "ग्रह का गोचर वेध-मुक्त है। पूर्ण फल मिलेगा।",
        "कोई वेध नहीं है। ग्रह का शुभ प्रभाव मिलेगा।",
    ],
}


# =============================================================================
# PERIOD-SPECIFIC MODIFIERS
# =============================================================================

PERIOD_BINDU_MODIFIERS = {
    "daily": {
        "primary_planet": "MOON",
        "bindu_weight": 0.3,  # Less weight for daily (Moon moves fast)
    },
    "weekly": {
        "primary_planet": "MERCURY",
        "bindu_weight": 0.5,
    },
    "monthly": {
        "primary_planet": "SUN",
        "bindu_weight": 0.7,
    },
    "yearly": {
        "primary_planet": "JUPITER",
        "bindu_weight": 1.0,  # Full weight for yearly predictions
    },
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_bindu_category(bindus: int) -> str:
    """Get bindu category name based on count."""
    if bindus >= 5:
        return "swarna"
    elif bindus == 4:
        return "rajata"
    elif bindus == 3:
        return "tamra"
    else:
        return "loha"


def get_bindu_prediction(
    category: str,
    bindus: int,
    seed: int = 0
) -> str:
    """
    Get a prediction based on category and bindu count.

    Args:
        category: Prediction category (career, finance, health, relationships, family, overall)
        bindus: Ashtakavarga bindu count (0-8)
        seed: Random seed for variety

    Returns:
        Hindi prediction text
    """
    bindu_cat = get_bindu_category(bindus)

    predictions_map = {
        "career": CAREER_BINDU_PREDICTIONS,
        "finance": FINANCE_BINDU_PREDICTIONS,
        "health": HEALTH_BINDU_PREDICTIONS,
        "relationships": RELATIONSHIP_BINDU_PREDICTIONS,
        "family": FAMILY_BINDU_PREDICTIONS,
        "overall": OVERALL_BINDU_PREDICTIONS,
    }

    predictions = predictions_map.get(category, OVERALL_BINDU_PREDICTIONS)
    bindu_predictions = predictions.get(bindu_cat, predictions["tamra"])

    return bindu_predictions[seed % len(bindu_predictions)]


def get_vedha_prediction(is_blocked: bool, seed: int = 0) -> str:
    """Get Vedha-related prediction text."""
    key = "blocked" if is_blocked else "not_blocked"
    predictions = VEDHA_PREDICTIONS[key]
    return predictions[seed % len(predictions)]


def get_combined_prediction(
    category: str,
    bindus: int,
    vedha_blocked: bool = False,
    period: str = "daily",
    seed: int = 0
) -> Dict:
    """
    Get combined prediction with bindu and vedha consideration.

    Args:
        category: Prediction category
        bindus: Bindu count (0-8)
        vedha_blocked: Whether favorable transit is blocked by vedha
        period: Prediction period (daily, weekly, monthly, yearly)
        seed: Random seed

    Returns:
        Dict with prediction text and metadata
    """
    bindu_cat = get_bindu_category(bindus)
    main_prediction = get_bindu_prediction(category, bindus, seed)

    result = {
        "prediction_hindi": main_prediction,
        "bindu_category": bindu_cat,
        "bindu_category_hindi": {
            "swarna": "स्वर्ण (उत्तम)",
            "rajata": "रजत (अच्छा)",
            "tamra": "ताम्र (मध्यम)",
            "loha": "लोह (कठिन)",
        }.get(bindu_cat, ""),
        "bindus": bindus,
        "vedha_blocked": vedha_blocked,
    }

    if vedha_blocked and bindu_cat in ["swarna", "rajata"]:
        result["vedha_note"] = get_vedha_prediction(True, seed)
        # Downgrade prediction if vedha blocked
        if bindu_cat == "swarna":
            result["effective_category"] = "rajata"
        else:
            result["effective_category"] = "tamra"

    return result
