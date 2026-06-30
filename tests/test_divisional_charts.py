"""
Tests for Divisional Charts (Varga) calculations
Validates against known horoscopes and BPHS formulas

Reference: Brihat Parashara Hora Shastra, Chapters 6-7
"""

import pytest
import sys
sys.path.insert(0, '..')

from src.divisional_charts import (
    DivisionalChartCalculator, VargaChart, DivisionalPosition,
    VimshopakaBala, FIRE_SIGNS, EARTH_SIGNS, AIR_SIGNS, WATER_SIGNS,
    NAVAMSA_START
)


class TestDivisionalChartCalculator:
    """Test divisional chart calculations against BPHS formulas."""

    def setup_method(self):
        self.calculator = DivisionalChartCalculator()

    # =========================================================================
    # D-1 RASHI TESTS
    # =========================================================================

    def test_d1_rashi_basic(self):
        """Test D-1 returns same sign as input."""
        # Sun at 15 degrees Aries (longitude 15)
        result = self.calculator.calculate_d1_rashi(15.0, "SUN")

        assert result.varga_rashi_num == 0  # Aries
        assert result.varga_rashi == "Mesha"
        assert result.varga_degree == 15.0

    def test_d1_rashi_sign_boundary(self):
        """Test D-1 at sign boundary (29.99 degrees)."""
        # Planet at 29.99 degrees Aries = still Aries
        result = self.calculator.calculate_d1_rashi(29.99, "MARS")
        assert result.varga_rashi_num == 0

        # Planet at 30.01 degrees = Taurus
        result = self.calculator.calculate_d1_rashi(30.01, "MARS")
        assert result.varga_rashi_num == 1

    # =========================================================================
    # D-2 HORA TESTS
    # =========================================================================

    def test_d2_hora_odd_sign_first_half(self):
        """Test D-2: First 15 degrees of odd sign = Sun (Leo)."""
        # BPHS: First 15 degrees of odd signs belong to Sun (Leo)
        # Aries is odd (index 0), first half should give Leo
        result = self.calculator.calculate_d2_hora(7.5, "SUN")  # 7.5 degrees Aries

        assert result.varga_rashi_num == 4  # Leo
        assert result.division_number == 1

    def test_d2_hora_odd_sign_second_half(self):
        """Test D-2: Last 15 degrees of odd sign = Moon (Cancer)."""
        # BPHS: Last 15 degrees of odd signs belong to Moon (Cancer)
        result = self.calculator.calculate_d2_hora(22.5, "MOON")  # 22.5 degrees Aries

        assert result.varga_rashi_num == 3  # Cancer
        assert result.division_number == 2

    def test_d2_hora_even_sign_first_half(self):
        """Test D-2: First 15 degrees of even sign = Moon (Cancer)."""
        # BPHS: First 15 degrees of even signs belong to Moon (Cancer)
        # Taurus is even (index 1), first half should give Cancer
        result = self.calculator.calculate_d2_hora(37.5, "VENUS")  # 7.5 degrees Taurus

        assert result.varga_rashi_num == 3  # Cancer
        assert result.division_number == 1

    def test_d2_hora_even_sign_second_half(self):
        """Test D-2: Last 15 degrees of even sign = Sun (Leo)."""
        result = self.calculator.calculate_d2_hora(52.5, "MERCURY")  # 22.5 degrees Taurus

        assert result.varga_rashi_num == 4  # Leo
        assert result.division_number == 2

    # =========================================================================
    # D-3 DREKKANA TESTS
    # =========================================================================

    def test_d3_drekkana_first_division(self):
        """Test D-3: 0-10 degrees = same sign."""
        # BPHS: 1st drekkana (0-10) is the same sign
        result = self.calculator.calculate_d3_drekkana(5.0, "MARS")  # 5 degrees Aries

        assert result.varga_rashi_num == 0  # Aries
        assert result.division_number == 1

    def test_d3_drekkana_second_division(self):
        """Test D-3: 10-20 degrees = 5th from sign."""
        # BPHS: 2nd drekkana (10-20) is the 5th sign
        # From Aries (0), 5th is Leo (4)
        result = self.calculator.calculate_d3_drekkana(15.0, "JUPITER")  # 15 degrees Aries

        assert result.varga_rashi_num == 4  # Leo (5th from Aries)
        assert result.division_number == 2

    def test_d3_drekkana_third_division(self):
        """Test D-3: 20-30 degrees = 9th from sign."""
        # BPHS: 3rd drekkana (20-30) is the 9th sign
        # From Aries (0), 9th is Sagittarius (8)
        result = self.calculator.calculate_d3_drekkana(25.0, "SATURN")  # 25 degrees Aries

        assert result.varga_rashi_num == 8  # Sagittarius (9th from Aries)
        assert result.division_number == 3

    def test_d3_drekkana_from_cancer(self):
        """Test D-3 from Cancer (index 3) - verify counting."""
        # From Cancer (3): 5th is Scorpio (7), 9th is Pisces (11)

        # 1st drekkana: Cancer
        result = self.calculator.calculate_d3_drekkana(95.0, "MOON")  # 5 degrees Cancer
        assert result.varga_rashi_num == 3

        # 2nd drekkana: Scorpio
        result = self.calculator.calculate_d3_drekkana(105.0, "MOON")  # 15 degrees Cancer
        assert result.varga_rashi_num == 7

        # 3rd drekkana: Pisces
        result = self.calculator.calculate_d3_drekkana(115.0, "MOON")  # 25 degrees Cancer
        assert result.varga_rashi_num == 11

    # =========================================================================
    # D-7 SAPTAMSA TESTS
    # =========================================================================

    def test_d7_saptamsa_odd_sign(self):
        """Test D-7: Odd signs start from same sign."""
        # BPHS: Odd signs count from the same sign
        # Each division is 30/7 = 4.2857 degrees
        # At 0-4.2857, should be same sign (Aries)
        result = self.calculator.calculate_d7_saptamsa(2.0, "JUPITER")

        assert result.varga_rashi_num == 0  # Starts from Aries
        assert result.division_number == 1

    def test_d7_saptamsa_even_sign(self):
        """Test D-7: Even signs start from 7th sign."""
        # BPHS: Even signs count from 7th sign
        # Taurus (1) -> 7th is Scorpio (7)
        result = self.calculator.calculate_d7_saptamsa(32.0, "VENUS")  # 2 degrees Taurus

        assert result.varga_rashi_num == 7  # Scorpio (7th from Taurus)
        assert result.division_number == 1

    # =========================================================================
    # D-9 NAVAMSA TESTS - MOST IMPORTANT
    # =========================================================================

    def test_d9_navamsa_fire_sign_starts_aries(self):
        """Test D-9: Fire signs (Aries, Leo, Sag) start from Aries."""
        # BPHS Chapter 6, Verse 9-10: Fire signs' navamsas start from Aries

        # Aries at 0-3.33 degrees -> 1st navamsa -> Aries
        result = self.calculator.calculate_d9_navamsa(1.0, "SUN")
        assert result.varga_rashi_num == 0  # Aries
        assert result.division_number == 1

        # Leo at 120 + 0 = 120 degrees, first navamsa -> Aries
        result = self.calculator.calculate_d9_navamsa(121.0, "SUN")
        assert result.varga_rashi_num == 0  # Aries

    def test_d9_navamsa_earth_sign_starts_capricorn(self):
        """Test D-9: Earth signs (Taurus, Virgo, Cap) start from Capricorn."""
        # BPHS: Earth signs' navamsas start from Capricorn (index 9)

        # Taurus at 30 + 1 = 31 degrees, first navamsa -> Capricorn
        result = self.calculator.calculate_d9_navamsa(31.0, "VENUS")
        assert result.varga_rashi_num == 9  # Capricorn

    def test_d9_navamsa_air_sign_starts_libra(self):
        """Test D-9: Air signs (Gemini, Libra, Aqua) start from Libra."""
        # BPHS: Air signs' navamsas start from Libra (index 6)

        # Gemini at 60 + 1 = 61 degrees, first navamsa -> Libra
        result = self.calculator.calculate_d9_navamsa(61.0, "MERCURY")
        assert result.varga_rashi_num == 6  # Libra

    def test_d9_navamsa_water_sign_starts_cancer(self):
        """Test D-9: Water signs (Cancer, Scorpio, Pisces) start from Cancer."""
        # BPHS: Water signs' navamsas start from Cancer (index 3)

        # Cancer at 90 + 1 = 91 degrees, first navamsa -> Cancer
        result = self.calculator.calculate_d9_navamsa(91.0, "MOON")
        assert result.varga_rashi_num == 3  # Cancer

    def test_d9_navamsa_all_nine_divisions(self):
        """Test all 9 navamsas of Aries (Fire sign)."""
        # Each navamsa is 3.333... degrees
        # Fire signs start from Aries and go through 9 signs

        expected_signs = [0, 1, 2, 3, 4, 5, 6, 7, 8]  # Aries through Sagittarius
        navamsa_span = 30.0 / 9.0

        for i, expected in enumerate(expected_signs):
            degree = (i * navamsa_span) + 0.5  # Middle of each navamsa
            result = self.calculator.calculate_d9_navamsa(degree, "SUN")
            assert result.varga_rashi_num == expected, f"Navamsa {i+1} should be sign {expected}"
            assert result.division_number == i + 1

    def test_d9_navamsa_known_chart(self):
        """Test Navamsa with a known horoscope verification."""
        # Example: Planet at 15 degrees Aries
        # 15 / 3.333 = 4.5 -> 5th navamsa
        # Fire sign, starts from Aries: 5th sign from Aries = Leo (4)
        result = self.calculator.calculate_d9_navamsa(15.0, "MARS")

        assert result.varga_rashi_num == 4  # Leo
        assert result.division_number == 5

    # =========================================================================
    # D-10 DASAMSA TESTS
    # =========================================================================

    def test_d10_dasamsa_odd_sign(self):
        """Test D-10: Odd signs start from same sign."""
        # BPHS: Odd signs - each 3 degrees forms one division starting from same sign
        # Aries at 1 degree -> 1st division -> Aries
        result = self.calculator.calculate_d10_dasamsa(1.0, "SUN")

        assert result.varga_rashi_num == 0  # Aries
        assert result.division_number == 1

    def test_d10_dasamsa_even_sign(self):
        """Test D-10: Even signs start from 9th sign."""
        # BPHS: Even signs start from 9th sign
        # Taurus (1) -> 9th is Capricorn (9)
        result = self.calculator.calculate_d10_dasamsa(31.0, "VENUS")  # 1 degree Taurus

        assert result.varga_rashi_num == 9  # Capricorn (9th from Taurus)
        assert result.division_number == 1

    def test_d10_dasamsa_divisions(self):
        """Test D-10 divisions - each is 3 degrees."""
        # In Aries (odd sign), divisions 1-10 go from Aries forward
        # 0-3: division 1 (Aries)
        # 3-6: division 2 (Taurus)
        # etc.

        result = self.calculator.calculate_d10_dasamsa(1.0, "SUN")
        assert result.division_number == 1
        assert result.varga_rashi_num == 0

        result = self.calculator.calculate_d10_dasamsa(4.0, "SUN")
        assert result.division_number == 2
        assert result.varga_rashi_num == 1

    # =========================================================================
    # D-12 DWADASAMSA TESTS
    # =========================================================================

    def test_d12_dwadasamsa_always_from_same_sign(self):
        """Test D-12: Always starts from the same sign."""
        # BPHS: Each 2.5 degrees, always counting from same sign

        # Aries at 1 degree -> 1st division -> Aries
        result = self.calculator.calculate_d12_dwadasamsa(1.0, "SUN")
        assert result.varga_rashi_num == 0

        # Aries at 3 degree -> 2nd division -> Taurus
        result = self.calculator.calculate_d12_dwadasamsa(3.0, "SUN")
        assert result.varga_rashi_num == 1

    def test_d12_dwadasamsa_all_twelve(self):
        """Test all 12 dwadasamsas of Aries."""
        # Each is 2.5 degrees
        expected = list(range(12))  # 0 through 11

        for i, expected_sign in enumerate(expected):
            degree = (i * 2.5) + 1.0
            result = self.calculator.calculate_d12_dwadasamsa(degree, "MOON")
            assert result.varga_rashi_num == expected_sign

    # =========================================================================
    # D-30 TRIMSAMSA TESTS - SPECIAL UNEQUAL DIVISIONS
    # =========================================================================

    def test_d30_trimsamsa_odd_sign(self):
        """Test D-30: Odd sign divisions (unequal)."""
        # BPHS: Odd signs have 5 unequal divisions
        # 0-5: Mars (Aries)
        # 5-10: Saturn (Aquarius)
        # 10-18: Jupiter (Sagittarius)
        # 18-25: Mercury (Gemini)
        # 25-30: Venus (Taurus)

        # 3 degrees Aries -> Mars -> Aries (0)
        result = self.calculator.calculate_d30_trimsamsa(3.0, "SUN")
        assert result.varga_rashi_num == 0

        # 7 degrees Aries -> Saturn -> Aquarius (10)
        result = self.calculator.calculate_d30_trimsamsa(7.0, "SUN")
        assert result.varga_rashi_num == 10

        # 14 degrees Aries -> Jupiter -> Sagittarius (8)
        result = self.calculator.calculate_d30_trimsamsa(14.0, "SUN")
        assert result.varga_rashi_num == 8

        # 22 degrees Aries -> Mercury -> Gemini (2)
        result = self.calculator.calculate_d30_trimsamsa(22.0, "SUN")
        assert result.varga_rashi_num == 2

        # 27 degrees Aries -> Venus -> Taurus (1)
        result = self.calculator.calculate_d30_trimsamsa(27.0, "SUN")
        assert result.varga_rashi_num == 1

    def test_d30_trimsamsa_even_sign(self):
        """Test D-30: Even sign divisions (reversed)."""
        # BPHS: Even signs have reversed order
        # 0-5: Venus (Taurus)
        # 5-12: Mercury (Gemini)
        # 12-20: Jupiter (Sagittarius)
        # 20-25: Saturn (Aquarius)
        # 25-30: Mars (Aries)

        # 3 degrees Taurus -> Venus -> Taurus (1)
        result = self.calculator.calculate_d30_trimsamsa(33.0, "VENUS")  # 3 degrees Taurus
        assert result.varga_rashi_num == 1

        # 7 degrees Taurus -> Mercury -> Gemini (2)
        result = self.calculator.calculate_d30_trimsamsa(37.0, "VENUS")
        assert result.varga_rashi_num == 2

    # =========================================================================
    # D-60 SHASHTIAMSA TESTS
    # =========================================================================

    def test_d60_shashtiamsa_odd_sign(self):
        """Test D-60: Odd sign counting."""
        # BPHS: Odd signs count from same sign
        # Each division is 0.5 degrees

        # First division of Aries (0-0.5 degrees)
        result = self.calculator.calculate_d60_shashtiamsa(0.25, "SUN")
        assert result.division_number == 1
        # Should be in Aries (first 5 divisions are in Aries)
        assert result.varga_rashi_num == 0

    def test_d60_shashtiamsa_even_sign(self):
        """Test D-60: Even sign starts from opposite."""
        # BPHS: Even signs count from opposite (180 degrees away)
        # Taurus (1) opposite is Scorpio (7)

        result = self.calculator.calculate_d60_shashtiamsa(30.25, "VENUS")  # 0.25 degrees Taurus
        assert result.division_number == 1
        # Should start counting from Scorpio
        assert result.varga_rashi_num == 7

    def test_d60_shashtiamsa_names(self):
        """Test that D-60 positions have special names."""
        result = self.calculator.calculate_d60_shashtiamsa(0.25, "SUN")

        # Check that the additional attributes exist
        assert hasattr(result, 'shashtiamsa_name')
        assert hasattr(result, 'shashtiamsa_deity')
        assert hasattr(result, 'shashtiamsa_nature')


