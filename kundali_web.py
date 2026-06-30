"""
FULL DETAILED Kundali Web Application
Complete predictions with all sections
With AI Chat Assistant
"""

from flask import Flask, render_template_string, request, jsonify, session
from datetime import datetime
import secrets

from src.kundali import create_kundali
from src.config import RASHIS, PLANET_NAMES, Planet, BHAVA_NAMES
from src.predictions import GRAHA_BHAVA_PHAL, CAREER_BY_LAGNA, MARRIAGE_PREDICTIONS, CHILDREN_PREDICTIONS, HEALTH_PREDICTIONS, DASHA_EFFECTS
from src.full_predictions import (
    get_full_career_analysis, get_full_marriage_analysis,
    get_full_children_analysis, get_full_health_analysis,
    get_full_wealth_analysis, get_full_dasha_analysis,
    get_full_yoga_analysis, get_full_remedies, get_full_transit_analysis
)
from src.chat_assistant import KundaliChatAssistant
from src.muhurta import MuhurtaCalculator, EventType
from src.panchang import PanchangCalculator
from src.health_predictor import HealthPredictor


def calculate_career_rating(planets_in_houses):
    """Calculate career rating based on 10th house and related positions."""
    score = 3  # Base score
    tenth_planets = planets_in_houses.get(10, [])
    sixth_planets = planets_in_houses.get(6, [])

    # Benefics in 10th house increase score
    if "JUPITER" in tenth_planets or "VENUS" in tenth_planets:
        score += 1
    if "SUN" in tenth_planets:  # Authority
        score += 1
    # Malefics in 6th (enemies defeated)
    if "SATURN" in sixth_planets or "MARS" in sixth_planets:
        score += 0.5
    # Sun in good position
    sun_house = 0
    for h, p in planets_in_houses.items():
        if "SUN" in p:
            sun_house = h
    if sun_house in [1, 9, 10, 11]:
        score += 0.5

    return "⭐" * min(5, max(1, int(score)))


def calculate_marriage_rating(planets_in_houses):
    """Calculate marriage rating based on 7th house and Venus."""
    score = 3  # Base score
    seventh_planets = planets_in_houses.get(7, [])

    # Find Venus position
    venus_house = 0
    for h, p in planets_in_houses.items():
        if "VENUS" in p:
            venus_house = h

    # Venus in good houses
    if venus_house in [1, 2, 4, 5, 7, 9, 11]:
        score += 1
    # Jupiter aspects/placement
    jupiter_house = 0
    for h, p in planets_in_houses.items():
        if "JUPITER" in p:
            jupiter_house = h
    if jupiter_house in [1, 5, 7, 9, 11]:
        score += 0.5
    # Malefics in 7th reduce
    if "SATURN" in seventh_planets or "RAHU" in seventh_planets:
        score -= 0.5

    return "⭐" * min(5, max(1, int(score)))


def calculate_children_rating(planets_in_houses):
    """Calculate children rating based on 5th house and Jupiter."""
    score = 3  # Base score
    fifth_planets = planets_in_houses.get(5, [])

    # Jupiter position
    jupiter_house = 0
    for h, p in planets_in_houses.items():
        if "JUPITER" in p:
            jupiter_house = h

    if jupiter_house in [1, 2, 5, 9, 11]:
        score += 1
    # Benefics in 5th
    if "JUPITER" in fifth_planets or "VENUS" in fifth_planets:
        score += 1
    # Saturn in 5th causes delay
    if "SATURN" in fifth_planets:
        score -= 0.5

    return "⭐" * min(5, max(1, int(score)))


def calculate_health_rating(planets_in_houses):
    """Calculate health rating based on lagna, 6th and 8th houses."""
    score = 3  # Base score
    first_planets = planets_in_houses.get(1, [])
    sixth_planets = planets_in_houses.get(6, [])
    eighth_planets = planets_in_houses.get(8, [])

    # Benefics in lagna increase health
    if "JUPITER" in first_planets or "VENUS" in first_planets:
        score += 1
    # Too many planets in 6th/8th reduce
    if len(sixth_planets) >= 2:
        score -= 0.5
    if len(eighth_planets) >= 2:
        score -= 0.5
    # Moon well placed
    moon_house = 0
    for h, p in planets_in_houses.items():
        if "MOON" in p:
            moon_house = h
    if moon_house in [1, 4, 5, 9, 10]:
        score += 0.5

    return "⭐" * min(5, max(1, int(score)))


def calculate_wealth_rating(planets_in_houses):
    """Calculate wealth rating based on 2nd, 9th and 11th houses."""
    score = 3  # Base score
    second_planets = planets_in_houses.get(2, [])
    ninth_planets = planets_in_houses.get(9, [])
    eleventh_planets = planets_in_houses.get(11, [])

    # Multiple planets in 2nd (dhana yoga)
    if len(second_planets) >= 2:
        score += 1
    if len(second_planets) >= 3:
        score += 0.5
    # Jupiter/Venus in wealth houses
    if "JUPITER" in second_planets or "JUPITER" in ninth_planets or "JUPITER" in eleventh_planets:
        score += 0.5
    if "VENUS" in second_planets or "VENUS" in eleventh_planets:
        score += 0.5
    # 11th house strength
    if len(eleventh_planets) >= 1:
        score += 0.5

    return "⭐" * min(5, max(1, int(score)))


app = Flask(__name__)
app.secret_key = 'kundali-app-dev-secret-key-2024'  # Fixed key for session persistence across restarts

# Store kundalis temporarily (in production use Redis/DB)
kundali_store = {}

