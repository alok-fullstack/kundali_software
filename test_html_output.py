# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from src.kundali import create_kundali
from backend.api.html_generator import generate_kundali_html
import re

k = create_kundali(name='Alok', year=1993, month=10, day=25, hour=5, minute=15, city='Amethi')

print("=" * 60)
print("MOON DATA FROM KUNDALI OBJECT:")
print("=" * 60)
print(f"  planets['MOON']['rashi']: {k.planets['MOON']['rashi']}")
print(f"  planets['MOON']['rashi_num']: {k.planets['MOON']['rashi_num']}")
print(f"  planets['MOON']['rashi_english']: {k.planets['MOON']['rashi_english']}")

html = generate_kundali_html(k)

print("\n" + "=" * 60)
print("HTML OUTPUT CHECK:")
print("=" * 60)

# Find Chandra Rashi
match = re.search(r'चंद्र राशि</div><div class="value">([^<]+)</div>', html)
if match:
    print(f"  Chandra Rashi displayed: {match.group(1)}")
else:
    print("  ERROR: Could not find Chandra Rashi in HTML")

# Find Lagna Rashi
match2 = re.search(r'लग्न राशि</div><div class="value">([^<]+)</div>', html)
if match2:
    print(f"  Lagna Rashi displayed: {match2.group(1)}")

# Check if Makara appears anywhere near Moon
if 'मकर' in html:
    # Find all occurrences of Makara
    positions = [m.start() for m in re.finditer('मकर', html)]
    print(f"\n  'मकर' (Makara) found at {len(positions)} positions in HTML")

    # Check context around each
    for pos in positions[:5]:  # First 5
        context = html[max(0, pos-50):pos+50]
        # Clean up for display
        context = context.replace('\n', ' ').replace('  ', ' ')
        print(f"    Context: ...{context}...")

print("\n" + "=" * 60)
