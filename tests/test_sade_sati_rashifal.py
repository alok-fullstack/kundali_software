"""
Tests for Sade Sati Rashifal Integration Module

Tests cover:
- Sade Sati phase detection
- Dhaiya detection
- Score modifiers
- Remedial factors
- Integration with Rashifal
"""

import pytest
from datetime import datetime

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.sade_sati_rashifal import (
    SadeSatiPhase,
    DhaiyaType,
    SadeSatiRashifalCalculator,
    check_sade_sati_for_moon_sign,
    get_sade_sati_affected_rashis,
    get_dhaiya_affected_rashis,
    SADE_SATI_PHASE_EFFECTS,
    DHAIYA_EFFECTS,
    SATURN_YOGAKARAKA_LAGNAS,
)


class TestSadeSatiPhaseDetection:
    """Test Sade Sati phase detection logic."""

    def setup_method(self):
        """Set up test fixtures."""
        self.calculator = SadeSatiRashifalCalculator()

    def test_detect_rising_phase(self):
        """Saturn in 12th from Moon should be Rising phase."""
        # Moon in Aries (0), Saturn in Pisces (11) = 12th from Moon
        saturn_house = self.calculator.get_saturn_position_from_moon(11, 0)
        assert saturn_house == 12
        phase = self.calculator.detect_sade_sati_phase(saturn_house)
        assert phase == SadeSatiPhase.RISING

    def test_detect_peak_phase(self):
        """Saturn over Moon should be Peak phase."""
        # Moon in Aries (0), Saturn in Aries (0) = 1st from Moon
        saturn_house = self.calculator.get_saturn_position_from_moon(0, 0)
        assert saturn_house == 1
        phase = self.calculator.detect_sade_sati_phase(saturn_house)
        assert phase == SadeSatiPhase.PEAK

    def test_detect_setting_phase(self):
        """Saturn in 2nd from Moon should be Setting phase."""
        # Moon in Aries (0), Saturn in Taurus (1) = 2nd from Moon
        saturn_house = self.calculator.get_saturn_position_from_moon(1, 0)
        assert saturn_house == 2
        phase = self.calculator.detect_sade_sati_phase(saturn_house)
        assert phase == SadeSatiPhase.SETTING

    def test_no_sade_sati(self):
        """Saturn in other houses should return NONE."""
        # Moon in Aries (0), Saturn in Cancer (3) = 4th from Moon
        saturn_house = self.calculator.get_saturn_position_from_moon(3, 0)
        assert saturn_house == 4
        phase = self.calculator.detect_sade_sati_phase(saturn_house)
        assert phase == SadeSatiPhase.NONE

    def test_sade_sati_wrap_around(self):
        """Test phase detection with wrap-around (e.g., Moon in Pisces)."""
        # Moon in Pisces (11), Saturn in Aquarius (10) = 12th from Moon
        saturn_house = self.calculator.get_saturn_position_from_moon(10, 11)
        assert saturn_house == 12
        phase = self.calculator.detect_sade_sati_phase(saturn_house)
        assert phase == SadeSatiPhase.RISING


class TestDhaiyaDetection:
    """Test Dhaiya (Small Panoti) detection."""

    def setup_method(self):
        self.calculator = SadeSatiRashifalCalculator()

    def test_detect_kantak_shani(self):
        """Saturn in 4th from Moon should be Kantak Shani."""
        # Moon in Aries (0), Saturn in Cancer (3) = 4th from Moon
        saturn_house = self.calculator.get_saturn_position_from_moon(3, 0)
        assert saturn_house == 4
        dhaiya_type = self.calculator.detect_dhaiya_type(saturn_house)
        assert dhaiya_type == DhaiyaType.KANTAK

    def test_detect_ashtama_shani(self):
        """Saturn in 8th from Moon should be Ashtama Shani."""
        # Moon in Aries (0), Saturn in Scorpio (7) = 8th from Moon
        saturn_house = self.calculator.get_saturn_position_from_moon(7, 0)
        assert saturn_house == 8
        dhaiya_type = self.calculator.detect_dhaiya_type(saturn_house)
        assert dhaiya_type == DhaiyaType.ASHTAMA

    def test_no_dhaiya(self):
        """Saturn in other houses should return NONE."""
        # Moon in Aries (0), Saturn in Gemini (2) = 3rd from Moon
        saturn_house = self.calculator.get_saturn_position_from_moon(2, 0)
        assert saturn_house == 3
        dhaiya_type = self.calculator.detect_dhaiya_type(saturn_house)
        assert dhaiya_type == DhaiyaType.NONE


