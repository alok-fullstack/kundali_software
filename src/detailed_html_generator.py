"""
Detailed Hindi Kundali HTML Generator
Complete predictions with all sections
"""

from datetime import datetime
from typing import Dict, List
import os

from .kundali import Kundali, create_kundali
from .config import RASHIS, PLANET_NAMES, Planet, BHAVA_NAMES
from .predictions import (
    GRAHA_BHAVA_PHAL, CAREER_BY_LAGNA, MARRIAGE_PREDICTIONS,
    CHILDREN_PREDICTIONS, HEALTH_PREDICTIONS
)
from .full_predictions import (
    get_lagna_specific_dasha_effect, get_full_career_analysis,
    get_full_marriage_analysis, get_full_children_analysis,
    get_full_health_analysis, get_full_wealth_analysis,
    get_full_dasha_analysis, get_full_yoga_analysis,
    get_full_remedies, get_planetary_strength_analysis
)

# Rashi lords mapping
RASHI_LORDS = {
    "Mesha": "Mars", "Vrishabha": "Venus", "Mithuna": "Mercury", "Karka": "Moon",
    "Simha": "Sun", "Kanya": "Mercury", "Tula": "Venus", "Vrishchika": "Mars",
    "Dhanu": "Jupiter", "Makara": "Saturn", "Kumbha": "Saturn", "Meena": "Jupiter"
}

def get_house_lord(house_num, lagna_name):
    """Get the lord of a house based on lagna."""
    rashi_order = ["Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
                   "Tula", "Vrishchika", "Dhanu", "Makara", "Kumbha", "Meena"]
    lagna_idx = rashi_order.index(lagna_name)
    house_rashi = rashi_order[(lagna_idx + house_num - 1) % 12]
    return RASHI_LORDS[house_rashi]