def get_or_recreate_kundali(kundali_id):
    """Get kundali from store, or recreate from session params if server restarted."""
    if kundali_id in kundali_store:
        return kundali_store[kundali_id]

    # Try to recreate from session (survives server restarts)
    session_params = session.get('kundali_params', {})
    if kundali_id in session_params:
        params = session_params[kundali_id]
        kundali = create_kundali(**params)
        kundali_store[kundali_id] = kundali
        return kundali

    return None

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>विस्तृत कुंडली जनरेटर</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;500;600;700&display=swap');

        :root {
            --primary: #ff6b35;
            --secondary: #8b4513;
            --accent: #f7931e;
            --success: #28a745;
            --warning: #ffc107;
            --danger: #dc3545;
            --light: #fff8f0;
            --dark: #333;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Noto Sans Devanagari', sans-serif;
            background: linear-gradient(135deg, #fff5e6 0%, #ffe4c4 100%);
            min-height: 100vh;
            padding: 20px;
            color: var(--dark);
            line-height: 1.7;
        }

        .container { max-width: 1100px; margin: 0 auto; }

        .header {
            background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
            color: white;
            padding: 35px;
            border-radius: 20px 20px 0 0;
            text-align: center;
        }

        .header .om { font-size: 3.5em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
        .header h1 { font-size: 2.2em; margin-bottom: 5px; }

        .form-section {
            background: white;
            padding: 30px;
            border-radius: 0 0 20px 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
            margin-bottom: 30px;
        }

        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }

        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; color: var(--secondary); }
        .form-group input, .form-group select {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            font-family: inherit;
        }
        .form-group input:focus, .form-group select:focus { border-color: var(--primary); outline: none; }

        .submit-btn {
            background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            margin-top: 20px;
            transition: transform 0.2s;
        }
        .submit-btn:hover { transform: scale(1.02); }
        .submit-btn:disabled { background: #ccc; cursor: not-allowed; }

        .loading { text-align: center; padding: 40px; display: none; }
        .loading.show { display: block; }

        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid var(--primary);
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

        .results { display: none; background: white; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.15); overflow: hidden; margin-bottom: 30px; }
        .results.show { display: block; }

        .results-header {
            background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }

        .section { padding: 25px; border-bottom: 1px solid #eee; }
        .section:last-child { border-bottom: none; }

        .section-title {
            color: var(--primary);
            font-size: 1.5em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid var(--primary);
        }

        /* Detail boxes */
        .detail-box {
            background: var(--light);
            border-radius: 12px;
            padding: 20px;
            margin: 15px 0;
            border-left: 5px solid var(--primary);
        }
        .detail-box h3 { color: var(--secondary); margin-bottom: 15px; font-size: 1.2em; }
        .detail-box.highlight-green { background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); border-left-color: var(--success); }
        .detail-box.highlight-gold { background: linear-gradient(135deg, #fff3cd 0%, #ffeeba 100%); border-left-color: var(--warning); }
        .detail-box.highlight-blue { background: linear-gradient(135deg, #cce5ff 0%, #b8daff 100%); border-left-color: #007bff; }
        .detail-box.highlight-yellow { background: linear-gradient(135deg, #fff3cd 0%, #ffeeba 100%); border-left-color: var(--warning); }

        /* Tables */
        .detail-table { width: 100%; border-collapse: collapse; margin: 10px 0; }
        .detail-table th { background: var(--primary); color: white; padding: 12px; text-align: left; }
        .detail-table td { padding: 10px 12px; border-bottom: 1px solid #ddd; }
        .detail-table tr:nth-child(even) { background: rgba(255,255,255,0.5); }
        .detail-table tr:hover { background: rgba(255,107,53,0.1); }
        .detail-table .highlight-row { background: #fff3cd !important; font-weight: 600; }

        /* Prediction list */
        .prediction-list { list-style: none; padding: 0; }
        .prediction-list li { padding: 8px 0 8px 25px; position: relative; border-bottom: 1px dotted #ddd; }
        .prediction-list li:last-child { border-bottom: none; }
        .prediction-list li::before { content: "•"; color: var(--primary); font-weight: bold; position: absolute; left: 5px; }

        /* Status */
        .status-good { color: var(--success); font-weight: 600; }
        .status-warning { color: #856404; font-weight: 600; }
        .status-caution { color: var(--danger); font-weight: 600; }

        /* Birth grid */
        .birth-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 15px; }
        .birth-item { background: var(--light); padding: 15px; border-radius: 10px; border-left: 4px solid var(--primary); }
        .birth-item .label { color: #666; font-size: 0.85em; }
        .birth-item .value { font-size: 1.1em; font-weight: 600; margin-top: 5px; }

        /* Chart */
        .chart-container { display: flex; justify-content: center; margin: 20px 0; overflow-x: auto; }
        .chart-table { border-collapse: collapse; }
        .chart-table td { width: 95px; height: 95px; border: 2px solid var(--secondary); background: var(--light); vertical-align: top; padding: 6px; font-size: 0.85em; }
        .chart-table .rashi-name { color: var(--primary); font-weight: 600; }
        .chart-table .house-num { color: #666; font-size: 0.75em; }
        .chart-table .lagna-cell { background: #fff3cd; border: 3px solid var(--primary); }

        /* Yoga cards */
        .yoga-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; }
        .yoga-card { background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 10px; padding: 15px; border-left: 4px solid #6c757d; }
        .yoga-card.active { background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); border-left-color: var(--success); }
        .yoga-card h4 { color: var(--secondary); margin-bottom: 10px; }
        .yoga-card ul { font-size: 0.9em; margin-left: 15px; }

        /* Summary */
        .summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; }
        .summary-card { background: var(--light); padding: 20px; border-radius: 10px; text-align: center; border-top: 4px solid var(--primary); }
        .summary-card .rating { font-size: 1.3em; color: var(--accent); margin-bottom: 5px; }

        /* Planet effect */
        .planet-effect { background: white; padding: 10px; border-radius: 8px; margin: 10px 0; border-left: 3px solid var(--accent); }

        /* Action buttons */
        .action-buttons { text-align: center; padding: 20px; }
        .print-btn, .new-btn { padding: 12px 30px; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; margin: 5px; }
        .print-btn { background: var(--secondary); color: white; }
        .new-btn { background: var(--success); color: white; }

        /* Warning */
        .warning { background: #fff3cd; padding: 10px; border-radius: 5px; border-left: 4px solid var(--warning); margin: 10px 0; }

        /* Footer */
        .footer { background: var(--dark); color: white; padding: 25px; text-align: center; }
        .footer p { margin: 5px 0; opacity: 0.9; }

        /* Chat Assistant Styles */
        .chat-container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
            margin: 30px 0;
            overflow: hidden;
            display: none;
        }
        .chat-container.show { display: block; }

        .chat-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }
        .chat-header h3 { margin: 0; font-size: 1.4em; }
        .chat-header p { margin: 5px 0 0; opacity: 0.9; font-size: 0.9em; }

        .chat-messages {
            height: 400px;
            overflow-y: auto;
            padding: 20px;
            background: #f8f9fa;
        }

        .chat-message {
            margin: 15px 0;
            display: flex;
            flex-direction: column;
        }
        .chat-message.user { align-items: flex-end; }
        .chat-message.bot { align-items: flex-start; }

        .message-bubble {
            max-width: 80%;
            padding: 15px 20px;
            border-radius: 20px;
            line-height: 1.6;
        }
        .chat-message.user .message-bubble {
            background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
            color: white;
            border-bottom-right-radius: 5px;
        }
        .chat-message.bot .message-bubble {
            background: white;
            border: 1px solid #ddd;
            border-bottom-left-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }

        .chat-input-container {
            display: flex;
            padding: 20px;
            background: white;
            border-top: 1px solid #eee;
        }

        .chat-input {
            flex: 1;
            padding: 15px 20px;
            border: 2px solid #ddd;
            border-radius: 25px;
            font-size: 16px;
            font-family: inherit;
            outline: none;
        }
        .chat-input:focus { border-color: #667eea; }

        .chat-send {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 25px;
            border-radius: 25px;
            margin-left: 10px;
            cursor: pointer;
            font-size: 16px;
            transition: transform 0.2s;
        }
        .chat-send:hover { transform: scale(1.05); }

        .quick-questions {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            padding: 15px 20px;
            background: #f0f0f0;
            border-top: 1px solid #ddd;
        }
        .quick-btn {
            background: white;
            border: 1px solid #ddd;
            padding: 8px 15px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 14px;
            font-family: inherit;
            transition: all 0.2s;
        }
        .quick-btn:hover { background: #667eea; color: white; border-color: #667eea; }

        .typing-indicator {
            display: none;
            padding: 15px 20px;
        }
        .typing-indicator.show { display: flex; }
        .typing-indicator span {
            width: 10px;
            height: 10px;
            background: #667eea;
            border-radius: 50%;
            margin: 0 3px;
            animation: typing 1s infinite;
        }
        .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
        .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
        @keyframes typing {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-8px); }
        }

        @media print { .form-section, .action-buttons, .chat-container { display: none; } body { background: white; } }
        @media (max-width: 600px) { .header h1 { font-size: 1.5em; } .chart-table td { width: 70px; height: 70px; font-size: 0.7em; } .message-bubble { max-width: 90%; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="form-section" id="formSection">
            <div class="header">
                <div class="om">ॐ</div>
                <h1>विस्तृत कुंडली जनरेटर</h1>
                <p>Complete Kundali with Full Predictions</p>
            </div>
            <form id="kundaliForm" style="padding: 20px;">
                <div class="form-grid">
                    <div class="form-group">
                        <label>नाम (Name) *</label>
                        <input type="text" id="name" required placeholder="Enter name">
                    </div>
                    <div class="form-group">
                        <label>जन्म तिथि (Date of Birth) *</label>
                        <input type="date" id="dob" required>
                    </div>
                    <div class="form-group">
                        <label>जन्म समय (Time of Birth) *</label>
                        <input type="time" id="tob" required>
                    </div>
                    <div class="form-group">
                        <label>जन्म स्थान (Place of Birth) *</label>
                        <input type="text" id="city" required placeholder="e.g., Delhi, Mumbai">
                    </div>
                    <div class="form-group">
                        <label>अक्षांश (Latitude) - Optional</label>
                        <input type="number" id="latitude" step="0.0001" placeholder="e.g., 28.6139">
                    </div>
                    <div class="form-group">
                        <label>देशांतर (Longitude) - Optional</label>
                        <input type="number" id="longitude" step="0.0001" placeholder="e.g., 77.2090">
                    </div>
                </div>
                <button type="submit" class="submit-btn" id="submitBtn">🔮 विस्तृत कुंडली बनाएं</button>
            </form>
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>विस्तृत कुंडली बना रहे हैं... Please wait...</p>
            </div>
        </div>
        <div class="results" id="results"></div>

        <!-- AI Chat Assistant -->
        <div class="chat-container" id="chatContainer">
            <div class="chat-header">
                <h3>🤖 AI Kundali Assistant</h3>
                <p>Apni kundali ke baare mein kuch bhi puchiye!</p>
            </div>
            <div class="chat-messages" id="chatMessages">
                <div class="chat-message bot">
                    <div class="message-bubble">
                        <b>Namaste! Main aapka Kundali Assistant hoon.</b><br><br>
                        Aap mujhse apni kundali ke baare mein kuch bhi puch sakte hain jaise:<br>
                        - Career ke baare mein batao<br>
                        - Shaadi kab hogi?<br>
                        - Health kaisi rahegi?<br>
                        - Shani ka prabhav kya hai?<br><br>
                        Neeche quick buttons bhi hain ya apna sawaal type karein!
                    </div>
                </div>
            </div>
            <div class="typing-indicator" id="typingIndicator">
                <span></span><span></span><span></span>
            </div>
            <div class="quick-questions">
                <button class="quick-btn" onclick="askQuestion('Career ke baare mein batao')">💼 Career</button>
                <button class="quick-btn" onclick="askQuestion('Shaadi kab hogi?')">💑 Shaadi</button>
                <button class="quick-btn" onclick="askQuestion('Bachche ke baare mein')">👶 Santan</button>
                <button class="quick-btn" onclick="askQuestion('Health kaisi rahegi?')">🏥 Health</button>
                <button class="quick-btn" onclick="askQuestion('Dhan ke baare mein batao')">💰 Dhan</button>
                <button class="quick-btn" onclick="askQuestion('Dasha ka prabhav?')">📅 Dasha</button>
                <button class="quick-btn" onclick="askQuestion('Gochar ke baare mein batao')">🌍 Transit</button>
                <button class="quick-btn" onclick="askQuestion('Sade sati ke baare mein batao')">⚠️ Sade Sati</button>
                <button class="quick-btn" onclick="askQuestion('Shubh ratna konsa hai?')">💎 Ratna</button>
                <button class="quick-btn" onclick="askQuestion('Upay batao')">🙏 Upay</button>
            </div>
            <div class="chat-input-container">
                <input type="text" class="chat-input" id="chatInput" placeholder="Apna sawaal yahan likhein..." onkeypress="if(event.key==='Enter')sendMessage()">
                <button class="chat-send" onclick="sendMessage()">भेजें ➤</button>
            </div>
        </div>
    </div>
    <script>
        let currentKundaliId = null;
        document.getElementById('kundaliForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const submitBtn = document.getElementById('submitBtn');
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            const data = {
                name: document.getElementById('name').value,
                dob: document.getElementById('dob').value,
                tob: document.getElementById('tob').value,
                city: document.getElementById('city').value,
                latitude: document.getElementById('latitude').value || null,
                longitude: document.getElementById('longitude').value || null
            };
            submitBtn.disabled = true;
            loading.classList.add('show');
            results.classList.remove('show');
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                const result = await response.json();
                if (result.success) {
                    results.innerHTML = result.html;
                    results.classList.add('show');
                    currentKundaliId = result.kundali_id;
                    const personName = data.name;
                    // Clear previous chat and show fresh welcome with person's name
                    document.getElementById('chatMessages').innerHTML = `
                        <div class="chat-message bot">
                            <div class="message-bubble">
                                <b>Namaste! Main aapka Kundali Assistant hoon.</b><br><br>
                                <b style="color:#ff6b35;">${personName}</b> ki kundali taiyaar ho gayi hai!<br><br>
                                Ab aap <b>${personName}</b> ke baare mein kuch bhi puch sakte hain:<br>
                                - Career ke baare mein batao<br>
                                - Shaadi kab hogi?<br>
                                - Health kaisi rahegi?<br>
                                - Shani ka prabhav kya hai?<br><br>
                                Neeche quick buttons click karein ya apna sawaal type karein!
                            </div>
                        </div>
                    `;
                    document.getElementById('chatContainer').classList.add('show');
                    results.scrollIntoView({ behavior: 'smooth' });
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                alert('Error: ' + error.message);
            } finally {
                submitBtn.disabled = false;
                loading.classList.remove('show');
            }
        });
        function printKundali() { window.print(); }
        function newKundali() {
            document.getElementById('results').classList.remove('show');
            document.getElementById('chatContainer').classList.remove('show');
            document.getElementById('chatMessages').innerHTML = `
                <div class="chat-message bot">
                    <div class="message-bubble">
                        <b>Namaste! Main aapka Kundali Assistant hoon.</b><br><br>
                        Aap mujhse apni kundali ke baare mein kuch bhi puch sakte hain jaise:<br>
                        - Career ke baare mein batao<br>
                        - Shaadi kab hogi?<br>
                        - Health kaisi rahegi?<br>
                        - Shani ka prabhav kya hai?<br><br>
                        Neeche quick buttons bhi hain ya apna sawaal type karein!
                    </div>
                </div>
            `;
            currentKundaliId = null;
            document.getElementById('kundaliForm').reset();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        function askQuestion(question) {
            document.getElementById('chatInput').value = question;
            sendMessage();
        }

        // Muhurta Functions
        function showMuhurtaModal() {
            if (!currentKundaliId) {
                alert('Pehle apni Kundali banayein!');
                return;
            }
            document.getElementById('muhurtaModal').style.display = 'block';
            document.getElementById('muhurtaResults').innerHTML = '';
        }

        function closeMuhurtaModal() {
            document.getElementById('muhurtaModal').style.display = 'none';
        }

        async function findMuhurta() {
            const eventType = document.getElementById('muhurtaEventType').value;
            const year = document.getElementById('muhurtaYear').value;
            const loading = document.getElementById('muhurtaLoading');
            const results = document.getElementById('muhurtaResults');

            loading.style.display = 'block';
            results.innerHTML = '';

            try {
                const response = await fetch('/muhurta', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        kundali_id: currentKundaliId,
                        event_type: eventType,
                        year: year
                    })
                });
                const result = await response.json();

                loading.style.display = 'none';

                if (result.success) {
                    results.innerHTML = result.html;
                } else {
                    results.innerHTML = '<p style="color:red; text-align:center;">Error: ' + result.error + '</p>';
                }
            } catch (error) {
                loading.style.display = 'none';
                results.innerHTML = '<p style="color:red; text-align:center;">Error: ' + error.message + '</p>';
            }
        }

        // Close modal on outside click
        document.getElementById('muhurtaModal')?.addEventListener('click', function(e) {
            if (e.target === this) closeMuhurtaModal();
        });

        // Health Functions
        function showHealthModal() {
            if (!currentKundaliId) {
                alert('Pehle apni Kundali banayein!');
                return;
            }
            document.getElementById('healthModal').style.display = 'block';
            document.getElementById('healthResults').innerHTML = '';
        }

        function closeHealthModal() {
            document.getElementById('healthModal').style.display = 'none';
        }

        async function findHealthRisks() {
            const startYear = document.getElementById('healthStartYear').value;
            const endYear = document.getElementById('healthEndYear').value;
            const loading = document.getElementById('healthLoading');
            const results = document.getElementById('healthResults');

            loading.style.display = 'block';
            results.innerHTML = '';

            try {
                const response = await fetch('/health', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        kundali_id: currentKundaliId,
                        start_year: startYear,
                        end_year: endYear
                    })
                });
                const result = await response.json();

                loading.style.display = 'none';

                if (result.success) {
                    results.innerHTML = result.html;
                } else {
                    results.innerHTML = '<p style="color:red; text-align:center;">Error: ' + result.error + '</p>';
                }
            } catch (error) {
                loading.style.display = 'none';
                results.innerHTML = '<p style="color:red; text-align:center;">Error: ' + error.message + '</p>';
            }
        }

        // Close health modal on outside click
        document.getElementById('healthModal')?.addEventListener('click', function(e) {
            if (e.target === this) closeHealthModal();
        });

        async function sendMessage() {
            const input = document.getElementById('chatInput');
            const message = input.value.trim();
            if (!message || !currentKundaliId) return;

            const messagesDiv = document.getElementById('chatMessages');
            const typingIndicator = document.getElementById('typingIndicator');

            // Add user message
            messagesDiv.innerHTML += `
                <div class="chat-message user">
                    <div class="message-bubble">${message}</div>
                </div>
            `;
            input.value = '';
            messagesDiv.scrollTop = messagesDiv.scrollHeight;

            // Show typing indicator
            typingIndicator.classList.add('show');

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question: message, kundali_id: currentKundaliId })
                });
                const result = await response.json();

                typingIndicator.classList.remove('show');

                // Add bot response
                messagesDiv.innerHTML += `
                    <div class="chat-message bot">
                        <div class="message-bubble">${result.answer}</div>
                    </div>
                `;
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            } catch (error) {
                typingIndicator.classList.remove('show');
                messagesDiv.innerHTML += `
                    <div class="chat-message bot">
                        <div class="message-bubble">Sorry, kuch gadbad ho gayi. Please dobara try karein.</div>
                    </div>
                `;
            }
        }
    </script>
