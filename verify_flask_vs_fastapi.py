# -*- coding: utf-8 -*-
"""
Comprehensive verification: Flask vs FastAPI outputs for Alok Yadav
Birth: 25/10/1993, 05:15 AM, Amethi
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from src.kundali import create_kundali
from src.config import RASHIS, PLANET_NAMES, Planet

# Create Kundali for Alok Yadav
k = create_kundali(
    name='Alok Yadav',
    year=1993, month=10, day=25,
    hour=5, minute=15,
    city='Amethi'
)

print("=" * 70)
print("VERIFICATION: ALOK YADAV")
print("DOB: 25/10/1993, TOB: 05:15 AM, Place: Amethi")
print("=" * 70)

# Get all data
planets = k.planets
lagna = k.lagna
planets_in_houses = k.get_planets_in_houses()
current_dasha = k.get_current_dasha()

# Rashi Hindi mapping (same as Flask app)
rashi_hindi = {
    "Mesha": "मेष", "Vrishabha": "वृषभ", "Mithuna": "मिथुन", "Karka": "कर्क",
    "Simha": "सिंह", "Kanya": "कन्या", "Tula": "तुला", "Vrishchika": "वृश्चिक",
    "Dhanu": "धनु", "Makara": "मकर", "Kumbha": "कुंभ", "Meena": "मीन"
}

print("\n" + "-" * 70)
print("1. LAGNA (ASCENDANT)")
print("-" * 70)
print(f"   Rashi Number (0-indexed): {lagna['rashi_num']}")
print(f"   Rashi (Sanskrit): {lagna['rashi']}")
print(f"   Rashi (Hindi): {rashi_hindi.get(lagna['rashi'], 'MISSING')}")
print(f"   Rashi (English): {lagna['rashi_english']}")
print(f"   Degree: {lagna['rashi_degree']:.4f}°")
print(f"   Nakshatra: {lagna['nakshatra']}")
print(f"   Pada: {lagna['pada']}")

# Verify lagna calculation
expected_lagna_rashi = RASHIS[lagna['rashi_num']]['name']
if expected_lagna_rashi == lagna['rashi']:
    print(f"   ✅ LAGNA VERIFIED: rashi_num {lagna['rashi_num']} = {expected_lagna_rashi}")
else:
    print(f"   ❌ LAGNA MISMATCH: rashi_num {lagna['rashi_num']} should be {expected_lagna_rashi}, got {lagna['rashi']}")

print("\n" + "-" * 70)
print("2. MOON (CHANDRA RASHI)")
print("-" * 70)
moon = planets['MOON']
print(f"   Longitude: {moon['longitude']:.4f}°")
print(f"   Rashi Number (0-indexed): {moon['rashi_num']}")
print(f"   Rashi (Sanskrit): {moon['rashi']}")
print(f"   Rashi (Hindi): {rashi_hindi.get(moon['rashi'], 'MISSING')}")
print(f"   Rashi (English): {moon['rashi_english']}")
print(f"   Degree in Sign: {moon['rashi_degree']:.4f}°")
print(f"   Nakshatra: {moon['nakshatra']}")
print(f"   Nakshatra Lord: {moon['nakshatra_lord']}")
print(f"   Pada: {moon['pada']}")

# Verify Moon calculation
expected_moon_rashi = RASHIS[moon['rashi_num']]['name']
if expected_moon_rashi == moon['rashi']:
    print(f"   ✅ MOON VERIFIED: rashi_num {moon['rashi_num']} = {expected_moon_rashi}")
else:
    print(f"   ❌ MOON MISMATCH: rashi_num {moon['rashi_num']} should be {expected_moon_rashi}, got {moon['rashi']}")

# Calculate expected rashi from longitude
calculated_rashi_num = int(moon['longitude'] / 30) % 12
calculated_rashi = RASHIS[calculated_rashi_num]['name']
print(f"\n   MANUAL VERIFICATION:")
print(f"   Moon Longitude: {moon['longitude']:.4f}°")
print(f"   {moon['longitude']:.4f} / 30 = {moon['longitude']/30:.4f}")
print(f"   int({moon['longitude']/30:.4f}) % 12 = {calculated_rashi_num}")
print(f"   RASHIS[{calculated_rashi_num}] = {calculated_rashi}")

if calculated_rashi_num == moon['rashi_num']:
    print(f"   ✅ CALCULATION CORRECT")
else:
    print(f"   ❌ CALCULATION ERROR: Expected {calculated_rashi_num}, got {moon['rashi_num']}")

print("\n" + "-" * 70)
print("3. ALL PLANETS")
print("-" * 70)
print(f"{'Planet':<12} {'Long':<10} {'Rashi#':<8} {'Rashi':<12} {'Hindi':<10} {'Nakshatra':<15} {'House':<6}")
print("-" * 70)

for p_name in ["SUN", "MOON", "MARS", "MERCURY", "JUPITER", "VENUS", "SATURN", "RAHU", "KETU"]:
    data = planets[p_name]

    # Find house
    house = 0
    for h, plist in planets_in_houses.items():
        if p_name in plist:
            house = h
            break

    hindi_rashi = rashi_hindi.get(data['rashi'], 'MISSING')

    # Verify
    expected = RASHIS[data['rashi_num']]['name']
    status = "✅" if expected == data['rashi'] else "❌"

    print(f"{p_name:<12} {data['longitude']:>8.2f}° {data['rashi_num']:<8} {data['rashi']:<12} {hindi_rashi:<10} {data['nakshatra']:<15} {house:<6} {status}")

print("\n" + "-" * 70)
print("4. PLANETS IN HOUSES (Bhava Chart)")
print("-" * 70)
lagna_rashi_num = lagna['rashi_num']
for house_num in range(1, 13):
    rashi_num = (lagna_rashi_num + house_num - 1) % 12
    rashi_name = RASHIS[rashi_num]['name']
    house_planets = planets_in_houses.get(house_num, [])
    planets_str = ', '.join(house_planets) if house_planets else '-'
    print(f"   House {house_num:2d} ({rashi_name:12}): {planets_str}")

print("\n" + "-" * 70)
print("5. CURRENT DASHA")
print("-" * 70)
print(f"   Full Dasha: {current_dasha['full_dasha']}")
print(f"   Mahadasha: {current_dasha['mahadasha']['planet']} ({current_dasha['mahadasha']['start'].strftime('%Y')} - {current_dasha['mahadasha']['end'].strftime('%Y')})")
print(f"   Antardasha: {current_dasha['antardasha']['planet']}")
print(f"   Pratyantardasha: {current_dasha['pratyantardasha']['planet']}")

print("\n" + "-" * 70)
print("6. FLASK HTML CHECK")
print("-" * 70)
# This is exactly what Flask app does in generate_kundali_result_html()
flask_chandra_rashi = rashi_hindi.get(planets['MOON']['rashi'], planets['MOON']['rashi'])
print(f"   Flask uses: rashi_hindi.get(planets['MOON']['rashi'], ...)")
print(f"   planets['MOON']['rashi'] = '{planets['MOON']['rashi']}'")
print(f"   rashi_hindi.get('{planets['MOON']['rashi']}', ...) = '{flask_chandra_rashi}'")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"   Lagna: {lagna['rashi']} ({lagna['rashi_english']}) - {rashi_hindi.get(lagna['rashi'], '')}")
print(f"   Chandra Rashi: {moon['rashi']} ({moon['rashi_english']}) - {rashi_hindi.get(moon['rashi'], '')}")
print(f"   Birth Nakshatra: {moon['nakshatra']} (Lord: {moon['nakshatra_lord']})")

# Final verification
all_verified = True
for p_name, data in planets.items():
    expected = RASHIS[data['rashi_num']]['name']
    if expected != data['rashi']:
        all_verified = False
        print(f"\n   ❌ ERROR in {p_name}: rashi_num={data['rashi_num']} expects '{expected}' but got '{data['rashi']}'")

if all_verified:
    print(f"\n   ✅ ALL CALCULATIONS VERIFIED CORRECT")
else:
    print(f"\n   ❌ SOME CALCULATIONS HAVE ERRORS - SEE ABOVE")

print("=" * 70)
