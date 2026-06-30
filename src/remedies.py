"""
Comprehensive Vedic Remedies Module

Based on authentic texts:
- Brihat Parashara Hora Shastra (BPHS) - Graha Shanti chapter
- Lal Kitab remedies
- Mantra Shastra
- Ratna Shastra (Gemstone science)

Provides remedies for:
1. Weak/afflicted planets
2. Doshas (Manglik, Kaal Sarp, Pitra, etc.)
3. House-specific issues
4. General life improvements
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum


# =============================================================================
# CONSTANTS - Based on BPHS and Classical Texts
# =============================================================================

# Planet mantras from Mantra Shastra
PLANET_MANTRAS = {
    "SUN": {
        "beej_mantra": "ॐ ह्रां ह्रीं ह्रौं सः सूर्याय नमः",
        "beej_transliteration": "Om Hraam Hreem Hraum Sah Suryaya Namah",
        "vedic_mantra": "ॐ आ कृष्णेन रजसा वर्तमानो निवेशयन्नमृतं मर्त्यं च",
        "gayatri": "ॐ भास्कराय विद्महे महाद्युतिकराय धीमहि तन्नो आदित्यः प्रचोदयात्",
        "jaap_count": 7000,
        "best_day": "रविवार / Sunday"
    },
    "MOON": {
        "beej_mantra": "ॐ श्रां श्रीं श्रौं सः चन्द्राय नमः",
        "beej_transliteration": "Om Shraam Shreem Shraum Sah Chandraya Namah",
        "vedic_mantra": "ॐ इमं देवा असपत्नं सुवध्वं महते क्षत्राय महते ज्यैष्ठ्याय",
        "gayatri": "ॐ क्षीरपुत्राय विद्महे अमृततत्त्वाय धीमहि तन्नो चन्द्रः प्रचोदयात्",
        "jaap_count": 11000,
        "best_day": "सोमवार / Monday"
    },
    "MARS": {
        "beej_mantra": "ॐ क्रां क्रीं क्रौं सः भौमाय नमः",
        "beej_transliteration": "Om Kraam Kreem Kraum Sah Bhaumaya Namah",
        "vedic_mantra": "ॐ अग्निर्मूर्धा दिवः ककुत्पतिः पृथिव्या अयम्",
        "gayatri": "ॐ अंगारकाय विद्महे शक्तिहस्ताय धीमहि तन्नो भौमः प्रचोदयात्",
        "jaap_count": 10000,
        "best_day": "मंगलवार / Tuesday"
    },
    "MERCURY": {
        "beej_mantra": "ॐ ब्रां ब्रीं ब्रौं सः बुधाय नमः",
        "beej_transliteration": "Om Braam Breem Braum Sah Budhaya Namah",
        "vedic_mantra": "ॐ उद्बुध्यस्वाग्ने प्रति जागृहि त्वमिष्टापूर्ते सं सृजेथामयं च",
        "gayatri": "ॐ गजध्वजाय विद्महे परोक्षप्रियाय धीमहि तन्नो बुधः प्रचोदयात्",
        "jaap_count": 9000,
        "best_day": "बुधवार / Wednesday"
    },
    "JUPITER": {
        "beej_mantra": "ॐ ग्रां ग्रीं ग्रौं सः गुरवे नमः",
        "beej_transliteration": "Om Graam Greem Graum Sah Gurave Namah",
        "vedic_mantra": "ॐ बृहस्पते अति यदर्यो अर्हाद् द्युमद्विभाति क्रतुमज्जनेषु",
        "gayatri": "ॐ वृषभध्वजाय विद्महे क्रुणिहस्ताय धीमहि तन्नो गुरुः प्रचोदयात्",
        "jaap_count": 19000,
        "best_day": "गुरुवार / Thursday"
    },
    "VENUS": {
        "beej_mantra": "ॐ द्रां द्रीं द्रौं सः शुक्राय नमः",
        "beej_transliteration": "Om Draam Dreem Draum Sah Shukraya Namah",
        "vedic_mantra": "ॐ अन्नात्परिस्रुतो रसं ब्रह्मणा व्यपिबत्क्षत्रं पयः सोमं प्रजापतिः",
        "gayatri": "ॐ अश्वध्वजाय विद्महे धनुर्हस्ताय धीमहि तन्नो शुक्रः प्रचोदयात्",
        "jaap_count": 16000,
        "best_day": "शुक्रवार / Friday"
    },
    "SATURN": {
        "beej_mantra": "ॐ प्रां प्रीं प्रौं सः शनैश्चराय नमः",
        "beej_transliteration": "Om Praam Preem Praum Sah Shanaischaraya Namah",
        "vedic_mantra": "ॐ शं नो देवीरभिष्टय आपो भवन्तु पीतये",
        "gayatri": "ॐ काकध्वजाय विद्महे खड्गहस्ताय धीमहि तन्नो मन्दः प्रचोदयात्",
        "jaap_count": 23000,
        "best_day": "शनिवार / Saturday"
    },
    "RAHU": {
        "beej_mantra": "ॐ भ्रां भ्रीं भ्रौं सः राहवे नमः",
        "beej_transliteration": "Om Bhraam Bhreem Bhraum Sah Rahave Namah",
        "vedic_mantra": "ॐ कयानश्चित्र आ भुवदूती सदावृधः सखा",
        "gayatri": "ॐ नागध्वजाय विद्महे पद्महस्ताय धीमहि तन्नो राहुः प्रचोदयात्",
        "jaap_count": 18000,
        "best_day": "शनिवार / Saturday"
    },
    "KETU": {
        "beej_mantra": "ॐ स्रां स्रीं स्रौं सः केतवे नमः",
        "beej_transliteration": "Om Sraam Sreem Sraum Sah Ketave Namah",
        "vedic_mantra": "ॐ केतुं कृण्वन्नकेतवे पेशो मर्या अपेशसे",
        "gayatri": "ॐ अश्वध्वजाय विद्महे शूलहस्ताय धीमहि तन्नो केतुः प्रचोदयात्",
        "jaap_count": 17000,
        "best_day": "मंगलवार / Tuesday"
    }
}

# Planet gemstones from Ratna Shastra
PLANET_GEMSTONES = {
    "SUN": {
        "primary": "माणिक्य / Ruby (Manikya)",
        "substitute": ["गार्नेट / Garnet", "लाल स्पिनेल / Red Spinel"],
        "weight": "3-6 carats",
        "metal": "सोना / Gold",
        "finger": "अनामिका / Ring finger",
        "day": "रविवार सुबह / Sunday morning"
    },
    "MOON": {
        "primary": "मोती / Pearl (Moti)",
        "substitute": ["मूनस्टोन / Moonstone", "सफेद मूंगा / White Coral"],
        "weight": "4-6 carats",
        "metal": "चांदी / Silver",
        "finger": "कनिष्ठा / Little finger",
        "day": "सोमवार शाम / Monday evening"
    },
    "MARS": {
        "primary": "मूंगा / Red Coral (Moonga)",
        "substitute": ["कार्नेलियन / Carnelian"],
        "weight": "6-9 carats",
        "metal": "सोना/तांबा / Gold/Copper",
        "finger": "अनामिका / Ring finger",
        "day": "मंगलवार सुबह / Tuesday morning"
    },
    "MERCURY": {
        "primary": "पन्ना / Emerald (Panna)",
        "substitute": ["पेरीडॉट / Peridot", "हरा टूरमालाइन / Green Tourmaline"],
        "weight": "3-6 carats",
        "metal": "सोना / Gold",
        "finger": "कनिष्ठा / Little finger",
        "day": "बुधवार सुबह / Wednesday morning"
    },
    "JUPITER": {
        "primary": "पुखराज / Yellow Sapphire (Pukhraj)",
        "substitute": ["सिट्रीन / Citrine", "पीला पुखराज / Yellow Topaz"],
        "weight": "3-5 carats",
        "metal": "सोना / Gold",
        "finger": "तर्जनी / Index finger",
        "day": "गुरुवार सुबह / Thursday morning"
    },
    "VENUS": {
        "primary": "हीरा / Diamond (Heera)",
        "substitute": ["सफेद जिरकॉन / White Zircon", "सफेद नीलम / White Sapphire"],
        "weight": "1-2 carats",
        "metal": "प्लैटिनम/सोना / Platinum/Gold",
        "finger": "मध्यमा / Middle finger",
        "day": "शुक्रवार सुबह / Friday morning"
    },
    "SATURN": {
        "primary": "नीलम / Blue Sapphire (Neelam)",
        "substitute": ["नीला टोपाज / Blue Topaz", "अमेथिस्ट / Amethyst"],
        "weight": "4-7 carats",
        "metal": "पंचधातु/लोहा / Panchdhatu/Iron",
        "finger": "मध्यमा / Middle finger",
        "day": "शनिवार शाम / Saturday evening"
    },
    "RAHU": {
        "primary": "गोमेद / Hessonite (Gomed)",
        "substitute": ["स्पेसर्टाइट गार्नेट / Spessartite Garnet"],
        "weight": "5-7 carats",
        "metal": "अष्टधातु / Ashtadhatu",
        "finger": "मध्यमा / Middle finger",
        "day": "शनिवार शाम / Saturday evening"
    },
    "KETU": {
        "primary": "लहसुनिया / Cat's Eye (Lehsuniya)",
        "substitute": ["टाइगर आई / Tiger Eye"],
        "weight": "4-6 carats",
        "metal": "पंचधातु / Panchdhatu",
        "finger": "मध्यमा / Middle finger",
        "day": "मंगलवार शाम / Tuesday evening"
    }
}

# Charity items for planets (Daan)
PLANET_CHARITY = {
    "SUN": {
        "items": ["गेहूं / Wheat", "गुड़ / Jaggery", "तांबा / Copper", "लाल वस्त्र / Red cloth"],
        "recipient": "ब्राह्मण, पिता तुल्य / Brahmin, father figures",
        "day": "रविवार / Sunday",
        "time": "सूर्योदय के समय / At sunrise"
    },
    "MOON": {
        "items": ["चावल / Rice", "दूध / Milk", "चांदी / Silver", "सफेद वस्त्र / White cloth"],
        "recipient": "महिलाएं, माता तुल्य / Women, mother figures",
        "day": "सोमवार / Monday",
        "time": "शाम को / Evening"
    },
    "MARS": {
        "items": ["मसूर दाल / Masoor dal", "लाल वस्त्र / Red cloth", "तांबा / Copper", "गुड़ / Jaggery"],
        "recipient": "युवक, भाई तुल्य / Young men, brother figures",
        "day": "मंगलवार / Tuesday",
        "time": "दोपहर से पहले / Before noon"
    },
    "MERCURY": {
        "items": ["मूंग दाल / Moong dal", "हरी सब्जियां / Green vegetables", "कापड़ा / Cloth"],
        "recipient": "विद्यार्थी, बुआ/मामा / Students, aunt/uncle",
        "day": "बुधवार / Wednesday",
        "time": "सुबह / Morning"
    },
    "JUPITER": {
        "items": ["चना दाल / Chana dal", "हल्दी / Turmeric", "पीला वस्त्र / Yellow cloth", "केला / Banana"],
        "recipient": "गुरु, ब्राह्मण / Guru, Brahmin",
        "day": "गुरुवार / Thursday",
        "time": "सूर्योदय के समय / At sunrise"
    },
    "VENUS": {
        "items": ["चीनी / Sugar", "सफेद वस्त्र / White cloth", "चावल / Rice", "इत्र / Perfume"],
        "recipient": "महिलाएं / Women",
        "day": "शुक्रवार / Friday",
        "time": "सुबह / Morning"
    },
    "SATURN": {
        "items": ["उड़द दाल / Urad dal", "काला तिल / Black sesame", "सरसों का तेल / Mustard oil", "काला कंबल / Black blanket"],
        "recipient": "गरीब, मजदूर / Poor, laborers",
        "day": "शनिवार / Saturday",
        "time": "शाम को / Evening"
    },
    "RAHU": {
        "items": ["सरसों / Mustard", "नीला वस्त्र / Blue cloth", "नारियल / Coconut"],
        "recipient": "अनाथ, विधवा / Orphans, widows",
        "day": "शनिवार / Saturday",
        "time": "शाम को / Evening"
    },
    "KETU": {
        "items": ["तिल / Sesame", "सात अनाज / Seven grains", "कंबल / Blanket"],
        "recipient": "साधु, भिखारी / Sadhus, beggars",
        "day": "मंगलवार / Tuesday",
        "time": "शाम को / Evening"
    }
}

# Dosha-specific remedies
DOSHA_REMEDIES = {
    "MANGLIK": {
        "name_hindi": "मांगलिक दोष उपाय",
        "mantras": [
            "ॐ क्रां क्रीं क्रौं सः भौमाय नमः - 108 बार मंगलवार को",
            "हनुमान चालीसा पाठ - मंगलवार और शनिवार"
        ],
        "temples": [
            "हनुमान मंदिर जाएं / Visit Hanuman temple",
            "मंगल ग्रह मंदिर - वैथीश्वरनकोविल, तमिलनाडु / Mangal Graha temple"
        ],
        "rituals": [
            "मंगल शांति पूजा करवाएं / Perform Mangal Shanti Puja",
            "कुंभ विवाह (केला/पीपल से) / Kumbh Vivah (marriage with banana/peepal)"
        ],
        "charity": [
            "मंगलवार को लाल वस्तुओं का दान / Donate red items on Tuesday",
            "मसूर दाल, गुड़ का दान / Donate masoor dal and jaggery"
        ],
        "lifestyle": [
            "मंगलवार को व्रत रखें / Fast on Tuesday",
            "लाल वस्त्र धारण करें / Wear red clothes",
            "मूंगा रत्न धारण करें / Wear coral gemstone"
        ]
    },
    "KAAL_SARP": {
        "name_hindi": "काल सर्प दोष उपाय",
        "mantras": [
            "महा मृत्युंजय मंत्र - 1.25 लाख जाप",
            "ॐ नमः शिवाय - प्रतिदिन 108 बार"
        ],
        "temples": [
            "त्र्यंबकेश्वर मंदिर, नासिक / Trimbakeshwar, Nashik",
            "महाकालेश्वर मंदिर, उज्जैन / Mahakaleshwar, Ujjain",
            "रामेश्वरम / Rameshwaram"
        ],
        "rituals": [
            "काल सर्प शांति पूजा / Kaal Sarp Shanti Puja",
            "नाग पंचमी पूजा / Nag Panchami Puja",
            "रुद्राभिषेक / Rudrabhishek"
        ],
        "charity": [
            "सांपों को दूध चढ़ाएं (मूर्ति पर) / Offer milk to snake idols",
            "काले तिल का दान / Donate black sesame"
        ],
        "lifestyle": [
            "श्रावण मास में शिव पूजा / Shiva worship in Shravan",
            "नाग पंचमी पर व्रत / Fast on Nag Panchami"
        ]
    },
    "PITRA": {
        "name_hindi": "पितृ दोष उपाय",
        "mantras": [
            "पितृ गायत्री मंत्र - ॐ पितृगणाय विद्महे...",
            "ॐ पितृभ्यो नमः - 108 बार"
        ],
        "temples": [
            "गया, बिहार में पिंड दान / Pind Daan at Gaya",
            "त्रयंबकेश्वर / Trimbakeshwar",
            "बद्रीनाथ / Badrinath"
        ],
        "rituals": [
            "पितृ पक्ष में श्राद्ध / Shradh during Pitru Paksha",
            "तर्पण करें / Perform Tarpan",
            "पिंड दान करें / Perform Pind Daan"
        ],
        "charity": [
            "ब्राह्मण भोजन / Feed Brahmins",
            "गौ दान / Donate cow",
            "अमावस्या पर दान / Charity on Amavasya"
        ],
        "lifestyle": [
            "पितृ पक्ष में मांस-मदिरा त्यागें / Avoid meat-alcohol in Pitru Paksha",
            "पूर्वजों का नाम याद रखें / Remember ancestors' names"
        ]
    },
    "SADE_SATI": {
        "name_hindi": "साढ़े साती उपाय",
        "mantras": [
            "शनि बीज मंत्र - ॐ प्रां प्रीं प्रौं सः शनैश्चराय नमः",
            "शनि चालीसा - शनिवार को",
            "हनुमान चालीसा - शनिवार को"
        ],
        "temples": [
            "शनि शिंगणापुर, महाराष्ट्र / Shani Shingnapur",
            "शनि देव मंदिर, तिरुनलार / Thirunallar"
        ],
        "rituals": [
            "शनि शांति पूजा / Shani Shanti Puja",
            "तैल अभिषेक शनिवार को / Oil Abhishek on Saturday"
        ],
        "charity": [
            "शनिवार को काली वस्तुएं दान / Donate black items on Saturday",
            "अंधों-विकलांगों की सेवा / Serve blind and disabled"
        ],
        "lifestyle": [
            "शनिवार व्रत / Saturday fasting",
            "नीलम या लोहे की अंगूठी / Blue sapphire or iron ring",
            "पीपल पूजा / Worship Peepal tree"
        ]
    },
    "GURU_CHANDAL": {
        "name_hindi": "गुरु चांडाल दोष उपाय",
        "mantras": [
            "गुरु बीज मंत्र - ॐ ग्रां ग्रीं ग्रौं सः गुरवे नमः",
            "विष्णु सहस्रनाम पाठ"
        ],
        "temples": [
            "बृहस्पति मंदिर / Jupiter temple",
            "विष्णु मंदिर / Vishnu temple"
        ],
        "rituals": [
            "गुरु ग्रह शांति पूजा / Guru Graha Shanti",
            "सत्यनारायण कथा / Satyanarayan Katha"
        ],
        "charity": [
            "गुरुवार को पीली वस्तुएं दान / Yellow items on Thursday",
            "गुरु (शिक्षक) की सेवा / Serve teachers"
        ],
        "lifestyle": [
            "गुरुवार व्रत / Thursday fasting",
            "पुखराज धारण / Wear Yellow Sapphire"
        ]
    }
}

# House-specific remedies
HOUSE_REMEDIES = {
    1: {
        "name": "लग्न भाव / 1st House (Self)",
        "issues": "आत्मविश्वास, स्वास्थ्य / Confidence, health",
        "remedies": [
            "सूर्य को जल चढ़ाएं प्रतिदिन / Offer water to Sun daily",
            "माणिक्य धारण / Wear Ruby",
            "सूर्य नमस्कार करें / Do Surya Namaskar"
        ]
    },
    2: {
        "name": "धन भाव / 2nd House (Wealth)",
        "issues": "धन, वाणी, परिवार / Wealth, speech, family",
        "remedies": [
            "लक्ष्मी पूजा शुक्रवार को / Lakshmi Puja on Friday",
            "हरे रंग की वस्तुएं दान / Donate green items",
            "ॐ श्रीं नमः का जाप / Chant Om Shreem Namah"
        ]
    },
    3: {
        "name": "सहज भाव / 3rd House (Courage)",
        "issues": "साहस, भाई-बहन / Courage, siblings",
        "remedies": [
            "मंगलवार को हनुमान पूजा / Hanuman worship on Tuesday",
            "मूंगा धारण / Wear Coral",
            "भाई-बहनों की सेवा / Serve siblings"
        ]
    },
    4: {
        "name": "सुख भाव / 4th House (Happiness)",
        "issues": "माता, गृह सुख / Mother, domestic happiness",
        "remedies": [
            "सोमवार को चांदी दान / Donate silver on Monday",
            "माता की सेवा / Serve mother",
            "मोती धारण / Wear Pearl"
        ]
    },
    5: {
        "name": "पुत्र भाव / 5th House (Children)",
        "issues": "संतान, बुद्धि / Children, intelligence",
        "remedies": [
            "गुरुवार को पीला दान / Yellow donations on Thursday",
            "संतान गोपाल मंत्र जाप / Santan Gopal Mantra",
            "विष्णु पूजा / Vishnu worship"
        ]
    },
    6: {
        "name": "रोग भाव / 6th House (Health)",
        "issues": "रोग, शत्रु, ऋण / Disease, enemies, debt",
        "remedies": [
            "दुर्गा पूजा / Durga worship",
            "हनुमान चालीसा पाठ / Hanuman Chalisa",
            "गरीबों को भोजन / Feed the poor"
        ]
    },
    7: {
        "name": "दाम्पत्य भाव / 7th House (Marriage)",
        "issues": "विवाह, साझेदारी / Marriage, partnership",
        "remedies": [
            "शुक्रवार को श्वेत वस्त्र दान / White cloth on Friday",
            "राधा-कृष्ण पूजा / Radha-Krishna worship",
            "हीरा/सफेद जिरकॉन धारण / Wear Diamond/White Zircon"
        ]
    },
    8: {
        "name": "आयु भाव / 8th House (Longevity)",
        "issues": "आयु, रहस्य, विरासत / Longevity, secrets, inheritance",
        "remedies": [
            "महा मृत्युंजय मंत्र जाप / Maha Mrityunjaya Mantra",
            "शनिवार को काला दान / Black donations on Saturday",
            "शिव पूजा / Shiva worship"
        ]
    },
    9: {
        "name": "भाग्य भाव / 9th House (Fortune)",
        "issues": "भाग्य, पिता, धर्म / Fortune, father, dharma",
        "remedies": [
            "गुरुवार व्रत / Thursday fasting",
            "पुखराज धारण / Wear Yellow Sapphire",
            "पिता की सेवा / Serve father"
        ]
    },
    10: {
        "name": "कर्म भाव / 10th House (Career)",
        "issues": "करियर, प्रतिष्ठा / Career, reputation",
        "remedies": [
            "रविवार को लाल दान / Red donations on Sunday",
            "सूर्य बीज मंत्र / Sun Beej Mantra",
            "माणिक्य धारण / Wear Ruby"
        ]
    },
    11: {
        "name": "लाभ भाव / 11th House (Gains)",
        "issues": "लाभ, आय, मित्र / Gains, income, friends",
        "remedies": [
            "शुक्रवार को मिठाई दान / Sweets on Friday",
            "गणेश पूजा / Ganesh worship",
            "पुखराज धारण / Wear Yellow Sapphire"
        ]
    },
    12: {
        "name": "व्यय भाव / 12th House (Expenses)",
        "issues": "खर्च, मोक्ष, विदेश / Expenses, moksha, foreign",
        "remedies": [
            "शनिवार को तेल दान / Oil donation on Saturday",
            "विष्णु सहस्रनाम / Vishnu Sahasranama",
            "गोमेद धारण / Wear Hessonite"
        ]
    }
}

# Lal Kitab remedies (practical everyday remedies)
LAL_KITAB_REMEDIES = {
    "SUN_WEAK": [
        "तांबे के गिलास में पानी पिएं / Drink water from copper glass",
        "गुड़ खाएं / Eat jaggery",
        "सूर्य को जल अर्पित करें / Offer water to Sun",
        "पिता की सेवा करें / Serve your father"
    ],
    "MOON_WEAK": [
        "चांदी का छल्ला पहनें / Wear silver ring",
        "दूध पिएं / Drink milk",
        "माता की सेवा करें / Serve mother",
        "सोमवार को सफेद वस्त्र धारण / White clothes on Monday"
    ],
    "MARS_WEAK": [
        "मीठा खाएं / Eat sweets",
        "भाइयों से अच्छे संबंध / Good relations with brothers",
        "लाल रुमाल रखें / Keep red handkerchief",
        "शहद का सेवन / Consume honey"
    ],
    "MERCURY_WEAK": [
        "नाक छिदवाएं (महिलाएं) / Nose piercing (women)",
        "हरी सब्जियां खाएं / Eat green vegetables",
        "तोते को दाना खिलाएं / Feed parrots",
        "दांत साफ रखें / Keep teeth clean"
    ],
    "JUPITER_WEAK": [
        "केसर का तिलक / Saffron tilak",
        "पीले वस्त्र गुरुवार को / Yellow clothes on Thursday",
        "गुरु का सम्मान / Respect teachers",
        "मंदिर जाएं / Visit temples"
    ],
    "VENUS_WEAK": [
        "इत्र लगाएं / Use perfume",
        "गाय को चारा / Feed cow",
        "पत्नी का सम्मान / Respect wife",
        "सफेद वस्त्र धारण / Wear white clothes"
    ],
    "SATURN_WEAK": [
        "कौवों को रोटी / Feed crows",
        "सरसों का तेल दान / Donate mustard oil",
        "लोहे की वस्तु दान / Donate iron items",
        "बुजुर्गों की सेवा / Serve elderly"
    ],
    "RAHU_WEAK": [
        "प्याज-लहसुन त्यागें / Avoid onion-garlic",
        "इलेक्ट्रिक उपकरण दान / Donate electrical items",
        "सरसों के बीज बहते पानी में / Mustard seeds in flowing water",
        "नीला रंग पहनें / Wear blue color"
    ],
    "KETU_WEAK": [
        "कुत्ते को रोटी / Feed dogs",
        "भगवान गणेश की पूजा / Worship Lord Ganesha",
        "बादाम दान / Donate almonds",
        "ध्यान करें / Meditate"
    ]
}


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class RemedyItem:
    """Single remedy item"""
    category: str  # mantra, gemstone, charity, ritual, lifestyle
    description: str
    description_hindi: str
    timing: str = ""
    duration: str = ""
    important_notes: List[str] = field(default_factory=list)


@dataclass
class PlanetRemedies:
    """Remedies for a specific planet"""
    planet: str
    planet_hindi: str
    is_weak: bool
    is_afflicted: bool
    mantras: List[Dict[str, str]]
    gemstone: Dict[str, Any]
    charity: Dict[str, Any]
    lal_kitab: List[str]
    general_tips: List[str]


@dataclass
class DoshaRemedyPlan:
    """Remedies for a specific dosha"""
    dosha_name: str
    dosha_name_hindi: str
    severity: str  # Mild, Moderate, Severe
    mantras: List[str]
    temples: List[str]
    rituals: List[str]
    charity: List[str]
    lifestyle: List[str]
    timeline: str


@dataclass
class ComprehensiveRemedyReport:
    """Complete remedy report"""
    planet_remedies: List[PlanetRemedies]
    dosha_remedies: List[DoshaRemedyPlan]
    house_remedies: List[Dict[str, Any]]
    priority_remedies: List[str]
    priority_remedies_hindi: List[str]
    daily_routine: List[str]
    weekly_routine: List[str]
    monthly_routine: List[str]
    yearly_routine: List[str]


# =============================================================================
# REMEDY ANALYZER
# =============================================================================

class RemedyAnalyzer:
    """
    Comprehensive Vedic remedy system based on authentic texts.

    Analyzes Kundali and provides personalized remedies.
    """

    PLANET_NAMES_HINDI = {
        "SUN": "सूर्य", "MOON": "चंद्र", "MARS": "मंगल",
        "MERCURY": "बुध", "JUPITER": "गुरु", "VENUS": "शुक्र",
        "SATURN": "शनि", "RAHU": "राहु", "KETU": "केतु"
    }

    def __init__(self, kundali_data: Dict[str, Any], doshas: Optional[Dict[str, Any]] = None):
        """
        Initialize remedy analyzer.

        Args:
            kundali_data: Kundali dictionary with planet positions
            doshas: Optional pre-analyzed dosha results
        """
        self.kundali = kundali_data
        self.planets = kundali_data.get("planets", {})
        self.doshas = doshas or {}
        self.lagna_num = self._get_lagna_num()

    def _get_lagna_num(self) -> int:
        """Get lagna rashi number"""
        lagna = self.kundali.get("lagna", {})
        return lagna.get("rashi_num", 0)

    def _is_planet_weak(self, planet: str) -> bool:
        """Check if planet is weak based on various factors"""
        planet_data = self.planets.get(planet, {})

        # Debilitated
        if planet_data.get("is_debilitated", False):
            return True

        # In enemy sign
        if planet_data.get("dignity", "") == "Enemy":
            return True

        # Retrograde (considered weak for benefics)
        if planet_data.get("is_retrograde", False) and planet in ["JUPITER", "VENUS", "MERCURY"]:
            return True

        # Combust
        if planet_data.get("is_combust", False):
            return True

        return False

    def _is_planet_afflicted(self, planet: str) -> bool:
        """Check if planet is afflicted by malefics"""
        planet_data = self.planets.get(planet, {})

        # Conjunct with malefics
        conjuncts = planet_data.get("conjuncts", [])
        malefics = ["SATURN", "MARS", "RAHU", "KETU"]
        if any(m in conjuncts for m in malefics):
            return True

        # Aspected by malefics
        aspects = planet_data.get("aspected_by", [])
        if any(m in aspects for m in malefics):
            return True

        return False

    def get_planet_remedies(self, planet: str) -> PlanetRemedies:
        """Get remedies for a specific planet"""

        is_weak = self._is_planet_weak(planet)
        is_afflicted = self._is_planet_afflicted(planet)

        mantra_data = PLANET_MANTRAS.get(planet, {})
        gem_data = PLANET_GEMSTONES.get(planet, {})
        charity_data = PLANET_CHARITY.get(planet, {})

        # Get Lal Kitab remedies if weak
        lal_kitab = []
        if is_weak or is_afflicted:
            lal_kitab = LAL_KITAB_REMEDIES.get(f"{planet}_WEAK", [])

        # General tips based on planet
        general_tips = []
        if planet == "SUN":
            general_tips = [
                "सुबह जल्दी उठें / Wake up early",
                "सूर्योदय देखें / Watch sunrise",
                "आत्मविश्वास बढ़ाएं / Build confidence"
            ]
        elif planet == "MOON":
            general_tips = [
                "मन शांत रखें / Keep mind calm",
                "पानी अधिक पिएं / Drink more water",
                "माता का सम्मान करें / Respect mother"
            ]
        elif planet == "JUPITER":
            general_tips = [
                "ज्ञान अर्जित करें / Acquire knowledge",
                "धर्म का पालन करें / Follow dharma",
                "गुरुओं का सम्मान / Respect teachers"
            ]

        return PlanetRemedies(
            planet=planet,
            planet_hindi=self.PLANET_NAMES_HINDI.get(planet, planet),
            is_weak=is_weak,
            is_afflicted=is_afflicted,
            mantras=[{
                "type": "Beej Mantra",
                "text": mantra_data.get("beej_mantra", ""),
                "transliteration": mantra_data.get("beej_transliteration", ""),
                "jaap_count": mantra_data.get("jaap_count", 108),
                "best_day": mantra_data.get("best_day", "")
            }],
            gemstone=gem_data,
            charity=charity_data,
            lal_kitab=lal_kitab,
            general_tips=general_tips
        )

    def get_dosha_remedies(self, dosha_type: str) -> Optional[DoshaRemedyPlan]:
        """Get remedies for a specific dosha"""

        remedy_data = DOSHA_REMEDIES.get(dosha_type.upper())
        if not remedy_data:
            return None

        # Determine severity from dosha analysis
        dosha_info = self.doshas.get(dosha_type.lower(), {})
        severity = dosha_info.get("severity", "Moderate")

        # Timeline based on severity
        timeline = "3-6 महीने / 3-6 months"
        if severity == "Severe":
            timeline = "1-2 साल / 1-2 years"
        elif severity == "Mild":
            timeline = "1-3 महीने / 1-3 months"

        return DoshaRemedyPlan(
            dosha_name=dosha_type,
            dosha_name_hindi=remedy_data.get("name_hindi", dosha_type),
            severity=severity,
            mantras=remedy_data.get("mantras", []),
            temples=remedy_data.get("temples", []),
            rituals=remedy_data.get("rituals", []),
            charity=remedy_data.get("charity", []),
            lifestyle=remedy_data.get("lifestyle", []),
            timeline=timeline
        )

    def get_house_remedies(self, house_num: int) -> Dict[str, Any]:
        """Get remedies for a specific house"""
        return HOUSE_REMEDIES.get(house_num, {})

    def get_comprehensive_report(self) -> ComprehensiveRemedyReport:
        """Generate comprehensive remedy report"""

        # Analyze all planets
        planet_remedies = []
        weak_planets = []

        for planet in ["SUN", "MOON", "MARS", "MERCURY", "JUPITER", "VENUS", "SATURN", "RAHU", "KETU"]:
            remedy = self.get_planet_remedies(planet)
            if remedy.is_weak or remedy.is_afflicted:
                planet_remedies.append(remedy)
                weak_planets.append(planet)

        # Analyze doshas
        dosha_remedies = []
        dosha_types = ["MANGLIK", "KAAL_SARP", "PITRA", "SADE_SATI", "GURU_CHANDAL"]

        for dosha in dosha_types:
            if self.doshas.get(dosha.lower(), {}).get("is_present", False):
                remedy = self.get_dosha_remedies(dosha)
                if remedy:
                    dosha_remedies.append(remedy)

        # House-based remedies (focus on problematic houses)
        house_remedies = []
        problem_houses = [6, 8, 12]  # Dusthana houses

        for house in problem_houses:
            house_remedy = self.get_house_remedies(house)
            if house_remedy:
                house_remedies.append(house_remedy)

        # Priority remedies
        priority = []
        priority_hindi = []

        if dosha_remedies:
            priority.append(f"Address {dosha_remedies[0].dosha_name} dosha first")
            priority_hindi.append(f"पहले {dosha_remedies[0].dosha_name_hindi} का उपाय करें")

        if weak_planets:
            priority.append(f"Strengthen {weak_planets[0]} through mantras and charity")
            priority_hindi.append(f"{self.PLANET_NAMES_HINDI[weak_planets[0]]} को मंत्र और दान से मजबूत करें")

        # Daily routine suggestions
        daily = [
            "सूर्योदय से पहले उठें / Wake before sunrise",
            "सूर्य को जल अर्पित करें / Offer water to Sun",
            "इष्ट देव का स्मरण / Remember your deity",
            "ध्यान करें 10 मिनट / Meditate 10 minutes"
        ]

        # Weekly routine
        weekly = [
            "रविवार: सूर्य पूजा / Sunday: Sun worship",
            "सोमवार: शिव पूजा / Monday: Shiva worship",
            "मंगलवार: हनुमान पूजा / Tuesday: Hanuman worship",
            "गुरुवार: गुरु पूजा, पीला दान / Thursday: Guru puja, yellow charity",
            "शुक्रवार: लक्ष्मी पूजा / Friday: Lakshmi worship",
            "शनिवार: शनि पूजा, काला दान / Saturday: Shani puja, black charity"
        ]

        # Monthly routine
        monthly = [
            "अमावस्या: पितृ तर्पण / Amavasya: Pitru Tarpan",
            "पूर्णिमा: सत्यनारायण कथा / Purnima: Satyanarayan Katha",
            "एकादशी: व्रत / Ekadashi: Fasting",
            "संक्रांति: दान / Sankranti: Charity"
        ]

        # Yearly routine
        yearly = [
            "जन्मदिन पर पूजा / Puja on birthday",
            "नवरात्रि में दुर्गा पूजा / Durga puja in Navratri",
            "श्रावण में शिव पूजा / Shiva puja in Shravan",
            "पितृ पक्ष में श्राद्ध / Shradh in Pitru Paksha"
        ]

        return ComprehensiveRemedyReport(
            planet_remedies=planet_remedies,
            dosha_remedies=dosha_remedies,
            house_remedies=house_remedies,
            priority_remedies=priority,
            priority_remedies_hindi=priority_hindi,
            daily_routine=daily,
            weekly_routine=weekly,
            monthly_routine=monthly,
            yearly_routine=yearly
        )


# =============================================================================
# CONVENIENCE FUNCTION
# =============================================================================

def get_remedies(kundali_data: Dict[str, Any], doshas: Optional[Dict[str, Any]] = None) -> ComprehensiveRemedyReport:
    """
    Convenience function to get comprehensive remedies.

    Args:
        kundali_data: Kundali dictionary
        doshas: Optional dosha analysis results

    Returns:
        ComprehensiveRemedyReport object
    """
    analyzer = RemedyAnalyzer(kundali_data, doshas)
    return analyzer.get_comprehensive_report()