def generate_detailed_kundali_html(kundali: Kundali, output_path: str = None) -> str:
    """Generate comprehensive Hindi Kundali HTML with all details."""

    # Get all data
    planets = kundali.planets
    lagna = kundali.lagna
    planets_in_houses = kundali.get_planets_in_houses()
    mahadashas = kundali.get_mahadashas(years=100)
    current_dasha = kundali.get_current_dasha()

    # Calculate house rashis
    lagna_num = lagna["rashi_num"]
    house_rashis = {}
    for i in range(1, 13):
        rashi_num = (lagna_num + i - 1) % 12
        house_rashis[i] = RASHIS[rashi_num]

    # Birth details
    birth = kundali.birth_data
    name = birth.name

    # Rashi names in Hindi
    rashi_hindi = {
        "Mesha": "मेष", "Vrishabha": "वृषभ", "Mithuna": "मिथुन", "Karka": "कर्क",
        "Simha": "सिंह", "Kanya": "कन्या", "Tula": "तुला", "Vrishchika": "वृश्चिक",
        "Dhanu": "धनु", "Makara": "मकर", "Kumbha": "कुंभ", "Meena": "मीन"
    }

    html = f"""<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>विस्तृत जन्म कुंडली - {name}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;500;600;700&display=swap');

        :root {{
            --primary: #ff6b35;
            --secondary: #8b4513;
            --accent: #f7931e;
            --success: #28a745;
            --warning: #ffc107;
            --danger: #dc3545;
            --light: #fff8f0;
            --dark: #333;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Noto Sans Devanagari', sans-serif;
            background: linear-gradient(135deg, #fff5e6 0%, #ffe4c4 100%);
            min-height: 100vh;
            padding: 20px;
            color: var(--dark);
            line-height: 1.8;
        }}

        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        .header .om {{
            font-size: 4em;
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .header .name {{
            font-size: 1.8em;
            opacity: 0.95;
            margin-top: 10px;
        }}

        .section {{
            padding: 30px;
            border-bottom: 1px solid #eee;
        }}

        .section:last-child {{
            border-bottom: none;
        }}

        .section-title {{
            color: var(--primary);
            font-size: 1.6em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid var(--primary);
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .section-title .icon {{
            font-size: 1.2em;
        }}

        /* Birth Details Grid */
        .birth-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}

        .birth-item {{
            background: var(--light);
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid var(--primary);
        }}

        .birth-item .label {{
            color: #666;
            font-size: 0.9em;
        }}

        .birth-item .value {{
            font-size: 1.1em;
            font-weight: 600;
            color: var(--dark);
            margin-top: 5px;
        }}

        /* Tables */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}

        th {{
            background: var(--primary);
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}

        td {{
            padding: 12px;
            border-bottom: 1px solid #eee;
        }}

        tr:nth-child(even) {{
            background: var(--light);
        }}

        tr:hover {{
            background: #ffe4c4;
        }}

        /* Prediction Cards */
        .prediction-card {{
            background: linear-gradient(135deg, var(--light) 0%, #ffe4c4 100%);
            border-radius: 15px;
            padding: 20px;
            margin: 15px 0;
            border-left: 5px solid var(--primary);
        }}

        .prediction-card h3 {{
            color: var(--secondary);
            margin-bottom: 15px;
            font-size: 1.2em;
        }}

        .prediction-card ul {{
            list-style: none;
            padding: 0;
        }}

        .prediction-card li {{
            padding: 8px 0;
            padding-left: 25px;
            position: relative;
        }}

        .prediction-card li::before {{
            content: "•";
            color: var(--primary);
            font-weight: bold;
            position: absolute;
            left: 5px;
        }}

        /* Status indicators */
        .status-good {{
            color: var(--success);
            font-weight: 600;
        }}

        .status-warning {{
            color: var(--warning);
            font-weight: 600;
        }}

        .status-caution {{
            color: var(--danger);
            font-weight: 600;
        }}

        /* Rating stars */
        .rating {{
            color: var(--accent);
            font-size: 1.2em;
        }}

        /* Highlight boxes */
        .highlight-box {{
            background: linear-gradient(135deg, #fff3cd 0%, #ffeeba 100%);
            border: 2px solid var(--warning);
            border-radius: 10px;
            padding: 15px;
            margin: 15px 0;
        }}

        .highlight-box.success {{
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            border-color: var(--success);
        }}

        .highlight-box.danger {{
            background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
            border-color: var(--danger);
        }}

        /* Kundali Chart */
        .chart-container {{
            display: flex;
            justify-content: center;
            margin: 20px 0;
        }}

        .chart-table {{
            border-collapse: collapse;
        }}

        .chart-table td {{
            width: 100px;
            height: 100px;
            border: 2px solid var(--secondary);
            background: var(--light);
            vertical-align: top;
            padding: 8px;
            font-size: 0.85em;
        }}

        .chart-table .rashi-name {{
            color: var(--primary);
            font-weight: 600;
            font-size: 0.9em;
        }}

        .chart-table .house-num {{
            color: #666;
            font-size: 0.75em;
        }}

        .chart-table .planets {{
            margin-top: 5px;
            font-size: 0.9em;
        }}

        .chart-table .lagna-house {{
            background: #fff3cd;
            border: 3px solid var(--primary);
        }}

        /* Timeline */
        .timeline {{
            position: relative;
            padding-left: 30px;
        }}

        .timeline::before {{
            content: '';
            position: absolute;
            left: 10px;
            top: 0;
            bottom: 0;
            width: 3px;
            background: var(--primary);
        }}

        .timeline-item {{
            position: relative;
            padding: 15px;
            margin-bottom: 15px;
            background: var(--light);
            border-radius: 10px;
        }}

        .timeline-item::before {{
            content: '';
            position: absolute;
            left: -24px;
            top: 20px;
            width: 12px;
            height: 12px;
            background: var(--primary);
            border-radius: 50%;
        }}

        .timeline-item.current {{
            background: #fff3cd;
            border: 2px solid var(--warning);
        }}

        .timeline-item.current::before {{
            background: var(--warning);
            width: 16px;
            height: 16px;
            left: -26px;
        }}

        /* Summary Grid */
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 15px;
        }}

        .summary-card {{
            background: var(--light);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border-top: 4px solid var(--primary);
        }}

        .summary-card .title {{
            font-weight: 600;
            margin-bottom: 10px;
        }}

        .summary-card .rating {{
            font-size: 1.5em;
            margin-bottom: 5px;
        }}

        /* Footer */
        .footer {{
            background: var(--dark);
            color: white;
            padding: 25px;
            text-align: center;
        }}

        .footer p {{
            margin: 5px 0;
            opacity: 0.9;
        }}

        .disclaimer {{
            background: #fff3cd;
            border: 1px solid var(--warning);
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            font-size: 0.9em;
        }}

        /* Yoga Section */
        .yoga-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }}

        .yoga-card {{
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            border-radius: 10px;
            padding: 15px;
            border-left: 4px solid var(--success);
        }}

        .yoga-card h4 {{
            color: var(--success);
            margin-bottom: 10px;
        }}

        @media print {{
            body {{ background: white; }}
            .container {{ box-shadow: none; }}
        }}

        @media (max-width: 600px) {{
            .header h1 {{ font-size: 1.8em; }}
            .section {{ padding: 20px; }}
            .chart-table td {{ width: 70px; height: 70px; font-size: 0.7em; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <div class="om">ॐ</div>
            <h1>॥ श्री गणेशाय नमः ॥</h1>
            <h1>विस्तृत जन्म कुंडली</h1>
            <p class="name">{name}</p>
        </div>

        <!-- Birth Details Section -->
        <div class="section">
            <h2 class="section-title"><span class="icon">🪔</span> जन्म विवरण</h2>
            <div class="birth-grid">
                <div class="birth-item">
                    <div class="label">नाम</div>
                    <div class="value">{name}</div>
                </div>
                <div class="birth-item">
                    <div class="label">जन्म तिथि</div>
                    <div class="value">{birth.date.strftime('%d-%m-%Y')}</div>
                </div>
                <div class="birth-item">
                    <div class="label">जन्म समय</div>
                    <div class="value">{birth.date.strftime('%H:%M:%S')}</div>
                </div>
                <div class="birth-item">
                    <div class="label">जन्म स्थान</div>
                    <div class="value">{birth.city}</div>
                </div>
                <div class="birth-item">
                    <div class="label">लग्न राशि</div>
                    <div class="value">{rashi_hindi.get(lagna['rashi'], lagna['rashi'])} ({lagna['rashi_english']})</div>
                </div>
                <div class="birth-item">
                    <div class="label">चंद्र राशि</div>
                    <div class="value">{rashi_hindi.get(planets['MOON']['rashi'], planets['MOON']['rashi'])}</div>
                </div>
                <div class="birth-item">
                    <div class="label">जन्म नक्षत्र</div>
                    <div class="value">{planets['MOON']['nakshatra']} पाद {planets['MOON']['pada']}</div>
                </div>
                <div class="birth-item">
                    <div class="label">वर्तमान दशा</div>
                    <div class="value">{current_dasha['full_dasha']}</div>
                </div>
            </div>
        </div>

        <!-- Kundali Chart Section -->
        <div class="section">
            <h2 class="section-title"><span class="icon">📊</span> लग्न कुंडली</h2>
            {generate_south_indian_chart(kundali, planets_in_houses, lagna_num, rashi_hindi)}
            <p style="text-align: center; color: #666; margin-top: 10px;">
                (व) = वक्री (Retrograde) | पीला बॉक्स = लग्न भाव
            </p>
        </div>

        <!-- Bhava Chart Section -->
        <div class="section">
            <h2 class="section-title"><span class="icon">🏠</span> भाव चार्ट (House Chart)</h2>
            <table>
                <thead>
                    <tr>
                        <th>भाव</th>
                        <th>राशि</th>
                        <th>ग्रह</th>
                        <th>महत्व</th>
                    </tr>
                </thead>
                <tbody>
                    {generate_bhava_rows(planets_in_houses, house_rashis, rashi_hindi)}
                </tbody>
            </table>
        </div>

        <!-- Planet Positions Section -->
        <div class="section">
            <h2 class="section-title"><span class="icon">🌟</span> ग्रह स्थिति (Planetary Positions)</h2>
            <table>
                <thead>
                    <tr>
                        <th>ग्रह</th>
                        <th>राशि</th>
                        <th>अंश</th>
                        <th>नक्षत्र</th>
                        <th>भाव</th>
                        <th>स्थिति</th>
                    </tr>
                </thead>
                <tbody>
                    {generate_planet_table_rows(kundali, planets_in_houses, rashi_hindi)}
                </tbody>
            </table>
        </div>

        <!-- Career Section -->
        <div class="section">
            <h2 class="section-title"><span class="icon">💼</span> करियर एवं व्यवसाय (Career Analysis)</h2>
            {generate_career_section(kundali, planets_in_houses, house_rashis, current_dasha, rashi_hindi)}
        </div>

        <!-- Marriage Section -->
        <div class="section">
            <h2 class="section-title"><span class="icon">💑</span> विवाह एवं दाम्पत्य (Marriage Analysis)</h2>
            {generate_marriage_section(kundali, planets_in_houses, house_rashis, rashi_hindi)}
        </div>

        <!-- Children Section -->
        <div class="section">
            <h2 class="section-title"><span class="icon">👶</span> संतान (Children Analysis)</h2>
            {generate_children_section(kundali, planets_in_houses, house_rashis, rashi_hindi)}
        </div>

        <!-- Health Section -->
        <div class="section">
            <h2 class="section-title"><span class="icon">🏥</span> स्वास्थ्य (Health Analysis)</h2>
            {generate_health_section(kundali, planets_in_houses, rashi_hindi)}
        </div>

        <!-- Wealth Section -->
        <div class="section">
            <h2 class="section-title"><span class="icon">💰</span> धन एवं संपत्ति (Wealth Analysis)</h2>
            {generate_wealth_section(kundali, planets_in_houses, house_rashis, rashi_hindi)}
        </div>

        <!-- Dasha Section -->
        <div class="section" id="dasha-section">
            <h2 class="section-title"><span class="icon">📅</span> दशा विश्लेषण (Dasha Analysis)</h2>
            {generate_dasha_section(kundali, mahadashas, current_dasha)}
        </div>

        <!-- Special Yogas Section -->
        <div class="section">
            <h2 class="section-title"><span class="icon">🔮</span> विशेष योग (Special Yogas)</h2>
            {generate_yoga_section(kundali, planets_in_houses)}
        </div>

        <!-- Summary Section -->
        <div class="section">
            <h2 class="section-title"><span class="icon">📝</span> सारांश एवं सुझाव (Summary & Recommendations)</h2>
            {generate_summary_section(kundali, planets_in_houses, current_dasha)}
        </div>

        <!-- Disclaimer -->
        <div class="section">
            <div class="disclaimer">
                <strong>⚠️ अस्वीकरण (Disclaimer):</strong><br>
                यह कुंडली केवल सूचनात्मक उद्देश्यों के लिए है। ज्योतिष एक प्राचीन विद्या है और इसके परिणाम व्यक्ति के कर्मों पर भी निर्भर करते हैं।
                महत्वपूर्ण निर्णयों के लिए किसी अनुभवी ज्योतिषी से परामर्श लें।<br><br>
                <strong>सटीकता (Accuracy):</strong> यह सॉफ्टवेयर Swiss Ephemeris (NASA JPL DE431) पर आधारित है
                जो 0.001 arc-second (sub-milli-arc-second) की सटीकता प्रदान करता है।
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <p style="font-size: 1.5em;">🙏 शुभम् भवतु 🙏</p>
            <p>Generated: {datetime.now().strftime('%d-%m-%Y %H:%M')}</p>
            <p>Powered by Swiss Ephemeris (NASA JPL DE431)</p>
            <p>Kundali Software v1.1 | Sub-Arc-Second Precision</p>
        </div>
    </div>
</body>
</html>"""

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Detailed Kundali HTML generated: {output_path}")

    return html


