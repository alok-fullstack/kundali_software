"""
WeasyPrint PDF Generator for Kundali Software

Converts HTML to PDF using WeasyPrint for web-accurate rendering.
Supports Hindi/Devanagari text with proper fonts.
"""

import io
from typing import Optional
from datetime import datetime

try:
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False
    print("WeasyPrint not available. Install with: pip install weasyprint")

from .kundali import Kundali
from .config import PLANET_NAMES, Planet, BHAVA_NAMES, RASHIS


# =============================================================================
# CSS STYLES FOR PDF
# =============================================================================

PDF_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;600;700&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Noto Sans Devanagari', 'Segoe UI', Tahoma, sans-serif;
    font-size: 11pt;
    line-height: 1.4;
    color: #333;
    background: white;
}

.page {
    padding: 15mm;
    page-break-after: always;
}

.page:last-child {
    page-break-after: avoid;
}

/* Header */
.header {
    background: linear-gradient(135deg, #ff6b00 0%, #ff8c00 50%, #ffa500 100%);
    color: white;
    padding: 20px;
    text-align: center;
    border-radius: 10px;
    margin-bottom: 20px;
}

.header h1 {
    font-size: 24pt;
    margin-bottom: 5px;
}

.header .subtitle {
    font-size: 14pt;
    opacity: 0.9;
}

.om-symbol {
    font-size: 36pt;
    color: #fff;
}

/* Section */
.section {
    margin-bottom: 20px;
    page-break-inside: avoid;
}

.section-title {
    background: linear-gradient(90deg, #ff6b00, #ff8c00);
    color: white;
    padding: 8px 15px;
    font-size: 13pt;
    font-weight: bold;
    border-radius: 5px;
    margin-bottom: 10px;
}

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 15px;
}

th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
    font-size: 10pt;
}

th {
    background: #fff8dc;
    color: #8b4513;
    font-weight: 600;
}

tr:nth-child(even) {
    background: #fafafa;
}

/* Kundali Chart */
.chart-container {
    display: flex;
    justify-content: center;
    margin: 20px 0;
}

.chart-table {
    border: 3px solid #8b4513;
    background: #fffaf0;
}

.chart-table td {
    width: 80px;
    height: 80px;
    border: 2px solid #d2691e;
    text-align: center;
    vertical-align: middle;
    font-size: 9pt;
    position: relative;
}

.chart-table .rashi-name {
    font-size: 8pt;
    color: #666;
    position: absolute;
    top: 2px;
    left: 4px;
}

.chart-table .house-num {
    font-size: 7pt;
    color: #999;
    position: absolute;
    bottom: 2px;
    right: 4px;
}

.chart-table .planets {
    font-weight: bold;
    color: #8b0000;
}

/* Info Grid */
.info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
    margin-bottom: 20px;
}

.info-box {
    background: #fff8dc;
    border: 1px solid #daa520;
    border-radius: 8px;
    padding: 12px;
}

.info-box h3 {
    color: #8b4513;
    font-size: 11pt;
    margin-bottom: 8px;
    border-bottom: 1px solid #daa520;
    padding-bottom: 5px;
}

.info-row {
    display: flex;
    justify-content: space-between;
    padding: 4px 0;
    font-size: 10pt;
}

.info-label {
    color: #666;
}

.info-value {
    font-weight: 600;
    color: #333;
}

/* Dasha Section */
.dasha-table th {
    background: #e6f3ff;
    color: #1a5276;
}

/* Yoga Section */
.yoga-item {
    background: #f0fff0;
    border-left: 4px solid #228b22;
    padding: 10px;
    margin-bottom: 10px;
    border-radius: 0 5px 5px 0;
}

.yoga-name {
    font-weight: bold;
    color: #228b22;
    font-size: 11pt;
}

.yoga-desc {
    color: #666;
    font-size: 10pt;
    margin-top: 5px;
}