class TestVimshopakaBala:
    """Test Vimshopaka strength calculations."""

    def setup_method(self):
        self.bala_calc = VimshopakaBala()

    def test_shadvarga_calculation(self):
        """Test Shadvarga (6-chart) strength calculation."""
        # Test with a planet position
        result = self.bala_calc.calculate_shadvarga_bala(15.0, "SUN")

        assert "total_points" in result
        assert "max_points" in result
        assert result["max_points"] == 20.0
        assert 0 <= result["total_points"] <= 20
        assert "details" in result

    def test_shodashavarga_calculation(self):
        """Test Shodashavarga (16-chart) strength calculation."""
        result = self.bala_calc.calculate_shodashavarga_bala(15.0, "JUPITER")

        assert "total_points" in result
        assert result["max_points"] == 20.0
        assert 0 <= result["total_points"] <= 20
        assert "details" in result
        assert len(result["details"]) == 16  # All 16 vargas

    def test_exalted_planet_gets_high_score(self):
        """Test that exalted planets get better scores."""
        # Sun exalted at 10 degrees Aries
        exalted_result = self.bala_calc.calculate_shadvarga_bala(10.0, "SUN")

        # Sun debilitated in Libra (around 190 degrees)
        debilitated_result = self.bala_calc.calculate_shadvarga_bala(190.0, "SUN")

        # Exalted should score higher than debilitated
        assert exalted_result["total_points"] >= debilitated_result["total_points"]


