# -*- coding: utf-8 -*-
"""
COMPLETE VERIFICATION: All Kundali Details for Alok Yadav
Birth: 25/10/1993, 05:15 AM, Amethi
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from datetime import datetime
from src.kundali import create_kundali
from src.config import RASHIS, PLANET_NAMES, Planet, NAKSHATRAS, BHAVA_NAMES
# from src.yogas import YogaAnalyzer  # Not available
from src.dasha import VimshottariDasha

# Create Kundali
k = create_kundali(
    name='Alok Yadav',
    year=1993, month=10, day=25,
    hour=5, minute=15,
    city='Amethi'
)

planets = k.planets
lagna = k.lagna
planets_in_houses = k.get_planets_in_houses()
houses = k.houses
mahadashas = k.get_mahadashas(years=120)
current_dasha = k.get_current_dasha()

rashi_hindi = {
    "Mesha": "मेष", "Vrishabha": "वृषभ", "Mithuna": "मिथुन", "Karka": "कर्क",
    "Simha": "सिंह", "Kanya": "कन्या", "Tula": "तुला", "Vrishchika": "वृश्चिक",
    "Dhanu": "धनु", "Makara": "मकर", "Kumbha": "कुंभ", "Meena": "मीन"
}

print("=" * 80)
print("COMPLETE KUNDALI VERIFICATION: ALOK YADAV")
print("DOB: 25/10/1993, TOB: 05:15 AM, Place: Amethi")
print("=" * 80)

# ============================================================================
# 1. BIRTH DATA
# ============================================================================
print("\n" + "=" * 80)
print("1. BIRTH DATA VERIFICATION")
print("=" * 80)
bd = k.birth_data
print(f"   Name: {bd.name}")
print(f"   Date: {bd.date.strftime('%d-%m-%Y')}")
print(f"   Time: {bd.date.strftime('%H:%M:%S')} ({bd.date.strftime('%I:%M %p')})")
print(f"   City: {bd.city}")
print(f"   Latitude: {bd.latitude:.4f}°")
print(f"   Longitude: {bd.longitude:.4f}°")
print(f"   Timezone: {bd.timezone}")
print(f"   Julian Day: {k.jd:.6f}")

# Verify coordinates for Amethi
# Amethi is approximately 26.15°N, 81.81°E
if 25 < bd.latitude < 27 and 80 < bd.longitude < 83:
    print(f"   ✅ Coordinates verified for Amethi region")
else:
    print(f"   ⚠️ Coordinates may not be accurate for Amethi")

# ============================================================================
# 2. LAGNA (ASCENDANT) DETAILS
# ============================================================================
print("\n" + "=" * 80)
print("2. LAGNA (ASCENDANT) - COMPLETE DETAILS")
print("=" * 80)
print(f"   Total Longitude: {lagna['longitude']:.4f}°")
print(f"   Rashi Number (0-11): {lagna['rashi_num']}")
print(f"   Rashi: {lagna['rashi']} ({lagna['rashi_english']}) - {rashi_hindi.get(lagna['rashi'], '')}")
print(f"   Degree in Rashi: {lagna['rashi_degree']:.4f}°")
print(f"   Nakshatra Number (0-26): {lagna['nakshatra_num']}")
print(f"   Nakshatra: {lagna['nakshatra']}")
print(f"   Nakshatra Lord: {lagna['nakshatra_lord']}")
print(f"   Pada: {lagna['pada']}")

# Manual verification
calc_rashi = int(lagna['longitude'] / 30) % 12
calc_nakshatra = int(lagna['longitude'] / (360/27)) % 27
print(f"\n   MANUAL CALCULATION:")
print(f"   {lagna['longitude']:.4f}° / 30 = {lagna['longitude']/30:.4f} → Rashi {calc_rashi} ({RASHIS[calc_rashi]['name']})")
print(f"   {lagna['longitude']:.4f}° / 13.333 = {lagna['longitude']/13.333:.4f} → Nakshatra {calc_nakshatra} ({NAKSHATRAS[calc_nakshatra]['name']})")

if calc_rashi == lagna['rashi_num'] and RASHIS[calc_rashi]['name'] == lagna['rashi']:
    print(f"   ✅ LAGNA CALCULATION VERIFIED")
else:
    print(f"   ❌ LAGNA CALCULATION ERROR")

# ============================================================================
# 3. ALL PLANET POSITIONS - DETAILED
# ============================================================================
print("\n" + "=" * 80)
print("3. PLANETARY POSITIONS - COMPLETE DETAILS")
print("=" * 80)

for p_name in ["SUN", "MOON", "MARS", "MERCURY", "JUPITER", "VENUS", "SATURN", "RAHU", "KETU"]:
    p = planets[p_name]
    hindi_name = PLANET_NAMES[Planet[p_name]]["hindi"]

    # Find house
    house = 0
    for h, plist in planets_in_houses.items():
        if p_name in plist:
            house = h
            break

    # Manual verification
    calc_rashi = int(p['longitude'] / 30) % 12
    calc_nak = int(p['longitude'] / (360/27)) % 27

    rashi_match = calc_rashi == p['rashi_num'] and RASHIS[calc_rashi]['name'] == p['rashi']
    nak_match = calc_nak == p['nakshatra_num']

    status = "✅" if rashi_match and nak_match else "❌"

    print(f"\n   {p_name} ({hindi_name}) {status}")
    print(f"   ├── Longitude: {p['longitude']:.4f}°")
    print(f"   ├── Rashi: {p['rashi']} ({p['rashi_english']}) - {rashi_hindi.get(p['rashi'], '')}")
    print(f"   ├── Degree in Rashi: {p['rashi_degree']:.4f}°")
    print(f"   ├── Nakshatra: {p['nakshatra']} (Lord: {p['nakshatra_lord']})")
    print(f"   ├── Pada: {p['pada']}")
    print(f"   ├── House: {house}")
    print(f"   ├── Retrograde: {'Yes (वक्री)' if p['is_retrograde'] else 'No (मार्गी)'}")
    if p.get('speed'):
        print(f"   └── Speed: {p['speed']:.6f}°/day")
    else:
        print(f"   └── Speed: N/A")

# ============================================================================
# 4. HOUSE (BHAVA) ANALYSIS
# ============================================================================
print("\n" + "=" * 80)
print("4. BHAVA (HOUSE) ANALYSIS")
print("=" * 80)

lagna_rashi_num = lagna['rashi_num']
print(f"\n   Lagna Rashi Number: {lagna_rashi_num} ({RASHIS[lagna_rashi_num]['name']})")
print(f"\n   {'House':<8} {'Rashi':<12} {'Hindi':<10} {'Lord':<10} {'Planets':<25} {'Significance'}")
print("   " + "-" * 90)

for house_num in range(1, 13):
    rashi_num = (lagna_rashi_num + house_num - 1) % 12
    rashi = RASHIS[rashi_num]
    house_planets = planets_in_houses.get(house_num, [])
    planets_str = ', '.join(house_planets) if house_planets else '-'
    significance = BHAVA_NAMES[house_num]['significance'][:30] + "..." if len(BHAVA_NAMES[house_num]['significance']) > 30 else BHAVA_NAMES[house_num]['significance']

    print(f"   {house_num:<8} {rashi['name']:<12} {rashi_hindi.get(rashi['name'], ''):<10} {rashi['lord']:<10} {planets_str:<25} {significance}")

# ============================================================================
# 5. NAKSHATRA DETAILS
# ============================================================================
print("\n" + "=" * 80)
print("5. NAKSHATRA ANALYSIS")
print("=" * 80)

moon = planets['MOON']
print(f"\n   BIRTH NAKSHATRA (Moon's Nakshatra):")
print(f"   ├── Nakshatra: {moon['nakshatra']}")
print(f"   ├── Nakshatra Number: {moon['nakshatra_num']} (of 27)")
print(f"   ├── Nakshatra Lord: {moon['nakshatra_lord']}")
print(f"   ├── Pada: {moon['pada']}")
print(f"   └── Degree in Nakshatra: {moon['longitude'] % (360/27):.4f}°")

# Nakshatra characteristics
nakshatra_data = NAKSHATRAS[moon['nakshatra_num']]
print(f"\n   SHATABHISHA NAKSHATRA DETAILS:")
print(f"   ├── Name: {nakshatra_data['name']}")
print(f"   ├── Lord: {nakshatra_data['lord']}")
print(f"   ├── Deity: {nakshatra_data['deity']}")
print(f"   └── Start Degree: {nakshatra_data['start']}°")

# ============================================================================
# 6. VIMSHOTTARI DASHA
# ============================================================================
print("\n" + "=" * 80)
print("6. VIMSHOTTARI DASHA ANALYSIS")
print("=" * 80)

print(f"\n   CURRENT DASHA:")
print(f"   ├── Full: {current_dasha['full_dasha']}")
print(f"   ├── Mahadasha: {current_dasha['mahadasha']['planet']}")
print(f"   │   ├── Start: {current_dasha['mahadasha']['start'].strftime('%d-%m-%Y')}")
print(f"   │   └── End: {current_dasha['mahadasha']['end'].strftime('%d-%m-%Y')}")
print(f"   ├── Antardasha: {current_dasha['antardasha']['planet']}")
print(f"   │   ├── Start: {current_dasha['antardasha']['start'].strftime('%d-%m-%Y')}")
print(f"   │   └── End: {current_dasha['antardasha']['end'].strftime('%d-%m-%Y')}")
print(f"   └── Pratyantardasha: {current_dasha['pratyantardasha']['planet']}")
print(f"       ├── Start: {current_dasha['pratyantardasha']['start'].strftime('%d-%m-%Y')}")
print(f"       └── End: {current_dasha['pratyantardasha']['end'].strftime('%d-%m-%Y')}")

print(f"\n   MAHADASHA TIMELINE (Full 120 Years):")
print(f"   {'Dasha':<12} {'Start':<12} {'End':<12} {'Duration':<12} {'Status'}")
print("   " + "-" * 60)

now = datetime.now()
for m in mahadashas:
    if m.start_date <= now <= m.end_date:
        status = "← CURRENT"
    elif m.start_date > now:
        status = "Future"
    else:
        status = "Past"
    print(f"   {m.planet:<12} {m.start_date.strftime('%d-%m-%Y'):<12} {m.end_date.strftime('%d-%m-%Y'):<12} {m.duration_years:.1f} years    {status}")

# ============================================================================
# 7. YOGA ANALYSIS
# ============================================================================
print("\n" + "=" * 80)
print("7. YOGA ANALYSIS")
print("=" * 80)

try:
    yoga_analyzer = YogaAnalyzer(k)
    yogas = yoga_analyzer.analyze_all_yogas()

    print(f"\n   Found {len(yogas)} Yogas:")
    for i, yoga in enumerate(yogas, 1):
        print(f"\n   {i}. {yoga.get('name', 'Unknown Yoga')}")
        print(f"      Type: {yoga.get('type', 'N/A')}")
        print(f"      Planets: {yoga.get('planets', 'N/A')}")
        if yoga.get('description'):
            desc = yoga['description'][:80] + "..." if len(yoga.get('description', '')) > 80 else yoga.get('description', '')
            print(f"      Description: {desc}")
except Exception as e:
    print(f"   Yoga analysis error: {e}")

# ============================================================================
# 8. SPECIAL POSITIONS CHECK
# ============================================================================
print("\n" + "=" * 80)
print("8. SPECIAL PLANETARY CONDITIONS")
print("=" * 80)

for p_name, p_data in planets.items():
    rashi = p_data['rashi']
    rashi_lord = RASHIS[p_data['rashi_num']]['lord']

    conditions = []

    # Check if planet is in own sign
    planet_rules = {
        'SUN': ['Simha'],
        'MOON': ['Karka'],
        'MARS': ['Mesha', 'Vrishchika'],
        'MERCURY': ['Mithuna', 'Kanya'],
        'JUPITER': ['Dhanu', 'Meena'],
        'VENUS': ['Vrishabha', 'Tula'],
        'SATURN': ['Makara', 'Kumbha'],
    }

    if p_name in planet_rules and rashi in planet_rules[p_name]:
        conditions.append("OWN SIGN (स्वराशि)")

    # Check exaltation
    exaltation = {
        'SUN': 'Mesha', 'MOON': 'Vrishabha', 'MARS': 'Makara',
        'MERCURY': 'Kanya', 'JUPITER': 'Karka', 'VENUS': 'Meena', 'SATURN': 'Tula'
    }
    if p_name in exaltation and rashi == exaltation[p_name]:
        conditions.append("EXALTED (उच्च)")

    # Check debilitation
    debilitation = {
        'SUN': 'Tula', 'MOON': 'Vrishchika', 'MARS': 'Karka',
        'MERCURY': 'Meena', 'JUPITER': 'Makara', 'VENUS': 'Kanya', 'SATURN': 'Mesha'
    }
    if p_name in debilitation and rashi == debilitation[p_name]:
        conditions.append("DEBILITATED (नीच)")

    # Retrograde
    if p_data['is_retrograde']:
        conditions.append("RETROGRADE (वक्री)")

    if conditions:
        print(f"   {p_name}: {', '.join(conditions)}")

# Check for special conditions
print(f"\n   SPECIAL NOTES:")

# Sun debilitated in Tula
if planets['SUN']['rashi'] == 'Tula':
    print(f"   ⚠️ Sun is DEBILITATED in Tula (Libra) - Neecha Surya")

# Saturn in own sign
if planets['SATURN']['rashi'] in ['Makara', 'Kumbha']:
    print(f"   ✅ Saturn is in OWN SIGN ({planets['SATURN']['rashi']}) - Strong Saturn")

# Venus in Lagna
if 'VENUS' in planets_in_houses.get(1, []):
    print(f"   ✅ Venus in Lagna - Good for personality and relationships")

# Multiple planets in one house
for h, plist in planets_in_houses.items():
    if len(plist) >= 3:
        print(f"   ⚠️ {len(plist)} planets in House {h} ({RASHIS[(lagna_rashi_num + h - 1) % 12]['name']}) - Strong house influence")

# ============================================================================
# 9. ASHTAKAVARGA POINTS (if available)
# ============================================================================
print("\n" + "=" * 80)
print("9. KEY PREDICTIONS SUMMARY")
print("=" * 80)

# Career
tenth_house_planets = planets_in_houses.get(10, [])
tenth_lord = RASHIS[(lagna_rashi_num + 9) % 12]['lord']
print(f"\n   CAREER (10th House):")
print(f"   ├── 10th House Rashi: {RASHIS[(lagna_rashi_num + 9) % 12]['name']}")
print(f"   ├── 10th Lord: {tenth_lord}")
print(f"   └── Planets in 10th: {', '.join(tenth_house_planets) if tenth_house_planets else 'None'}")

# Marriage
seventh_house_planets = planets_in_houses.get(7, [])
seventh_lord = RASHIS[(lagna_rashi_num + 6) % 12]['lord']
print(f"\n   MARRIAGE (7th House):")
print(f"   ├── 7th House Rashi: {RASHIS[(lagna_rashi_num + 6) % 12]['name']}")
print(f"   ├── 7th Lord: {seventh_lord}")
print(f"   └── Planets in 7th: {', '.join(seventh_house_planets) if seventh_house_planets else 'None'}")

# Wealth
second_house_planets = planets_in_houses.get(2, [])
print(f"\n   WEALTH (2nd House):")
print(f"   ├── 2nd House Rashi: {RASHIS[(lagna_rashi_num + 1) % 12]['name']}")
print(f"   ├── Planets in 2nd: {', '.join(second_house_planets) if second_house_planets else 'None'}")
if len(second_house_planets) >= 3:
    print(f"   └── ⭐ STRONG DHANA YOGA - Multiple planets in 2nd house!")

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("FINAL VERIFICATION SUMMARY")
print("=" * 80)

errors = []

# Verify all rashis
for p_name, p_data in planets.items():
    calc_rashi = int(p_data['longitude'] / 30) % 12
    if calc_rashi != p_data['rashi_num']:
        errors.append(f"{p_name}: rashi_num mismatch")
    if RASHIS[p_data['rashi_num']]['name'] != p_data['rashi']:
        errors.append(f"{p_name}: rashi name mismatch")

# Verify all nakshatras
for p_name, p_data in planets.items():
    calc_nak = int(p_data['longitude'] / (360/27)) % 27
    if calc_nak != p_data['nakshatra_num']:
        errors.append(f"{p_name}: nakshatra_num mismatch")

if errors:
    print(f"\n   ❌ ERRORS FOUND:")
    for e in errors:
        print(f"      - {e}")
else:
    print(f"\n   ✅ ALL CALCULATIONS VERIFIED CORRECT")
    print(f"\n   KEY DETAILS:")
    print(f"   ├── Lagna: {lagna['rashi']} ({lagna['rashi_english']}) - {rashi_hindi.get(lagna['rashi'], '')}")
    print(f"   ├── Chandra Rashi: {planets['MOON']['rashi']} ({planets['MOON']['rashi_english']}) - {rashi_hindi.get(planets['MOON']['rashi'], '')}")
    print(f"   ├── Surya Rashi: {planets['SUN']['rashi']} ({planets['SUN']['rashi_english']}) - {rashi_hindi.get(planets['SUN']['rashi'], '')}")
    print(f"   ├── Birth Nakshatra: {planets['MOON']['nakshatra']} (Pada {planets['MOON']['pada']})")
    print(f"   ├── Nakshatra Lord: {planets['MOON']['nakshatra_lord']}")
    print(f"   └── Current Dasha: {current_dasha['full_dasha']}")

print("\n" + "=" * 80)
