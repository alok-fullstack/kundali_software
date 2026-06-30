"""
Vedic Astrology Predictions in Hindi
Based on planetary positions, houses, and dashas
"""

from typing import Dict, List, Optional
from .config import RASHIS, BHAVA_NAMES, Planet, PLANET_NAMES


# Retrograde planet effects - BALANCED (both positive and challenges)
RETROGRADE_EFFECTS = {
    "MARS": {
        "positive": "रणनीतिक सोच, नियंत्रित ऊर्जा, गहन साहस, आंतरिक शक्ति",
        "challenges": "कार्यों में विलंब, आंतरिक क्रोध पर नियंत्रण आवश्यक",
        "summary": "वक्री मंगल: ऊर्जा अंदर की ओर। रणनीतिक सोच उत्तम, कार्य धीरे पर सुदृढ़।"
    },
    "MERCURY": {
        "positive": "गहन चिंतन, शोध क्षमता, आत्मनिरीक्षण, पुराने ज्ञान का लाभ",
        "challenges": "संचार में सावधानी, यात्रा में विलंब संभव",
        "summary": "वक्री बुध: शोध और विश्लेषण में उत्तम। संचार में सोच-समझकर बोलें।"
    },
    "JUPITER": {
        "positive": "आंतरिक ज्ञान, आध्यात्मिक विकास, गहरी समझ, स्वयं के गुरु",
        "challenges": "बाहरी शिक्षा/गुरु से कम लाभ",
        "summary": "वक्री गुरु: आंतरिक ज्ञान प्रबल। आध्यात्मिक विकास में सहायक।"
    },
    "VENUS": {
        "positive": "गहरा प्रेम, आंतरिक सौंदर्य, कलात्मक प्रतिभा, सच्चे संबंध",
        "challenges": "प्रेम में पुनर्विचार, पुराने संबंधों का आगमन",
        "summary": "वक्री शुक्र: गहरे प्रेम और कला में निपुण। सच्चे संबंध बनते हैं।"
    },
    "SATURN": {
        "positive": "आंतरिक अनुशासन, कर्म का गहन फल, धैर्य में वृद्धि, पिछले कर्मों का समाधान",
        "challenges": "परिणाम में विलंब, धैर्य की परीक्षा",
        "summary": "वक्री शनि: आंतरिक अनुशासन उत्तम। पिछले कर्मों का समाधान होता है।"
    },
    "RAHU": {
        "positive": "अंतर्दृष्टि, छिपी प्रतिभाओं का उदय, अनोखे अवसर",
        "challenges": "अप्रत्याशित मोड़, भ्रम से सावधान",
        "summary": "वक्री राहु: अंतर्दृष्टि तीव्र। अप्रत्याशित अवसर मिल सकते हैं।"
    },
    "KETU": {
        "positive": "आध्यात्मिक जागृति, मोक्ष की ओर, पिछले जन्म का ज्ञान",
        "challenges": "भौतिक मामलों में अरुचि",
        "summary": "वक्री केतु: आध्यात्मिक विकास में सहायक। वैराग्य की ओर झुकाव।"
    },
}

# Combust (Asta) planet effects - when planet is too close to Sun
COMBUST_EFFECTS = {
    "MOON": "अस्त चंद्र: मानसिक अशांति, माता से दूरी/चिंता, भावनात्मक उतार-चढ़ाव।",
    "MARS": "अस्त मंगल: योद्धा ग्रह होने से प्रभाव कम। आंतरिक शक्ति बढ़ती है।",
    "MERCURY": "अस्त बुध: बुध अक्सर सूर्य के साथ रहता है - सामान्य स्थिति। गहन विचार शक्ति।",
    "JUPITER": "अस्त गुरु: आंतरिक ज्ञान बढ़ता है, बाहरी गुरु कृपा में कमी संभव।",
    "VENUS": "अस्त शुक्र: सूर्य-शुक्र युति सामान्य। आंतरिक सौंदर्य बोध बढ़ता है।",
    "SATURN": "अस्त शनि: कर्म फल में विलंब, लेकिन आंतरिक अनुशासन बढ़ता है।",
}

# Combustion degrees (how close to Sun = combust)
COMBUSTION_DEGREES = {
    "MOON": 12,
    "MARS": 17,
    "MERCURY": 14,  # 12 when retrograde
    "JUPITER": 11,
    "VENUS": 10,    # 8 when retrograde
    "SATURN": 15,
}

# Planet exaltation signs for combustion mitigation
PLANET_EXALTATION = {
    "MOON": "Vrishabha", "MARS": "Makara", "MERCURY": "Kanya",
    "JUPITER": "Karka", "VENUS": "Meena", "SATURN": "Tula"
}

# Planet own signs for combustion mitigation
PLANET_OWN_SIGNS = {
    "MOON": ["Karka"], "MARS": ["Mesha", "Vrishchika"],
    "MERCURY": ["Mithuna", "Kanya"], "JUPITER": ["Dhanu", "Meena"],
    "VENUS": ["Vrishabha", "Tula"], "SATURN": ["Makara", "Kumbha"]
}