def generate_south_indian_chart(kundali, planets_in_houses, lagna_num, rashi_hindi):
    """Generate South Indian style chart."""
    rashi_positions = [
        [12, 1, 2, 3],
        [11, 0, 0, 4],
        [10, 0, 0, 5],
        [9, 8, 7, 6]
    ]

    rashi_names = {
        1: "मेष", 2: "वृषभ", 3: "मिथुन", 4: "कर्क",
        5: "सिंह", 6: "कन्या", 7: "तुला", 8: "वृश्चिक",
        9: "धनु", 10: "मकर", 11: "कुंभ", 12: "मीन"
    }

    html = '<div class="chart-container"><table class="chart-table">'

    for row in rashi_positions:
        html += "<tr>"
        for rashi_num in row:
            if rashi_num == 0:
                html += '<td style="background: linear-gradient(135deg, #fff8dc, #ffe4b5);"></td>'
            else:
                house_num = ((rashi_num - lagna_num - 1) % 12) + 1
                house_planets = planets_in_houses.get(house_num, [])

                planet_str = ""
                for p in house_planets:
                    symbol = PLANET_NAMES[Planet[p]]["symbol"]
                    is_retro = kundali.planets[p]["is_retrograde"]
                    retro_mark = "(व)" if is_retro else ""
                    planet_str += f"{symbol}{retro_mark} "

                is_lagna = house_num == 1
                cell_class = 'class="lagna-house"' if is_lagna else ''

                html += f'''
                <td {cell_class}>
                    <div class="rashi-name">{rashi_names[rashi_num]}</div>
                    <div class="house-num">भाव {house_num}</div>
                    <div class="planets">{planet_str}</div>
                </td>'''
        html += "</tr>"

    html += "</table></div>"
    return html


def generate_bhava_rows(planets_in_houses, house_rashis, rashi_hindi):
    """Generate bhava table rows."""
    bhava_significance = {
        1: "आत्म, व्यक्तित्व, शरीर",
        2: "धन, परिवार, वाणी",
        3: "भाई-बहन, साहस, संचार",
        4: "माता, घर, सुख, वाहन",
        5: "संतान, बुद्धि, शिक्षा",
        6: "शत्रु, रोग, ऋण",
        7: "विवाह, साझेदारी",
        8: "आयु, बाधाएं, रहस्य",
        9: "भाग्य, पिता, धर्म",
        10: "करियर, कर्म, यश",
        11: "लाभ, आय, मित्र",
        12: "व्यय, मोक्ष, विदेश"
    }

    rows = ""
    for h in range(1, 13):
        planets = planets_in_houses.get(h, [])
        rashi = house_rashis[h]
        rashi_name = rashi_hindi.get(rashi['name'], rashi['name'])

        planet_symbols = []
        for p in planets:
            symbol = PLANET_NAMES[Planet[p]]["symbol"]
            hindi = PLANET_NAMES[Planet[p]]["hindi"]
            planet_symbols.append(f"{symbol} {hindi}")

        rows += f"""
        <tr>
            <td><strong>{h}</strong> ({BHAVA_NAMES[h]['name']})</td>
            <td>{rashi_name}</td>
            <td>{', '.join(planet_symbols) if planet_symbols else '-'}</td>
            <td>{bhava_significance[h]}</td>
        </tr>"""

    return rows


def generate_planet_table_rows(kundali, planets_in_houses, rashi_hindi):
    """Generate planet position table rows."""
    planet_order = ["SUN", "MOON", "MARS", "MERCURY", "JUPITER", "VENUS", "SATURN", "RAHU", "KETU"]
    rows = ""

    for p_name in planet_order:
        data = kundali.planets[p_name]
        hindi = PLANET_NAMES[Planet[p_name]]["hindi"]
        symbol = PLANET_NAMES[Planet[p_name]]["symbol"]
        rashi = rashi_hindi.get(data['rashi'], data['rashi'])

        house = 0
        for h, planets in planets_in_houses.items():
            if p_name in planets:
                house = h
                break

        retro_class = 'class="status-caution"' if data["is_retrograde"] else 'class="status-good"'
        retro_text = "वक्री" if data["is_retrograde"] else "मार्गी"

        rows += f"""
        <tr>
            <td>{symbol} {hindi}</td>
            <td>{rashi}</td>
            <td>{data['rashi_degree']:.2f}°</td>
            <td>{data['nakshatra']} पाद {data['pada']}</td>
            <td>{house}</td>
            <td {retro_class}>{retro_text}</td>
        </tr>"""

    return rows


def generate_career_section(kundali, planets_in_houses, house_rashis, current_dasha, rashi_hindi):
    """Generate detailed career analysis section."""
    lagna = kundali.lagna['rashi']
    tenth_rashi = house_rashis[10]['name']
    tenth_planets = planets_in_houses.get(10, [])
    second_planets = planets_in_houses.get(2, [])

    html = f"""
    <div class="prediction-card">
        <h3>लग्न आधारित करियर विश्लेषण</h3>
        <p><strong>लग्न राशि:</strong> {rashi_hindi.get(lagna, lagna)}</p>
        <p><strong>उपयुक्त क्षेत्र:</strong> {CAREER_BY_LAGNA.get(lagna, 'विविध क्षेत्र')}</p>
    </div>

    <div class="prediction-card">
        <h3>दशम भाव (करियर स्थान) - {rashi_hindi.get(tenth_rashi, tenth_rashi)}</h3>
    """

    if tenth_planets:
        html += "<ul>"
        for p in tenth_planets:
            hindi = PLANET_NAMES[Planet[p]]["hindi"]
            html += f"<li><strong>{hindi}:</strong> {GRAHA_BHAVA_PHAL[p][10]}</li>"
        html += "</ul>"
    else:
        html += "<p>दशम भाव खाली है - दशमेश की स्थिति महत्वपूर्ण है।</p>"

    html += "</div>"

    if second_planets:
        html += f"""
        <div class="highlight-box success">
            <h3>🌟 विशेष धन योग - द्वितीय भाव में {len(second_planets)} ग्रह!</h3>
            <p>यह बहुत शक्तिशाली योग है जो Multiple Income Sources देता है:</p>
            <ul>
        """
        for p in second_planets:
            hindi = PLANET_NAMES[Planet[p]]["hindi"]
            html += f"<li><strong>{hindi}:</strong> {GRAHA_BHAVA_PHAL[p][2]}</li>"
        html += "</ul></div>"

    # Career timing - dynamic based on chart
    maha = current_dasha['mahadasha']['planet']
    lagna_name = kundali.lagna['rashi']
    dasha_effect = get_lagna_specific_dasha_effect(maha, lagna_name)

    html += f"""
    <div class="prediction-card">
        <h3>करियर समय विश्लेषण</h3>
        <p><strong>वर्तमान {maha} महादशा:</strong></p>
        <p>{dasha_effect['effect']}</p>
        <p><strong>कारण:</strong> {dasha_effect['reason']}</p>
        <p><em>विस्तृत समय के लिए नीचे दशा विश्लेषण खंड देखें। / See Dasha section below for detailed timing.</em></p>
    </div>
    """

    return html


