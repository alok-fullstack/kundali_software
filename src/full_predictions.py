"""
Full Detailed Predictions Generator
Complete analysis for all aspects of life

Now includes accuracy components (BPHS-based):
- Shadbala (6-fold planetary strength)
- Combustion (Asta) detection
- Planetary War (Graha Yuddha)
- Navamsa D9 strength
"""

from .config import RASHIS, PLANET_NAMES, Planet, BHAVA_NAMES, NAKSHATRAS, COMBUSTION_ORBS, PLANET_DIGNITIES, RASHI_LIST
from .predictions import GRAHA_BHAVA_PHAL, CAREER_BY_LAGNA, MARRIAGE_PREDICTIONS, CHILDREN_PREDICTIONS, HEALTH_PREDICTIONS
from .yogas import check_kaal_sarp_dosh, check_pitra_dosh, check_neecha_bhanga_raja_yoga

# Import accuracy components
try:
    from .shadbala import ShadbalaCalculator
    SHADBALA_AVAILABLE = True
except ImportError:
    SHADBALA_AVAILABLE = False

try:
    from .rashifal import check_combustion, check_planetary_war, get_navamsa_strength_modifier
    ACCURACY_COMPONENTS_AVAILABLE = True
except ImportError:
    ACCURACY_COMPONENTS_AVAILABLE = False

# Lords for each rashi
RASHI_LORDS = {
    "Mesha": ("मंगल", "Mars"), "Vrishabha": ("शुक्र", "Venus"), "Mithuna": ("बुध", "Mercury"),
    "Karka": ("चंद्र", "Moon"), "Simha": ("सूर्य", "Sun"), "Kanya": ("बुध", "Mercury"),
    "Tula": ("शुक्र", "Venus"), "Vrishchika": ("मंगल", "Mars"), "Dhanu": ("गुरु", "Jupiter"),
    "Makara": ("शनि", "Saturn"), "Kumbha": ("शनि", "Saturn"), "Meena": ("गुरु", "Jupiter")
}

# Spouse qualities by 7th house rashi
SPOUSE_QUALITIES = {
    "Mesha": ["साहसी और स्वतंत्र विचारों वाला/वाली", "ऊर्जावान और क्रियाशील", "नेतृत्व गुण वाला/वाली", "कभी-कभी जिद्दी स्वभाव"],
    "Vrishabha": ["स्थिर और धैर्यवान", "सुंदरता और कला प्रेमी", "भौतिक सुख-सुविधा पसंद", "वफादार और समर्पित"],
    "Mithuna": ["बुद्धिमान और वाकपटु", "विविध विषयों में रुचि", "संवाद में निपुण", "हंसमुख और चंचल स्वभाव"],
    "Karka": ["भावुक और संवेदनशील", "परिवार के प्रति समर्पित", "घरेलू कार्यों में निपुण", "सहानुभूतिपूर्ण स्वभाव"],
    "Simha": ["आत्मविश्वासी और गरिमामय", "उदार और दिलदार", "नेतृत्व क्षमता", "सम्मान की अपेक्षा"],
    "Kanya": ["व्यावहारिक और विश्लेषणात्मक", "स्वास्थ्य के प्रति जागरूक", "सेवाभावी स्वभाव", "परिपूर्णतावादी"],
    "Tula": ["संतुलित और न्यायप्रिय", "सौंदर्य और कला प्रेमी", "सामाजिक और मिलनसार", "सामंजस्य पसंद"],
    "Vrishchika": ["गहन और रहस्यमय", "भावनात्मक रूप से तीव्र", "वफादार और समर्पित", "शक्तिशाली व्यक्तित्व"],
    "Dhanu": ["आशावादी और दार्शनिक", "स्वतंत्रता प्रेमी", "उच्च शिक्षित या धार्मिक", "यात्रा प्रेमी"],
    "Makara": ["महत्वाकांक्षी और मेहनती", "व्यावहारिक और जिम्मेदार", "परंपरा का सम्मान", "धीमी लेकिन स्थायी प्रगति"],
    "Kumbha": ["अनोखे विचारों वाला/वाली", "मानवतावादी दृष्टिकोण", "स्वतंत्र विचारक", "मित्रता में निपुण"],
    "Meena": ["आध्यात्मिक और संवेदनशील", "कल्पनाशील और रचनात्मक", "दयालु और सहानुभूतिपूर्ण", "कलात्मक रुचि"]
}

# Body constitution by lagna
LAGNA_BODY_CONSTITUTION = {
    "Mesha": ("पित्त प्रधान", "सिर, चेहरा, मस्तिष्क"),
    "Vrishabha": ("कफ प्रधान", "गला, गर्दन, थायरॉयड"),
    "Mithuna": ("वात-पित्त", "कंधे, बाहें, फेफड़े"),
    "Karka": ("कफ प्रधान", "छाती, पेट, स्तन"),
    "Simha": ("पित्त प्रधान", "हृदय, रीढ़, पीठ"),
    "Kanya": ("वात-पित्त", "पेट, आंतें, नर्वस सिस्टम"),
    "Tula": ("वात-कफ", "किडनी, कमर, त्वचा"),
    "Vrishchika": ("पित्त-कफ", "प्रजनन अंग, मूत्र तंत्र"),
    "Dhanu": ("पित्त प्रधान", "कूल्हे, जांघें, लिवर"),
    "Makara": ("वात प्रधान", "घुटने, हड्डियां, दांत"),
    "Kumbha": ("वात प्रधान", "टांगें, टखने, रक्त संचार"),
    "Meena": ("कफ प्रधान", "पैर, लसीका तंत्र")
}

# Children qualities by 5th house rashi
CHILDREN_QUALITIES = {
    "Mesha": ["साहसी और ऊर्जावान", "खेलकूद में रुचि", "नेतृत्व क्षमता", "स्वतंत्र विचार"],
    "Vrishabha": ["धैर्यवान और स्थिर", "कला और संगीत में रुचि", "भौतिक सुख पसंद", "जिद्दी लेकिन वफादार"],
    "Mithuna": ["बुद्धिमान और जिज्ञासु", "पढ़ाई में तेज", "संवाद में निपुण", "बहुमुखी प्रतिभा"],
    "Karka": ["भावुक और संवेदनशील", "परिवार से जुड़ाव", "कल्पनाशील", "देखभाल करने वाला स्वभाव"],
    "Simha": ["आत्मविश्वासी", "नाटक/कला में रुचि", "नेतृत्व गुण", "प्रशंसा की आवश्यकता"],
    "Kanya": ["विश्लेषणात्मक मस्तिष्क", "पढ़ाई में होशियार", "व्यवस्थित और साफ-सुथरा", "सेवाभावी"],
    "Tula": ["सामाजिक और मिलनसार", "कला प्रेमी", "न्यायप्रिय", "सौंदर्य बोध"],
    "Vrishchika": ["तीव्र और गहन", "रहस्य में रुचि", "दृढ़ इच्छाशक्ति", "शोध प्रवृत्ति"],
    "Dhanu": ["आशावादी और उत्साही", "दर्शन/धर्म में रुचि", "यात्रा प्रेमी", "उच्च शिक्षा की ओर झुकाव"],
    "Makara": ["जिम्मेदार और परिपक्व", "महत्वाकांक्षी", "अनुशासित", "व्यावहारिक सोच"],
    "Kumbha": ["अनोखे विचार", "तकनीक में रुचि", "मानवतावादी", "स्वतंत्र विचारक"],
    "Meena": ["कल्पनाशील और रचनात्मक", "कला में प्रतिभा", "आध्यात्मिक झुकाव", "दयालु स्वभाव"]
}


def get_lagna_specific_dasha_effect(planet, lagna):
    """Generate lagna-specific dasha effects based on house rulership - NOT generic text."""
    # Planet to houses ruled mapping (1-12)
    PLANET_RULES_HOUSES = {
        "Mesha": {"Mars": [1, 8], "Venus": [2, 7], "Mercury": [3, 6], "Moon": [4], "Sun": [5], "Jupiter": [9, 12], "Saturn": [10, 11]},
        "Vrishabha": {"Venus": [1, 6], "Mercury": [2, 5], "Moon": [3], "Sun": [4], "Jupiter": [8, 11], "Saturn": [9, 10], "Mars": [7, 12]},
        "Mithuna": {"Mercury": [1, 4], "Moon": [2], "Sun": [3], "Venus": [5, 12], "Mars": [6, 11], "Jupiter": [7, 10], "Saturn": [8, 9]},
        "Karka": {"Moon": [1], "Sun": [2], "Mercury": [3, 12], "Venus": [4, 11], "Mars": [5, 10], "Jupiter": [6, 9], "Saturn": [7, 8]},
        "Simha": {"Sun": [1], "Mercury": [2, 11], "Venus": [3, 10], "Mars": [4, 9], "Jupiter": [5, 8], "Saturn": [6, 7], "Moon": [12]},
        "Kanya": {"Mercury": [1, 10], "Venus": [2, 9], "Mars": [3, 8], "Jupiter": [4, 7], "Saturn": [5, 6], "Moon": [11], "Sun": [12]},
        "Tula": {"Venus": [1, 8], "Mars": [2, 7], "Jupiter": [3, 6], "Saturn": [4, 5], "Moon": [10], "Sun": [11], "Mercury": [9, 12]},
        "Vrishchika": {"Mars": [1, 6], "Jupiter": [2, 5], "Saturn": [3, 4], "Moon": [9], "Sun": [10], "Mercury": [8, 11], "Venus": [7, 12]},
        "Dhanu": {"Jupiter": [1, 4], "Saturn": [2, 3], "Mars": [5, 12], "Venus": [6, 11], "Mercury": [7, 10], "Moon": [8], "Sun": [9]},
        "Makara": {"Saturn": [1, 2], "Jupiter": [3, 12], "Mars": [4, 11], "Venus": [5, 10], "Mercury": [6, 9], "Moon": [7], "Sun": [8]},
        "Kumbha": {"Saturn": [1, 12], "Jupiter": [2, 11], "Mars": [3, 10], "Venus": [4, 9], "Mercury": [5, 8], "Moon": [6], "Sun": [7]},
        "Meena": {"Jupiter": [1, 10], "Mars": [2, 9], "Venus": [3, 8], "Mercury": [4, 7], "Saturn": [11, 12], "Moon": [5], "Sun": [6]},
    }

    # House meanings
    HOUSE_MEANINGS = {
        1: ("व्यक्तित्व, स्वास्थ्य", "Personality, Health"),
        2: ("धन, परिवार, वाणी", "Wealth, Family, Speech"),
        3: ("साहस, भाई-बहन, यात्रा", "Courage, Siblings, Short Travel"),
        4: ("माता, सुख, संपत्ति, वाहन", "Mother, Happiness, Property, Vehicle"),
        5: ("संतान, प्रेम, शिक्षा, बुद्धि", "Children, Love, Education, Intelligence"),
        6: ("रोग, शत्रु, ऋण, नौकरी", "Disease, Enemies, Debts, Service"),
        7: ("विवाह, साझेदारी, व्यापार", "Marriage, Partnership, Business"),
        8: ("अचानक घटनाएं, विरासत, गुप्त", "Sudden events, Inheritance, Secrets"),
        9: ("भाग्य, पिता, धर्म, विदेश", "Fortune, Father, Religion, Foreign"),
        10: ("करियर, प्रसिद्धि, सामाजिक स्थिति", "Career, Fame, Social Status"),
        11: ("लाभ, आय, इच्छापूर्ति", "Gains, Income, Fulfillment"),
        12: ("खर्च, विदेश, मोक्ष, हानि", "Expenses, Foreign, Moksha, Loss"),
    }

    # Functional benefic/malefic status
    FUNCTIONAL_STATUS = {
        "Mesha": {"benefics": ["Sun", "Moon", "Jupiter", "Mars"], "malefics": ["Saturn", "Mercury", "Venus"], "yogakaraka": None},
        "Vrishabha": {"benefics": ["Saturn", "Mercury", "Venus", "Sun"], "malefics": ["Jupiter", "Moon", "Mars"], "yogakaraka": "Saturn"},
        "Mithuna": {"benefics": ["Venus", "Saturn", "Mercury"], "malefics": ["Mars", "Jupiter", "Sun"], "yogakaraka": None},
        "Karka": {"benefics": ["Mars", "Jupiter", "Moon"], "malefics": ["Saturn", "Mercury", "Venus"], "yogakaraka": "Mars"},
        "Simha": {"benefics": ["Sun", "Mars", "Jupiter"], "malefics": ["Saturn", "Venus", "Mercury"], "yogakaraka": "Mars"},
        "Kanya": {"benefics": ["Venus", "Mercury"], "malefics": ["Mars", "Jupiter", "Moon", "Sun"], "yogakaraka": None},
        "Tula": {"benefics": ["Saturn", "Mercury", "Venus"], "malefics": ["Sun", "Mars", "Jupiter"], "yogakaraka": "Saturn"},
        "Vrishchika": {"benefics": ["Moon", "Jupiter", "Sun", "Mars"], "malefics": ["Mercury", "Venus", "Saturn"], "yogakaraka": "Moon"},
        "Dhanu": {"benefics": ["Sun", "Mars", "Jupiter"], "malefics": ["Venus", "Saturn", "Mercury"], "yogakaraka": None},
        "Makara": {"benefics": ["Venus", "Mercury", "Saturn"], "malefics": ["Mars", "Jupiter", "Moon"], "yogakaraka": "Venus"},
        "Kumbha": {"benefics": ["Venus", "Saturn", "Mercury"], "malefics": ["Mars", "Jupiter", "Moon", "Sun"], "yogakaraka": "Venus"},
        "Meena": {"benefics": ["Moon", "Mars", "Jupiter"], "malefics": ["Saturn", "Venus", "Mercury", "Sun"], "yogakaraka": "Mars"},
    }

    # Get houses ruled by this planet for this lagna
    planet_houses = PLANET_RULES_HOUSES.get(lagna, {})
    houses_ruled = planet_houses.get(planet, [])

    # Get functional status
    func_status = FUNCTIONAL_STATUS.get(lagna, {})
    is_benefic = planet in func_status.get("benefics", [])
    is_yogakaraka = planet == func_status.get("yogakaraka")
    is_malefic = planet in func_status.get("malefics", [])

    # Build effect based on houses ruled
    house_effects = []
    for h in houses_ruled:
        meaning = HOUSE_MEANINGS.get(h, ("", ""))
        house_effects.append(f"भाव {h} ({meaning[0]} / {meaning[1]})")

    houses_text = " और ".join(house_effects) if house_effects else "विशेष प्रभाव"

    # Determine overall effect
    if is_yogakaraka:
        status_hindi = "योगकारक - बहुत शुभ!"
        status_en = "Yogakaraka - Very Auspicious!"
        effect_desc = f"{planet} आपके लिए योगकारक है। इसकी दशा जीवन के सबसे अच्छे समय में से एक होगी। {houses_text} से संबंधित क्षेत्रों में उत्कृष्ट परिणाम।"
        effect_en = f"{planet} is Yogakaraka for you. This Dasha will be one of the best periods. Excellent results in areas related to {houses_text}."
    elif is_benefic:
        status_hindi = "शुभ ग्रह"
        status_en = "Benefic Planet"
        effect_desc = f"{planet} आपके लिए शुभ ग्रह है। यह {houses_text} का स्वामी है। इन क्षेत्रों में अच्छे परिणाम मिलेंगे।"
        effect_en = f"{planet} is benefic for you. It rules {houses_text}. Good results in these areas."
    else:
        status_hindi = "कठिन ग्रह - सावधानी"
        status_en = "Challenging Planet - Caution"
        effect_desc = f"{planet} आपके लिए कठिन ग्रह है। यह {houses_text} का स्वामी है। इन क्षेत्रों में challenges आ सकती हैं। उपाय करें।"
        effect_en = f"{planet} is challenging for you. It rules {houses_text}. Challenges may come in these areas. Do remedies."

    # Build reason text based on houses ruled
    if houses_ruled:
        reason_text = f"{planet} भाव {', '.join(map(str, houses_ruled))} का स्वामी है।"
        if is_yogakaraka:
            reason_text += " योगकारक होने से अति शुभ।"
        elif is_benefic:
            reason_text += " शुभ ग्रह।"
        else:
            reason_text += " कठिन ग्रह - उपाय करें।"
    else:
        reason_text = f"{planet} छाया ग्रह है।"

    return {
        "status_hindi": status_hindi,
        "status_en": status_en,
        "effect_hindi": effect_desc,
        "effect_en": effect_en,
        "effect": effect_desc,  # Alias for effect_hindi
        "reason": reason_text,  # Reason based on house rulership
        "houses_ruled": houses_ruled,
        "is_benefic": is_benefic,
        "is_yogakaraka": is_yogakaraka
    }


def get_lagna_specific_remedies_html(lagna, data):
    """Generate lagna-specific mantras, puja and donations - based on functional benefics."""
    # Functional benefics and malefics for each lagna (Vedic astrology rules)
    LAGNA_BENEFICS = {
        "Mesha": {"benefics": ["Sun", "Moon", "Jupiter"], "yogakaraka": None, "malefics": ["Saturn", "Mercury", "Venus"]},
        "Vrishabha": {"benefics": ["Saturn", "Mercury", "Venus"], "yogakaraka": "Saturn", "malefics": ["Jupiter", "Moon"]},
        "Mithuna": {"benefics": ["Venus", "Saturn"], "yogakaraka": None, "malefics": ["Mars", "Jupiter"]},
        "Karka": {"benefics": ["Mars", "Jupiter", "Moon"], "yogakaraka": "Mars", "malefics": ["Saturn", "Mercury", "Venus"]},
        "Simha": {"benefics": ["Sun", "Mars", "Jupiter"], "yogakaraka": "Mars", "malefics": ["Saturn", "Venus"]},
        "Kanya": {"benefics": ["Venus", "Mercury"], "yogakaraka": None, "malefics": ["Mars", "Jupiter", "Moon"]},
        "Tula": {"benefics": ["Saturn", "Mercury", "Venus"], "yogakaraka": "Saturn", "malefics": ["Sun", "Mars", "Jupiter"]},
        "Vrishchika": {"benefics": ["Moon", "Jupiter", "Sun"], "yogakaraka": "Moon", "malefics": ["Mercury", "Venus"]},
        "Dhanu": {"benefics": ["Sun", "Mars"], "yogakaraka": None, "malefics": ["Venus", "Saturn"]},
        "Makara": {"benefics": ["Venus", "Mercury", "Saturn"], "yogakaraka": "Venus", "malefics": ["Mars", "Jupiter", "Moon"]},
        "Kumbha": {"benefics": ["Venus", "Saturn"], "yogakaraka": "Venus", "malefics": ["Mars", "Jupiter", "Moon"]},
        "Meena": {"benefics": ["Moon", "Mars"], "yogakaraka": "Mars", "malefics": ["Saturn", "Venus", "Mercury"]},
    }

    # Planet donation items
    PLANET_DONATIONS = {
        "Sun": ("सूर्य / Sun", "गेहूं, गुड़, तांबा, लाल वस्त्र, माणिक्य / Wheat, jaggery, copper, red clothes", "रविवार / Sunday"),
        "Moon": ("चंद्र / Moon", "चावल, दूध, सफेद वस्त्र, चांदी, मोती / Rice, milk, white clothes, silver, pearl", "सोमवार / Monday"),
        "Mars": ("मंगल / Mars", "मसूर दाल, लाल वस्त्र, तांबा, गुड़ / Red lentils, red clothes, copper, jaggery", "मंगलवार / Tuesday"),
        "Mercury": ("बुध / Mercury", "हरी मूंग, हरे वस्त्र, पन्ना / Green moong, green clothes, emerald items", "बुधवार / Wednesday"),
        "Jupiter": ("गुरु / Jupiter", "चना दाल, हल्दी, पीले वस्त्र, केला / Chana dal, turmeric, yellow clothes, banana", "गुरुवार / Thursday"),
        "Venus": ("शुक्र / Venus", "चावल, घी, सफेद वस्त्र, इत्र / Rice, ghee, white clothes, perfume", "शुक्रवार / Friday"),
        "Saturn": ("शनि / Saturn", "काले तिल, सरसों तेल, लोहा, छाता / Black sesame, mustard oil, iron, umbrella", "शनिवार / Saturday"),
    }

    # Planet mantras
    PLANET_MANTRAS = {
        "Sun": ("ॐ ह्रां ह्रीं ह्रौं सः सूर्याय नमः", "रविवार / Sunday"),
        "Moon": ("ॐ श्रां श्रीं श्रौं सः चंद्राय नमः", "सोमवार / Monday"),
        "Mars": ("ॐ क्रां क्रीं क्रौं सः भौमाय नमः", "मंगलवार / Tuesday"),
        "Mercury": ("ॐ ब्रां ब्रीं ब्रौं सः बुधाय नमः", "बुधवार / Wednesday"),
        "Jupiter": ("ॐ ग्रां ग्रीं ग्रौं सः गुरवे नमः", "गुरुवार / Thursday"),
        "Venus": ("ॐ द्रां द्रीं द्रौं सः शुक्राय नमः", "शुक्रवार / Friday"),
        "Saturn": ("ॐ प्रां प्रीं प्रौं सः शनैश्चराय नमः", "शनिवार / Saturday"),
    }

    # Planet worship
    PLANET_WORSHIP = {
        "Sun": "सूर्य नमस्कार, आदित्य हृदयम / Surya Namaskar, Aditya Hridayam",
        "Moon": "शिव पूजा, चंद्र दर्शन / Shiva worship, Moon gazing",
        "Mars": "हनुमान पूजा, मंगल स्तोत्र / Hanuman worship, Mars hymn",
        "Mercury": "विष्णु पूजा, बुध स्तोत्र / Vishnu worship, Mercury hymn",
        "Jupiter": "विष्णु सहस्रनाम, गुरु स्तोत्र / Vishnu Sahasranam, Jupiter hymn",
        "Venus": "लक्ष्मी पूजा, शुक्र स्तोत्र / Lakshmi worship, Venus hymn",
        "Saturn": "हनुमान चालीसा, शनि स्तोत्र / Hanuman Chalisa, Saturn hymn",
    }

    lagna_info = LAGNA_BENEFICS.get(lagna, LAGNA_BENEFICS["Mesha"])
    benefics = lagna_info["benefics"]
    yogakaraka = lagna_info["yogakaraka"]
    malefics = lagna_info["malefics"]

    # Build mantras table for benefics only
    mantras_html = f'''
    <tr><td><strong>{data['lord']}</strong> (लग्नेश)<br><span style="font-size:10px;">आपके लग्नेश - सबसे महत्वपूर्ण / Your Lagna Lord - Most important</span></td><td>{data['mantra']}</td><td>108/दिन</td><td>{data['day']}</td></tr>
    '''
    for planet in benefics:
        if planet != data['lord_en']:  # Don't duplicate lagna lord
            mantra_data = PLANET_MANTRAS.get(planet, ("", ""))
            mantras_html += f'''
            <tr><td><strong>{PLANET_DONATIONS[planet][0]}</strong><br><span style="font-size:10px;">आपके शुभ ग्रह / Benefic for your lagna</span></td><td>{mantra_data[0]}</td><td>108/दिन</td><td>{mantra_data[1]}</td></tr>
            '''

    # Build worship list for benefics only
    worship_html = f'''<li><strong>{data['day']}:</strong> लग्नेश {data['lord']} की पूजा / Worship your Lagna Lord - <span style="color:#666;">सबसे महत्वपूर्ण / Most important</span></li>'''
    for planet in benefics[:2]:  # Top 2 benefics
        if planet != data['lord_en']:
            worship_html += f'''<li><strong>{PLANET_MANTRAS[planet][1]}:</strong> {PLANET_WORSHIP.get(planet, "")} - <span style="color:#666;">आपके लिए शुभ / Benefic for you</span></li>'''

    # Build donations table for benefics only
    donations_html = ""
    # First add lagna lord with specific items
    lord_donations = PLANET_DONATIONS.get(data['lord_en'], ("", "लग्नेश की वस्तुएं", ""))
    donations_html += f'''
    <tr><td><strong>{data['lord']}</strong><br><span style="font-size:10px;">आपके लग्नेश / Your Lagna Lord</span></td><td>{lord_donations[1]}</td><td>{data['day']}</td></tr>
    '''
    for planet in benefics:
        if planet != data['lord_en']:
            donation_data = PLANET_DONATIONS.get(planet, ("", "", ""))
            donations_html += f'''
            <tr><td><strong>{donation_data[0]}</strong><br><span style="font-size:10px;">आपके शुभ ग्रह / Benefic</span></td><td>{donation_data[1]}</td><td>{donation_data[2]}</td></tr>
            '''

    # Warning for malefics
    malefic_names = ", ".join([PLANET_DONATIONS.get(p, (p, "", ""))[0].split(" / ")[0] for p in malefics[:3]])

    html = f'''
    <div class="detail-box">
        <h3>🙏 आपके लग्न के लिए मंत्र जाप / Mantras for YOUR Lagna</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #10b981;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 केवल शुभ ग्रहों के मंत्र जपें! / Chant mantras of BENEFIC planets only!</strong><br>
                {lagna} लग्न के लिए <strong>{", ".join(benefics)}</strong> शुभ ग्रह हैं। केवल इन्हीं के मंत्र जपें।
                {malefic_names} के मंत्र आपके लिए अनुकूल नहीं हैं।<br>
                <em>For {lagna} ascendant, <strong>{", ".join(benefics)}</strong> are benefic planets. Chant only their mantras.
                {malefic_names} mantras are not favorable for you.</em>
            </p>
        </div>
        <table class="detail-table">
            <tr><th>ग्रह / Planet</th><th>मंत्र / Mantra</th><th>जाप / Count</th><th>दिन / Day</th></tr>
            {mantras_html}
        </table>
    </div>

    <div class="detail-box">
        <h3>🙏 आपके लग्न के लिए पूजा / Worship for YOUR Lagna</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #3b82f6;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 शुभ ग्रहों की पूजा करें / Worship benefic planets!</strong><br>
                केवल अपने शुभ ग्रहों ({", ".join(benefics)}) की पूजा करें। अशुभ ग्रहों की पूजा से बचें।<br>
                <em>Worship only your benefic planets. Avoid worshipping malefic planets.</em>
            </p>
        </div>
        <ul class="prediction-list">
            {worship_html}
        </ul>
    </div>

    <div class="detail-box">
        <h3>🎁 आपके लग्न के लिए दान / Donations for YOUR Lagna</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #f59e0b;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 शुभ ग्रहों की वस्तुएं दान करें / Donate items of benefic planets!</strong><br>
                दान से ग्रह बली होते हैं। <strong>केवल शुभ ग्रहों</strong> की वस्तुएं दान करें। अशुभ ग्रहों को बली करने से बचें।<br>
                <em>Donation strengthens planets. Donate items of <strong>benefic planets only</strong>. Avoid strengthening malefic planets.</em>
            </p>
        </div>
        <table class="detail-table">
            <tr><th>ग्रह / Planet</th><th>दान वस्तु / Donation Items</th><th>दिन / Day</th></tr>
            {donations_html}
        </table>
        <p style="margin-top: 10px; padding: 8px; background: #fef2f2; border-radius: 6px; font-size: 12px;">
            ⚠️ <strong>सावधानी:</strong> {malefic_names} आपके लिए अशुभ ग्रह हैं। इनकी वस्तुएं दान न करें।<br>
            <em>Caution: {malefic_names} are malefic for you. Don't donate their items.</em>
        </p>
    </div>
    '''
    return html