def check_combustion(planets: Dict) -> List[Dict]:
    """Check if any planet is combust (too close to Sun) with mitigations."""
    combust_planets = []
    sun_longitude = planets.get("SUN", {}).get("longitude", 0)

    for planet, max_degrees in COMBUSTION_DEGREES.items():
        planet_data = planets.get(planet, {})
        planet_longitude = planet_data.get("longitude", 0)
        planet_rashi = planet_data.get("rashi", "")
        is_retrograde = planet_data.get("is_retrograde", False)

        # Adjust degrees for retrograde Mercury/Venus
        if is_retrograde and planet == "MERCURY":
            max_degrees = 12
        elif is_retrograde and planet == "VENUS":
            max_degrees = 8

        # Calculate angular distance
        diff = abs(sun_longitude - planet_longitude)
        if diff > 180:
            diff = 360 - diff

        if diff <= max_degrees:
            mitigations = []
            severity = "High"

            # Check mitigations
            # 1. Mars is warrior planet - less affected
            if planet == "MARS":
                mitigations.append("मंगल योद्धा ग्रह - अस्त प्रभाव कम")
                severity = "Low"

            # 2. Mercury commonly with Sun - normal
            if planet == "MERCURY":
                mitigations.append("बुध सूर्य का सहचर - सामान्य स्थिति")
                severity = "Low"

            # 3. Venus within 10 degrees is common
            if planet == "VENUS" and diff <= 10:
                mitigations.append("शुक्र-सूर्य युति सामान्य")
                severity = "Moderate"

            # 4. Planet in exaltation - mitigated
            if planet_rashi == PLANET_EXALTATION.get(planet):
                mitigations.append(f"{planet} उच्च राशि में - अस्त प्रभाव क्षीण")
                severity = "Low"

            # 5. Planet in own sign - mitigated
            if planet_rashi in PLANET_OWN_SIGNS.get(planet, []):
                mitigations.append(f"{planet} स्वराशि में - अस्त प्रभाव कम")
                severity = "Moderate" if severity == "High" else severity

            combust_planets.append({
                "planet": planet,
                "distance": round(diff, 2),
                "effect": COMBUST_EFFECTS.get(planet, ""),
                "mitigations": mitigations,
                "severity": severity,
                "mitigated": len(mitigations) > 0
            })

    return combust_planets


def check_sade_sati(moon_rashi_num: int, saturn_rashi_num: int,
                    saturn_rashi: str = None, moon_rashi: str = None,
                    lagna: str = None, jupiter_rashi_num: int = None) -> Dict:
    """
    Sade Sati = Saturn in 12th, 1st, or 2nd from Moon (7.5 years)
    Returns: Dictionary with active status, phase, severity, effects, and mitigations
    """
    diff = (saturn_rashi_num - moon_rashi_num) % 12

    # Check if Sade Sati is active
    if diff not in [11, 0, 1]:
        return {"active": False, "phase": None, "severity": None, "effects": None, "mitigations": []}

    # Base phase and severity
    if diff == 11:
        phase = "First Phase (Rising)"
        base_severity = "Moderate"
        effects = "शुरुआती दबाव, मानसिक तनाव, खर्चे बढ़ना"
    elif diff == 0:
        phase = "Peak Phase (Climax)"
        base_severity = "High"
        effects = "सबसे कठिन समय, स्वास्थ्य/करियर में चुनौती, धैर्य रखें"
    else:  # diff == 1
        phase = "Last Phase (Setting)"
        base_severity = "Moderate"
        effects = "धीरे-धीरे राहत, आर्थिक सुधार, परिवार में तनाव कम"

    # Check for mitigations/cancellations
    mitigations = []
    severity_reduction = 0

    # 1. Saturn in own sign (Makara/Kumbha)
    if saturn_rashi in ['Makara', 'Kumbha']:
        mitigations.append("शनि स्वराशि में - प्रभाव कम")
        severity_reduction += 1

    # 2. Saturn exalted (Tula)
    if saturn_rashi == 'Tula':
        mitigations.append("शनि उच्च राशि में - प्रभाव बहुत कम")
        severity_reduction += 2

    # 3. Moon in own sign (Karka) or exalted (Vrishabha)
    if moon_rashi == 'Karka':
        mitigations.append("चंद्र स्वराशि में - मानसिक शक्ति अच्छी")
        severity_reduction += 1
    elif moon_rashi == 'Vrishabha':
        mitigations.append("चंद्र उच्च राशि में - सहनशक्ति उत्तम")
        severity_reduction += 1

    # 4. Jupiter aspects Saturn (5th, 7th, 9th from Jupiter)
    if jupiter_rashi_num is not None:
        jupiter_aspect_diff = (saturn_rashi_num - jupiter_rashi_num) % 12
        if jupiter_aspect_diff in [4, 6, 8]:  # 5th, 7th, 9th aspects
            mitigations.append("गुरु की दृष्टि शनि पर - शुभ प्रभाव")
            severity_reduction += 1

    # 5. Saturn is Yogakaraka for lagna (Tula, Vrishabha)
    if lagna in ['Tula', 'Vrishabha']:
        mitigations.append(f"शनि {lagna} लग्न के लिए योगकारक - लाभकारी")
        severity_reduction += 2

    # Adjust severity based on mitigations
    if severity_reduction >= 3:
        final_severity = "Very Low (Mitigated)"
    elif severity_reduction >= 2:
        final_severity = "Low"
    elif severity_reduction >= 1:
        final_severity = "Moderate (Reduced)"
    else:
        final_severity = base_severity

    return {
        "active": True,
        "phase": phase,
        "severity": final_severity,
        "effects": effects,
        "mitigations": mitigations,
        "mitigated": len(mitigations) > 0
    }


