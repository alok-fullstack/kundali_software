# -*- coding: utf-8 -*-
"""Verify Kundali for Alok Yadav"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from src.kundali import create_kundali
from src.divisional_charts import DivisionalChartCalculator

# Create Kundali for Alok Yadav
k = create_kundali(
    name='Alok Yadav',
    year=1993, month=10, day=25,
    hour=5, minute=15,
    city='Amethi'
)

signs_en = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
            'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

print('=' * 65)
print('KUNDALI FOR ALOK YADAV')
print('DOB: 25/10/1993, TOB: 05:15 AM, Place: Amethi')
print('=' * 65)

# Lagna details
lagna_data = k.lagna
if isinstance(lagna_data, dict):
    print(f"\nLagna (Ascendant): {lagna_data.get('rashi_english', 'Unknown')} ({lagna_data.get('rashi', '')})")
    print(f"Lagna Degree: {lagna_data.get('rashi_degree', 0):.2f}")
    print(f"Lagna Nakshatra: {lagna_data.get('nakshatra', 'Unknown')}")
else:
    print(f"\nLagna: {signs_en[lagna_data - 1] if 1 <= lagna_data <= 12 else 'Unknown'}")

print()
print('PLANETARY POSITIONS (D-1 Rashi Chart):')
print('-' * 65)
print(f"{'Planet':<12} {'Rashi (Sign)':<18} {'Degree':<10} {'Nakshatra':<15}")
print('-' * 65)

for planet, pos in k.planets.items():
    rashi = pos.get('rashi_english', pos.get('rashi', 'Unknown'))
    degree = pos.get('rashi_degree', pos.get('longitude', 0) % 30)
    nakshatra = pos.get('nakshatra', 'Unknown')
    retro = ' (R)' if pos.get('retrograde', False) else ''
    print(f"{planet:<12} {rashi:<18} {degree:>6.2f}{retro:<4} {nakshatra:<15}")

# Moon sign for reference
moon = k.planets.get('MOON', {})
print()
print(f"Moon Sign (Rashi): {moon.get('rashi_english', 'Unknown')} ({moon.get('rashi', '')})")
print(f"Birth Nakshatra: {moon.get('nakshatra', 'Unknown')}")

# Divisional Charts
calc = DivisionalChartCalculator()

print()
print('=' * 65)
print('D-9 NAVAMSA CHART (Marriage/Spouse/Dharma):')
print('=' * 65)
print(f"{'Planet':<12} {'D-1 Sign':<15} {'D-9 Navamsa':<15}")
print('-' * 65)

for planet, pos in k.planets.items():
    rashi_num = pos.get('rashi_num', 1)
    degree = pos.get('rashi_degree', pos.get('longitude', 0) % 30)
    navamsa = calc.calculate_d9_navamsa(rashi_num, degree)
    d1_sign = pos.get('rashi_english', 'Unknown')
    # Handle DivisionalPosition object
    d9_sign = navamsa.varga_rashi_english if hasattr(navamsa, 'varga_rashi_english') else 'Unknown'
    print(f"{planet:<12} {d1_sign:<15} {d9_sign:<15}")

print()
print('=' * 65)
print('D-10 DASAMSA CHART (Career/Profession):')
print('=' * 65)
print(f"{'Planet':<12} {'D-1 Sign':<15} {'D-10 Dasamsa':<15}")
print('-' * 65)

for planet, pos in k.planets.items():
    rashi_num = pos.get('rashi_num', 1)
    degree = pos.get('rashi_degree', pos.get('longitude', 0) % 30)
    dasamsa = calc.calculate_d10_dasamsa(rashi_num, degree)
    d1_sign = pos.get('rashi_english', 'Unknown')
    # Handle DivisionalPosition object
    d10_sign = dasamsa.varga_rashi_english if hasattr(dasamsa, 'varga_rashi_english') else 'Unknown'
    print(f"{planet:<12} {d1_sign:<15} {d10_sign:<15}")

print()
print('=' * 65)
print('VERIFICATION COMPLETE')
print('=' * 65)
