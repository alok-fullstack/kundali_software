# Kundali Software - Development Notes

## Project Overview

A Vedic astrology (Kundali) software built with:
- **Frontend**: Next.js 14 (React)
- **Backend**: FastAPI (Python)
- **Calculations**: Swiss Ephemeris (pyswisseph)

## Architecture

```
kundali_software/
├── frontend/                 # Next.js 14 app
│   └── app/
│       ├── components/
│       │   ├── KundaliForm.tsx      # Main birth data input form
│       │   ├── KundaliDisplay.tsx   # Kundali results display
│       │   └── ui/
│       │       └── DateTimePicker.tsx  # Custom date/time pickers
│       ├── matching/
│       │   └── page.tsx             # Kundali matching (Ashtakoot)
│       └── page.tsx                 # Home page
├── backend/
│   └── api/
│       ├── main.py                  # FastAPI app entry
│       └── html_generator.py        # Generates Kundali HTML
├── src/                             # Core calculation modules
│   ├── kundali.py                   # Main Kundali class
│   ├── calculations.py              # Swiss Ephemeris calculations
│   ├── dasha.py                     # Vimshottari Dasha system
│   ├── divisional_charts.py         # 16 Varga charts (D1-D60)
│   ├── kundali_matching.py          # Ashtakoot Milan (36 Guna)
│   ├── config.py                    # Constants (Rashis, Nakshatras, etc.)
│   └── panchang.py                  # Panchang calculations
└── web_app.py                       # Original Flask app (reference)
```

## Key Features Implemented

### 1. Core Kundali Generation
- Lagna (Ascendant) calculation
- All 9 planets: Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu
- Nakshatra and Pada calculations
- House (Bhava) placements

### 2. Vimshottari Dasha System
- 120-year Mahadasha cycle
- Antardasha (sub-periods)
- Pratyantardasha (sub-sub-periods)
- Current dasha calculation

### 3. Divisional Charts (Varga)
All 16 standard divisional charts per BPHS:
- D1 (Rashi), D2 (Hora), D3 (Drekkana), D4 (Chaturthamsha)
- D7 (Saptamsha), D9 (Navamsha), D10 (Dashamsha), D12 (Dwadashamsha)
- D16 (Shodashamsha), D20 (Vimshamsha), D24 (Chaturvimshamsha)
- D27 (Bhamsha), D30 (Trimshamsha), D40 (Khavedamsha)
- D45 (Akshavedamsha), D60 (Shashtiamsha)

### 4. Kundali Matching (Ashtakoot Milan)
8 Koota matching system with 36 total Gunas:
| Koota | Max Points | What it Measures |
|-------|------------|------------------|
| Varna | 1 | Spiritual compatibility |
| Vashya | 2 | Mutual attraction |
| Tara | 3 | Birth star compatibility |
| Yoni | 4 | Sexual compatibility |
| Graha Maitri | 5 | Mental compatibility |
| Gana | 6 | Temperament |
| Bhakoot | 7 | Love and affection |
| Nadi | 8 | Health and genes |

### 5. Panchang
Five limbs of Vedic time:
- Tithi (lunar day)
- Nakshatra (lunar mansion)
- Yoga (Sun-Moon combination)
- Karana (half-tithi)
- Vara (weekday)

---

## Bug Fixes

### Timezone Bug in Date Picker (Fixed: 2026-06-26)

**Problem**: Date picker was sending wrong date to backend due to UTC conversion.

**Root Cause**: Using `toISOString()` converts local date to UTC:
```javascript
// BUG: This shifts the date for IST (UTC+5:30)
dob: birthDate.toISOString().split('T')[0]

// Example: User selects 25-10-1993 05:15 AM IST
// toISOString() converts to: 1993-10-24T23:45:00.000Z (UTC)
// split('T')[0] extracts: "1993-10-24" (WRONG!)
```

**Impact**: Moon moves ~13° per day. One day difference changes:
- 24-10-1993: Moon at 295.33° = Makara (Capricorn), Dhanishta
- 25-10-1993: Moon at 307.46° = Kumbha (Aquarius), Shatabhisha

**Fix**: Use local date methods instead:
```javascript
// CORRECT: Uses local date without UTC conversion
const year = birthDate.getFullYear();
const month = (birthDate.getMonth() + 1).toString().padStart(2, '0');
const day = birthDate.getDate().toString().padStart(2, '0');
dob: `${year}-${month}-${day}`
```

**Files Fixed**:
1. `frontend/app/components/KundaliForm.tsx` (line 72-79)
2. `frontend/app/matching/page.tsx` (line 224-232)

---

### Muhurta and Health API Missing HTML (Fixed: 2026-06-27)

**Problem**: The Muhurta (Subha Muhrat) and Health (Swasth) modals were not displaying results because the backend API was returning JSON data but the frontend expected an `html` field.

