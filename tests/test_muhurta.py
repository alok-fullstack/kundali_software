"""
Tests for Muhurta Module
Validates Panchang calculations, inauspicious periods, and Muhurta selection
"""

import pytest
from datetime import datetime
import sys
sys.path.insert(0, '..')

from src.panchang import PanchangCalculator, TithiData, YogaData
from src.muhurta_rules import (
    EventType,
    calculate_rahu_kala,
    calculate_yamaghantaka,
    calculate_tarabala,
    calculate_chandrabala,
    get_event_rules,
)
from src.muhurta import MuhurtaCalculator, find_best_muhurtas
from src.kundali import create_kundali


class TestPanchangCalculator:
    """Test Panchang calculations."""

    def setup_method(self):
        self.calculator = PanchangCalculator()

    def test_panchang_has_five_limbs(self):
        """Test that Panchang returns all five limbs."""
        dt = datetime(2024, 6, 15, 12, 0, 0)
        panchang = self.calculator.get_panchang(dt)

        assert panchang.tithi is not None
        assert panchang.nakshatra is not None
        assert panchang.yoga is not None
        assert panchang.karana is not None
        assert panchang.vara is not None

    def test_tithi_range(self):
        """Test Tithi number is in valid range (1-30)."""
        dt = datetime(2024, 6, 15, 12, 0, 0)
        panchang = self.calculator.get_panchang(dt)

        assert 1 <= panchang.tithi.number <= 30

    def test_tithi_paksha(self):
        """Test Tithi paksha is Shukla or Krishna."""
        dt = datetime(2024, 6, 15, 12, 0, 0)
        panchang = self.calculator.get_panchang(dt)

        assert panchang.tithi.paksha in ["Shukla", "Krishna"]

    def test_yoga_range(self):
        """Test Yoga number is in valid range (1-27)."""
        dt = datetime(2024, 6, 15, 12, 0, 0)
        panchang = self.calculator.get_panchang(dt)

        assert 1 <= panchang.yoga.number <= 27

    def test_karana_has_name(self):
        """Test Karana has a valid name."""
        dt = datetime(2024, 6, 15, 12, 0, 0)
        panchang = self.calculator.get_panchang(dt)

        assert panchang.karana.name in [
            "Bava", "Balava", "Kaulava", "Taitila", "Gara",
            "Vanija", "Vishti", "Shakuni", "Chatushpada", "Naga", "Kimstughna"
        ]

    def test_vara_weekday(self):
        """Test Vara matches expected weekday."""
        dt = datetime(2024, 6, 15, 12, 0, 0)
        panchang = self.calculator.get_panchang(dt)

        expected_weekday = "Saturday"
        assert panchang.vara.english == expected_weekday

    def test_sunrise_before_sunset(self):
        """Test sunrise is before sunset."""
        dt = datetime(2024, 6, 15, 12, 0, 0)
        panchang = self.calculator.get_panchang(dt)

        assert panchang.sunrise < panchang.sunset

    def test_rikta_tithi_detection(self):
        """Test Rikta tithi detection (4th, 9th, 14th)."""
        panchang = self.calculator.get_panchang(datetime(2024, 6, 15, 12, 0, 0))

        if panchang.tithi.number in [4, 9, 14, 19, 24, 29]:
            assert panchang.tithi.is_rikta == True


class TestInauspiciousPeriods:
    """Test inauspicious period calculations."""

    def test_rahu_kala_duration(self):
        """Test Rahu Kala is approximately 1/8 of day."""
        sunrise = datetime(2024, 6, 15, 6, 0, 0)
        sunset = datetime(2024, 6, 15, 18, 0, 0)

        for weekday in range(7):
            start, end = calculate_rahu_kala(sunrise, sunset, weekday)
            duration = (end - start).total_seconds()

            expected_duration = (12 * 3600) / 8
            assert abs(duration - expected_duration) < 60

    def test_rahu_kala_within_day(self):
        """Test Rahu Kala is within sunrise-sunset."""
        sunrise = datetime(2024, 6, 15, 6, 0, 0)
        sunset = datetime(2024, 6, 15, 18, 0, 0)

        for weekday in range(7):
            start, end = calculate_rahu_kala(sunrise, sunset, weekday)
            assert start >= sunrise
            assert end <= sunset

    def test_yamaghantaka_duration(self):
        """Test Yamaghantaka is approximately 1/8 of day."""
        sunrise = datetime(2024, 6, 15, 6, 0, 0)
        sunset = datetime(2024, 6, 15, 18, 0, 0)

        for weekday in range(7):
            start, end = calculate_yamaghantaka(sunrise, sunset, weekday)
            duration = (end - start).total_seconds()

            expected_duration = (12 * 3600) / 8
            assert abs(duration - expected_duration) < 60


