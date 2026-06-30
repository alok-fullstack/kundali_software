"""
HTML Kundali Generator - Beautiful Hindi Kundali Report
"""

from datetime import datetime
from typing import Dict
import os

from .kundali import Kundali, create_kundali
from .config import RASHIS, PLANET_NAMES, Planet, BHAVA_NAMES
from .predictions import (
    get_career_prediction, get_marriage_prediction,
    get_children_prediction, get_health_prediction,
    get_dasha_prediction, GRAHA_BHAVA_PHAL
)


def generate_kundali_html(kundali: Kundali, output_path: str = None) -> str:
    """
    Generate a beautiful Hindi Kundali HTML report.

    Args:
        kundali: Kundali object with all calculations
        output_path: Path to save HTML file (optional)

    Returns:
        HTML content as string
    """

    # Get all data
    summary = kundali.get_chart_summary()
    planets_in_houses = kundali.get_planets_in_houses()
    mahadashas = kundali.get_mahadashas(years=80)

    # Calculate house rashis
    lagna_rashi_num = kundali.lagna["rashi_num"]
    house_rashis = {}
    for i in range(1, 13):
        rashi_num = (lagna_rashi_num + i - 1) % 12
        house_rashis[i] = RASHIS[rashi_num]["name"]

    # Generate predictions
    career_pred = get_career_prediction(
        kundali.lagna["rashi"],
        planets_in_houses,
        kundali.planets
    )
    marriage_pred = get_marriage_prediction(
        kundali.lagna["rashi"],
        planets_in_houses,
        house_rashis[7]
    )
    children_pred = get_children_prediction(
        planets_in_houses,
        house_rashis[5]
    )
    health_pred = get_health_prediction(
        kundali.lagna["rashi"],
        planets_in_houses
    )
    dasha_pred = get_dasha_prediction(summary["current_dasha"])

    # Build HTML
    html = f"""<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>जन्म कुंडली - {summary['birth_details']['name']}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;600;700&display=swap');

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Noto Sans Devanagari', 'Mangal', sans-serif;
            background: linear-gradient(135deg, #fff5e6 0%, #ffe4c4 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}

        .header .om {{
            font-size: 3em;
            margin-bottom: 10px;
        }}

        .header .subtitle {{
            font-size: 1.2em;
            opacity: 0.9;
        }}

        .birth-details {{
            background: #fff8f0;
            padding: 25px;
            border-bottom: 3px solid #ff6b35;
        }}

        .birth-details h2 {{
            color: #ff6b35;
            margin-bottom: 15px;
            font-size: 1.5em;
        }}

        .birth-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }}

        .birth-item {{
            background: white;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #ff6b35;
        }}

        .birth-item label {{
            color: #666;
            font-size: 0.9em;
        }}

        .birth-item value {{
            display: block;
            font-size: 1.1em;
            font-weight: 600;
            color: #333;
            margin-top: 5px;
        }}

        .section {{
            padding: 25px;
            border-bottom: 1px solid #eee;
        }}

        .section h2 {{
            color: #ff6b35;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #ff6b35;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .section h2 .icon {{
            font-size: 1.5em;
        }}

        /* Kundali Chart */
        .kundali-chart {{
            display: flex;
            justify-content: center;
            margin: 20px 0;
        }}

        .chart-container {{
            width: 400px;
            height: 400px;
            position: relative;
        }}

        .chart-box {{
            position: absolute;
            border: 2px solid #8b4513;
            background: #fffaf0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            font-size: 0.8em;
            padding: 5px;
        }}

        .chart-box .house-num {{
            position: absolute;
            top: 2px;
            left: 5px;
            font-size: 0.7em;
            color: #8b4513;
            font-weight: bold;
        }}

        .chart-box .rashi {{
            color: #ff6b35;
            font-weight: 600;
            font-size: 0.9em;
        }}

        .chart-box .planets {{
            color: #333;
            font-size: 0.75em;
            text-align: center;
            margin-top: 3px;
        }}

        /* North Indian Chart positions */
        .box-1 {{ top: 100px; left: 100px; width: 100px; height: 100px; }}
        .box-2 {{ top: 0; left: 100px; width: 100px; height: 100px; }}
        .box-3 {{ top: 0; left: 200px; width: 100px; height: 100px; }}
        .box-4 {{ top: 100px; left: 200px; width: 100px; height: 100px; }}
        .box-5 {{ top: 200px; left: 200px; width: 100px; height: 100px; }}
        .box-6 {{ top: 300px; left: 200px; width: 100px; height: 100px; }}
        .box-7 {{ top: 300px; left: 100px; width: 100px; height: 100px; }}
        .box-8 {{ top: 300px; left: 0; width: 100px; height: 100px; }}
        .box-9 {{ top: 200px; left: 0; width: 100px; height: 100px; }}
        .box-10 {{ top: 100px; left: 0; width: 100px; height: 100px; }}
        .box-11 {{ top: 0; left: 0; width: 100px; height: 100px; }}
        .box-12 {{ top: 0; left: 200px; width: 100px; height: 100px; transform: translateX(100px); }}

        /* Diamond style chart */
        .diamond-chart {{
            width: 400px;
            height: 400px;
            position: relative;
            margin: 0 auto;
        }}

        .diamond-chart .center {{
            position: absolute;
            top: 100px;
            left: 100px;
            width: 200px;
            height: 200px;
            border: 2px solid #8b4513;
            transform: rotate(45deg);
            background: #fffaf0;
        }}

        /* Planet Table */
        .planet-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}

        .planet-table th {{
            background: #ff6b35;
            color: white;
            padding: 12px;
            text-align: left;
        }}

        .planet-table td {{
            padding: 12px;
            border-bottom: 1px solid #eee;
        }}

        .planet-table tr:nth-child(even) {{
            background: #fff8f0;
        }}

        .planet-table tr:hover {{
            background: #ffe4c4;
        }}

        .retrograde {{
            color: #e74c3c;
            font-weight: bold;
        }}

        /* Dasha Table */
        .dasha-table {{
            width: 100%;
            border-collapse: collapse;
        }}

        .dasha-table th {{
            background: #8b4513;
            color: white;
            padding: 10px;
        }}

        .dasha-table td {{
            padding: 10px;
            border-bottom: 1px solid #ddd;
            text-align: center;
        }}

        .current-dasha {{
            background: #fff3cd !important;
            font-weight: bold;
        }}

        /* Prediction Cards */
        .prediction-card {{
            background: linear-gradient(135deg, #fff8f0 0%, #ffe4c4 100%);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 5px solid #ff6b35;
        }}

        .prediction-card h3 {{
            color: #8b4513;
            margin-bottom: 15px;
            font-size: 1.3em;
        }}

        .prediction-card p {{
            line-height: 1.8;
            color: #555;
        }}

        .prediction-card strong {{
            color: #ff6b35;
        }}

        /* Footer */
        .footer {{
            background: #333;
            color: white;
            padding: 20px;
            text-align: center;
        }}

        .footer p {{
            margin: 5px 0;
            opacity: 0.8;
        }}

        .disclaimer {{
            background: #fff3cd;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            font-size: 0.9em;
            color: #856404;
        }}

        @media print {{
            body {{
                background: white;
            }}
            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <div class="om">ॐ</div>
            <h1>श्री गणेशाय नमः</h1>
            <h1>जन्म कुंडली</h1>
            <p class="subtitle">{summary['birth_details']['name']}</p>
        </div>

        <!-- Birth Details -->
        <div class="birth-details">
            <h2>🪔 जन्म विवरण</h2>
            <div class="birth-grid">
                <div class="birth-item">
                    <label>नाम</label>
                    <value>{summary['birth_details']['name']}</value>
                </div>
                <div class="birth-item">
                    <label>जन्म तिथि एवं समय</label>
                    <value>{summary['birth_details']['date']}</value>
                </div>
                <div class="birth-item">
                    <label>जन्म स्थान</label>
                    <value>{summary['birth_details']['city']}</value>
                </div>
                <div class="birth-item">
                    <label>अक्षांश-देशांतर</label>
                    <value>{summary['birth_details']['coordinates']}</value>
                </div>
                <div class="birth-item">
                    <label>लग्न राशि</label>
                    <value>{summary['lagna']['rashi']} ({summary['lagna']['rashi_english']})</value>
                </div>
                <div class="birth-item">
                    <label>चंद्र राशि</label>
                    <value>{summary['moon_sign']['rashi']}</value>
                </div>
                <div class="birth-item">
                    <label>जन्म नक्षत्र</label>
                    <value>{summary['moon_sign']['nakshatra']} - पाद {summary['moon_sign']['pada']}</value>
                </div>
                <div class="birth-item">
                    <label>सूर्य राशि</label>
                    <value>{summary['sun_sign']['rashi']}</value>
                </div>
            </div>
        </div>

        <!-- Kundali Chart -->
        <div class="section">
            <h2><span class="icon">📊</span> लग्न कुंडली</h2>
            {generate_chart_html(kundali, planets_in_houses, house_rashis)}
        </div>

        <!-- Planet Positions -->
        <div class="section">
            <h2><span class="icon">🌟</span> ग्रह स्थिति</h2>
            <table class="planet-table">
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
                    {generate_planet_rows(kundali, planets_in_houses)}
                </tbody>
            </table>
        </div>

        <!-- Current Dasha -->
        <div class="section">
            <h2><span class="icon">⏰</span> वर्तमान दशा</h2>
            <div class="prediction-card">
                <h3>चल रही दशा: {summary['current_dasha']['full_dasha']}</h3>
                <p><strong>महादशा:</strong> {summary['current_dasha']['mahadasha']['planet']}
                   ({summary['current_dasha']['mahadasha']['start'].strftime('%d-%m-%Y')} से
                    {summary['current_dasha']['mahadasha']['end'].strftime('%d-%m-%Y')} तक)</p>
                <p><strong>अंतर्दशा:</strong> {summary['current_dasha']['antardasha']['planet']}
                   ({summary['current_dasha']['antardasha']['start'].strftime('%d-%m-%Y')} से
                    {summary['current_dasha']['antardasha']['end'].strftime('%d-%m-%Y')} तक)</p>
                <p><strong>प्रत्यंतर्दशा:</strong> {summary['current_dasha']['pratyantardasha']['planet']}</p>
            </div>
            {format_prediction(dasha_pred)}
        </div>

        <!-- Mahadasha Timeline -->
        <div class="section">
            <h2><span class="icon">📅</span> महादशा क्रम</h2>
            <table class="dasha-table">
                <thead>
                    <tr>
                        <th>महादशा</th>
                        <th>आरंभ तिथि</th>
                        <th>समाप्ति तिथि</th>
                        <th>अवधि (वर्ष)</th>
                    </tr>
                </thead>
                <tbody>
                    {generate_dasha_rows(mahadashas, summary['current_dasha']['mahadasha']['planet'])}
                </tbody>
            </table>
        </div>

        <!-- Career Prediction -->
        <div class="section">
            <h2><span class="icon">💼</span> करियर एवं व्यवसाय</h2>
            {format_prediction(career_pred)}
        </div>

        <!-- Marriage Prediction -->
        <div class="section">
            <h2><span class="icon">💑</span> विवाह एवं दाम्पत्य</h2>
            {format_prediction(marriage_pred)}
        </div>

        <!-- Children Prediction -->
        <div class="section">
            <h2><span class="icon">👶</span> संतान</h2>
            {format_prediction(children_pred)}
        </div>

        <!-- Health Prediction -->
        <div class="section">
            <h2><span class="icon">🏥</span> स्वास्थ्य</h2>
            {format_prediction(health_pred)}
        </div>

        <!-- Disclaimer -->
        <div class="section">
            <div class="disclaimer">
                <strong>⚠️ अस्वीकरण:</strong> यह कुंडली केवल सूचनात्मक उद्देश्यों के लिए है।
                ज्योतिष एक प्राचीन विद्या है और इसके परिणाम व्यक्ति के कर्मों पर भी निर्भर करते हैं।
                महत्वपूर्ण निर्णयों के लिए किसी अनुभवी ज्योतिषी से परामर्श लें।
                <br><br>
                <strong>सटीकता:</strong> यह सॉफ्टवेयर Swiss Ephemeris (NASA JPL DE431) पर आधारित है
                जो 0.001 arc-second की सटीकता प्रदान करता है।
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <p>🙏 शुभम् भवतु 🙏</p>
            <p>Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M')}</p>
            <p>Powered by Swiss Ephemeris (NASA JPL DE431)</p>
        </div>
    </div>
</body>
</html>"""

    # Save to file if path provided
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Kundali HTML generated successfully: {output_path}")

    return html


