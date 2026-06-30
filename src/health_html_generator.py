"""
Health Predictions HTML Generator
Generates beautiful HTML reports for health and accident predictions
"""

from datetime import datetime
from typing import List

from .kundali import Kundali
from .health_predictor import HealthPredictor, HealthWarning, RiskLevel, HealthEventType


def generate_health_html(
    kundali: Kundali,
    start_year: int,
    end_year: int,
    min_risk_score: int = 35
) -> str:
    """
    Generate HTML report for health predictions.

    Args:
        kundali: Birth chart
        start_year: Start year for predictions
        end_year: End year for predictions
        min_risk_score: Minimum risk score threshold

    Returns:
        HTML string
    """
    predictor = HealthPredictor(kundali)
    warnings = predictor.predict_health_issues(start_year, end_year, min_risk_score)
    summary = predictor.get_health_summary(start_year, end_year)

    name = kundali.birth_data.name
    birth = kundali.birth_data

    risk_hindi = {
        "Critical": "गंभीर",
        "High": "उच्च",
        "Medium": "मध्यम",
        "Low": "निम्न"
    }

    event_hindi = {
        "Accident/Injury": "दुर्घटना/चोट",
        "Chronic Disease": "दीर्घकालिक रोग",
        "Surgery": "शल्य चिकित्सा",
        "Hospitalization": "अस्पताल में भर्ती",
        "Mental Stress": "मानसिक तनाव",
        "General Health Issue": "सामान्य स्वास्थ्य समस्या"
    }

    html = f"""<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>स्वास्थ्य विश्लेषण - {name}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;500;600;700&display=swap');

        :root {{
            --primary: #dc3545;
            --secondary: #6c757d;
            --success: #28a745;
            --warning: #ffc107;
            --danger: #dc3545;
            --critical: #721c24;
            --light: #fff5f5;
            --dark: #333;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Noto Sans Devanagari', sans-serif;
            background: linear-gradient(135deg, #fff5f5 0%, #ffe0e0 100%);
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
            background: linear-gradient(135deg, var(--danger) 0%, #c82333 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        .header .icon {{
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
            color: var(--danger);
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid var(--danger);
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

        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}

        .summary-box {{
            padding: 20px;
            border-radius: 15px;
            text-align: center;
        }}

        .summary-box.critical {{
            background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
            border: 2px solid var(--danger);
        }}

        .summary-box.high {{
            background: linear-gradient(135deg, #fff3cd 0%, #ffeeba 100%);
            border: 2px solid var(--warning);
        }}

        .summary-box.medium {{
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            border: 2px solid var(--success);
        }}

        .summary-box.total {{
            background: linear-gradient(135deg, #e2e3e5 0%, #d6d8db 100%);
            border: 2px solid var(--secondary);
        }}

        .summary-number {{
            font-size: 2.5em;
            font-weight: 700;
        }}

        .summary-label {{
            font-size: 0.9em;
            color: #666;
        }}

        .warning-card {{
            background: white;
            border: 2px solid #eee;
            border-radius: 15px;
            margin-bottom: 20px;
            overflow: hidden;
            transition: all 0.3s ease;
        }}

        .warning-card:hover {{
            box-shadow: 0 5px 20px rgba(220, 53, 69, 0.2);
        }}

        .warning-card.critical {{
            border-left: 5px solid var(--critical);
        }}

        .warning-card.high {{
            border-left: 5px solid var(--warning);
        }}

        .warning-card.medium {{
            border-left: 5px solid var(--success);
        }}

        .warning-header {{
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--light);
            border-bottom: 1px solid #eee;
        }}

        .warning-date {{
            font-size: 1.1em;
            font-weight: 600;
            color: var(--dark);
        }}

        .warning-dasha {{
            font-size: 0.9em;
            color: #666;
        }}

        .risk-badge {{
            padding: 8px 20px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.9em;
        }}

        .risk-badge.critical {{
            background: var(--critical);
            color: white;
        }}

        .risk-badge.high {{
            background: var(--warning);
            color: var(--dark);
        }}

        .risk-badge.medium {{
            background: var(--success);
            color: white;
        }}

        .warning-body {{
            padding: 20px;
        }}

        .event-type {{
            display: inline-block;
            padding: 5px 15px;
            background: #f8f9fa;
            border-radius: 20px;
            font-size: 0.9em;
            margin-bottom: 15px;
            border: 1px solid #ddd;
        }}

        .warning-details {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }}

        .detail-section {{
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
        }}

        .detail-section h4 {{
            font-size: 0.95em;
            color: var(--danger);
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 5px;
        }}

        .detail-list {{
            list-style: none;
        }}

        .detail-list li {{
            padding: 5px 0;
            font-size: 0.9em;
            padding-left: 15px;
            position: relative;
        }}

        .detail-list li:before {{
            content: "•";
            position: absolute;
            left: 0;
            color: var(--danger);
        }}

        .remedies-section {{
            background: #e8f5e9;
            padding: 15px;
            border-radius: 10px;
            margin-top: 15px;
        }}

        .remedies-section h4 {{
            color: var(--success);
            margin-bottom: 10px;
        }}

        .remedies-list {{
            list-style: none;
        }}

        .remedies-list li {{
            padding: 5px 0;
            font-size: 0.9em;
            padding-left: 20px;
            position: relative;
        }}

        .remedies-list li:before {{
            content: "✓";
            position: absolute;
            left: 0;
            color: var(--success);
            font-weight: bold;
        }}

        .advice-box {{
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            padding: 20px;
            border-radius: 15px;
            margin-top: 20px;
        }}

        .advice-box h4 {{
            color: #1565c0;
            margin-bottom: 15px;
        }}

        .no-warnings {{
            text-align: center;
            padding: 50px;
            color: var(--success);
        }}

        .no-warnings .icon {{
            font-size: 4em;
            margin-bottom: 20px;
        }}

        .footer {{
            background: var(--dark);
            color: white;
            padding: 20px;
            text-align: center;
            font-size: 0.9em;
        }}

        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            .container {{
                box-shadow: none;
            }}
            .warning-card {{
                break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="icon">⚠️</div>
            <h1>स्वास्थ्य एवं दुर्घटना विश्लेषण</h1>
            <div class="subtitle">{name} के लिए स्वास्थ्य पूर्वानुमान</div>
            <div class="subtitle" style="margin-top: 10px; font-size: 0.9em;">
                {start_year} से {end_year} तक
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
                    <value>{kundali.lagna['rashi']}</value>
                </div>
                <div class="birth-info-item">
                    <label>चंद्र राशि</label>
                    <value>{kundali.planets['MOON']['rashi']}</value>
                </div>
            </div>
        </div>

        <div class="section">
            <div class="section-title">📊 सारांश</div>
            <div class="summary-grid">
                <div class="summary-box total">
                    <div class="summary-number">{summary['total_warnings']}</div>
                    <div class="summary-label">कुल चेतावनियाँ</div>
                </div>
                <div class="summary-box critical">
                    <div class="summary-number">{summary['critical_periods']}</div>
                    <div class="summary-label">गंभीर अवधि</div>
                </div>
                <div class="summary-box high">
                    <div class="summary-number">{summary['high_risk_periods']}</div>
                    <div class="summary-label">उच्च जोखिम</div>
                </div>
                <div class="summary-box medium">
                    <div class="summary-number">{summary['medium_risk_periods']}</div>
                    <div class="summary-label">मध्यम जोखिम</div>
                </div>
            </div>
"""

    if summary.get('general_advice'):
        html += """
            <div class="advice-box">
                <h4>📝 सामान्य सलाह</h4>
                <ul class="detail-list">
"""
        for advice in summary['general_advice']:
            html += f"                    <li>{advice}</li>\n"
        html += """                </ul>
            </div>
"""

    html += """
        </div>

        <div class="section">
            <div class="section-title">⚠️ स्वास्थ्य चेतावनियाँ</div>
"""

    if not warnings:
        html += """
            <div class="no-warnings">
                <div class="icon">✅</div>
                <h3>इस अवधि में कोई महत्वपूर्ण स्वास्थ्य चिंता नहीं</h3>
                <p>आपकी कुंडली में इस समय सीमा के लिए कोई गंभीर स्वास्थ्य संकेत नहीं मिले</p>
            </div>
"""
    else:
        for i, w in enumerate(warnings[:15], 1):
            risk_class = w.risk_level.value.lower()
            risk_text = risk_hindi.get(w.risk_level.value, w.risk_level.value)
            event_text = event_hindi.get(w.event_type.value, w.event_type.value)

            html += f"""
            <div class="warning-card {risk_class}">
                <div class="warning-header">
                    <div>
                        <div class="warning-date">
                            {w.start_date.strftime('%d %b %Y')} - {w.end_date.strftime('%d %b %Y')}
                        </div>
                        <div class="warning-dasha">दशा: {w.dasha_info}</div>
                    </div>
                    <span class="risk-badge {risk_class}">{risk_text}</span>
                </div>
                <div class="warning-body">
                    <span class="event-type">{event_text}</span>

                    <div class="warning-details">
                        <div class="detail-section">
                            <h4>📌 कारण</h4>
                            <ul class="detail-list">
"""
            for reason in w.reasons[:4]:
                html += f"                                <li>{reason}</li>\n"

            html += """                            </ul>
                        </div>

                        <div class="detail-section">
                            <h4>🏥 प्रभावित अंग</h4>
                            <ul class="detail-list">
"""
            for part in w.affected_body_parts[:4]:
                html += f"                                <li>{part}</li>\n"

            html += """                            </ul>
                        </div>
                    </div>

                    <div class="remedies-section">
                        <h4>🙏 उपाय</h4>
                        <ul class="remedies-list">
"""
            for remedy in w.remedies[:4]:
                html += f"                            <li>{remedy}</li>\n"

            html += """                        </ul>
                    </div>
                </div>
            </div>
"""

    html += f"""
        </div>

        <div class="footer">
            <p>⚠️ स्वास्थ्य विश्लेषण | Vedic Astrology Health Predictor</p>
            <p>Generated on {datetime.now().strftime('%d %B %Y, %H:%M')}</p>
            <p style="margin-top: 10px; font-size: 0.8em;">
                Based on: Brihat Parashara Hora Shastra, Phaladeepika, Jataka Parijata
            </p>
            <p style="margin-top: 10px; font-size: 0.75em; opacity: 0.8;">
                Note: This is for informational purposes only. Please consult a medical professional for health concerns.
            </p>
        </div>
    </div>
</body>
</html>
"""

    return html
