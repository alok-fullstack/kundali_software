"""
Health and Accident Timing Predictor

Predicts vulnerable periods for accidents and major health issues based on:
1. Dasha of 6th/8th/12th lords (disease, accidents, hospitalization)
2. Dasha of Maraka planets (2nd/7th lords)
3. Malefic transits (Saturn, Mars, Rahu) over sensitive points
4. Afflictions to Lagna and Moon

Based on authentic Vedic texts:
- Brihat Parashara Hora Shastra (BPHS)
- Phaladeepika
- Jataka Parijata
"""

from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum

from .planets import PlanetaryCalculator
from .config import (
    Planet, RASHIS, HOUSE_LORDSHIPS, FUNCTIONAL_MALEFICS,
    VIMSHOTTARI_YEARS, DASHA_SEQUENCE
)
from .dasha import VimshottariDasha
from .transit import TransitCalculator


class RiskLevel(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class HealthEventType(Enum):
    ACCIDENT = "Accident/Injury"
    CHRONIC_DISEASE = "Chronic Disease"
    SURGERY = "Surgery"
    HOSPITALIZATION = "Hospitalization"
    MENTAL_STRESS = "Mental Stress"
    GENERAL_HEALTH = "General Health Issue"


@dataclass
class HealthWarning:
    """Represents a health/accident warning period."""
    start_date: datetime
    end_date: datetime
    event_type: HealthEventType
    risk_level: RiskLevel
    reasons: List[str]
    dasha_info: str
    affected_body_parts: List[str]
    remedies: List[str]


class HealthPredictor:
    """
    Predicts vulnerable periods for health issues and accidents.

    Key Factors (from BPHS and Phaladeepika):

    1. HOUSES:
       - 1st (Lagna): Physical body, vitality, constitution
       - 6th: Diseases, injuries, enemies
       - 8th: Accidents, sudden events, surgeries, longevity
       - 12th: Hospitalization, confinement, loss

    2. MARAKA PLANETS (Death-inflicting):
       - 2nd lord: Primary Maraka
       - 7th lord: Secondary Maraka
       - Planets in 2nd/7th houses
       - Planets aspecting 2nd/7th houses

    3. MALEFIC PLANETS:
       - Mars: Accidents, injuries, blood, surgeries, burns
       - Saturn: Chronic diseases, bones, delays, depression
       - Rahu: Sudden/mysterious ailments, poisoning, phobias
       - Ketu: Surgeries, infections, spiritual crises
       - Sun (afflicted): Heart, eyes, vitality issues

    4. TRANSITS (Gochara):
       - Saturn over Moon (Sade Sati): General hardship
       - Saturn over 8th house: Sudden troubles
       - Mars over 8th house: Accidents, surgeries
       - Rahu/Ketu over Lagna/Moon: Mysterious ailments
    """

    # Body parts ruled by planets (from Jataka Parijata)
    PLANET_BODY_PARTS = {
        "SUN": ["Heart", "Eyes", "Head", "Bones", "Right eye"],
        "MOON": ["Mind", "Chest", "Blood", "Left eye", "Stomach"],
        "MARS": ["Blood", "Muscles", "Head injuries", "Bone marrow", "Accidents"],
        "MERCURY": ["Nervous system", "Skin", "Speech", "Lungs", "Arms"],
        "JUPITER": ["Liver", "Fat", "Ears", "Thighs", "Diabetes"],
        "VENUS": ["Reproductive system", "Kidneys", "Face", "Throat", "Eyes"],
        "SATURN": ["Bones", "Teeth", "Legs", "Chronic diseases", "Depression"],
        "RAHU": ["Skin diseases", "Poisoning", "Phobias", "Mysterious ailments"],
        "KETU": ["Wounds", "Infections", "Surgeries", "Fever", "Accidents"],
    }

    # Houses and body parts (from BPHS)
    HOUSE_BODY_PARTS = {
        1: ["Head", "Brain", "Overall vitality"],
        2: ["Face", "Right eye", "Teeth", "Throat"],
        3: ["Arms", "Shoulders", "Ears", "Nervous system"],
        4: ["Chest", "Heart", "Lungs", "Breasts"],
        5: ["Stomach", "Upper abdomen", "Mind", "Heart"],
        6: ["Intestines", "Kidneys", "Digestive system"],
        7: ["Lower abdomen", "Reproductive organs", "Kidneys"],
        8: ["Reproductive organs", "Chronic diseases", "Death"],
        9: ["Thighs", "Hips", "Arteries"],
        10: ["Knees", "Bones", "Joints"],
        11: ["Calves", "Ankles", "Left ear"],
        12: ["Feet", "Left eye", "Hospitalization"],
    }

    def __init__(self, kundali):
        """
        Initialize with a Kundali object.

        Args:
            kundali: Kundali object containing birth chart data
        """
        self.kundali = kundali
        self.planets = kundali.planets
        self.lagna = kundali.lagna
        self.lagna_rashi = kundali.lagna["rashi"]
        self.lagna_rashi_num = kundali.lagna["rashi_num"]
        self.moon_rashi_num = kundali.planets["MOON"]["rashi_num"]
        self.birth_date = kundali.birth_data.date

        self.dasha_calculator = VimshottariDasha()
        self.planet_calculator = PlanetaryCalculator()
        self.transit_calculator = TransitCalculator(kundali)

        # Get planets in houses (needed for other calculations)
        self.planets_in_houses = kundali.get_planets_in_houses()

        # Calculate house lords
        self.house_lords = self._get_house_lords()

        # Identify Maraka planets
        self.maraka_planets = self._identify_maraka_planets()

        # Identify health-sensitive planets (6th, 8th, 12th lords)
        self.health_lords = self._identify_health_lords()

    def _get_house_lords(self) -> Dict[int, str]:
        """Get lords of all 12 houses for this lagna."""
        lordships = HOUSE_LORDSHIPS.get(self.lagna_rashi, {})
        house_lords = {}
        for planet, houses in lordships.items():
            for house in houses:
                house_lords[house] = planet
        return house_lords

    def _identify_maraka_planets(self) -> List[str]:
        """
        Identify Maraka (death-inflicting) planets.

        Maraka planets are:
        1. Lords of 2nd and 7th houses
        2. Planets placed in 2nd and 7th houses
        3. Natural malefics associating with 2nd/7th
        """
        marakas = set()

        # 2nd and 7th lords are primary Marakas
        second_lord = self.house_lords.get(2)
        seventh_lord = self.house_lords.get(7)

        if second_lord:
            marakas.add(second_lord)
        if seventh_lord:
            marakas.add(seventh_lord)

        # Planets in 2nd and 7th houses
        for planet in self.planets_in_houses.get(2, []):
            marakas.add(planet)
        for planet in self.planets_in_houses.get(7, []):
            marakas.add(planet)

        return list(marakas)

    def _identify_health_lords(self) -> Dict[str, List[str]]:
        """
        Identify lords of health-sensitive houses.

        - 6th lord: Diseases, enemies, injuries
        - 8th lord: Accidents, sudden events, longevity
        - 12th lord: Hospitalization, confinement
        """
        return {
            "sixth_lord": self.house_lords.get(6),
            "eighth_lord": self.house_lords.get(8),
            "twelfth_lord": self.house_lords.get(12),
            "lagna_lord": self.house_lords.get(1),
        }

    def _get_dasha_periods(
        self,
        start_year: int,
        end_year: int
    ) -> List[Dict]:
        """Get all Mahadasha and Antardasha periods in range."""
        periods = []
        moon_longitude = self.planets["MOON"]["longitude"]

        mahadashas = self.dasha_calculator.calculate_mahadashas(
            moon_longitude,
            self.birth_date,
            years_ahead=150
        )

        start_date = datetime(start_year, 1, 1)
        end_date = datetime(end_year, 12, 31)

        for maha in mahadashas:
            if maha.end_date < start_date or maha.start_date > end_date:
                continue

            antardashas = self.dasha_calculator.calculate_antardashas(maha)

            for antar in antardashas:
                if antar.end_date < start_date or antar.start_date > end_date:
                    continue

                period_start = max(antar.start_date, start_date)
                period_end = min(antar.end_date, end_date)

                periods.append({
                    "start_date": period_start,
                    "end_date": period_end,
                    "mahadasha": maha.planet,
                    "antardasha": antar.planet,
                })

        return periods

    def _score_health_risk(
        self,
        mahadasha: str,
        antardasha: str,
        period_start: datetime,
        period_end: datetime
    ) -> Tuple[int, List[str], HealthEventType, List[str]]:
        """
        Score health risk for a dasha period.

        Returns:
            Tuple of (risk_score 0-100, reasons, event_type, body_parts)
        """
        score = 0
        reasons = []
        body_parts = set()
        event_type = HealthEventType.GENERAL_HEALTH

        # Normalize to uppercase for comparison
        maha_upper = mahadasha.upper()
        antar_upper = antardasha.upper()

        sixth_lord = self.health_lords.get("sixth_lord", "").upper()
        eighth_lord = self.health_lords.get("eighth_lord", "").upper()
        twelfth_lord = self.health_lords.get("twelfth_lord", "").upper()
        maraka_upper = [p.upper() for p in self.maraka_planets]

        # === MAHADASHA ANALYSIS ===

        # 8th lord Mahadasha - accidents, sudden events
        if maha_upper == eighth_lord:
            score += 30
            reasons.append(f"8th lord ({mahadasha}) Mahadasha - accident/sudden event risk")
            event_type = HealthEventType.ACCIDENT
            body_parts.update(self.PLANET_BODY_PARTS.get(maha_upper, []))

        # 6th lord Mahadasha - diseases
        if maha_upper == sixth_lord:
            score += 25
            reasons.append(f"6th lord ({mahadasha}) Mahadasha - disease risk")
            event_type = HealthEventType.CHRONIC_DISEASE
            body_parts.update(self.PLANET_BODY_PARTS.get(maha_upper, []))

        # 12th lord Mahadasha - hospitalization
        if maha_upper == twelfth_lord:
            score += 20
            reasons.append(f"12th lord ({mahadasha}) Mahadasha - hospitalization risk")
            event_type = HealthEventType.HOSPITALIZATION

        # Maraka planet Mahadasha
        if maha_upper in maraka_upper:
            score += 25
            reasons.append(f"Maraka planet ({mahadasha}) Mahadasha - health vulnerability")

        # Mars Mahadasha - accidents, surgeries
        if maha_upper == "MARS":
            score += 15
            reasons.append("Mars Mahadasha - accident/surgery risk")
            event_type = HealthEventType.ACCIDENT
            body_parts.update(["Head injuries", "Blood", "Accidents"])

        # Saturn Mahadasha - chronic diseases
        if maha_upper == "SATURN":
            score += 15
            reasons.append("Saturn Mahadasha - chronic health issues")
            event_type = HealthEventType.CHRONIC_DISEASE
            body_parts.update(["Bones", "Joints", "Chronic diseases"])

        # Rahu Mahadasha - mysterious ailments
        if maha_upper == "RAHU":
            score += 15
            reasons.append("Rahu Mahadasha - mysterious/sudden ailments")
            body_parts.update(["Mysterious ailments", "Phobias"])

        # Ketu Mahadasha - surgeries, infections
        if maha_upper == "KETU":
            score += 15
            reasons.append("Ketu Mahadasha - surgery/infection risk")
            event_type = HealthEventType.SURGERY
            body_parts.update(["Surgeries", "Infections"])

        # === ANTARDASHA ANALYSIS ===

        # 8th lord Antardasha
        if antar_upper == eighth_lord:
            score += 20
            reasons.append(f"8th lord ({antardasha}) Antardasha - accident trigger")
            event_type = HealthEventType.ACCIDENT

        # 6th lord Antardasha
        if antar_upper == sixth_lord:
            score += 15
            reasons.append(f"6th lord ({antardasha}) Antardasha - disease trigger")

        # Maraka Antardasha
        if antar_upper in maraka_upper:
            score += 20
            reasons.append(f"Maraka ({antardasha}) Antardasha - critical health period")

        # Mars Antardasha in malefic Mahadasha
        if antar_upper == "MARS" and maha_upper in ["SATURN", "RAHU", "KETU"]:
            score += 15
            reasons.append(f"Mars Antardasha in {mahadasha} Mahadasha - accident risk elevated")
            event_type = HealthEventType.ACCIDENT

        # Saturn Antardasha
        if antar_upper == "SATURN":
            score += 10
            reasons.append("Saturn Antardasha - health delays/chronic issues")

        # === TRANSIT ANALYSIS (at mid-point of period) ===
        mid_date = period_start + (period_end - period_start) / 2

        try:
            # Saturn transit
            saturn_info = self.transit_calculator.get_transit_house_from_moon("SATURN", mid_date)
            saturn_house = saturn_info.get("house_from_moon", 0)

            # Saturn in 8th from Moon
            if saturn_house == 8:
                score += 15
                reasons.append("Saturn transiting 8th from Moon - sudden troubles")
                event_type = HealthEventType.ACCIDENT

            # Saturn in 1st from Moon (Sade Sati peak)
            if saturn_house == 1:
                score += 10
                reasons.append("Saturn over Moon (Sade Sati peak) - health stress")

            # Mars transit
            mars_info = self.transit_calculator.get_transit_house_from_lagna("MARS", mid_date)
            mars_house = mars_info.get("house_from_lagna", 0)

            # Mars in 8th from Lagna
            if mars_house == 8:
                score += 12
                reasons.append("Mars transiting 8th house - accident/surgery risk")
                event_type = HealthEventType.ACCIDENT

            # Mars in 6th
            if mars_house == 6:
                score += 8
                reasons.append("Mars transiting 6th house - injury/disease risk")

        except Exception:
            pass  # Transit calculation failed, continue with dasha

        # Cap score at 100
        score = min(100, score)

        return score, reasons, event_type, list(body_parts)

    def _get_remedies(self, event_type: HealthEventType, planets: List[str]) -> List[str]:
        """Get remedies based on event type and afflicting planets."""
        remedies = []

        # General remedies
        remedies.append("Regular health check-ups recommended during this period")

        if event_type == HealthEventType.ACCIDENT:
            remedies.append("Avoid risky activities, especially on Tuesdays and Saturdays")
            remedies.append("Recite Hanuman Chalisa for protection")
            remedies.append("Wear protective gemstone (Red Coral after consultation)")

        if event_type == HealthEventType.CHRONIC_DISEASE:
            remedies.append("Focus on preventive healthcare")
            remedies.append("Recite Maha Mrityunjaya Mantra (महामृत्युंजय मंत्र)")
            remedies.append("Donate medicines or food on Saturdays")

        if event_type == HealthEventType.SURGERY:
            remedies.append("Avoid elective surgeries if possible during this period")
            remedies.append("If surgery needed, choose muhurta carefully")
            remedies.append("Worship Lord Dhanvantari for medical protection")

        if event_type == HealthEventType.HOSPITALIZATION:
            remedies.append("Keep emergency contacts ready")
            remedies.append("Donate to hospitals or medical charities")
            remedies.append("Recite Vishnu Sahasranama")

        # Planet-specific remedies
        if "Mars" in planets:
            remedies.append("Offer red flowers to Hanuman on Tuesdays")
        if "Saturn" in planets:
            remedies.append("Feed crows and donate black items on Saturdays")
        if "Rahu" in planets:
            remedies.append("Donate to orphanages, avoid intoxicants")
        if "Ketu" in planets:
            remedies.append("Donate blankets, worship Lord Ganesha")

        return remedies[:5]  # Return top 5 remedies

    def predict_health_issues(
        self,
        start_year: int,
        end_year: int,
        min_risk_score: int = 40
    ) -> List[HealthWarning]:
        """
        Predict health issues and accident-prone periods.

        Args:
            start_year: Start year for prediction
            end_year: End year for prediction
            min_risk_score: Minimum risk score to include (0-100)

        Returns:
            List of HealthWarning objects sorted by risk level
        """
        warnings = []

        # Get all dasha periods in range
        dasha_periods = self._get_dasha_periods(start_year, end_year)

        for period in dasha_periods:
            score, reasons, event_type, body_parts = self._score_health_risk(
                period["mahadasha"],
                period["antardasha"],
                period["start_date"],
                period["end_date"]
            )

            if score >= min_risk_score:
                # Determine risk level
                if score >= 70:
                    risk_level = RiskLevel.CRITICAL
                elif score >= 55:
                    risk_level = RiskLevel.HIGH
                elif score >= 40:
                    risk_level = RiskLevel.MEDIUM
                else:
                    risk_level = RiskLevel.LOW

                # Get remedies
                afflicting_planets = [period["mahadasha"], period["antardasha"]]
                remedies = self._get_remedies(event_type, afflicting_planets)

                warnings.append(HealthWarning(
                    start_date=period["start_date"],
                    end_date=period["end_date"],
                    event_type=event_type,
                    risk_level=risk_level,
                    reasons=reasons,
                    dasha_info=f"{period['mahadasha']}-{period['antardasha']}",
                    affected_body_parts=body_parts if body_parts else ["General health"],
                    remedies=remedies
                ))

        # Sort by risk score (highest first)
        warnings.sort(key=lambda w: (
            {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}[w.risk_level.value],
            w.start_date
        ), reverse=True)

        return warnings

    def get_current_health_status(self) -> Dict:
        """Get current health risk status."""
        today = datetime.now()
        warnings = self.predict_health_issues(
            today.year,
            today.year + 1,
            min_risk_score=30
        )

        current_warnings = [
            w for w in warnings
            if w.start_date <= today <= w.end_date
        ]

        if not current_warnings:
            return {
                "status": "Good",
                "risk_level": "Low",
                "message": "No significant health concerns indicated currently",
                "warnings": []
            }

        highest_risk = current_warnings[0]
        return {
            "status": "Caution" if highest_risk.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL] else "Monitor",
            "risk_level": highest_risk.risk_level.value,
            "message": f"Current period ({highest_risk.dasha_info}) indicates {highest_risk.event_type.value} risk",
            "warnings": current_warnings[:3],
            "remedies": highest_risk.remedies
        }

    def get_accident_prone_periods(
        self,
        start_year: int,
        end_year: int,
        top_n: int = 5
    ) -> List[HealthWarning]:
        """Get specifically accident-prone periods."""
        all_warnings = self.predict_health_issues(start_year, end_year, min_risk_score=35)

        accident_warnings = [
            w for w in all_warnings
            if w.event_type in [HealthEventType.ACCIDENT, HealthEventType.SURGERY]
        ]

        return accident_warnings[:top_n]

    def get_health_summary(self, start_year: int, end_year: int) -> Dict:
        """Get a summary of health predictions."""
        warnings = self.predict_health_issues(start_year, end_year, min_risk_score=40)

        critical = [w for w in warnings if w.risk_level == RiskLevel.CRITICAL]
        high = [w for w in warnings if w.risk_level == RiskLevel.HIGH]
        medium = [w for w in warnings if w.risk_level == RiskLevel.MEDIUM]

        return {
            "period": f"{start_year} - {end_year}",
            "total_warnings": len(warnings),
            "critical_periods": len(critical),
            "high_risk_periods": len(high),
            "medium_risk_periods": len(medium),
            "top_warnings": warnings[:5],
            "accident_prone": self.get_accident_prone_periods(start_year, end_year, 3),
            "general_advice": self._get_general_advice()
        }

    def _get_general_advice(self) -> List[str]:
        """Get general health advice based on chart."""
        advice = []

        # Check 6th house
        sixth_planets = self.planets_in_houses.get(6, [])
        if "Mars" in sixth_planets:
            advice.append("Mars in 6th: Watch for inflammation, fevers, and accidents")
        if "Saturn" in sixth_planets:
            advice.append("Saturn in 6th: Chronic health issues possible, regular check-ups advised")

        # Check 8th house
        eighth_planets = self.planets_in_houses.get(8, [])
        if "Mars" in eighth_planets:
            advice.append("Mars in 8th: Be cautious about surgeries and accidents")
        if "Rahu" in eighth_planets:
            advice.append("Rahu in 8th: Watch for mysterious ailments, avoid risky activities")

        # Check Lagna lord
        lagna_lord = self.health_lords.get("lagna_lord")
        if lagna_lord in self.planets_in_houses.get(6, []):
            advice.append("Lagna lord in 6th: General health needs attention")
        if lagna_lord in self.planets_in_houses.get(8, []):
            advice.append("Lagna lord in 8th: Be cautious about sudden health events")

        if not advice:
            advice.append("No major chronic health indicators in birth chart")

        return advice