def get_prakriti_based_remedies_html(prakriti, moon_house, eighth_planets):
    """Generate prakriti-specific health remedies - NOT generic for everyone."""
    # Prakriti-specific remedies
    PRAKRITI_REMEDIES = {
        "वात": {
            "yoga": ("सूर्य नमस्कार, पवनमुक्तासन / Sun Salutation, Wind-releasing poses", "वात शांत करने वाले धीमे आसन / Slow poses to calm Vata"),
            "pranayama": ("अनुलोम-विलोम, भ्रामरी / Alternate nostril, Humming bee", "नर्वस सिस्टम को शांत करता है / Calms nervous system"),
            "diet": ("गर्म, तैलीय भोजन / Warm, oily foods", "ठंडे, सूखे भोजन से बचें / Avoid cold, dry foods"),
            "herbs": [("अश्वगंधा / Ashwagandha", "वात शांति, शक्ति"), ("शतावरी / Shatavari", "पोषण, शांति"), ("त्रिफला / Triphala", "पाचन, detox")],
            "time": "प्रातः 6-8 बजे / Morning 6-8 AM"
        },
        "पित्त": {
            "yoga": ("चंद्र नमस्कार, शीतली / Moon Salutation, Cooling poses", "शरीर की गर्मी कम करने वाले आसन / Poses to reduce body heat"),
            "pranayama": ("शीतली, शीतकारी / Cooling breath, Hissing breath", "शरीर को ठंडा करता है / Cools the body"),
            "diet": ("ठंडे, मीठे भोजन / Cool, sweet foods", "तीखे, खट्टे से बचें / Avoid spicy, sour foods"),
            "herbs": [("आंवला / Amla", "पित्त शांति, vitamin C"), ("गिलोय / Giloy", "रक्त शुद्धि"), ("चंदन / Sandalwood", "शीतलता")],
            "time": "प्रातः या सायं (ठंडे समय में) / Morning or evening (cooler times)"
        },
        "कफ": {
            "yoga": ("सूर्य नमस्कार तेज गति से, कपालभाति / Fast Sun Salutation, Skull-shining breath", "ऊर्जा बढ़ाने वाले आसन / Energizing poses"),
            "pranayama": ("कपालभाति, भस्त्रिका / Skull-shining, Bellows breath", "कफ को निकालता है / Expels Kapha"),
            "diet": ("हल्का, गर्म, तीखा भोजन / Light, warm, spicy foods", "भारी, तैलीय से बचें / Avoid heavy, oily foods"),
            "herbs": [("त्रिकटु / Trikatu", "पाचन अग्नि"), ("पुनर्नवा / Punarnava", "सूजन कम"), ("हरीतकी / Haritaki", "detox")],
            "time": "प्रातः 6-10 बजे / Morning 6-10 AM"
        },
        "वात-पित्त": {
            "yoga": ("मध्यम गति के आसन / Moderate pace poses", "संतुलित अभ्यास / Balanced practice"),
            "pranayama": ("अनुलोम-विलोम / Alternate nostril", "दोनों दोषों को संतुलित करता है / Balances both doshas"),
            "diet": ("न बहुत गर्म, न बहुत ठंडा / Neither too hot nor cold", "मसालेदार से बचें / Avoid very spicy"),
            "herbs": [("अश्वगंधा / Ashwagandha", "वात-पित्त शांति"), ("आंवला / Amla", "cooling + nourishing"), ("ब्राह्मी / Brahmi", "मानसिक शांति")],
            "time": "प्रातः 7-9 बजे / Morning 7-9 AM"
        },
        "पित्त-कफ": {
            "yoga": ("धीमे से मध्यम आसन / Slow to moderate poses", "ठंडक और हल्कापन / Cooling and lightness"),
            "pranayama": ("शीतली, अनुलोम-विलोम / Cooling breath, Alternate nostril", "पित्त-कफ संतुलन / Balances both"),
            "diet": ("हल्का, ठंडा भोजन / Light, cool foods", "तैलीय और तीखे से बचें / Avoid oily and spicy"),
            "herbs": [("आंवला / Amla", "पित्त शांति"), ("त्रिफला / Triphala", "पाचन"), ("गिलोय / Giloy", "रक्त शुद्धि")],
            "time": "प्रातः या सायं / Morning or evening"
        },
        "वात-कफ": {
            "yoga": ("गर्माहट देने वाले आसन / Warming poses", "सूर्य नमस्कार मध्यम गति / Sun Salutation moderate pace"),
            "pranayama": ("भस्त्रिका, अनुलोम-विलोम / Bellows breath, Alternate nostril", "गर्माहट और ऊर्जा / Warmth and energy"),
            "diet": ("गर्म, हल्का, तीखा / Warm, light, mildly spicy", "ठंडे और भारी से बचें / Avoid cold and heavy"),
            "herbs": [("अश्वगंधा / Ashwagandha", "शक्ति"), ("त्रिकटु / Trikatu", "पाचन अग्नि"), ("पिप्पली / Pippali", "कफ निवारण")],
            "time": "प्रातः 6-9 बजे / Morning 6-9 AM"
        }
    }

    # Get prakriti-specific remedies or default
    prakriti_key = prakriti if prakriti in PRAKRITI_REMEDIES else "वात-पित्त"
    remedies = PRAKRITI_REMEDIES.get(prakriti_key, PRAKRITI_REMEDIES["वात-पित्त"])

    # Mental health issues based on Moon position
    moon_issues = ""
    if moon_house in [6, 8, 12]:
        moon_house_effects = {
            6: "चंद्र 6th भाव - तनाव, चिंता की प्रवृत्ति / Moon in 6th - tendency for stress, anxiety",
            8: "चंद्र 8th भाव - गहरी भावनाएं, emotional ups-downs / Moon in 8th - deep emotions, emotional fluctuations",
            12: "चंद्र 12th भाव - अकेलापन, नींद की समस्या संभव / Moon in 12th - isolation, possible sleep issues"
        }
        moon_issues = moon_house_effects.get(moon_house, "")

    # 8th house planet analysis for chronic issues - PLANET-SPECIFIC warnings
    eighth_house_html = ""
    if eighth_planets:
        eighth_house_html = '''
        <div style="margin-top: 15px; padding: 10px; background: #fef2f2; border-radius: 8px; border-left: 4px solid #ef4444;">
            <strong>⚠️ अष्टम भाव (8th House) में ग्रह - ध्यान दें:</strong><br>
            <span style="font-size: 12px;">8th भाव chronic/hidden ailments से जुड़ा है। / 8th house relates to chronic/hidden ailments.</span>
            <ul style="margin: 10px 0; padding-left: 20px;">
        '''
        # Add PLANET-SPECIFIC warnings for each planet in 8th house
        for p in eighth_planets:
            planet_hindi = PLANET_NAMES[Planet[p]]["hindi"]
            # Get planet-specific 8th house effect
            effect = GRAHA_BHAVA_PHAL.get(p, {}).get(8, "नियमित check-up करवाएं / Get regular check-ups")
            eighth_house_html += f'''
                <li><strong>{planet_hindi} ({p}):</strong> {effect}</li>'''
        eighth_house_html += '''
            </ul>
            <em style="font-size: 11px;">Specific health areas to monitor based on YOUR chart's 8th house planets.</em>
        </div>
        '''

    html = f'''
    <div class="detail-box highlight-green">
        <h3>🧘 आपकी प्रकृति ({prakriti}) के अनुसार उपाय / Remedies for YOUR Constitution</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #10b981;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 ये उपाय आपकी {prakriti} प्रकृति के लिए विशेष हैं / These remedies are specific to YOUR {prakriti} constitution:</strong><br>
                आयुर्वेद में हर प्रकृति के लिए अलग-अलग आहार, योग और जड़ी-बूटियां होती हैं। नीचे दिए गए उपाय <strong>आपकी कुंडली के अनुसार</strong> हैं।<br>
                <em>In Ayurveda, each constitution has specific diet, yoga and herbs. Below remedies are <strong>based on your chart</strong>.</em>
            </p>
        </div>
        <table class="detail-table">
            <tr><th>उपाय / Remedy</th><th>आपके लिए विशेष / Specific for You</th><th>समय / Time</th></tr>
            <tr>
                <td><strong>योग आसन / Yoga</strong></td>
                <td>{remedies["yoga"][0]}<br><span style="font-size:11px;color:#666;">↳ {remedies["yoga"][1]}</span></td>
                <td>{remedies["time"]}</td>
            </tr>
            <tr>
                <td><strong>प्राणायाम / Pranayama</strong></td>
                <td>{remedies["pranayama"][0]}<br><span style="font-size:11px;color:#666;">↳ {remedies["pranayama"][1]}</span></td>
                <td>प्रातः 10-15 मिनट</td>
            </tr>
            <tr>
                <td><strong>आहार / Diet</strong></td>
                <td>{remedies["diet"][0]}<br><span style="font-size:11px;color:#666;">↳ {remedies["diet"][1]}</span></td>
                <td>नियमित / Regular</td>
            </tr>
        </table>
        {eighth_house_html}
        {f'<p style="margin-top:10px;padding:8px;background:#dbeafe;border-radius:6px;"><strong>🧠 मानसिक स्वास्थ्य नोट:</strong> {moon_issues}</p>' if moon_issues else ''}
    </div>

    <div class="detail-box">
        <h3>💊 आपकी प्रकृति ({prakriti}) के लिए जड़ी-बूटियां / Herbs for YOUR Constitution</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #f59e0b;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 ये जड़ी-बूटियां {prakriti} प्रकृति के लिए विशेष हैं:</strong><br>
                हर प्रकृति के लिए अलग herbs होती हैं। गलत herb से असंतुलन हो सकता है।<br>
                <em>Each constitution has specific herbs. Wrong herbs can cause imbalance.</em>
            </p>
        </div>
        <ul class="prediction-list">
    '''

    for herb in remedies["herbs"]:
        html += f'<li><strong>{herb[0]}</strong> - {herb[1]}</li>'

    html += '''
        </ul>
        <p style="font-size: 12px; color: #666; margin-top: 10px;">
            ⚠️ <strong>नोट:</strong> कोई भी जड़ी-बूटी लेने से पहले आयुर्वेदिक चिकित्सक से परामर्श लें।<br>
            <em>Consult an Ayurvedic doctor before taking any herbs.</em>
        </p>
    </div>
    '''
    return html


def get_investment_suggestions_html(planets_in_houses, house_rashis, lagna=None):
    """Calculate investment suitability based on actual chart - NOT generic ratings."""
    if lagna is None:
        raise ValueError("lagna parameter is required for accurate investment suggestions")

    fourth_planets = planets_in_houses.get(4, [])
    fifth_planets = planets_in_houses.get(5, [])
    second_planets = planets_in_houses.get(2, [])
    ninth_planets = planets_in_houses.get(9, [])
    eleventh_planets = planets_in_houses.get(11, [])

    # Find key planet positions
    saturn_house = jupiter_house = mercury_house = rahu_house = mars_house = 0
    for h, planets in planets_in_houses.items():
        if "SATURN" in planets: saturn_house = h
        if "JUPITER" in planets: jupiter_house = h
        if "MERCURY" in planets: mercury_house = h
        if "RAHU" in planets: rahu_house = h
        if "MARS" in planets: mars_house = h

    # Calculate Real Estate suitability (4th house, Saturn, Mars)
    real_estate_score = 3  # Base score
    real_estate_reasons = []
    if saturn_house == 4 or mars_house == 4:
        real_estate_score += 2
        real_estate_reasons.append("शनि/मंगल 4th में - भूमि योग प्रबल")
    if "SATURN" in fourth_planets or "MARS" in fourth_planets:
        real_estate_score += 1
    if saturn_house in [1, 4, 7, 10]:
        real_estate_score += 1
        real_estate_reasons.append("शनि केंद्र में - property से लाभ")
    fourth_rashi = house_rashis.get(4, {}).get('name', '')
    if fourth_rashi in ["Vrishabha", "Simha", "Vrishchika", "Kumbha"]:  # Fixed signs
        real_estate_score += 1
        real_estate_reasons.append("4th में स्थिर राशि - स्थायी संपत्ति")

    # Calculate Stocks/Trading suitability (5th house speculation, Mercury, Rahu)
    stocks_score = 2  # Base score
    stocks_reasons = []
    if mercury_house in [2, 5, 10, 11]:
        stocks_score += 2
        stocks_reasons.append(f"बुध भाव {mercury_house} में - व्यापार बुद्धि अच्छी")
    if rahu_house in [2, 5, 11]:
        stocks_score += 1
        stocks_reasons.append("राहु धन/लाभ भाव में - speculation में लाभ")
    if "MERCURY" in fifth_planets or "RAHU" in fifth_planets:
        stocks_score += 1
    if fifth_planets:
        stocks_score += 1
        stocks_reasons.append(f"5th भाव में ग्रह - speculation योग")

    # Calculate FD/Safe investments (2nd house, Saturn stability)
    fd_score = 3  # Base score
    fd_reasons = []
    if second_planets:
        fd_score += 1
        fd_reasons.append("2nd भाव सक्रिय - बचत की प्रवृत्ति")
    if saturn_house in [2, 9, 11]:
        fd_score += 2
        fd_reasons.append("शनि धन भावों में - सुरक्षित निवेश से लाभ")
    if "SATURN" in second_planets:
        fd_score += 1
        fd_reasons.append("शनि 2nd में - long-term savings अच्छा")

    # Calculate Gold/Precious metals (Jupiter, 9th house)
    gold_score = 3  # Base score
    gold_reasons = []
    if jupiter_house in [1, 2, 5, 9, 11]:
        gold_score += 2
        gold_reasons.append(f"गुरु भाव {jupiter_house} में - सोने से लाभ")
    if ninth_planets:
        gold_score += 1
        gold_reasons.append("9th भाव सक्रिय - भाग्य से धन")
    if "JUPITER" in ninth_planets or "JUPITER" in second_planets:
        gold_score += 1

    # Calculate Mutual Funds (Jupiter wisdom, 11th gains)
    mf_score = 3  # Base score
    mf_reasons = []
    if eleventh_planets:
        mf_score += 1
        mf_reasons.append("11th भाव में ग्रह - नियमित लाभ")
    if jupiter_house in [1, 5, 9, 11]:
        mf_score += 2
        mf_reasons.append("गुरु शुभ स्थान में - SIP से लाभ")

    # Cap scores at 5
    real_estate_score = min(5, real_estate_score)
    stocks_score = min(5, stocks_score)
    fd_score = min(5, fd_score)
    gold_score = min(5, gold_score)
    mf_score = min(5, mf_score)

    def stars(score):
        return "⭐" * score + "☆" * (5 - score)

    def get_reason(reasons, default):
        return reasons[0] if reasons else default

    html = f'''
    <div class="detail-box highlight-green">
        <h3>💹 आपके लिए निवेश सुझाव / Investment Suggestions FOR YOU</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #10b981;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 ये ratings आपकी कुंडली के आधार पर हैं / These ratings are based on YOUR chart:</strong><br>
                • <strong>4th भाव + शनि/मंगल</strong> = Real Estate suitability<br>
                • <strong>5th भाव + बुध/राहु</strong> = Stocks/Trading potential<br>
                • <strong>2nd भाव + शनि</strong> = Safe investments<br>
                • <strong>9th भाव + गुरु</strong> = Gold & fortune-based gains
            </p>
        </div>
        <table class="detail-table">
            <tr><th>निवेश प्रकार / Investment Type</th><th>आपके लिए / For You</th><th>कारण / Reason</th></tr>
            <tr>
                <td><strong>Real Estate</strong> (भूमि-भवन)</td>
                <td>{stars(real_estate_score)}</td>
                <td>{get_reason(real_estate_reasons, f"4th भाव का स्वामी {RASHI_LORDS.get(house_rashis.get(4, dict()).get('name', ''), ('', ''))[1]} की दशा में")}</td>
            </tr>
            <tr>
                <td><strong>Mutual Funds</strong> (SIP)</td>
                <td>{stars(mf_score)}</td>
                <td>{get_reason(mf_reasons, f"11th भाव का स्वामी {RASHI_LORDS.get(house_rashis.get(11, dict()).get('name', ''), ('', ''))[1]} की दशा में")}</td>
            </tr>
            <tr>
                <td><strong>Fixed Deposits</strong> (FD)</td>
                <td>{stars(fd_score)}</td>
                <td>{get_reason(fd_reasons, f"2nd भाव का स्वामी {RASHI_LORDS.get(house_rashis.get(2, dict()).get('name', ''), ('', ''))[1]} की दशा में")}</td>
            </tr>
            <tr>
                <td><strong>Stocks</strong> (शेयर/Trading)</td>
                <td>{stars(stocks_score)}</td>
                <td>{get_reason(stocks_reasons, f"5th भाव का स्वामी {RASHI_LORDS.get(house_rashis.get(5, dict()).get('name', ''), ('', ''))[1]} की दशा में")}</td>
            </tr>
            <tr>
                <td><strong>Gold</strong> (सोना)</td>
                <td>{stars(gold_score)}</td>
                <td>{get_reason(gold_reasons, f"9th भाव का स्वामी {RASHI_LORDS.get(house_rashis.get(9, dict()).get('name', ''), ('', ''))[1]} की दशा में")}</td>
            </tr>
        </table>
    </div>
    '''
    return html


def get_property_timing_html(house_rashis, planets_in_houses, lagna=None):
    """Calculate actual property timing based on 4th house lord - NOT generic text."""
    if lagna is None:
        raise ValueError("lagna parameter is required for accurate property timing")
    fourth_rashi = house_rashis.get(4, {}).get('name', '')
    fourth_lord = RASHI_LORDS.get(fourth_rashi, ("", ""))
    fourth_lord_hindi = fourth_lord[0]
    fourth_lord_english = fourth_lord[1]

    # Check if Saturn is in 4th house (strong for property)
    saturn_in_4th = "SATURN" in planets_in_houses.get(4, [])
    # Check if Mars is in 4th house (land)
    mars_in_4th = "MARS" in planets_in_houses.get(4, [])
    # Check if 4th lord is in good houses (1, 4, 7, 10 - Kendra)
    fourth_lord_house = 0
    for house, planets in planets_in_houses.items():
        if fourth_lord_english.upper() in planets:
            fourth_lord_house = house
            break

    kendra_houses = [1, 4, 7, 10]
    fourth_lord_strong = fourth_lord_house in kendra_houses

    html = '<ul class="prediction-list">'

    # Dynamic analysis based on actual chart
    html += f'''
        <li><span class="status-good">✅</span> <strong>आपके चतुर्थेश / Your 4th Lord:</strong> {fourth_lord_hindi} ({fourth_lord_english})<br>
        <span style="font-size: 12px; color: #666;">↳ {fourth_lord_hindi} की महादशा/अंतर्दशा में संपत्ति खरीदना शुभ<br>
        <em>Property purchase is auspicious during {fourth_lord_english}'s Mahadasha/Antardasha period</em></span></li>
    '''

    if fourth_lord_house:
        html += f'''
        <li><span class="status-good">✅</span> <strong>चतुर्थेश {fourth_lord_hindi} भाव {fourth_lord_house} में / 4th Lord in House {fourth_lord_house}</strong><br>
        <span style="font-size: 12px; color: #666;">↳ {'केंद्र में होने से संपत्ति योग प्रबल / Strong property yoga as 4th lord is in Kendra' if fourth_lord_strong else 'संपत्ति प्राप्ति संभव / Property acquisition possible'}</span></li>
        '''

    if saturn_in_4th:
        html += '''
        <li><span class="status-good">✅</span> <strong>शनि चतुर्थ भाव में / Saturn in 4th House</strong><br>
        <span style="font-size: 12px; color: #666;">↳ पुरानी संपत्ति, विरासत में प्राप्ति संभव / Old property, inheritance possible</span></li>
        '''

    if mars_in_4th:
        html += '''
        <li><span class="status-good">✅</span> <strong>मंगल चतुर्थ भाव में / Mars in 4th House</strong><br>
        <span style="font-size: 12px; color: #666;">↳ भूमि (land) से लाभ, लेकिन विवाद से बचें / Gains from land, but avoid disputes</span></li>
        '''

    # Saturn's dasha for property - CHECK IF SATURN IS BENEFIC FOR THIS LAGNA
    saturn_effect = get_lagna_specific_dasha_effect("Saturn", lagna)
    if saturn_effect['is_benefic'] or saturn_effect['is_yogakaraka']:
        saturn_status = "शुभ" if saturn_effect['is_benefic'] else "योगकारक - अत्यंत शुभ!"
        html += f'''
        <li><span class="status-good">✅</span> <strong>शनि की दशा / Saturn's Dasha Period ({saturn_status})</strong><br>
        <span style="font-size: 12px; color: #059669;">↳ आपके {lagna} लग्न के लिए शनि {saturn_effect['status_hindi']} है - शनि दशा में property investment बहुत शुभ!<br>
        <em>Saturn is {saturn_effect['status_en']} for your {lagna} lagna - excellent for property in Saturn period!</em></span></li>
    '''
    else:
        html += f'''
        <li><span class="status-warning">⚠️</span> <strong>शनि की दशा / Saturn's Dasha Period (सावधानी)</strong><br>
        <span style="font-size: 12px; color: #dc2626;">↳ आपके {lagna} लग्न के लिए शनि कठिन ग्रह है - शनि दशा में property decision सोच-समझ कर लें<br>
        <em>Saturn is challenging for your {lagna} lagna - be careful with property decisions in Saturn period</em></span></li>
    '''

    html += '</ul>'
    return html


