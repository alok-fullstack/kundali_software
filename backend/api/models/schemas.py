"""
Pydantic schemas for request/response validation.

These models define the API contract for the Kundali software FastAPI backend.
"""

from datetime import datetime, date, time
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator


# ============================================================
# REQUEST MODELS
# ============================================================

class KundaliRequest(BaseModel):
    """Request model for generating a new kundali."""
    name: str = Field(..., min_length=1, max_length=100, description="Person's name")
    dob: str = Field(..., description="Date of birth in YYYY-MM-DD format")
    tob: str = Field(..., description="Time of birth in HH:MM format (24-hour)")
    city: str = Field(..., min_length=1, max_length=100, description="Birth city name")
    latitude: Optional[float] = Field(None, ge=-90, le=90, description="Latitude (optional, will geocode from city if not provided)")
    longitude: Optional[float] = Field(None, ge=-180, le=180, description="Longitude (optional, will geocode from city if not provided)")
    timezone: str = Field("Asia/Kolkata", description="Timezone string")

    @field_validator('dob')
    @classmethod
    def validate_dob(cls, v: str) -> str:
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('dob must be in YYYY-MM-DD format')
        return v

    @field_validator('tob')
    @classmethod
    def validate_tob(cls, v: str) -> str:
        try:
            datetime.strptime(v, '%H:%M')
        except ValueError:
            raise ValueError('tob must be in HH:MM format')
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "John Doe",
                    "dob": "1990-05-15",
                    "tob": "10:30",
                    "city": "Delhi",
                    "latitude": None,
                    "longitude": None,
                    "timezone": "Asia/Kolkata"
                }
            ]
        }
    }


class ChatRequest(BaseModel):
    """Request model for chat with kundali assistant."""
    kundali_id: str = Field(..., description="UUID of the generated kundali")
    question: str = Field(..., min_length=1, max_length=1000, description="Question to ask about the kundali")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "kundali_id": "abc123def456",
                    "question": "Career ke baare mein batao"
                }
            ]
        }
    }


class MuhurtaRequest(BaseModel):
    """Request model for finding auspicious muhurtas."""
    kundali_id: str = Field(..., description="UUID of the generated kundali")
    event_type: str = Field(..., description="Event type: marriage, career, property, travel, griha_pravesh")
    year: int = Field(..., ge=2020, le=2100, description="Year to search for muhurtas")
    top_n: int = Field(10, ge=1, le=50, description="Maximum number of results to return")
    min_score: int = Field(45, ge=0, le=100, description="Minimum score threshold")

    @field_validator('event_type')
    @classmethod
    def validate_event_type(cls, v: str) -> str:
        valid_types = ['marriage', 'career', 'property', 'travel', 'griha_pravesh', 'education', 'general']
        if v.lower() not in valid_types:
            raise ValueError(f'event_type must be one of: {", ".join(valid_types)}')
        return v.lower()

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "kundali_id": "abc123def456",
                    "event_type": "marriage",
                    "year": 2027,
                    "top_n": 10,
                    "min_score": 45
                }
            ]
        }
    }


class HealthRequest(BaseModel):
    """Request model for health/accident predictions."""
    kundali_id: str = Field(..., description="UUID of the generated kundali")
    start_year: int = Field(..., ge=1950, le=2100, description="Start year for predictions")
    end_year: int = Field(..., ge=1950, le=2100, description="End year for predictions")
    min_risk_score: int = Field(35, ge=0, le=100, description="Minimum risk score to include")

    @field_validator('end_year')
    @classmethod
    def validate_end_year(cls, v: int, info) -> int:
        start_year = info.data.get('start_year')
        if start_year and v < start_year:
            raise ValueError('end_year must be >= start_year')
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "kundali_id": "abc123def456",
                    "start_year": 2026,
                    "end_year": 2030,
                    "min_risk_score": 35
                }
            ]
        }
    }


# ============================================================
# RESPONSE MODELS
# ============================================================

class PlanetPosition(BaseModel):
    """Planet position details."""
    name: str
    rashi: str
    rashi_english: str
    rashi_degree: float
    nakshatra: str
    pada: int
    longitude: float
    is_retrograde: bool
    house: int  # House number from Lagna


