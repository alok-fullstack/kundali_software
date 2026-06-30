"""
Muhurta HTML Generator
Generates beautiful HTML reports for Muhurta (auspicious timing) results
"""

from datetime import datetime
from typing import List, Optional
import os

from .kundali import Kundali
from .muhurta import MuhurtaCalculator, MuhurtaWindow, EventType
from .panchang import PanchangCalculator


def generate_muhurta_html(
    kundali: Kundali,
    event_type: str,
    start_date: datetime,
    end_date: datetime,
    output_path: str = None,
    top_n: int = 10,
    min_score: int = 50
) -> str:
    """
    Generate HTML report for Muhurta results.

    Args:
        kundali: Birth chart
        event_type: "marriage", "career", "property", "travel", "griha_pravesh"
        start_date: Start of search range
        end_date: End of search range
        output_path: Path to save HTML (optional)
        top_n: Number of muhurtas to show
        min_score: Minimum score threshold

    Returns:
        HTML string (also saves to file if output_path provided)
    """
    event_map = {
        "marriage": EventType.MARRIAGE,
        "career": EventType.CAREER,
        "property": EventType.PROPERTY,
        "travel": EventType.TRAVEL,
        "griha_pravesh": EventType.GRIHA_PRAVESH,
    }
    event = event_map.get(event_type.lower(), EventType.MARRIAGE)

    event_hindi = {
        "marriage": "विवाह मुहूर्त",
        "career": "करियर मुहूर्त",
        "property": "संपत्ति मुहूर्त",
        "travel": "यात्रा मुहूर्त",
        "griha_pravesh": "गृह प्रवेश मुहूर्त",
    }

    calc = MuhurtaCalculator(kundali)
    muhurtas = calc.find_muhurtas(
        event_type=event,
        start_date=start_date,
        end_date=end_date,
        use_event_predictor=True,
        min_score=min_score,
        top_n=top_n
    )

    panchang_calc = PanchangCalculator()
    today_panchang = panchang_calc.get_panchang(datetime.now())

    name = kundali.birth_data.name
    birth = kundali.birth_data

    html = f"""<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{event_hindi.get(event_type, 'मुहूर्त')} - {name}</title>
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
            font-size: 3em;
            margin-bottom: 10px;
        }}

        .header h1 {{
            font-size: 2em;
            margin-bottom: 10px;
        }}

        .header .subtitle {{
            font-size: 1.1em;
            opacity: 0.9;
        }}

        .section {{
            padding: 30px;
            border-bottom: 1px solid #eee;
        }}

        .section-title {{
            font-size: 1.5em;
            color: var(--primary);
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid var(--accent);
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .birth-info {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            background: var(--light);
            padding: 20px;
            border-radius: 10px;
        }}

        .birth-info-item {{
            text-align: center;
        }}

        .birth-info-item label {{
            font-size: 0.9em;
            color: #666;
            display: block;
        }}

        .birth-info-item value {{
            font-size: 1.1em;
            font-weight: 600;
            color: var(--secondary);
        }}

        .panchang-today {{
            background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}

        .panchang-today h3 {{
            color: var(--success);
            margin-bottom: 15px;
        }}

        .panchang-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
        }}

        .panchang-item {{
            background: white;
            padding: 10px;
            border-radius: 8px;
            text-align: center;
        }}

        .panchang-item label {{
            font-size: 0.8em;
            color: #666;
            display: block;
        }}

        .muhurta-card {{
            background: white;
            border: 2px solid #eee;
            border-radius: 15px;
            margin-bottom: 20px;
            overflow: hidden;
            transition: all 0.3s ease;
        }}

        .muhurta-card:hover {{
            border-color: var(--primary);
            box-shadow: 0 5px 20px rgba(255, 107, 53, 0.2);
        }}

        .muhurta-header {{
            background: linear-gradient(135deg, var(--light) 0%, #fff 100%);
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #eee;
        }}

        .muhurta-date {{
            font-size: 1.3em;
            font-weight: 700;
            color: var(--secondary);
        }}

        .muhurta-weekday {{
            font-size: 0.9em;
            color: #666;
        }}

        .muhurta-score {{
            background: linear-gradient(135deg, var(--success) 0%, #20c997 100%);
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            font-weight: 700;
            font-size: 1.2em;
        }}

        .muhurta-score.medium {{
            background: linear-gradient(135deg, var(--warning) 0%, #ffb300 100%);
            color: var(--dark);
        }}

        .muhurta-score.low {{
            background: linear-gradient(135deg, #6c757d 0%, #adb5bd 100%);
        }}

        .muhurta-body {{
            padding: 20px;
        }}

        .muhurta-details {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 15px;
        }}

        .detail-box {{
            background: var(--light);
            padding: 15px;
            border-radius: 10px;
        }}

        .detail-box label {{
            font-size: 0.85em;
            color: #666;
            display: block;
            margin-bottom: 5px;
        }}

        .detail-box value {{
            font-weight: 600;
            color: var(--secondary);
        }}

        .reasons {{
            margin-top: 15px;
        }}

        .reasons h4 {{
            color: var(--success);
            font-size: 0.95em;
            margin-bottom: 10px;
        }}

        .reason-list {{
            list-style: none;
        }}

        .reason-list li {{
            padding: 5px 0;
            padding-left: 20px;
            position: relative;
            font-size: 0.9em;
        }}

        .reason-list li:before {{
            content: "✓";
            position: absolute;
            left: 0;
            color: var(--success);
            font-weight: bold;
        }}

        .warnings {{
            margin-top: 15px;
            background: #fff3cd;
            padding: 15px;
            border-radius: 10px;
        }}

        .warnings h4 {{
            color: var(--warning);
            font-size: 0.95em;
            margin-bottom: 10px;
        }}

        .warning-list {{
            list-style: none;
        }}

        .warning-list li {{
            padding: 5px 0;
            padding-left: 20px;
            position: relative;
            font-size: 0.9em;
            color: #856404;
        }}

        .warning-list li:before {{
            content: "⚠";
            position: absolute;
            left: 0;
        }}

        .avoid-periods {{
            margin-top: 15px;
            background: #f8d7da;
            padding: 15px;
            border-radius: 10px;
        }}

        .avoid-periods h4 {{
            color: var(--danger);
            font-size: 0.95em;
            margin-bottom: 10px;
        }}

        .avoid-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}

        .avoid-tag {{
            background: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            border: 1px solid var(--danger);
            color: var(--danger);
        }}

        .no-muhurtas {{
            text-align: center;
            padding: 50px;
            color: #666;
        }}

        .footer {{
            background: var(--dark);
            color: white;
            padding: 20px;
            text-align: center;
            font-size: 0.9em;
        }}

        .compatibility-section {{
            display: flex;
            gap: 20px;
            margin-top: 15px;
        }}

        .compat-box {{
            flex: 1;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }}

        .compat-box.good {{
            background: #d4edda;
            border: 1px solid #c3e6cb;
        }}

        .compat-box.bad {{
            background: #f8d7da;
            border: 1px solid #f5c6cb;
        }}

        .compat-box.neutral {{
            background: #fff3cd;
            border: 1px solid #ffeeba;
        }}

        .compat-score {{
            font-size: 1.5em;
            font-weight: 700;
        }}

        .abhijit-badge {{
            background: linear-gradient(135deg, #ffd700 0%, #ffb300 100%);
            color: var(--dark);
            padding: 5px 15px;
            border-radius: 15px;
            font-size: 0.85em;
            font-weight: 600;
            margin-left: 10px;
        }}

        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            .container {{
                box-shadow: none;
            }}
            .muhurta-card {{
                break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="om">🙏 ॐ</div>
            <h1>{event_hindi.get(event_type, 'शुभ मुहूर्त')}</h1>
            <div class="subtitle">{name} के लिए शुभ समय</div>
            <div class="subtitle" style="margin-top: 10px; font-size: 0.9em;">
                {start_date.strftime('%d %b %Y')} से {end_date.strftime('%d %b %Y')} तक
            </div>
        </div>

        <div class="section">
            <div class="section-title">📋 जन्म विवरण</div>
            <div class="birth-info">
                <div class="birth-info-item">
                    <label>नाम</label>
                    <value>{name}</value>
                </div>
                <div class="birth-info-item">
                    <label>जन्म तिथि</label>
                    <value>{birth.date.strftime('%d-%m-%Y')}</value>
                </div>
                <div class="birth-info-item">
                    <label>जन्म समय</label>
                    <value>{birth.date.strftime('%H:%M')}</value>
                </div>
                <div class="birth-info-item">
                    <label>जन्म स्थान</label>
                    <value>{birth.city}</value>
                </div>
                <div class="birth-info-item">
                    <label>लग्न</label>
                    <value>{kundali.lagna['rashi']} ({kundali.lagna['rashi_english']})</value>
                </div>
                <div class="birth-info-item">
                    <label>चंद्र राशि</label>
                    <value>{kundali.planets['MOON']['rashi']}</value>
                </div>
                <div class="birth-info-item">
                    <label>जन्म नक्षत्र</label>
                    <value>{kundali.planets['MOON']['nakshatra']}</value>
                </div>
            </div>
        </div>

        <div class="section">
            <div class="section-title">📅 आज का पंचांग ({datetime.now().strftime('%d %b %Y')})</div>
            <div class="panchang-today">
                <div class="panchang-grid">
                    <div class="panchang-item">
                        <label>वार</label>
                        <value>{today_panchang.vara.english}</value>
                    </div>
                    <div class="panchang-item">
                        <label>तिथि</label>
                        <value>{today_panchang.tithi.name} ({today_panchang.tithi.paksha})</value>
                    </div>
                    <div class="panchang-item">
                        <label>नक्षत्र</label>
                        <value>{today_panchang.nakshatra.name}</value>
                    </div>
                    <div class="panchang-item">
                        <label>योग</label>
                        <value>{today_panchang.yoga.name}</value>
                    </div>
                    <div class="panchang-item">
                        <label>करण</label>
                        <value>{today_panchang.karana.name}</value>
                    </div>
                    <div class="panchang-item">
                        <label>सूर्योदय</label>
                        <value>{today_panchang.timings.sunrise.strftime('%H:%M')}</value>
                    </div>
                </div>
            </div>
        </div>

        <div class="section">
            <div class="section-title">🌟 शुभ मुहूर्त ({len(muhurtas)} परिणाम)</div>
"""

    if not muhurtas:
        html += """
            <div class="no-muhurtas">
                <h3>इस अवधि में कोई उपयुक्त मुहूर्त नहीं मिला</h3>
                <p>कृपया तिथि सीमा बढ़ाकर पुनः प्रयास करें</p>
            </div>
"""
    else:
        for i, m in enumerate(muhurtas, 1):
            score_class = "high" if m.score >= 70 else ("medium" if m.score >= 55 else "low")

            tarabala_class = "good" if m.tarabala_score >= 8 else ("bad" if m.tarabala_score == 0 else "neutral")
            chandrabala_class = "good" if m.chandrabala_score >= 8 else ("bad" if m.chandrabala_score == 0 else "neutral")

            html += f"""
            <div class="muhurta-card">
                <div class="muhurta-header">
                    <div>
                        <div class="muhurta-date">#{i} - {m.date.strftime('%d %B %Y')}</div>
                        <div class="muhurta-weekday">{m.panchang.vara.english} ({m.panchang.vara.name})</div>
                    </div>
                    <div class="muhurta-score {score_class}">{m.score}/100</div>
                </div>
                <div class="muhurta-body">
                    <div class="muhurta-details">
                        <div class="detail-box">
                            <label>समय</label>
                            <value>{m.start_time.strftime('%H:%M')} - {m.end_time.strftime('%H:%M')}</value>
                            {f'<span class="abhijit-badge">अभिजीत: {m.abhijit_muhurta[0].strftime("%H:%M")}-{m.abhijit_muhurta[1].strftime("%H:%M")}</span>' if m.abhijit_muhurta else ''}
                        </div>
                        <div class="detail-box">
                            <label>तिथि</label>
                            <value>{m.panchang.tithi.name} ({m.panchang.tithi.paksha} पक्ष)</value>
                        </div>
                        <div class="detail-box">
                            <label>नक्षत्र</label>
                            <value>{m.panchang.nakshatra.name} (पद {m.panchang.nakshatra.pada})</value>
                        </div>
                        <div class="detail-box">
                            <label>योग</label>
                            <value>{m.panchang.yoga.name} {'⚠️' if m.panchang.yoga.is_inauspicious else '✓'}</value>
                        </div>
                        <div class="detail-box">
                            <label>करण</label>
                            <value>{m.panchang.karana.name}</value>
                        </div>
                        <div class="detail-box">
                            <label>दशा</label>
                            <value>{m.dasha_info if m.dasha_info else 'N/A'}</value>
                        </div>
                    </div>

                    <div class="compatibility-section">
                        <div class="compat-box {tarabala_class}">
                            <label>ताराबल</label>
                            <div class="compat-score">{m.tarabala_score}/10</div>
                            <div>{m.tarabala_name}</div>
                        </div>
                        <div class="compat-box {chandrabala_class}">
                            <label>चंद्रबल</label>
                            <div class="compat-score">{m.chandrabala_score}/10</div>
                            <div>भाव {m.chandrabala_house}</div>
                        </div>
                    </div>
"""

            if m.reasons:
                html += """
                    <div class="reasons">
                        <h4>✓ अनुकूल कारण</h4>
                        <ul class="reason-list">
"""
                for reason in m.reasons[:5]:
                    html += f"                            <li>{reason}</li>\n"
                html += """                        </ul>
                    </div>
"""

            if m.warnings:
                html += """
                    <div class="warnings">
                        <h4>⚠ सावधानी</h4>
                        <ul class="warning-list">
"""
                for warning in m.warnings[:3]:
                    html += f"                            <li>{warning}</li>\n"
                html += """                        </ul>
                    </div>
"""

            html += """
                    <div class="avoid-periods">
                        <h4>🚫 इन समयों से बचें</h4>
                        <div class="avoid-list">
"""
            for p in m.inauspicious_periods:
                if p.severity == "high":
                    html += f'                            <span class="avoid-tag">{p.name}: {p.start_time.strftime("%H:%M")}-{p.end_time.strftime("%H:%M")}</span>\n'
            html += """                        </div>
                    </div>
                </div>
            </div>
"""

    html += f"""
        </div>

        <div class="footer">
            <p>🙏 शुभ मुहूर्त कैलकुलेटर | Swiss Ephemeris (NASA JPL DE431)</p>
            <p>Generated on {datetime.now().strftime('%d %B %Y, %H:%M')}</p>
            <p style="margin-top: 10px; font-size: 0.8em;">
                Based on: Muhurta Chintamani, Brihat Samhita, Phaladeepika
            </p>
        </div>
    </div>
</body>
</html>
"""

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Muhurta report saved: {output_path}")

    return html


def open_muhurta_in_browser(
    kundali: Kundali,
    event_type: str = "marriage",
    start_date: datetime = None,
    end_date: datetime = None,
    top_n: int = 10
):
    """
    Generate Muhurta HTML and open in browser.

    Args:
        kundali: Birth chart
        event_type: Type of event
        start_date: Start date (default: today)
        end_date: End date (default: 6 months from today)
        top_n: Number of muhurtas
    """
    import webbrowser
    import tempfile

    if start_date is None:
        start_date = datetime.now()
    if end_date is None:
        end_date = start_date + timedelta(days=180)

    from datetime import timedelta

    safe_name = "".join(c if c.isalnum() else "_" for c in kundali.birth_data.name)
    filename = f"Muhurta_{safe_name}_{event_type}.html"

    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(script_dir, filename)

    generate_muhurta_html(
        kundali=kundali,
        event_type=event_type,
        start_date=start_date,
        end_date=end_date,
        output_path=output_path,
        top_n=top_n
    )

    webbrowser.open(f'file://{output_path}')
    return output_path