def get_full_career_analysis(kundali, planets_in_houses, house_rashis, rashi_hindi):
    """Generate comprehensive career analysis."""
    lagna = kundali.lagna['rashi']
    tenth_rashi = house_rashis[10]['name']
    second_planets = planets_in_houses.get(2, [])
    sixth_planets = planets_in_houses.get(6, [])
    tenth_planets = planets_in_houses.get(10, [])
    eleventh_planets = planets_in_houses.get(11, [])

    # Calculate actual Lagna Lord and 10th Lord from chart
    lagna_lord = RASHI_LORDS.get(lagna, ("", ""))
    lagna_lord_hindi = lagna_lord[0]
    lagna_lord_english = lagna_lord[1]
    tenth_lord = RASHI_LORDS.get(tenth_rashi, ("", ""))
    tenth_lord_hindi = tenth_lord[0]
    tenth_lord_english = tenth_lord[1]

    # Find key planet positions
    sun_house = moon_house = mars_house = mercury_house = jupiter_house = venus_house = saturn_house = rahu_house = ketu_house = 0
    for h, planets in planets_in_houses.items():
        if "SUN" in planets: sun_house = h
        if "MOON" in planets: moon_house = h
        if "MARS" in planets: mars_house = h
        if "MERCURY" in planets: mercury_house = h
        if "JUPITER" in planets: jupiter_house = h
        if "VENUS" in planets: venus_house = h
        if "SATURN" in planets: saturn_house = h
        if "RAHU" in planets: rahu_house = h
        if "KETU" in planets: ketu_house = h

    # House meanings for explanation
    HOUSE_MEANINGS = {
        1: ("प्रथम भाव / 1st House", "व्यक्तित्व, शरीर, आत्म-छवि", "Personality, Body, Self-image", "यह भाव आपके व्यक्तित्व और जीवन के तरीके को दर्शाता है"),
        2: ("द्वितीय भाव / 2nd House", "धन, परिवार, वाणी", "Wealth, Family, Speech", "यह भाव आपकी कमाई और बचत को दर्शाता है"),
        3: ("तृतीय भाव / 3rd House", "साहस, भाई-बहन, संचार", "Courage, Siblings, Communication", "यह भाव आपके प्रयासों और संचार कौशल को दर्शाता है"),
        4: ("चतुर्थ भाव / 4th House", "माता, घर, सुख, वाहन", "Mother, Home, Comfort, Vehicles", "यह भाव आपके घरेलू सुख और संपत्ति को दर्शाता है"),
        5: ("पंचम भाव / 5th House", "संतान, बुद्धि, शिक्षा", "Children, Intelligence, Education", "यह भाव आपकी बुद्धि और रचनात्मकता को दर्शाता है"),
        6: ("षष्ठम भाव / 6th House", "शत्रु, रोग, नौकरी, प्रतिस्पर्धा", "Enemies, Disease, Job, Competition", "यह भाव नौकरी, दैनिक कार्य और प्रतिस्पर्धा को दर्शाता है"),
        7: ("सप्तम भाव / 7th House", "विवाह, साझेदारी, व्यापार", "Marriage, Partnership, Business", "यह भाव विवाह और व्यापारिक साझेदारी को दर्शाता है"),
        8: ("अष्टम भाव / 8th House", "आयु, रहस्य, अचानक लाभ/हानि", "Longevity, Secrets, Sudden gains/losses", "यह भाव अप्रत्याशित घटनाओं और विरासत को दर्शाता है"),
        9: ("नवम भाव / 9th House", "भाग्य, धर्म, पिता, विदेश यात्रा", "Fortune, Religion, Father, Foreign travel", "यह भाव आपके भाग्य और उच्च शिक्षा को दर्शाता है"),
        10: ("दशम भाव / 10th House", "करियर, पेशा, प्रसिद्धि, सामाजिक स्थिति", "Career, Profession, Fame, Social status", "यह सबसे महत्वपूर्ण भाव है करियर के लिए - यह आपके पेशे और सफलता को दर्शाता है"),
        11: ("एकादश भाव / 11th House", "लाभ, आय, इच्छा पूर्ति", "Gains, Income, Fulfillment of desires", "यह भाव आपकी आय और सफलता को दर्शाता है"),
        12: ("द्वादश भाव / 12th House", "व्यय, विदेश, मोक्ष", "Expenses, Foreign lands, Spirituality", "यह भाव विदेश और आध्यात्मिकता को दर्शाता है"),
    }

    html = f'''
    <div class="detail-box">
        <h3>🎯 लग्न आधारित करियर विश्लेषण / Ascendant-based Career Analysis</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); padding: 15px; border-radius: 10px; margin-bottom: 15px; border-left: 4px solid #3b82f6;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 लग्न क्या है और करियर से कैसे जुड़ा है? / What is Lagna and how does it relate to Career?</strong><br><br>
                <strong>लग्न (Ascendant)</strong> वह राशि है जो आपके जन्म के समय पूर्व दिशा में उदय हो रही थी। यह आपके व्यक्तित्व,
                स्वभाव और जीवन के तरीके को निर्धारित करता है। <strong>आपकी लग्न राशि के गुण बताते हैं कि आप किस प्रकार के काम में
                स्वाभाविक रूप से अच्छे होंगे।</strong><br><br>
                <em>Lagna (Ascendant) is the zodiac sign rising in the east at your birth time. It determines your personality,
                nature and approach to life. <strong>Your Lagna sign's qualities indicate what type of work you'll naturally excel at.</strong></em>
            </p>
        </div>
        <table class="detail-table">
            <tr>
                <td><strong>आपकी लग्न राशि / Your Ascendant</strong></td>
                <td><span style="font-size: 16px; font-weight: bold; color: #ea580c;">{rashi_hindi.get(lagna, lagna)} ({lagna})</span></td>
            </tr>
            <tr>
                <td><strong>उपयुक्त क्षेत्र / Suitable Fields</strong></td>
                <td>{CAREER_BY_LAGNA.get(lagna, 'विविध क्षेत्र')}<br>
                <span style="font-size: 11px; color: #666;">↳ आपकी लग्न राशि के गुणों के अनुसार ये क्षेत्र आपके लिए स्वाभाविक रूप से अनुकूल हैं<br>
                <em>These fields naturally suit your ascendant sign's qualities</em></span></td>
            </tr>
            <tr>
                <td><strong>दशम भाव की राशि / 10th House Sign</strong></td>
                <td>{rashi_hindi.get(tenth_rashi, tenth_rashi)} ({tenth_rashi})<br>
                <span style="font-size: 11px; color: #666;">↳ दशम भाव (10वां घर) = करियर का घर। इस राशि के गुण आपके पेशे को प्रभावित करते हैं<br>
                <em>10th house = Career house. This sign's qualities influence your profession</em></span></td>
            </tr>
        </table>
    </div>

    <div class="detail-box highlight-green">
        <h3>📊 दशम भाव (करियर स्थान) विश्लेषण / 10th House (Career House) Analysis</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); padding: 15px; border-radius: 10px; margin-bottom: 15px; border-left: 4px solid #10b981;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 दशम भाव (10वां घर) क्यों सबसे महत्वपूर्ण है? / Why is the 10th House most important?</strong><br><br>
                कुंडली में <strong>12 भाव (घर)</strong> होते हैं, जिनमें से <strong>दशम भाव (10वां घर)</strong> करियर, पेशा, सामाजिक प्रतिष्ठा
                और जीवन में सफलता का प्रतिनिधित्व करता है। इस भाव में जो ग्रह बैठे हों या इस पर जिन ग्रहों की दृष्टि हो,
                वे आपके करियर को सीधे प्रभावित करते हैं।<br><br>
                <em>A birth chart has <strong>12 houses</strong>, and the <strong>10th house</strong> represents career, profession,
                social status and success in life. Planets placed in or aspecting this house directly influence your career.</em>
            </p>
        </div>
    '''

    if tenth_planets:
        html += "<p><strong>🌟 आपके दशम भाव में ग्रह / Planets in your 10th House:</strong></p>"
        html += "<p style='font-size: 12px; color: #666; margin-bottom: 10px;'>दशम भाव में ग्रह होना शुभ है - यह करियर में विशेष सफलता का संकेत है। / Having planets in 10th house is auspicious - indicates special career success.</p>"
        html += "<ul class='prediction-list'>"
        for p in tenth_planets:
            hindi = PLANET_NAMES[Planet[p]]["hindi"]
            html += f'''<li>
                <strong>{hindi} ({p.title()}):</strong> {GRAHA_BHAVA_PHAL[p][10]}<br>
                <span style="font-size: 11px; color: #666;">↳ यह ग्रह आपके करियर को सीधे प्रभावित कर रहा है / This planet directly influences your career</span>
            </li>'''
        html += "</ul>"
    else:
        html += f'''
        <p style="padding: 10px; background: #fef3c7; border-radius: 6px;">
            <strong>📝 नोट / Note:</strong> आपके दशम भाव में कोई ग्रह नहीं है। यह सामान्य स्थिति है - लगभग 60% लोगों की कुंडली में ऐसा होता है।
            इस स्थिति में <strong>दशमेश</strong> (दशम भाव का स्वामी ग्रह) की स्थिति महत्वपूर्ण होती है।<br>
            <em>Your 10th house has no planets. This is normal - about 60% of charts are like this.
            In this case, the <strong>10th lord's</strong> (ruler of 10th house) position becomes important.</em><br><br>
            आपका दशमेश: <strong>{rashi_hindi.get(tenth_rashi, tenth_rashi)}</strong> राशि का स्वामी ग्रह
        </p>
        '''
    html += "</div>"

    # 2nd house analysis for wealth from career
    if second_planets:
        html += f'''
        <div class="detail-box highlight-gold">
            <h3>💰 द्वितीय भाव में {len(second_planets)} ग्रह - विशेष धन योग! / {len(second_planets)} Planets in 2nd House - Special Wealth Yoga!</h3>
            <div class="info-note" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #f59e0b;">
                <p style="margin: 0; font-size: 13px;">
                    <strong>💡 द्वितीय भाव (2nd House) क्या है? / What is the 2nd House?</strong><br>
                    द्वितीय भाव <strong>धन, बैंक बैलेंस, परिवार और वाणी</strong> का घर है। इस भाव में ग्रह होना धन कमाने की
                    विशेष क्षमता देता है। जितने अधिक शुभ ग्रह यहां होंगे, उतने अधिक आय के स्रोत होंगे।<br>
                    <em>2nd house represents <strong>wealth, bank balance, family and speech</strong>. Planets here give special
                    ability to earn money. More benefic planets here = more income sources.</em>
                </p>
            </div>
            <p><strong>🎉 बधाई! यह अत्यंत शक्तिशाली योग है / Congratulations! This is a powerful yoga:</strong></p>
            <table class="detail-table">
                <tr><th>ग्रह / Planet</th><th>धन स्रोत / Income Source</th><th>विस्तृत फल / Detailed Effect</th></tr>
        '''
        wealth_sources = {
            "SUN": ("Government, Authority", "सरकारी क्षेत्र, उच्च पद, पिता से धन / Govt sector, high position, wealth from father"),
            "MOON": ("Public, Liquids", "जनता से जुड़े कार्य, तरल पदार्थ, माता से धन / Public dealing, liquids business, wealth from mother"),
            "MARS": ("Technical, Property", "तकनीकी कार्य, भूमि-भवन, भाई से सहयोग / Technical work, real estate, support from siblings"),
            "MERCURY": ("Business, IT", "व्यापार, IT, संचार, लेखन से धन / Business, IT, communication, writing"),
            "JUPITER": ("Teaching, Finance", "शिक्षा, बैंकिंग, परामर्श, गुरु कृपा / Education, banking, consulting, divine blessings"),
            "VENUS": ("Arts, Luxury", "कला, फैशन, सौंदर्य, विलासिता / Arts, fashion, beauty, luxury goods"),
            "SATURN": ("Labor, Mining", "मेहनत, खनन, कृषि, सेवा क्षेत्र / Hard work, mining, agriculture, service sector"),
            "RAHU": ("Foreign, Tech", "विदेश, अपारंपरिक, तकनीक / Foreign sources, unconventional, technology"),
            "KETU": ("Spiritual, Occult", "आध्यात्मिक, गुप्त विद्या / Spiritual work, occult sciences"),
        }
        for p in second_planets:
            hindi = PLANET_NAMES[Planet[p]]["hindi"]
            src = wealth_sources.get(p, ("", ""))
            html += f"<tr><td><strong>{hindi}</strong></td><td>{src[0]}</td><td>{src[1]}</td></tr>"
        html += "</table></div>"

    # Sun position for government jobs
    sun_house_info = HOUSE_MEANINGS.get(sun_house, ("", "", "", ""))
    saturn_house_info = HOUSE_MEANINGS.get(saturn_house, ("", "", "", ""))
    mercury_house_info = HOUSE_MEANINGS.get(mercury_house, ("", "", "", ""))

    html += f'''
    <div class="detail-box">
        <h3>☉ सूर्य की स्थिति / Sun's Position - {sun_house_info[0]}</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #f59e0b;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 सूर्य करियर में क्यों महत्वपूर्ण है? / Why is Sun important for Career?</strong><br>
                सूर्य <strong>सरकारी नौकरी, अधिकार, नेतृत्व और पिता</strong> का कारक है। सूर्य की स्थिति बताती है कि आपको
                सरकारी क्षेत्र में कितनी सफलता मिलेगी और आपकी leadership क्षमता कैसी है।<br>
                <em>Sun signifies <strong>government job, authority, leadership and father</strong>. Sun's position reveals
                your success in government sector and leadership ability.</em>
            </p>
        </div>
        <table class="detail-table">
            <tr>
                <td><strong>सूर्य का भाव / Sun's House</strong></td>
                <td><strong>भाव {sun_house}</strong> - {sun_house_info[1]}<br>
                <span style="font-size: 11px; color: #666;">({sun_house_info[2]})</span></td>
            </tr>
            <tr>
                <td><strong>इस भाव का अर्थ / House Meaning</strong></td>
                <td>{sun_house_info[3]}</td>
            </tr>
            <tr>
                <td><strong>सूर्य का प्रभाव / Sun's Effect</strong></td>
                <td>{GRAHA_BHAVA_PHAL['SUN'][sun_house]}</td>
            </tr>
            <tr>
                <td><strong>सरकारी नौकरी / Government Job</strong></td>
                <td>{'✅ <strong>अनुकूल</strong> - सरकारी क्षेत्र में सफलता संभव / Favorable - Success in govt sector possible' if sun_house in [1, 9, 10, 11] else '⚠️ प्रयास आवश्यक / Extra effort needed'}</td>
            </tr>
        </table>
    </div>

    <div class="detail-box">
        <h3>♄ शनि की स्थिति / Saturn's Position - {saturn_house_info[0]}</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%); padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #6366f1;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 शनि करियर में क्यों महत्वपूर्ण है? / Why is Saturn important for Career?</strong><br>
                शनि <strong>मेहनत, अनुशासन, धीरे-धीरे सफलता और स्थिरता</strong> का कारक है। शनि देर से फल देता है लेकिन
                स्थायी सफलता देता है। <strong>शनि की महादशा/अंतर्दशा</strong> में करियर में स्थिरता आती है।<br>
                <em>Saturn signifies <strong>hard work, discipline, gradual success and stability</strong>. Saturn gives delayed
                but permanent results. Career stability comes during <strong>Saturn's Mahadasha/Antardasha</strong>.</em>
            </p>
        </div>
        <table class="detail-table">
            <tr>
                <td><strong>शनि का भाव / Saturn's House</strong></td>
                <td><strong>भाव {saturn_house}</strong> - {saturn_house_info[1]}<br>
                <span style="font-size: 11px; color: #666;">({saturn_house_info[2]})</span></td>
            </tr>
            <tr>
                <td><strong>इस भाव का अर्थ / House Meaning</strong></td>
                <td>{saturn_house_info[3]}</td>
            </tr>
            <tr>
                <td><strong>शनि का प्रभाव / Saturn's Effect</strong></td>
                <td>{GRAHA_BHAVA_PHAL['SATURN'][saturn_house]}</td>
            </tr>
            <tr>
                <td><strong>करियर टाइमिंग / Career Timing</strong></td>
                <td>⏰ <strong>शनि की दशा (19 वर्ष)</strong> में मुख्य करियर सफलता - अपनी दशा देखें<br>
                <span style="font-size: 11px; color: #666;">Main career success in <strong>Saturn's Dasha (19 years)</strong> - check your Dasha section</span></td>
            </tr>
        </table>
    </div>

    <div class="detail-box">
        <h3>☿ बुध की स्थिति / Mercury's Position - {mercury_house_info[0]}</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #10b981;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 बुध करियर में क्यों महत्वपूर्ण है? / Why is Mercury important for Career?</strong><br>
                बुध <strong>व्यापार, IT, संचार, लेखन और बुद्धि</strong> का कारक है। आज के युग में IT, Marketing, Content Writing,
                Business जैसे क्षेत्रों में सफलता के लिए बुध की स्थिति बहुत महत्वपूर्ण है।<br>
                <em>Mercury signifies <strong>business, IT, communication, writing and intelligence</strong>. In today's era,
                Mercury's position is crucial for success in IT, Marketing, Content Writing, Business fields.</em>
            </p>
        </div>
        <table class="detail-table">
            <tr>
                <td><strong>बुध का भाव / Mercury's House</strong></td>
                <td><strong>भाव {mercury_house}</strong> - {mercury_house_info[1]}<br>
                <span style="font-size: 11px; color: #666;">({mercury_house_info[2]})</span></td>
            </tr>
            <tr>
                <td><strong>इस भाव का अर्थ / House Meaning</strong></td>
                <td>{mercury_house_info[3]}</td>
            </tr>
            <tr>
                <td><strong>बुध का प्रभाव / Mercury's Effect</strong></td>
                <td>{GRAHA_BHAVA_PHAL['MERCURY'][mercury_house]}</td>
            </tr>
            <tr>
                <td><strong>व्यापार/IT योग्यता / Business/IT Aptitude</strong></td>
                <td>{'✅ <strong>बहुत अनुकूल</strong> - व्यापार और IT में उत्कृष्ट सफलता / Highly favorable for Business & IT' if mercury_house in [1, 2, 4, 5, 7, 9, 10, 11] else '⚠️ सामान्य - अतिरिक्त प्रयास से सफलता / Average - success with extra effort'}</td>
            </tr>
        </table>
    </div>
    '''

    # Career predictions based on lagna
    LAGNA_CAREERS = {
        "Mesha": [("Military/Police", "⭐⭐⭐⭐⭐", "मंगल लग्नेश"), ("Sports", "⭐⭐⭐⭐⭐", "ऊर्जा प्रधान"), ("Surgery", "⭐⭐⭐⭐", "मंगल का प्रभाव"), ("Engineering", "⭐⭐⭐⭐", "तकनीकी योग्यता")],
        "Vrishabha": [("Finance/Banking", "⭐⭐⭐⭐⭐", "शुक्र लग्नेश"), ("Arts/Music", "⭐⭐⭐⭐⭐", "कलात्मक प्रतिभा"), ("Luxury Goods", "⭐⭐⭐⭐", "शुक्र का प्रभाव"), ("Hospitality", "⭐⭐⭐⭐", "सेवा भाव")],
        "Mithuna": [("IT/Software", "⭐⭐⭐⭐⭐", "बुध लग्नेश"), ("Communication", "⭐⭐⭐⭐⭐", "वाणी कौशल"), ("Writing/Media", "⭐⭐⭐⭐", "बुध का प्रभाव"), ("Trading", "⭐⭐⭐⭐", "व्यापार योग्यता")],
        "Karka": [("Hospitality", "⭐⭐⭐⭐⭐", "चंद्र लग्नेश"), ("Nursing/Care", "⭐⭐⭐⭐⭐", "सेवा भाव"), ("Real Estate", "⭐⭐⭐⭐", "4th भाव संबंध"), ("Food Industry", "⭐⭐⭐⭐", "पोषण से जुड़ाव")],
        "Simha": [("Politics", "⭐⭐⭐⭐⭐", "सूर्य लग्नेश"), ("Entertainment", "⭐⭐⭐⭐⭐", "नेतृत्व गुण"), ("Administration", "⭐⭐⭐⭐", "अधिकार योग"), ("Government", "⭐⭐⭐⭐", "सूर्य का प्रभाव")],
        "Kanya": [("IT/Software", "⭐⭐⭐⭐⭐", "बुध लग्नेश"), ("Data Science", "⭐⭐⭐⭐⭐", "विश्लेषण क्षमता"), ("Medical", "⭐⭐⭐⭐", "स्वास्थ्य से जुड़ाव"), ("Accounting", "⭐⭐⭐⭐", "गणितीय योग्यता")],
        "Tula": [("Law", "⭐⭐⭐⭐⭐", "शुक्र लग्नेश, न्याय भाव"), ("Diplomacy", "⭐⭐⭐⭐⭐", "संतुलन गुण"), ("Fashion", "⭐⭐⭐⭐", "सौंदर्य बोध"), ("Interior Design", "⭐⭐⭐⭐", "कलात्मक दृष्टि")],
        "Vrishchika": [("Research", "⭐⭐⭐⭐⭐", "मंगल लग्नेश"), ("Surgery", "⭐⭐⭐⭐⭐", "गहन विश्लेषण"), ("Detective/CBI", "⭐⭐⭐⭐", "रहस्य जानने की क्षमता"), ("Occult", "⭐⭐⭐⭐", "8th भाव प्रभाव")],
        "Dhanu": [("Teaching", "⭐⭐⭐⭐⭐", "गुरु लग्नेश"), ("Law", "⭐⭐⭐⭐⭐", "धर्म-न्याय"), ("Religion/Philosophy", "⭐⭐⭐⭐", "आध्यात्मिक झुकाव"), ("Publishing", "⭐⭐⭐⭐", "ज्ञान प्रसार")],
        "Makara": [("Government", "⭐⭐⭐⭐⭐", "शनि लग्नेश"), ("Administration", "⭐⭐⭐⭐⭐", "अनुशासन"), ("Real Estate", "⭐⭐⭐⭐", "भूमि से संबंध"), ("Mining", "⭐⭐⭐⭐", "पृथ्वी तत्व")],
        "Kumbha": [("IT/Technology", "⭐⭐⭐⭐⭐", "शनि लग्नेश"), ("Electronics", "⭐⭐⭐⭐⭐", "नवीनता"), ("Social Work", "⭐⭐⭐⭐", "समाज सेवा"), ("Aviation", "⭐⭐⭐⭐", "वायु तत्व")],
        "Meena": [("Spirituality", "⭐⭐⭐⭐⭐", "गुरु लग्नेश"), ("Art/Music", "⭐⭐⭐⭐⭐", "कल्पनाशीलता"), ("Hospital/Charity", "⭐⭐⭐⭐", "सेवा भाव"), ("Film/Media", "⭐⭐⭐⭐", "रचनात्मकता")],
    }

    career_options = LAGNA_CAREERS.get(lagna, [("General", "⭐⭐⭐", "विविध क्षेत्र")])

    # Also check 10th house planets to modify ratings
    tenth_house_bonus = ""
    if tenth_planets:
        tenth_planet_names = [PLANET_NAMES[Planet[p]]["hindi"] for p in tenth_planets]
        tenth_house_bonus = f" (10वें भाव में: {', '.join(tenth_planet_names)} - और भी अनुकूल!)"

    html += f'''
    <div class="detail-box">
        <h3>📋 {rashi_hindi.get(lagna, lagna)} ({lagna}) लग्न के लिए करियर सुझाव / Career Suggestions for your Ascendant</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #f59e0b;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 यह सुझाव कैसे काम करते हैं? / How do these suggestions work?</strong><br>
                हर लग्न राशि के कुछ विशेष गुण होते हैं। जैसे मेष लग्न के लोग साहसी होते हैं (इसलिए Military/Police अच्छा),
                मिथुन लग्न के लोग बुद्धिमान होते हैं (इसलिए IT/Communication अच्छा)। ये सुझाव आपकी <strong>प्राकृतिक प्रतिभाओं</strong>
                के अनुसार हैं।{tenth_house_bonus}<br>
                <em>Each ascendant has unique qualities. These suggestions match your <strong>natural talents</strong>. Your 10th lord ({tenth_lord_english}) and 10th house analysis is shown below for more specific timing.</em>
            </p>
        </div>
        <table class="detail-table">
            <tr><th>क्षेत्र / Field</th><th>अनुकूलता / Suitability</th><th>कारण / Reason</th></tr>
    '''

    for career, rating, reason in career_options:
        html += f"<tr><td><strong>{career}</strong></td><td>{rating}</td><td>{reason}</td></tr>"

    html += '''
        </table>
    </div>
    '''

    html += f'''
    <div class="detail-box highlight-blue">
        <h3>⏰ करियर टाइमिंग विश्लेषण / Career Timing Analysis</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); padding: 15px; border-radius: 10px; margin-bottom: 15px; border-left: 4px solid #3b82f6;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 दशा क्या है और करियर से कैसे जुड़ी है? / What is Dasha and how does it relate to Career?</strong><br><br>
                <strong>दशा</strong> एक ग्रह का शासनकाल होता है जो 6-20 वर्ष तक चलता है। जीवन में जो भी बड़े परिवर्तन होते हैं
                (नौकरी लगना, प्रमोशन, बिज़नेस शुरू होना) वे अक्सर किसी विशेष ग्रह की दशा में होते हैं।<br><br>
                <strong>महादशा</strong> = मुख्य ग्रह का समय (6-20 वर्ष)<br>
                <strong>अंतर्दशा</strong> = महादशा के अंदर छोटे ग्रहों का समय (कुछ महीने से कुछ वर्ष)<br><br>
                <em><strong>Dasha</strong> is a planetary period lasting 6-20 years. Major life changes (getting job, promotion,
                starting business) often happen during specific planetary periods.</em>
            </p>
        </div>
        <p><em>विस्तृत समय के लिए नीचे दशा विश्लेषण खंड देखें। / See Dasha Analysis section below for detailed timing.</em></p>
        <p><strong>आपके करियर के लिए शुभ दशाएं / Favorable Dashas for YOUR Career:</strong></p>
        <ul class="prediction-list">
            <li>
                <strong>🌟 आपके लग्नेश {lagna_lord_hindi} ({lagna_lord_english}) की दशा - सबसे महत्वपूर्ण!</strong><br>
                <span style="font-size: 12px; color: #666;">↳ {lagna_lord_hindi} आपके व्यक्तित्व का स्वामी है ({lagna} लग्न) - इसकी दशा में व्यक्तिगत उन्नति और पहचान मिलती है<br>
                <em>{lagna_lord_english} rules your personality ({lagna} ascendant) - its period brings personal growth & recognition</em></span>
            </li>
            <li>
                <strong>🎯 आपके दशमेश {tenth_lord_hindi} ({tenth_lord_english}) की दशा - करियर के लिए!</strong><br>
                <span style="font-size: 12px; color: #666;">↳ {tenth_lord_hindi} आपके करियर का स्वामी है ({tenth_rashi} 10वें भाव में) - इसकी दशा में करियर में मुख्य प्रगति होती है<br>
                <em>{tenth_lord_english} rules your career ({tenth_rashi} in 10th) - its period brings major career progress</em></span>
            </li>
    '''

    # Add LAGNA-SPECIFIC beneficial dashas (not generic Jupiter/Saturn/Mercury for everyone)
    jupiter_effect = get_lagna_specific_dasha_effect("Jupiter", lagna)
    saturn_effect = get_lagna_specific_dasha_effect("Saturn", lagna)
    mercury_effect = get_lagna_specific_dasha_effect("Mercury", lagna)

    # Only show planets that are BENEFIC for this specific lagna
    if jupiter_effect['is_benefic'] or jupiter_effect['is_yogakaraka']:
        html += f'''
            <li>
                <strong>♃ गुरु की दशा / Jupiter's Dasha (16 वर्ष) - {jupiter_effect['status_hindi']}</strong><br>
                <span style="font-size: 12px; color: #059669;">↳ आपके {lagna} लग्न के लिए गुरु शुभ ग्रह है (भाव {jupiter_effect['houses_ruled']} का स्वामी)<br>
                <em>Jupiter is benefic for your {lagna} lagna (rules houses {jupiter_effect['houses_ruled']}) - good for career</em></span>
            </li>'''

    if saturn_effect['is_benefic'] or saturn_effect['is_yogakaraka']:
        yogakaraka_note = " (योगकारक!)" if saturn_effect['is_yogakaraka'] else ""
        html += f'''
            <li>
                <strong>♄ शनि की दशा / Saturn's Dasha (19 वर्ष) - {saturn_effect['status_hindi']}{yogakaraka_note}</strong><br>
                <span style="font-size: 12px; color: #059669;">↳ आपके {lagna} लग्न के लिए शनि शुभ ग्रह है (भाव {saturn_effect['houses_ruled']} का स्वामी)<br>
                <em>Saturn is benefic for your {lagna} lagna (rules houses {saturn_effect['houses_ruled']}) - excellent for career stability</em></span>
            </li>'''
    else:
        html += f'''
            <li>
                <strong>♄ शनि की दशा / Saturn's Dasha (19 वर्ष) - {saturn_effect['status_hindi']}</strong><br>
                <span style="font-size: 12px; color: #dc2626;">↳ आपके {lagna} लग्न के लिए शनि कठिन ग्रह है - करियर में मेहनत ज्यादा, फल धीरे<br>
                <em>Saturn is challenging for your {lagna} lagna - more effort needed, slow results. Do Saturn remedies.</em></span>
            </li>'''

    if mercury_effect['is_benefic'] or mercury_effect['is_yogakaraka']:
        html += f'''
            <li>
                <strong>☿ बुध की दशा / Mercury's Dasha (17 वर्ष) - {mercury_effect['status_hindi']}</strong><br>
                <span style="font-size: 12px; color: #059669;">↳ आपके {lagna} लग्न के लिए बुध शुभ ग्रह है - Business/IT में अच्छे अवसर<br>
                <em>Mercury is benefic for your {lagna} lagna - great for Business/IT/Communication</em></span>
            </li>'''

    html += '''
        </ul>
    </div>
    '''

    return html


