# Kundali Software - Vedic Astrology Application

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![Node.js](https://img.shields.io/badge/node.js-18+-brightgreen.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)
![Next.js](https://img.shields.io/badge/Next.js-14+-black.svg)
![GitHub stars](https://img.shields.io/github/stars/alok-fullstack/kundali_software?style=social)
![GitHub forks](https://img.shields.io/github/forks/alok-fullstack/kundali_software?style=social)

A comprehensive Vedic Astrology (Jyotish) application that generates accurate Kundali (birth charts), predictions, and astrological analysis based on traditional Hindu astrology principles.

## 🌐 Live Demo

**Try it now:** [https://kundali-software-eight.vercel.app/](https://kundali-software-eight.vercel.app/)

## Features

- **Kundali Generation** - Accurate birth chart calculation with planetary positions using Swiss Ephemeris
- **Dasha System** - Vimshottari Dasha calculations with predictions
- **Kundali Matching** - Marriage compatibility analysis with Ashtakoot Guna Milan
- **Muhurta** - Auspicious timing recommendations for important events
- **Panchang** - Daily Hindu calendar with Tithi, Nakshatra, Yoga, Karana
- **Divisional Charts** - D1 to D60 Varga charts analysis
- **Dosha Analysis** - Manglik, Kaal Sarp, Pitra Dosha detection
- **Numerology** - Name and birth number analysis
- **Gemstone Recommendations** - Based on planetary positions (BPHS principles)
- **Health Predictions** - Medical astrology insights
- **Career & Finance** - Professional guidance based on chart analysis
- **Remedies** - Personalized remedial measures
- **Rashifal** - Daily/Monthly/Yearly horoscope predictions
- **Prashna Kundali** - Horary astrology for specific questions

## Tech Stack

### Backend
- **Python 3.10+**
- **FastAPI** - High-performance API framework
- **Swiss Ephemeris** - Accurate planetary calculations
- **Pydantic** - Data validation

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Chart.js** - Radar charts for Guna visualization

## Project Structure

```
kundali_software/
├── backend/                 # FastAPI backend
│   ├── api/
│   │   ├── routes/         # API endpoints
│   │   └── models/         # Pydantic schemas
│   ├── app.py              # FastAPI app
│   └── requirements.txt
├── frontend/               # Next.js frontend
│   ├── app/
│   │   ├── components/     # React components
│   │   └── */page.tsx      # Page routes
│   └── lib/                # Utilities & API client
├── src/                    # Core astrology logic
│   ├── kundali.py          # Birth chart calculations
│   ├── dasha.py            # Dasha system
│   ├── muhurta.py          # Muhurta calculations
│   ├── panchang.py         # Panchang logic
│   ├── divisional_charts.py
│   ├── dosha_analysis.py
│   ├── gemstone_recommendations.py
│   └── ...
├── tests/                  # Test suite
└── docs/                   # Documentation
```

## Installation

### Prerequisites
- Python 3.10 or higher
- Node.js 18 or higher
- npm or yarn

### Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run backend
cd backend
python run.py
```

Backend runs at: http://localhost:8000

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend runs at: http://localhost:3000

## Quick Start

### Using Batch Files (Windows)

```bash
# One-time setup
setup.bat

# Run the application
run_app.bat
```

### API Usage

```python
import requests

# Generate Kundali
response = requests.post("http://localhost:8000/api/kundali", json={
    "name": "John Doe",
    "date": "1990-05-15",
    "time": "10:30",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "timezone": 5.5
})

kundali = response.json()
print(kundali["planets"])
print(kundali["lagna"])
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/kundali` | POST | Generate birth chart |
| `/api/dasha` | POST | Calculate Dasha periods |
| `/api/matching` | POST | Kundali matching for marriage |
| `/api/muhurta` | POST | Find auspicious timings |
| `/api/panchang` | GET | Get Panchang for date |
| `/api/divisional-charts` | POST | Generate Varga charts |
| `/api/dosha` | POST | Analyze doshas |
| `/api/gemstone` | POST | Gemstone recommendations |
| `/api/numerology` | POST | Numerology analysis |
| `/api/rashifal` | GET | Horoscope predictions |
| `/api/remedies` | POST | Get remedial measures |

## Screenshots

*Coming soon*

## Accuracy

- Planetary positions calculated using Swiss Ephemeris (accuracy: < 1 arc second)
- Ayanamsa: Lahiri (Chitrapaksha)
- Supports both North Indian and South Indian chart styles

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Alok Yadav**
- GitHub: [@alok-fullstack](https://github.com/alok-fullstack)
- LinkedIn: [Alok Kumar Yadav](https://www.linkedin.com/in/alok-kumar-yadav-538835b5/)

## Acknowledgments

- [Swiss Ephemeris](https://www.astro.com/swisseph/) for planetary calculations
- Traditional Vedic astrology texts (BPHS, Jataka Parijata)