</body>
</html>
'''


def generate_full_result_html(kundali):
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

    rashi_hindi = {
        "Mesha": "मेष", "Vrishabha": "वृषभ", "Mithuna": "मिथुन", "Karka": "कर्क",
        "Simha": "सिंह", "Kanya": "कन्या", "Tula": "तुला", "Vrishchika": "वृश्चिक",
        "Dhanu": "धनु", "Makara": "मकर", "Kumbha": "कुंभ", "Meena": "मीन"
    }

    # Generate chart
    chart_html = generate_chart(kundali, planets_in_houses, lagna_num)

    # Generate planet rows
    planet_rows = ""
    for p_name in ["SUN", "MOON", "MARS", "MERCURY", "JUPITER", "VENUS", "SATURN", "RAHU", "KETU"]:
        data = planets[p_name]
        hindi = PLANET_NAMES[Planet[p_name]]["hindi"]
        symbol = PLANET_NAMES[Planet[p_name]]["symbol"]
        rashi = rashi_hindi.get(data['rashi'], data['rashi'])
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
        rashi = rashi_hindi.get(house_rashis[h]['name'], house_rashis[h]['name'])
        p_str = ', '.join([PLANET_NAMES[Planet[p]]["hindi"] for p in p_list]) if p_list else '-'
        bhava_rows += f'<tr><td>{h} ({BHAVA_NAMES[h]["name"]})</td><td>{rashi}</td><td>{p_str}</td><td>{bhava_significance[h]}</td></tr>'

    # Get full predictions
    career_html = get_full_career_analysis(kundali, planets_in_houses, house_rashis, rashi_hindi)
    marriage_html = get_full_marriage_analysis(kundali, planets_in_houses, house_rashis, rashi_hindi)
    children_html = get_full_children_analysis(kundali, planets_in_houses, house_rashis, rashi_hindi)
    health_html = get_full_health_analysis(kundali, planets_in_houses, house_rashis, rashi_hindi)
    wealth_html = get_full_wealth_analysis(kundali, planets_in_houses, house_rashis, rashi_hindi)
    dasha_html = get_full_dasha_analysis(kundali, mahadashas, current_dasha)
    yoga_html = get_full_yoga_analysis(kundali, planets_in_houses)
    remedies_html = get_full_remedies(kundali, planets_in_houses)

    # Get transit analysis (with graceful fallback)
    try:
        transit_html = get_full_transit_analysis(kundali, planets_in_houses, house_rashis, rashi_hindi)
    except Exception as e:
        transit_html = f'''
        <div class="detail-box">
            <p>Transit analysis temporarily unavailable.</p>
        </div>
        '''

    html = f'''
    <div class="results-header">
        <div style="font-size: 2.5em;">ॐ</div>
        <h2>विस्तृत जन्म कुंडली</h2>
        <h2>{birth.name}</h2>
    </div>

    <div class="action-buttons">
        <button class="print-btn" onclick="printKundali()">🖨️ Print</button>
        <button class="new-btn" onclick="newKundali()">➕ New Kundali</button>
        <button class="muhurta-btn" onclick="showMuhurtaModal()" style="background: linear-gradient(135deg, #9c27b0 0%, #673ab7 100%);">🌟 शुभ मुहूर्त</button>
        <button class="health-btn" onclick="showHealthModal()" style="background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);">⚠️ स्वास्थ्य/दुर्घटना</button>
    </div>

    <!-- Muhurta Modal -->
    <div id="muhurtaModal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:1000; overflow-y:auto;">
        <div style="max-width:900px; margin:50px auto; background:white; border-radius:15px; overflow:hidden;">
            <div style="background:linear-gradient(135deg, #9c27b0 0%, #673ab7 100%); color:white; padding:20px; display:flex; justify-content:space-between; align-items:center;">
                <h2>🌟 शुभ मुहूर्त खोजें</h2>
                <button onclick="closeMuhurtaModal()" style="background:none; border:none; color:white; font-size:1.5em; cursor:pointer;">✕</button>
            </div>
            <div style="padding:20px;">
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:15px; margin-bottom:20px;">
                    <div>
                        <label style="display:block; margin-bottom:5px; font-weight:600;">कार्य का प्रकार</label>
                        <select id="muhurtaEventType" style="width:100%; padding:10px; border:2px solid #ddd; border-radius:8px;">
                            <option value="marriage">विवाह (Marriage)</option>
                            <option value="career">करियर (Career/Job)</option>
                            <option value="property">संपत्ति (Property)</option>
                            <option value="griha_pravesh">गृह प्रवेश (House Warming)</option>
                            <option value="travel">यात्रा (Travel)</option>
                        </select>
                    </div>
                    <div>
                        <label style="display:block; margin-bottom:5px; font-weight:600;">वर्ष</label>
                        <select id="muhurtaYear" style="width:100%; padding:10px; border:2px solid #ddd; border-radius:8px;">
                            <option value="2025">2025</option>
                            <option value="2026">2026</option>
                            <option value="2027" selected>2027</option>
                            <option value="2028">2028</option>
                            <option value="2029">2029</option>
                            <option value="2030">2030</option>
                        </select>
                    </div>
                </div>
                <button onclick="findMuhurta()" style="width:100%; padding:12px; background:linear-gradient(135deg, #9c27b0 0%, #673ab7 100%); color:white; border:none; border-radius:8px; font-size:1.1em; cursor:pointer;">🔍 मुहूर्त खोजें</button>
                <div id="muhurtaLoading" style="display:none; text-align:center; padding:30px;">
                    <div style="border:4px solid #f3f3f3; border-top:4px solid #9c27b0; border-radius:50%; width:40px; height:40px; animation:spin 1s linear infinite; margin:0 auto 15px;"></div>
                    <p>मुहूर्त खोज रहे हैं...</p>
                </div>
                <div id="muhurtaResults" style="margin-top:20px;"></div>
            </div>
        </div>
    </div>

    <!-- Health Modal -->
    <div id="healthModal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:1000; overflow-y:auto;">
        <div style="max-width:900px; margin:50px auto; background:white; border-radius:15px; overflow:hidden;">
            <div style="background:linear-gradient(135deg, #dc3545 0%, #c82333 100%); color:white; padding:20px; display:flex; justify-content:space-between; align-items:center;">
                <h2>⚠️ स्वास्थ्य एवं दुर्घटना विश्लेषण</h2>
                <button onclick="closeHealthModal()" style="background:none; border:none; color:white; font-size:1.5em; cursor:pointer;">✕</button>
            </div>
            <div style="padding:20px;">
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:15px; margin-bottom:20px;">
                    <div>
                        <label style="display:block; margin-bottom:5px; font-weight:600;">प्रारंभ वर्ष</label>
                        <select id="healthStartYear" style="width:100%; padding:10px; border:2px solid #ddd; border-radius:8px;">
                            <option value="2025">2025</option>
                            <option value="2026" selected>2026</option>
                            <option value="2027">2027</option>
                            <option value="2028">2028</option>
                        </select>
                    </div>
                    <div>
                        <label style="display:block; margin-bottom:5px; font-weight:600;">अंत वर्ष</label>
                        <select id="healthEndYear" style="width:100%; padding:10px; border:2px solid #ddd; border-radius:8px;">
                            <option value="2028">2028</option>
                            <option value="2029">2029</option>
                            <option value="2030" selected>2030</option>
                            <option value="2035">2035</option>
                        </select>
                    </div>
                </div>
                <button onclick="findHealthRisks()" style="width:100%; padding:12px; background:linear-gradient(135deg, #dc3545 0%, #c82333 100%); color:white; border:none; border-radius:8px; font-size:1.1em; cursor:pointer;">🔍 विश्लेषण करें</button>
                <div id="healthLoading" style="display:none; text-align:center; padding:30px;">
                    <div style="border:4px solid #f3f3f3; border-top:4px solid #dc3545; border-radius:50%; width:40px; height:40px; animation:spin 1s linear infinite; margin:0 auto 15px;"></div>
                    <p>विश्लेषण कर रहे हैं...</p>
                </div>
                <div id="healthResults" style="margin-top:20px;"></div>
            </div>
        </div>
    </div>

    <div class="section">
        <h2 class="section-title">🪔 जन्म विवरण (Birth Details)</h2>
        <div class="birth-grid">
            <div class="birth-item"><div class="label">नाम</div><div class="value">{birth.name}</div></div>
            <div class="birth-item"><div class="label">जन्म तिथि</div><div class="value">{birth.date.strftime('%d-%m-%Y')}</div></div>
            <div class="birth-item"><div class="label">जन्म समय</div><div class="value">{birth.date.strftime('%I:%M %p')}</div></div>
            <div class="birth-item"><div class="label">जन्म स्थान</div><div class="value">{birth.city}</div></div>
            <div class="birth-item"><div class="label">लग्न राशि</div><div class="value">{rashi_hindi.get(lagna['rashi'], lagna['rashi'])} ({lagna['rashi_english']})</div></div>
            <div class="birth-item"><div class="label">चंद्र राशि</div><div class="value">{rashi_hindi.get(planets['MOON']['rashi'], planets['MOON']['rashi'])}</div></div>
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