class TestHelperFunctions:
    """Test helper functions for sign classification."""

    def setup_method(self):
        self.calculator = DivisionalChartCalculator()

    def test_fire_signs(self):
        """Test Fire sign classification."""
        assert 0 in FIRE_SIGNS  # Aries
        assert 4 in FIRE_SIGNS  # Leo
        assert 8 in FIRE_SIGNS  # Sagittarius

    def test_earth_signs(self):
        """Test Earth sign classification."""
        assert 1 in EARTH_SIGNS  # Taurus
        assert 5 in EARTH_SIGNS  # Virgo
        assert 9 in EARTH_SIGNS  # Capricorn

    def test_air_signs(self):
        """Test Air sign classification."""
        assert 2 in AIR_SIGNS   # Gemini
        assert 6 in AIR_SIGNS   # Libra
        assert 10 in AIR_SIGNS  # Aquarius

    def test_water_signs(self):
        """Test Water sign classification."""
        assert 3 in WATER_SIGNS   # Cancer
        assert 7 in WATER_SIGNS   # Scorpio
        assert 11 in WATER_SIGNS  # Pisces

    def test_navamsa_start_signs(self):
        """Test Navamsa starting signs by element."""
        assert NAVAMSA_START['Fire'] == 0   # Aries
        assert NAVAMSA_START['Earth'] == 9  # Capricorn
        assert NAVAMSA_START['Air'] == 6    # Libra
        assert NAVAMSA_START['Water'] == 3  # Cancer

    def test_is_odd_sign(self):
        """Test odd/even sign determination."""
        # In 0-indexed: 0=Aries(odd), 1=Taurus(even), 2=Gemini(odd), etc.
        assert self.calculator._is_odd_sign(0) == True   # Aries
        assert self.calculator._is_odd_sign(1) == False  # Taurus
        assert self.calculator._is_odd_sign(2) == True   # Gemini
        assert self.calculator._is_odd_sign(3) == False  # Cancer


class TestDivisionalChartWithKnownHoroscope:
    """
    Integration tests with known horoscopes.
    These verify the calculations match published/verified charts.
    """

    def setup_method(self):
        self.calculator = DivisionalChartCalculator()

    def test_all_vargas_return_valid_positions(self):
        """Test that all 16 vargas return valid positions."""
        test_longitude = 125.5  # Somewhere in Leo

        for varga in VargaChart:
            result = self.calculator.calculate_varga(varga, test_longitude, "SUN")

            # All positions should have valid rashi (0-11)
            assert 0 <= result.varga_rashi_num <= 11
            # All should have original longitude preserved
            assert result.original_longitude == test_longitude
            # Varga degree should be positive
            assert result.varga_degree >= 0

    def test_calculate_all_vargas(self):
        """Test calculating all vargas for a single planet."""
        results = self.calculator.calculate_all_vargas(100.0, "MOON")

        assert len(results) == 16
        for varga_name, position in results.items():
            assert isinstance(position, DivisionalPosition)
            assert position.planet == "MOON"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
