"""
HTML Generator for Kundali Results
Generates the same HTML as the Flask version for frontend display.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
parent_dir = Path(__file__).resolve().parent.parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from src.config import PLANET_NAMES, Planet, BHAVA_NAMES, RASHIS
from src.full_predictions import (
    get_full_career_analysis, get_full_marriage_analysis,
    get_full_children_analysis, get_full_health_analysis,
    get_full_wealth_analysis, get_full_dasha_analysis,
    get_full_yoga_analysis, get_full_remedies, get_full_transit_analysis,
    get_planetary_strength_analysis
)

RASHI_HINDI = {
    "Mesha": "मेष", "Vrishabha": "वृषभ", "Mithuna": "मिथुन", "Karka": "कर्क",
    "Simha": "सिंह", "Kanya": "कन्या", "Tula": "तुला", "Vrishchika": "वृश्चिक",
    "Dhanu": "धनु", "Makara": "मकर", "Kumbha": "कुंभ", "Meena": "मीन"
}


def calculate_career_rating(planets_in_houses):
    score = 3
    tenth_planets = planets_in_houses.get(10, [])
    if "JUPITER" in tenth_planets or "SUN" in tenth_planets:
        score += 1
    if "SATURN" in tenth_planets:
        score += 0.5
    if "MARS" in planets_in_houses.get(10, []) or "MARS" in planets_in_houses.get(6, []):
        score += 0.5
    return f"{'⭐' * min(5, int(score))}"


def calculate_marriage_rating(planets_in_houses):
    score = 3
    seventh = planets_in_houses.get(7, [])
    if "VENUS" in seventh or "JUPITER" in seventh:
        score += 1
    if "SATURN" in seventh or "RAHU" in seventh:
        score -= 0.5
    return f"{'⭐' * min(5, max(1, int(score)))}"


def calculate_children_rating(planets_in_houses):
    score = 3
    fifth = planets_in_houses.get(5, [])
    if "JUPITER" in fifth:
        score += 1
    if "SATURN" in fifth or "RAHU" in fifth:
        score -= 0.5
    return f"{'⭐' * min(5, max(1, int(score)))}"


def calculate_health_rating(planets_in_houses):
    score = 3
    sixth = planets_in_houses.get(6, [])
    if len(sixth) == 0:
        score += 1
    if "SATURN" in planets_in_houses.get(1, []):
        score -= 0.5
    return f"{'⭐' * min(5, max(1, int(score)))}"


def calculate_wealth_rating(planets_in_houses):
    score = 3
    second = planets_in_houses.get(2, [])
    eleventh = planets_in_houses.get(11, [])
    if "JUPITER" in second or "VENUS" in second:
        score += 1
    if "JUPITER" in eleventh:
        score += 0.5
    return f"{'⭐' * min(5, max(1, int(score)))}"


def generate_chart(kundali, planets_in_houses, lagna_num):
    """Generate the traditional Kundali chart HTML."""
    rashi_positions = [[12,1,2,3],[11,0,0,4],[10,0,0,5],[9,8,7,6]]
    rashi_names = {1:"मेष",2:"वृषभ",3:"मिथुन",4:"कर्क",5:"सिंह",6:"कन्या",7:"तुला",8:"वृश्चिक",9:"धनु",10:"मकर",11:"कुंभ",12:"मीन"}

    html = '<div class="chart-container"><table class="chart-table">'
    for row in rashi_positions:
        html += "<tr>"
        for rashi_num in row:
            if rashi_num == 0:
                html += '<td style="background:linear-gradient(135deg,#fff8dc,#ffe4b5);"></td>'
            else:
                house_num = ((rashi_num - lagna_num - 1) % 12) + 1
                house_planets = planets_in_houses.get(house_num, [])
                planet_str = ""
                for p in house_planets:
                    symbol = PLANET_NAMES[Planet[p]]["symbol"]
                    retro = "(व)" if kundali.planets[p]["is_retrograde"] else ""
                    planet_str += f"{symbol}{retro} "
                cell_class = 'class="lagna-cell"' if house_num == 1 else ''
                html += f'<td {cell_class}><div class="rashi-name">{rashi_names[rashi_num]}</div><div class="house-num">भाव {house_num}</div><div style="margin-top:5px;">{planet_str}</div></td>'
        html += "</tr>"
    html += "</table></div>"
    return html


def generate_kundali_html(kundali) -> str:
    """Generate complete detailed kundali HTML."""
    planets = kundali.planets
    lagna = kundali.lagna
    planets_in_houses = kundali.get_planets_in_houses()
    mahadashas = kundali.get_mahadashas(years=100)
    current_dasha = kundali.get_current_dasha()
    birth = kundali.birth_data

    lagna_num = lagna["rashi_num"]
    house_rashis = {}
    for i in range(1, 13):
        rashi_num = (lagna_num + i - 1) % 12
        house_rashis[i] = RASHIS[rashi_num]

    # Generate chart
    chart_html = generate_chart(kundali, planets_in_houses, lagna_num)

    # Generate planet rows
    planet_rows = ""
    for p_name in ["SUN", "MOON", "MARS", "MERCURY", "JUPITER", "VENUS", "SATURN", "RAHU", "KETU"]:
        data = planets[p_name]
        hindi = PLANET_NAMES[Planet[p_name]]["hindi"]
        symbol = PLANET_NAMES[Planet[p_name]]["symbol"]
        rashi = RASHI_HINDI.get(data['rashi'], data['rashi'])
        house = 0
        for h, plist in planets_in_houses.items():
            if p_name in plist:
                house = h
                break
        retro = "वक्री" if data["is_retrograde"] else "मार्गी"
        retro_class = "status-caution" if data["is_retrograde"] else "status-good"
        planet_rows += f'''<tr>
            <td>{symbol} {hindi}</td>
            <td>{rashi}</td>
            <td>{data['rashi_degree']:.2f}°</td>
            <td>{data['nakshatra']} पाद {data['pada']}</td>
            <td>{house}</td>
            <td class="{retro_class}">{retro}</td>
        </tr>'''

    # Generate bhava rows
    bhava_rows = ""
    bhava_significance = {
        1: "आत्म, व्यक्तित्व", 2: "धन, परिवार", 3: "भाई-बहन, साहस",
        4: "माता, घर, सुख", 5: "संतान, बुद्धि", 6: "शत्रु, रोग",
        7: "विवाह, साझेदारी", 8: "आयु, रहस्य", 9: "भाग्य, धर्म",
        10: "करियर, यश", 11: "लाभ, आय", 12: "व्यय, मोक्ष"
    }
    for h in range(1, 13):
        p_list = planets_in_houses.get(h, [])
        rashi = RASHI_HINDI.get(house_rashis[h]['name'], house_rashis[h]['name'])
        p_str = ', '.join([PLANET_NAMES[Planet[p]]["hindi"] for p in p_list]) if p_list else '-'
        bhava_rows += f'<tr><td>{h} ({BHAVA_NAMES[h]["name"]})</td><td>{rashi}</td><td>{p_str}</td><td>{bhava_significance[h]}</td></tr>'

    # Get full predictions
    career_html = get_full_career_analysis(kundali, planets_in_houses, house_rashis, RASHI_HINDI)
    marriage_html = get_full_marriage_analysis(kundali, planets_in_houses, house_rashis, RASHI_HINDI)
    children_html = get_full_children_analysis(kundali, planets_in_houses, house_rashis, RASHI_HINDI)
    health_html = get_full_health_analysis(kundali, planets_in_houses, house_rashis, RASHI_HINDI)
    wealth_html = get_full_wealth_analysis(kundali, planets_in_houses, house_rashis, RASHI_HINDI)
    dasha_html = get_full_dasha_analysis(kundali, mahadashas, current_dasha)
    yoga_html = get_full_yoga_analysis(kundali, planets_in_houses)
    remedies_html = get_full_remedies(kundali, planets_in_houses)

    # Get planetary strength analysis (Shadbala, Combustion, War, Navamsa)
    try:
        strength_html = get_planetary_strength_analysis(kundali)
    except Exception:
        strength_html = '<div class="detail-box"><p>Planetary strength analysis temporarily unavailable.</p></div>'

    # Get transit analysis (with graceful fallback)
    try:
        transit_html = get_full_transit_analysis(kundali, planets_in_houses, house_rashis, RASHI_HINDI)
    except Exception:
        transit_html = '<div class="detail-box"><p>Transit analysis temporarily unavailable.</p></div>'

    html = f'''
    <div class="results-header">
        <div style="font-size: 2.5em;">ॐ</div>
        <h2>विस्तृत जन्म कुंडली</h2>
        <h2>{birth.name}</h2>
    </div>

    <div class="section">
        <h2 class="section-title">🪔 जन्म विवरण (Birth Details)</h2>
        <div class="birth-grid">
            <div class="birth-item"><div class="label">नाम</div><div class="value">{birth.name}</div></div>
            <div class="birth-item"><div class="label">जन्म तिथि</div><div class="value">{birth.date.strftime('%d-%m-%Y')}</div></div>
            <div class="birth-item"><div class="label">जन्म समय</div><div class="value">{birth.date.strftime('%I:%M %p')}</div></div>
            <div class="birth-item"><div class="label">जन्म स्थान</div><div class="value">{birth.city}</div></div>
            <div class="birth-item"><div class="label">लग्न राशि</div><div class="value">{RASHI_HINDI.get(lagna['rashi'], lagna['rashi'])} ({lagna['rashi_english']})</div></div>
            <div class="birth-item"><div class="label">चंद्र राशि</div><div class="value">{RASHI_HINDI.get(planets['MOON']['rashi'], planets['MOON']['rashi'])}</div></div>
            <div class="birth-item"><div class="label">जन्म नक्षत्र</div><div class="value">{planets['MOON']['nakshatra']} पाद {planets['MOON']['pada']}</div></div>
            <div class="birth-item"><div class="label">वर्तमान दशा</div><div class="value">{current_dasha['full_dasha']}</div></div>
        </div>
    </div>

    <div class="section">
        <h2 class="section-title">📊 लग्न कुंडली (Birth Chart)</h2>
        {chart_html}
        <p style="text-align:center;color:#666;">(व) = वक्री | पीला = लग्न</p>
    </div>

    <div class="section">
        <h2 class="section-title">🏠 भाव चार्ट (House Analysis)</h2>
        <table class="detail-table">
            <tr><th>भाव</th><th>राशि</th><th>ग्रह</th><th>महत्व</th></tr>
            {bhava_rows}
        </table>
    </div>

    <div class="section">
        <h2 class="section-title">🌟 ग्रह स्थिति (Planet Positions)</h2>
        <table class="detail-table">
            <tr><th>ग्रह</th><th>राशि</th><th>अंश</th><th>नक्षत्र</th><th>भाव</th><th>गति</th></tr>
            {planet_rows}
        </table>
    </div>

    <div class="section">
        <h2 class="section-title">💼 करियर विस्तृत विश्लेषण (Career Analysis)</h2>
        {career_html}
    </div>

    <div class="section">
        <h2 class="section-title">💑 विवाह विस्तृत विश्लेषण (Marriage Analysis)</h2>
        {marriage_html}
    </div>

    <div class="section">
        <h2 class="section-title">👶 संतान विस्तृत विश्लेषण (Children Analysis)</h2>
        {children_html}
    </div>

    <div class="section">
        <h2 class="section-title">🏥 स्वास्थ्य विस्तृत विश्लेषण (Health Analysis)</h2>
        {health_html}
    </div>

    <div class="section">
        <h2 class="section-title">💰 धन विस्तृत विश्लेषण (Wealth Analysis)</h2>
        {wealth_html}
    </div>

    <div class="section">
        <h2 class="section-title">📅 दशा विस्तृत विश्लेषण (Dasha Analysis)</h2>
        {dasha_html}
    </div>

    <div class="section">
        <h2 class="section-title">🌍 गोचर एवं भविष्यवाणी (Transit & Predictions)</h2>
        {transit_html}
    </div>

    <div class="section">
        <h2 class="section-title">🔮 विशेष योग (Special Yogas)</h2>
        {yoga_html}
    </div>

    <div class="section">
        <h2 class="section-title">🔬 ग्रह बल विश्लेषण (Planetary Strength - BPHS)</h2>
        {strength_html}
    </div>

    <div class="section">
        <h2 class="section-title">✨ शुभ तत्व एवं उपाय (Remedies)</h2>
        {remedies_html}
    </div>

    <div class="section">
        <h2 class="section-title">📝 सारांश (Summary)</h2>
        <div class="summary-grid">
            <div class="summary-card"><div class="rating">{calculate_career_rating(planets_in_houses)}</div><strong>करियर</strong></div>
            <div class="summary-card"><div class="rating">{calculate_marriage_rating(planets_in_houses)}</div><strong>विवाह</strong></div>
            <div class="summary-card"><div class="rating">{calculate_children_rating(planets_in_houses)}</div><strong>संतान</strong></div>
            <div class="summary-card"><div class="rating">{calculate_health_rating(planets_in_houses)}</div><strong>स्वास्थ्य</strong></div>
            <div class="summary-card"><div class="rating">{calculate_wealth_rating(planets_in_houses)}</div><strong>धन</strong></div>
        </div>
    </div>

    <div class="footer">
        <p style="font-size:1.5em;">🙏 शुभम् भवतु 🙏</p>
        <p>Generated: {datetime.now().strftime('%d-%m-%Y %H:%M')}</p>
        <p>Swiss Ephemeris (NASA JPL DE431) | 99.9%+ Accuracy</p>
    </div>
    '''
    return html
