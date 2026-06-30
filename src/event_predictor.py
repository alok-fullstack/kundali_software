"""
Event Timing Predictor for Vedic Astrology
Predicts favorable periods for major life events based on Dasha and Transit analysis

Supported predictions:
- Marriage timing
- Career change
- Property purchase
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from .dasha import VimshottariDasha, DashaPeriod
from .planets import PlanetaryCalculator
from .transit import TransitCalculator
from .config import (
    Planet, RASHIS, HOUSE_LORDSHIPS, VIMSHOTTARI_YEARS,
    FUNCTIONAL_BENEFICS, FUNCTIONAL_MALEFICS, YOGAKARAKA
)


@dataclass
class PredictionPeriod:
    """Represents a favorable period for an event."""
    period: str  # Human readable format "Jan 2027 - Jun 2027"
    start_date: datetime
    end_date: datetime
    favorability: str  # "High", "Medium", "Low"
    score: int  # 0-100
    reasons: List[str]
    event_type: str  # "marriage", "career", "property"


class EventPredictor:
    """
    Predicts timing of major life events based on Vedic astrology.

    Uses combination of:
    1. Dasha analysis (Mahadasha, Antardasha)
    2. Transit analysis (Jupiter, Saturn transits)
    3. Age considerations
    """

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
        self.moon_rashi = kundali.planets["MOON"]["rashi"]
        self.moon_rashi_num = kundali.planets["MOON"]["rashi_num"]
        self.lagna_rashi_num = kundali.lagna["rashi_num"]
        self.birth_date = kundali.birth_data.date

        # Get dasha calculator
        self.dasha_calculator = VimshottariDasha()
        self.planet_calculator = PlanetaryCalculator()

        # Initialize transit calculator for accurate transit analysis
        self.transit_calculator = TransitCalculator(kundali)

        # Calculate house lords for this lagna
        self.house_lords = self._calculate_house_lords()

        # Get planets in houses
        self.planets_in_houses = kundali.get_planets_in_houses()

    def _calculate_house_lords(self) -> Dict[int, str]:
        """Calculate which planet rules each house for this lagna."""
        house_lords = {}
        lordships = HOUSE_LORDSHIPS.get(self.lagna_rashi, {})

        # Reverse the mapping: from planet->houses to house->planet
        for planet, houses in lordships.items():
            for house in houses:
                house_lords[house] = planet

        return house_lords

    def _get_seventh_lord(self) -> str:
        """Get the lord of the 7th house (marriage house)."""
        return self.house_lords.get(7, "VENUS")

    def _get_fourth_lord(self) -> str:
        """Get the lord of the 4th house (property/home house)."""
        return self.house_lords.get(4, "MOON")

    def _get_tenth_lord(self) -> str:
        """Get the lord of the 10th house (career house)."""
        return self.house_lords.get(10, "SATURN")

    def _get_dasha_periods_in_range(
        self,
        start_year: int,
        end_year: int
    ) -> List[Dict]:
        """
        Get all Mahadasha and Antardasha periods within the given year range.

        Returns list of periods with start_date, end_date, mahadasha, antardasha
        """
        periods = []

        # Get mahadashas
        moon_longitude = self.planets["MOON"]["longitude"]
        mahadashas = self.dasha_calculator.calculate_mahadashas(
            moon_longitude,
            self.birth_date,
            years_ahead=150
        )

        start_date = datetime(start_year, 1, 1)
        end_date = datetime(end_year, 12, 31)

        for maha in mahadashas:
            # Skip if mahadasha is completely outside range
            if maha.end_date < start_date or maha.start_date > end_date:
                continue

            # Get antardashas for this mahadasha
            antardashas = self.dasha_calculator.calculate_antardashas(maha)

            for antar in antardashas:
                # Skip if antardasha is outside range
                if antar.end_date < start_date or antar.start_date > end_date:
                    continue

                # Clip to our range
                period_start = max(antar.start_date, start_date)
                period_end = min(antar.end_date, end_date)

                periods.append({
                    "start_date": period_start,
                    "end_date": period_end,
                    "mahadasha": maha.planet,
                    "antardasha": antar.planet,
                    "mahadasha_lord": maha.planet,
                    "antardasha_lord": antar.planet
                })

        return periods

    def _get_planet_transit_info(self, planet: str, date: datetime) -> Dict:
        """
        Get comprehensive transit info for a planet using TransitCalculator.

        Args:
            planet: Planet name (e.g., "JUPITER", "SATURN")
            date: Date to check transit

        Returns:
            Dict with rashi_num, house_from_moon, house_from_lagna, etc.
        """
        transit_from_moon = self.transit_calculator.get_transit_house_from_moon(planet, date)
        transit_from_lagna = self.transit_calculator.get_transit_house_from_lagna(planet, date)

        # Get position data for rashi number
        pos = self.transit_calculator.get_single_planet_position(planet, date)

        return {
            "rashi_num": pos["rashi_num"],
            "rashi": pos["rashi"],
            "house_from_moon": transit_from_moon["house_from_moon"],
            "house_from_lagna": transit_from_lagna["house_from_lagna"],
            "general_effect": transit_from_moon["general_effect"],
            "is_retrograde": pos["is_retrograde"]
        }

    def _calculate_jupiter_transit_rashi(self, date: datetime) -> int:
        """Calculate Jupiter's rashi on a given date."""
        return self._get_planet_transit_info("JUPITER", date)["rashi_num"]

    def _calculate_saturn_transit_rashi(self, date: datetime) -> int:
        """Calculate Saturn's rashi on a given date."""
        return self._get_planet_transit_info("SATURN", date)["rashi_num"]

    def _calculate_venus_transit_rashi(self, date: datetime) -> int:
        """Calculate Venus's rashi on a given date."""
        return self._get_planet_transit_info("VENUS", date)["rashi_num"]

    def _calculate_mars_transit_rashi(self, date: datetime) -> int:
        """Calculate Mars's rashi on a given date."""
        return self._get_planet_transit_info("MARS", date)["rashi_num"]

    def _is_jupiter_aspecting_house(self, jupiter_rashi_num: int, target_house: int) -> bool:
        """
        Check if Jupiter aspects a given house from current position.
        Jupiter aspects 5th, 7th, and 9th houses from its position.
        """
        target_rashi_num = (self.lagna_rashi_num + target_house - 1) % 12

        # Calculate difference
        diff = (target_rashi_num - jupiter_rashi_num) % 12

        # Jupiter aspects 5th (index 4), 7th (index 6), 9th (index 8) from its position
        # Also direct aspect on the house it occupies (index 0)
        return diff in [0, 4, 6, 8]

    def _is_jupiter_in_house(self, jupiter_rashi_num: int, target_house: int) -> bool:
        """Check if Jupiter is transiting a given house."""
        target_rashi_num = (self.lagna_rashi_num + target_house - 1) % 12
        return jupiter_rashi_num == target_rashi_num

    def _get_house_from_rashi(self, rashi_num: int, reference: str = "lagna") -> int:
        """Get house number from rashi, relative to lagna or moon."""
        if reference == "moon":
            ref_rashi = self.moon_rashi_num
        else:
            ref_rashi = self.lagna_rashi_num

        return ((rashi_num - ref_rashi) % 12) + 1

    def _calculate_age_at_date(self, date: datetime) -> float:
        """Calculate age at a given date."""
        birth_date = self.birth_date
        if hasattr(birth_date, 'tzinfo') and birth_date.tzinfo:
            birth_date = birth_date.replace(tzinfo=None)
        if hasattr(date, 'tzinfo') and date.tzinfo:
            date = date.replace(tzinfo=None)

        age_days = (date - birth_date).days
        return age_days / 365.25

    def _format_period_string(self, start: datetime, end: datetime) -> str:
        """Format date range as human readable string."""
        return f"{start.strftime('%b %Y')} - {end.strftime('%b %Y')}"

    def predict_marriage_timing(
        self,
        start_year: int,
        end_year: int,
        gender: str = "male"
    ) -> List[Dict]:
        """
        Predict favorable periods for marriage.

        Marriage timing factors in Vedic astrology:
        1. Dasha Analysis (most important):
           - Venus Mahadasha/Antardasha - Venus is karaka for marriage
           - 7th lord Mahadasha/Antardasha - 7th house rules marriage
           - Jupiter dasha for females, Venus dasha for males
           - Rahu dasha can also give marriage (unconventional)

        2. Transit Analysis:
           - Jupiter transiting 7th house from Moon/Lagna
           - Jupiter aspecting 7th house or 7th lord
           - Venus transiting favorable houses

        3. Age considerations:
           - Typical marriage age: 24-32 for modern India
           - Weight periods within this range higher

        Args:
            start_year: Start year for prediction
            end_year: End year for prediction
            gender: "male" or "female" (affects dasha interpretation)

        Returns:
            List of favorable periods with scores and reasons
        """
        predictions = []
        seventh_lord = self._get_seventh_lord()

        # Get all dasha periods in range
        dasha_periods = self._get_dasha_periods_in_range(start_year, end_year)

        # Marriage-favorable dashas
        marriage_favorable_mahadasha = {"Venus", "Jupiter", "Rahu", "Moon"}
        marriage_favorable_antardasha = {"Venus", "Jupiter", seventh_lord, "Moon", "Rahu"}

        # Add 7th lord to favorable mahadashas
        if seventh_lord not in marriage_favorable_mahadasha:
            marriage_favorable_mahadasha.add(seventh_lord)

        for period in dasha_periods:
            score = 0
            reasons = []

            maha = period["mahadasha"]
            antar = period["antardasha"]
            mid_date = period["start_date"] + (period["end_date"] - period["start_date"]) / 2

            # === DASHA ANALYSIS ===

            # Venus Mahadasha (karaka for marriage)
            if maha == "Venus":
                score += 25
                reasons.append("Venus Mahadasha active - primary marriage karaka")

            # 7th lord Mahadasha
            if maha == seventh_lord:
                score += 25
                reasons.append(f"7th lord ({seventh_lord}) Mahadasha - direct marriage indicator")

            # Jupiter Mahadasha (especially for females)
            if maha == "Jupiter":
                if gender == "female":
                    score += 20
                    reasons.append("Jupiter Mahadasha - auspicious for female marriage")
                else:
                    score += 10
                    reasons.append("Jupiter Mahadasha - generally favorable")

            # Rahu Mahadasha (can give marriage, especially unconventional)
            if maha == "Rahu":
                score += 10
                reasons.append("Rahu Mahadasha - can indicate marriage (possibly unconventional)")

            # Moon Mahadasha
            if maha == "Moon":
                score += 10
                reasons.append("Moon Mahadasha - emotional fulfillment period")

            # === ANTARDASHA ANALYSIS ===

            # Venus Antardasha
            if antar == "Venus":
                score += 20
                reasons.append("Venus Antardasha - marriage karaka period active")

            # 7th lord Antardasha
            if antar == seventh_lord:
                score += 20
                reasons.append(f"7th lord ({seventh_lord}) Antardasha - marriage activation")

            # Jupiter Antardasha
            if antar == "Jupiter":
                if gender == "female":
                    score += 15
                    reasons.append("Jupiter Antardasha - husband karaka for females")
                else:
                    score += 10
                    reasons.append("Jupiter Antardasha - blessings and expansion")

            # Moon Antardasha in Venus Mahadasha
            if maha == "Venus" and antar == "Moon":
                score += 5
                reasons.append("Venus-Moon period - romantic and emotional")

            # === TRANSIT ANALYSIS ===

            try:
                jupiter_rashi = self._calculate_jupiter_transit_rashi(mid_date)

                # Jupiter in 7th from Lagna
                seventh_house_from_lagna = self._get_house_from_rashi(jupiter_rashi, "lagna")
                if seventh_house_from_lagna == 7:
                    score += 15
                    reasons.append("Jupiter transiting 7th house from Lagna")

                # Jupiter in 7th from Moon
                seventh_house_from_moon = self._get_house_from_rashi(jupiter_rashi, "moon")
                if seventh_house_from_moon == 7:
                    score += 15
                    reasons.append("Jupiter transiting 7th house from Moon")

                # Jupiter aspecting 7th house
                if self._is_jupiter_aspecting_house(jupiter_rashi, 7):
                    score += 10
                    reasons.append("Jupiter aspecting 7th house")

                # Jupiter in 1st house (auspicious for self)
                if seventh_house_from_lagna == 1:
                    score += 8
                    reasons.append("Jupiter transiting Lagna - personal growth")

                # Jupiter in 5th house (romance)
                if seventh_house_from_lagna == 5:
                    score += 8
                    reasons.append("Jupiter transiting 5th house - romance favorable")

            except Exception:
                pass  # Transit calculation failed, continue with dasha analysis

            # === AGE CONSIDERATION ===

            age = self._calculate_age_at_date(mid_date)

            # Optimal marriage age range (modern India)
            if 24 <= age <= 32:
                score += 10
                reasons.append(f"Age {int(age)} - optimal marriage age range")
            elif 22 <= age <= 24 or 32 <= age <= 35:
                score += 5
                reasons.append(f"Age {int(age)} - reasonable marriage age")
            elif age < 21:
                score -= 10
                reasons.append(f"Age {int(age)} - too young for marriage")
            elif age > 40:
                score -= 5
                reasons.append(f"Age {int(age)} - later in typical range")

            # Normalize score to 0-100
            score = max(0, min(100, score))

            # Only include periods with meaningful scores
            if score >= 20:
                # Determine favorability
                if score >= 70:
                    favorability = "High"
                elif score >= 45:
                    favorability = "Medium"
                else:
                    favorability = "Low"

                predictions.append({
                    "period": self._format_period_string(period["start_date"], period["end_date"]),
                    "start_date": period["start_date"],
                    "end_date": period["end_date"],
                    "favorability": favorability,
                    "score": score,
                    "reasons": reasons,
                    "dasha": f"{maha}-{antar}"
                })

        # Sort by score (highest first)
        predictions.sort(key=lambda x: x["score"], reverse=True)

        return predictions

    def predict_career_change(
        self,
        start_year: int,
        end_year: int
    ) -> List[Dict]:
        """
        Predict favorable periods for career change or advancement.

        Career timing factors:
        1. Dasha Analysis:
           - 10th lord Mahadasha/Antardasha - career house
           - Saturn dasha - karaka for profession
           - Sun dasha - authority and government
           - Mercury dasha - business and communication
           - Rahu dasha - sudden changes, unconventional careers

        2. Transit Analysis:
           - Jupiter transiting 10th house
           - Saturn transiting 10th or aspecting 10th
           - Jupiter aspecting 10th house

        3. Career houses: 10th (profession), 6th (service), 2nd (income)

        Args:
            start_year: Start year for prediction
            end_year: End year for prediction

        Returns:
            List of favorable periods for career change
        """
        predictions = []
        tenth_lord = self._get_tenth_lord()
        sixth_lord = self.house_lords.get(6, "MERCURY")
        second_lord = self.house_lords.get(2, "VENUS")

        # Get all dasha periods in range
        dasha_periods = self._get_dasha_periods_in_range(start_year, end_year)

        for period in dasha_periods:
            score = 0
            reasons = []

            maha = period["mahadasha"]
            antar = period["antardasha"]
            mid_date = period["start_date"] + (period["end_date"] - period["start_date"]) / 2

            # === DASHA ANALYSIS ===

            # 10th lord Mahadasha
            if maha == tenth_lord:
                score += 25
                reasons.append(f"10th lord ({tenth_lord}) Mahadasha - career activation")

            # Saturn Mahadasha (karaka for profession)
            if maha == "Saturn":
                score += 20
                reasons.append("Saturn Mahadasha - profession karaka period")

            # Sun Mahadasha (authority, government)
            if maha == "Sun":
                score += 15
                reasons.append("Sun Mahadasha - authority and recognition")

            # Mercury Mahadasha (business, communication)
            if maha == "Mercury":
                score += 15
                reasons.append("Mercury Mahadasha - business and intellectual pursuits")

            # Rahu Mahadasha (sudden changes)
            if maha == "Rahu":
                score += 15
                reasons.append("Rahu Mahadasha - sudden career changes possible")

            # Jupiter Mahadasha (growth and expansion)
            if maha == "Jupiter":
                score += 15
                reasons.append("Jupiter Mahadasha - growth and expansion")

            # === ANTARDASHA ANALYSIS ===

            # 10th lord Antardasha
            if antar == tenth_lord:
                score += 20
                reasons.append(f"10th lord ({tenth_lord}) Antardasha - career focus")

            # Saturn Antardasha
            if antar == "Saturn":
                score += 15
                reasons.append("Saturn Antardasha - professional responsibilities")

            # Sun Antardasha
            if antar == "Sun":
                score += 10
                reasons.append("Sun Antardasha - leadership opportunities")

            # 6th lord Antardasha (service)
            if antar == sixth_lord:
                score += 10
                reasons.append(f"6th lord ({sixth_lord}) Antardasha - service sector activity")

            # Mercury Antardasha
            if antar == "Mercury":
                score += 10
                reasons.append("Mercury Antardasha - new skills and communication")

            # === TRANSIT ANALYSIS ===

            try:
                jupiter_rashi = self._calculate_jupiter_transit_rashi(mid_date)
                saturn_rashi = self._calculate_saturn_transit_rashi(mid_date)

                # Jupiter in 10th from Lagna
                house_from_lagna = self._get_house_from_rashi(jupiter_rashi, "lagna")
                if house_from_lagna == 10:
                    score += 15
                    reasons.append("Jupiter transiting 10th house - career growth")

                # Jupiter aspecting 10th house
                if self._is_jupiter_aspecting_house(jupiter_rashi, 10):
                    score += 10
                    reasons.append("Jupiter aspecting 10th house")

                # Saturn in 10th from Lagna (can be challenging but transformative)
                saturn_house = self._get_house_from_rashi(saturn_rashi, "lagna")
                if saturn_house == 10:
                    score += 10
                    reasons.append("Saturn transiting 10th house - career restructuring")

                # Jupiter in 11th house (gains)
                if house_from_lagna == 11:
                    score += 8
                    reasons.append("Jupiter in 11th house - gains from profession")

                # Jupiter in 2nd house (income)
                if house_from_lagna == 2:
                    score += 8
                    reasons.append("Jupiter in 2nd house - income increase")

            except Exception:
                pass

            # === AGE CONSIDERATION ===

            age = self._calculate_age_at_date(mid_date)

            # Career change more common in certain age ranges
            if 25 <= age <= 35:
                score += 5
                reasons.append(f"Age {int(age)} - prime career development years")
            elif 35 <= age <= 45:
                score += 5
                reasons.append(f"Age {int(age)} - career peak transition period")

            # Normalize score
            score = max(0, min(100, score))

            if score >= 20:
                if score >= 65:
                    favorability = "High"
                elif score >= 40:
                    favorability = "Medium"
                else:
                    favorability = "Low"

                predictions.append({
                    "period": self._format_period_string(period["start_date"], period["end_date"]),
                    "start_date": period["start_date"],
                    "end_date": period["end_date"],
                    "favorability": favorability,
                    "score": score,
                    "reasons": reasons,
                    "dasha": f"{maha}-{antar}"
                })

        predictions.sort(key=lambda x: x["score"], reverse=True)
        return predictions

    def predict_property_purchase(
        self,
        start_year: int,
        end_year: int
    ) -> List[Dict]:
        """
        Predict favorable periods for property/home purchase.

        Property timing factors:
        1. Dasha Analysis:
           - 4th lord Mahadasha/Antardasha - home and property house
           - Mars dasha - karaka for land and property
           - Moon dasha - comfort and domestic happiness
           - Venus dasha - luxury and comforts
           - Saturn dasha - real estate and building

        2. Transit Analysis:
           - Jupiter transiting 4th house
           - Jupiter aspecting 4th house
           - Saturn transiting/aspecting 4th (construction/renovation)

        3. Property houses: 4th (home), 2nd (wealth), 11th (gains)

        Args:
            start_year: Start year for prediction
            end_year: End year for prediction

        Returns:
            List of favorable periods for property purchase
        """
        predictions = []
        fourth_lord = self._get_fourth_lord()
        second_lord = self.house_lords.get(2, "VENUS")
        eleventh_lord = self.house_lords.get(11, "SATURN")

        # Get all dasha periods in range
        dasha_periods = self._get_dasha_periods_in_range(start_year, end_year)

        for period in dasha_periods:
            score = 0
            reasons = []

            maha = period["mahadasha"]
            antar = period["antardasha"]
            mid_date = period["start_date"] + (period["end_date"] - period["start_date"]) / 2

            # === DASHA ANALYSIS ===

            # 4th lord Mahadasha
            if maha == fourth_lord:
                score += 25
                reasons.append(f"4th lord ({fourth_lord}) Mahadasha - property acquisition period")

            # Mars Mahadasha (karaka for land)
            if maha == "Mars":
                score += 20
                reasons.append("Mars Mahadasha - land and property karaka")

            # Moon Mahadasha (domestic happiness)
            if maha == "Moon":
                score += 15
                reasons.append("Moon Mahadasha - domestic comfort and settlement")

            # Venus Mahadasha (luxuries, vehicles, comforts)
            if maha == "Venus":
                score += 15
                reasons.append("Venus Mahadasha - luxury and comforts")

            # Saturn Mahadasha (real estate, building)
            if maha == "Saturn":
                score += 15
                reasons.append("Saturn Mahadasha - real estate and construction")

            # Jupiter Mahadasha (expansion, growth)
            if maha == "Jupiter":
                score += 10
                reasons.append("Jupiter Mahadasha - expansion and blessings")

            # === ANTARDASHA ANALYSIS ===

            # 4th lord Antardasha
            if antar == fourth_lord:
                score += 20
                reasons.append(f"4th lord ({fourth_lord}) Antardasha - home matters activated")

            # Mars Antardasha
            if antar == "Mars":
                score += 15
                reasons.append("Mars Antardasha - property and land acquisition")

            # Moon Antardasha
            if antar == "Moon":
                score += 10
                reasons.append("Moon Antardasha - emotional attachment to home")

            # Venus Antardasha
            if antar == "Venus":
                score += 10
                reasons.append("Venus Antardasha - beautiful home and comforts")

            # Saturn Antardasha
            if antar == "Saturn":
                score += 10
                reasons.append("Saturn Antardasha - building or buying property")

            # 2nd lord Antardasha (wealth for purchase)
            if antar == second_lord:
                score += 10
                reasons.append(f"2nd lord ({second_lord}) Antardasha - wealth availability")

            # 11th lord Antardasha (gains)
            if antar == eleventh_lord:
                score += 8
                reasons.append(f"11th lord ({eleventh_lord}) Antardasha - gains and fulfillment")

            # === TRANSIT ANALYSIS ===

            try:
                jupiter_rashi = self._calculate_jupiter_transit_rashi(mid_date)
                saturn_rashi = self._calculate_saturn_transit_rashi(mid_date)
                mars_rashi = self._calculate_mars_transit_rashi(mid_date)

                # Jupiter in 4th from Lagna
                house_from_lagna = self._get_house_from_rashi(jupiter_rashi, "lagna")
                if house_from_lagna == 4:
                    score += 15
                    reasons.append("Jupiter transiting 4th house - home blessings")

                # Jupiter aspecting 4th house
                if self._is_jupiter_aspecting_house(jupiter_rashi, 4):
                    score += 10
                    reasons.append("Jupiter aspecting 4th house")

                # Jupiter in 4th from Moon
                house_from_moon = self._get_house_from_rashi(jupiter_rashi, "moon")
                if house_from_moon == 4:
                    score += 10
                    reasons.append("Jupiter in 4th from Moon - mental peace")

                # Saturn in 4th (renovation/restructuring)
                saturn_house = self._get_house_from_rashi(saturn_rashi, "lagna")
                if saturn_house == 4:
                    score += 8
                    reasons.append("Saturn transiting 4th house - property restructuring")

                # Mars in 4th or aspecting (can be double-edged)
                mars_house = self._get_house_from_rashi(mars_rashi, "lagna")
                if mars_house == 4:
                    score += 5
                    reasons.append("Mars transiting 4th house - property activity")

                # Jupiter in 11th (gains)
                if house_from_lagna == 11:
                    score += 8
                    reasons.append("Jupiter in 11th house - gains and fulfillment")

                # Jupiter in 2nd (wealth)
                if house_from_lagna == 2:
                    score += 8
                    reasons.append("Jupiter in 2nd house - wealth accumulation")

            except Exception:
                pass

            # === AGE CONSIDERATION ===

            age = self._calculate_age_at_date(mid_date)

            # Property purchase common in certain age ranges
            if 28 <= age <= 45:
                score += 5
                reasons.append(f"Age {int(age)} - typical property buying age")
            elif 45 <= age <= 55:
                score += 3
                reasons.append(f"Age {int(age)} - second property/upgrade period")

            # Normalize score
            score = max(0, min(100, score))

            if score >= 20:
                if score >= 65:
                    favorability = "High"
                elif score >= 40:
                    favorability = "Medium"
                else:
                    favorability = "Low"

                predictions.append({
                    "period": self._format_period_string(period["start_date"], period["end_date"]),
                    "start_date": period["start_date"],
                    "end_date": period["end_date"],
                    "favorability": favorability,
                    "score": score,
                    "reasons": reasons,
                    "dasha": f"{maha}-{antar}"
                })

        predictions.sort(key=lambda x: x["score"], reverse=True)
        return predictions

    def get_best_periods(
        self,
        event_type: str,
        start_year: int,
        end_year: int,
        top_n: int = 5,
        gender: str = "male"
    ) -> List[Dict]:
        """
        Get the top N best periods for a given event type.

        Args:
            event_type: "marriage", "career", or "property"
            start_year: Start year for prediction
            end_year: End year for prediction
            top_n: Number of best periods to return
            gender: Gender for marriage prediction (ignored for others)

        Returns:
            Top N favorable periods sorted by score
        """
        if event_type == "marriage":
            predictions = self.predict_marriage_timing(start_year, end_year, gender)
        elif event_type == "career":
            predictions = self.predict_career_change(start_year, end_year)
        elif event_type == "property":
            predictions = self.predict_property_purchase(start_year, end_year)
        else:
            raise ValueError(f"Unknown event type: {event_type}")

        # Sort by score descending and return top N
        # Include all favorability levels, sorted by score
        sorted_predictions = sorted(predictions, key=lambda x: x.get("score", 0), reverse=True)

        return sorted_predictions[:top_n]

    def get_comprehensive_prediction(
        self,
        start_year: int,
        end_year: int,
        gender: str = "male"
    ) -> Dict:
        """
        Get comprehensive prediction for all major life events.

        Returns:
            Dictionary with predictions for marriage, career, and property
        """
        return {
            "marriage": self.get_best_periods("marriage", start_year, end_year, 5, gender),
            "career": self.get_best_periods("career", start_year, end_year, 5),
            "property": self.get_best_periods("property", start_year, end_year, 5),
            "analysis_period": f"{start_year} - {end_year}",
            "lagna": self.lagna_rashi,
            "moon_sign": self.moon_rashi
        }