def generate_marriage_section(kundali, planets_in_houses, house_rashis, rashi_hindi):
    """Generate detailed marriage analysis section."""
    seventh_rashi = house_rashis[7]['name']
    seventh_planets = planets_in_houses.get(7, [])

    venus_house = None
    for h, planets in planets_in_houses.items():
        if "VENUS" in planets:
            venus_house = h
            break

    html = f"""
    <div class="prediction-card">
        <h3>सप्तम भाव (विवाह स्थान) - {rashi_hindi.get(seventh_rashi, seventh_rashi)}</h3>
        <p>{MARRIAGE_PREDICTIONS.get(seventh_rashi, '')}</p>
    """

    if seventh_planets:
        html += "<h4>सप्तम भाव में ग्रह:</h4><ul>"
        for p in seventh_planets:
            hindi = PLANET_NAMES[Planet[p]]["hindi"]
            html += f"<li><strong>{hindi}:</strong> {GRAHA_BHAVA_PHAL[p][7]}</li>"
        html += "</ul>"

    html += "</div>"

    if venus_house:
        html += f"""
        <div class="prediction-card">
            <h3>शुक्र (विवाह कारक) - भाव {venus_house}</h3>
            <p>{GRAHA_BHAVA_PHAL['VENUS'][venus_house]}</p>
        </div>
        """

    # Dynamic marriage timing based on actual dasha from chart
    lagna_name = kundali.lagna['rashi']
    seventh_lord = get_house_lord(7, lagna_name)
    moon_house = None
    for h, planets in planets_in_houses.items():
        if "MOON" in planets:
            moon_house = h
            break

    html += f"""
    <div class="prediction-card">
        <h3>विवाह समय विश्लेषण</h3>
        <p><strong>सप्तम भाव का स्वामी:</strong> {seventh_lord}</p>
    """

    # Add relevant predictions based on actual planets
    predictions = []
    if venus_house:
        predictions.append(f"<li><span class='status-good'>✅</span> शुक्र भाव {venus_house} में - {GRAHA_BHAVA_PHAL['VENUS'][venus_house]}</li>")

    if seventh_planets:
        for p in seventh_planets:
            effect = get_lagna_specific_dasha_effect(p, lagna_name)
            status = "status-good" if effect['is_benefic'] else "status-warning"
            icon = "✅" if effect['is_benefic'] else "⚠️"
            predictions.append(f"<li><span class='{status}'>{icon}</span> {p} सप्तम में - {effect['effect']}</li>")

    if moon_house:
        moon_effect = get_lagna_specific_dasha_effect("Moon", lagna_name)
        predictions.append(f"<li><span class='status-{'good' if moon_effect['is_benefic'] else 'warning'}'>{'✅' if moon_effect['is_benefic'] else '⚠️'}</span> चंद्र भाव {moon_house} में</li>")

    if predictions:
        html += "<h4>विवाह भविष्यवाणी:</h4><ul>" + "".join(predictions) + "</ul>"

    html += "<p><em>विस्तृत समय के लिए नीचे दशा विश्लेषण खंड देखें। / See Dasha section below for detailed timing.</em></p>"
    html += "</div>"
    return html


def generate_children_section(kundali, planets_in_houses, house_rashis, rashi_hindi):
    """Generate detailed children analysis section."""
    fifth_rashi = house_rashis[5]['name']
    fifth_planets = planets_in_houses.get(5, [])

    html = f"""
    <div class="prediction-card">
        <h3>पंचम भाव (संतान स्थान) - {rashi_hindi.get(fifth_rashi, fifth_rashi)}</h3>
        <p>{CHILDREN_PREDICTIONS.get(fifth_rashi, '')}</p>
    """

    if fifth_planets:
        html += "<h4>पंचम भाव में ग्रह:</h4><ul>"
        for p in fifth_planets:
            hindi = PLANET_NAMES[Planet[p]]["hindi"]
            html += f"<li><strong>{hindi}:</strong> {GRAHA_BHAVA_PHAL[p][5]}</li>"
        html += "</ul>"

    html += "</div>"

    # Dynamic children predictions based on actual chart
    lagna_name = kundali.lagna['rashi']
    fifth_lord = get_house_lord(5, lagna_name)
    fifth_lord_effect = get_lagna_specific_dasha_effect(fifth_lord, lagna_name)

    html += f"""
    <div class="prediction-card">
        <h3>संतान भविष्यवाणी</h3>
        <p><strong>पंचम भाव का स्वामी:</strong> {fifth_lord} - {fifth_lord_effect['effect']}</p>
        <ul>
    """

    # Check what's actually in 5th house
    if "SATURN" in fifth_planets:
        saturn_effect = get_lagna_specific_dasha_effect("Saturn", lagna_name)
        if saturn_effect['is_benefic']:
            html += "<li><span class='status-good'>✅</span> शनि पंचम में - अनुशासित और जिम्मेदार संतान</li>"
        else:
            html += "<li><span class='status-warning'>⏰</span> शनि पंचम में - संतान में देरी संभव</li>"

    if "JUPITER" in fifth_planets:
        jupiter_effect = get_lagna_specific_dasha_effect("Jupiter", lagna_name)
        if jupiter_effect['is_benefic']:
            html += "<li><span class='status-good'>✅</span> गुरु पंचम में - संतान बुद्धिमान और धार्मिक होगी</li>"

    if "MARS" in fifth_planets:
        mars_effect = get_lagna_specific_dasha_effect("Mars", lagna_name)
        status = "status-good" if mars_effect['is_benefic'] else "status-warning"
        icon = "✅" if mars_effect['is_benefic'] else "⚠️"
        html += f"<li><span class='{status}'>{icon}</span> मंगल पंचम में - {mars_effect['effect']}</li>"

    # 5th lord status
    html += f"<li><span class='status-{'good' if fifth_lord_effect['is_benefic'] else 'warning'}'>{'✅' if fifth_lord_effect['is_benefic'] else '⚠️'}</span> पंचमेश {fifth_lord} - {fifth_lord_effect['reason']}</li>"

    html += "</ul>"
    html += "<p><em>विस्तृत समय के लिए नीचे दशा विश्लेषण खंड देखें। / See Dasha section below for detailed timing.</em></p>"
    html += "</div>"
    return html