def get_full_marriage_analysis(kundali, planets_in_houses, house_rashis, rashi_hindi):
    """Generate comprehensive marriage analysis."""
    lagna = kundali.lagna.get('rashi', 'Mesha')  # For lagna-specific Mars analysis
    seventh_rashi = house_rashis[7]['name']
    seventh_planets = planets_in_houses.get(7, [])

    # Get actual 7th house lord based on 7th rashi
    seventh_lord = RASHI_LORDS.get(seventh_rashi, ("", ""))
    seventh_lord_hindi = seventh_lord[0]
    seventh_lord_en = seventh_lord[1]

    # Find planet positions
    venus_house = jupiter_house = mars_house = moon_house = 0
    seventh_lord_house = 0
    planet_to_key = {"Mars": "MARS", "Venus": "VENUS", "Mercury": "MERCURY", "Moon": "MOON",
                     "Sun": "SUN", "Jupiter": "JUPITER", "Saturn": "SATURN"}
    seventh_lord_key = planet_to_key.get(seventh_lord_en, "")

    saturn_house = 0
    for h, planets in planets_in_houses.items():
        if "VENUS" in planets: venus_house = h
        if "JUPITER" in planets: jupiter_house = h
        if "MARS" in planets: mars_house = h
        if "MOON" in planets: moon_house = h
        if "SATURN" in planets: saturn_house = h
        if seventh_lord_key and seventh_lord_key in planets: seventh_lord_house = h

    # Check for Manglik dosha
    manglik_from_lagna = mars_house in [1, 4, 7, 8, 12]

    # Check for Manglik cancellations
    manglik_cancellations = []
    mars_rashi = ""
    for p in kundali.planets:
        if hasattr(p, 'name') and p.name.upper() == "MARS":
            mars_rashi = p.rashi
        elif isinstance(kundali.planets, dict):
            mars_rashi = kundali.planets.get('MARS', {}).get('rashi', '')
            break

    # Cancellation 1: Shani Manglik (Saturn in 1, 4, 7, 8, 12)
    if saturn_house in [1, 4, 7, 8, 12]:
        manglik_cancellations.append(f"शनि मांगलिक (शनि भाव {saturn_house} में) - दोष परस्पर निवारण")

    # Cancellation 2: Jupiter in Kendra
    if jupiter_house in [1, 4, 7, 10]:
        manglik_cancellations.append(f"गुरु केंद्र में (भाव {jupiter_house}) - मांगलिक दोष शांत")

    # Cancellation 3: Venus in Kendra
    if venus_house in [1, 4, 7, 10]:
        manglik_cancellations.append(f"शुक्र केंद्र में (भाव {venus_house}) - मांगलिक दोष शांत")

    # Cancellation 4: Mars in own sign
    if mars_rashi in ['Mesha', 'Vrishchika']:
        manglik_cancellations.append(f"मंगल स्वराशि में - दोष क्षीण")

    # Cancellation 5: Mars exalted
    if mars_rashi == 'Makara':
        manglik_cancellations.append("मंगल उच्च राशि में - दोष क्षीण")

    # Final Manglik status
    manglik = manglik_from_lagna and len(manglik_cancellations) == 0
    manglik_cancelled = manglik_from_lagna and len(manglik_cancellations) > 0

    # Get dynamic spouse qualities based on 7th rashi
    spouse_qualities = SPOUSE_QUALITIES.get(seventh_rashi, ["जीवनसाथी गुणवान होगा/होगी"])

    # Determine marriage quality based on planetary positions
    marriage_good = venus_house in [1, 2, 4, 5, 7, 9, 11] or jupiter_house in [1, 5, 7, 9, 11]
    seventh_afflicted = "SATURN" in seventh_planets or "RAHU" in seventh_planets or "KETU" in seventh_planets

    html = f'''
    <div class="detail-box">
        <h3>💍 सप्तम भाव (विवाह स्थान) विश्लेषण / 7th House (Marriage House) Analysis</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%); padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #ec4899;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 सप्तम भाव क्या है? / What is the 7th House?</strong><br>
                कुंडली में 12 भाव (घर) होते हैं, जिनमें से <strong>सप्तम भाव (7वां घर)</strong> विवाह, जीवनसाथी और साझेदारी का प्रतिनिधित्व करता है।
                इस भाव की राशि और उसका स्वामी ग्रह (सप्तमेश) बताता है कि आपका जीवनसाथी कैसा होगा और वैवाहिक जीवन कैसा रहेगा।<br>
                <em>A birth chart has 12 houses, and the <strong>7th house</strong> represents marriage, spouse and partnerships.
                The zodiac sign in this house and its ruling planet (7th lord) reveal your spouse's nature and married life.</em>
            </p>
        </div>
        <table class="detail-table">
            <tr>
                <td><strong>सप्तम भाव राशि / 7th House Sign</strong></td>
                <td>{rashi_hindi.get(seventh_rashi, seventh_rashi)} ({seventh_rashi})</td>
            </tr>
            <tr>
                <td><strong>सप्तमेश / 7th House Lord</strong></td>
                <td>{seventh_lord_hindi} ({seventh_lord_en})<br>
                <span style="font-size: 11px; color: #666;">↳ यह ग्रह आपके विवाह भाग्य का स्वामी है / This planet rules your marriage destiny</span></td>
            </tr>
            <tr>
                <td><strong>सप्तमेश की स्थिति / 7th Lord Position</strong></td>
                <td>भाव {seventh_lord_house if seventh_lord_house else '-'} / House {seventh_lord_house if seventh_lord_house else '-'}<br>
                <span style="font-size: 11px; color: #666;">↳ सप्तमेश जिस भाव में बैठता है, वह विवाह को प्रभावित करता है / The house where 7th lord sits influences your marriage</span></td>
            </tr>
        </table>
    </div>

    <div class="detail-box">
        <h3>👫 जीवनसाथी के गुण / Spouse Characteristics</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #0ea5e9;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 यह कैसे निर्धारित होता है? / How is this determined?</strong><br>
                आपके सप्तम भाव (विवाह भाव) में जो राशि है, उसके गुणों के अनुसार आपके जीवनसाथी का स्वभाव और व्यक्तित्व होता है।
                यह एक सामान्य संकेत है - वास्तविक व्यक्तित्व कई कारकों पर निर्भर करता है।<br>
                <em>The zodiac sign in your 7th house (marriage house) indicates your spouse's nature and personality.
                This is a general indication - actual personality depends on many factors.</em>
            </p>
        </div>
        <p><strong>{rashi_hindi.get(seventh_rashi, seventh_rashi)} ({seventh_rashi}) राशि के अनुसार / According to this sign:</strong></p>
        <p>{MARRIAGE_PREDICTIONS.get(seventh_rashi, '')}</p>
        <ul class="prediction-list">
    '''

    for quality in spouse_qualities:
        html += f"<li>{quality}</li>"

    html += '''
        </ul>
    </div>
    '''

    if seventh_planets:
        html += '''<div class="detail-box"><h3>सप्तम भाव में ग्रह</h3><ul class="prediction-list">'''
        for p in seventh_planets:
            hindi = PLANET_NAMES[Planet[p]]["hindi"]
            html += f"<li><strong>{hindi}:</strong> {GRAHA_BHAVA_PHAL[p][7]}</li>"
        html += "</ul></div>"

    # Venus house quality explanation
    venus_quality = 'उत्तम / Excellent' if venus_house in [1, 2, 4, 5, 7, 9, 11] else 'सामान्य / Average'
    venus_explanation = ""
    if venus_house in [1, 2, 4, 5, 7, 9, 11]:
        venus_explanation = "शुक्र शुभ भाव में होने से प्रेम, रोमांस और वैवाहिक सुख प्रबल रहता है। / Venus in auspicious house indicates strong love, romance and marital happiness."
    else:
        venus_explanation = "शुक्र की स्थिति सामान्य है। विवाह में कुछ प्रयास की आवश्यकता हो सकती है। / Venus position is average. Some effort may be needed in marriage."

    html += f'''
    <div class="detail-box">
        <h3>♀ शुक्र (विवाह कारक) विश्लेषण / Venus (Marriage Significator) Analysis</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #f59e0b;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 शुक्र क्यों महत्वपूर्ण है? / Why Venus is Important?</strong><br>
                वैदिक ज्योतिष में शुक्र को <strong>विवाह का कारक ग्रह</strong> माना जाता है। यह प्रेम, सौंदर्य, रोमांस और वैवाहिक सुख का प्रतिनिधित्व करता है।
                शुक्र की स्थिति से पता चलता है कि व्यक्ति का प्रेम जीवन और विवाह कैसा रहेगा।<br>
                <em>In Vedic astrology, Venus is the <strong>significator of marriage</strong>. It represents love, beauty, romance and marital happiness.
                Venus's position reveals how your love life and marriage will be.</em>
            </p>
        </div>
        <table class="detail-table">
            <tr>
                <td><strong>शुक्र की स्थिति / Venus Position</strong></td>
                <td>भाव {venus_house} / House {venus_house}</td>
            </tr>
            <tr>
                <td><strong>शुक्र का प्रभाव / Venus Effect</strong></td>
                <td>{GRAHA_BHAVA_PHAL['VENUS'][venus_house]}</td>
            </tr>
            <tr>
                <td><strong>विवाह सुख / Marriage Happiness</strong></td>
                <td>{venus_quality}</td>
            </tr>
        </table>
        <p style="margin-top: 10px; padding: 8px; background: #f0fdf4; border-radius: 6px; font-size: 13px;">
            <strong>📝 विश्लेषण / Analysis:</strong> {venus_explanation}
        </p>
    </div>

    <div class="detail-box {'highlight-yellow' if manglik else 'highlight-green' if manglik_cancelled else ''}">
        <h3>♂ मांगलिक दोष विचार / Manglik Dosha Analysis</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%); padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #ef4444;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 मांगलिक दोष क्या है? / What is Manglik Dosha?</strong><br>
                जब मंगल ग्रह कुंडली के <strong>1, 4, 7, 8 या 12वें भाव</strong> में होता है, तो व्यक्ति को "मांगलिक" कहा जाता है।
                पारंपरिक मान्यता है कि मांगलिक व्यक्ति का विवाह किसी अन्य मांगलिक से होना चाहिए। हालांकि, कई स्थितियों में यह दोष <strong>स्वतः निरस्त</strong> हो जाता है।<br>
                <em>When Mars is in the <strong>1st, 4th, 7th, 8th or 12th house</strong>, the person is called "Manglik".
                Traditional belief suggests Manglik should marry another Manglik. However, this dosha is <strong>automatically cancelled</strong> in many situations.</em>
            </p>
        </div>
        <table class="detail-table">
            <tr>
                <td><strong>मंगल की स्थिति / Mars Position</strong></td>
                <td>भाव {mars_house} / House {mars_house}</td>
            </tr>
            <tr>
                <td><strong>मांगलिक दोष (लग्न से) / Manglik (from Lagna)</strong></td>
                <td>{'हां / Yes' if manglik_from_lagna else 'नहीं / No'}</td>
            </tr>
            <tr>
                <td><strong>दोष स्थिति / Dosha Status</strong></td>
                <td>{'❌ सक्रिय - विचार करें / Active - Consider' if manglik else '✅ निरस्त/शांत / Cancelled' if manglik_cancelled else '✅ नहीं है / Not Present'}</td>
            </tr>
        </table>
    '''

    if manglik_cancelled:
        html += '''
        <p><strong>🎉 मांगलिक दोष निरस्त है! कारण: / Manglik Dosha Cancelled! Reasons:</strong></p>
        <ul class="prediction-list">'''
        for reason in manglik_cancellations:
            html += f"<li><span class='status-good'>✅</span> {reason}</li>"
        html += '''
        </ul>
        <p style="padding: 8px; background: #f0fdf4; border-radius: 6px; font-size: 13px;">
            <em>इन कारणों से मांगलिक दोष का प्रभाव नगण्य है। आप किसी भी व्यक्ति से विवाह कर सकते हैं।<br>
            Due to these reasons, Manglik dosha effect is negligible. You can marry anyone.</em>
        </p>'''

    if manglik:
        # Check if Mars is benefic/yogakaraka for this lagna
        mars_effect = get_lagna_specific_dasha_effect("Mars", lagna)
        is_mars_benefic = mars_effect['is_benefic'] or mars_effect['is_yogakaraka']

        html += '''
        <p><strong>उपाय / Remedies:</strong></p>
        <ul class="prediction-list">'''

        if is_mars_benefic:
            # Mars is benefic - strengthen it
            html += f'''
            <li style="color: #059669;"><strong>मंगल आपके {lagna} लग्न के लिए शुभ ग्रह है</strong> - मंगल मंत्र जाप करें, मूंगा पहनना लाभकारी<br>
            <em>Mars is benefic for your {lagna} lagna - chant Mars mantra, wearing coral is beneficial</em></li>
            <li>मंगलवार को हनुमान जी की पूजा करें / Worship Lord Hanuman on Tuesdays</li>'''
        else:
            # Mars is malefic - pacify it
            html += f'''
            <li style="color: #dc2626;"><strong>मंगल आपके {lagna} लग्न के लिए कठिन ग्रह है</strong> - मूंगा न पहनें, हनुमान पूजा से शांति करें<br>
            <em>Mars is challenging for your {lagna} lagna - do NOT wear coral, pacify with Hanuman worship</em></li>
            <li>मंगलवार को हनुमान जी की पूजा करें (मंगल को शांत करता है) / Hanuman worship pacifies Mars</li>'''

        html += '''
            <li>कुंभ विवाह विचार करें / Consider Kumbh Vivah (symbolic marriage with a pot)</li>
            <li>मांगलिक से मांगलिक का विवाह श्रेष्ठ / Marriage with another Manglik is best</li>
        </ul>
        '''
    html += "</div>"

    html += f'''
    <div class="detail-box highlight-green">
        <h3>📅 विवाह समय विश्लेषण / Marriage Timing Analysis</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #10b981;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 दशा क्या है? / What is Dasha?</strong><br>
                दशा एक ग्रह का शासन काल होता है जो जीवन के विभिन्न पहलुओं को प्रभावित करता है।
                <strong>महादशा</strong> मुख्य ग्रह का समय (6-20 वर्ष) और <strong>अंतर्दशा</strong> उसके अंदर छोटे ग्रहों का समय होता है।<br>
                <em>Dasha is a planetary period that influences different aspects of life.
                <strong>Mahadasha</strong> is the main planet's period (6-20 years) and <strong>Antardasha</strong> is a sub-period within it.</em>
            </p>
        </div>
        <p><em>विस्तृत समय के लिए नीचे दशा विश्लेषण खंड देखें। / See Dasha Analysis section below for detailed timing.</em></p>
        <p><strong>विवाह के लिए शुभ दशाएं / Favorable Dashas for Marriage:</strong></p>
        <ul class="prediction-list">
            <li>
                <strong>{seventh_lord_hindi} (सप्तमेश) / {seventh_lord_en} (7th Lord)</strong> की महादशा/अंतर्दशा<br>
                <span style="font-size: 12px; color: #666;">↳ सप्तमेश विवाह भाव का स्वामी है, इसकी दशा में विवाह की प्रबल संभावना रहती है।<br>
                <em>The 7th lord rules the marriage house, so its period strongly indicates marriage.</em></span>
            </li>
            <li>
                <strong>शुक्र / Venus</strong> की दशा (विवाह कारक / Marriage Significator)<br>
                <span style="font-size: 12px; color: #666;">↳ शुक्र प्रेम और विवाह का नैसर्गिक कारक है, इसकी दशा में रोमांस और विवाह के योग बनते हैं।<br>
                <em>Venus is the natural significator of love and marriage, its period brings romance and marriage opportunities.</em></span>
            </li>
            <li>
                <strong>गुरु / Jupiter</strong> की दशा (शुभ ग्रह / Benefic Planet)<br>
                <span style="font-size: 12px; color: #666;">↳ गुरु सबसे शुभ ग्रह है और विवाह जैसे मांगलिक कार्यों को आशीर्वाद देता है।<br>
                <em>Jupiter is the most benefic planet and blesses auspicious events like marriage.</em></span>
            </li>
            <li>
                <strong>गोचर में गुरु का सप्तम भाव पर प्रभाव / Jupiter's Transit over 7th House</strong><br>
                <span style="font-size: 12px; color: #666;">↳ जब गुरु गोचर (वर्तमान आकाश में चलता हुआ) आपके सप्तम भाव से गुजरता है, तो विवाह के अवसर आते हैं।<br>
                <em>When transiting Jupiter passes through your 7th house, marriage opportunities arise.</em></span>
            </li>
        </ul>
    </div>
    '''

    # Build chart-specific marriage predictions
    marriage_reasons = []
    if venus_house in [1, 2, 4, 5, 7, 9, 11]:
        marriage_reasons.append(f"शुक्र भाव {venus_house} में शुभ स्थान पर है / Venus in favorable house {venus_house}")
    if jupiter_house in [1, 5, 7, 9, 11]:
        marriage_reasons.append(f"गुरु भाव {jupiter_house} में विवाह को आशीर्वाद दे रहे हैं / Jupiter blessing marriage from house {jupiter_house}")

    delay_reasons = []
    if venus_house in [6, 8, 12]:
        delay_reasons.append(f"शुक्र भाव {venus_house} (दुःस्थान) में है / Venus in house {venus_house} (difficult house)")
    if jupiter_house in [6, 8, 12]:
        delay_reasons.append(f"गुरु भाव {jupiter_house} में है / Jupiter in house {jupiter_house}")
    if "SATURN" in seventh_planets:
        delay_reasons.append("शनि 7th भाव में - देरी का कारक / Saturn in 7th - causes delay")

    affliction_reasons = []
    if "SATURN" in seventh_planets:
        affliction_reasons.append("शनि 7th में - समय के साथ संबंध मजबूत होते हैं / Saturn in 7th - relationship strengthens over time")
    if "RAHU" in seventh_planets:
        affliction_reasons.append("राहु 7th में - unconventional match संभव / Rahu in 7th - unconventional match possible")
    if "KETU" in seventh_planets:
        affliction_reasons.append("केतु 7th में - आध्यात्मिक जीवनसाथी मिल सकते हैं / Ketu in 7th - spiritual spouse possible")

    html += '''
    <div class="detail-box">
        <h3>&#128145; वैवाहिक जीवन भविष्यवाणी / Married Life Predictions</h3>'''
    html += f'''
        <div class="info-note" style="background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%); padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #ec4899;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 ये भविष्यवाणियां आपकी कुंडली के आधार पर हैं / These predictions are based on YOUR chart:</strong><br>
                शुक्र (भाव {venus_house}), गुरु (भाव {jupiter_house}), और 7th भाव में ग्रहों की स्थिति के आधार पर।<br>
                <em>Based on Venus (house {venus_house}), Jupiter (house {jupiter_house}), and planets in 7th house.</em>
            </p>
        </div>
        <ul class="prediction-list">
    '''

    if marriage_good:
        reason_text = " | ".join(marriage_reasons) if marriage_reasons else "शुभ ग्रह स्थिति"
        html += f'''<li><span class="status-good">✅</span> विवाह योग शुभ है / Marriage prospects are favorable<br>
            <span style="font-size: 11px; color: #666;">↳ कारण: {reason_text}</span></li>'''
    else:
        reason_text = " | ".join(delay_reasons) if delay_reasons else "शुक्र/गुरु कमजोर स्थिति में"
        html += f'''<li><span class="status-warning">⚠️</span> विवाह में थोड़ी देरी संभव / Slight delay in marriage possible<br>
            <span style="font-size: 11px; color: #666;">↳ कारण: {reason_text}</span></li>'''

    if not seventh_afflicted:
        # Build SPECIFIC positive reasons based on chart
        positive_reasons = []
        positive_reasons.append("7th भाव पर कोई पाप ग्रह (शनि/राहु/केतु) नहीं")

        # Check for benefics in 7th house
        benefics_in_7th = [p for p in seventh_planets if p in ["JUPITER", "VENUS", "MOON", "MERCURY"]]
        if benefics_in_7th:
            benefic_names = ", ".join([PLANET_NAMES[Planet[p]]["hindi"] for p in benefics_in_7th])
            positive_reasons.append(f"7th भाव में शुभ ग्रह: {benefic_names}")

        # Check Venus placement
        if venus_house in [1, 2, 4, 5, 7, 9, 11]:
            positive_reasons.append(f"शुक्र अच्छे भाव ({venus_house}) में")

        # Check Jupiter's aspect on 7th
        if jupiter_house in [1, 3, 5, 7, 9, 11]:
            positive_reasons.append(f"गुरु की दृष्टि/स्थिति शुभ (भाव {jupiter_house})")

        # Check 7th lord placement
        if seventh_lord_house in [1, 4, 5, 7, 9, 10, 11]:
            positive_reasons.append(f"सप्तमेश {seventh_lord_hindi} अच्छे भाव ({seventh_lord_house}) में")

        positive_text = " | ".join(positive_reasons)
        html += f'''<li><span class="status-good">✅</span> पारिवारिक जीवन सुखमय रहेगा / Family life will be happy<br>
            <span style="font-size: 11px; color: #059669;">↳ कारण: {positive_text}</span></li>'''

        # Add specific compatibility reason based on 7th rashi qualities
        compatibility_reason = f"7th राशि {seventh_rashi} की विशेषताएं अनुकूल"
        if venus_house in [1, 2, 4, 5, 7, 9, 11]:
            compatibility_reason += f" | शुक्र अच्छे भाव ({venus_house}) में"
        html += f'''<li><span class="status-good">✅</span> जीवनसाथी से अच्छा तालमेल / Good compatibility with spouse<br>
            <span style="font-size: 11px; color: #059669;">↳ {compatibility_reason}</span></li>'''
    else:
        affliction_text = " | ".join(affliction_reasons) if affliction_reasons else "7th भाव पर ग्रह प्रभाव"
        html += f'''<li><span class="status-warning">⚠️</span> कभी-कभी मतभेद संभव - संवाद बनाए रखें / Occasional disagreements possible<br>
            <span style="font-size: 11px; color: #666;">↳ {affliction_text}</span></li>'''

        # Add specific patience reason based on which malefic
        patience_reasons = []
        if "SATURN" in seventh_planets:
            patience_reasons.append("शनि 7th में - देरी और जिम्मेदारियां")
        if "RAHU" in seventh_planets:
            patience_reasons.append("राहु 7th में - अप्रत्याशित घटनाएं")
        if "KETU" in seventh_planets:
            patience_reasons.append("केतु 7th में - आध्यात्मिक विचारधारा अलग")
        patience_text = " | ".join(patience_reasons) if patience_reasons else "7th भाव पर पाप ग्रह प्रभाव"
        html += f'''<li><span class="status-warning">⚠️</span> धैर्य और समझदारी आवश्यक / Patience and understanding needed<br>
            <span style="font-size: 11px; color: #666;">↳ {patience_text}</span></li>'''

    html += '''
        </ul>
    </div>
    '''

    return html


