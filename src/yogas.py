"""
Vedic Yoga Detection Module
Detects various yogas from kundali
"""

from .config import (
    RASHIS, PLANET_DIGNITIES, HOUSE_LORDSHIPS,
    KENDRA_HOUSES, TRIKONA_HOUSES, DUSTHANA_HOUSES
)


def get_planet_house(planets_in_houses, planet):
    """Get house number where a planet is placed."""
    for house, planet_list in planets_in_houses.items():
        if planet in planet_list:
            return house
    return 0


def is_in_kendra(house):
    """Check if house is a Kendra (1, 4, 7, 10)."""
    return house in KENDRA_HOUSES


def is_planet_in_own_or_exalted(planet, rashi):
    """Check if planet is in own sign or exalted."""
    dignity = PLANET_DIGNITIES.get(planet, {})
    own_signs = dignity.get("own", [])
    exalted = dignity.get("exalted", "")
    return rashi in own_signs or rashi == exalted


# ============ PANCH MAHAPURUSHA YOGAS ============

def check_hamsa_yoga(planets, planets_in_houses):
    """
    Hamsa Yoga: Jupiter in Kendra in own sign (Dhanu, Meena) or exalted (Karka)
    Results: Wisdom, spirituality, respected, long life
    """
    jupiter = planets.get('JUPITER', {})
    jupiter_house = get_planet_house(planets_in_houses, 'JUPITER')
    jupiter_rashi = jupiter.get('rashi', '')

    if is_in_kendra(jupiter_house) and jupiter_rashi in ['Dhanu', 'Meena', 'Karka']:
        return {
            "present": True,
            "name": "हंस योग (Hamsa Yoga)",
            "planet": "Jupiter",
            "description": "गुरु केंद्र में स्वराशि/उच्च में। ज्ञान, आध्यात्मिकता, सम्मान, दीर्घायु।",
            "effects": "विद्वान, धार्मिक, राजकीय सम्मान, सुखी जीवन।"
        }
    return {"present": False}


def check_malavya_yoga(planets, planets_in_houses):
    """
    Malavya Yoga: Venus in Kendra in own sign (Vrishabha, Tula) or exalted (Meena)
    Results: Beauty, luxury, artistic, happy marriage
    """
    venus = planets.get('VENUS', {})
    venus_house = get_planet_house(planets_in_houses, 'VENUS')
    venus_rashi = venus.get('rashi', '')

    if is_in_kendra(venus_house) and venus_rashi in ['Vrishabha', 'Tula', 'Meena']:
        return {
            "present": True,
            "name": "मालव्य योग (Malavya Yoga)",
            "planet": "Venus",
            "description": "शुक्र केंद्र में स्वराशि/उच्च में। सौंदर्य, विलासिता, कला, सुखी विवाह।",
            "effects": "आकर्षक व्यक्तित्व, धनवान, कलाप्रेमी, वाहन सुख।"
        }
    return {"present": False}


def check_ruchaka_yoga(planets, planets_in_houses):
    """
    Ruchaka Yoga: Mars in Kendra in own sign (Mesha, Vrishchika) or exalted (Makara)
    Results: Courage, leadership, military success
    """
    mars = planets.get('MARS', {})
    mars_house = get_planet_house(planets_in_houses, 'MARS')
    mars_rashi = mars.get('rashi', '')

    if is_in_kendra(mars_house) and mars_rashi in ['Mesha', 'Vrishchika', 'Makara']:
        return {
            "present": True,
            "name": "रुचक योग (Ruchaka Yoga)",
            "planet": "Mars",
            "description": "मंगल केंद्र में स्वराशि/उच्च में। साहस, नेतृत्व, सैन्य सफलता।",
            "effects": "वीर, साहसी, भूमि लाभ, शत्रु विजय।"
        }
    return {"present": False}


def check_bhadra_yoga(planets, planets_in_houses):
    """
    Bhadra Yoga: Mercury in Kendra in own sign (Mithuna, Kanya)
    Results: Intelligence, communication skills, business success
    """
    mercury = planets.get('MERCURY', {})
    mercury_house = get_planet_house(planets_in_houses, 'MERCURY')
    mercury_rashi = mercury.get('rashi', '')

    if is_in_kendra(mercury_house) and mercury_rashi in ['Mithuna', 'Kanya']:
        return {
            "present": True,
            "name": "भद्र योग (Bhadra Yoga)",
            "planet": "Mercury",
            "description": "बुध केंद्र में स्वराशि/उच्च में। बुद्धि, वाक्पटुता, व्यापार सफलता।",
            "effects": "विद्वान, वक्ता, गणितज्ञ, व्यापार में सफल।"
        }
    return {"present": False}


