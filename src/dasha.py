"""
Vimshottari Dasha Calculator
The most widely used dasha system in Vedic Astrology
Total cycle: 120 years
"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from dataclasses import dataclass

from .config import (
    NAKSHATRAS, NAKSHATRA_SPAN,
    VIMSHOTTARI_YEARS, DASHA_SEQUENCE, VIMSHOTTARI_TOTAL_YEARS
)


@dataclass
class DashaPeriod:
    """Represents a Mahadasha or Antardasha period."""
    planet: str
    start_date: datetime
    end_date: datetime
    duration_years: float
    level: str  # "mahadasha", "antardasha", "pratyantardasha"

    def __str__(self):
        return f"{self.planet} {self.level}: {self.start_date.strftime('%Y-%m-%d')} to {self.end_date.strftime('%Y-%m-%d')}"


class VimshottariDasha:
    """
    Calculate Vimshottari Dasha based on Moon's Nakshatra at birth.

    The dasha system divides life into planetary periods based on
    the Moon's position in a Nakshatra at birth.
    """

    def __init__(self):
        self.total_years = VIMSHOTTARI_TOTAL_YEARS
        self.dasha_years = VIMSHOTTARI_YEARS
        self.sequence = DASHA_SEQUENCE

    def get_nakshatra_lord(self, nakshatra_num: int) -> str:
        """Get the ruling planet of a nakshatra."""
        return NAKSHATRAS[nakshatra_num]["lord"]

    def get_balance_of_dasha(
        self,
        moon_longitude: float,
        birth_datetime: datetime
    ) -> Tuple[str, float, datetime]:
        """
        Calculate the balance of Mahadasha at birth.

        When a person is born, they are in the middle of a Mahadasha.
        This calculates how much of that dasha remains.

        Returns:
            Tuple of (dasha_lord, years_remaining, dasha_end_date)
        """
        # Find nakshatra and position within it
        nakshatra_num = int(moon_longitude / NAKSHATRA_SPAN)
        degree_in_nakshatra = moon_longitude % NAKSHATRA_SPAN

        # Percentage of nakshatra already traversed
        proportion_elapsed = degree_in_nakshatra / NAKSHATRA_SPAN

        # Get nakshatra lord (starting dasha planet)
        dasha_lord = self.get_nakshatra_lord(nakshatra_num)

        # Get total years for this dasha
        total_dasha_years = self.dasha_years[dasha_lord]

        # Calculate remaining years
        years_remaining = total_dasha_years * (1 - proportion_elapsed)

        # Calculate end date
        days_remaining = years_remaining * 365.25
        dasha_end_date = birth_datetime + timedelta(days=days_remaining)

        return dasha_lord, years_remaining, dasha_end_date

    def calculate_mahadashas(
        self,
        moon_longitude: float,
        birth_datetime: datetime,
        years_ahead: int = 120
    ) -> List[DashaPeriod]:
        """
        Calculate all Mahadasha periods from birth.

        Args:
            moon_longitude: Moon's sidereal longitude at birth
            birth_datetime: Date and time of birth
            years_ahead: How many years of dashas to calculate

        Returns:
            List of DashaPeriod objects for each Mahadasha
        """
        mahadashas = []

        # Make datetime timezone-naive for consistent calculations
        if hasattr(birth_datetime, 'tzinfo') and birth_datetime.tzinfo:
            birth_datetime = birth_datetime.replace(tzinfo=None)

        # Get balance of first dasha
        first_lord, balance_years, first_end = self.get_balance_of_dasha(
            moon_longitude, birth_datetime
        )

        # Find starting position in sequence
        start_idx = self.sequence.index(first_lord)

        current_date = birth_datetime
        end_limit = birth_datetime + timedelta(days=years_ahead * 365.25)

        # First (partial) dasha
        mahadashas.append(DashaPeriod(
            planet=first_lord,
            start_date=current_date,
            end_date=first_end,
            duration_years=balance_years,
            level="mahadasha"
        ))
        current_date = first_end

        # Subsequent full dashas
        idx = (start_idx + 1) % 9
        while current_date < end_limit:
            planet = self.sequence[idx]
            years = self.dasha_years[planet]
            end_date = current_date + timedelta(days=years * 365.25)

            mahadashas.append(DashaPeriod(
                planet=planet,
                start_date=current_date,
                end_date=end_date,
                duration_years=years,
                level="mahadasha"
            ))

            current_date = end_date
            idx = (idx + 1) % 9

        return mahadashas

    def calculate_antardashas(
        self,
        mahadasha: DashaPeriod
    ) -> List[DashaPeriod]:
        """
        Calculate Antardasha (sub-periods) within a Mahadasha.

        Each Mahadasha contains 9 Antardashas in the same sequence,
        starting from the Mahadasha lord itself.
        """
        antardashas = []
        start_idx = self.sequence.index(mahadasha.planet)

        current_date = mahadasha.start_date
        mahadasha_days = (mahadasha.end_date - mahadasha.start_date).days

        for i in range(9):
            idx = (start_idx + i) % 9
            planet = self.sequence[idx]

            # Antardasha duration is proportional to its Mahadasha years
            proportion = self.dasha_years[planet] / self.total_years
            antardasha_days = mahadasha_days * proportion
            end_date = current_date + timedelta(days=antardasha_days)

            antardashas.append(DashaPeriod(
                planet=planet,
                start_date=current_date,
                end_date=end_date,
                duration_years=antardasha_days / 365.25,
                level="antardasha"
            ))

            current_date = end_date

        return antardashas

    def calculate_pratyantardashas(
        self,
        antardasha: DashaPeriod
    ) -> List[DashaPeriod]:
        """
        Calculate Pratyantardasha (sub-sub-periods) within an Antardasha.
        """
        pratyantardashas = []
        start_idx = self.sequence.index(antardasha.planet)

        current_date = antardasha.start_date
        antardasha_days = (antardasha.end_date - antardasha.start_date).days

        for i in range(9):
            idx = (start_idx + i) % 9
            planet = self.sequence[idx]

            proportion = self.dasha_years[planet] / self.total_years
            pratyantar_days = antardasha_days * proportion
            end_date = current_date + timedelta(days=pratyantar_days)

            pratyantardashas.append(DashaPeriod(
                planet=planet,
                start_date=current_date,
                end_date=end_date,
                duration_years=pratyantar_days / 365.25,
                level="pratyantardasha"
            ))

            current_date = end_date

        return pratyantardashas

    def get_current_dasha(
        self,
        moon_longitude: float,
        birth_datetime: datetime,
        target_date: datetime = None
    ) -> Dict:
        """
        Get the running Mahadasha, Antardasha, and Pratyantardasha
        for a given date (default: today).
        """
        if target_date is None:
            target_date = datetime.now()

        # Make both datetimes timezone-naive for comparison
        if hasattr(birth_datetime, 'tzinfo') and birth_datetime.tzinfo:
            birth_datetime = birth_datetime.replace(tzinfo=None)
        if hasattr(target_date, 'tzinfo') and target_date.tzinfo:
            target_date = target_date.replace(tzinfo=None)

        mahadashas = self.calculate_mahadashas(moon_longitude, birth_datetime)

        current_maha = None
        for maha in mahadashas:
            if maha.start_date <= target_date <= maha.end_date:
                current_maha = maha
                break

        if not current_maha:
            return {"error": "Date outside calculated range"}

        antardashas = self.calculate_antardashas(current_maha)
        current_antar = None
        for antar in antardashas:
            if antar.start_date <= target_date <= antar.end_date:
                current_antar = antar
                break

        if not current_antar:
            return {"error": "Antardasha not found for target date"}

        pratyantardashas = self.calculate_pratyantardashas(current_antar)
        current_pratyantar = None
        for pratyantar in pratyantardashas:
            if pratyantar.start_date <= target_date <= pratyantar.end_date:
                current_pratyantar = pratyantar
                break

        if not current_pratyantar:
            return {"error": "Pratyantardasha not found for target date"}

        return {
            "date": target_date,
            "mahadasha": {
                "planet": current_maha.planet,
                "start": current_maha.start_date,
                "end": current_maha.end_date,
            },
            "antardasha": {
                "planet": current_antar.planet,
                "start": current_antar.start_date,
                "end": current_antar.end_date,
            },
            "pratyantardasha": {
                "planet": current_pratyantar.planet,
                "start": current_pratyantar.start_date,
                "end": current_pratyantar.end_date,
            },
            "full_dasha": f"{current_maha.planet}-{current_antar.planet}-{current_pratyantar.planet}"
        }