def get_full_children_analysis(kundali, planets_in_houses, house_rashis, rashi_hindi):
    """Generate comprehensive children analysis."""
    fifth_rashi = house_rashis[5]['name']
    fifth_planets = planets_in_houses.get(5, [])

    # Get actual 5th house lord based on 5th rashi
    fifth_lord = RASHI_LORDS.get(fifth_rashi, ("", ""))
    fifth_lord_hindi = fifth_lord[0]
    fifth_lord_en = fifth_lord[1]

    jupiter_house = 0
    saturn_house = 0
    for h, planets in planets_in_houses.items():
        if "JUPITER" in planets: jupiter_house = h
        if "SATURN" in planets: saturn_house = h

    # Get dynamic children qualities based on 5th rashi
    children_qualities = CHILDREN_QUALITIES.get(fifth_rashi, ["संतान गुणवान होगी"])

    # Check if Saturn is in 5th house (causes delay)
    saturn_in_fifth = "SATURN" in fifth_planets

    html = f'''
    <div class="detail-box">
        <h3>👶 पंचम भाव (संतान स्थान) विश्लेषण / 5th House (Children House) Analysis</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #f59e0b;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 पंचम भाव क्या है? / What is the 5th House?</strong><br>
                कुंडली का <strong>पंचम भाव (5वां घर)</strong> संतान, बुद्धि, शिक्षा और रचनात्मकता का प्रतिनिधित्व करता है।
                इस भाव की राशि और उसका स्वामी ग्रह बताता है कि संतान कैसी होगी और कब होगी।<br>
                <em>The <strong>5th house</strong> represents children, intelligence, education and creativity.
                The sign in this house and its ruling planet reveal the nature of children and timing.</em>
            </p>
        </div>
        <table class="detail-table">
            <tr>
                <td><strong>पंचम भाव राशि / 5th House Sign</strong></td>
                <td>{rashi_hindi.get(fifth_rashi, fifth_rashi)} ({fifth_rashi})</td>
            </tr>
            <tr>
                <td><strong>पंचमेश / 5th House Lord</strong></td>
                <td>{fifth_lord_hindi} ({fifth_lord_en})<br>
                <span style="font-size: 11px; color: #666;">↳ यह ग्रह संतान भाग्य का स्वामी है / This planet rules your children's destiny</span></td>
            </tr>
            <tr>
                <td><strong>पुत्र कारक गुरु / Jupiter (Child Significator)</strong></td>
                <td>भाव {jupiter_house} / House {jupiter_house}<br>
                <span style="font-size: 11px; color: #666;">↳ गुरु संतान का नैसर्गिक कारक है / Jupiter is the natural significator of children</span></td>
            </tr>
        </table>
    </div>

    <div class="detail-box">
        <h3>🌟 पंचम भाव का विस्तृत फल</h3>
        <p><strong>{rashi_hindi.get(fifth_rashi, fifth_rashi)} राशि:</strong></p>
        <p>{CHILDREN_PREDICTIONS.get(fifth_rashi, '')}</p>
    </div>
    '''

    if fifth_planets:
        html += '''<div class="detail-box"><h3>पंचम भाव में ग्रह</h3>'''
        for p in fifth_planets:
            hindi = PLANET_NAMES[Planet[p]]["hindi"]
            html += f'''
            <div class="planet-effect">
                <strong>{hindi}:</strong>
                <p>{GRAHA_BHAVA_PHAL[p][5]}</p>
            </div>
            '''
        html += "</div>"

    # Jupiter quality for children - HOUSE-SPECIFIC explanations
    jupiter_quality = 'उत्तम / Excellent' if jupiter_house in [1, 2, 5, 9, 11] else 'सामान्य / Average'

    # House-specific Jupiter explanations for children
    JUPITER_CHILD_EFFECTS = {
        1: "गुरु लग्न में - संतान से आत्मसम्मान और प्रसिद्धि। बच्चे आपकी पहचान बनेंगे। / Jupiter in 1st - children bring pride and recognition",
        2: "गुरु 2nd में - बच्चों से धन लाभ, पारिवारिक संपन्नता। / Jupiter in 2nd - children bring wealth and family prosperity",
        5: "गुरु पंचम में - उत्तम! पुत्र कारक अपने भाव में। बच्चे बुद्धिमान और संस्कारी। / Jupiter in 5th - Excellent! Children will be intelligent and cultured",
        9: "गुरु 9th में - भाग्यशाली संतान, बच्चों से आध्यात्मिक उन्नति। / Jupiter in 9th - fortunate children, spiritual growth through them",
        11: "गुरु 11th में - बच्चों से लाभ और इच्छापूर्ति। / Jupiter in 11th - gains and wish fulfillment through children",
        6: "गुरु 6th में - संतान में रोग/विवाद संभव, स्वास्थ्य ध्यान दें। / Jupiter in 6th - possible health issues, be careful",
        8: "गुरु 8th में - संतान में अप्रत्याशित घटनाएं, गहरा बंधन। / Jupiter in 8th - unexpected events, deep bond with children",
        12: "गुरु 12th में - संतान से दूरी संभव (विदेश/आध्यात्मिक)। / Jupiter in 12th - possible separation (foreign/spiritual)",
    }
    default_explanation = f"गुरु भाव {jupiter_house} में - सामान्य स्थिति, प्रयास से फल मिलेगा। / Jupiter in house {jupiter_house} - average position, results with effort"
    jupiter_explanation = JUPITER_CHILD_EFFECTS.get(jupiter_house, default_explanation)

    html += f'''
    <div class="detail-box">
        <h3>♃ गुरु (पुत्र कारक) विश्लेषण / Jupiter (Child Significator) Analysis</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #f59e0b;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 गुरु क्यों महत्वपूर्ण है? / Why Jupiter is Important?</strong><br>
                वैदिक ज्योतिष में गुरु (बृहस्पति) को <strong>पुत्र कारक</strong> (संतान का कारक ग्रह) माना जाता है। यह ज्ञान, आशीर्वाद और संतान सुख का प्रतिनिधित्व करता है।<br>
                <em>In Vedic astrology, Jupiter is considered the <strong>significator of children</strong>. It represents wisdom, blessings and happiness from children.</em>
            </p>
        </div>
        <table class="detail-table">
            <tr>
                <td><strong>गुरु की स्थिति / Jupiter Position</strong></td>
                <td>भाव {jupiter_house} / House {jupiter_house}</td>
            </tr>
            <tr>
                <td><strong>गुरु का प्रभाव / Jupiter Effect</strong></td>
                <td>{GRAHA_BHAVA_PHAL['JUPITER'][jupiter_house]}</td>
            </tr>
            <tr>
                <td><strong>संतान सुख / Happiness from Children</strong></td>
                <td>{jupiter_quality}</td>
            </tr>
        </table>
        <p style="margin-top: 10px; padding: 8px; background: #f0fdf4; border-radius: 6px; font-size: 13px;">
            <strong>📝 विश्लेषण / Analysis:</strong> {jupiter_explanation}
        </p>
    </div>

    <div class="detail-box">
        <h3>👨‍👩‍👧‍👦 संतान के गुण ({rashi_hindi.get(fifth_rashi, fifth_rashi)} राशि अनुसार)</h3>
        <ul class="prediction-list">
    '''

    for quality in children_qualities:
        html += f"<li>{quality}</li>"

    html += '''
        </ul>
    </div>

    <div class="detail-box highlight-blue">
        <h3>📅 संतान समय विश्लेषण / Children Timing Analysis</h3>
        <p><em>विस्तृत समय के लिए नीचे दशा विश्लेषण खंड देखें। / See Dasha Analysis section below for detailed timing.</em></p>
        <p><strong>संतान के लिए शुभ दशाएं / Favorable Dashas for Children:</strong></p>
        <ul class="prediction-list">
    '''

    html += f'''<li>
        <strong>{fifth_lord_hindi} (पंचमेश) / {fifth_lord_en} (5th Lord)</strong> की महादशा/अंतर्दशा<br>
        <span style="font-size: 12px; color: #666;">↳ पंचमेश संतान भाव का स्वामी है, इसकी दशा में संतान की संभावना बढ़ती है।<br>
        <em>The 5th lord rules the children house, its period increases chances of children.</em></span>
    </li>'''
    html += '''<li>
        <strong>गुरु / Jupiter</strong> की दशा (पुत्र कारक / Child Significator)<br>
        <span style="font-size: 12px; color: #666;">↳ गुरु संतान का नैसर्गिक कारक है, इसकी दशा संतान के लिए अनुकूल होती है।<br>
        <em>Jupiter is the natural significator of children, its period is favorable for children.</em></span>
    </li>'''
    html += '''<li>
        <strong>शुक्र / Venus</strong> की दशा (सुख कारक / Comfort Significator)<br>
        <span style="font-size: 12px; color: #666;">↳ शुक्र सुख और प्रजनन का कारक है, इसकी दशा भी शुभ मानी जाती है।<br>
        <em>Venus signifies comfort and fertility, its period is also considered auspicious.</em></span>
    </li>'''
    html += "</ul>"

    if saturn_in_fifth:
        html += f'''<p style="padding: 10px; background: #fef3c7; border-radius: 6px; margin-top: 10px;">
            <strong>⚠️ नोट / Note:</strong> शनि पंचम भाव में होने से पहली संतान में थोड़ी देरी संभव है। यह दोष नहीं है, बस समय लग सकता है।<br>
            <em>Saturn in 5th house may cause slight delay in first child. This is not a defect, just a timing indication.</em>
        </p>'''

    html += '''
    </div>
    '''

    return html


def get_full_health_analysis(kundali, planets_in_houses, house_rashis, rashi_hindi):
    """Generate comprehensive health analysis."""
    lagna = kundali.lagna['rashi']
    sixth_planets = planets_in_houses.get(6, [])
    eighth_planets = planets_in_houses.get(8, [])

    moon_house = 0
    for h, planets in planets_in_houses.items():
        if "MOON" in planets: moon_house = h

    # Get dynamic body constitution based on actual lagna
    body_const = LAGNA_BODY_CONSTITUTION.get(lagna, ("वात-पित्त", "सामान्य अंग"))
    prakriti = body_const[0]
    sensitive_organs = body_const[1]

    html = f'''
    <div class="detail-box">
        <h3>🏥 लग्न आधारित स्वास्थ्य विश्लेषण / Lagna-based Health Analysis</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #10b981;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 आयुर्वेदिक प्रकृति क्या है? / What is Ayurvedic Constitution?</strong><br>
                आयुर्वेद के अनुसार शरीर तीन दोषों (वात, पित्त, कफ) से बना है। आपकी लग्न राशि आपकी प्राकृतिक शरीर प्रकृति और
                संवेदनशील अंगों को दर्शाती है। इससे आप अपने स्वास्थ्य की बेहतर देखभाल कर सकते हैं।<br>
                <em>According to Ayurveda, the body is composed of three doshas (Vata, Pitta, Kapha). Your Lagna sign reveals your
                natural body constitution and sensitive organs. This helps you take better care of your health.</em>
            </p>
        </div>
        <table class="detail-table">
            <tr>
                <td><strong>लग्न राशि / Ascendant Sign</strong></td>
                <td>{rashi_hindi.get(lagna, lagna)} ({lagna})</td>
            </tr>
            <tr>
                <td><strong>शरीर प्रकृति / Body Constitution</strong></td>
                <td>{prakriti}<br>
                <span style="font-size: 11px; color: #666;">↳ आपके शरीर की प्राकृतिक संरचना / Your body's natural tendency</span></td>
            </tr>
            <tr>
                <td><strong>संवेदनशील अंग / Sensitive Organs</strong></td>
                <td>{sensitive_organs}<br>
                <span style="font-size: 11px; color: #666;">↳ इन अंगों का विशेष ध्यान रखें / Pay special attention to these organs</span></td>
            </tr>
        </table>
    </div>

    <div class="detail-box">
        <h3>🩺 {rashi_hindi.get(lagna, lagna)} लग्न स्वास्थ्य विशेषताएं / {lagna} Ascendant Health Characteristics</h3>
        <p>{HEALTH_PREDICTIONS.get(lagna, '')}</p>
    </div>

    <div class="detail-box">
        <h3>⚠️ स्वास्थ्य संवेदनशील क्षेत्र / Health Sensitive Areas</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%); padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #ef4444;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 संवेदनशील क्षेत्र का अर्थ / What are Sensitive Areas?</strong><br>
                हर लग्न राशि के कुछ विशेष अंग <strong>अधिक संवेदनशील</strong> होते हैं। इसका मतलब यह नहीं कि आपको रोग होगा,
                बल्कि इन अंगों का <strong>विशेष ध्यान</strong> रखें।<br>
                <em>Every ascendant sign has certain organs that are <strong>more sensitive</strong>. This doesn't mean you will get sick,
                but <strong>take special care</strong> of these organs.</em>
            </p>
        </div>
        <p><strong>मुख्य संवेदनशील अंग / Main Sensitive Organs:</strong> {sensitive_organs}</p>
        <p><strong>आयुर्वेदिक प्रकृति / Ayurvedic Constitution:</strong> {prakriti} - इस प्रकृति के अनुसार आहार-विहार का ध्यान रखें / Follow diet and lifestyle according to this constitution.</p>
    </div>
    '''

    if sixth_planets:
        html += '''<div class="detail-box highlight-yellow">
        <h3>षष्ठ भाव (रोग स्थान) में ग्रह / Planets in 6th House (Disease House)</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #f59e0b;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 छठा भाव क्या दर्शाता है? / What does 6th House indicate?</strong><br>
                छठा भाव <strong>रोग, शत्रु और ऋण</strong> का भाव है। यहां स्थित ग्रह बताते हैं कि आपको किस प्रकार की
                स्वास्थ्य समस्याएं हो सकती हैं और उनसे कैसे बचें।<br>
                <em>6th house represents <strong>diseases, enemies and debts</strong>. Planets here indicate what kind of
                health issues you may face and how to prevent them.</em>
            </p>
        </div>'''
        for p in sixth_planets:
            hindi = PLANET_NAMES[Planet[p]]["hindi"]
            html += f'''
            <div class="planet-effect">
                <strong>{hindi}:</strong>
                <p>{GRAHA_BHAVA_PHAL[p][6]}</p>
            </div>
            '''
        html += "</div>"

    html += f'''
    <div class="detail-box">
        <h3>☽ चंद्र (मन) की स्थिति / Moon (Mind) Position - भाव {moon_house} / House {moon_house}</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #3b82f6;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 चंद्रमा मानसिक स्वास्थ्य से क्यों जुड़ा है? / Why is Moon linked to mental health?</strong><br>
                ज्योतिष में चंद्रमा <strong>मन, भावनाओं और मानसिक स्थिति</strong> का कारक है। चंद्रमा जिस भाव में हो,
                वह आपकी मानसिक प्रवृत्ति और भावनात्मक स्वास्थ्य को दर्शाता है।<br>
                <em>In astrology, Moon represents <strong>mind, emotions and mental state</strong>. The house where Moon is placed
                indicates your mental tendencies and emotional health.</em>
            </p>
        </div>
        <p><strong>मानसिक स्वास्थ्य / Mental Health:</strong> {GRAHA_BHAVA_PHAL['MOON'][moon_house]}</p>
        <p><strong>सुझाव / Suggestion:</strong> {
            'चंद्र 6th भाव में - तनाव/चिंता की प्रवृत्ति। नियमित ध्यान और प्राणायाम करें। / Moon in 6th house - tendency for stress/anxiety. Practice regular meditation and pranayama.'
            if moon_house == 6 else
            'चंद्र 8th भाव में - भावनात्मक उतार-चढ़ाव। गहरी नींद लें, तनाव से बचें। / Moon in 8th house - emotional ups-downs. Get deep sleep, avoid stress.'
            if moon_house == 8 else
            'चंद्र 12th भाव में - अकेलापन/नींद की समस्या संभव। सोने से पहले मोबाइल बंद करें, शांत वातावरण रखें। / Moon in 12th house - possible isolation/sleep issues. Avoid screens before sleep, keep calm environment.'
            if moon_house == 12 else
            'मानसिक स्थिति संतुलित / Mental state is balanced - Moon in good house'
        }</p>
    </div>

    {get_prakriti_based_remedies_html(prakriti, moon_house, eighth_planets)}
    '''

    return html


def get_full_wealth_analysis(kundali, planets_in_houses, house_rashis, rashi_hindi):
    """Generate comprehensive wealth analysis."""
    lagna = kundali.lagna.get('rashi', 'Mesha')  # For lagna-specific Saturn analysis
    second_planets = planets_in_houses.get(2, [])
    eleventh_planets = planets_in_houses.get(11, [])
    ninth_planets = planets_in_houses.get(9, [])

    html = f'''
    <div class="detail-box">
        <h3>💰 धन भाव विश्लेषण / Wealth Houses Analysis</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); padding: 15px; border-radius: 10px; margin-bottom: 15px; border-left: 4px solid #f59e0b;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 धन के लिए कौन से भाव महत्वपूर्ण हैं? / Which houses are important for Wealth?</strong><br><br>
                कुंडली में तीन भाव धन से सीधे जुड़े हैं:<br>
                • <strong>द्वितीय भाव (2nd House)</strong> = बैंक बैलेंस, बचत, पारिवारिक धन / Bank balance, savings, family wealth<br>
                • <strong>नवम भाव (9th House)</strong> = भाग्य, किस्मत से मिलने वाला धन / Fortune, luck-based wealth<br>
                • <strong>एकादश भाव (11th House)</strong> = आय, लाभ, इच्छाओं की पूर्ति / Income, gains, fulfillment of desires<br><br>
                <em>इन भावों में जितने अधिक शुभ ग्रह होंगे, धन प्राप्ति उतनी अधिक होगी।<br>
                More benefic planets in these houses = More wealth accumulation.</em>
            </p>
        </div>
        <table class="detail-table">
            <tr><th>भाव / House</th><th>राशि / Sign</th><th>ग्रह / Planets</th><th>महत्व / Significance</th></tr>
            <tr>
                <td><strong>2nd (द्वितीय)</strong><br><span style="font-size:11px;color:#666;">धन भाव / Wealth House</span></td>
                <td>{rashi_hindi.get(house_rashis[2]['name'], house_rashis[2]['name'])}</td>
                <td>{', '.join(second_planets) if second_planets else '- (खाली/Empty)'}</td>
                <td>मुख्य धन स्थान - आपकी बचत और बैंक बैलेंस<br><span style="font-size:11px;color:#666;">Main wealth house - your savings & bank balance</span></td>
            </tr>
            <tr>
                <td><strong>9th (नवम)</strong><br><span style="font-size:11px;color:#666;">भाग्य भाव / Fortune House</span></td>
                <td>{rashi_hindi.get(house_rashis[9]['name'], house_rashis[9]['name'])}</td>
                <td>{', '.join(ninth_planets) if ninth_planets else '- (खाली/Empty)'}</td>
                <td>भाग्य से धन - लॉटरी, विरासत, अप्रत्याशित लाभ<br><span style="font-size:11px;color:#666;">Fortune-based wealth - lottery, inheritance, unexpected gains</span></td>
            </tr>
            <tr>
                <td><strong>11th (एकादश)</strong><br><span style="font-size:11px;color:#666;">लाभ भाव / Gains House</span></td>
                <td>{rashi_hindi.get(house_rashis[11]['name'], house_rashis[11]['name'])}</td>
                <td>{', '.join(eleventh_planets) if eleventh_planets else '- (खाली/Empty)'}</td>
                <td>आय स्थान - नियमित आय और लाभ<br><span style="font-size:11px;color:#666;">Income house - regular income & profits</span></td>
            </tr>
        </table>
    </div>
    '''

    if second_planets:
        html += f'''
        <div class="detail-box highlight-gold">
            <h3>🌟 विशेष धन योग / Special Wealth Yoga - {len(second_planets)} ग्रह द्वितीय भाव में!</h3>
            <div class="info-note" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #f59e0b;">
                <p style="margin: 0; font-size: 13px;">
                    <strong>🎉 बधाई! यह अत्यंत दुर्लभ और शक्तिशाली योग है! / Congratulations! This is rare & powerful!</strong><br>
                    द्वितीय भाव (धन का घर) में ग्रह होना धन कमाने की विशेष क्षमता देता है। हर ग्रह एक अलग स्रोत से धन लाता है।
                    आपके पास <strong>{len(second_planets)} ग्रह</strong> हैं, यानी <strong>{len(second_planets)} अलग-अलग आय के स्रोत</strong> संभव हैं!<br>
                    <em>Planets in 2nd house (wealth house) give special ability to earn money. Each planet brings wealth from different source.
                    You have <strong>{len(second_planets)} planets</strong> = <strong>{len(second_planets)} different income sources</strong> possible!</em>
                </p>
            </div>
            <table class="detail-table">
                <tr><th>ग्रह / Planet</th><th>धन स्रोत / Income Source</th><th>विस्तृत प्रभाव / Detailed Effect</th></tr>
        '''
        wealth_details = {
            "SUN": ("सरकारी/Authority", "उच्च पदों से धन, पिता से संपत्ति, सरकारी अनुदान / Wealth from high positions, father's property, govt grants"),
            "MOON": ("जनता/Public", "जन संपर्क से आय, तरल व्यापार, माता से धन / Income from public dealing, liquid business, wealth from mother"),
            "MARS": ("तकनीकी/Property", "रियल एस्टेट, भूमि-भवन, तकनीकी कार्य, भाई से सहयोग / Real estate, land-building, technical work, sibling support"),
            "MERCURY": ("व्यापार/IT", "व्यापार लाभ, IT/Software, लेखन, संचार क्षेत्र / Business profit, IT/Software, writing, communication"),
            "JUPITER": ("शिक्षा/Finance", "बैंकिंग, शिक्षा, परामर्श, धार्मिक कार्य / Banking, education, consulting, religious work"),
            "VENUS": ("कला/Luxury", "कला, फैशन, सौंदर्य, मनोरंजन उद्योग / Arts, fashion, beauty, entertainment industry"),
            "SATURN": ("सेवा/Labor", "मेहनत से धन, सेवा क्षेत्र, खनन / Wealth through hard work, service sector, mining"),
            "RAHU": ("विदेश/Tech", "विदेशी स्रोत, अपारंपरिक तरीके, तकनीक / Foreign sources, unconventional methods, technology"),
            "KETU": ("आध्यात्मिक/Spiritual", "आध्यात्मिक कार्य, गुप्त विद्या / Spiritual work, occult sciences"),
        }
        for p in second_planets:
            hindi = PLANET_NAMES[Planet[p]]["hindi"]
            details = wealth_details.get(p, ("", ""))
            html += f"<tr><td><strong>{hindi}</strong></td><td>{details[0]}</td><td>{details[1]}</td></tr>"
        html += "</table></div>"

    html += f'''
    <div class="detail-box">
        <h3>📊 धन प्राप्ति के समय / Wealth Timing</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #10b981;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 धन कब आएगा? / When will wealth come?</strong><br>
                जीवन में धन प्राप्ति का समय <strong>दशा (ग्रहों के शासनकाल)</strong> पर निर्भर करता है। कुछ ग्रहों की दशा में धन आसानी से आता है,
                जबकि कुछ में मेहनत करनी पड़ती है।<br>
                <em>Wealth timing depends on <strong>Dasha (planetary periods)</strong>. Some planets' periods bring easy wealth,
                while others require hard work.</em>
            </p>
        </div>
        <p><em>विस्तृत समय के लिए नीचे दशा विश्लेषण खंड देखें। / See Dasha Analysis section below for detailed timing.</em></p>
        <p><strong>धन के लिए शुभ दशाएं / Favorable Dashas for Wealth:</strong></p>
        <ul class="prediction-list">
            <li>
                <strong>द्वितीयेश और एकादशेश / 2nd & 11th House Lords</strong> की महादशा/अंतर्दशा<br>
                <span style="font-size: 12px; color: #666;">↳ द्वितीयेश = धन भाव का मालिक, एकादशेश = लाभ भाव का मालिक - इनकी दशा में धन वृद्धि निश्चित<br>
                <em>2nd lord = wealth house owner, 11th lord = gains house owner - wealth increase certain in their periods</em></span>
            </li>
            <li>
                <strong>गुरु / Jupiter</strong> की दशा (धन कारक / Wealth Significator)<br>
                <span style="font-size: 12px; color: #666;">↳ गुरु विस्तार और वृद्धि का कारक है - इसकी दशा में धन में वृद्धि होती है<br>
                <em>Jupiter signifies expansion & growth - its period brings wealth increase</em></span>
            </li>
            <li>
                <strong>शुक्र / Venus</strong> की दशा (सुख-वैभव / Luxury & Comfort)<br>
                <span style="font-size: 12px; color: #666;">↳ शुक्र विलासिता और सुख-सुविधाओं का कारक है - इसकी दशा में जीवन स्तर ऊंचा होता है<br>
                <em>Venus signifies luxury & comfort - its period elevates lifestyle</em></span>
            </li>
            <li>
                <strong>बुध / Mercury</strong> की दशा (व्यापार से लाभ / Business Profit)<br>
                <span style="font-size: 12px; color: #666;">↳ बुध व्यापार और गणना का कारक है - इसकी दशा में business और investment से लाभ होता है<br>
                <em>Mercury rules business & calculation - its period brings profit from business & investments</em></span>
            </li>
        </ul>
    </div>

    <div class="detail-box">
        <h3>🏠 संपत्ति योग / Property Yoga</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #f59e0b;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 संपत्ति (Property) के लिए कौन से भाव देखें? / Which houses for Property?</strong><br>
                <strong>चतुर्थ भाव (4th House)</strong> = घर, जमीन, वाहन / Home, land, vehicles<br>
                <strong>शनि</strong> = भूमि और स्थायी संपत्ति का कारक / Saturn = significator of land & permanent assets<br>
                <em>When 4th lord or Saturn's period is running, it's good time for property purchase.</em>
            </p>
        </div>
        {get_property_timing_html(house_rashis, planets_in_houses, lagna)}
    </div>

    {get_investment_suggestions_html(planets_in_houses, house_rashis, lagna)}
    '''

    return html


