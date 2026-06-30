"""
Tests for Kundali Software
Validates planetary calculations against known ephemeris data
"""

import pytest
from datetime import datetime
import sys
sys.path.insert(0, '..')

from src.planets import PlanetaryCalculator, format_degree
from src.dasha import VimshottariDasha
from src.config import Planet, NAKSHATRAS


class TestPlanetaryCalculator:
    """Test planetary position calculations."""

    def setup_method(self):
        self.calculator = PlanetaryCalculator()

    def test_julian_day_conversion(self):
        """Test Julian Day calculation."""
        # Known value: J2000.0 epoch = 2451545.0
        dt = datetime(2000, 1, 1, 12, 0, 0)
        jd = self.calculator.datetime_to_jd(dt, "UTC")
        assert abs(jd - 2451545.0) < 0.01

    def test_ayanamsa_lahiri(self):
        """Test Lahiri ayanamsa calculation."""
        # Ayanamsa on Jan 1, 2000 should be approximately 23.85 degrees
        jd = 2451545.0  # J2000.0
        ayanamsa = self.calculator.get_ayanamsa_value(jd)
        assert 23.5 < ayanamsa < 24.5

    def test_planet_position_sun(self):
        """Test Sun position calculation."""
        # On April 14, 2024, Sun enters Mesha (Aries)
        dt = datetime(2024, 4, 14, 12, 0, 0)
        jd = self.calculator.datetime_to_jd(dt, "Asia/Kolkata")
        sun_pos = self.calculator.get_planet_position(Planet.SUN, jd)

        # Sun should be in Mesha (Aries) around this date
        assert sun_pos["rashi"] == "Mesha"

    def test_planet_position_moon(self):
        """Test Moon position calculation."""
        dt = datetime(2024, 1, 1, 12, 0, 0)
        jd = self.calculator.datetime_to_jd(dt, "Asia/Kolkata")
        moon_pos = self.calculator.get_planet_position(Planet.MOON, jd)

        # Moon should have valid nakshatra
        assert moon_pos["nakshatra"] in [n["name"] for n in NAKSHATRAS]
        assert 1 <= moon_pos["pada"] <= 4

    def test_rahu_ketu_opposite(self):
        """Test that Rahu and Ketu are always 180° apart."""
        dt = datetime(2024, 6, 15, 12, 0, 0)
        jd = self.calculator.datetime_to_jd(dt, "Asia/Kolkata")

        rahu_pos = self.calculator.get_planet_position(Planet.RAHU, jd)
        ketu_pos = self.calculator.get_planet_position(Planet.KETU, jd)

        diff = abs(rahu_pos["longitude"] - ketu_pos["longitude"])
        assert abs(diff - 180) < 0.01 or abs(diff - 180) > 359.99

    def test_lagna_calculation(self):
        """Test Lagna (Ascendant) calculation."""
        dt = datetime(2024, 1, 1, 6, 0, 0)  # Early morning
        jd = self.calculator.datetime_to_jd(dt, "Asia/Kolkata")

        # Delhi coordinates
        lagna = self.calculator.get_lagna(jd, 28.6139, 77.2090)

        assert 0 <= lagna["rashi_num"] <= 11
        assert lagna["nakshatra"] in [n["name"] for n in NAKSHATRAS]

    def test_all_planets(self):
        """Test that all 9 planets are calculated."""
        dt = datetime(2024, 1, 1, 12, 0, 0)
        jd = self.calculator.datetime_to_jd(dt, "Asia/Kolkata")

        planets = self.calculator.get_all_planets(jd)

        assert len(planets) == 9
        for planet in Planet:
            assert planet.name in planets


class TestVimshottariDasha:
    """Test Vimshottari Dasha calculations."""

    def setup_method(self):
        self.dasha = VimshottariDasha()

    def test_total_dasha_years(self):
        """Test that total dasha cycle is 120 years."""
        total = sum(self.dasha.dasha_years.values())
        assert total == 120

    def test_dasha_sequence(self):
        """Test dasha sequence has 9 planets."""
        assert len(self.dasha.sequence) == 9

    def test_balance_of_dasha(self):
        """Test balance calculation."""
        # Moon at 0° (start of Ashwini) should give full Ketu dasha
        moon_long = 0.0
        birth_dt = datetime(2000, 1, 1, 0, 0, 0)

        lord, balance, _ = self.dasha.get_balance_of_dasha(moon_long, birth_dt)

        assert lord == "Ketu"
        assert abs(balance - 7.0) < 0.1  # Ketu dasha is 7 years

    def test_mahadasha_sequence(self):
        """Test that mahadashas follow correct sequence."""
        moon_long = 50.0  # Somewhere in Rohini (Moon's nakshatra)
        birth_dt = datetime(2000, 1, 1, 0, 0, 0)

        mahadashas = self.dasha.calculate_mahadashas(moon_long, birth_dt, years=50)

        # Check that dashas progress correctly
        assert len(mahadashas) > 0
        for maha in mahadashas:
            assert maha.planet in self.dasha.sequence

    def test_antardasha_count(self):
        """Test that each mahadasha has 9 antardashas."""
        moon_long = 100.0
        birth_dt = datetime(2000, 1, 1, 0, 0, 0)

        mahadashas = self.dasha.calculate_mahadashas(moon_long, birth_dt, years=20)
        antardashas = self.dasha.calculate_antardashas(mahadashas[0])

        assert len(antardashas) == 9


class TestFormatting:
    """Test formatting functions."""

    def test_format_degree(self):
        """Test degree formatting."""
        assert "23°30'" in format_degree(23.5)
        assert "0°00'" in format_degree(0.0)
        assert "29°59'" in format_degree(29.99)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
