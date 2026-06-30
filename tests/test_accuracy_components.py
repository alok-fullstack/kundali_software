"""
Unit tests for Rashifal accuracy enhancement components.

Tests cover:
1. Shadbala (Six-fold strength) calculation
2. Combustion (Asta) detection
3. Planetary War (Graha Yuddha) detection
4. Tara Bala (Nakshatra strength) calculation
5. Navamsa (D9) strength check

Reference: BPHS Chapters 6, 17, 25, 27
"""

import pytest
from datetime import datetime

# Import functions from rashifal module
from src.rashifal import (
    check_combustion,
    check_planetary_war,
    calculate_tarabala,
    get_navamsa_strength_modifier,
    RashifalCalculator,
    RashifalPeriod,
)

# Import Shadbala calculator
try:
    from src.shadbala import ShadbalaCalculator, ShadbalaResult
    SHADBALA_AVAILABLE = True
except ImportError:
    SHADBALA_AVAILABLE = False


class TestCombustion:
    """Tests for combustion (Asta) detection."""

    def test_mercury_combust_close(self):
        """Mercury within 5° of Sun should be combust with high severity."""
        is_combust, severity = check_combustion("MERCURY", 100.0, 105.0, False)
        assert is_combust is True
        assert severity > 0.5

    def test_mercury_not_combust_far(self):
        """Mercury more than 14° from Sun should not be combust."""
        is_combust, severity = check_combustion("MERCURY", 100.0, 120.0, False)
        assert is_combust is False
        assert severity == 0.0

    def test_venus_combust(self):
        """Venus within 10° of Sun should be combust."""
        is_combust, severity = check_combustion("VENUS", 150.0, 155.0, False)
        assert is_combust is True

    def test_retrograde_tighter_orb(self):
        """Retrograde Mercury has tighter combustion orb (12° instead of 14°)."""
        # At 13° - combust if direct, not combust if retrograde
        is_combust_direct, _ = check_combustion("MERCURY", 100.0, 113.0, False)
        is_combust_retro, _ = check_combustion("MERCURY", 100.0, 113.0, True)
        assert is_combust_direct is True  # 13 < 14
        assert is_combust_retro is False  # 13 > 12

    def test_sun_cannot_combust(self):
        """Sun itself cannot be combust."""
        is_combust, severity = check_combustion("SUN", 100.0, 100.0, False)
        assert is_combust is False

    def test_rahu_cannot_combust(self):
        """Rahu (node) cannot be combust."""
        is_combust, severity = check_combustion("RAHU", 100.0, 105.0, False)
        assert is_combust is False

    def test_severity_calculation(self):
        """Severity should be proportional to distance."""
        # Very close = high severity
        _, severity_close = check_combustion("MARS", 100.0, 101.0, False)
        # At orb boundary = low severity
        _, severity_far = check_combustion("MARS", 100.0, 115.0, False)
        assert severity_close > severity_far


class TestPlanetaryWar:
    """Tests for planetary war (Graha Yuddha) detection."""

    def test_war_within_one_degree(self):
        """Planets within 1° should be in war."""
        positions = {
            "MARS": {"longitude": 45.5},
            "SATURN": {"longitude": 45.8}
        }
        wars = check_planetary_war(positions)
        assert len(wars) == 1
        assert wars[0]["winner"] == "SATURN"  # Higher longitude wins
        assert wars[0]["loser"] == "MARS"

    def test_no_war_beyond_one_degree(self):
        """Planets more than 1° apart should not be in war."""
        positions = {
            "MARS": {"longitude": 45.0},
            "SATURN": {"longitude": 47.0}
        }
        wars = check_planetary_war(positions)
        assert len(wars) == 0

    def test_sun_moon_excluded(self):
        """Sun and Moon cannot participate in planetary war."""
        positions = {
            "SUN": {"longitude": 100.0},
            "MARS": {"longitude": 100.5},
            "MOON": {"longitude": 100.2},
        }
        wars = check_planetary_war(positions)
        # Only MARS in the war_planets list, so no war possible
        assert len(wars) == 0

    def test_multiple_wars(self):
        """Multiple planets in close proximity create multiple wars."""
        positions = {
            "MARS": {"longitude": 100.0},
            "MERCURY": {"longitude": 100.3},
            "VENUS": {"longitude": 100.6},
        }
        wars = check_planetary_war(positions)
        # Mars-Mercury war, Mars-Venus war, Mercury-Venus war
        assert len(wars) == 3