def generate_health_section(kundali, planets_in_houses, rashi_hindi):
    """Generate detailed health analysis section based on actual chart."""
    lagna = kundali.lagna['rashi']
    sixth_planets = planets_in_houses.get(6, [])

    # Prakriti (constitution) based on lagna
    PRAKRITI_BY_LAGNA = {
        "Mesha": ("Pitta", "पित्त प्रकृति - अग्नि तत्व प्रधान, शरीर में गर्मी"),
        "Vrishabha": ("Kapha", "कफ प्रकृति - जल/पृथ्वी तत्व, शांत स्वभाव"),
        "Mithuna": ("Vata", "वात प्रकृति - वायु तत्व, चंचल मन"),
        "Karka": ("Kapha", "कफ प्रकृति - जल तत्व प्रधान"),
        "Simha": ("Pitta", "पित्त प्रकृति - अग्नि तत्व, नेतृत्व"),
        "Kanya": ("Vata", "वात प्रकृति - वायु/पृथ्वी तत्व, विश्लेषणात्मक"),
        "Tula": ("Vata", "वात प्रकृति - वायु तत्व, संतुलन प्रिय"),
        "Vrishchika": ("Pitta", "पित्त प्रकृति - जल/अग्नि तत्व"),
        "Dhanu": ("Pitta", "पित्त प्रकृति - अग्नि तत्व"),
        "Makara": ("Vata", "वात प्रकृति - पृथ्वी/वायु तत्व"),
        "Kumbha": ("Vata", "वात प्रकृति - वायु तत्व प्रधान"),
        "Meena": ("Kapha", "कफ प्रकृति - जल तत्व प्रधान")
    }

    prakriti, prakriti_desc = PRAKRITI_BY_LAGNA.get(lagna, ("Mixed", "मिश्र प्रकृति"))

    html = f"""
    <div class="prediction-card">
        <h3>लग्न आधारित स्वास्थ्य</h3>
        <p><strong>{rashi_hindi.get(lagna, lagna)} लग्न:</strong> {HEALTH_PREDICTIONS.get(lagna, '')}</p>
        <p><strong>आयुर्वेदिक प्रकृति:</strong> {prakriti_desc}</p>
    </div>
    """

    # Dynamic health table based on actual planets
    html += """<div class="prediction-card"><h3>स्वास्थ्य संवेदनशील क्षेत्र</h3><table><tr><th>अंग/क्षेत्र</th><th>सावधानी</th></tr>"""

    # Find Moon's house for mental health
    moon_house = None
    mars_house = None
    for h, planets in planets_in_houses.items():
        if "MOON" in planets:
            moon_house = h
        if "MARS" in planets:
            mars_house = h

    # Add lagna-specific health concerns
    health_concerns = {
        "Mesha": ("सिर/मस्तिष्क", "सिरदर्द, बुखार से बचें"),
        "Vrishabha": ("गला/थायरॉइड", "गले की समस्याओं का ध्यान"),
        "Mithuna": ("फेफड़े/हाथ", "श्वास संबंधी सावधानी"),
        "Karka": ("छाती/पेट", "पाचन का ध्यान रखें"),
        "Simha": ("हृदय", "हृदय स्वास्थ्य का ध्यान"),
        "Kanya": ("आंतें", "पाचन तंत्र संवेदनशील"),
        "Tula": ("किडनी", "किडनी का ध्यान रखें"),
        "Vrishchika": ("प्रजनन अंग", "गुप्त रोगों से बचाव"),
        "Dhanu": ("जांघ/यकृत", "यकृत स्वास्थ्य"),
        "Makara": ("घुटने/जोड़", "जोड़ों का ध्यान"),
        "Kumbha": ("टखने/रक्त", "रक्त संचार"),
        "Meena": ("पैर", "पैरों की देखभाल")
    }

    area, concern = health_concerns.get(lagna, ("सामान्य", "संतुलित आहार"))
    html += f"<tr><td>{area}</td><td>{concern}</td></tr>"

    if moon_house in [6, 8, 12]:
        html += f"<tr><td>मानसिक स्वास्थ्य</td><td>चंद्र भाव {moon_house} में - तनाव प्रबंधन जरूरी</td></tr>"

    if mars_house in [6, 8]:
        html += f"<tr><td>चोट/शल्य</td><td>मंगल भाव {mars_house} में - सर्जरी/चोट से सावधान</td></tr>"

    html += "</table></div>"

    if sixth_planets:
        html += """<div class="prediction-card"><h3>षष्ठ भाव (रोग स्थान) में ग्रह</h3><ul>"""
        for p in sixth_planets:
            hindi = PLANET_NAMES[Planet[p]]["hindi"]
            html += f"<li><strong>{hindi}:</strong> {GRAHA_BHAVA_PHAL[p][6]}</li>"
        html += "</ul></div>"

    # Dynamic health suggestions based on actual chart
    html += """<div class="highlight-box"><h3>🧘 स्वास्थ्य सुझाव</h3><ul>"""

    if moon_house in [6, 8, 12]:
        html += f"<li>योग और ध्यान नियमित करें (चंद्र {moon_house} भाव में)</li>"

    if prakriti == "Vata":
        html += "<li>गर्म और तैलीय भोजन लें (वात प्रकृति के लिए)</li>"
    elif prakriti == "Pitta":
        html += "<li>ठंडे और मधुर भोजन लें (पित्त प्रकृति के लिए)</li>"
    else:
        html += "<li>हल्का और गर्म भोजन लें (कफ प्रकृति के लिए)</li>"

    html += "<li>पानी पर्याप्त पिएं</li>"

    if mars_house:
        mars_effect = get_lagna_specific_dasha_effect("Mars", lagna)
        if not mars_effect['is_benefic']:
            html += f"<li>Regular exercise - मंगल भाव {mars_house} में</li>"

    html += "</ul></div>"
    return html