def check_shasha_yoga(planets, planets_in_houses):
    """
    Shasha Yoga: Saturn in Kendra in own sign (Makara, Kumbha) or exalted (Tula)
    Results: Authority, discipline, late but lasting success
    """
    saturn = planets.get('SATURN', {})
    saturn_house = get_planet_house(planets_in_houses, 'SATURN')
    saturn_rashi = saturn.get('rashi', '')

    if is_in_kendra(saturn_house) and saturn_rashi in ['Makara', 'Kumbha', 'Tula']:
        return {
            "present": True,
            "name": "शश योग (Shasha Yoga)",
            "planet": "Saturn",
            "description": "शनि केंद्र में स्वराशि/उच्च में। अधिकार, अनुशासन, स्थायी सफलता।",
            "effects": "नेता, न्यायप्रिय, सेवकों का स्वामी, देर से पर स्थायी सफलता।"
        }
    return {"present": False}


# ============ OTHER IMPORTANT YOGAS ============

def check_gajakesari_yoga(planets, planets_in_houses):
    """
    Gajakesari Yoga: Jupiter in Kendra (1, 4, 7, 10) from Moon
    One of the most auspicious yogas
    """
    moon_house = get_planet_house(planets_in_houses, 'MOON')
    jupiter_house = get_planet_house(planets_in_houses, 'JUPITER')

    if moon_house and jupiter_house:
        # Calculate Jupiter's position from Moon
        diff = ((jupiter_house - moon_house) % 12)
        if diff in [0, 3, 6, 9]:  # 1st, 4th, 7th, 10th from Moon
            return {
                "present": True,
                "name": "गजकेसरी योग (Gajakesari Yoga)",
                "description": "गुरु चंद्र से केंद्र में। अत्यंत शुभ योग।",
                "effects": "प्रसिद्धि, धन, बुद्धि, सम्मान, दीर्घायु। हाथी जैसी शक्ति और सिंह जैसा साहस।"
            }
    return {"present": False}


def check_budhaditya_yoga(planets, planets_in_houses):
    """
    Budhaditya Yoga: Sun and Mercury in same house
    Intelligence and communication skills
    """
    sun_house = get_planet_house(planets_in_houses, 'SUN')
    mercury_house = get_planet_house(planets_in_houses, 'MERCURY')

    if sun_house and mercury_house and sun_house == mercury_house:
        return {
            "present": True,
            "name": "बुधादित्य योग (Budhaditya Yoga)",
            "description": "सूर्य और बुध एक भाव में।",
            "effects": "बुद्धिमान, वाक्पटु, प्रसिद्ध, राजकीय सम्मान।"
        }
    return {"present": False}


def check_chandra_mangal_yoga(planets, planets_in_houses):
    """
    Chandra-Mangal Yoga: Moon and Mars conjunction
    Wealth through own efforts
    """
    moon_house = get_planet_house(planets_in_houses, 'MOON')
    mars_house = get_planet_house(planets_in_houses, 'MARS')

    if moon_house and mars_house and moon_house == mars_house:
        return {
            "present": True,
            "name": "चंद्र-मंगल योग (Chandra-Mangal Yoga)",
            "description": "चंद्र और मंगल एक भाव में।",
            "effects": "स्वयं के प्रयास से धन, व्यापार में सफलता, साहसी।"
        }
    return {"present": False}


# ============ NEGATIVE YOGAS ============