class TestTaraBala:
    """Tests for Tara Bala (nakshatra strength) calculation."""

    def test_janma_tara(self):
        """Same nakshatra = Janma (1st Tara) - challenging."""
        result = calculate_tarabala(0, 0)
        assert result["name"] == "Janma"
        assert result["favorable"] is False
        assert result["modifier"] < 0

    def test_sampat_tara(self):
        """2nd nakshatra = Sampat - good for wealth."""
        result = calculate_tarabala(0, 1)
        assert result["name"] == "Sampat"
        assert result["favorable"] is True
        assert result["modifier"] > 0

    def test_vipat_tara(self):
        """3rd nakshatra = Vipat - dangerous."""
        result = calculate_tarabala(0, 2)
        assert result["name"] == "Vipat"
        assert result["favorable"] is False

    def test_naidhana_tara(self):
        """7th nakshatra = Naidhana - most inauspicious."""
        result = calculate_tarabala(0, 6)
        assert result["name"] == "Naidhana"
        assert result["favorable"] is False
        assert result["modifier"] < -0.2  # Strong negative

    def test_parama_mitra_tara(self):
        """9th nakshatra = Parama Mitra - best friend, most auspicious."""
        result = calculate_tarabala(0, 8)
        assert result["name"] == "Parama Mitra"
        assert result["favorable"] is True
        assert result["modifier"] > 0.2  # Strong positive

    def test_cycle_wraps(self):
        """Tara cycle should wrap around (10th = 1st of next cycle)."""
        result = calculate_tarabala(0, 9)
        # 9 % 9 = 0, which gives tara_num = 1 (Janma)
        assert result["name"] == "Janma"

    def test_with_offset(self):
        """Birth nakshatra offset should work correctly."""
        # Birth nak = 5, transit = 7 → count = 2 → tara = 3 (Vipat)
        result = calculate_tarabala(5, 7)
        assert result["name"] == "Vipat"


class TestNavamsa:
    """Tests for Navamsa (D9) strength check."""

    def test_fire_sign_navamsa_start(self):
        """Fire sign navamsas start from Aries."""
        # Aries (0°-30°), first navamsa (0°-3.33°) = Aries
        modifier = get_navamsa_strength_modifier("MARS", 1.0)
        # Mars in Aries navamsa could be own sign
        # (depends on Mars own signs in PLANET_DIGNITIES)
        assert isinstance(modifier, float)

    def test_modifier_range(self):
        """Navamsa modifier should be within expected range."""
        modifier = get_navamsa_strength_modifier("JUPITER", 180.0)
        assert -0.15 <= modifier <= 0.20

    def test_rahu_ketu_no_modifier(self):
        """Rahu and Ketu should return 0 modifier."""
        modifier_rahu = get_navamsa_strength_modifier("RAHU", 100.0)
        modifier_ketu = get_navamsa_strength_modifier("KETU", 100.0)
        assert modifier_rahu == 0.0
        assert modifier_ketu == 0.0