# Planet predictions based on house placement
GRAHA_BHAVA_PHAL = {
    "SUN": {
        1: "आत्मविश्वास और नेतृत्व क्षमता उत्तम। सरकारी क्षेत्र में सफलता।",
        2: "पैतृक संपत्ति से लाभ। वाणी में अधिकार।",
        3: "भाई-बहनों से सहयोग। साहसी स्वभाव।",
        4: "माता से स्नेह। भूमि-भवन का सुख।",
        5: "संतान से सुख। राजनीति में रुचि।",
        6: "शत्रुओं पर विजय। स्वास्थ्य का ध्यान रखें।",
        7: "विवाह में देरी संभव। जीवनसाथी प्रभावशाली।",
        8: "पैतृक संपत्ति में बाधा। आध्यात्मिक रुझान।",
        9: "पिता से शुभ संबंध। धार्मिक कार्यों में रुचि।",
        10: "उच्च पद प्राप्ति। सरकारी नौकरी में सफलता।",
        11: "आय में वृद्धि। मित्रों से लाभ।",
        12: "विदेश यात्रा। खर्चों पर नियंत्रण रखें।",
    },
    "MOON": {
        1: "मन शांत और स्थिर। जनप्रियता।",
        2: "धन संचय में सफलता। परिवार से प्रेम।",
        3: "भाई-बहनों से मधुर संबंध। यात्राएं लाभदायक।",
        4: "माता का पूर्ण स्नेह। गृह सुख उत्तम।",
        5: "संतान से सुख। कला में रुचि।",
        6: "मानसिक तनाव से बचें। पाचन का ध्यान रखें।",
        7: "सुंदर जीवनसाथी। वैवाहिक सुख।",
        8: "मानसिक अशांति संभव। ध्यान करें।",
        9: "तीर्थ यात्राएं। धार्मिक प्रवृत्ति।",
        10: "जनता से संबंधित कार्य में सफलता।",
        11: "मित्रों से लाभ। इच्छाओं की पूर्ति।",
        12: "एकांतप्रिय। विदेश में निवास संभव।",
    },
    "MARS": {
        1: "ऊर्जावान और साहसी। नेतृत्व क्षमता।",
        2: "वाणी में तीखापन। धन कमाने में सक्षम।",
        3: "भाइयों से सहयोग। साहसिक कार्य।",
        4: "भूमि-भवन से लाभ। वाहन सुख।",
        5: "संतान से चिंता संभव। खेल में रुचि।",
        6: "शत्रुओं पर विजय। प्रतियोगिता में सफलता।",
        7: "मांगलिक दोष का विचार करें। जीवनसाथी ऊर्जावान।",
        8: "दुर्घटना से सावधान। बीमा करवाएं।",
        9: "धर्म में कम रुचि। पिता से मतभेद।",
        10: "पुलिस, सेना, इंजीनियरिंग में सफलता।",
        11: "भाइयों से लाभ। इच्छापूर्ति।",
        12: "खर्चे अधिक। विदेश में कार्य।",
    },
    "MERCURY": {
        1: "बुद्धिमान और वाक्पटु। व्यापार में सफलता।",
        2: "वाणी मधुर। लेखन से धन।",
        3: "संचार क्षेत्र में सफलता। भाई-बहनों से लाभ।",
        4: "शिक्षा उत्तम। माता बुद्धिमान।",
        5: "संतान बुद्धिमान। शेयर बाजार में लाभ।",
        6: "गणित और विश्लेषण में निपुण।",
        7: "जीवनसाथी बुद्धिमान। व्यापारिक साझेदारी।",
        8: "गुप्त विद्या में रुचि। शोध कार्य।",
        9: "उच्च शिक्षा। विदेश में अध्ययन।",
        10: "लेखन, पत्रकारिता, IT में सफलता।",
        11: "मित्रों से लाभ। आय के अनेक स्रोत।",
        12: "विदेश में शिक्षा। एकांत में अध्ययन।",
    },
    "JUPITER": {
        1: "भाग्यशाली और ज्ञानी। सम्मान प्राप्ति।",
        2: "धनवान परिवार। वाणी प्रभावशाली।",
        3: "धार्मिक भाई-बहन। लेखन में सफलता।",
        4: "माता धार्मिक। बड़ा घर।",
        5: "संतान से सुख। शिक्षा क्षेत्र में सफलता।",
        6: "शत्रुओं का अभाव। स्वास्थ्य अच्छा।",
        7: "उत्तम जीवनसाथी। सुखी दाम्पत्य।",
        8: "दीर्घायु। आध्यात्मिक ज्ञान।",
        9: "अत्यंत भाग्यशाली। गुरुकृपा।",
        10: "उच्च पद। शिक्षा, कानून, बैंकिंग में सफलता।",
        11: "धन लाभ। इच्छापूर्ति।",
        12: "मोक्ष की इच्छा। आश्रम में रुचि।",
    },
    "VENUS": {
        1: "सुंदर और आकर्षक। कला में निपुण।",
        2: "धनवान। मधुर वाणी।",
        3: "कला में रुचि। बहनों से प्रेम।",
        4: "सुंदर घर। वाहन सुख।",
        5: "प्रेम विवाह। कला में संतान।",
        6: "प्रेम में बाधा। स्वास्थ्य का ध्यान।",
        7: "सुंदर जीवनसाथी। सुखी विवाह।",
        8: "ससुराल से धन। गुप्त प्रेम।",
        9: "विदेश यात्रा। धार्मिक पत्नी।",
        10: "फिल्म, फैशन, कला में सफलता।",
        11: "मित्रों से लाभ। विलासिता।",
        12: "विदेश में प्रेम। खर्चीले स्वभाव।",
    },
    "SATURN": {
        1: "मेहनती और अनुशासित। देर से सफलता।",
        2: "धन संचय धीरे-धीरे। मितव्ययी।",
        3: "भाइयों से कष्ट। साहस में कमी।",
        4: "माता से दूरी। भूमि से लाभ देर से।",
        5: "संतान में देरी। गंभीर स्वभाव।",
        6: "शत्रुओं पर विजय। सेवा क्षेत्र में सफलता।",
        7: "विवाह में देरी। जीवनसाथी गंभीर।",
        8: "दीर्घायु। कष्टों से सीख।",
        9: "कर्मकांड में कम रुचि। व्यावहारिक सोच।",
        10: "कड़ी मेहनत से सफलता। उच्च पद 36 के बाद।",
        11: "देर से लाभ। वरिष्ठ मित्र।",
        12: "विदेश में कष्ट। आध्यात्मिक उन्नति।",
    },
    "RAHU": {
        1: "महत्वाकांक्षी। अपारंपरिक सोच।",
        2: "विदेशी धन। वाणी में भ्रम।",
        3: "मीडिया में सफलता। साहसिक कार्य।",
        4: "विदेश में निवास। माता से दूरी।",
        5: "अपारंपरिक संतान। सट्टे से बचें।",
        6: "शत्रुओं पर विजय। चिकित्सा क्षेत्र।",
        7: "विदेशी जीवनसाथी। अंतरजातीय विवाह।",
        8: "तांत्रिक विद्या। रहस्यमय जीवन।",
        9: "विदेश यात्रा। अपारंपरिक धर्म।",
        10: "राजनीति में सफलता। प्रसिद्धि।",
        11: "बड़े लाभ। प्रभावशाली मित्र।",
        12: "विदेश में निवास। मोक्ष की इच्छा।",
    },
    "KETU": {
        1: "आध्यात्मिक। संन्यासी प्रवृत्ति।",
        2: "वाणी में कटुता। पैतृक धन में कमी।",
        3: "भाइयों से दूरी। अंतर्मुखी।",
        4: "माता से वियोग। विदेश में निवास।",
        5: "संतान से दूरी। आध्यात्मिक ज्ञान।",
        6: "शत्रुनाश। चिकित्सा में रुचि।",
        7: "वैवाहिक कष्ट। आध्यात्मिक साथी।",
        8: "तांत्रिक सिद्धि। गुप्त विद्या।",
        9: "पूर्वजन्म के संस्कार। तीर्थाटन।",
        10: "अचानक परिवर्तन। अस्थिर करियर।",
        11: "मित्रों से हानि। आध्यात्मिक लाभ।",
        12: "मोक्ष प्राप्ति। विदेश में आश्रम।",
    },
}