def generate_chart(kundali, planets_in_houses, lagna_num):
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


@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)


@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        dob = data['dob'].split('-')
        tob = data['tob'].split(':')
        year, month, day = int(dob[0]), int(dob[1]), int(dob[2])
        hour, minute = int(tob[0]), int(tob[1])

        # Build params dict for storage
        params = {
            'name': data['name'],
            'year': year,
            'month': month,
            'day': day,
            'hour': hour,
            'minute': minute,
            'city': data['city']
        }
        if data.get('latitude') and data.get('longitude'):
            params['latitude'] = float(data['latitude'])
            params['longitude'] = float(data['longitude'])

        kundali = create_kundali(**params)

        # Store kundali in memory and params in session (for recreation after restart)
        kundali_id = secrets.token_hex(8)
        kundali_store[kundali_id] = kundali

        # Store params in session for persistence across server restarts
        if 'kundali_params' not in session:
            session['kundali_params'] = {}
        session['kundali_params'][kundali_id] = params
        session.modified = True

        result_html = generate_full_result_html(kundali)
        return jsonify({'success': True, 'html': result_html, 'kundali_id': kundali_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        question = data.get('question', '')
        kundali_id = data.get('kundali_id', '')

        kundali = get_or_recreate_kundali(kundali_id) if kundali_id else None
        if not kundali:
            return jsonify({'answer': 'Kundali nahi mili. Pehle apni kundali banayein.'})

        assistant = KundaliChatAssistant(kundali)
        answer = assistant.get_response(question)

        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'answer': f'Error: {str(e)}'})