def generate_wealth_section(kundali, planets_in_houses, house_rashis, rashi_hindi):
    """Generate detailed wealth analysis section."""
    second_planets = planets_in_houses.get(2, [])
    eleventh_planets = planets_in_houses.get(11, [])

    html = """
    <div class="prediction-card">
        <h3>द्वितीय भाव (धन स्थान)</h3>
    """

    if second_planets:
        html += f"""
        <div class="highlight-box success">
            <strong>🌟 {len(second_planets)} ग्रह धन भाव में - उत्तम धन योग!</strong>
        </div>
        <table>
            <tr><th>ग्रह</th><th>धन स्रोत</th></tr>
        """
        wealth_sources = {
            "SUN": "Government, Authority positions",
            "MOON": "Public dealing, Liquids",
            "MARS": "Technical work, Property, Real Estate",
            "MERCURY": "Business, Communication, IT",
            "JUPITER": "Teaching, Consulting, Finance, Law",
            "VENUS": "Arts, Entertainment, Luxury",
            "SATURN": "Labor, Mining, Agriculture",
            "RAHU": "Foreign, Unconventional",
            "KETU": "Spiritual, Occult"
        }
        for p in second_planets:
            hindi = PLANET_NAMES[Planet[p]]["hindi"]
            html += f"<tr><td>{hindi}</td><td>{wealth_sources.get(p, '')}</td></tr>"
        html += "</table>"

    html += "</div>"

    # Dynamic wealth predictions based on actual chart
    lagna_name = kundali.lagna['rashi']
    second_lord = get_house_lord(2, lagna_name)
    eleventh_lord = get_house_lord(11, lagna_name)

    # Find actual planet positions
    saturn_house = None
    mars_house = None
    moon_house = None
    for h, planets in planets_in_houses.items():
        if "SATURN" in planets:
            saturn_house = h
        if "MARS" in planets:
            mars_house = h
        if "MOON" in planets:
            moon_house = h

    html += """<div class="prediction-card"><h3>धन भविष्यवाणी</h3><ul>"""

    # 2nd lord analysis
    second_lord_effect = get_lagna_specific_dasha_effect(second_lord, lagna_name)
    status = "status-good" if second_lord_effect['is_benefic'] else "status-warning"
    icon = "💰" if second_lord_effect['is_benefic'] else "⚠️"
    html += f"<li><span class='{status}'>{icon}</span> द्वितीयेश {second_lord} - {second_lord_effect['reason']}</li>"

    # 11th lord analysis
    eleventh_lord_effect = get_lagna_specific_dasha_effect(eleventh_lord, lagna_name)
    status = "status-good" if eleventh_lord_effect['is_benefic'] else "status-warning"
    icon = "📈" if eleventh_lord_effect['is_benefic'] else "⚠️"
    html += f"<li><span class='{status}'>{icon}</span> एकादशेश {eleventh_lord} - {eleventh_lord_effect['reason']}</li>"

    # Property yoga - only if Saturn/Mars in relevant houses
    if saturn_house in [4, 5, 10] or mars_house in [2, 4]:
        positions = []
        if saturn_house in [4, 5, 10]:
            positions.append(f"शनि भाव {saturn_house}")
        if mars_house in [2, 4]:
            positions.append(f"मंगल भाव {mars_house}")
        html += f"<li><span class='status-good'>🏠</span> Property योग - {', '.join(positions)}</li>"

    # Multiple income if 2nd house has planets
    if len(second_planets) > 1:
        html += f"<li><span class='status-good'>💼</span> Multiple income sources - {len(second_planets)} ग्रह धन भाव में</li>"

    # Expense warning only if Moon in 6/8/12
    if moon_house in [6, 8, 12]:
        html += f"<li><span class='status-warning'>⚠️</span> खर्चों पर नियंत्रण - चंद्र भाव {moon_house} में</li>"

    html += "</ul>"
    html += "<p><em>विस्तृत समय के लिए नीचे दशा विश्लेषण खंड देखें। / See Dasha section below for detailed timing.</em></p>"
    html += "</div>"
    return html


def generate_dasha_section(kundali, mahadashas, current_dasha):
    """Generate detailed dasha analysis section based on actual chart."""
    lagna_name = kundali.lagna['rashi']

    html = f"""
    <div class="prediction-card">
        <h3>वर्तमान दशा</h3>
        <table>
            <tr><th>स्तर</th><th>ग्रह</th><th>आरंभ</th><th>समाप्ति</th></tr>
            <tr class="current">
                <td>महादशा</td>
                <td><strong>{current_dasha['mahadasha']['planet']}</strong></td>
                <td>{current_dasha['mahadasha']['start'].strftime('%d-%m-%Y')}</td>
                <td>{current_dasha['mahadasha']['end'].strftime('%d-%m-%Y')}</td>
            </tr>
            <tr>
                <td>अंतर्दशा</td>
                <td>{current_dasha['antardasha']['planet']}</td>
                <td>{current_dasha['antardasha']['start'].strftime('%d-%m-%Y')}</td>
                <td>{current_dasha['antardasha']['end'].strftime('%d-%m-%Y')}</td>
            </tr>
            <tr>
                <td>प्रत्यंतर्दशा</td>
                <td>{current_dasha['pratyantardasha']['planet']}</td>
                <td>{current_dasha['pratyantardasha']['start'].strftime('%d-%m-%Y')}</td>
                <td>{current_dasha['pratyantardasha']['end'].strftime('%d-%m-%Y')}</td>
            </tr>
        </table>
    </div>

    <div class="prediction-card">
        <h3>महादशा क्रम (Timeline)</h3>
        <div class="timeline">
    """

    maha_planet = current_dasha['mahadasha']['planet']
    for m in mahadashas[:8]:
        is_current = m.planet == maha_planet
        item_class = 'class="timeline-item current"' if is_current else 'class="timeline-item"'
        current_marker = " ← वर्तमान" if is_current else ""

        # Dynamic dasha effect based on lagna
        dasha_effect = get_lagna_specific_dasha_effect(m.planet, lagna_name)
        effect_text = dasha_effect['effect'][:80] + "..." if len(dasha_effect['effect']) > 80 else dasha_effect['effect']

        html += f"""
        <div {item_class}>
            <strong>{m.planet} महादशा{current_marker}</strong><br>
            {m.start_date.strftime('%d-%m-%Y')} से {m.end_date.strftime('%d-%m-%Y')}<br>
            <small>अवधि: {m.duration_years:.1f} वर्ष</small><br>
            <small>{effect_text}</small>
        </div>
        """

    html += """
        </div>
    </div>
    """

    # Dynamic analysis of current mahadasha (not hardcoded Saturn)
    current_maha = current_dasha['mahadasha']['planet']
    maha_effect = get_lagna_specific_dasha_effect(current_maha, lagna_name)

    # Find planet's rashi for dignity check
    planet_rashi = kundali.planets.get(current_maha.upper(), {}).get('rashi', '')
    dignity = ""
    own_signs = {"Sun": ["Simha"], "Moon": ["Karka"], "Mars": ["Mesha", "Vrishchika"],
                 "Mercury": ["Mithuna", "Kanya"], "Jupiter": ["Dhanu", "Meena"],
                 "Venus": ["Vrishabha", "Tula"], "Saturn": ["Makara", "Kumbha"]}
    exalt_signs = {"Sun": "Mesha", "Moon": "Vrishabha", "Mars": "Makara",
                   "Mercury": "Kanya", "Jupiter": "Karka", "Venus": "Meena", "Saturn": "Tula"}

    if planet_rashi in own_signs.get(current_maha, []):
        dignity = "स्वराशि में - शक्तिशाली"
    elif planet_rashi == exalt_signs.get(current_maha):
        dignity = "उच्च में - अति शक्तिशाली"

    quality = "शुभ" if maha_effect['is_benefic'] else "अशुभ"
    if maha_effect.get('is_yogakaraka'):
        quality = "योगकारक - अति शुभ"

    html += f"""
    <div class="prediction-card">
        <h3>{current_maha} महादशा - विस्तृत विश्लेषण</h3>
        <p><strong>{current_maha} {lagna_name} लग्न के लिए {quality}</strong></p>
    """

    if dignity:
        html += f"<p><strong>{current_maha} {planet_rashi} में ({dignity})</strong></p>"

    html += f"""
        <p><strong>प्रभाव:</strong> {maha_effect['effect']}</p>
        <p><strong>कारण:</strong> {maha_effect['reason']}</p>
    </div>
    """

    return html