# Rashi-based career predictions
CAREER_BY_LAGNA = {
    "Mesha": "सेना, पुलिस, खेल, सर्जरी, इंजीनियरिंग, मशीनरी, अग्निशमन",
    "Vrishabha": "बैंकिंग, वित्त, कृषि, होटल, फैशन, संगीत, आभूषण",
    "Mithuna": "पत्रकारिता, लेखन, IT, संचार, व्यापार, शिक्षा, अनुवाद",
    "Karka": "होटल, रेस्टोरेंट, नर्सिंग, रियल एस्टेट, जल संबंधी कार्य",
    "Simha": "राजनीति, प्रशासन, मनोरंजन, शेयर बाजार, नेतृत्व",
    "Kanya": "चिकित्सा, लेखा, विश्लेषण, संपादन, गुणवत्ता नियंत्रण",
    "Tula": "कानून, कूटनीति, फैशन, सौंदर्य, कला, इंटीरियर डिजाइन",
    "Vrishchika": "शोध, जासूसी, सर्जरी, बीमा, खनन, तांत्रिक विद्या",
    "Dhanu": "शिक्षा, कानून, धर्म, प्रकाशन, विदेश मामले, यात्रा",
    "Makara": "सरकारी नौकरी, प्रशासन, खनन, भवन निर्माण, कृषि",
    "Kumbha": "IT, इलेक्ट्रॉनिक्स, विज्ञान, सामाजिक कार्य, NGO",
    "Meena": "चिकित्सा, फिल्म, कला, आध्यात्म, जल संबंधी कार्य, विदेश",
}