@app.route('/muhurta', methods=['POST'])
def muhurta():
    """Generate Muhurta (auspicious timing) results."""
    try:
        data = request.json
        kundali_id = data.get('kundali_id', '')
        event_type = data.get('event_type', 'marriage')
        year = int(data.get('year', datetime.now().year + 1))

        kundali = get_or_recreate_kundali(kundali_id) if kundali_id else None
        if not kundali:
            return jsonify({'success': False, 'error': 'Kundali not found. Please generate kundali first.'})

        event_map = {
            'marriage': EventType.MARRIAGE,
            'career': EventType.CAREER,
            'property': EventType.PROPERTY,
            'travel': EventType.TRAVEL,
            'griha_pravesh': EventType.GRIHA_PRAVESH
        }
        event = event_map.get(event_type, EventType.MARRIAGE)

        calc = MuhurtaCalculator(kundali)
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)

        muhurtas = calc.find_muhurtas(
            event_type=event,
            start_date=start_date,
            end_date=end_date,
            use_event_predictor=True,
            min_score=45,
            top_n=10
        )

        muhurta_html = generate_muhurta_html(kundali, muhurtas, event_type, year)
        return jsonify({'success': True, 'html': muhurta_html})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


def generate_muhurta_html(kundali, muhurtas, event_type, year):
    """Generate HTML for Muhurta results."""
    event_hindi = {
        'marriage': 'विवाह मुहूर्त',
        'career': 'करियर मुहूर्त',
        'property': 'संपत्ति मुहूर्त',
        'travel': 'यात्रा मुहूर्त',
        'griha_pravesh': 'गृह प्रवेश मुहूर्त'
    }

    html = f'''
    <div class="muhurta-results">
        <h2 style="color: var(--primary); margin-bottom: 20px;">🌟 {event_hindi.get(event_type, 'शुभ मुहूर्त')} - {year}</h2>
        <p style="margin-bottom: 20px; color: #666;">
            जन्म नक्षत्र: <strong>{kundali.planets["MOON"]["nakshatra"]}</strong> |
            चंद्र राशि: <strong>{kundali.planets["MOON"]["rashi"]}</strong>
        </p>
    '''

    if not muhurtas:
        html += '<p style="color: #666; text-align: center; padding: 30px;">इस वर्ष कोई उपयुक्त मुहूर्त नहीं मिला।</p>'
    else:
        for i, m in enumerate(muhurtas, 1):
            score_color = '#28a745' if m.score >= 70 else ('#ffc107' if m.score >= 55 else '#6c757d')
            tarabala_color = '#28a745' if m.tarabala_score >= 8 else ('#dc3545' if m.tarabala_score == 0 else '#ffc107')
            chandrabala_color = '#28a745' if m.chandrabala_score >= 8 else ('#dc3545' if m.chandrabala_score == 0 else '#ffc107')

            html += f'''
            <div style="background: #fff; border: 2px solid #eee; border-radius: 12px; margin-bottom: 15px; overflow: hidden;">
                <div style="background: linear-gradient(135deg, #fff8f0 0%, #fff 100%); padding: 15px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #eee;">
                    <div>
                        <div style="font-size: 1.2em; font-weight: 700; color: #8b4513;">#{i} - {m.date.strftime('%d %B %Y')}</div>
                        <div style="color: #666; font-size: 0.9em;">{m.panchang.vara.english} ({m.panchang.vara.name})</div>
                    </div>
                    <div style="background: {score_color}; color: white; padding: 8px 16px; border-radius: 20px; font-weight: 700;">{m.score}/100</div>
                </div>
                <div style="padding: 15px;">
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin-bottom: 15px;">
                        <div style="background: #fff8f0; padding: 10px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 0.8em; color: #666;">समय</div>
                            <div style="font-weight: 600;">{m.start_time.strftime('%H:%M')} - {m.end_time.strftime('%H:%M')}</div>
                        </div>
                        <div style="background: #fff8f0; padding: 10px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 0.8em; color: #666;">तिथि</div>
                            <div style="font-weight: 600;">{m.panchang.tithi.name} ({m.panchang.tithi.paksha})</div>
                        </div>
                        <div style="background: #fff8f0; padding: 10px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 0.8em; color: #666;">नक्षत्र</div>
                            <div style="font-weight: 600;">{m.panchang.nakshatra}</div>
                        </div>
                        <div style="background: #fff8f0; padding: 10px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 0.8em; color: #666;">योग</div>
                            <div style="font-weight: 600;">{m.panchang.yoga.name} {'⚠️' if m.panchang.yoga.is_inauspicious else '✓'}</div>
                        </div>
                    </div>
                    <div style="display: flex; gap: 15px; margin-bottom: 10px;">
                        <div style="flex: 1; background: {'#d4edda' if m.tarabala_score >= 8 else ('#f8d7da' if m.tarabala_score == 0 else '#fff3cd')}; padding: 10px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 0.8em; color: #666;">ताराबल</div>
                            <div style="font-size: 1.3em; font-weight: 700; color: {tarabala_color};">{m.tarabala_score}/10</div>
                            <div style="font-size: 0.85em;">{m.tarabala_name}</div>
                        </div>
                        <div style="flex: 1; background: {'#d4edda' if m.chandrabala_score >= 8 else ('#f8d7da' if m.chandrabala_score == 0 else '#fff3cd')}; padding: 10px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 0.8em; color: #666;">चंद्रबल</div>
                            <div style="font-size: 1.3em; font-weight: 700; color: {chandrabala_color};">{m.chandrabala_score}/10</div>
                            <div style="font-size: 0.85em;">भाव {m.chandrabala_house}</div>
                        </div>
                    </div>
            '''

            if m.dasha_info:
                html += f'<div style="background: #e8f4fd; padding: 8px 12px; border-radius: 6px; font-size: 0.9em; margin-bottom: 10px;"><strong>दशा:</strong> {m.dasha_info}</div>'

            if m.inauspicious_periods:
                avoid_times = ' | '.join([f'{p.name}: {p.start_time.strftime("%H:%M")}-{p.end_time.strftime("%H:%M")}' for p in m.inauspicious_periods if p.severity == 'high'])
                if avoid_times:
                    html += f'<div style="background: #f8d7da; padding: 8px 12px; border-radius: 6px; font-size: 0.85em; color: #721c24;"><strong>🚫 बचें:</strong> {avoid_times}</div>'

            html += '</div></div>'

    html += '</div>'
    return html