def generate_chart_html(kundali: Kundali, planets_in_houses: Dict, house_rashis: Dict) -> str:
    """Generate South Indian style chart HTML."""

    # South Indian chart layout (fixed rashi positions)
    # Using a simple grid representation
    chart_html = """
    <div style="display: flex; justify-content: center; margin: 20px 0;">
        <table style="border-collapse: collapse; width: 360px; height: 360px;">
    """

    # South Indian chart - 4x4 grid with center empty
    # Positions: Meena(12), Mesha(1), Vrishabha(2), Mithuna(3)
    #            Kumbha(11), [center], [center], Karka(4)
    #            Makara(10), [center], [center], Simha(5)
    #            Dhanu(9), Vrishchika(8), Tula(7), Kanya(6)

    rashi_positions = [
        [12, 1, 2, 3],
        [11, 0, 0, 4],
        [10, 0, 0, 5],
        [9, 8, 7, 6]
    ]

    rashi_names_hindi = {
        1: "मेष", 2: "वृषभ", 3: "मिथुन", 4: "कर्क",
        5: "सिंह", 6: "कन्या", 7: "तुला", 8: "वृश्चिक",
        9: "धनु", 10: "मकर", 11: "कुंभ", 12: "मीन"
    }

    lagna_rashi_num = kundali.lagna["rashi_num"] + 1  # 1-indexed

    for row in rashi_positions:
        chart_html += "<tr>"
        for rashi_num in row:
            if rashi_num == 0:
                chart_html += """<td style="border: 2px solid #8b4513; width: 90px; height: 90px;
                                background: linear-gradient(135deg, #fff8dc, #ffe4b5);"></td>"""
            else:
                # Find which house this rashi is
                house_num = ((rashi_num - lagna_rashi_num) % 12) + 1

                # Get planets in this house
                house_planets = planets_in_houses.get(house_num, [])
                planet_str = ""
                for p in house_planets:
                    hindi_name = PLANET_NAMES[Planet[p]]["hindi"]
                    symbol = PLANET_NAMES[Planet[p]]["symbol"]
                    is_retro = kundali.planets[p]["is_retrograde"]
                    retro_mark = "(व)" if is_retro else ""
                    planet_str += f"{symbol}{retro_mark} "

                is_lagna = house_num == 1
                bg_color = "#fff3cd" if is_lagna else "#fffaf0"
                border_extra = "border: 3px solid #ff6b35;" if is_lagna else "border: 2px solid #8b4513;"

                chart_html += f"""
                <td style="{border_extra} width: 90px; height: 90px;
                    background: {bg_color}; vertical-align: top; padding: 5px; font-size: 12px;">
                    <div style="color: #8b4513; font-weight: bold;">{rashi_names_hindi[rashi_num]}</div>
                    <div style="font-size: 10px; color: #666;">भाव {house_num}</div>
                    <div style="color: #333; margin-top: 5px; font-size: 14px;">{planet_str}</div>
                </td>"""
        chart_html += "</tr>"

    chart_html += """
        </table>
    </div>
    <p style="text-align: center; color: #666; font-size: 0.9em;">
        (व) = वक्री (Retrograde) | पीला बॉक्स = लग्न भाव
    </p>
    """

    return chart_html