@pytest.mark.skipif(not SHADBALA_AVAILABLE, reason="Shadbala module not available")
class TestShadbala:
    """Tests for Shadbala (six-fold strength) calculation."""

    def test_naisargika_bala_sun(self):
        """Sun should have highest natural strength."""
        planets_data = {
            "SUN": {"longitude": 100.0, "rashi": "Karka", "rashi_num": 3}
        }
        calc = ShadbalaCalculator(planets_data=planets_data)
        result = calc.calculate_naisargika_bala("SUN")
        assert result == 60.0  # Sun has maximum natural bala

    def test_naisargika_bala_saturn(self):
        """Saturn should have lowest natural strength."""
        planets_data = {
            "SATURN": {"longitude": 200.0, "rashi": "Tula", "rashi_num": 6}
        }
        calc = ShadbalaCalculator(planets_data=planets_data)
        result = calc.calculate_naisargika_bala("SATURN")
        assert result == 8.57  # Saturn has minimum natural bala

    def test_dig_bala_sun_in_10th(self):
        """Sun in 10th house should have maximum directional strength."""
        planets_data = {
            "SUN": {"longitude": 270.0, "rashi": "Makara", "rashi_num": 9}
        }
        calc = ShadbalaCalculator(planets_data=planets_data)
        calc.lagna_rashi = "Mesha"  # Aries lagna
        # Sun in Capricorn from Aries lagna = 10th house
        result = calc.calculate_dig_bala("SUN")
        assert result == 60.0  # Maximum dig bala in 10th

    def test_shadbala_result_structure(self):
        """ShadbalaResult should have all 6 components."""
        planets_data = {
            "JUPITER": {
                "longitude": 100.0,
                "rashi": "Karka",
                "rashi_num": 3,
                "speed": 0.08
            }
        }
        calc = ShadbalaCalculator(planets_data=planets_data)
        result = calc.calculate_shadbala("JUPITER")

        assert isinstance(result, ShadbalaResult)
        assert hasattr(result, "sthana_bala")
        assert hasattr(result, "dig_bala")
        assert hasattr(result, "kaala_bala")
        assert hasattr(result, "chesta_bala")
        assert hasattr(result, "naisargika_bala")
        assert hasattr(result, "drik_bala")
        assert hasattr(result, "total")
        assert hasattr(result, "strength_percent")
        assert hasattr(result, "strength_level")

    def test_strength_levels(self):
        """Strength levels should be correctly assigned."""
        planets_data = {
            "MARS": {"longitude": 15.0, "rashi": "Mesha", "rashi_num": 0}
        }
        calc = ShadbalaCalculator(planets_data=planets_data)

        # Test level classification
        assert calc.get_strength_level(450, "MARS") == "very_strong"
        assert calc.get_strength_level(300, "MARS") == "strong"
        assert calc.get_strength_level(210, "MARS") == "average"
        assert calc.get_strength_level(100, "MARS") == "weak"


class TestIntegration:
    """Integration tests for accuracy components in Rashifal."""

    def test_rashifal_has_accuracy_flags(self):
        """RashifalPrediction should include all accuracy flags."""
        calc = RashifalCalculator()
        result = calc.generate_rashifal(0, RashifalPeriod.DAILY)

        # Check base flags exist
        assert hasattr(result, "has_ashtakavarga")
        assert hasattr(result, "has_vedha")
        assert hasattr(result, "has_kakshya")

        # Check new accuracy flags exist
        assert hasattr(result, "has_shadbala")
        assert hasattr(result, "has_combustion_check")
        assert hasattr(result, "has_tarabala")
        assert hasattr(result, "has_planetary_war")
        assert hasattr(result, "has_navamsa_check")

        # Check new data fields exist
        assert hasattr(result, "combusted_planets")
        assert hasattr(result, "planetary_wars")
        assert hasattr(result, "tarabala_info")

    def test_planetary_influences_have_new_data(self):
        """Planetary influences should include new accuracy data when applicable."""
        calc = RashifalCalculator()
        result = calc.generate_rashifal(0, RashifalPeriod.DAILY)

        # Check structure of influences
        for influence in result.planetary_influences:
            assert "planet" in influence
            assert "house_from_moon" in influence
            assert "effect" in influence
            assert "intensity" in influence

    def test_different_periods_different_scores(self):
        """Different periods should potentially give different scores."""
        calc = RashifalCalculator()
        date = datetime(2026, 6, 28, 12, 0, 0)

        daily = calc.generate_rashifal(0, RashifalPeriod.DAILY, date)
        weekly = calc.generate_rashifal(0, RashifalPeriod.WEEKLY, date)
        monthly = calc.generate_rashifal(0, RashifalPeriod.MONTHLY, date)
        yearly = calc.generate_rashifal(0, RashifalPeriod.YEARLY, date)

        # All should have valid scores
        assert 1 <= daily.overall_score <= 10
        assert 1 <= weekly.overall_score <= 10
        assert 1 <= monthly.overall_score <= 10
        assert 1 <= yearly.overall_score <= 10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