@app.route('/health', methods=['POST'])
def health():
    """Generate Health/Accident prediction results."""
    try:
        data = request.json
        kundali_id = data.get('kundali_id', '')
        start_year = int(data.get('start_year', datetime.now().year))
        end_year = int(data.get('end_year', datetime.now().year + 5))

        kundali = get_or_recreate_kundali(kundali_id) if kundali_id else None
        if not kundali:
            return jsonify({'success': False, 'error': 'Kundali not found. Please generate kundali first.'})

        predictor = HealthPredictor(kundali)

        warnings = predictor.predict_health_issues(start_year, end_year, min_risk_score=35)
        summary = predictor.get_health_summary(start_year, end_year)

        health_html = generate_health_html(kundali, warnings, summary, start_year, end_year)
        return jsonify({'success': True, 'html': health_html})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


def generate_health_html(kundali, warnings, summary, start_year, end_year):
    """Generate HTML for Health/Accident predictions."""
    html = f'''
    <div class="health-results">
        <h2 style="color: #dc3545; margin-bottom: 20px;">⚠️ स्वास्थ्य एवं दुर्घटना विश्लेषण ({start_year}-{end_year})</h2>
        <p style="margin-bottom: 15px; color: #666;">
            लग्न: <strong>{kundali.lagna["rashi"]}</strong> |
            चंद्र राशि: <strong>{kundali.planets["MOON"]["rashi"]}</strong>
        </p>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 10px; margin-bottom: 20px;">
            <div style="background: #f8d7da; padding: 15px; border-radius: 10px; text-align: center;">
                <div style="font-size: 1.8em; font-weight: 700; color: #721c24;">{summary["critical_periods"]}</div>
                <div style="font-size: 0.85em; color: #721c24;">Critical</div>
            </div>
            <div style="background: #fff3cd; padding: 15px; border-radius: 10px; text-align: center;">
                <div style="font-size: 1.8em; font-weight: 700; color: #856404;">{summary["high_risk_periods"]}</div>
                <div style="font-size: 0.85em; color: #856404;">High Risk</div>
            </div>
            <div style="background: #d4edda; padding: 15px; border-radius: 10px; text-align: center;">
                <div style="font-size: 1.8em; font-weight: 700; color: #155724;">{summary["medium_risk_periods"]}</div>
                <div style="font-size: 0.85em; color: #155724;">Medium</div>
            </div>
        </div>

        <div style="background: #e8f4fd; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
            <h4 style="color: #0c5460; margin-bottom: 10px;">📋 सामान्य सलाह</h4>
            <ul style="margin: 0; padding-left: 20px; color: #0c5460;">
    '''

    for advice in summary.get("general_advice", [])[:3]:
        html += f'<li>{advice}</li>'

    html += '''
            </ul>
        </div>
    '''

    if not warnings:
        html += '<p style="color: #28a745; text-align: center; padding: 30px;">✓ इस अवधि में कोई महत्वपूर्ण स्वास्थ्य चिंता नहीं है।</p>'
    else:
        html += '<h3 style="color: #333; margin-bottom: 15px;">⚡ सावधानी अवधि</h3>'

        for i, w in enumerate(warnings[:8], 1):
            risk_colors = {
                "Critical": ("#721c24", "#f8d7da", "#f5c6cb"),
                "High": ("#856404", "#fff3cd", "#ffeeba"),
                "Medium": ("#0c5460", "#d1ecf1", "#bee5eb"),
                "Low": ("#155724", "#d4edda", "#c3e6cb")
            }
            text_color, bg_color, border_color = risk_colors.get(w.risk_level.value, ("#333", "#f8f9fa", "#dee2e6"))

            html += f'''
            <div style="background: {bg_color}; border: 2px solid {border_color}; border-radius: 12px; margin-bottom: 15px; overflow: hidden;">
                <div style="padding: 15px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid {border_color};">
                    <div>
                        <div style="font-size: 1.1em; font-weight: 700; color: {text_color};">
                            #{i} - {w.start_date.strftime('%b %Y')} to {w.end_date.strftime('%b %Y')}
                        </div>
                        <div style="color: {text_color}; font-size: 0.9em;">{w.event_type.value} | Dasha: {w.dasha_info}</div>
                    </div>
                    <div style="background: {text_color}; color: white; padding: 5px 12px; border-radius: 15px; font-weight: 600;">
                        {w.risk_level.value}
                    </div>
                </div>
                <div style="padding: 15px;">
                    <div style="margin-bottom: 10px;">
                        <strong>कारण:</strong>
                        <ul style="margin: 5px 0; padding-left: 20px;">
            '''

            for reason in w.reasons[:3]:
                html += f'<li style="font-size: 0.9em;">{reason}</li>'

            html += '''
                        </ul>
                    </div>
            '''

            if w.affected_body_parts:
                parts = ', '.join(w.affected_body_parts[:4])
                html += f'<div style="font-size: 0.9em; margin-bottom: 10px;"><strong>प्रभावित:</strong> {parts}</div>'

            if w.remedies:
                html += '<div style="background: white; padding: 10px; border-radius: 8px;"><strong>उपाय:</strong><ul style="margin: 5px 0; padding-left: 20px;">'
                for remedy in w.remedies[:3]:
                    html += f'<li style="font-size: 0.85em;">{remedy}</li>'
                html += '</ul></div>'

            html += '</div></div>'

    html += '</div>'
    return html


if __name__ == '__main__':
    print("\\n" + "="*50)
    print("   DETAILED KUNDALI WEB APP")
    print("   Open: http://localhost:5000")
    print("="*50 + "\\n")
    app.run(debug=True, port=5000)