def get_full_dasha_analysis(kundali, mahadashas, current_dasha):
    """Generate comprehensive dasha analysis with LAGNA-SPECIFIC effects."""

    # Get lagna for personalized effects
    lagna = kundali.lagna.get('rashi', 'Mesha')

    # Dasha period explanations
    DASHA_PERIODS = {
        "Sun": ("6 वर्ष / 6 Years", "सरकार, पिता, आत्मविश्वास, नेतृत्व", "Government, Father, Confidence, Leadership"),
        "Moon": ("10 वर्ष / 10 Years", "मन, माता, भावनाएं, जनता", "Mind, Mother, Emotions, Public"),
        "Mars": ("7 वर्ष / 7 Years", "साहस, भाई, संपत्ति, ऊर्जा", "Courage, Siblings, Property, Energy"),
        "Mercury": ("17 वर्ष / 17 Years", "बुद्धि, व्यापार, संचार, शिक्षा", "Intelligence, Business, Communication, Education"),
        "Jupiter": ("16 वर्ष / 16 Years", "ज्ञान, गुरु, धर्म, संतान", "Wisdom, Teacher, Religion, Children"),
        "Venus": ("20 वर्ष / 20 Years", "विवाह, प्रेम, कला, विलासिता", "Marriage, Love, Arts, Luxury"),
        "Saturn": ("19 वर्ष / 19 Years", "कर्म, मेहनत, अनुशासन, देरी", "Karma, Hard work, Discipline, Delays"),
        "Rahu": ("18 वर्ष / 18 Years", "विदेश, अप्रत्याशित, भ्रम, तकनीक", "Foreign, Unexpected, Illusion, Technology"),
        "Ketu": ("7 वर्ष / 7 Years", "मोक्ष, आध्यात्मिक, वैराग्य", "Liberation, Spiritual, Detachment"),
    }

    html = f'''
    <div class="detail-box">
        <h3>🔮 दशा प्रणाली का परिचय / Introduction to Dasha System</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); padding: 15px; border-radius: 10px; margin-bottom: 15px; border-left: 4px solid #3b82f6;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 दशा क्या है? / What is Dasha?</strong><br><br>
                <strong>दशा</strong> = ग्रहों का शासनकाल। वैदिक ज्योतिष में <strong>विंशोत्तरी दशा</strong> पद्धति सबसे प्रचलित है जिसमें
                जीवन के 120 वर्षों को 9 ग्रहों में बांटा गया है। <strong>आपके जीवन में जो भी बड़ी घटनाएं होती हैं - नौकरी, विवाह, संतान,
                धन लाभ/हानि - वे सब किसी न किसी ग्रह की दशा में होती हैं।</strong><br><br>
                <em><strong>Dasha</strong> = Planetary Period. In Vedic astrology, <strong>Vimshottari Dasha</strong> system divides
                120 years of life among 9 planets. <strong>All major life events - job, marriage, children, wealth gains/losses -
                happen during specific planetary periods.</strong></em>
            </p>
        </div>
        <div class="info-note" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); padding: 15px; border-radius: 10px; margin-bottom: 15px; border-left: 4px solid #f59e0b;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 दशा के तीन स्तर / Three Levels of Dasha:</strong><br><br>
                <strong>1. महादशा (Mahadasha)</strong> = मुख्य ग्रह का काल (6-20 वर्ष) - जीवन की मुख्य दिशा तय करता है<br>
                <strong>2. अंतर्दशा (Antardasha)</strong> = महादशा के अंदर छोटी दशा (कुछ महीने - कुछ वर्ष) - विशिष्ट घटनाएं<br>
                <strong>3. प्रत्यंतर्दशा (Pratyantardasha)</strong> = अंतर्दशा के अंदर और छोटी दशा - दैनिक प्रभाव<br><br>
                <em>1. Mahadasha = Main period (6-20 years) - determines life's main direction<br>
                2. Antardasha = Sub-period within Mahadasha - specific events<br>
                3. Pratyantardasha = Sub-sub period - daily influences</em>
            </p>
        </div>
    </div>

    <div class="detail-box highlight-blue">
        <h3>⏰ वर्तमान दशा विस्तृत विश्लेषण / Current Dasha Detailed Analysis</h3>
        <table class="detail-table">
            <tr><th>स्तर / Level</th><th>ग्रह / Planet</th><th>आरंभ / Start</th><th>समाप्ति / End</th><th>क्या प्रभावित करता है / What it affects</th></tr>
            <tr class="highlight-row">
                <td><strong>महादशा</strong><br><span style="font-size:11px;color:#666;">Main Period</span></td>
                <td><strong>{current_dasha['mahadasha']['planet']}</strong></td>
                <td>{current_dasha['mahadasha']['start'].strftime('%d-%m-%Y')}</td>
                <td>{current_dasha['mahadasha']['end'].strftime('%d-%m-%Y')}</td>
                <td>{DASHA_PERIODS.get(current_dasha['mahadasha']['planet'], ('', '', ''))[1]}</td>
            </tr>
            <tr>
                <td><strong>अंतर्दशा</strong><br><span style="font-size:11px;color:#666;">Sub Period</span></td>
                <td>{current_dasha['antardasha']['planet']}</td>
                <td>{current_dasha['antardasha']['start'].strftime('%d-%m-%Y')}</td>
                <td>{current_dasha['antardasha']['end'].strftime('%d-%m-%Y')}</td>
                <td>{DASHA_PERIODS.get(current_dasha['antardasha']['planet'], ('', '', ''))[1]}</td>
            </tr>
            <tr>
                <td><strong>प्रत्यंतर्दशा</strong><br><span style="font-size:11px;color:#666;">Sub-sub Period</span></td>
                <td>{current_dasha['pratyantardasha']['planet']}</td>
                <td>{current_dasha['pratyantardasha']['start'].strftime('%d-%m-%Y')}</td>
                <td>{current_dasha['pratyantardasha']['end'].strftime('%d-%m-%Y')}</td>
                <td>{DASHA_PERIODS.get(current_dasha['pratyantardasha']['planet'], ('', '', ''))[1]}</td>
            </tr>
        </table>
    </div>

    <div class="detail-box">
        <h3>🌟 {current_dasha['mahadasha']['planet']} महादशा का प्रभाव / {current_dasha['mahadasha']['planet']} Mahadasha Effects</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #10b981;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 {current_dasha['mahadasha']['planet']} ग्रह क्या प्रभावित करता है?</strong><br>
                {DASHA_PERIODS.get(current_dasha['mahadasha']['planet'], ('', '', ''))[1]}<br>
                <em>{DASHA_PERIODS.get(current_dasha['mahadasha']['planet'], ('', '', ''))[2]}</em>
            </p>
        </div>
        <p><strong>विस्तृत प्रभाव / Detailed Effects:</strong> {get_lagna_specific_dasha_effect(current_dasha['mahadasha']['planet'], lagna)['effect_hindi']}</p>
        <p style="color: #059669;"><strong>आपके लग्न के लिए विशेष / Specific for your Lagna:</strong> {get_lagna_specific_dasha_effect(current_dasha['mahadasha']['planet'], lagna)['status_hindi']} - {get_lagna_specific_dasha_effect(current_dasha['mahadasha']['planet'], lagna)['status_en']}</p>
    </div>

    <div class="detail-box">
        <h3>📅 संपूर्ण महादशा क्रम / Complete Mahadasha Sequence</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #f59e0b;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 यह क्या दर्शाता है? / What does this show?</strong><br>
                नीचे आपके जीवन की सभी महादशाओं का क्रम दिया गया है। <strong>पीले रंग</strong> वाली पंक्ति आपकी वर्तमान महादशा है।
                हर महादशा में जीवन का ध्यान अलग-अलग क्षेत्रों पर होता है।<br>
                <em>Below is the sequence of all Mahadashas in your life. <strong>Yellow highlighted</strong> row is your current period.
                Each Mahadasha focuses life on different areas.</em>
            </p>
        </div>
        <table class="detail-table">
            <tr><th>महादशा / Mahadasha</th><th>आरंभ / Start</th><th>समाप्ति / End</th><th>अवधि / Duration</th><th>प्रमुख प्रभाव / Key Effects</th></tr>
    '''

    maha_planet = current_dasha['mahadasha']['planet']
    for m in mahadashas[:10]:
        is_current = m.planet == maha_planet
        row_class = 'class="highlight-row"' if is_current else ''
        current_marker = " ← वर्तमान / Current" if is_current else ""
        # Use LAGNA-SPECIFIC effect instead of generic DASHA_EFFECTS
        dasha_effect = get_lagna_specific_dasha_effect(m.planet, lagna)
        effect = dasha_effect['status_hindi'] + " - " + str(dasha_effect['houses_ruled'])[:30]
        period_info = DASHA_PERIODS.get(m.planet, ('', '', ''))

        html += f'''
        <tr {row_class}>
            <td><strong>{m.planet}</strong>{current_marker}<br><span style="font-size:10px;color:#666;">{period_info[0]}</span></td>
            <td>{m.start_date.strftime('%d-%m-%Y')}</td>
            <td>{m.end_date.strftime('%d-%m-%Y')}</td>
            <td>{m.duration_years:.1f} वर्ष</td>
            <td>{effect}</td>
        </tr>'''

    html += '''
        </table>
    </div>
    '''

    # Show current mahadasha details dynamically
    current_maha = current_dasha['mahadasha']['planet']
    current_maha_start = current_dasha['mahadasha']['start'].strftime('%Y')
    current_maha_end = current_dasha['mahadasha']['end'].strftime('%Y')

    # Get LAGNA-SPECIFIC effect for current mahadasha
    current_maha_effect = get_lagna_specific_dasha_effect(current_maha, lagna)

    html += f'''
    <div class="detail-box highlight-green">
        <h3>🌟 वर्तमान {current_maha} महादशा ({current_maha_start}-{current_maha_end}) - विस्तृत विश्लेषण / Current Period Analysis</h3>
        <p><strong>{current_maha} महादशा का प्रभाव / Effects:</strong> {current_maha_effect['effect_hindi']}</p>
        <p style="color: #059669; font-weight: bold;"><strong>आपके {lagna} लग्न के लिए:</strong> {current_maha_effect['status_hindi']} ({current_maha_effect['status_en']})</p>
        <p><em>{current_maha_effect['effect_en']}</em></p>
    </div>

    <div class="detail-box">
        <h3>📚 दशा समझने के सामान्य सिद्धांत / General Principles to Understand Dasha</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); padding: 15px; border-radius: 10px; margin-bottom: 15px; border-left: 4px solid #3b82f6;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 कौन सी दशा अच्छी है? / Which Dasha is Good?</strong><br><br>
                यह आपकी कुंडली पर निर्भर करता है, लेकिन कुछ सामान्य नियम हैं:<br>
                <em>It depends on your chart, but some general rules apply:</em>
            </p>
        </div>
    '''

    # Get lagna-specific benefic/malefic info
    saturn_effect = get_lagna_specific_dasha_effect("Saturn", lagna)
    mars_effect = get_lagna_specific_dasha_effect("Mars", lagna)
    jupiter_effect = get_lagna_specific_dasha_effect("Jupiter", lagna)

    # Build personalized benefic list
    your_benefics = []
    your_malefics = []
    for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        effect = get_lagna_specific_dasha_effect(planet, lagna)
        if effect['is_yogakaraka']:
            your_benefics.insert(0, f"{planet} (योगकारक!)")
        elif effect['is_benefic']:
            your_benefics.append(planet)
        else:
            your_malefics.append(planet)

    benefics_str = ", ".join(your_benefics) if your_benefics else "कोई नहीं"
    malefics_str = ", ".join(your_malefics) if your_malefics else "कोई नहीं"

    # Saturn special note for Taurus/Libra
    saturn_note = ""
    if lagna in ["Vrishabha", "Tula"]:
        saturn_note = f"<br><span style='color: #059669; font-weight: bold;'>🌟 विशेष: आपके {lagna} लग्न के लिए शनि योगकारक है - शनि दशा बहुत शुभ! / Special: Saturn is Yogakaraka for your {lagna} lagna - Saturn dasha is very auspicious!</span>"

    html += f'''
        <ul class="prediction-list">
            <li>
                <strong style="color: #059669;">आपके {lagna} लग्न के शुभ ग्रह / Your Benefics:</strong> {benefics_str}<br>
                <span style="font-size: 12px; color: #059669;">↳ इनकी दशा में आपको अच्छे फल मिलेंगे / Good results in these periods</span>
            </li>
            <li>
                <strong style="color: #dc2626;">आपके {lagna} लग्न के कठिन ग्रह / Your Challenging Planets:</strong> {malefics_str}<br>
                <span style="font-size: 12px; color: #dc2626;">↳ इनकी दशा में चुनौतियां - उपाय करें / Challenges in these periods - do remedies</span>{saturn_note}
            </li>
            <li>
                <strong>योगकारक की दशा / Yogakaraka Dasha:</strong> {'शनि (Saturn) - आपके लिए सर्वश्रेष्ठ!' if saturn_effect['is_yogakaraka'] else ('मंगल (Mars) - आपके लिए सर्वश्रेष्ठ!' if mars_effect['is_yogakaraka'] else 'आपके लग्न का योगकारक ग्रह')}<br>
                <span style="font-size: 12px; color: #666;">↳ सर्वोत्तम फल - जीवन के कई क्षेत्रों में उन्नति / Best results - progress in multiple life areas</span>
            </li>
            <li>
                <strong>लग्नेश की दशा / Lagna Lord Dasha:</strong> आपकी {lagna} लग्न राशि के स्वामी की दशा<br>
                <span style="font-size: 12px; color: #666;">↳ आत्मविकास, व्यक्तित्व निखार, नई शुरुआत / Self-development, personality growth, new beginnings</span>
            </li>
        </ul>
    </div>
    '''

    return html


def get_full_yoga_analysis(kundali, planets_in_houses):
    """Generate comprehensive yoga analysis based on actual planetary positions."""
    first_planets = planets_in_houses.get(1, [])
    second_planets = planets_in_houses.get(2, [])

    # Find planet positions for yoga checks
    saturn_house = jupiter_house = venus_house = moon_house = sun_house = mercury_house = mars_house = 0
    saturn_rashi = ""
    for h, planets in planets_in_houses.items():
        if "SATURN" in planets: saturn_house = h
        if "JUPITER" in planets: jupiter_house = h
        if "VENUS" in planets: venus_house = h
        if "MOON" in planets: moon_house = h
        if "SUN" in planets: sun_house = h
        if "MERCURY" in planets: mercury_house = h
        if "MARS" in planets: mars_house = h

    # Get Saturn's rashi from kundali
    saturn_rashi = kundali.planets.get('SATURN', {}).get('rashi', '')

    # Check for actual yogas dynamically
    budhaditya = sun_house == mercury_house and sun_house != 0  # Sun and Mercury in same house
    guru_mangal = jupiter_house == mars_house and jupiter_house != 0  # Jupiter and Mars in same house
    saturn_swarashi = saturn_rashi in ["Makara", "Kumbha"]  # Saturn in own sign
    venus_in_lagna = "VENUS" in first_planets  # Venus in 1st house
    dhana_yoga = len(second_planets) >= 2  # Multiple planets in 2nd house

    # Check Kemadruma Yoga (Moon alone without planets in 2nd/12th from it)
    moon_2nd = (moon_house % 12) + 1
    moon_12th = ((moon_house - 2) % 12) + 1
    kemadruma_bhang = len(planets_in_houses.get(moon_2nd, [])) > 0 or len(planets_in_houses.get(moon_12th, [])) > 0

    html = '''
    <div class="detail-box">
        <h3>🔮 कुंडली में विशेष योग / Special Yogas in your Chart</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); padding: 15px; border-radius: 10px; margin-bottom: 15px; border-left: 4px solid #3b82f6;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 योग क्या है? / What is Yoga?</strong><br><br>
                <strong>योग</strong> = विशेष ग्रहों का संयोग जो जीवन में विशेष फल देता है। जब कुछ ग्रह विशेष स्थितियों में होते हैं,
                तो वे मिलकर एक "योग" बनाते हैं जो सामान्य फल से अधिक शक्तिशाली होता है।<br><br>
                <strong>✅ = योग उपस्थित है (आपकी कुंडली में है)</strong><br>
                <strong>⬜ = योग अनुपस्थित है (आपकी कुंडली में नहीं है)</strong><br><br>
                <em><strong>Yoga</strong> = Special planetary combination that gives special results in life. When certain planets
                are in specific positions, they form a "Yoga" that is more powerful than regular effects.<br>
                ✅ = Yoga is present (in your chart) | ⬜ = Yoga is absent (not in your chart)</em>
            </p>
        </div>
        <p><strong>आपकी कुंडली में निम्नलिखित योगों की जांच की गई / Following Yogas checked in your chart:</strong></p>
    </div>

    <div class="yoga-grid">
    '''

    # Budhaditya Yoga
    html += f'''
    <div class="yoga-card {'active' if budhaditya else ''}">
        <h4>{'✅' if budhaditya else '⬜'} बुधादित्य योग / Budhaditya Yoga</h4>
        <p><strong>क्या है / What:</strong> सूर्य + बुध एक भाव में / Sun & Mercury in same house</p>
        <p><strong>स्थिति / Status:</strong> {'भाव ' + str(sun_house) + ' में उपस्थित ✓ / Present in House ' + str(sun_house) if budhaditya else 'अनुपस्थित / Not present'}</p>
        <p><strong>फल / Effect:</strong> बुद्धि में तीव्रता, वाणी में प्रभाव, व्यापार कौशल<br><span style="font-size:11px;color:#666;">Sharp intelligence, impactful speech, business skills</span></p>
    </div>

    <div class="yoga-card {'active' if guru_mangal else ''}">
        <h4>{'✅' if guru_mangal else '⬜'} गुरु-मंगल योग / Guru-Mangal Yoga</h4>
        <p><strong>क्या है / What:</strong> गुरु + मंगल संयोग / Jupiter & Mars together</p>
        <p><strong>स्थिति / Status:</strong> {'भाव ' + str(jupiter_house) + ' में उपस्थित ✓ / Present in House ' + str(jupiter_house) if guru_mangal else 'अनुपस्थित / Not present'}</p>
        <p><strong>फल / Effect:</strong> धन संचय, भूमि-भवन लाभ, नेतृत्व क्षमता<br><span style="font-size:11px;color:#666;">Wealth accumulation, property gains, leadership ability</span></p>
    </div>

    <div class="yoga-card {'active' if saturn_swarashi else ''}">
        <h4>{'✅' if saturn_swarashi else '⬜'} शनि स्वराशि योग / Saturn Own Sign Yoga</h4>
        <p><strong>क्या है / What:</strong> शनि अपनी राशि (मकर/कुंभ) में / Saturn in own sign (Capricorn/Aquarius)</p>
        <p><strong>स्थिति / Status:</strong> {'शनि ' + saturn_rashi + ' में - स्वराशि! ✓ / Saturn in own sign!' if saturn_swarashi else 'शनि ' + saturn_rashi + ' में / Saturn in ' + saturn_rashi}</p>
        <p><strong>फल / Effect:</strong> दीर्घकालीन सफलता, अनुशासन से उन्नति<br><span style="font-size:11px;color:#666;">Long-term success, progress through discipline</span></p>
    </div>

    <div class="yoga-card {'active' if venus_in_lagna else ''}">
        <h4>{'✅' if venus_in_lagna else '⬜'} शुक्र लग्न योग / Venus in Lagna Yoga</h4>
        <p><strong>क्या है / What:</strong> शुक्र प्रथम भाव (लग्न) में / Venus in 1st house (Ascendant)</p>
        <p><strong>स्थिति / Status:</strong> {'लग्न में उपस्थित ✓ / Present in Lagna' if venus_in_lagna else 'अनुपस्थित / Not present'}</p>
        <p><strong>फल / Effect:</strong> आकर्षक व्यक्तित्व, कलात्मक प्रतिभा, सौंदर्य<br><span style="font-size:11px;color:#666;">Attractive personality, artistic talent, beauty</span></p>
    </div>

    <div class="yoga-card {'active' if kemadruma_bhang else ''}">
        <h4>{'✅' if kemadruma_bhang else '⬜'} केमद्रुम भंग योग / Kemadruma Bhanga</h4>
        <p><strong>क्या है / What:</strong> चंद्र के आसपास के भावों में ग्रह / Planets near Moon's houses</p>
        <p><strong>स्थिति / Status:</strong> {'चंद्र संरक्षित है ✓ / Moon is protected' if kemadruma_bhang else 'चंद्र अकेला / Moon alone'}</p>
        <p><strong>फल / Effect:</strong> मानसिक स्थिरता, सामाजिक सम्मान<br><span style="font-size:11px;color:#666;">Mental stability, social respect</span></p>
    </div>
    '''

    if dhana_yoga:
        html += f'''
    <div class="yoga-card active">
        <h4>✅ धन योग / Dhana Yoga (Wealth Yoga)</h4>
        <p><strong>क्या है / What:</strong> द्वितीय भाव (धन भाव) में एक से अधिक ग्रह / Multiple planets in 2nd house (wealth house)</p>
        <p><strong>स्थिति / Status:</strong> 2nd भाव में {len(second_planets)} ग्रह उपस्थित ✓ / {len(second_planets)} planets in 2nd house</p>
        <p><strong>फल / Effect:</strong> बहुस्रोतीय आय, धन संचय, पारिवारिक सुख<br><span style="font-size:11px;color:#666;">Multiple income sources, wealth accumulation, family happiness</span></p>
    </div>
    '''

    # Check for Neecha Bhanga Raja Yoga (AUSPICIOUS!)
    neecha_bhanga = check_neecha_bhanga_raja_yoga(kundali.planets, planets_in_houses, kundali.lagna)
    if neecha_bhanga["present"]:
        yoga_planets = neecha_bhanga.get("planets", [])
        html += f'''
    <div class="yoga-card active" style="background: linear-gradient(135deg, #fff3cd 0%, #ffeeba 100%); border-left-color: #ffc107;">
        <h4>🌟 नीच भंग राज योग / Neecha Bhanga Raja Yoga (अत्यंत शुभ! / Highly Auspicious!)</h4>
        <p><strong>क्या है / What:</strong> नीच राशि का ग्रह जिसका दोष निरस्त हो गया / Debilitated planet whose weakness is cancelled</p>
        <p><strong>ग्रह / Planet:</strong> '''
        for yp in yoga_planets:
            html += f'{yp["planet_hindi"]} '
        html += '''</p>
        <p><strong>फल / Effect:</strong> नीच ग्रह राजयोग देता है! कठिनाई से अप्रत्याशित सफलता, उच्च पद।<br>
        <span style="font-size:11px;color:#666;">Debilitated planet gives Raja Yoga! Unexpected success from struggles, high position.<br>
        यह योग बहुत विशेष है - जीवन में कठिनाइयों के बाद महान सफलता मिलती है। / This yoga is very special - great success comes after life struggles.</span></p>
    </div>
    '''

    html += '''
    </div>
    '''

    # Check for Doshas with cancellations
    kaal_sarp = check_kaal_sarp_dosh(kundali.planets, planets_in_houses)
    pitra_dosh = check_pitra_dosh(kundali.planets, planets_in_houses, kundali.lagna)

    # Add Dosha section if any present
    if kaal_sarp["present"] or pitra_dosh["present"]:
        html += '''
    <div class="detail-box">
        <h3>⚠️ विशेष दोष विश्लेषण</h3>
    </div>
    <div class="yoga-grid">
    '''

        # Kaal Sarp Dosh
        if kaal_sarp["present"]:
            cancelled = kaal_sarp.get("cancelled", False)
            partial = kaal_sarp.get("partial", False)
            cancellations = kaal_sarp.get("cancellations", [])

            rahu_house = ketu_house = 0
            for h, p in planets_in_houses.items():
                if 'RAHU' in p: rahu_house = h
                if 'KETU' in p: ketu_house = h

            if cancelled:
                html += f'''
        <div class="yoga-card" style="background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); border-left-color: #28a745;">
            <h4>🐍 काल सर्प दोष (✅ निरस्त)</h4>
            <p><strong>राहु:</strong> भाव {rahu_house} | <strong>केतु:</strong> भाव {ketu_house}</p>
            <p><strong>स्थिति:</strong> सभी ग्रह राहु-केतु अक्ष में, <span style="color: green; font-weight: bold;">पर दोष निरस्त!</span></p>
            <p><strong>निवारण कारण:</strong></p>
            <ul>'''
                for c in cancellations:
                    html += f'<li>✅ {c}</li>'
                html += '''</ul>
        </div>
        '''
            elif partial:
                html += f'''
        <div class="yoga-card" style="background: linear-gradient(135deg, #fff3cd 0%, #ffeeba 100%); border-left-color: #ffc107;">
            <h4>🐍 काल सर्प दोष (आंशिक)</h4>
            <p><strong>राहु:</strong> भाव {rahu_house} | <strong>केतु:</strong> भाव {ketu_house}</p>
            <p><strong>स्थिति:</strong> आंशिक निवारण</p>
            <p><strong>उपाय:</strong> नाग पूजा, राहु-केतु मंत्र जाप</p>
        </div>
        '''
            else:
                html += f'''
        <div class="yoga-card" style="background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); border-left-color: #dc3545;">
            <h4>🐍 काल सर्प दोष (❌ सक्रिय)</h4>
            <p><strong>राहु:</strong> भाव {rahu_house} | <strong>केतु:</strong> भाव {ketu_house}</p>
            <p><strong>प्रभाव:</strong> जीवन में बाधाएं, विलंब, अचानक समस्याएं</p>
            <p><strong>उपाय:</strong> नाग पूजा करें, त्र्यंबकेश्वर/कालहस्ती में सर्प दोष शांति</p>
        </div>
        '''

        # Pitra Dosh
        if pitra_dosh["present"]:
            cancelled = pitra_dosh.get("cancelled", False)
            reasons = pitra_dosh.get("reasons", [])
            cancellations = pitra_dosh.get("cancellations", [])

            if cancelled:
                html += f'''
        <div class="yoga-card" style="background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); border-left-color: #28a745;">
            <h4>🙏 पितृ दोष (✅ शांत)</h4>
            <p><strong>कारण:</strong> {', '.join(reasons)}</p>
            <p><strong>स्थिति:</strong> <span style="color: green; font-weight: bold;">शुभ योगों से शांत!</span></p>
            <p><strong>शांति कारण:</strong></p>
            <ul>'''
                for c in cancellations:
                    html += f'<li>✅ {c}</li>'
                html += '''</ul>
        </div>
        '''
            else:
                html += f'''
        <div class="yoga-card" style="background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); border-left-color: #dc3545;">
            <h4>🙏 पितृ दोष (❌ सक्रिय)</h4>
            <p><strong>कारण:</strong> {', '.join(reasons)}</p>
            <p><strong>प्रभाव:</strong> पैतृक संपत्ति में समस्या, संतान बाधा</p>
            <p><strong>उपाय:</strong> पितृ पक्ष में श्राद्ध, गया जी में पिंड दान</p>
        </div>
        '''

        html += '''
    </div>
    '''

    return html