def check_kemadruma_yoga(planets, planets_in_houses):
    """
    Kemadruma Yoga: No planet in 2nd or 12th from Moon (except Sun, Rahu, Ketu)
    Indicates struggles and poverty
    """
    moon_house = get_planet_house(planets_in_houses, 'MOON')
    if not moon_house:
        return {"present": False}

    # Houses 2nd and 12th from Moon
    second_from_moon = (moon_house % 12) + 1
    twelfth_from_moon = ((moon_house - 2) % 12) + 1

    # Check if any planet (except Sun, Rahu, Ketu) is in these houses
    check_planets = ['MARS', 'MERCURY', 'JUPITER', 'VENUS', 'SATURN']

    planet_in_2nd = any(get_planet_house(planets_in_houses, p) == second_from_moon for p in check_planets)
    planet_in_12th = any(get_planet_house(planets_in_houses, p) == twelfth_from_moon for p in check_planets)

    if not planet_in_2nd and not planet_in_12th:
        # Check for cancellation (Kemadruma Bhanga)
        # If Jupiter aspects Moon (7th from Jupiter) or Moon is in Kendra, yoga is cancelled
        jupiter_house = get_planet_house(planets_in_houses, 'JUPITER')
        moon_in_kendra = is_in_kendra(moon_house)

        # Jupiter aspects 5th, 7th, 9th from its position
        jupiter_aspects_moon = False
        if jupiter_house and moon_house:
            diff = (moon_house - jupiter_house) % 12
            jupiter_aspects_moon = diff in [4, 6, 8]  # 5th, 7th, 9th aspects

        if moon_in_kendra or jupiter_aspects_moon:
            return {
                "present": True,
                "cancelled": True,
                "name": "केमद्रुम योग (निरस्त)",
                "description": "केमद्रुम योग था पर निरस्त हो गया।",
                "effects": "चंद्र केंद्र में या गुरु दृष्टि से दोष निवारण।"
            }

        return {
            "present": True,
            "cancelled": False,
            "name": "केमद्रुम योग (Kemadruma Yoga)",
            "description": "चंद्र से 2nd और 12th में कोई ग्रह नहीं।",
            "effects": "आर्थिक कठिनाई, अकेलापन, संघर्ष। उपाय आवश्यक।"
        }
    return {"present": False}


def check_shakata_yoga(planets, planets_in_houses):
    """
    Shakata Yoga: Jupiter in 6th or 8th from Moon
    Fluctuating fortunes
    """
    moon_house = get_planet_house(planets_in_houses, 'MOON')
    jupiter_house = get_planet_house(planets_in_houses, 'JUPITER')

    if moon_house and jupiter_house:
        diff = ((jupiter_house - moon_house) % 12)
        if diff in [5, 7]:  # 6th or 8th from Moon
            return {
                "present": True,
                "name": "शकट योग (Shakata Yoga)",
                "description": "गुरु चंद्र से 6th/8th में।",
                "effects": "भाग्य में उतार-चढ़ाव, अस्थिर स्थिति, कभी सुख कभी दुख।"
            }
    return {"present": False}


# ============ DHANA (WEALTH) YOGAS ============

def check_dhana_yogas(planets, lagna, planets_in_houses):
    """
    Check various wealth-giving yogas.
    """
    dhana_yogas = []
    lagna_name = lagna['rashi']

    # Multiple planets in 2nd house
    second_house_planets = planets_in_houses.get(2, [])
    if len(second_house_planets) >= 2:
        dhana_yogas.append({
            "name": "धन योग (2nd House)",
            "description": f"द्वितीय भाव में {len(second_house_planets)} ग्रह।",
            "effects": "धन संचय, परिवार में समृद्धि।"
        })

    # Multiple planets in 11th house
    eleventh_house_planets = planets_in_houses.get(11, [])
    if len(eleventh_house_planets) >= 2:
        dhana_yogas.append({
            "name": "लाभ योग (11th House)",
            "description": f"एकादश भाव में {len(eleventh_house_planets)} ग्रह।",
            "effects": "आय में वृद्धि, लाभ, इच्छा पूर्ति।"
        })

    # 2nd and 11th lord connection
    lordships = HOUSE_LORDSHIPS.get(lagna_name, {})
    for planet, houses in lordships.items():
        if 2 in houses:
            second_lord = planet
        if 11 in houses:
            eleventh_lord = planet

    # Check if 2nd and 11th lords are conjunct
    second_lord_house = get_planet_house(planets_in_houses, second_lord) if 'second_lord' in dir() else 0
    eleventh_lord_house = get_planet_house(planets_in_houses, eleventh_lord) if 'eleventh_lord' in dir() else 0

    if second_lord_house and eleventh_lord_house and second_lord_house == eleventh_lord_house:
        dhana_yogas.append({
            "name": "धन-लाभ संयोग",
            "description": "2nd और 11th भाव के स्वामी एक साथ।",
            "effects": "उत्तम धन योग, व्यापार से लाभ।"
        })

    return dhana_yogas