class TestTarabala:
    """Test Tarabala calculations."""

    def test_tarabala_range(self):
        """Test Tarabala number is 1-9."""
        for birth in range(27):
            for current in range(27):
                tara_num, name, effect, score = calculate_tarabala(birth, current)
                assert 1 <= tara_num <= 9

    def test_janma_tara(self):
        """Test Janma tara when same nakshatra."""
        tara_num, name, effect, score = calculate_tarabala(0, 0)
        assert tara_num == 1
        assert name == "Janma"
        assert score == 0

    def test_sampat_tara(self):
        """Test Sampat tara (2nd from birth)."""
        tara_num, name, effect, score = calculate_tarabala(0, 1)
        assert tara_num == 2
        assert name == "Sampat"
        assert score == 10

    def test_tarabala_cycle(self):
        """Test 9-fold cycle repeats."""
        tara1, _, _, _ = calculate_tarabala(0, 9)
        tara2, _, _, _ = calculate_tarabala(0, 18)

        assert tara1 == tara2


class TestChandrabala:
    """Test Chandrabala calculations."""

    def test_chandrabala_range(self):
        """Test Chandrabala house is 1-12."""
        for natal in range(12):
            for transit in range(12):
                house, score, effect = calculate_chandrabala(natal, transit)
                assert 1 <= house <= 12

    def test_favorable_houses(self):
        """Test favorable houses have high scores."""
        favorable = [1, 3, 6, 7, 10, 11]

        for house in favorable:
            transit = house - 1
            h, score, _ = calculate_chandrabala(0, transit)
            assert score >= 5

    def test_unfavorable_houses(self):
        """Test unfavorable houses have zero score."""
        unfavorable = [4, 8, 12]

        for house in unfavorable:
            transit = house - 1
            h, score, _ = calculate_chandrabala(0, transit)
            assert score == 0


class TestEventRules:
    """Test event-specific rules."""

    def test_marriage_rules_exist(self):
        """Test marriage rules have required keys."""
        rules = get_event_rules(EventType.MARRIAGE)

        assert "favorable_nakshatras" in rules
        assert "unfavorable_nakshatras" in rules
        assert "favorable_tithis" in rules
        assert "unfavorable_tithis" in rules
        assert "favorable_weekdays" in rules

    def test_marriage_favorable_nakshatras(self):
        """Test marriage has specific favorable nakshatras."""
        rules = get_event_rules(EventType.MARRIAGE)

        assert 3 in rules["favorable_nakshatras"]
        assert 26 in rules["favorable_nakshatras"]

    def test_career_rules_different(self):
        """Test career rules differ from marriage."""
        marriage_rules = get_event_rules(EventType.MARRIAGE)
        career_rules = get_event_rules(EventType.CAREER)

        assert marriage_rules["favorable_nakshatras"] != career_rules["favorable_nakshatras"]


class TestMuhurtaCalculator:
    """Test MuhurtaCalculator integration."""

    def setup_method(self):
        self.kundali = create_kundali(
            name="Test Person",
            year=1990,
            month=5,
            day=15,
            hour=10,
            minute=30,
            city="Delhi"
        )

    def test_find_muhurtas_returns_list(self):
        """Test find_muhurtas returns a list."""
        calc = MuhurtaCalculator(self.kundali)

        muhurtas = calc.find_muhurtas(
            event_type=EventType.MARRIAGE,
            start_date=datetime(2027, 1, 1),
            end_date=datetime(2027, 1, 31),
            use_event_predictor=False,
            min_score=30,
            top_n=5
        )

        assert isinstance(muhurtas, list)

    def test_muhurtas_have_required_fields(self):
        """Test muhurta windows have all required fields."""
        calc = MuhurtaCalculator(self.kundali)

        muhurtas = calc.find_muhurtas(
            event_type=EventType.MARRIAGE,
            start_date=datetime(2027, 1, 1),
            end_date=datetime(2027, 1, 31),
            use_event_predictor=False,
            min_score=30,
            top_n=5
        )

        if muhurtas:
            m = muhurtas[0]
            assert hasattr(m, "date")
            assert hasattr(m, "score")
            assert hasattr(m, "panchang")
            assert hasattr(m, "tarabala_score")
            assert hasattr(m, "chandrabala_score")

    def test_muhurtas_sorted_by_score(self):
        """Test muhurtas are sorted by score (descending)."""
        calc = MuhurtaCalculator(self.kundali)

        muhurtas = calc.find_muhurtas(
            event_type=EventType.MARRIAGE,
            start_date=datetime(2027, 1, 1),
            end_date=datetime(2027, 1, 31),
            use_event_predictor=False,
            min_score=30,
            top_n=10
        )

        if len(muhurtas) > 1:
            for i in range(len(muhurtas) - 1):
                assert muhurtas[i].score >= muhurtas[i + 1].score

    def test_convenience_function(self):
        """Test find_best_muhurtas convenience function."""
        muhurtas = find_best_muhurtas(
            kundali=self.kundali,
            event_type="marriage",
            start_date=datetime(2027, 1, 1),
            end_date=datetime(2027, 1, 31),
            top_n=3,
            min_score=30
        )

        assert isinstance(muhurtas, list)
        assert len(muhurtas) <= 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