def get_planetary_strength_analysis(kundali):
    """
    Generate comprehensive planetary strength analysis using BPHS components.

    Components:
    - Shadbala (6-fold strength) - BPHS Chapter 27
    - Combustion (Asta) - BPHS Chapter 25
    - Planetary War (Graha Yuddha) - BPHS Chapter 17
    - Navamsa D9 dignity - BPHS Chapter 6
    """
    html = '''
    <div class="detail-section">
        <h2>🔬 ग्रह बल विश्लेषण (Planetary Strength Analysis)</h2>
        <p><em>BPHS आधारित षड्बल एवं अन्य बल गणना</em></p>
    '''

    planets = kundali.planets

    # ========================================
    # SHADBALA ANALYSIS
    # ========================================
    if SHADBALA_AVAILABLE:
        html += '''
        <div class="detail-box highlight-blue">
            <h3>📊 षड्बल / Shadbala (Six-fold Strength) - BPHS Ch. 27</h3>
            <table class="detail-table">
                <tr>
                    <th>ग्रह</th>
                    <th>स्थान बल</th>
                    <th>दिक् बल</th>
                    <th>काल बल</th>
                    <th>चेष्टा बल</th>
                    <th>नैसर्गिक बल</th>
                    <th>दृक् बल</th>
                    <th>कुल</th>
                    <th>स्तर</th>
                </tr>
        '''

        try:
            calc = ShadbalaCalculator(kundali)
            all_shadbala = calc.get_all_shadbala()

            strength_hindi = {
                "very_strong": "अति बली",
                "strong": "बली",
                "average": "सामान्य",
                "weak": "दुर्बल"
            }

            strength_colors = {
                "very_strong": "#28a745",
                "strong": "#17a2b8",
                "average": "#ffc107",
                "weak": "#dc3545"
            }

            for planet in ["SUN", "MOON", "MARS", "MERCURY", "JUPITER", "VENUS", "SATURN"]:
                if planet in all_shadbala:
                    sb = all_shadbala[planet]
                    hindi_name = PLANET_NAMES[Planet[planet]]["hindi"]
                    level_hindi = strength_hindi.get(sb.strength_level, "सामान्य")
                    color = strength_colors.get(sb.strength_level, "#ffc107")

                    html += f'''
                <tr>
                    <td><strong>{hindi_name}</strong></td>
                    <td>{sb.sthana_bala:.1f}</td>
                    <td>{sb.dig_bala:.1f}</td>
                    <td>{sb.kaala_bala:.1f}</td>
                    <td>{sb.chesta_bala:.1f}</td>
                    <td>{sb.naisargika_bala:.1f}</td>
                    <td>{sb.drik_bala:.1f}</td>
                    <td><strong>{sb.total:.1f}</strong></td>
                    <td style="color: {color}; font-weight: bold;">{level_hindi}</td>
                </tr>
                    '''
        except Exception as e:
            html += f'<tr><td colspan="9">षड्बल गणना में त्रुटि: {str(e)}</td></tr>'

        html += '''
            </table>
            <p><em>न्यूनतम आवश्यक बल: सूर्य/गुरु=390, चंद्र=360, मंगल/शनि=300, बुध=420, शुक्र=330</em></p>
        </div>
        '''

    # ========================================
    # COMBUSTION ANALYSIS
    # ========================================
    if ACCURACY_COMPONENTS_AVAILABLE:
        html += '''
        <div class="detail-box">
            <h3>🔥 अस्त ग्रह (Combustion) - BPHS Ch. 25</h3>
        '''

        sun_long = planets.get("SUN", {}).get("longitude", 0)
        combust_planets = []

        for planet_name in ["MOON", "MARS", "MERCURY", "JUPITER", "VENUS", "SATURN"]:
            if planet_name in planets:
                p_long = planets[planet_name].get("longitude", 0)
                is_retro = planets[planet_name].get("is_retrograde", False)
                is_combust, severity = check_combustion(planet_name, p_long, sun_long, is_retro)

                if is_combust:
                    hindi_name = PLANET_NAMES[Planet[planet_name]]["hindi"]
                    combust_planets.append({
                        "planet": planet_name,
                        "hindi": hindi_name,
                        "severity": severity
                    })

        if combust_planets:
            html += '''
            <table class="detail-table">
                <tr><th>ग्रह</th><th>तीव्रता</th><th>प्रभाव</th><th>उपाय</th></tr>
            '''

            # Get lagna for personalized combustion remedies
            comb_lagna = kundali.lagna.get('rashi', 'Mesha')

            # Base effects (same for all)
            combustion_effects = {
                "MOON": "मानसिक अशांति, माता से दूरी",
                "MARS": "साहस में कमी, भाई से विवाद",
                "MERCURY": "व्यापार में हानि, वाणी दोष",
                "JUPITER": "गुरु कृपा में कमी, विद्या बाधा",
                "VENUS": "वैवाहिक समस्या, सुख में कमी",
                "SATURN": "कार्य में देरी, मेहनत का फल कम",
            }

            # Remedies vary based on whether planet is benefic/malefic for lagna
            def get_combustion_remedy(planet, lagna):
                planet_effect = get_lagna_specific_dasha_effect(planet.title(), lagna)
                is_benefic = planet_effect['is_benefic'] or planet_effect['is_yogakaraka']

                if is_benefic:
                    # Strengthen the benefic planet
                    benefic_remedies = {
                        "MOON": "सोमवार व्रत, शिव पूजा, मोती धारण शुभ",
                        "MARS": "हनुमान चालीसा, मूंगा धारण शुभ",
                        "MERCURY": "बुध मंत्र, पन्ना धारण शुभ",
                        "JUPITER": "गुरुवार व्रत, पीला दान, पुखराज शुभ",
                        "VENUS": "शुक्र मंत्र, हीरा/ओपल शुभ",
                        "SATURN": "शनि मंत्र, नीलम धारण शुभ",
                    }
                    return benefic_remedies.get(planet, "ग्रह मंत्र जाप") + " (शुभ ग्रह - मजबूत करें)"
                else:
                    # Pacify the malefic planet (don't strengthen)
                    malefic_remedies = {
                        "MOON": "शिव पूजा करें, लेकिन मोती न पहनें",
                        "MARS": "हनुमान चालीसा, मूंगा न पहनें",
                        "MERCURY": "विष्णु पूजा, पन्ना न पहनें",
                        "JUPITER": "विष्णु पूजा, पीला दान करें लेकिन पुखराज न पहनें",
                        "VENUS": "लक्ष्मी पूजा, हीरा न पहनें",
                        "SATURN": "हनुमान पूजा, नीलम न पहनें, शनि को शांत करें",
                    }
                    return malefic_remedies.get(planet, "शांति पूजा") + " (कठिन ग्रह - शांत करें)"

            for cp in combust_planets:
                effect = combustion_effects.get(cp["planet"], "सामान्य प्रभाव")
                remedy = get_combustion_remedy(cp["planet"], comb_lagna)
                severity_text = "तीव्र" if cp["severity"] > 0.7 else "मध्यम" if cp["severity"] > 0.4 else "हल्का"
                html += f'''
                <tr>
                    <td><strong>{cp["hindi"]}</strong></td>
                    <td style="color: {"red" if cp["severity"] > 0.5 else "orange"};">{severity_text} ({cp["severity"]:.0%})</td>
                    <td>{effect}</td>
                    <td>{remedy}</td>
                </tr>
                '''
            html += '</table>'
        else:
            html += '<p style="color: green;">✅ <strong>कोई ग्रह अस्त नहीं है।</strong> सभी ग्रह अपना पूर्ण फल दे रहे हैं।</p>'

        html += '</div>'

    # ========================================
    # PLANETARY WAR ANALYSIS
    # ========================================
    if ACCURACY_COMPONENTS_AVAILABLE:
        html += '''
        <div class="detail-box">
            <h3>⚔️ ग्रह युद्ध (Planetary War) - BPHS Ch. 17</h3>
        '''

        positions = {p: {"longitude": data.get("longitude", 0)} for p, data in planets.items()}
        wars = check_planetary_war(positions)

        if wars:
            html += '''
            <table class="detail-table">
                <tr><th>विजयी ग्रह</th><th>पराजित ग्रह</th><th>दूरी</th><th>प्रभाव</th></tr>
            '''
            for war in wars:
                winner_hindi = PLANET_NAMES[Planet[war["winner"]]]["hindi"]
                loser_hindi = PLANET_NAMES[Planet[war["loser"]]]["hindi"]
                html += f'''
                <tr>
                    <td style="color: green;"><strong>{winner_hindi}</strong> (विजयी)</td>
                    <td style="color: red;"><strong>{loser_hindi}</strong> (पराजित)</td>
                    <td>{war["distance"]:.2f}°</td>
                    <td>{loser_hindi} के फल में 30% कमी</td>
                </tr>
                '''
            html += '</table>'
        else:
            html += '<p style="color: green;">✅ <strong>कोई ग्रह युद्ध नहीं है।</strong></p>'

        html += '</div>'

    # ========================================
    # NAVAMSA D9 STRENGTH
    # ========================================
    if ACCURACY_COMPONENTS_AVAILABLE:
        html += '''
        <div class="detail-box">
            <h3>🔮 नवांश (D9) बल - BPHS Ch. 6</h3>
            <p><em>नवांश में ग्रह की स्थिति विवाह और आत्मिक बल दर्शाती है</em></p>
            <table class="detail-table">
                <tr><th>ग्रह</th><th>नवांश स्थिति</th><th>बल संशोधक</th></tr>
        '''

        for planet_name in ["SUN", "MOON", "MARS", "MERCURY", "JUPITER", "VENUS", "SATURN"]:
            if planet_name in planets:
                p_long = planets[planet_name].get("longitude", 0)
                navamsa_mod = get_navamsa_strength_modifier(planet_name, p_long)
                hindi_name = PLANET_NAMES[Planet[planet_name]]["hindi"]

                if navamsa_mod > 0:
                    status = "स्वक्षेत्री/उच्च (बली)"
                    color = "green"
                elif navamsa_mod < 0:
                    status = "नीच (दुर्बल)"
                    color = "red"
                else:
                    status = "सामान्य"
                    color = "gray"

                html += f'''
                <tr>
                    <td><strong>{hindi_name}</strong></td>
                    <td style="color: {color};">{status}</td>
                    <td>{navamsa_mod:+.2f}</td>
                </tr>
                '''

        html += '''
            </table>
        </div>
        '''

    # ========================================
    # SUMMARY
    # ========================================
    html += '''
    <div class="detail-box highlight-green">
        <h3>📈 बल विश्लेषण सारांश</h3>
        <p><strong>गणना स्रोत:</strong></p>
        <ul>
            <li>षड्बल - बृहत् पाराशर होरा शास्त्र, अध्याय 27</li>
            <li>अस्त ग्रह - बृहत् पाराशर होरा शास्त्र, अध्याय 25</li>
            <li>ग्रह युद्ध - बृहत् पाराशर होरा शास्त्र, अध्याय 17</li>
            <li>नवांश बल - बृहत् पाराशर होरा शास्त्र, अध्याय 6</li>
        </ul>
        <p><em>बली ग्रह अपने भाव का शुभ फल देते हैं, दुर्बल ग्रह का फल कम होता है।</em></p>
    </div>
    </div>
    '''

    return html


def get_full_remedies(kundali, planets_in_houses):
    """Generate comprehensive remedies section based on actual lagna."""
    lagna = kundali.lagna['rashi']

    # Lagna-specific data
    LAGNA_REMEDIES = {
        "Mesha": {
            "lord": "मंगल", "lord_en": "Mars",
            "color": "लाल, नारंगी", "number": "9, 18, 27, 36",
            "day": "मंगलवार", "stone": "मूंगा (Red Coral)", "stone_alt": "कार्नेलियन",
            "metal": "तांबा", "direction": "दक्षिण",
            "stone_weight": "6-9 रत्ती", "finger": "अनामिका",
            "mantra": "ॐ क्रां क्रीं क्रौं सः भौमाय नमः",
            "avoid_stone": "नीलम, पन्ना"
        },
        "Vrishabha": {
            "lord": "शुक्र", "lord_en": "Venus",
            "color": "सफेद, गुलाबी, हल्का नीला", "number": "6, 15, 24, 33",
            "day": "शुक्रवार", "stone": "हीरा (Diamond)", "stone_alt": "ओपल, जरकन",
            "metal": "चांदी", "direction": "दक्षिण-पूर्व",
            "stone_weight": "0.5-1 कैरेट", "finger": "मध्यमा",
            "mantra": "ॐ द्रां द्रीं द्रौं सः शुक्राय नमः",
            "avoid_stone": "मूंगा, पुखराज"
        },
        "Mithuna": {
            "lord": "बुध", "lord_en": "Mercury",
            "color": "हरा", "number": "5, 14, 23, 32",
            "day": "बुधवार", "stone": "पन्ना (Emerald)", "stone_alt": "पेरिडॉट",
            "metal": "कांसा", "direction": "उत्तर",
            "stone_weight": "3-5 रत्ती", "finger": "कनिष्ठा",
            "mantra": "ॐ बुं बुधाय नमः",
            "avoid_stone": "मूंगा, माणिक्य"
        },
        "Karka": {
            "lord": "चंद्र", "lord_en": "Moon",
            "color": "सफेद, चांदी, हल्का हरा", "number": "2, 11, 20, 29",
            "day": "सोमवार", "stone": "मोती (Pearl)", "stone_alt": "मूनस्टोन",
            "metal": "चांदी", "direction": "उत्तर-पश्चिम",
            "stone_weight": "4-6 रत्ती", "finger": "कनिष्ठा",
            "mantra": "ॐ श्रां श्रीं श्रौं सः चंद्राय नमः",
            "avoid_stone": "नीलम, पन्ना, हीरा",
            "yogakaraka": "मंगल", "yogakaraka_stone": "मूंगा (Red Coral)"
        },
        "Simha": {
            "lord": "सूर्य", "lord_en": "Sun",
            "color": "सुनहरा, नारंगी, लाल", "number": "1, 10, 19, 28",
            "day": "रविवार", "stone": "माणिक्य (Ruby)", "stone_alt": "गार्नेट",
            "metal": "सोना", "direction": "पूर्व",
            "stone_weight": "3-6 रत्ती", "finger": "अनामिका",
            "mantra": "ॐ ह्रां ह्रीं ह्रौं सः सूर्याय नमः",
            "avoid_stone": "नीलम, हीरा",
            "yogakaraka": "मंगल", "yogakaraka_stone": "मूंगा (Red Coral)"
        },
        "Kanya": {
            "lord": "बुध", "lord_en": "Mercury",
            "color": "हरा, हल्का पीला", "number": "5, 14, 23, 32",
            "day": "बुधवार", "stone": "पन्ना (Emerald)", "stone_alt": "पेरिडॉट",
            "metal": "कांसा", "direction": "उत्तर",
            "stone_weight": "3-5 रत्ती", "finger": "कनिष्ठा",
            "mantra": "ॐ बुं बुधाय नमः",
            "avoid_stone": "मूंगा, मोती, पुखराज"
        },
        "Tula": {
            "lord": "शुक्र", "lord_en": "Venus",
            "color": "सफेद, हल्का नीला", "number": "6, 15, 24, 33",
            "day": "शुक्रवार", "stone": "हीरा (Diamond)", "stone_alt": "ओपल",
            "metal": "चांदी", "direction": "पश्चिम",
            "stone_weight": "0.5-1 कैरेट", "finger": "मध्यमा",
            "mantra": "ॐ द्रां द्रीं द्रौं सः शुक्राय नमः",
            "avoid_stone": "माणिक्य, मूंगा, पुखराज",
            "yogakaraka": "शनि", "yogakaraka_stone": "नीलम (Blue Sapphire)"
        },
        "Vrishchika": {
            "lord": "मंगल", "lord_en": "Mars",
            "color": "लाल, मैरून", "number": "9, 18, 27, 36",
            "day": "मंगलवार", "stone": "मूंगा (Red Coral)", "stone_alt": "कार्नेलियन",
            "metal": "तांबा", "direction": "दक्षिण",
            "stone_weight": "6-9 रत्ती", "finger": "अनामिका",
            "mantra": "ॐ क्रां क्रीं क्रौं सः भौमाय नमः",
            "avoid_stone": "पन्ना, हीरा"
        },
        "Dhanu": {
            "lord": "गुरु", "lord_en": "Jupiter",
            "color": "पीला, सुनहरा", "number": "3, 12, 21, 30",
            "day": "गुरुवार", "stone": "पुखराज (Yellow Sapphire)", "stone_alt": "सिट्रीन",
            "metal": "सोना", "direction": "उत्तर-पूर्व",
            "stone_weight": "3-5 रत्ती", "finger": "तर्जनी",
            "mantra": "ॐ ग्रां ग्रीं ग्रौं सः गुरवे नमः",
            "avoid_stone": "हीरा, नीलम, पन्ना"
        },
        "Makara": {
            "lord": "शनि", "lord_en": "Saturn",
            "color": "नीला, काला, बैंगनी", "number": "8, 17, 26, 35",
            "day": "शनिवार", "stone": "नीलम (Blue Sapphire)", "stone_alt": "एमेथिस्ट",
            "metal": "लोहा", "direction": "पश्चिम",
            "stone_weight": "2-5 रत्ती", "finger": "मध्यमा",
            "mantra": "ॐ प्रां प्रीं प्रौं सः शनैश्चराय नमः",
            "avoid_stone": "मूंगा, मोती, पुखराज",
            "yogakaraka": "शुक्र", "yogakaraka_stone": "हीरा (Diamond)"
        },
        "Kumbha": {
            "lord": "शनि", "lord_en": "Saturn",
            "color": "नीला, बैंगनी", "number": "8, 17, 26, 35",
            "day": "शनिवार", "stone": "नीलम (Blue Sapphire)", "stone_alt": "एमेथिस्ट",
            "metal": "लोहा", "direction": "पश्चिम",
            "stone_weight": "2-5 रत्ती", "finger": "मध्यमा",
            "mantra": "ॐ प्रां प्रीं प्रौं सः शनैश्चराय नमः",
            "avoid_stone": "मोती, मूंगा, पुखराज",
            "yogakaraka": "शुक्र", "yogakaraka_stone": "हीरा (Diamond)"
        },
        "Meena": {
            "lord": "गुरु", "lord_en": "Jupiter",
            "color": "पीला, सुनहरा, हल्का गुलाबी", "number": "3, 12, 21, 30",
            "day": "गुरुवार", "stone": "पुखराज (Yellow Sapphire)", "stone_alt": "सिट्रीन",
            "metal": "सोना", "direction": "उत्तर-पूर्व",
            "stone_weight": "3-5 रत्ती", "finger": "तर्जनी",
            "mantra": "ॐ ग्रां ग्रीं ग्रौं सः गुरवे नमः",
            "avoid_stone": "माणिक्य, हीरा, नीलम, पन्ना"
        },
    }

    data = LAGNA_REMEDIES.get(lagna, LAGNA_REMEDIES["Mesha"])
    rashi_hindi = {
        "Mesha": "मेष", "Vrishabha": "वृषभ", "Mithuna": "मिथुन", "Karka": "कर्क",
        "Simha": "सिंह", "Kanya": "कन्या", "Tula": "तुला", "Vrishchika": "वृश्चिक",
        "Dhanu": "धनु", "Makara": "मकर", "Kumbha": "कुंभ", "Meena": "मीन"
    }

    lagna_hindi = rashi_hindi.get(lagna, lagna)

    # Yogakaraka section
    yogakaraka_html = ""
    if data.get("yogakaraka"):
        yogakaraka_html = f'''
        <tr class="highlight-row"><td>योगकारक रत्न</td><td>{data['yogakaraka_stone']}</td><td>{data['yogakaraka']} (योगकारक ग्रह)</td></tr>'''

    html = f'''
    <div class="detail-box">
        <h3>🔮 {lagna_hindi} लग्न के शुभ तत्व / Auspicious Elements for {lagna_hindi} ({lagna}) Ascendant</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); padding: 15px; border-radius: 10px; margin-bottom: 15px; border-left: 4px solid #10b981;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 शुभ तत्व कैसे निर्धारित होते हैं? / How are auspicious elements determined?</strong><br><br>
                हर लग्न का एक <strong>लग्नेश</strong> (स्वामी ग्रह) होता है। आपके लग्नेश <strong>{data['lord']} ({data['lord_en']})</strong> हैं।
                इस ग्रह से जुड़े रंग, अंक, दिन, रत्न आदि आपके लिए शुभ माने जाते हैं क्योंकि ये आपके लग्नेश को बल देते हैं।<br><br>
                <em>Every ascendant has a <strong>Lagna Lord</strong> (ruling planet). Your Lagna Lord is <strong>{data['lord']} ({data['lord_en']})</strong>.
                Colors, numbers, days, gemstones associated with this planet are auspicious for you as they strengthen your Lagna Lord.</em>
            </p>
        </div>
        <table class="detail-table">
            <tr><th>तत्व / Element</th><th>शुभ / Auspicious</th><th>विवरण / Details</th></tr>
            <tr><td><strong>लग्नेश / Lagna Lord</strong></td><td>{data['lord']} ({data['lord_en']})</td><td>{lagna_hindi} लग्न के स्वामी - सबसे महत्वपूर्ण ग्रह<br><span style="font-size:11px;color:#666;">Ruler of your ascendant - most important planet</span></td></tr>
            <tr><td><strong>शुभ रंग / Lucky Colors</strong></td><td>{data['color']}</td><td>{data['lord']} के रंग पहनने से लग्नेश बली होता है<br><span style="font-size:11px;color:#666;">Wearing these colors strengthens Lagna Lord</span></td></tr>
            <tr><td><strong>शुभ अंक / Lucky Numbers</strong></td><td>{data['number']}</td><td>महत्वपूर्ण निर्णयों के लिए इन अंकों का उपयोग करें<br><span style="font-size:11px;color:#666;">Use these numbers for important decisions</span></td></tr>
            <tr><td><strong>शुभ दिन / Lucky Day</strong></td><td>{data['day']}</td><td>नए कार्य इस दिन शुरू करें<br><span style="font-size:11px;color:#666;">Start new ventures on this day</span></td></tr>
            <tr><td><strong>शुभ रत्न / Main Gemstone</strong></td><td><b>{data['stone']}</b></td><td>{data['lord']} का मुख्य रत्न - सबसे प्रभावशाली<br><span style="font-size:11px;color:#666;">Main gemstone of {data['lord_en']} - most effective</span></td></tr>
            <tr><td><strong>वैकल्पिक रत्न / Alternate Stone</strong></td><td>{data['stone_alt']}</td><td>बजट विकल्प - समान प्रभाव, कम कीमत<br><span style="font-size:11px;color:#666;">Budget option - similar effect, lower cost</span></td></tr>{yogakaraka_html}
            <tr><td><strong>शुभ धातु / Lucky Metal</strong></td><td>{data['metal']}</td><td>रत्न इसी धातु में पहनें<br><span style="font-size:11px;color:#666;">Wear gemstone in this metal</span></td></tr>
            <tr><td><strong>शुभ दिशा / Lucky Direction</strong></td><td>{data['direction']}</td><td>कार्यस्थल/अध्ययन कक्ष इस दिशा में रखें<br><span style="font-size:11px;color:#666;">Place workspace/study room in this direction</span></td></tr>
            <tr class="status-caution"><td><strong>❌ न पहनें / Avoid</strong></td><td>{data['avoid_stone']}</td><td>ये रत्न आपके अशुभ ग्रहों के हैं - हानिकारक हो सकते हैं<br><span style="font-size:11px;color:#666;">These are gemstones of your malefic planets - can be harmful</span></td></tr>
        </table>
    </div>

    <div class="detail-box">
        <h3>💎 रत्न धारण विधि / How to Wear Gemstone</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #f59e0b;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 रत्न सही तरीके से पहनना क्यों जरूरी है? / Why is correct method important?</strong><br>
                रत्न का प्रभाव तभी मिलता है जब इसे <strong>सही वजन, सही धातु, सही अंगुली और सही समय</strong> पर पहना जाए।
                गलत तरीके से पहनने पर लाभ नहीं मिलता या हानि भी हो सकती है।<br>
                <em>Gemstone works only when worn with <strong>correct weight, metal, finger and timing</strong>.
                Wrong method may give no benefit or even harm.</em>
            </p>
        </div>
        <table class="detail-table">
            <tr><th>रत्न / Gemstone</th><th>वजन / Weight</th><th>धातु / Metal</th><th>अंगुली / Finger</th><th>दिन/समय / Day/Time</th></tr>
            <tr><td><strong>{data['stone']}</strong> (Primary)</td><td>{data['stone_weight']}</td><td>सोना/चांदी<br><span style="font-size:10px;">Gold/Silver</span></td><td>{data['finger']}</td><td>{data['day']}, सूर्योदय<br><span style="font-size:10px;">At sunrise</span></td></tr>
        </table>
        <p class="warning" style="background: #fef2f2; padding: 10px; border-radius: 6px; border-left: 4px solid #ef4444;">
            ⚠️ <strong>महत्वपूर्ण / Important:</strong> रत्न धारण से पहले किसी अनुभवी ज्योतिषी से परामर्श अवश्य करें!
            कुंडली का पूर्ण विश्लेषण करके ही रत्न पहनें।<br>
            <em>Always consult an experienced astrologer before wearing any gemstone! Get full chart analysis first.</em>
        </p>
    </div>

    {get_lagna_specific_remedies_html(lagna, data)}
    '''

    return html