/* Footer */
.footer {
    text-align: center;
    padding: 15px;
    background: linear-gradient(135deg, #ff6b00, #ff8c00);
    color: white;
    border-radius: 10px;
    margin-top: 20px;
    font-size: 9pt;
}

.footer .blessing {
    font-size: 11pt;
    margin-bottom: 5px;
}

/* Print Settings */
@page {
    size: A4;
    margin: 10mm;
}

@media print {
    .page {
        padding: 0;
    }
}
"""


# =============================================================================
# HTML TEMPLATES
# =============================================================================

RASHI_HINDI = {
    "Mesha": "मेष", "Vrishabha": "वृषभ", "Mithuna": "मिथुन", "Karka": "कर्क",
    "Simha": "सिंह", "Kanya": "कन्या", "Tula": "तुला", "Vrishchika": "वृश्चिक",
    "Dhanu": "धनु", "Makara": "मकर", "Kumbha": "कुंभ", "Meena": "मीन"
}

PLANET_HINDI = {
    "SUN": "सूर्य", "MOON": "चंद्र", "MARS": "मंगल", "MERCURY": "बुध",
    "JUPITER": "गुरु", "VENUS": "शुक्र", "SATURN": "शनि",
    "RAHU": "राहु", "KETU": "केतु"
}


def generate_kundali_html(kundali: Kundali, include_css: bool = True) -> str:
    """Generate complete HTML for Kundali report."""

    birth_data = kundali.birth_data
    planets = kundali.planets
    lagna = kundali.lagna
    houses = kundali.houses
    planets_in_houses = kundali.get_planets_in_houses()
    dasha = kundali.dasha

    # Get yogas
    try:
        from .yogas import get_all_yogas
        yogas = get_all_yogas(kundali)
    except:
        yogas = []

    lagna_hindi = RASHI_HINDI.get(lagna['rashi'], lagna['rashi'])
    moon_hindi = RASHI_HINDI.get(planets['MOON']['rashi'], planets['MOON']['rashi'])

    css = f"<style>{PDF_CSS}</style>" if include_css else ""

    html = f"""
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <title>जन्म कुंडली - {birth_data.name}</title>
    {css}
</head>
<body>
    <div class="page">
        <!-- Header -->
        <div class="header">
            <div class="om-symbol">ॐ</div>
            <h1>जन्म कुंडली / JANAM KUNDALI</h1>
            <div class="subtitle">{birth_data.name}</div>
        </div>

        <!-- Birth Details -->
        <div class="section">
            <div class="section-title">जन्म विवरण / Birth Details</div>
            <table>
                <tr>
                    <th>विवरण / Detail</th>
                    <th>मान / Value</th>
                </tr>
                <tr>
                    <td>नाम / Name</td>
                    <td>{birth_data.name}</td>
                </tr>
                <tr>
                    <td>जन्म तिथि / Date of Birth</td>
                    <td>{birth_data.date.strftime('%d-%m-%Y')}</td>
                </tr>
                <tr>
                    <td>जन्म समय / Time of Birth</td>
                    <td>{birth_data.date.strftime('%I:%M %p')}</td>
                </tr>
                <tr>
                    <td>जन्म स्थान / Place of Birth</td>
                    <td>{birth_data.city}</td>
                </tr>
                <tr>
                    <td>निर्देशांक / Coordinates</td>
                    <td>{birth_data.latitude:.4f}°N, {birth_data.longitude:.4f}°E</td>
                </tr>
                <tr>
                    <td>लग्न / Lagna</td>
                    <td>{lagna_hindi} ({lagna['rashi']})</td>
                </tr>
                <tr>
                    <td>चंद्र राशि / Moon Sign</td>
                    <td>{moon_hindi} ({planets['MOON']['rashi']})</td>
                </tr>
                <tr>
                    <td>नक्षत्र / Nakshatra</td>
                    <td>{planets['MOON']['nakshatra']} Pada {planets['MOON']['nakshatra_pada']}</td>
                </tr>
            </table>
        </div>

        <!-- Kundali Chart -->
        <div class="section">
            <div class="section-title">लग्न कुंडली / Lagna Kundali</div>
            {generate_chart_html(planets_in_houses, lagna['rashi_num'])}
        </div>

        <!-- Planet Positions -->
        <div class="section">
            <div class="section-title">ग्रह स्थिति / Planet Positions</div>
            <table>
                <tr>
                    <th>ग्रह / Planet</th>
                    <th>राशि / Sign</th>
                    <th>अंश / Degree</th>
                    <th>नक्षत्र / Nakshatra</th>
                    <th>भाव / House</th>
                </tr>
                {generate_planet_rows(planets, planets_in_houses)}
            </table>
        </div>
    </div>

    <div class="page">
        <!-- Dasha -->
        <div class="section">
            <div class="section-title">विंशोत्तरी दशा / Vimshottari Dasha</div>
            <table class="dasha-table">
                <tr>
                    <th>महादशा / Mahadasha</th>
                    <th>प्रारंभ / Start</th>
                    <th>समाप्त / End</th>
                    <th>अवधि / Duration</th>
                </tr>
                {generate_dasha_rows(dasha)}
            </table>
        </div>

        <!-- Yogas -->
        {generate_yoga_section(yogas) if yogas else ''}

        <!-- Footer -->
        <div class="footer">
            <div class="blessing">ॐ शुभम् भवतु / May Auspiciousness Prevail ॐ</div>
            <div>Generated on {datetime.now().strftime('%d %B %Y, %I:%M %p')}</div>
            <div style="margin-top: 5px; font-size: 8pt; opacity: 0.8;">
                Powered by Kundali Software | Vedic Astrology Calculator
            </div>
        </div>
    </div>
</body>
</html>
"""
    return html


def generate_chart_html(planets_in_houses: dict, lagna_num: int) -> str:
    """Generate North Indian style Kundali chart HTML."""
    rashi_positions = [[12,1,2,3],[11,0,0,4],[10,0,0,5],[9,8,7,6]]
    rashi_names = {1:"मेष",2:"वृषभ",3:"मिथुन",4:"कर्क",5:"सिंह",6:"कन्या",
                   7:"तुला",8:"वृश्चिक",9:"धनु",10:"मकर",11:"कुंभ",12:"मीन"}

    html = '<div class="chart-container"><table class="chart-table">'
    for row in rashi_positions:
        html += "<tr>"
        for rashi_num in row:
            if rashi_num == 0:
                html += '<td style="background:linear-gradient(135deg,#fff8dc,#ffe4b5);"></td>'
            else:
                house_num = ((rashi_num - lagna_num) % 12) + 1
                house_planets = planets_in_houses.get(house_num, [])

                planet_symbols = []
                for p in house_planets:
                    symbol = PLANET_NAMES[Planet[p]]["symbol"]
                    planet_symbols.append(symbol)

                planets_str = " ".join(planet_symbols) if planet_symbols else ""
                rashi_name = rashi_names.get(rashi_num, "")

                html += f'''<td>
                    <span class="rashi-name">{rashi_name}</span>
                    <span class="planets">{planets_str}</span>
                    <span class="house-num">{house_num}</span>
                </td>'''
        html += "</tr>"
    html += "</table></div>"
    return html


def generate_planet_rows(planets: dict, planets_in_houses: dict) -> str:
    """Generate planet table rows."""
    rows = ""
    for planet_name, data in planets.items():
        hindi = PLANET_HINDI.get(planet_name, planet_name)
        symbol = PLANET_NAMES[Planet[planet_name]]["symbol"]
        rashi_hindi = RASHI_HINDI.get(data['rashi'], data['rashi'])

        # Find house
        house = 1
        for h, p_list in planets_in_houses.items():
            if planet_name in p_list:
                house = h
                break

        retro = " (R)" if data.get('is_retrograde') else ""

        rows += f"""
        <tr>
            <td>{symbol} {hindi} / {planet_name}{retro}</td>
            <td>{rashi_hindi} ({data['rashi']})</td>
            <td>{data['rashi_degree']:.2f}°</td>
            <td>{data['nakshatra']} Pada {data['nakshatra_pada']}</td>
            <td>{house}</td>
        </tr>
        """
    return rows


def generate_dasha_rows(dasha: list) -> str:
    """Generate dasha table rows."""
    rows = ""
    for period in dasha[:9]:  # Show 9 Mahadashas
        planet = period.planet
        hindi = PLANET_HINDI.get(planet, planet)
        start = period.start_date.strftime('%d-%m-%Y')
        end = period.end_date.strftime('%d-%m-%Y')
        years = (period.end_date - period.start_date).days / 365.25

        rows += f"""
        <tr>
            <td>{hindi} / {planet}</td>
            <td>{start}</td>
            <td>{end}</td>
            <td>{years:.1f} वर्ष / years</td>
        </tr>
        """
    return rows


def generate_yoga_section(yogas: list) -> str:
    """Generate yoga section HTML."""
    if not yogas:
        return ""

    html = '''
    <div class="section">
        <div class="section-title">योग / Yogas</div>
    '''

    for yoga in yogas[:10]:  # Show top 10 yogas
        name = yoga.get('name', 'Unknown')
        name_hindi = yoga.get('name_hindi', name)
        result = yoga.get('result', '')

        html += f'''
        <div class="yoga-item">
            <div class="yoga-name">{name_hindi} / {name}</div>
            <div class="yoga-desc">{result}</div>
        </div>
        '''

    html += '</div>'
    return html


# =============================================================================
# PDF GENERATION
# =============================================================================

def generate_kundali_pdf_weasy(kundali: Kundali) -> bytes:
    """
    Generate PDF from Kundali using WeasyPrint.

    Returns PDF as bytes.
    """
    if not WEASYPRINT_AVAILABLE:
        raise ImportError("WeasyPrint is not installed. Install with: pip install weasyprint")

    # Generate HTML
    html_content = generate_kundali_html(kundali, include_css=True)

    # Configure fonts
    font_config = FontConfiguration()

    # Convert to PDF
    html = HTML(string=html_content)
    pdf_bytes = html.write_pdf(font_config=font_config)

    return pdf_bytes


def generate_matching_pdf_weasy(boy_kundali: Kundali, girl_kundali: Kundali,
                                 matching_result: dict) -> bytes:
    """
    Generate Matching PDF using WeasyPrint.

    Returns PDF as bytes.
    """
    if not WEASYPRINT_AVAILABLE:
        raise ImportError("WeasyPrint is not installed. Install with: pip install weasyprint")

    # Generate HTML for matching report
    html_content = generate_matching_html(boy_kundali, girl_kundali, matching_result)

    # Configure fonts
    font_config = FontConfiguration()

    # Convert to PDF
    html = HTML(string=html_content)
    pdf_bytes = html.write_pdf(font_config=font_config)

    return pdf_bytes


def generate_matching_html(boy_kundali: Kundali, girl_kundali: Kundali,
                           matching_result: dict) -> str:
    """Generate HTML for matching report."""

    total_score = matching_result.get('total_score', 0)
    max_score = matching_result.get('max_score', 36)
    percentage = (total_score / max_score * 100) if max_score > 0 else 0

    html = f"""
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <title>कुंडली मिलान - {boy_kundali.birth_data.name} & {girl_kundali.birth_data.name}</title>
    <style>{PDF_CSS}</style>
</head>
<body>
    <div class="page">
        <div class="header">
            <div class="om-symbol">ॐ</div>
            <h1>कुंडली मिलान / KUNDALI MATCHING</h1>
            <div class="subtitle">{boy_kundali.birth_data.name} & {girl_kundali.birth_data.name}</div>
        </div>

        <div class="section">
            <div class="section-title">मिलान स्कोर / Matching Score</div>
            <div style="text-align: center; padding: 20px;">
                <div style="font-size: 48pt; color: {'#228b22' if percentage >= 60 else '#ff6b00'}; font-weight: bold;">
                    {total_score}/{max_score}
                </div>
                <div style="font-size: 18pt; color: #666;">
                    ({percentage:.1f}%)
                </div>
                <div style="margin-top: 10px; font-size: 14pt;">
                    {'शुभ विवाह / Favorable Match' if percentage >= 60 else 'सावधानी आवश्यक / Caution Required'}
                </div>
            </div>
        </div>

        <div class="info-grid">
            <div class="info-box">
                <h3>वर / Groom: {boy_kundali.birth_data.name}</h3>
                <div class="info-row">
                    <span class="info-label">राशि / Rashi:</span>
                    <span class="info-value">{boy_kundali.planets['MOON']['rashi']}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">नक्षत्र / Nakshatra:</span>
                    <span class="info-value">{boy_kundali.planets['MOON']['nakshatra']}</span>
                </div>
            </div>
            <div class="info-box">
                <h3>वधू / Bride: {girl_kundali.birth_data.name}</h3>
                <div class="info-row">
                    <span class="info-label">राशि / Rashi:</span>
                    <span class="info-value">{girl_kundali.planets['MOON']['rashi']}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">नक्षत्र / Nakshatra:</span>
                    <span class="info-value">{girl_kundali.planets['MOON']['nakshatra']}</span>
                </div>
            </div>
        </div>

        <div class="footer">
            <div class="blessing">ॐ शुभ विवाह / Shubh Vivah ॐ</div>
            <div>Generated on {datetime.now().strftime('%d %B %Y')}</div>
        </div>
    </div>
</body>
</html>
"""
    return html