# Marriage predictions by 7th house
MARRIAGE_PREDICTIONS = {
    "Mesha": "जीवनसाथी ऊर्जावान, साहसी और स्वतंत्र विचारों वाला होगा।",
    "Vrishabha": "जीवनसाथी सुंदर, धनवान और कला प्रेमी होगा।",
    "Mithuna": "जीवनसाथी बुद्धिमान, वाक्पटु और व्यापारिक होगा।",
    "Karka": "जीवनसाथी भावुक, गृहस्थ और परिवार प्रेमी होगा।",
    "Simha": "जीवनसाथी प्रभावशाली, आत्मविश्वासी और सम्मानित होगा।",
    "Kanya": "जीवनसाथी व्यावहारिक, विश्लेषक और सेवाभावी होगा।",
    "Tula": "जीवनसाथी सुंदर, कलात्मक और संतुलित स्वभाव का होगा।",
    "Vrishchika": "जीवनसाथी रहस्यमय, गहन और भावुक होगा।",
    "Dhanu": "जीवनसाथी धार्मिक, शिक्षित और यात्रा प्रेमी होगा।",
    "Makara": "जीवनसाथी गंभीर, मेहनती और व्यावहारिक होगा।",
    "Kumbha": "जीवनसाथी अपारंपरिक, बौद्धिक और स्वतंत्र होगा।",
    "Meena": "जीवनसाथी आध्यात्मिक, कलात्मक और भावुक होगा।",
}

# Children predictions by 5th house
CHILDREN_PREDICTIONS = {
    "Mesha": "संतान साहसी और नेतृत्व क्षमता वाली होगी। खेल में रुचि।",
    "Vrishabha": "संतान कला और संगीत में निपुण होगी। धनवान बनेगी।",
    "Mithuna": "संतान बुद्धिमान और वाक्पटु होगी। शिक्षा में उत्तम।",
    "Karka": "संतान भावुक और माता से जुड़ी होगी। पारिवारिक।",
    "Simha": "संतान प्रभावशाली और नेता होगी। राजनीति में रुचि।",
    "Kanya": "संतान विश्लेषक और व्यावहारिक होगी। चिकित्सा में रुचि।",
    "Tula": "संतान सुंदर और कलात्मक होगी। संतुलित स्वभाव।",
    "Vrishchika": "संतान गहन और शोधकर्ता होगी। विज्ञान में रुचि।",
    "Dhanu": "संतान धार्मिक और शिक्षित होगी। विदेश जाएगी।",
    "Makara": "संतान मेहनती और अनुशासित होगी। देर से सफलता।",
    "Kumbha": "संतान अपारंपरिक और वैज्ञानिक होगी। IT में रुचि।",
    "Meena": "संतान आध्यात्मिक और कलात्मक होगी। संवेदनशील।",
}

# Health predictions by Lagna and 6th house
HEALTH_PREDICTIONS = {
    "Mesha": "सिर, मस्तिष्क और रक्तचाप का ध्यान रखें। गर्मी से बचें।",
    "Vrishabha": "गला, थायराइड और गर्दन की समस्या संभव। मोटापे से बचें।",
    "Mithuna": "फेफड़े, हाथ और तंत्रिका तंत्र का ध्यान रखें।",
    "Karka": "पेट, छाती और पाचन तंत्र का ध्यान रखें। तनाव से बचें।",
    "Simha": "हृदय और रीढ़ का ध्यान रखें। अहंकार से बचें।",
    "Kanya": "आंत, पाचन और तनाव का ध्यान रखें। चिंता कम करें।",
    "Tula": "किडनी, त्वचा और कमर का ध्यान रखें। संतुलित आहार लें।",
    "Vrishchika": "प्रजनन अंग और मूत्र तंत्र का ध्यान रखें।",
    "Dhanu": "जांघ, लीवर और कूल्हे का ध्यान रखें। वजन नियंत्रित रखें।",
    "Makara": "घुटने, हड्डियां और जोड़ों का ध्यान रखें। कैल्शियम लें।",
    "Kumbha": "टखने, रक्त संचार और तंत्रिका का ध्यान रखें।",
    "Meena": "पैर, लसीका तंत्र और नींद का ध्यान रखें। नशे से बचें।",
}

# =============================================================================
# DEPRECATED: Generic dasha predictions - DO NOT USE
# Use get_lordship_based_dasha_prediction() or full_predictions.get_lagna_specific_dasha_effect() instead
# These generic texts give SAME prediction to everyone regardless of lagna - NOT ACCURATE
# Kept only for backward compatibility with external tools that haven't been updated
# =============================================================================
DASHA_EFFECTS = {
    "Sun": "सरकारी कार्यों में सफलता। पिता से लाभ। आत्मविश्वास बढ़ेगा।",
    "Moon": "मानसिक शांति। माता का साथ। यात्राएं होंगी। जनप्रियता।",
    "Mars": "ऊर्जा और साहस बढ़ेगा। भूमि-भवन लाभ। भाइयों से सहयोग।",
    "Mercury": "व्यापार में लाभ। शिक्षा में सफलता। संचार कौशल।",
    "Jupiter": "भाग्योदय। गुरुकृपा। धन लाभ। संतान सुख। विवाह योग।",
    "Venus": "विवाह योग। वाहन सुख। कला में सफलता। प्रेम संबंध।",
    "Saturn": "मेहनत का फल मिलेगा। धैर्य रखें। अनुशासन से सफलता।",
    "Rahu": "अचानक परिवर्तन। विदेश योग। अपारंपरिक सफलता।",
    "Ketu": "आध्यात्मिक उन्नति। मोक्ष की ओर। भौतिक वस्तुओं से विरक्ति।",
}