def get_full_transit_analysis(kundali, planets_in_houses, house_rashis, rashi_hindi):
    """
    Generate comprehensive transit analysis including Sade Sati, current transits,
    and event predictions.

    Args:
        kundali: Kundali object
        planets_in_houses: Dict mapping house numbers to planet lists
        house_rashis: Dict mapping house numbers to rashi info
        rashi_hindi: Dict mapping rashi names to Hindi names

    Returns:
        HTML string with transit analysis
    """
    from datetime import datetime

    # Try to import transit modules - handle gracefully if not available
    try:
        from .transit import TransitCalculator
        from .sade_sati_transit import SadeSatiTracker
        from .event_predictor import EventPredictor
        transit_modules_available = True
    except ImportError:
        transit_modules_available = False

    html = ""

    if not transit_modules_available:
        html = '''
        <div class="detail-box highlight-yellow">
            <h3>Transit Analysis</h3>
            <p>Transit modules not available. Please check installation.</p>
        </div>
        '''
        return html

    # Get current date
    current_date = datetime.now()
    current_year = current_date.year

    # ========== CRITICAL FIX: Use CURRENT transit positions, NOT natal positions ==========
    # Transit analysis requires where planets are TODAY, not where they were at birth

    # Get NATAL Moon position (this is fixed - used as reference point)
    moon_rashi_num = kundali.planets['MOON']['rashi_num']
    moon_rashi = kundali.planets['MOON']['rashi']
    lagna_num = kundali.lagna['rashi_num']

    # Get CURRENT transit positions using TransitCalculator
    transit_calc = TransitCalculator(kundali)
    current_positions = transit_calc.get_transit_positions(current_date)

    # Extract CURRENT (not natal) planet positions
    saturn_rashi_num = current_positions['SATURN']['rashi_num']
    saturn_rashi = current_positions['SATURN']['rashi']
    jupiter_rashi_num = current_positions['JUPITER']['rashi_num']
    jupiter_rashi = current_positions['JUPITER']['rashi']
    rahu_rashi_num = current_positions['RAHU']['rashi_num']
    rahu_rashi = current_positions['RAHU']['rashi']
    ketu_rashi_num = current_positions['KETU']['rashi_num']
    ketu_rashi = current_positions['KETU']['rashi']

    # Also get Sun and Mars current positions for additional transit info
    sun_rashi_num = current_positions['SUN']['rashi_num']
    sun_rashi = current_positions['SUN']['rashi']
    mars_rashi_num = current_positions['MARS']['rashi_num']
    mars_rashi = current_positions['MARS']['rashi']

    # Calculate houses from Moon
    def house_from_moon(planet_rashi_num):
        return ((planet_rashi_num - moon_rashi_num) % 12) + 1

    saturn_house_from_moon = house_from_moon(saturn_rashi_num)
    jupiter_house_from_moon = house_from_moon(jupiter_rashi_num)
    rahu_house_from_moon = house_from_moon(rahu_rashi_num)
    ketu_house_from_moon = house_from_moon(ketu_rashi_num)

    # Get lagna for personalized transit effects
    lagna = kundali.lagna.get('rashi', 'Mesha')
    saturn_lagna_effect = get_lagna_specific_dasha_effect("Saturn", lagna)
    jupiter_lagna_effect = get_lagna_specific_dasha_effect("Jupiter", lagna)

    # ========== SECTION 1: CURRENT TRANSIT OVERVIEW ==========
    current_date_str = current_date.strftime('%d-%m-%Y')
    html += f'''
    <div class="detail-box">
        <h3>🌍 वर्तमान ग्रह गोचर / Current Planetary Transits</h3>
        <div class="info-note" style="background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #10b981;">
            <p style="margin: 0; font-size: 14px; color: #065f46;">
                <strong>📅 आज की तिथि / Today's Date: {current_date_str}</strong><br>
                नीचे दी गई ग्रह स्थितियां <strong>आज आकाश में वास्तविक स्थिति</strong> हैं, जन्म कुंडली की नहीं।<br>
                <em>The planet positions below are <strong>REAL-TIME positions in the sky today</strong>, not birth chart positions.</em>
            </p>
        </div>
        <div class="info-note" style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); padding: 15px; border-radius: 10px; margin-bottom: 15px; border-left: 4px solid #3b82f6;">
            <p style="margin: 0; font-size: 13px;">
                <strong>💡 गोचर (Transit) क्या है? / What is Transit?</strong><br><br>
                <strong>गोचर</strong> = ग्रहों की वर्तमान आकाश में स्थिति। जन्म कुंडली स्थिर होती है, लेकिन ग्रह आकाश में चलते रहते हैं।
                जब ये चलते हुए ग्रह आपकी जन्म कुंडली के विभिन्न भावों से गुजरते हैं, तो विशेष प्रभाव देते हैं।<br><br>
                <strong>"चंद्र से भाव"</strong> = आपके जन्म चंद्रमा ({rashi_hindi.get(moon_rashi, moon_rashi)}) से गिनती करके ग्रह किस भाव में है।<br><br>
                <em><strong>Transit</strong> = Current position of planets in the sky. Birth chart is fixed, but planets keep moving.
                When these moving planets pass through different houses of your birth chart, they give specific effects.<br>
                <strong>"House from Moon"</strong> = Counting from your birth Moon ({moon_rashi}). This is the main method to analyze transit effects.</em>
            </p>
        </div>
        <table class="detail-table">
            <tr><th>ग्रह / Planet</th><th>वर्तमान राशि / Current Sign</th><th>चंद्र से भाव / House from Moon</th><th>प्रभाव / Effect</th></tr>
    '''

    # Saturn transit effect with LAGNA-SPECIFIC context
    saturn_effect = _get_saturn_transit_effect_hindi(saturn_house_from_moon)
    saturn_lagna_note = f"<br><span style='font-size:11px; color: #059669;'>({saturn_lagna_effect['status_hindi']} for your {lagna} lagna)</span>" if saturn_lagna_effect['is_benefic'] or saturn_lagna_effect['is_yogakaraka'] else f"<br><span style='font-size:11px; color: #dc2626;'>({saturn_lagna_effect['status_hindi']} for your {lagna} lagna - do remedies)</span>"
    html += f'''
            <tr>
                <td><strong>शनि (Saturn)</strong>{saturn_lagna_note}</td>
                <td>{rashi_hindi.get(saturn_rashi, saturn_rashi)}</td>
                <td>{saturn_house_from_moon}</td>
                <td>{saturn_effect['effect']}</td>
            </tr>
    '''

    # Jupiter transit effect with LAGNA-SPECIFIC context
    jupiter_effect = _get_jupiter_transit_effect_hindi(jupiter_house_from_moon)
    jupiter_lagna_note = f"<br><span style='font-size:11px; color: #059669;'>({jupiter_lagna_effect['status_hindi']} for your {lagna} lagna)</span>" if jupiter_lagna_effect['is_benefic'] or jupiter_lagna_effect['is_yogakaraka'] else f"<br><span style='font-size:11px; color: #dc2626;'>({jupiter_lagna_effect['status_hindi']} for your {lagna} lagna)</span>"
    html += f'''
            <tr>
                <td><strong>गुरु (Jupiter)</strong>{jupiter_lagna_note}</td>
                <td>{rashi_hindi.get(jupiter_rashi, jupiter_rashi)}</td>
                <td>{jupiter_house_from_moon}</td>
                <td>{jupiter_effect['effect']}</td>
            </tr>
    '''

    # Rahu transit effect
    rahu_effect = _get_rahu_transit_effect_hindi(rahu_house_from_moon)
    html += f'''
            <tr>
                <td><strong>राहु (Rahu)</strong></td>
                <td>{rashi_hindi.get(rahu_rashi, rahu_rashi)}</td>
                <td>{rahu_house_from_moon}</td>
                <td>{rahu_effect['effect']}</td>
            </tr>
    '''

    # Ketu transit effect
    ketu_effect = _get_ketu_transit_effect_hindi(ketu_house_from_moon)
    html += f'''
            <tr>
                <td><strong>केतु (Ketu)</strong></td>
                <td>{rashi_hindi.get(ketu_rashi, ketu_rashi)}</td>
                <td>{ketu_house_from_moon}</td>
                <td>{ketu_effect['effect']}</td>
            </tr>
        </table>
    </div>
    '''

    # ========== SECTION 2: SADE SATI ANALYSIS ==========
    try:
        sade_sati_tracker = SadeSatiTracker(moon_rashi_num)
        sade_sati_status = sade_sati_tracker.is_sade_sati_active(current_date)

        if sade_sati_status['active']:
            phase = sade_sati_status['phase']
            severity = sade_sati_status['severity']

            # Get progress if active
            progress = sade_sati_tracker.get_current_sade_sati_progress()

            html += f'''
    <div class="detail-box highlight-yellow">
        <h3>⚠️ साढ़े साती सक्रिय (Sade Sati Active)</h3>
        <table class="detail-table">
            <tr><td><strong>चरण (Phase)</strong></td><td>{phase}</td></tr>
            <tr><td><strong>तीव्रता (Severity)</strong></td><td>{severity}</td></tr>
            <tr><td><strong>चंद्र राशि</strong></td><td>{rashi_hindi.get(moon_rashi, moon_rashi)}</td></tr>
            <tr><td><strong>शनि राशि</strong></td><td>{sade_sati_status.get('saturn_rashi', 'N/A')}</td></tr>
        </table>
            '''

            if progress:
                html += f'''
        <p><strong>प्रगति (Progress):</strong></p>
        <ul class="prediction-list">
            <li>समग्र प्रगति: {progress.get('overall_progress_percent', 0)}%</li>
            <li>बीता समय: {progress.get('total_elapsed_years', 0)} वर्ष</li>
            <li>शेष समय: {progress.get('total_remaining_years', 0)} वर्ष (लगभग)</li>
        </ul>
                '''

            # Get lagna-specific Saturn status for personalized remedies
            lagna = kundali.lagna.get('rashi', 'Mesha')
            saturn_effect = get_lagna_specific_dasha_effect("Saturn", lagna)
            is_saturn_benefic = saturn_effect['is_benefic'] or saturn_effect['is_yogakaraka']

            html += f'''
        <p><strong>विवरण:</strong> {sade_sati_status.get('phase_description', '')}</p>

        <p><strong>आपके {lagna} लग्न के लिए शनि:</strong> {saturn_effect['status_hindi']}</p>

        <p><strong>उपाय (आपके लग्न के अनुसार):</strong></p>
        <ul class="prediction-list">
            <li>हनुमान चालीसा का नियमित पाठ करें (सभी के लिए अनिवार्य)</li>
            <li>शनिवार को काले कपड़े न पहनें</li>'''

            # If Saturn is benefic/yogakaraka, different remedies
            if is_saturn_benefic:
                html += f'''
            <li style="color: #059669;"><strong>शनि आपके लिए शुभ ग्रह है</strong> - शनि मंत्र जाप लाभदायक: ॐ शं शनैश्चराय नमः (108 बार)</li>
            <li>शनिवार व्रत रख सकते हैं - आपके लिए शनि को मजबूत करना ठीक है</li>
            <li>काले तिल, सरसों तेल का दान करें</li>'''
            else:
                html += f'''
            <li style="color: #dc2626;"><strong>शनि आपके लग्न के लिए कठिन ग्रह है</strong> - शनि मंत्र जाप की जगह हनुमान जी पर ध्यान दें</li>
            <li>शनि को मजबूत करने वाले उपाय (नीलम, शनि मंत्र) न करें</li>
            <li>गरीबों को काले कंबल, छाता, जूते का दान करें</li>
            <li>शनिदेव की पूजा की जगह हनुमान जी की पूजा करें (शनि को शांत करता है)</li>'''

            html += '''
        </ul>
    </div>
            '''
        else:
            # Get next Sade Sati timing
            next_sade_sati = sade_sati_tracker.get_next_sade_sati(current_date)

            html += f'''
    <div class="detail-box highlight-green">
        <h3>✅ साढ़े साती सक्रिय नहीं (No Active Sade Sati)</h3>
        <p><strong>चंद्र राशि:</strong> {rashi_hindi.get(moon_rashi, moon_rashi)}</p>
        <p><strong>वर्तमान शनि राशि:</strong> {sade_sati_status.get('saturn_rashi', 'N/A')}</p>
            '''

            if next_sade_sati.get('start_date'):
                html += f'''
        <p><strong>अगली साढ़े साती:</strong></p>
        <ul class="prediction-list">
            <li>प्रारंभ: {next_sade_sati['start_date'].strftime('%B %Y')}</li>
            <li>अभी से: लगभग {next_sade_sati.get('years_from_now', 'N/A')} वर्ष बाद</li>
        </ul>
                '''

            html += '''
    </div>
            '''

    except Exception as e:
        html += f'''
    <div class="detail-box">
        <h3>साढ़े साती विश्लेषण</h3>
        <p>विश्लेषण उपलब्ध नहीं। कृपया बाद में प्रयास करें।</p>
    </div>
        '''

    # ========== SECTION 3: EVENT PREDICTIONS ==========
    try:
        event_predictor = EventPredictor(kundali)
        prediction_years = 5

        # Get predictions
        marriage_predictions = event_predictor.get_best_periods(
            "marriage", current_year, current_year + prediction_years, top_n=3
        )
        career_predictions = event_predictor.get_best_periods(
            "career", current_year, current_year + prediction_years, top_n=3
        )
        property_predictions = event_predictor.get_best_periods(
            "property", current_year, current_year + prediction_years, top_n=3
        )

        html += f'''
    <div class="detail-box">
        <h3>📅 अगले {prediction_years} वर्षों के शुभ समय (Favorable Periods)</h3>
        '''

        # Marriage timing
        html += '''
        <h4>💑 विवाह के लिए शुभ समय (Marriage Timing)</h4>
        '''
        if marriage_predictions:
            html += '<table class="detail-table"><tr><th>अवधि</th><th>दशा</th><th>अनुकूलता</th><th>कारण</th></tr>'
            for pred in marriage_predictions[:3]:
                favorability_hindi = _get_favorability_hindi(pred['favorability'])
                reasons_short = '; '.join(pred['reasons'][:2])
                html += f'''
                <tr>
                    <td>{pred['period']}</td>
                    <td>{pred['dasha']}</td>
                    <td>{favorability_hindi}</td>
                    <td>{reasons_short}</td>
                </tr>
                '''
            html += '</table>'
        else:
            html += '<p>इस अवधि में विशेष शुभ योग नहीं मिले।</p>'

        # Career timing
        html += '''
        <h4>💼 करियर उन्नति के लिए शुभ समय (Career Advancement)</h4>
        '''
        if career_predictions:
            html += '<table class="detail-table"><tr><th>अवधि</th><th>दशा</th><th>अनुकूलता</th><th>कारण</th></tr>'
            for pred in career_predictions[:3]:
                favorability_hindi = _get_favorability_hindi(pred['favorability'])
                reasons_short = '; '.join(pred['reasons'][:2])
                html += f'''
                <tr>
                    <td>{pred['period']}</td>
                    <td>{pred['dasha']}</td>
                    <td>{favorability_hindi}</td>
                    <td>{reasons_short}</td>
                </tr>
                '''
            html += '</table>'
        else:
            html += '<p>इस अवधि में विशेष शुभ योग नहीं मिले।</p>'

        # Property timing
        html += '''
        <h4>🏠 संपत्ति खरीद के लिए शुभ समय (Property Purchase)</h4>
        '''
        if property_predictions:
            html += '<table class="detail-table"><tr><th>अवधि</th><th>दशा</th><th>अनुकूलता</th><th>कारण</th></tr>'
            for pred in property_predictions[:3]:
                favorability_hindi = _get_favorability_hindi(pred['favorability'])
                reasons_short = '; '.join(pred['reasons'][:2])
                html += f'''
                <tr>
                    <td>{pred['period']}</td>
                    <td>{pred['dasha']}</td>
                    <td>{favorability_hindi}</td>
                    <td>{reasons_short}</td>
                </tr>
                '''
            html += '</table>'
        else:
            html += '<p>इस अवधि में विशेष शुभ योग नहीं मिले।</p>'

        html += '''
    </div>
        '''

    except Exception as e:
        html += f'''
    <div class="detail-box">
        <h3>शुभ समय विश्लेषण</h3>
        <p>भविष्यवाणी विश्लेषण उपलब्ध नहीं। ({str(e)})</p>
    </div>
        '''

    # ========== SECTION 4: SADE SATI TIMELINE ==========
    try:
        timeline = sade_sati_tracker.get_sade_sati_timeline(30)

        if timeline:
            html += '''
    <div class="detail-box">
        <h3>📊 साढ़े साती समयरेखा (Sade Sati Timeline - Next 30 Years)</h3>
        <table class="detail-table">
            <tr><th>चक्र</th><th>स्थिति</th><th>प्रारंभ</th><th>समाप्ति</th><th>अवधि</th></tr>
            '''

            for cycle in timeline:
                status_hindi = "वर्तमान" if cycle['status'] == 'active' else "आगामी"
                start_str = cycle['total_start_date'].strftime('%b %Y')
                end_str = cycle['total_end_date'].strftime('%b %Y')
                duration = f"{cycle['total_duration_years']:.1f} वर्ष"

                row_class = 'class="highlight-row"' if cycle['status'] == 'active' else ''

                html += f'''
            <tr {row_class}>
                <td>{cycle['cycle_number']}</td>
                <td>{status_hindi}</td>
                <td>{start_str}</td>
                <td>{end_str}</td>
                <td>{duration}</td>
            </tr>
                '''

            html += '''
        </table>
    </div>
            '''

    except Exception:
        pass  # Timeline section is optional

    return html


def _get_saturn_transit_effect_hindi(house: int) -> dict:
    """Get Saturn transit effect in Hindi based on house from Moon."""
    effects = {
        1: {"nature": "चुनौतीपूर्ण", "effect": "साढ़े साती शिखर - स्वास्थ्य और मानसिक दबाव"},
        2: {"nature": "चुनौतीपूर्ण", "effect": "साढ़े साती अंतिम चरण - वित्तीय तनाव"},
        3: {"nature": "अनुकूल", "effect": "साहस और आत्मविश्वास में वृद्धि"},
        4: {"nature": "चुनौतीपूर्ण", "effect": "घर और माता से संबंधित चिंता"},
        5: {"nature": "मिश्रित", "effect": "संतान और शिक्षा में विलंब"},
        6: {"nature": "अनुकूल", "effect": "शत्रुओं पर विजय, प्रतियोगिता में सफलता"},
        7: {"nature": "चुनौतीपूर्ण", "effect": "वैवाहिक जीवन में तनाव"},
        8: {"nature": "बहुत चुनौतीपूर्ण", "effect": "अष्टम शनि - स्वास्थ्य और बाधाओं का समय"},
        9: {"nature": "मिश्रित", "effect": "भाग्य में विलंब, पिता से संबंध"},
        10: {"nature": "मिश्रित", "effect": "करियर में मेहनत से सफलता"},
        11: {"nature": "अनुकूल", "effect": "आय में वृद्धि, इच्छापूर्ति"},
        12: {"nature": "चुनौतीपूर्ण", "effect": "साढ़े साती प्रारंभ - खर्चों में वृद्धि"}
    }
    return effects.get(house, {"nature": "तटस्थ", "effect": "सामान्य प्रभाव"})


def _get_jupiter_transit_effect_hindi(house: int) -> dict:
    """Get Jupiter transit effect in Hindi based on house from Moon."""
    effects = {
        1: {"nature": "अत्यंत शुभ", "effect": "सम्मान, स्वास्थ्य और समृद्धि"},
        2: {"nature": "शुभ", "effect": "धन लाभ और पारिवारिक सुख"},
        3: {"nature": "मिश्रित", "effect": "भाई-बहनों से मतभेद संभव"},
        4: {"nature": "मिश्रित", "effect": "गृह सुख में कमी, स्थान परिवर्तन"},
        5: {"nature": "अत्यंत शुभ", "effect": "संतान सुख, बुद्धि विकास, शुभ समाचार"},
        6: {"nature": "चुनौतीपूर्ण", "effect": "शत्रु और रोग से सावधान"},
        7: {"nature": "अत्यंत शुभ", "effect": "विवाह योग, साझेदारी में लाभ"},
        8: {"nature": "चुनौतीपूर्ण", "effect": "बाधाएं और विलंब"},
        9: {"nature": "अत्यंत शुभ", "effect": "भाग्योदय, धार्मिक यात्रा, उच्च शिक्षा"},
        10: {"nature": "शुभ", "effect": "करियर उन्नति, यश प्राप्ति"},
        11: {"nature": "अत्यंत शुभ", "effect": "सर्वत्र लाभ, इच्छापूर्ति"},
        12: {"nature": "चुनौतीपूर्ण", "effect": "खर्चों में वृद्धि, विदेश यात्रा"}
    }
    return effects.get(house, {"nature": "तटस्थ", "effect": "सामान्य प्रभाव"})


def _get_rahu_transit_effect_hindi(house: int) -> dict:
    """Get Rahu transit effect in Hindi based on house from Moon."""
    effects = {
        1: {"nature": "मिश्रित", "effect": "व्यक्तित्व में परिवर्तन, भ्रम"},
        2: {"nature": "चुनौतीपूर्ण", "effect": "वाणी और धन में समस्या"},
        3: {"nature": "अनुकूल", "effect": "साहस और नए अवसर"},
        4: {"nature": "चुनौतीपूर्ण", "effect": "मन में अशांति, गृह सुख कम"},
        5: {"nature": "मिश्रित", "effect": "संतान चिंता, अनियमित सोच"},
        6: {"nature": "अनुकूल", "effect": "शत्रुओं पर विजय"},
        7: {"nature": "चुनौतीपूर्ण", "effect": "वैवाहिक जीवन में उलझन"},
        8: {"nature": "मिश्रित", "effect": "गुप्त लाभ या हानि"},
        9: {"nature": "मिश्रित", "effect": "धर्म में अरुचि, पिता से दूरी"},
        10: {"nature": "अनुकूल", "effect": "करियर में अप्रत्याशित उन्नति"},
        11: {"nature": "अनुकूल", "effect": "विदेशी स्रोतों से लाभ"},
        12: {"nature": "मिश्रित", "effect": "विदेश यात्रा, आध्यात्मिक रुझान"}
    }
    return effects.get(house, {"nature": "तटस्थ", "effect": "सामान्य प्रभाव"})


def _get_ketu_transit_effect_hindi(house: int) -> dict:
    """Get Ketu transit effect in Hindi based on house from Moon."""
    effects = {
        1: {"nature": "मिश्रित", "effect": "आत्म-चिंतन, स्वास्थ्य ध्यान"},
        2: {"nature": "चुनौतीपूर्ण", "effect": "वाणी में कटुता, पारिवारिक मतभेद"},
        3: {"nature": "अनुकूल", "effect": "आध्यात्मिक साहस"},
        4: {"nature": "चुनौतीपूर्ण", "effect": "मन में विरक्ति"},
        5: {"nature": "मिश्रित", "effect": "संतान में आध्यात्मिक रुझान"},
        6: {"nature": "अनुकूल", "effect": "शत्रु और रोग से मुक्ति"},
        7: {"nature": "चुनौतीपूर्ण", "effect": "साथी से विरक्ति"},
        8: {"nature": "मिश्रित", "effect": "गूढ़ ज्ञान, मोक्ष मार्ग"},
        9: {"nature": "अनुकूल", "effect": "आध्यात्मिक उन्नति"},
        10: {"nature": "चुनौतीपूर्ण", "effect": "करियर में अनिश्चितता"},
        11: {"nature": "अनुकूल", "effect": "आध्यात्मिक मित्रों से लाभ"},
        12: {"nature": "अनुकूल", "effect": "मोक्ष मार्ग, विदेश में साधना"}
    }
    return effects.get(house, {"nature": "तटस्थ", "effect": "सामान्य प्रभाव"})


def _get_favorability_hindi(favorability: str) -> str:
    """Convert favorability to Hindi."""
    mapping = {
        "High": "उच्च ⭐⭐⭐",
        "Medium": "मध्यम ⭐⭐",
        "Low": "निम्न ⭐"
    }
    return mapping.get(favorability, favorability)