# ============ MAIN FUNCTION ============

def get_all_yogas(kundali):
    """
    Get all yogas present in the kundali.
    Returns categorized dictionary of yogas.
    """
    planets = kundali.planets
    lagna = kundali.lagna
    planets_in_houses = kundali.get_planets_in_houses()

    yogas = {
        "mahapurusha": [],
        "positive": [],
        "negative": [],
        "dhana": []
    }

    # Check Panch Mahapurusha Yogas
    hamsa = check_hamsa_yoga(planets, planets_in_houses)
    if hamsa.get("present"):
        yogas["mahapurusha"].append(hamsa)

    malavya = check_malavya_yoga(planets, planets_in_houses)
    if malavya.get("present"):
        yogas["mahapurusha"].append(malavya)

    ruchaka = check_ruchaka_yoga(planets, planets_in_houses)
    if ruchaka.get("present"):
        yogas["mahapurusha"].append(ruchaka)

    bhadra = check_bhadra_yoga(planets, planets_in_houses)
    if bhadra.get("present"):
        yogas["mahapurusha"].append(bhadra)

    shasha = check_shasha_yoga(planets, planets_in_houses)
    if shasha.get("present"):
        yogas["mahapurusha"].append(shasha)

    # Check other positive yogas
    gajakesari = check_gajakesari_yoga(planets, planets_in_houses)
    if gajakesari.get("present"):
        yogas["positive"].append(gajakesari)

    budhaditya = check_budhaditya_yoga(planets, planets_in_houses)
    if budhaditya.get("present"):
        yogas["positive"].append(budhaditya)

    chandra_mangal = check_chandra_mangal_yoga(planets, planets_in_houses)
    if chandra_mangal.get("present"):
        yogas["positive"].append(chandra_mangal)

    # Check negative yogas
    kemadruma = check_kemadruma_yoga(planets, planets_in_houses)
    if kemadruma.get("present") and not kemadruma.get("cancelled"):
        yogas["negative"].append(kemadruma)

    shakata = check_shakata_yoga(planets, planets_in_houses)
    if shakata.get("present"):
        yogas["negative"].append(shakata)

    # Check Dhana yogas
    dhana = check_dhana_yogas(planets, lagna, planets_in_houses)
    yogas["dhana"].extend(dhana)

    # Check for additional doshas with cancellations
    kaal_sarp = check_kaal_sarp_dosh(planets, planets_in_houses)
    if kaal_sarp["present"]:
        yogas["negative"].append(kaal_sarp)

    pitra_dosh = check_pitra_dosh(planets, planets_in_houses, lagna)
    if pitra_dosh["present"]:
        yogas["negative"].append(pitra_dosh)

    # Check for Neecha Bhanga Raja Yoga (debilitation cancellation - very auspicious!)
    neecha_bhanga = check_neecha_bhanga_raja_yoga(planets, planets_in_houses, lagna)
    if neecha_bhanga["present"]:
        yogas["positive"].append(neecha_bhanga)

    return yogas


# ============ KAAL SARP DOSH ============