class TestScoreModifiers:
    """Test Rashifal score modifiers."""

    def setup_method(self):
        self.calculator = SadeSatiRashifalCalculator()

    def test_peak_phase_has_highest_negative_modifier(self):
        """Peak phase should have the most negative score modifier."""
        peak_modifier = SADE_SATI_PHASE_EFFECTS[SadeSatiPhase.PEAK]["score_modifier"]
        rising_modifier = SADE_SATI_PHASE_EFFECTS[SadeSatiPhase.RISING]["score_modifier"]
        setting_modifier = SADE_SATI_PHASE_EFFECTS[SadeSatiPhase.SETTING]["score_modifier"]

        assert peak_modifier < rising_modifier
        assert peak_modifier < setting_modifier
        assert peak_modifier == -2.5

    def test_dhaiya_modifiers_less_than_sade_sati(self):
        """Dhaiya should have less severe modifiers than Sade Sati peak."""
        peak_modifier = abs(SADE_SATI_PHASE_EFFECTS[SadeSatiPhase.PEAK]["score_modifier"])
        kantak_modifier = abs(DHAIYA_EFFECTS[DhaiyaType.KANTAK]["score_modifier"])
        ashtama_modifier = abs(DHAIYA_EFFECTS[DhaiyaType.ASHTAMA]["score_modifier"])

        assert kantak_modifier < peak_modifier
        assert ashtama_modifier < peak_modifier

    def test_ashtama_more_severe_than_kantak(self):
        """Ashtama Shani should be more severe than Kantak Shani."""
        kantak_modifier = abs(DHAIYA_EFFECTS[DhaiyaType.KANTAK]["score_modifier"])
        ashtama_modifier = abs(DHAIYA_EFFECTS[DhaiyaType.ASHTAMA]["score_modifier"])

        assert ashtama_modifier > kantak_modifier

    def test_modify_rashifal_score_clamps_to_range(self):
        """Score should be clamped between 1 and 10."""
        # Test lower bound
        analysis = self.calculator.get_complete_saturn_analysis(
            moon_rashi_num=0,
            saturn_rashi_num=0,  # Peak phase
            saturn_rashi="Mesha"
        )
        modified_score = self.calculator.modify_rashifal_score(2.0, analysis)
        assert modified_score >= 1.0

        # Test upper bound
        analysis_none = self.calculator.get_complete_saturn_analysis(
            moon_rashi_num=0,
            saturn_rashi_num=5,  # 6th from Moon - not afflicted
            saturn_rashi="Kanya"
        )
        modified_score_upper = self.calculator.modify_rashifal_score(10.0, analysis_none)
        assert modified_score_upper <= 10.0