**Root Cause**: 
- Frontend `MuhurtaModal.tsx` and `HealthModal.tsx` expected `response.html` to render results
- Backend routes were returning structured JSON without HTML generation

**Fix**:
1. Added `html: Optional[str]` field to `MuhurtaResponse` and `HealthResponse` schemas
2. Updated `backend/api/routes/muhurta.py` to call `generate_muhurta_html()` 
3. Created `src/health_html_generator.py` for health prediction HTML
4. Updated `backend/api/routes/health.py` to call `generate_health_html()`

**Files Modified**:
1. `backend/api/models/schemas.py` - Added `html` field to responses
2. `backend/api/routes/muhurta.py` - Added HTML generation
3. `backend/api/routes/health.py` - Added HTML generation
4. `src/__init__.py` - Added health_html_generator export

**Files Created**:
1. `src/health_html_generator.py` - Health predictions HTML generator

---

## Verification Scripts

### verify_flask_vs_fastapi.py
Compares Flask and FastAPI outputs for same birth data.

### full_verification.py
Complete verification of all Kundali calculations including:
- Birth data verification
- Lagna details
- All planet positions with manual calculation check
- House analysis
- Nakshatra analysis
- Dasha timeline
- Special planetary conditions

### verify_both_dates.py
Demonstrates Moon position difference between adjacent dates.

### test_html_output.py
Verifies HTML generator outputs correct Rashi names.

---

## Test Data

**Alok Yadav**:
- DOB: 25-10-1993
- TOB: 05:15 AM
- Place: Amethi (26.15°N, 81.81°E)

**Expected Results**:
- Lagna: Kanya (Virgo)
- Chandra Rashi: Kumbha (Aquarius)
- Surya Rashi: Tula (Libra)
- Birth Nakshatra: Shatabhisha, Pada 2
- Nakshatra Lord: Rahu

---

## Technical Notes

### Swiss Ephemeris
- Uses NASA JPL ephemeris data
- Accuracy: 99.99%
- Ayanamsha: Lahiri (Chitrapaksha)

### Rashi Calculation
```python
rashi_num = int(longitude / 30) % 12  # 0-11
# RASHIS[rashi_num] gives the rashi name
```

### Nakshatra Calculation
```python
nakshatra_num = int(longitude / (360/27)) % 27  # 0-26
pada = int((longitude % (360/27)) / (360/108)) + 1  # 1-4
```

### House Calculation (Whole Sign)
```python
house_num = ((planet_rashi - lagna_rashi) % 12) + 1  # 1-12
```

---

## UI Components

### Custom Date Picker
- Located: `frontend/app/components/ui/DateTimePicker.tsx`
- Features: Year selector (1900 to current), month navigation, calendar grid
- Z-index: 100 (to appear above other elements)

### Custom Time Picker
- 12-hour format with AM/PM
- Hour (1-12) and Minute (0-59) selectors

### Google Places Integration
- Autocomplete for city selection
- Automatically fetches latitude/longitude
- API Key: Set via `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY`

---

## API Endpoints

### POST /api/kundali
Generate Kundali for a person.

**Request**:
```json
{
  "name": "Alok Yadav",
  "dob": "1993-10-25",
  "tob": "05:15",
  "city": "Amethi",
  "latitude": 26.15,
  "longitude": 81.81
}
```

**Response**:
```json
{
  "success": true,
  "kundali_id": "uuid",
  "html": "<html>...</html>"
}
```

### POST /api/match
Match two Kundalis (Ashtakoot Milan).

**Request**:
```json
{
  "boy": { "name": "...", "dob": "...", ... },
  "girl": { "name": "...", "dob": "...", ... }
}
```

**Response**:
```json
{
  "success": true,
  "total_score": 28,
  "max_score": 36,
  "percentage": 77.78,
  "compatibility": "Good",
  "kootas": [...]
}
```

---

## Running the Application

### Backend (FastAPI)
```bash
cd kundali_software
pip install -r requirements.txt
uvicorn backend.api.main:app --reload --port 8000
```

### Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
```

### Full Verification
```bash
cd kundali_software
python full_verification.py
```

---

## Future Enhancements

1. **Muhurta System** - Finding auspicious times for events
2. **Yoga Analysis** - Identifying planetary yogas (Raj Yoga, Dhana Yoga, etc.)
3. **Transit Analysis** - Current planetary transits over natal chart
4. **Ashtakavarga** - Point-based strength analysis
5. **PDF Export** - Download Kundali as PDF
6. **Multi-language** - Support for more Indian languages

---

## References

- **BPHS** (Brihat Parashara Hora Shastra) - Divisional chart calculations
- **Muhurta Chintamani** - Muhurta selection rules
- **Swiss Ephemeris Documentation** - Astronomical calculations
- **Lahiri Ayanamsha** - Standard for Vedic astrology in India