def generate_yoga_section(kundali, planets_in_houses):
    """Generate special yogas section based on actual chart."""

    # YOGA DEFINITIONS based on actual chart
    detected_yogas = []

    # 1. Budhaditya Yoga - Sun + Mercury in same house
    sun_house = None
    mercury_house = None
    for h, planets in planets_in_houses.items():
        if "SUN" in planets:
            sun_house = h
        if "MERCURY" in planets:
            mercury_house = h

    if sun_house and sun_house == mercury_house:
        detected_yogas.append({
            "name": "बुधादित्य योग",
            "desc": f"सूर्य + बुध भाव {sun_house} में",
            "effects": ["बुद्धि और वाणी में निपुणता", "Business acumen", "Good communication skills"]
        })

    # 2. Gajakesari Yoga - Jupiter + Moon in kendra from each other
    jupiter_house = None
    moon_house = None
    for h, planets in planets_in_houses.items():
        if "JUPITER" in planets:
            jupiter_house = h
        if "MOON" in planets:
            moon_house = h

    if jupiter_house and moon_house:
        diff = abs(jupiter_house - moon_house)
        if diff in [0, 3, 6, 9]:  # Same or kendra
            detected_yogas.append({
                "name": "गजकेसरी योग",
                "desc": f"गुरु भाव {jupiter_house} + चंद्र भाव {moon_house}",
                "effects": ["प्रसिद्धि और सम्मान", "धन और संपत्ति", "बुद्धिमान संतान"]
            })

    # 3. Chandra-Mangal Yoga - Moon + Mars conjunction
    mars_house = None
    for h, planets in planets_in_houses.items():
        if "MARS" in planets:
            mars_house = h

    if moon_house and moon_house == mars_house:
        detected_yogas.append({
            "name": "चंद्र-मंगल योग",
            "desc": f"चंद्र + मंगल भाव {moon_house} में",
            "effects": ["धन लाभ", "व्यापार में सफलता", "साहसिक निर्णय"]
        })

    # 4. Planet in own sign or exaltation
    own_signs = {"SUN": ["Simha"], "MOON": ["Karka"], "MARS": ["Mesha", "Vrishchika"],
                 "MERCURY": ["Mithuna", "Kanya"], "JUPITER": ["Dhanu", "Meena"],
                 "VENUS": ["Vrishabha", "Tula"], "SATURN": ["Makara", "Kumbha"]}
    exalt_signs = {"SUN": "Mesha", "MOON": "Vrishabha", "MARS": "Makara",
                   "MERCURY": "Kanya", "JUPITER": "Karka", "VENUS": "Meena", "SATURN": "Tula"}
    planet_hindi = {"SUN": "सूर्य", "MOON": "चंद्र", "MARS": "मंगल", "MERCURY": "बुध",
                    "JUPITER": "गुरु", "VENUS": "शुक्र", "SATURN": "शनि"}

    for planet, info in kundali.planets.items():
        if planet in ["RAHU", "KETU"]:
            continue
        rashi = info.get('rashi', '')
        if rashi in own_signs.get(planet, []):
            detected_yogas.append({
                "name": f"{planet_hindi.get(planet, planet)} स्वराशि योग",
                "desc": f"{planet_hindi.get(planet, planet)} {rashi} में (Own sign)",
                "effects": ["ग्रह अपनी पूर्ण शक्ति में", "शुभ फल प्राप्त", "दशा में विशेष लाभ"]
            })
        elif rashi == exalt_signs.get(planet):
            detected_yogas.append({
                "name": f"{planet_hindi.get(planet, planet)} उच्च योग",
                "desc": f"{planet_hindi.get(planet, planet)} {rashi} में (Exalted)",
                "effects": ["ग्रह अति शक्तिशाली", "महत्वपूर्ण उपलब्धियां", "राज योग तुल्य फल"]
            })

    # 5. Planets in 1st house (Lagna Yoga)
    first_planets = planets_in_houses.get(1, [])
    for p in first_planets:
        if p in planet_hindi:
            detected_yogas.append({
                "name": f"{planet_hindi[p]} लग्न योग",
                "desc": f"{planet_hindi[p]} लग्न भाव में",
                "effects": ["व्यक्तित्व पर प्रभाव", "स्वास्थ्य और जीवन शक्ति", "प्रथम भाव के गुण"]
            })

    # Generate HTML
    if detected_yogas:
        html = '<div class="yoga-grid">'
        for yoga in detected_yogas[:6]:  # Show max 6 yogas
            html += f"""
            <div class="yoga-card">
                <h4>✅ {yoga['name']}</h4>
                <p><strong>{yoga['desc']}</strong></p>
                <ul>
            """
            for effect in yoga['effects']:
                html += f"<li>{effect}</li>"
            html += "</ul></div>"
        html += "</div>"
    else:
        html = """
        <div class="prediction-card">
            <h4>विशेष योग विश्लेषण</h4>
            <p>कुंडली में कोई प्रमुख शुभ योग नहीं पाया गया।</p>
            <p>ग्रहों की स्थिति सामान्य है।</p>
        </div>
        """

    return html