def check_kaal_sarp_dosh(planets, planets_in_houses):
    """
    Kaal Sarp Dosh: All planets between Rahu and Ketu axis.
    Includes cancellation checks.
    """
    rahu_house = get_planet_house(planets_in_houses, 'RAHU')
    ketu_house = get_planet_house(planets_in_houses, 'KETU')

    if not rahu_house or not ketu_house:
        return {"present": False}

    # Get all planet houses (excluding Rahu/Ketu)
    check_planets = ['SUN', 'MOON', 'MARS', 'MERCURY', 'JUPITER', 'VENUS', 'SATURN']
    planet_houses = [get_planet_house(planets_in_houses, p) for p in check_planets]
    planet_houses = [h for h in planet_houses if h > 0]

    # Check if all planets are between Rahu and Ketu
    # Rahu-Ketu axis divides the chart into two halves
    if rahu_house < ketu_house:
        # Planets should be between rahu_house and ketu_house
        all_between = all(rahu_house <= h <= ketu_house for h in planet_houses)
        all_outside = all(h <= rahu_house or h >= ketu_house for h in planet_houses)
    else:
        # Planets should be between ketu_house and rahu_house (wrapping around)
        all_between = all(ketu_house <= h <= rahu_house for h in planet_houses)
        all_outside = all(h <= ketu_house or h >= rahu_house for h in planet_houses)

    if not (all_between or all_outside):
        return {"present": False}

    # Kaal Sarp Dosh is present - now check cancellations
    cancellations = []

    # 1. Any planet conjunct Rahu or Ketu (partial cancellation)
    rahu_planets = planets_in_houses.get(rahu_house, [])
    ketu_planets = planets_in_houses.get(ketu_house, [])
    if len(rahu_planets) > 1 or len(ketu_planets) > 1:
        cancellations.append("ग्रह राहु/केतु के साथ युत - आंशिक निवारण")

    # 2. Jupiter aspects Rahu or Ketu
    jupiter_house = get_planet_house(planets_in_houses, 'JUPITER')
    if jupiter_house:
        rahu_diff = (rahu_house - jupiter_house) % 12
        ketu_diff = (ketu_house - jupiter_house) % 12
        if rahu_diff in [4, 6, 8] or ketu_diff in [4, 6, 8]:
            cancellations.append("गुरु दृष्टि राहु/केतु पर - दोष शांत")

    # 3. Rahu/Ketu in benefic houses (3, 6, 11)
    if rahu_house in [3, 6, 11]:
        cancellations.append(f"राहु उपचय भाव {rahu_house} में - कम हानिकारक")
    if ketu_house in [3, 6, 11]:
        cancellations.append(f"केतु उपचय भाव {ketu_house} में - कम हानिकारक")

    # 4. Moon outside Rahu-Ketu axis (partial Kaal Sarp)
    moon_house = get_planet_house(planets_in_houses, 'MOON')
    # Check if Moon is near Rahu or Ketu (conjunction helps)
    if moon_house == rahu_house or moon_house == ketu_house:
        cancellations.append("चंद्र राहु/केतु के साथ - आंशिक निवारण")

    cancelled = len(cancellations) >= 2  # 2+ cancellations = mostly cancelled
    partial = len(cancellations) == 1

    if cancelled:
        return {
            "present": True,
            "cancelled": True,
            "name": "काल सर्प दोष (निरस्त)",
            "description": "सभी ग्रह राहु-केतु अक्ष में, पर दोष निरस्त।",
            "effects": "शुभ योगों से दोष का प्रभाव नगण्य।",
            "cancellations": cancellations
        }
    elif partial:
        return {
            "present": True,
            "cancelled": False,
            "partial": True,
            "name": "काल सर्प दोष (आंशिक)",
            "description": "सभी ग्रह राहु-केतु अक्ष में, आंशिक निवारण।",
            "effects": "मध्यम प्रभाव, उपाय से लाभ।",
            "cancellations": cancellations
        }
    else:
        return {
            "present": True,
            "cancelled": False,
            "name": "काल सर्प दोष (Kaal Sarp Dosh)",
            "description": "सभी ग्रह राहु-केतु अक्ष में।",
            "effects": "जीवन में बाधाएं, विलंब, अचानक समस्याएं। नाग पूजा करें।",
            "cancellations": []
        }


# ============ PITRA DOSH ============