# =============================================================================
# DASHA LORDSHIP EFFECTS (Effects based on which houses the dasha lord rules)
# =============================================================================
DASHA_LORDSHIP_EFFECTS = {
    1: "आत्म-विकास, स्वास्थ्य, व्यक्तित्व में परिवर्तन",
    2: "धन लाभ, परिवार, वाणी संबंधित फल",
    3: "भाई-बहन, साहस, छोटी यात्राएं",
    4: "माता, घर, वाहन, शिक्षा, सुख",
    5: "संतान, बुद्धि, प्रेम, पूर्व पुण्य",
    6: "शत्रु, रोग, ऋण, सेवा, प्रतियोगिता",
    7: "विवाह, साझेदारी, व्यापार",
    8: "आयु, रहस्य, परिवर्तन, विरासत",
    9: "भाग्य, धर्म, पिता, गुरु, लंबी यात्रा",
    10: "करियर, यश, कर्म, सामाजिक स्थिति",
    11: "लाभ, आय, मित्र, इच्छा पूर्ति",
    12: "व्यय, विदेश, मोक्ष, हानि, आध्यात्म",
}

# Planet name mapping (English to uppercase key for config lookups)
PLANET_NAME_TO_KEY = {
    "Sun": "SUN",
    "Moon": "MOON",
    "Mars": "MARS",
    "Mercury": "MERCURY",
    "Jupiter": "JUPITER",
    "Venus": "VENUS",
    "Saturn": "SATURN",
    "Rahu": "RAHU",
    "Ketu": "KETU",
}

# Planet name in Hindi for display
PLANET_HINDI_NAMES = {
    "Sun": "सूर्य",
    "Moon": "चंद्र",
    "Mars": "मंगल",
    "Mercury": "बुध",
    "Jupiter": "गुरु",
    "Venus": "शुक्र",
    "Saturn": "शनि",
    "Rahu": "राहु",
    "Ketu": "केतु",
}


def get_career_prediction(lagna_rashi: str, planets_in_houses: Dict, planets: Dict) -> str:
    """Generate career prediction based on Lagna, 10th house, and planetary positions."""
    prediction = f"**लग्न आधारित करियर:** {CAREER_BY_LAGNA.get(lagna_rashi, '')}\n\n"

    # 10th house planets
    if planets_in_houses.get(10):
        prediction += "**दशम भाव में ग्रह:**\n"
        for planet in planets_in_houses[10]:
            prediction += f"- {PLANET_NAMES[Planet[planet]]['hindi']}: {GRAHA_BHAVA_PHAL[planet][10]}\n"

    # Sun position for government jobs
    sun_house = None
    for house, planets_list in planets_in_houses.items():
        if "SUN" in planets_list:
            sun_house = house
            break
    if sun_house:
        prediction += f"\n**सूर्य की स्थिति ({sun_house}वें भाव में):** {GRAHA_BHAVA_PHAL['SUN'][sun_house]}\n"

    return prediction


def get_marriage_prediction(lagna_rashi: str, planets_in_houses: Dict, seventh_rashi: str) -> str:
    """Generate marriage prediction based on 7th house."""
    prediction = f"**सप्तम भाव ({seventh_rashi}):** {MARRIAGE_PREDICTIONS.get(seventh_rashi, '')}\n\n"

    # Venus position
    venus_house = None
    for house, planets_list in planets_in_houses.items():
        if "VENUS" in planets_list:
            venus_house = house
            break
    if venus_house:
        prediction += f"**शुक्र की स्थिति ({venus_house}वें भाव में):** {GRAHA_BHAVA_PHAL['VENUS'][venus_house]}\n"

    # 7th house planets
    if planets_in_houses.get(7):
        prediction += "\n**सप्तम भाव में ग्रह:**\n"
        for planet in planets_in_houses[7]:
            prediction += f"- {PLANET_NAMES[Planet[planet]]['hindi']}: {GRAHA_BHAVA_PHAL[planet][7]}\n"

    return prediction


def get_children_prediction(planets_in_houses: Dict, fifth_rashi: str) -> str:
    """Generate children prediction based on 5th house."""
    prediction = f"**पंचम भाव ({fifth_rashi}):** {CHILDREN_PREDICTIONS.get(fifth_rashi, '')}\n\n"

    # Jupiter position (karaka for children)
    jupiter_house = None
    for house, planets_list in planets_in_houses.items():
        if "JUPITER" in planets_list:
            jupiter_house = house
            break
    if jupiter_house:
        prediction += f"**गुरु की स्थिति ({jupiter_house}वें भाव में):** {GRAHA_BHAVA_PHAL['JUPITER'][jupiter_house]}\n"

    # 5th house planets
    if planets_in_houses.get(5):
        prediction += "\n**पंचम भाव में ग्रह:**\n"
        for planet in planets_in_houses[5]:
            prediction += f"- {PLANET_NAMES[Planet[planet]]['hindi']}: {GRAHA_BHAVA_PHAL[planet][5]}\n"

    return prediction


