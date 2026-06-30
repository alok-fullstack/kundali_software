# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from src.kundali import create_kundali
from backend.api.html_generator import generate_kundali_html
import re

k = create_kundali(
    name='Alok',
    year=1993, month=10, day=25,
    hour=5, minute=15,
    city='Amethi'
)

html = generate_kundali_html(k)

# Find Chandra Rashi in HTML
print("=" * 60)
print("CHECKING HTML OUTPUT")
print("=" * 60)

# Check Moon data directly
print(f"\nMoon data from Kundali object:")
print(f"  rashi: {k.planets['MOON']['rashi']}")
print(f"  rashi_english: {k.planets['MOON']['rashi_english']}")
print(f"  rashi_num: {k.planets['MOON']['rashi_num']}")

# Search for Chandra Rashi in HTML
patterns = [
    (r'चंद्र राशि</div><div class="value">(.*?)</div>', 'Chandra Rashi (Hindi)'),
    (r'Moon Sign.*?<td>(.*?)</td>', 'Moon Sign table'),
    (r'MOON.*?<td>(.*?)</td>', 'MOON row'),
]

print(f"\nSearching in HTML ({len(html)} chars):")
for pattern, name in patterns:
    match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
    if match:
        print(f"  {name}: {match.group(1)[:50]}")
    else:
        print(f"  {name}: NOT FOUND")

# Extract the specific birth-item section
birth_section = re.search(r'<div class="birth-item">.*?चंद्र राशि.*?</div></div>', html, re.DOTALL)
if birth_section:
    print(f"\nBirth section excerpt:")
    print(birth_section.group(0)[:200])