def check_pitra_dosh(planets, planets_in_houses, lagna):
    """
    Pitra Dosh: Affliction to 9th house or Sun-Rahu/Ketu conjunction.
    Indicates issues related to ancestors/father.
    """
    sun_house = get_planet_house(planets_in_houses, 'SUN')
    rahu_house = get_planet_house(planets_in_houses, 'RAHU')
    ketu_house = get_planet_house(planets_in_houses, 'KETU')
    saturn_house = get_planet_house(planets_in_houses, 'SATURN')
    jupiter_house = get_planet_house(planets_in_houses, 'JUPITER')

    ninth_planets = planets_in_houses.get(9, [])

    pitra_dosh_present = False
    reasons = []
    cancellations = []

    # 1. Sun conjunct Rahu or Ketu
    if sun_house == rahu_house:
        pitra_dosh_present = True
        reasons.append("सूर्य-राहु युति (ग्रहण योग)")
    if sun_house == ketu_house:
        pitra_dosh_present = True
        reasons.append("सूर्य-केतु युति (पितृ दोष संकेत)")

    # 2. 9th house afflicted by Rahu, Ketu, or Saturn
    if 'RAHU' in ninth_planets:
        pitra_dosh_present = True
        reasons.append("राहु 9th भाव में")
    if 'KETU' in ninth_planets:
        pitra_dosh_present = True
        reasons.append("केतु 9th भाव में")
    if 'SATURN' in ninth_planets:
        pitra_dosh_present = True
        reasons.append("शनि 9th भाव में")

    if not pitra_dosh_present:
        return {"present": False}

    # Check cancellations
    # 1. Jupiter aspect on 9th house
    if jupiter_house:
        ninth_diff = (9 - jupiter_house) % 12
        if ninth_diff in [0, 4, 6, 8]:  # Conjunction or 5th/7th/9th aspect
            cancellations.append("गुरु दृष्टि 9th भाव पर - दोष शांत")

    # 2. Jupiter in 9th house
    if 'JUPITER' in ninth_planets:
        cancellations.append("गुरु 9th भाव में - पितृ कृपा")

    # 3. Benefics (Jupiter, Venus) in 9th house
    if 'VENUS' in ninth_planets:
        cancellations.append("शुक्र 9th भाव में - शुभ प्रभाव")

    # 4. Sun in own sign (Simha) or exalted (Mesha)
    sun_rashi = planets.get('SUN', {}).get('rashi', '')
    if sun_rashi == 'Simha':
        cancellations.append("सूर्य स्वराशि में - पितृ बल")
    elif sun_rashi == 'Mesha':
        cancellations.append("सूर्य उच्च राशि में - पितृ बल")

    cancelled = len(cancellations) >= 2

    if cancelled:
        return {
            "present": True,
            "cancelled": True,
            "name": "पितृ दोष (शांत)",
            "description": f"कारण: {', '.join(reasons)}। शुभ योगों से शांत।",
            "effects": "दोष का प्रभाव नगण्य। पितृ कृपा प्राप्त।",
            "reasons": reasons,
            "cancellations": cancellations
        }
    else:
        return {
            "present": True,
            "cancelled": False,
            "name": "पितृ दोष (Pitra Dosh)",
            "description": f"कारण: {', '.join(reasons)}",
            "effects": "पितृ ऋण, पैतृक संपत्ति में समस्या। श्राद्ध और पिंड दान करें।",
            "reasons": reasons,
            "cancellations": cancellations
        }


# ============ NEECHA BHANGA RAJA YOGA ============