class TestRemedialFactors:
    """Test remedial factor calculations."""

    def setup_method(self):
        self.calculator = SadeSatiRashifalCalculator()

    def test_yogakaraka_lagna_reduces_severity(self):
        """Saturn Yogakaraka lagna should reduce Sade Sati severity."""
        # Taurus lagna - Saturn is Yogakaraka
        analysis_with_yoga = self.calculator.get_complete_saturn_analysis(
            moon_rashi_num=0,
            saturn_rashi_num=0,  # Peak phase
            saturn_rashi="Mesha",
            lagna_rashi="Vrishabha"  # Saturn Yogakaraka
        )

        analysis_without = self.calculator.get_complete_saturn_analysis(
            moon_rashi_num=0,
            saturn_rashi_num=0,  # Peak phase
            saturn_rashi="Mesha",
            lagna_rashi="Simha"  # Not Yogakaraka
        )

        # With Yogakaraka should have less severe (closer to 0) modifier
        assert abs(analysis_with_yoga.total_score_modifier) < abs(analysis_without.total_score_modifier)

    def test_saturn_own_sign_reduces_severity(self):
        """Saturn in own sign should reduce Sade Sati effects."""
        # Moon in Capricorn, Saturn in Capricorn (own sign, peak phase)
        analysis_own = self.calculator.get_complete_saturn_analysis(
            moon_rashi_num=9,   # Capricorn
            saturn_rashi_num=9,  # Capricorn (own sign)
            saturn_rashi="Makara"
        )

        # Moon in Aries, Saturn in Aries (not own sign, peak phase)
        analysis_not_own = self.calculator.get_complete_saturn_analysis(
            moon_rashi_num=0,
            saturn_rashi_num=0,
            saturn_rashi="Mesha"
        )

        assert abs(analysis_own.total_score_modifier) < abs(analysis_not_own.total_score_modifier)

    def test_saturn_exalted_has_strong_reduction(self):
        """Saturn exalted in Libra should significantly reduce effects."""
        # Moon in Libra, Saturn in Libra (exalted, peak phase)
        analysis = self.calculator.get_complete_saturn_analysis(
            moon_rashi_num=6,
            saturn_rashi_num=6,
            saturn_rashi="Tula"  # Exalted
        )

        assert analysis.sade_sati is not None
        # Should have remedial factors applied
        assert len(analysis.sade_sati.remedial_factors) > 0
        # Check exalted factor is present
        factor_types = [f["type"] for f in analysis.sade_sati.remedial_factors]
        assert "saturn_exalted" in factor_types

    def test_saturn_debilitated_increases_severity(self):
        """Saturn debilitated in Aries should increase effects."""
        # Moon in Aries, Saturn in Aries (debilitated, peak phase)
        analysis = self.calculator.get_complete_saturn_analysis(
            moon_rashi_num=0,
            saturn_rashi_num=0,
            saturn_rashi="Mesha"  # Debilitated
        )

        assert analysis.sade_sati is not None
        # Check debilitated factor is present
        factor_types = [f["type"] for f in analysis.sade_sati.remedial_factors]
        assert "saturn_debilitated" in factor_types


class TestCompleteAnalysis:
    """Test complete Saturn transit analysis."""

    def setup_method(self):
        self.calculator = SadeSatiRashifalCalculator()

    def test_sade_sati_analysis_complete(self):
        """Test that Sade Sati analysis returns all required fields."""
        analysis = self.calculator.get_complete_saturn_analysis(
            moon_rashi_num=0,
            saturn_rashi_num=0,
            saturn_rashi="Mesha"
        )

        assert analysis.has_affliction is True
        assert analysis.sade_sati is not None
        assert analysis.dhaiya is None  # Sade Sati takes precedence
        assert analysis.total_score_modifier < 0
        assert len(analysis.remedies) > 0
        assert len(analysis.remedies_hindi) > 0

    def test_dhaiya_analysis_complete(self):
        """Test that Dhaiya analysis returns all required fields."""
        analysis = self.calculator.get_complete_saturn_analysis(
            moon_rashi_num=0,
            saturn_rashi_num=3,  # 4th from Moon - Kantak
            saturn_rashi="Karka"
        )

        assert analysis.has_affliction is True
        assert analysis.sade_sati is None
        assert analysis.dhaiya is not None
        assert analysis.dhaiya.dhaiya_type == DhaiyaType.KANTAK
        assert analysis.total_score_modifier < 0

    def test_no_affliction_analysis(self):
        """Test analysis when no affliction is present."""
        analysis = self.calculator.get_complete_saturn_analysis(
            moon_rashi_num=0,
            saturn_rashi_num=5,  # 6th from Moon - favorable
            saturn_rashi="Kanya"
        )

        assert analysis.has_affliction is False
        assert analysis.sade_sati is None
        assert analysis.dhaiya is None
        assert analysis.total_score_modifier == 0.0
        assert len(analysis.remedies) == 0