def generate_planet_rows(kundali: Kundali, planets_in_houses: Dict) -> str:
    """Generate planet table rows."""
    rows = ""

    planet_order = ["SUN", "MOON", "MARS", "MERCURY", "JUPITER", "VENUS", "SATURN", "RAHU", "KETU"]

    for planet_name in planet_order:
        data = kundali.planets[planet_name]
        hindi_name = PLANET_NAMES[Planet[planet_name]]["hindi"]
        symbol = PLANET_NAMES[Planet[planet_name]]["symbol"]

        # Find house
        house_num = 0
        for h, planets in planets_in_houses.items():
            if planet_name in planets:
                house_num = h
                break

        retro_class = 'class="retrograde"' if data["is_retrograde"] else ""
        retro_text = "वक्री" if data["is_retrograde"] else "मार्गी"

        rows += f"""
        <tr>
            <td>{symbol} {hindi_name}</td>
            <td>{data['rashi']}</td>
            <td>{data['rashi_degree']:.2f}°</td>
            <td>{data['nakshatra']} (पाद {data['pada']})</td>
            <td>{house_num}</td>
            <td {retro_class}>{retro_text}</td>
        </tr>
        """

    return rows


def generate_dasha_rows(mahadashas, current_maha_planet: str) -> str:
    """Generate dasha table rows."""
    rows = ""

    for maha in mahadashas[:10]:  # Show first 10
        is_current = maha.planet == current_maha_planet
        row_class = 'class="current-dasha"' if is_current else ""

        rows += f"""
        <tr {row_class}>
            <td>{maha.planet}</td>
            <td>{maha.start_date.strftime('%d-%m-%Y')}</td>
            <td>{maha.end_date.strftime('%d-%m-%Y')}</td>
            <td>{maha.duration_years:.1f}</td>
        </tr>
        """

    return rows


def format_prediction(prediction: str) -> str:
    """Format prediction text to HTML."""
    lines = prediction.strip().split('\n')
    html = '<div class="prediction-card">'

    for line in lines:
        if line.startswith('**') and line.endswith('**'):
            # Header
            html += f'<h3>{line.replace("**", "")}</h3>'
        elif line.startswith('**'):
            # Bold line
            html += f'<p>{line.replace("**", "<strong>").replace(":**", ":</strong>")}</p>'
        elif line.startswith('- '):
            # List item
            html += f'<p>• {line[2:]}</p>'
        elif line.strip():
            html += f'<p>{line}</p>'

    html += '</div>'
    return html
