# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from src.kundali import create_kundali

print("=" * 70)
print("COMPARING TWO DATES - Moon moves ~13° per day!")
print("=" * 70)

# Date from screenshot: 24-10-1993
k1 = create_kundali(name='Alok', year=1993, month=10, day=24, hour=5, minute=15, city='Amethi')

print("\n24-10-1993, 05:15 AM (From Screenshot):")
print(f"  Moon Longitude: {k1.planets['MOON']['longitude']:.4f}°")
print(f"  Moon Rashi: {k1.planets['MOON']['rashi']} ({k1.planets['MOON']['rashi_english']})")
print(f"  Moon Nakshatra: {k1.planets['MOON']['nakshatra']} Pada {k1.planets['MOON']['pada']}")

# Date you told me: 25-10-1993
k2 = create_kundali(name='Alok', year=1993, month=10, day=25, hour=5, minute=15, city='Amethi')

print("\n25-10-1993, 05:15 AM (Date you told me):")
print(f"  Moon Longitude: {k2.planets['MOON']['longitude']:.4f}°")
print(f"  Moon Rashi: {k2.planets['MOON']['rashi']} ({k2.planets['MOON']['rashi_english']})")
print(f"  Moon Nakshatra: {k2.planets['MOON']['nakshatra']} Pada {k2.planets['MOON']['pada']}")

print("\n" + "=" * 70)
print("MOON MOVEMENT:")
print(f"  Movement in 1 day: {k2.planets['MOON']['longitude'] - k1.planets['MOON']['longitude']:.4f}°")
print("=" * 70)

# Determine which is correct
print("\nWHICH IS YOUR ACTUAL BIRTH DATE?")
print("  24-10-1993 → Moon in Makara (Capricorn), Dhanishta")
print("  25-10-1993 → Moon in Kumbha (Aquarius), Shatabhisha")