def get_health_prediction(lagna_rashi: str, planets_in_houses: Dict) -> str:
    """Generate health prediction based on Lagna and 6th house."""
    prediction = f"**लग्न आधारित स्वास्थ्य:** {HEALTH_PREDICTIONS.get(lagna_rashi, '')}\n\n"

    # 6th house planets
    if planets_in_houses.get(6):
        prediction += "**षष्ठ भाव में ग्रह (रोग स्थान):**\n"
        for planet in planets_in_houses[6]:
            prediction += f"- {PLANET_NAMES[Planet[planet]]['hindi']}: {GRAHA_BHAVA_PHAL[planet][6]}\n"

    # 8th house planets (longevity)
    if planets_in_houses.get(8):
        prediction += "\n**अष्टम भाव में ग्रह (आयु स्थान):**\n"
        for planet in planets_in_houses[8]:
            prediction += f"- {PLANET_NAMES[Planet[planet]]['hindi']}: {GRAHA_BHAVA_PHAL[planet][8]}\n"

    return prediction


def get_dasha_prediction(current_dasha: Dict, lagna: str = None) -> str:
    """
    Generate prediction based on current dasha.
    DEPRECATED: Use get_lordship_based_dasha_prediction() for accurate lagna-specific predictions.
    """
    maha = current_dasha.get("mahadasha", {}).get("planet", "")
    antar = current_dasha.get("antardasha", {}).get("planet", "")

    # If lagna provided, use lordship-based prediction
    if lagna:
        maha_pred = get_lordship_based_dasha_prediction(maha, lagna)
        antar_pred = get_lordship_based_dasha_prediction(antar, lagna)
        prediction = f"**वर्तमान महादशा ({maha}):** {maha_pred['overall_prediction']}\n\n"
        prediction += f"**वर्तमान अंतर्दशा ({antar}):** {antar_pred['overall_prediction']}\n"
    else:
        # Fallback to house-based if no lagna (deprecated usage)
        prediction = f"**वर्तमान महादशा ({maha}):** दशा फल के लिए लग्न आवश्यक है।\n\n"
        prediction += f"**वर्तमान अंतर्दशा ({antar}):** दशा फल के लिए लग्न आवश्यक है।\n"

    return prediction


def get_planet_lordships(planet: str, lagna: str) -> List[int]:
    """
    Get the houses ruled by a planet for a specific lagna.

    Args:
        planet: Planet name (e.g., "Jupiter", "Venus")
        lagna: Lagna rashi name (e.g., "Karka", "Mesha")

    Returns:
        List of house numbers ruled by the planet
    """
    from .config import HOUSE_LORDSHIPS

    planet_key = PLANET_NAME_TO_KEY.get(planet, planet.upper())

    if lagna not in HOUSE_LORDSHIPS:
        return []

    lordships = HOUSE_LORDSHIPS[lagna]

    # Rahu and Ketu don't have traditional lordships
    if planet_key in ["RAHU", "KETU"]:
        return []

    return lordships.get(planet_key, [])


def is_functional_benefic(planet: str, lagna: str) -> bool:
    """Check if a planet is a functional benefic for the given lagna."""
    from .config import FUNCTIONAL_BENEFICS

    planet_key = PLANET_NAME_TO_KEY.get(planet, planet.upper())
    benefics = FUNCTIONAL_BENEFICS.get(lagna, [])
    return planet_key in benefics


def is_functional_malefic(planet: str, lagna: str) -> bool:
    """Check if a planet is a functional malefic for the given lagna."""
    from .config import FUNCTIONAL_MALEFICS

    planet_key = PLANET_NAME_TO_KEY.get(planet, planet.upper())
    malefics = FUNCTIONAL_MALEFICS.get(lagna, [])
    return planet_key in malefics


def get_yogakaraka(lagna: str) -> str:
    """Get the Yogakaraka planet for the given lagna (if any)."""
    from .config import YOGAKARAKA

    return YOGAKARAKA.get(lagna)


def is_yogakaraka(planet: str, lagna: str) -> bool:
    """Check if a planet is Yogakaraka for the given lagna."""
    from .config import YOGAKARAKA

    planet_key = PLANET_NAME_TO_KEY.get(planet, planet.upper())
    yogakaraka = YOGAKARAKA.get(lagna)
    return yogakaraka == planet_key


def get_natural_relationship(planet1: str, planet2: str) -> str:
    """
    Get the natural relationship between two planets.

    Returns: "friend", "enemy", or "neutral"
    """
    from .config import NATURAL_RELATIONSHIPS

    planet1_key = PLANET_NAME_TO_KEY.get(planet1, planet1.upper())
    planet2_key = PLANET_NAME_TO_KEY.get(planet2, planet2.upper())

    if planet1_key not in NATURAL_RELATIONSHIPS:
        return "neutral"

    relations = NATURAL_RELATIONSHIPS[planet1_key]

    if planet2_key in relations.get("friends", []):
        return "friend"
    elif planet2_key in relations.get("enemies", []):
        return "enemy"
    else:
        return "neutral"