def generate_summary_section(kundali, planets_in_houses, current_dasha):
    """Generate summary and recommendations section based on actual chart."""
    lagna_name = kundali.lagna['rashi']

    # Lucky elements by lagna
    LUCKY_ELEMENTS_BY_LAGNA = {
        "Mesha": {"color": "लाल, नारंगी", "number": "9, 1", "day": "मंगलवार", "gem": "मूंगा (Coral)", "metal": "तांबा", "direction": "पूर्व"},
        "Vrishabha": {"color": "सफेद, हल्का नीला", "number": "6, 5", "day": "शुक्रवार", "gem": "हीरा (Diamond)", "metal": "चांदी", "direction": "दक्षिण-पूर्व"},
        "Mithuna": {"color": "हरा, पीला", "number": "5, 3", "day": "बुधवार", "gem": "पन्ना (Emerald)", "metal": "पीतल", "direction": "उत्तर"},
        "Karka": {"color": "सफेद, चांदी", "number": "2, 7", "day": "सोमवार", "gem": "मोती (Pearl)", "metal": "चांदी", "direction": "उत्तर-पश्चिम"},
        "Simha": {"color": "सुनहरा, नारंगी", "number": "1, 4", "day": "रविवार", "gem": "माणिक (Ruby)", "metal": "सोना", "direction": "पूर्व"},
        "Kanya": {"color": "हरा, हल्का पीला", "number": "5, 2", "day": "बुधवार", "gem": "पन्ना (Emerald)", "metal": "कांसा", "direction": "उत्तर"},
        "Tula": {"color": "सफेद, गुलाबी", "number": "6, 9", "day": "शुक्रवार", "gem": "हीरा (Diamond)", "metal": "चांदी", "direction": "पश्चिम"},
        "Vrishchika": {"color": "लाल, मरून", "number": "9, 4", "day": "मंगलवार", "gem": "मूंगा (Coral)", "metal": "तांबा", "direction": "दक्षिण"},
        "Dhanu": {"color": "पीला, नारंगी", "number": "3, 12", "day": "गुरुवार", "gem": "पुखराज (Yellow Sapphire)", "metal": "सोना", "direction": "उत्तर-पूर्व"},
        "Makara": {"color": "नीला, काला", "number": "8, 10", "day": "शनिवार", "gem": "नीलम (Blue Sapphire)", "metal": "लोहा", "direction": "दक्षिण"},
        "Kumbha": {"color": "नीला, बैंगनी", "number": "8, 4", "day": "शनिवार", "gem": "नीलम (Blue Sapphire)", "metal": "लोहा", "direction": "पश्चिम"},
        "Meena": {"color": "पीला, केसरिया", "number": "3, 9", "day": "गुरुवार", "gem": "पुखराज (Yellow Sapphire)", "metal": "सोना", "direction": "उत्तर-पूर्व"}
    }

    lucky = LUCKY_ELEMENTS_BY_LAGNA.get(lagna_name, {})

    # Calculate dynamic ratings based on chart
    def calculate_rating(lord, benefics_count):
        effect = get_lagna_specific_dasha_effect(lord, lagna_name)
        base = 3
        if effect['is_benefic']:
            base += 1
        if effect.get('is_yogakaraka'):
            base += 1
        base += min(benefics_count, 2)
        return min(base, 5)

    # Career rating - 10th lord
    tenth_lord = get_house_lord(10, lagna_name)
    tenth_planets = len(planets_in_houses.get(10, []))
    career_rating = calculate_rating(tenth_lord, tenth_planets)
    career_desc = f"{tenth_lord} दशमेश"

    # Marriage rating - 7th lord
    seventh_lord = get_house_lord(7, lagna_name)
    seventh_planets = len(planets_in_houses.get(7, []))
    marriage_rating = calculate_rating(seventh_lord, seventh_planets)

    # Children rating - 5th lord
    fifth_lord = get_house_lord(5, lagna_name)
    fifth_planets = len(planets_in_houses.get(5, []))
    children_rating = calculate_rating(fifth_lord, fifth_planets)
    fifth_effect = get_lagna_specific_dasha_effect(fifth_lord, lagna_name)
    children_desc = "शुभ" if fifth_effect['is_benefic'] else "उपाय करें"

    # Health rating - 6th lord and Lagna lord
    lagna_lord = get_house_lord(1, lagna_name)
    sixth_planets = len(planets_in_houses.get(6, []))
    health_rating = max(2, 4 - sixth_planets)

    # Wealth rating - 2nd lord and 2nd house planets
    second_lord = get_house_lord(2, lagna_name)
    second_planets = planets_in_houses.get(2, [])
    wealth_rating = calculate_rating(second_lord, len(second_planets))
    wealth_desc = f"{len(second_planets)} ग्रह धन भाव में" if second_planets else f"{second_lord} द्वितीयेश"

    def stars(n):
        return "⭐" * n

    html = f"""
    <div class="summary-grid">
        <div class="summary-card">
            <div class="title">करियर</div>
            <div class="rating">{stars(career_rating)}</div>
            <div>{career_desc}</div>
        </div>
        <div class="summary-card">
            <div class="title">विवाह</div>
            <div class="rating">{stars(marriage_rating)}</div>
            <div>{seventh_lord} सप्तमेश</div>
        </div>
        <div class="summary-card">
            <div class="title">संतान</div>
            <div class="rating">{stars(children_rating)}</div>
            <div>{children_desc}</div>
        </div>
        <div class="summary-card">
            <div class="title">स्वास्थ्य</div>
            <div class="rating">{stars(health_rating)}</div>
            <div>{lagna_lord} लग्नेश</div>
        </div>
        <div class="summary-card">
            <div class="title">धन</div>
            <div class="rating">{stars(wealth_rating)}</div>
            <div>{wealth_desc}</div>
        </div>
    </div>
    """

    # Dynamic recommendations
    current_maha = current_dasha['mahadasha']['planet']
    maha_effect = get_lagna_specific_dasha_effect(current_maha, lagna_name)
    quality = "शुभ" if maha_effect['is_benefic'] else "सावधानी"

    html += f"""
    <div class="highlight-box {'success' if maha_effect['is_benefic'] else ''}">
        <h3>🎯 मुख्य सुझाव</h3>
        <ol>
            <li><strong>वर्तमान {current_maha} महादशा</strong> {lagna_name} लग्न के लिए {quality}</li>
            <li><strong>{maha_effect['reason']}</strong></li>
    """

    # Add specific suggestions based on weak planets
    for planet in ["SATURN", "MARS", "RAHU"]:
        effect = get_lagna_specific_dasha_effect(planet, lagna_name)
        if not effect['is_benefic']:
            html += f"<li>{planet} के लिए उपाय करें - {effect['reason']}</li>"

    html += """
        </ol>
    </div>
    """

    # Lucky elements based on lagna
    html += f"""
    <div class="prediction-card">
        <h3>🔮 शुभ तत्व ({lagna_name} लग्न)</h3>
        <table>
            <tr><th>तत्व</th><th>शुभ</th></tr>
            <tr><td>शुभ रंग</td><td>{lucky.get('color', 'N/A')}</td></tr>
            <tr><td>शुभ अंक</td><td>{lucky.get('number', 'N/A')}</td></tr>
            <tr><td>शुभ दिन</td><td>{lucky.get('day', 'N/A')}</td></tr>
            <tr><td>शुभ रत्न</td><td>{lucky.get('gem', 'N/A')}</td></tr>
            <tr><td>शुभ धातु</td><td>{lucky.get('metal', 'N/A')}</td></tr>
            <tr><td>शुभ दिशा</td><td>{lucky.get('direction', 'N/A')}</td></tr>
        </table>
    </div>
    """

    # Dynamic mantras based on lagna
    PLANET_MANTRAS = {
        "Sun": ("ॐ घृणि सूर्याय नमः", "रविवार"),
        "Moon": ("ॐ सों सोमाय नमः", "सोमवार"),
        "Mars": ("ॐ अं अंगारकाय नमः", "मंगलवार"),
        "Mercury": ("ॐ बुं बुधाय नमः", "बुधवार"),
        "Jupiter": ("ॐ गुरवे नमः", "गुरुवार"),
        "Venus": ("ॐ शुं शुक्राय नमः", "शुक्रवार"),
        "Saturn": ("ॐ शं शनैश्चराय नमः", "शनिवार")
    }

    html += """
    <div class="prediction-card">
        <h3>🙏 उपाय एवं मंत्र</h3>
        <ul>
    """

    # Lagna lord mantra
    lagna_lord_mantra, lagna_lord_day = PLANET_MANTRAS.get(lagna_lord, ("", ""))
    if lagna_lord_mantra:
        html += f"<li><strong>{lagna_lord} मंत्र (लग्नेश):</strong> {lagna_lord_mantra} - {lagna_lord_day}</li>"

    # Current dasha lord mantra (only if benefic for lagna)
    current_dasha_mantra, current_dasha_day = PLANET_MANTRAS.get(current_maha, ("", ""))
    if current_dasha_mantra and maha_effect['is_benefic']:
        html += f"<li><strong>{current_maha} मंत्र (वर्तमान दशा):</strong> {current_dasha_mantra} - {current_dasha_day}</li>"

    # Yogakaraka mantra
    yogakaraka_planets = {"Mesha": "Sun", "Vrishabha": "Saturn", "Mithuna": "Venus",
                          "Karka": "Mars", "Simha": "Mars", "Kanya": "Venus",
                          "Tula": "Saturn", "Vrishchika": "Sun", "Dhanu": "Sun",
                          "Makara": "Venus", "Kumbha": "Venus", "Meena": "Mars"}
    yogakaraka = yogakaraka_planets.get(lagna_name)
    if yogakaraka and yogakaraka != lagna_lord:
        yk_mantra, yk_day = PLANET_MANTRAS.get(yogakaraka, ("", ""))
        if yk_mantra:
            html += f"<li><strong>{yogakaraka} मंत्र (योगकारक):</strong> {yk_mantra} - {yk_day}</li>"

    html += """
        </ul>
    </div>
    """

    return html