class HouseInfo(BaseModel):
    """House/Bhava details."""
    house: int
    name: str
    significance: str
    rashi: str
    rashi_english: str
    planets: List[str]


class DashaInfo(BaseModel):
    """Current dasha details."""
    planet: str
    start: str
    end: str


class MahadashaInfo(BaseModel):
    """Mahadasha period information."""
    planet: str
    start_date: str
    end_date: str


class KundaliResponse(BaseModel):
    """Full kundali data response."""
    # Birth details
    name: str
    birth_date: str
    birth_time: str
    birth_city: str
    latitude: float
    longitude: float
    timezone: str

    # Lagna details
    lagna_rashi: str
    lagna_rashi_english: str
    lagna_degree: float
    lagna_nakshatra: str
    lagna_pada: int

    # Moon details
    moon_rashi: str
    moon_nakshatra: str
    moon_pada: int

    # Sun details
    sun_rashi: str

    # Planet positions
    planets: Dict[str, PlanetPosition]

    # Houses
    houses: List[HouseInfo]

    # Planets in houses (dict of house_num -> list of planet names)
    planets_in_houses: Dict[str, List[str]]

    # Current Dasha
    current_dasha: Dict[str, Any]
    full_dasha: str

    # Mahadashas (next several years)
    mahadashas: List[MahadashaInfo]


class KundaliGenerateResponse(BaseModel):
    """Response for kundali generation endpoint."""
    success: bool
    kundali_id: str
    kundali: KundaliResponse
    html: Optional[str] = None  # HTML representation for frontend display
    message: str = "Kundali generated successfully"


class ChatResponse(BaseModel):
    """Response for chat endpoint."""
    success: bool
    answer: str
    kundali_id: str


class PanchangInfo(BaseModel):
    """Panchang details for a muhurta."""
    tithi: str
    tithi_paksha: str
    nakshatra: str
    nakshatra_pada: int
    yoga: str
    yoga_is_inauspicious: bool
    karana: str
    vara: str
    vara_english: str


class InauspiciousPeriodInfo(BaseModel):
    """Inauspicious period within a muhurta day."""
    name: str
    start_time: str
    end_time: str
    severity: str


class MuhurtaWindowResponse(BaseModel):
    """Single muhurta window details."""
    date: str
    weekday: str
    start_time: str
    end_time: str
    score: int
    panchang: PanchangInfo
    tarabala_num: int
    tarabala_name: str
    tarabala_score: int
    chandrabala_house: int
    chandrabala_score: int
    dasha_info: str
    abhijit_muhurta: Optional[str]
    hora_lord: str
    reasons: List[str]
    warnings: List[str]
    inauspicious_periods: List[InauspiciousPeriodInfo]


class MuhurtaResponse(BaseModel):
    """Response for muhurta endpoint."""
    success: bool
    kundali_id: str
    event_type: str
    year: int
    birth_nakshatra: str
    moon_rashi: str
    muhurtas: List[MuhurtaWindowResponse]
    total_found: int
    message: str = ""
    html: Optional[str] = None  # HTML representation for frontend display


class HealthWarningResponse(BaseModel):
    """Single health warning period."""
    start_date: str
    end_date: str
    event_type: str
    risk_level: str
    reasons: List[str]
    dasha_info: str
    affected_body_parts: List[str]
    remedies: List[str]


class HealthSummary(BaseModel):
    """Health prediction summary."""
    period: str
    total_warnings: int
    critical_periods: int
    high_risk_periods: int
    medium_risk_periods: int
    general_advice: List[str]


class HealthResponse(BaseModel):
    """Response for health endpoint."""
    success: bool
    kundali_id: str
    start_year: int
    end_year: int
    lagna: str
    moon_rashi: str
    summary: HealthSummary
    warnings: List[HealthWarningResponse]
    message: str = ""
    html: Optional[str] = None  # HTML representation for frontend display


class ErrorResponse(BaseModel):
    """Standard error response."""
    success: bool = False
    error: str
    detail: Optional[str] = None