class TestHelperFunctions:
    """Test helper functions."""

    def test_check_sade_sati_for_moon_sign(self):
        """Test quick check function."""
        result = check_sade_sati_for_moon_sign(
            moon_rashi_num=0,
            saturn_rashi_num=0,
            saturn_rashi="Mesha"
        )

        assert result["has_affliction"] is True
        assert result["is_sade_sati"] is True
        assert result["sade_sati_phase"] == "peak"
        assert result["is_dhaiya"] is False
        assert result["score_modifier"] < 0
        assert "prediction_hindi" in result

    def test_get_sade_sati_affected_rashis(self):
        """Test getting all affected rashis for given Saturn position."""
        # Saturn in Aries (0)
        affected = get_sade_sati_affected_rashis(0)

        assert affected["rising"] == 1   # Taurus Moon - Saturn in 12th
        assert affected["peak"] == 0     # Aries Moon - Saturn over Moon
        assert affected["setting"] == 11  # Pisces Moon - Saturn in 2nd

    def test_get_dhaiya_affected_rashis(self):
        """Test getting Dhaiya affected rashis."""
        # Saturn in Cancer (3)
        affected = get_dhaiya_affected_rashis(3)

        assert affected["kantak"] == 0   # Aries Moon - Saturn in 4th
        assert affected["ashtama"] == 8  # Sagittarius Moon - Saturn in 8th (3-7=-4, +12=8)


class TestPredictionTexts:
    """Test prediction text generation."""

    def setup_method(self):
        self.calculator = SadeSatiRashifalCalculator()

    def test_sade_sati_has_prediction_text(self):
        """Sade Sati analysis should include prediction text."""
        analysis = self.calculator.get_complete_saturn_analysis(
            moon_rashi_num=0,
            saturn_rashi_num=0,
            saturn_rashi="Mesha"
        )

        assert analysis.sade_sati.prediction_text_hindi is not None
        assert len(analysis.sade_sati.prediction_text_hindi) > 0
        assert analysis.combined_prediction_hindi is not None

    def test_sade_sati_has_effects_list(self):
        """Sade Sati should have primary effects list."""
        analysis = self.calculator.get_complete_saturn_analysis(
            moon_rashi_num=0,
            saturn_rashi_num=0,
            saturn_rashi="Mesha"
        )

        assert len(analysis.sade_sati.primary_effects) > 0
        assert len(analysis.sade_sati.primary_effects_hindi) > 0
        assert len(analysis.sade_sati.affected_areas) > 0


class TestIntensityLevels:
    """Test intensity levels for different phases."""

    def test_peak_has_highest_intensity(self):
        """Peak phase should have intensity of 1.0."""
        assert SADE_SATI_PHASE_EFFECTS[SadeSatiPhase.PEAK]["intensity"] == 1.0

    def test_rising_and_setting_lower_intensity(self):
        """Rising and Setting phases should have lower intensity."""
        rising_intensity = SADE_SATI_PHASE_EFFECTS[SadeSatiPhase.RISING]["intensity"]
        setting_intensity = SADE_SATI_PHASE_EFFECTS[SadeSatiPhase.SETTING]["intensity"]

        assert rising_intensity < 1.0
        assert setting_intensity < 1.0

    def test_dhaiya_intensity_less_than_peak(self):
        """Dhaiya intensity should be less than Sade Sati peak."""
        peak_intensity = SADE_SATI_PHASE_EFFECTS[SadeSatiPhase.PEAK]["intensity"]
        kantak_intensity = DHAIYA_EFFECTS[DhaiyaType.KANTAK]["intensity"]
        ashtama_intensity = DHAIYA_EFFECTS[DhaiyaType.ASHTAMA]["intensity"]

        assert kantak_intensity < peak_intensity
        assert ashtama_intensity < peak_intensity


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