def get_dasha_relationship(maha_planet: str, antar_planet: str, lagna: str) -> str:
    """
    Returns relationship quality between Mahadasha and Antardasha lords.

    Considers:
    1. Natural friendship between planets
    2. Whether both are functional benefics/malefics for this lagna
    3. Yogakaraka status

    Returns: "Excellent", "Good", "Mixed", or "Challenging"
    """
    # Same planet = neutral/good
    if maha_planet == antar_planet:
        if is_functional_benefic(maha_planet, lagna):
            return "Excellent"
        elif is_functional_malefic(maha_planet, lagna):
            return "Challenging"
        else:
            return "Mixed"

    # Check natural relationship
    natural_rel = get_natural_relationship(maha_planet, antar_planet)

    # Check functional nature
    maha_benefic = is_functional_benefic(maha_planet, lagna)
    maha_malefic = is_functional_malefic(maha_planet, lagna)
    antar_benefic = is_functional_benefic(antar_planet, lagna)
    antar_malefic = is_functional_malefic(antar_planet, lagna)

    # Check Yogakaraka
    maha_yogakaraka = is_yogakaraka(maha_planet, lagna)
    antar_yogakaraka = is_yogakaraka(antar_planet, lagna)

    # Score calculation
    score = 0

    # Natural relationship score
    if natural_rel == "friend":
        score += 2
    elif natural_rel == "enemy":
        score -= 2

    # Functional benefic/malefic score
    if maha_benefic and antar_benefic:
        score += 3
    elif maha_malefic and antar_malefic:
        score -= 2  # Both malefics can sometimes work together
    elif (maha_benefic and antar_malefic) or (maha_malefic and antar_benefic):
        score -= 1

    # Yogakaraka bonus
    if maha_yogakaraka:
        score += 2
    if antar_yogakaraka:
        score += 2

    # Determine result
    if score >= 4:
        return "Excellent"
    elif score >= 2:
        return "Good"
    elif score >= -1:
        return "Mixed"
    else:
        return "Challenging"


def get_lordship_based_dasha_prediction(planet: str, lagna: str) -> Dict:
    """
    Get comprehensive lordship-based prediction for a dasha planet.

    Args:
        planet: Dasha lord name (e.g., "Jupiter")
        lagna: Lagna rashi name (e.g., "Karka")

    Returns:
        Dictionary with lordship details, functional nature, and predictions
    """
    lordships = get_planet_lordships(planet, lagna)
    planet_hindi = PLANET_HINDI_NAMES.get(planet, planet)

    result = {
        "planet": planet,
        "planet_hindi": planet_hindi,
        "lagna": lagna,
        "lordships": lordships,
        "lordship_effects": [],
        "is_benefic": is_functional_benefic(planet, lagna),
        "is_malefic": is_functional_malefic(planet, lagna),
        "is_yogakaraka": is_yogakaraka(planet, lagna),
        "overall_nature": "",
        "overall_prediction": "",
    }

    # Get effects for each house ruled
    for house in lordships:
        effect = DASHA_LORDSHIP_EFFECTS.get(house, "")
        result["lordship_effects"].append({
            "house": house,
            "effect": effect
        })

    # Determine overall nature
    if result["is_yogakaraka"]:
        result["overall_nature"] = "योगकारक (अत्यंत शुभ)"
    elif result["is_benefic"] and not result["is_malefic"]:
        result["overall_nature"] = "शुभ (Functional Benefic)"
    elif result["is_malefic"] and not result["is_benefic"]:
        result["overall_nature"] = "अशुभ (Functional Malefic)"
    else:
        result["overall_nature"] = "मिश्रित (Mixed)"

    # Generate overall prediction based on lordships
    if result["is_yogakaraka"]:
        result["overall_prediction"] = f"अत्यंत शुभ समय। {planet_hindi} योगकारक होने से सभी क्षेत्रों में उन्नति।"
    elif lordships:
        good_houses = [h for h in lordships if h in [1, 4, 5, 7, 9, 10, 11]]
        bad_houses = [h for h in lordships if h in [6, 8, 12]]

        if good_houses and not bad_houses:
            result["overall_prediction"] = f"शुभ समय। भाव {', '.join(map(str, good_houses))} से संबंधित लाभ।"
        elif bad_houses and not good_houses:
            result["overall_prediction"] = f"चुनौतीपूर्ण समय। भाव {', '.join(map(str, bad_houses))} से संबंधित कठिनाइयां। सावधानी रखें।"
        else:
            result["overall_prediction"] = f"मिश्रित फल। शुभ भाव {', '.join(map(str, good_houses))} से लाभ, भाव {', '.join(map(str, bad_houses))} से कुछ चुनौतियां।"
    else:
        # Rahu/Ketu - shadow planets with no house lordship
        if planet in ["Rahu", "RAHU"]:
            result["overall_prediction"] = "राहु छाया ग्रह है - भौतिक सुख, विदेश, अप्रत्याशित घटनाएं। राहु की भाव स्थिति से फल निर्धारित।"
        elif planet in ["Ketu", "KETU"]:
            result["overall_prediction"] = "केतु मोक्ष कारक छाया ग्रह - आध्यात्मिक उन्नति, वैराग्य। केतु की भाव स्थिति से फल निर्धारित।"
        else:
            result["overall_prediction"] = "इस ग्रह के प्रभाव का विस्तृत विश्लेषण आवश्यक।"

    return result