def check_neecha_bhanga_raja_yoga(planets, planets_in_houses, lagna):
    """
    Neecha Bhanga Raja Yoga: Cancellation of debilitation creates Raja Yoga!
    Very powerful and auspicious yoga.
    """
    # Debilitation signs for each planet
    debilitation_signs = {
        'SUN': 'Tula', 'MOON': 'Vrishchika', 'MARS': 'Karka',
        'MERCURY': 'Meena', 'JUPITER': 'Makara', 'VENUS': 'Kanya', 'SATURN': 'Mesha'
    }

    # Exaltation signs
    exaltation_signs = {
        'SUN': 'Mesha', 'MOON': 'Vrishabha', 'MARS': 'Makara',
        'MERCURY': 'Kanya', 'JUPITER': 'Karka', 'VENUS': 'Meena', 'SATURN': 'Tula'
    }

    # Lord of each sign
    sign_lords = {
        'Mesha': 'MARS', 'Vrishabha': 'VENUS', 'Mithuna': 'MERCURY', 'Karka': 'MOON',
        'Simha': 'SUN', 'Kanya': 'MERCURY', 'Tula': 'VENUS', 'Vrishchika': 'MARS',
        'Dhanu': 'JUPITER', 'Makara': 'SATURN', 'Kumbha': 'SATURN', 'Meena': 'JUPITER'
    }

    lagna_num = lagna.get('rashi_num', 0)

    neecha_bhanga_yogas = []

    for planet, debil_sign in debilitation_signs.items():
        planet_data = planets.get(planet, {})
        planet_rashi = planet_data.get('rashi', '')
        planet_house = get_planet_house(planets_in_houses, planet)

        if planet_rashi != debil_sign:
            continue  # Planet is not debilitated

        # Planet IS debilitated - check for Neecha Bhanga
        cancellation_reasons = []

        # 1. Lord of debilitation sign in Kendra from Lagna
        debil_lord = sign_lords.get(debil_sign, '')
        debil_lord_house = get_planet_house(planets_in_houses, debil_lord)
        if is_in_kendra(debil_lord_house):
            cancellation_reasons.append(f"{debil_lord} (नीच राशि स्वामी) केंद्र में")

        # 2. Lord of exaltation sign in Kendra from Lagna
        exalt_sign = exaltation_signs.get(planet, '')
        exalt_lord = sign_lords.get(exalt_sign, '')
        exalt_lord_house = get_planet_house(planets_in_houses, exalt_lord)
        if exalt_lord and is_in_kendra(exalt_lord_house):
            cancellation_reasons.append(f"{exalt_lord} (उच्च राशि स्वामी) केंद्र में")

        # 3. Debilitated planet itself in Kendra
        if is_in_kendra(planet_house):
            cancellation_reasons.append(f"{planet} स्वयं केंद्र में")

        # 4. Debilitated planet aspected by its dispositor (sign lord)
        dispositor = sign_lords.get(planet_rashi, '')
        dispositor_house = get_planet_house(planets_in_houses, dispositor)
        if dispositor_house:
            aspect_diff = (planet_house - dispositor_house) % 12
            if aspect_diff in [0, 4, 6, 8]:  # Conjunction or major aspects
                cancellation_reasons.append(f"{dispositor} की दृष्टि {planet} पर")

        # 5. Debilitated planet conjunct exalted planet
        for other_planet, other_exalt in exaltation_signs.items():
            if other_planet != planet:
                other_data = planets.get(other_planet, {})
                other_rashi = other_data.get('rashi', '')
                other_house = get_planet_house(planets_in_houses, other_planet)
                if other_rashi == other_exalt and other_house == planet_house:
                    cancellation_reasons.append(f"उच्च {other_planet} के साथ युति")

        # If any cancellation reason exists, Neecha Bhanga Raja Yoga is formed!
        if cancellation_reasons:
            planet_hindi = {'SUN': 'सूर्य', 'MOON': 'चंद्र', 'MARS': 'मंगल', 'MERCURY': 'बुध',
                          'JUPITER': 'गुरु', 'VENUS': 'शुक्र', 'SATURN': 'शनि'}.get(planet, planet)
            neecha_bhanga_yogas.append({
                "planet": planet,
                "planet_hindi": planet_hindi,
                "reasons": cancellation_reasons
            })

    if neecha_bhanga_yogas:
        yoga_planets = [y['planet_hindi'] for y in neecha_bhanga_yogas]
        all_reasons = []
        for y in neecha_bhanga_yogas:
            all_reasons.extend(y['reasons'])

        return {
            "present": True,
            "name": "नीच भंग राज योग (Neecha Bhanga Raja Yoga)",
            "description": f"{', '.join(yoga_planets)} का नीच भंग। अत्यंत शुभ योग!",
            "effects": "नीच ग्रह राजयोग देता है! अप्रत्याशित सफलता, उच्च पद, कठिनाई से विजय।",
            "planets": neecha_bhanga_yogas,
            "reasons": all_reasons
        }

    return {"present": False}


def get_yoga_summary(yogas):
    """Get a summary string of all yogas."""
    summary = []

    if yogas["mahapurusha"]:
        summary.append(f"<b>पंच महापुरुष योग:</b> {len(yogas['mahapurusha'])} योग")
        for y in yogas["mahapurusha"]:
            summary.append(f"• {y['name']}")

    if yogas["positive"]:
        summary.append(f"<br><b>शुभ योग:</b> {len(yogas['positive'])} योग")
        for y in yogas["positive"]:
            summary.append(f"• {y['name']}")

    if yogas["dhana"]:
        summary.append(f"<br><b>धन योग:</b> {len(yogas['dhana'])} योग")
        for y in yogas["dhana"]:
            summary.append(f"• {y['name']}")

    if yogas["negative"]:
        summary.append(f"<br><b>दोष योग:</b> {len(yogas['negative'])} योग")
        for y in yogas["negative"]:
            summary.append(f"• {y['name']} (उपाय आवश्यक)")

    if not any(yogas.values()):
        summary.append("कोई विशेष योग नहीं पाया गया।")

    return "<br>".join(summary)
